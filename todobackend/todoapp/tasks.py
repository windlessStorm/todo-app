from __future__ import absolute_import, unicode_literals
from celery.task import task
import requests
from datetime import date, timedelta


@task()
def deletion_task():
	print("here")
	today = date.today()
	check_date = today - timedelta(days=0)
	url = "http://localhost:8000/api/v1/delete/?delete_time__gt=" + check_date.strftime('%Y-%m-%d')
	print(url)
	res = requests.delete(url)
	print(res)