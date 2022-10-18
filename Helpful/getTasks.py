from todoist_api_python.api import TodoistAPI

api = TodoistAPI("d33dd92fc3f7ccc8aebea5f02b802ae44e532e05")


def getProjectObject(name):
    # DEFINE PROJECTS
    projects = api.get_projects()

    # DEFINE THE PROJECT NAME
    return next((project for project in projects if project.name == name), None)


try:

    project = getProjectObject("Fall 2022")
    print("Project:", project.name)
    print("Project ID:", project.id)

    # OBJECT OF SECTIONS
    sections = [section for section in api.get_sections(
    ) if section.project_id == project.id]
    # print("Sections:\n\t", sections)

    print("Sections:")
    print('\n'.join([("\t" + str(section.id) + " - " + section.name)
          for section in sections]))

    # DEFINE SECTION OBJECT
    sectionDict = {}
    for section in sections:
        sectionDict[section.name] = section.id

    print(sectionDict)

except Exception as error:
    print(error)
