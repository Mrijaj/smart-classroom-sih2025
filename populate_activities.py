import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from activities.models import Activity

def run():
    tasks = [
        # DSA Tasks
        {
            'title': 'Solve Two Sum on LeetCode',
            'category': 'dsa',
            'time': 30,
            'link': 'https://leetcode.com/problems/two-sum/'
        },
        {
            'title': 'Understand Big O Notation',
            'category': 'dsa',
            'time': 45,
            'link': 'https://www.geeksforgeeks.org/analysis-of-algorithms-set-1-asymptotic-analysis/'
        },

        # Development / Python Tasks
        {
            'title': 'Vibe Coding: Build a Flask API',
            'category': 'dev',
            'time': 60,
            'link': 'https://flask.palletsprojects.com/'
        },
        {
            'title': 'Master Python Decorators',
            'category': 'dev',
            'time': 20,
            'link': 'https://realpython.com/primer-on-python-decorators/'
        },

        # Astronomy Tasks
        {
            'title': 'Track the James Webb Telescope',
            'category': 'ast',
            'time': 15,
            'link': 'https://webb.nasa.gov/content/webbLaunch/whereIsWebb.html'
        },
        {
            'title': 'Identify Constellations tonight',
            'category': 'ast',
            'time': 30,
            'link': 'https://stellarium-web.org/'
        },
    ]

    print("Populating activities...")
    for task in tasks:
        # Using get_or_create ensures no duplicates if you run the script twice
        activity, created = Activity.objects.get_or_create(
            title=task['title'],
            category=task['category'],
            defaults={
                'estimated_time': task['time'],
                'external_link': task['link'],
                'description': f"A structured {task['category']} task to maximize your free period productivity."
            }
        )
        if created:
            print(f" - Created: {task['title']}")
        else:
            print(f" - Already exists: {task['title']}")

    print("\nSuccessfully populated smart activities!")

if __name__ == '__main__':
    run()