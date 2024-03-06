class RunDTO:
    def __init__(self, runName=None, projectCode=None, repositoryUrl=None, repositoryBranch=None):
        self.runName = runName
        self.projectCode = projectCode
        self.repositoryUrl = repositoryUrl
        self.repositoryBranch = repositoryBranch

    def set_run_name(self, runName):
        self.runName = runName

    def get_run_name(self):
        return self.runName

    def set_project_code(self, projectCode):
        self.projectCode = projectCode

    def get_project_code(self):
        return self.projectCode

    def set_repository_url(self, repositoryUrl):
        self.repositoryUrl = repositoryUrl

    def get_repository_url(self):
        return self.repositoryUrl

    def set_repository_branch(self, repositoryBranch):
        self.repositoryBranch = repositoryBranch

    def get_repository_branch(self):
        return self.repositoryBranch

    def to_dict(self):
        return {
            "runName": self.runName,
            "projectCode": self.projectCode,
            "repositoryUrl": self.repositoryUrl,
            "repositoryBranch": self.repositoryBranch
        }
