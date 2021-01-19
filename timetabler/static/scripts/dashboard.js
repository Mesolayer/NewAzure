// Function that allows a user to click outside of a popup to close it
$(document).click(function (e) {
    var $target = $(e.target);
    if (($target.hasClass('btn')) || ($target.parents('div').hasClass('popup'))) {
        return;
    } else {
        $('.popup').fadeOut();
    }
});

//Function To Display Popup
function div_show(task) {
    my_task = task;
    // assign information to HTML elements
    document.getElementById('detailBoxWhole').style.display = "block";
    var title = document.getElementById('title');
    title.innerText = "Title: " + task.title;
    var start = document.getElementById('start_time');
    start.innerText = "Start time: " + task.start;
    var end = document.getElementById('end_time');
    end.innerText = "End time: " + task.end;

}

//Function to Hide Popup
function div_hide() {
    document.getElementById('detailBoxWhole').style.display = "none";
}

$(function () {
    $("#start_time_date").datetimepicker({
        format: 'Y-m-d H:i:s',
    });
    $("#end_time_date").datetimepicker({
        format: 'Y-m-d H:i:s',
    });
    $("#reminder_time_date").datetimepicker({
        format: 'Y-m-d H:i:s',
    })
    $("#start_time_date_editing").datetimepicker({
        format: 'Y-m-d H:i:s',
    });
    $("#end_time_date_editing").datetimepicker({
        format: 'Y-m-d H:i:s',
    });
    $("#reminder_time_date_editing").datetimepicker({
        format: 'Y-m-d H:i:s',
    })
});

// Fade element in/out
function toggle(id) {
    $('#' + id).fadeIn();
};

//Hide Popup of the whole detail box
function detail_hide() {
    flag = true;
    document.getElementById('detailBoxWhole').style.display = "none";
    stop_clock();
    reset_clock();
};

// Show the editing task panel

$(function () {
    $("#start_time").datetimepicker({
        format: 'Y-m-d H:i:s',
    });
    $("#end_time").datetimepicker({
        format: 'Y-m-d H:i:s',
    });
});
var n = 0, timer = null;

//start timer
function start_clock() {
    var oTxt = document.getElementById("clock");
    clearInterval(timer);
    timer = setInterval(function () {
        n++;
        var h = parseInt(n / 3600);
        if ((n / 60) > 60) {
            var m = parseInt(n / 60) - 60 * h;
        } else {
            var m = parseInt(n / 60);
        }
        var s = parseInt(n % 60);
        oTxt.value = toDub(h) + ":" + toDub(m);
    }, 1000 / 60);
};

//pause
function stop_clock() {
    clearInterval(timer);
};

//reset
function reset_clock() {
    stop_clock();
    var oTxt = document.getElementById("clock");
    oTxt.value = "00:00";
    n = 0;
};

//add zero
function toDub(n) {
    return n < 10 ? "0" + n : "" + n;
};

function clock_show() {
    var myDate = new Date();
    document.getElementById('buttons_detail').style.display = "none";
    document.getElementById('popupClock').style.display = "block";
    document.getElementById('start_time_clock').innerText = "STARTED AT: " + myDate.toLocaleString()
};