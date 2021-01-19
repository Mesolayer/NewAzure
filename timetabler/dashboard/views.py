from django.http import HttpResponse, JsonResponse
import json
from datetime import date, datetime
# import datetime
from django.db import models
from django.urls import reverse_lazy

from django.contrib.auth.models import User
from engine.models import Task, Tag, UserData
from django.contrib.auth.decorators import login_required

from django.db.models.signals import post_save
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.timezone import make_aware


@login_required(login_url=reverse_lazy('login'))
def daily_dashboard(request):
    user = request.user
    # Only display tasks belonging to the signed in user
    user_tasks = Task.objects.filter(user=user)

    # Get all of a user's tasks' tags
    user_tags = Tag.objects.filter(user=user)

    # if filters applied then get parameter and filter based on condition else return object

    context = {
        'title': 'daily dashboard',
        'tasks': user_tasks,
        'tags': user_tags,
    }

    return render(request, 'html/dashboard/dashboardwithFullCalenar.html', context)


@login_required(login_url=reverse_lazy('login'))
def dashboard_filter_tags(request):
    tag_id = request.GET.get("id")
    user_id = request.user.pk

    if tag_id == "clear":
        tasks = list(Task.objects.filter(user=user_id))
    else:
        tasks = list(Tag.objects.get(pk=tag_id).tasks.filter(user=user_id))

    # Courtesy of https://stackoverflow.com/questions/39902405/fullcalendar-in-django
    response = []
    for i in tasks:
        res_sub = {}
        res_sub["title"] = i.name
        res_sub['start'] = i.start_time_date.strftime("%Y-%m-%dT%H:%M:%S")
        res_sub['end'] = i.end_time_date.strftime("%Y-%m-%dT%H:%M:%S")
        res_sub['id'] = i.pk
        response.append(res_sub)

    return HttpResponse(json.dumps(response))


@login_required(login_url=reverse_lazy('login'))
def dashboard_show_details(request):
    task_id = request.GET.get("id")
    # load the corresponding tasks from db
    task = Task.objects.get(id=task_id)
    response = []
    # put the needed data into a dictionary for further transit
    task_details = {}
    task_details["name"] = task.name
    task_details["comments"] = task.comments
    task_details["start"] = task.start_time_date.strftime("%Y-%m-%dT%H:%M:%S")
    task_details["end"] = task.end_time_date.strftime("%Y-%m-%dT%H:%M:%S")
    task_details["recurring"] = task.is_recurring

    # try load the reminder time since there could be none for this variable
    try:
        task_details["notification"] = task.reminder_time_date.strftime("%Y-%m-%dT%H:%M:%S")
    except:
        task_details["notification"] = "You have not set yet"

    response.append(task_details)
    return HttpResponse(json.dumps(response))


# Arbitrary XP calculation function based on task duration in hours. 1hr = 10XP
def calculate_xp(diff):
    return diff * 10


@login_required(login_url=reverse_lazy('login'))
def create_task(request):
    context = {}
    if request.method == 'POST':
        if request.POST.get('is_recurring') == None:
            recur = False
        elif request.POST.get('is_recurring') == "on":
            recur = True
        else:
            recur = False

        reminder = None

        # Allow empty reminders
        if not request.POST.get('reminder_time_date') == '':
            reminder = make_aware(datetime.strptime(request.POST.get('reminder_time_date'), "%Y-%m-%d %H:%M:%S"))

        # Attempt to convert date time strings to datetime objects
        try:
            start_time = make_aware(datetime.strptime(request.POST.get('start_time_date'), "%Y-%m-%d %H:%M:%S"))
            end_time = make_aware(datetime.strptime(request.POST.get('end_time_date'), "%Y-%m-%d %H:%M:%S"))
            diff = end_time - start_time
            diff = diff.total_seconds() / 3600
        except:
            return redirect(reverse_lazy("daily-dashboard"))

        if diff < 0:
            diff = 0

        xp = calculate_xp(diff)

        # Create new task object and save to DB
        task = Task(user=request.user, name=request.POST.get('name'),
                    start_time_date=start_time, end_time_date=end_time,
                    xp_amount_awarded=xp, is_recurring=recur,
                    comments=request.POST.get('comments'), is_completed=False,
                    reminder_time_date=reminder)
        task.save()
    else:
        form = CreateTaskForm()

    return redirect(reverse_lazy("daily-dashboard"))


