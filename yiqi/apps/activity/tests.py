from django.test import TestCase

# Create your tests here.
import datetime
now = datetime.datetime.now()
start = now - datetime.timedelta(hours=23, minutes=59, seconds=59)


print(now > start)

print(now)

print(start)