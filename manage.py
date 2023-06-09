# -*- coding: utf-8 -*-
import sys
import os 


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neoxam.settings')
    os.environ.setdefault('DJANGO_CONFIGURATION', 'Development')
    from configurations.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