@login_required(login_url=reverse_lazy('login'))
def assign_tag(request):
    tag_id = request.GET.get("tag_id")
    task_id = request.GET.get("task_id")

    # Make sure both tag and task exist
    try:
        tag = Tag.objects.get(pk=tag_id)
        task = Task.objects.get(pk=task_id)
    except:
        return HttpResponse(status=412)

    # Make sure the user actually owns the task
    if request.user == task.user:
        tag.tasks.add(task)
        return HttpResponse(status=200)

    else:
        # Unauthorized status
        return HttpResponse(status=401)


@login_required(login_url=reverse_lazy('login'))
def create_tag(request):
    tag = Tag(user=request.user, name=request.POST.get('name'))
    tag.save()
    return redirect(reverse_lazy("daily-dashboard"))


@login_required(login_url=reverse_lazy('login'))
def complete_task(request):
    task_id = request.POST.get("id")
    user_data = UserData.objects.get(user=request.user)

    try:
        # Prevent task farming
        if not Task.objects.get(pk=task_id).is_completed:
            user_data.tasks_completed = user_data.tasks_completed + 1
            task = Task.objects.get(pk=task_id)

            # calculate the time studied and record
            start_time = task.start_time_date
            end_time = task.end_time_date
            diff = end_time - start_time
            diff = diff.total_seconds() / 3600
            user_data.time_studied = user_data.time_studied + diff

            user_data.save()

        Task.objects.filter(id=task_id).filter(user=request.user).update(is_completed=True)
        return redirect(reverse_lazy("daily-dashboard"))
    except Exception as e:
        print(e)
        return redirect(reverse_lazy("daily-dashboard"))


@login_required(login_url=reverse_lazy('login'))
def update_task(request):
    if request.method == 'POST':
        id = request.POST.get('id_editing')
        original_task = Task.objects.get(id=id)

        # Prevent users from editing tasks they don't own
        if request.user != original_task.user:
            return redirect(reverse_lazy("daily-dashboard"))

        # load the original information of the task edited
        name = original_task.name
        comments = original_task.comments
        start_time = original_task.start_time_date
        end_time = original_task.end_time_date
        reminder = original_task.reminder_time_date
        recur = original_task.is_recurring

        # update the information of the task which are changed
        if not request.POST.get('start_time_date_editing') == "":
            start_time = make_aware(datetime.strptime(request.POST.get('start_time_date_editing'), "%Y-%m-%d %H:%M:%S"))
        if not request.POST.get('end_time_date_editing') == "":
            end_time = make_aware(datetime.strptime(request.POST.get('end_time_date_editing'), "%Y-%m-%d %H:%M:%S"))
        if not request.POST.get('name_editing') == "":
            name = request.POST.get('name_editing')
        if not request.POST.get('comments_editing') == "":
            comments = request.POST.get('comments_editing')

        if request.POST.get('is_recurring_editing') == None:
            recur = False
        elif request.POST.get('is_recurring_editing') == "on":
            recur = True
        else:
            recur = False

        if not request.POST.get('reminder_time_date_editing') == '':
            reminder = make_aware(
                datetime.strptime(request.POST.get('reminder_time_date_editing'), "%Y-%m-%d %H:%M:%S"))

        # save the updated task
        Task.objects.filter(id=id).update(name=name,
                                          start_time_date=start_time, end_time_date=end_time,
                                          is_recurring=recur,
                                          comments=comments,
                                          reminder_time_date=reminder)

    else:
        pass

    return redirect(reverse_lazy("daily-dashboard"))

# delete the chosen task
@login_required(login_url=reverse_lazy('login'))
def delete_task(request):
    task_id = request.POST.get("id")
    try:
        # Make sure the requesting user actually owns the task
        if Task.objects.get(id=task_id).user == request.user:
            Task.objects.filter(id=task_id).delete()
    except Exception as e:
        print(e)
    return JsonResponse({
        'url': reverse_lazy("daily-dashboard"),
    })
