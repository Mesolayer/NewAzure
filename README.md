This is the final website for the Fibre Optic Strain Visualisation, Integration and Scalability project.

For non-experienced Django users, a link has been provided for your basic Django understanding: https://www.youtube.com/watch?v=UmljXZIypDc&t=609s

Description: Basic Django python project skeleton was used, and adjusted for Azure deployment. With a Django backend, the main settings files are located in the timetabler folder, and the download requirements are set in the requirements.txt file. 

The website is created mainly to show the Homepage and the Dashboard

Base: The base.html file contains the basic html featurettes using the bootstrap framework. The top navigation bar has been created here to be extended in all corresponding webpages.

Css: The css stylings are all located in the base.css file. It contains classes that were manually created, and classes used to alter the bootstrap frameworks used.

Homepage: The homepage is created in the home.html file. It extends from the base.html, and features the descriptions, images and the location of the ETP building.

Dashboard: The dashboard is created in the dashboard.html file. It also extends from the base.html, and features the grafana data visuals along with their descriptions. The visuals are embedded in the html using iframes, so any future additions in any visuals can simply be embedded using iframe classes.
 
Database: dbsqlite3 is being used. It can be changed to postgresql, for better performance. But the database currently has no use, as the data is being taken from the grafana visual embeddings, so now data is being stored in the WebApp resource itself.

How to locally run the website:
      python3 manage.py runserver
