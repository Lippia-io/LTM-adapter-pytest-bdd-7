class StepDTO:
    def __init__(self, title=None, description=None, base64_image=None, status=None):
        self.title = title
        self.description = description
        self.base64_image = base64_image
        self.status = status

    def set_title(self, title):
        self.title = title

    def get_title(self):
        return self.title

    def set_description(self, description):
        self.description = description

    def get_description(self):
        return self.description

    def set_base64_image(self, base64_image):
        self.base64_image = base64_image

    def get_base64_image(self):
        return self.base64_image

    def set_status(self, status):
        self.status = status

    def get_status(self):
        return self.status


    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "base64_image": self.base64_image,
            "status": self.status
        }
