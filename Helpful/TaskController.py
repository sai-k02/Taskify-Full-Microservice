"""
Author: Srilokh Karuturi
Date: Thu Feb 24 2022
File: TaskBot.py
Purpose: Parse JSON FILE ... create Task objects .. add to TODoIst
License: MIT
"""
import argparse
import json
import os
import sys
import time

import dateutil
import dateutil.parser
import pandas
from dateutil import tz

from TaskObject import Task

# TASK BOT CLASSIFICATION


class TaskController():

    # MAIN
    @staticmethod
    def main():
        # SET UP PARSER
        parser = argparse.ArgumentParser(
            description='TASK BOT WILL POPULATE TODOIST WITH USERS CURRENT TASKS')

        # ADD ARGUMENT TO TAKE IN A INTEGER
        parser.add_argument('integer', metavar='N', type=int, nargs=1,
                            help='0 = TEST, 1 = NORMAL')

        # RETRIEVE ARGS
        args = parser.parse_args()

        # CONVERT INTO DICTIONARY
        args = args.__dict__

        # DEFINE USER PREFERENCE
        USERPREF = args["integer"][0]

        # DEFINE FILE
        f = open("output.json")

        # LOAD INTO A JSON OBJECT
        jsonObject = json.load(f)

        # GO INTO RESULTS
        jsonObject = jsonObject["results"]

        # PANDAS
        tasksFound = {
            "Class": [],
            "Assignment": [],
            "Due": []
        }

        # GO THROUGH EACH ELEMENT IN RESULTS
        for element in jsonObject:
            # GO THROUGH EACH OBJECT OF RESULTS
            for inner in element:
                # WHEN WE COME ACROSS CALENDAR NAME ... DEFINE CLASSNAME
                if(inner == "calendarName"):
                    # GET CLASSNAME RAW
                    ClassNameRaw = str(element[inner])
                    # GET UP TO FIRST COLON
                    ClassNameRaw = ClassNameRaw[ClassNameRaw.find(":"):]
                    # DEFINE CLASSNAME
                    className = ClassNameRaw[(1):(
                        ClassNameRaw.find("-"))].strip()
                # WHEN WE COME ACROSS TITLE DEFINE ASSIGNMENTTITLE
                if(inner == "title"):
                    assignmentTitle = element[inner]
                # WHEN WE COME ACROSS END DEFINE END
                if(inner == "end"):
                    endDate = element[inner]
                    endDate = dateutil.parser.parse(endDate)
                    endDate = endDate.astimezone(tz.gettz("America/Texas"))
                    endDate = str(endDate)[0:16]

                    # DEFINE TASK AND ADD
                    t = Task(assignmentTitle, endDate, className)
                    t.add()

                    # ADD TO OUR LOCAL LIST FOR EASY PRINTING
                    tasksFound["Class"].append(className)
                    tasksFound["Assignment"].append(assignmentTitle)
                    tasksFound["Due"].append(endDate)

        # PRINT PANDAS DATAFRAME
        print((pandas.DataFrame(tasksFound)).to_markdown(index=False))

        # SLEEP
        time.sleep(30)

        if(USERPREF == 0):
            Task.removeAllTasks()


TaskController.main()
