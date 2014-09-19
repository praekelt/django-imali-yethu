#!/bin/sh
export DATABASE_URL="sqlite://:memory:"
export DJANGO_SETTINGS_MODULE="imaliyethu.testsettings"
./manage.py test
