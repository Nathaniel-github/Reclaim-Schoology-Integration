import schoolopy
import os
from dotenv import load_dotenv, find_dotenv
from reclaim_sdk.models.task import ReclaimTask
from reclaim_sdk.client import ReclaimClient
from datetime import datetime
from tqdm import tqdm

load_dotenv(find_dotenv())

key = os.getenv('KEY')
secret = os.getenv('SECRET')

reclaim_token = os.getenv('RECLAIM')

sc = schoolopy.Schoology(schoolopy.Auth(key, secret))

uid = sc.get_me()['uid']

ReclaimClient(token=reclaim_token)

all_tasks = ''.join([str(i) for i in ReclaimTask.search()])

for section in sc.get_user_sections(uid):
    course_name = section['course_title']
    for assignment in tqdm(sc.get_assignments(section['id'])):
        if assignment['due'] != '':
            due_date = datetime.strptime(assignment['due'], '%Y-%m-%d %H:%M:%S')
            task_name = f"{course_name}: {assignment['title']}"
            if due_date < datetime.now():
                continue
            if task_name in all_tasks:
                continue
            with ReclaimTask() as task:
                task.name = task_name
                # All durations are set in hours
                task.duration = 1
                task.min_work_duration = 0.75
                task.max_work_duration = 2
                task.start_date = datetime.now()
                task.due_date = due_date
                task.save()
