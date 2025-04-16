import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meiaribe.meiari_v1')
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and available on your PYTHONPATH?"
        )
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
