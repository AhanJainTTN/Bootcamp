Django Setup

Create the root directory which houses the project. This is where the manage.py file resides. [Docs] This directory name doesn’t matter to Django; we can rename it to anything we like.

$ mkdir <directory-name>

This command creates the actual project directory and starting structure.

$ django-admin startproject <project-name> <directory>

This will create a project called <project-name> inside the <directory>.

Start the server.

Run inside the root directory i.e. the one which holds manage.py.

(Root Directory: One which holds manage.py)
(Project Directory: Holds config files for the project like asgi.py, settings.py, urls.py)

Run server: $ python manage.py runserver

Create an app: $ python manage.py startapp polls