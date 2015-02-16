#!/bin/bash

case $1 in \
    0)
        export SELENIUM_BROWSER=chrome
        testproject/manage.py test testproject.tests --noinput
        ;;
    1)
        export SELENIUM_BROWSER=firefox
        testproject/manage.py test testproject.tests --noinput
        ;;
esac
