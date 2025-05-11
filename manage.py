#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from django.core.management import call_command
from django.core.wsgi import get_wsgi_application


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'budget_buddy.settings')
    try:
        from django.core.management import execute_from_command_line
        #1
        # sys.argv = ['manage.py', 'runserver', 'localhost:8000']
        # execute_from_command_line(sys.argv)
        #2
        # get_wsgi_application()
        # call_command('runserver', 'localhost:8000')
        execute_from_command_line(sys.argv)
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc



if __name__ == '__main__':
    main()
