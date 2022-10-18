"""
Author: Srilokh Karuturi
Date: Thu Feb 24 2022
File: Task.py
Purpose: STASK objects which will interact with TODOSIT
License: MIT
"""

import secrets
# imports
from pydoc import classname

from todoist_api_python.api import TodoistAPI

# GLOBAL LIST TO KEEP TRACK OF ALL TASKS
global tasks
tasks = []

# ALLOW TO CREATE A TASK OBJECT
global projectID
projectID = 2296933858

global section
# SECTION ID
section = {'CS 4349.005': 98125039, 'CS 4348.502': 98125066, 'CS 4347.002': 98125081,
           'CS 4341.001': 98125101, 'CS 4141.605': 101884086, 'Other': 100648096}


api = TodoistAPI(secrets.TODOIST_API_KEY)


class Task():
    # CONSTRUCTOR TAKES TITLE, DUE DATE, CLASS NAME
    def __init__(self, title, due, className):
        # DEFINE TITLE
        self.content = title

        # DEFINE DUE TIME
        self.due = due

        # DEFINE CLASS NAME / SECTIONNAME
        self.className = className

        self.exists = Task.checkIfExists(className, due, projectID)

        print("Processing: %s %s %s %s %s" %
              (self.content, self.due, self.className, self.exists))
    # remove is a static function that will remove all element

    # 1. MAKE EVERYTHING WE NEED
    # - Make Project
    # - Make Sections
    # - STORE PROJECTS AND SECTIONS
    # 2. IF THEY ALREADY HAVE A PROJECT READY
    # - Specify the project name
    # - MAKE SURE YOUR FULL CLASS NAME AND NUMBER IS IN THE SECTIONS OTHER WISE OUR BOT IS GONNA CREATE A NEW ONE
    # def preCheck():
    #     pass

    # ADD TODOIST IF PROJECT AND SECTIONS ARE READY
    def add(self):
        print("Adding: ")
        try:
            print(self.title)
            # SET API KEY

            # TASK OBJECT
            taskJSON = {
                "content": self.title,
                "due_string": self.due,
                "due_lang": 'en',
                "priority": 4,
                "description": "todobot",
                "project_id": projectID,
                "section_id": section[self.className]
            }

            # CHECK FOR DUPLICATE
            if not Task.checkIfExists():
                # ADD TASK JSON
                task = api.add_task(
                    taskJSON
                )

                # APPEND THE TASK ID
                tasks.append(task.id)

        except Exception as error:
            # PRINT ERROR JUST IN CASE
            print(error)

    '''
    @attr.s
    class Task(object):
        comment_count: int = attr.ib()
        completed: bool = attr.ib()
        content: str = attr.ib()
        created: str = attr.ib()
        creator: int = attr.ib()
        description: str = attr.ib()
        id: int = attr.ib()
        project_id: int = attr.ib()
        section_id: int = attr.ib()
        priority: int = attr.ib()
        url: str = attr.ib()
        assignee: Optional[int] = attr.ib(default=None)
        assigner: Optional[int] = attr.ib(default=None)
        due: Optional[Due] = attr.ib(default=None)
        label_ids: Optional[List[int]] = attr.ib(default=None)
        order: Optional[int] = attr.ib(default=None)
        parent_id: Optional[int] = attr.ib(default=None)
        sync_id: Optional[int] = attr.ib(default=None)
    '''

    def checkIfExists(className: str, dueDate: str, projectID: str) -> bool:
        # DEFINE INITIAL VARIABLES
        # DEFINE SECTION
        section_id = className

        # DEFINE PROJECT
        project_id = projectID

        # DEFINE DUE DATE
        due_date = dueDate

        # GET ALL SECTION TASkS
        existingTasks = api.get_tasks(
            project_id=project_id, section_id=section_id)

        # CHECK TO SEE IF ANY OF THE TASK OBJECTS HAVE THESE SAID PROPERTIES ALREADY
        for task in existingTasks:
            if task.completed:
                return True
            if task.content == self.content and (task.due == self.due):
                return True

        return False

    def removeAllTasks():
        try:
            # SET API KEY

            # GO THROUGH EACH ELEMENT
            for element in tasks:
                # delete task
                task = api.delete_task(task_id=element)
        except Exception as error:
            print(error)

    # PRINT TASKS
    def printTasks():
        print(tasks)
