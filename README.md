drScratch
=========

drScratch is an analytical tool that evaluates your Scratch projects in a variety of computational areas to provide feedback on aspects such as abstraction, logical thinking, synchronization, parallelization, flow control, user interactivity and data representation. This analyzer is a helpful tool to evaluate your own projects, or those of your Scratch students.

You can try an online version of drScratch at http://drscratch.programamos.es

Installation
============

* Clone this repo
* Edit drScratch/settings.py for
  * ALLOWED HOSTS (leave empty if trying out in your box)
  * DATABASES (use 'ENGINE': 'django.db.backends.sqlite3', and 'NAME': "db" for instance)
* Run python manage.py syncdb
* Run python manage.py runserver (to have it running on http://localhost:8080/)

Dependencies
============

* Python
* Django
* kurt python module
