class RunDTO:
    def __init__(self, runName=None, projectCode=None):
        self.runName = runName
        self.projectCode = projectCode

    def set_run_name(self, runName):
        self.runName = runName

    def get_run_name(self):
        return self.runName

    def set_project_code(self, projectCode):
        self.projectCode = projectCode

    def get_project_code(self):
        return self.projectCode