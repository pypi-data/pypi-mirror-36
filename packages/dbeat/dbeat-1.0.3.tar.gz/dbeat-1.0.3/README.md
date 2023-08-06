# Database-backed Periodic Tasks

name|value
-|-
Version| 1.0.0
Download| http://pypi.python.org/pypi/dbeat
Source|http://github.com/aohan237/dbeat
Keywords|peewee, celery, beat, periodic task, cron, scheduling

# Why this module

maybe your proj admin based on django.(django-celery-beat is enough)
but if your apps or proj not based on django, then django orm is hard to use.
then this is the module's purpose

# Using the Extension

## install the module
    python setup.py install

## initial database in celery app
    from peewee import SqliteDatabase
    database = SqliteDatabase('app.db')
    app.database = database

## start the beat

    celery -A proj beat -l info --scheduler dbeat.schedulers:DatabaseScheduler