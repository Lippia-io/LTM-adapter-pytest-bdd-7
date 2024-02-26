from typing import List

from adapterPytest.src.main.pytest.ltm.models.runs.request.StepDTO import StepDTO


class TestDTO:
    def __init__(
        self,
        title: str = None,
        run_id: str = None,
        status: str = None,
        feature: str = None,
        type: str = None,
        tags: List[str] = None,
        steps: List[StepDTO] = None,
    ):
        self.title = title
        self.run_id = run_id
        self.status = status
        self.feature = feature
        self.type = type
        self.tags = tags if tags else []
        self.steps = steps if steps else []

    def set_title(self, title: str) -> None:
        self.title = title

    def to_dict(self):
        return {
            "title": self.title,
            "run_id": self.run_id,
            "status": self.status,
            "feature": self.feature,
            "type": self.type,
            "tags": self.tags,
            "steps": [step.to_dict() for step in self.steps]
        }


    def get_title(self) -> str:
        return self.title

    def set_run_id(self, run_id: str) -> None:
        self.run_id = run_id

    def get_run_id(self) -> str:
        return self.run_id

    def set_status(self, status: str) -> None:
        self.status = status

    def get_status(self) -> str:
        return self.status

    def set_feature(self, feature: str) -> None:
        self.feature = feature

    def get_feature(self) -> str:
        return self.feature

    def set_type(self, type: str) -> None:
        self.type = type

    def get_type(self) -> str:
        return self.type

    def add_tag(self, tag: str) -> None:
        self.tags.append(tag)

    def get_tags(self) -> List[str]:
        return self.tags

    def add_step(self, step: StepDTO) -> None:
        self.steps.append(step)

    def get_steps(self) -> List[StepDTO]:
        return self.steps