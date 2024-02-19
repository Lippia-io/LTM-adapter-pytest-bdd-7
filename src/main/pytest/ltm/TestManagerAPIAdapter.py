import self
from pytest_bdd import given, when, then, parsers
from threading import local
from collections import deque

from pytest_bdd.reporting import after_step

from src.main.pytest.ltm.TestManagerAPIClient import TestManagerAPIClient
from src.main.pytest.ltm.models.runs.request.StepDTO import StepDTO
from src.main.pytest.ltm.models.runs.request.TestDTO import TestDTO
from src.main.pytest.ltm.screenshots import SSConfig, Strategy


class TestManagerAPIAdapter:
    runResponseDTO = None
    currentFeatureFile = local()
    screenshotConfig = None
    steps = local()

    def __init__(self):
        self.screenshotConfig = SSConfig.load()
        self.runResponseDTO = TestManagerAPIClient.create_run()
        self.steps = local()

    def pytest_bdd_after_scenario(request, feature, scenario):
        title = scenario.name
        status = "failed" if scenario.failed else "passed"
        status = status.upper()[:len(status) - 2]
        feature_name = feature.name
        test = TestDTO(title, request.runResponseDTO.get_id(), status, feature_name, "SCENARIO", scenario.tags, self.steps.get())
        TestManagerAPIClient.createTest(test)
        self.clean_steps()

    @after_step
    def pytest_bdd_after_step(request, feature, scenario, step, step_func, step_func_args):
        step_text = self.get_step_text(step)
        status = step_func.status
        status = status.upper()[:len(status) - 2]
        base64_image = None
        stack_trace = None
        if self.steps.get() is None:
            self.steps.set(deque())
        if self.screenshotConfig.contains(Strategy.ON_EACH_STEP):
            base64_image = self.get_base64_image()
        elif self.screenshotConfig.contains(Strategy.ON_FAILURE) and status == "FAILED":
            base64_image = self.get_base64_image()
            stack_trace = self.truncate(step_func_args.result.error.message, 5)
        self.steps.get().append(StepDTO(step_text, stack_trace, base64_image, status))

    def get_step_text(self, step):
        step_text_builder = ""
        step_text_builder += step.prefix + " "
        step_text_builder += step.name
        if step.doc_string is not None:
            step_text_builder += step.doc_string
        return step_text_builder

    def clean_steps(self):
        if self.steps.get() is not None:
            self.steps.remove()

    @staticmethod
    def truncate(str, length):
        if len(str) <= length:
            return str[:length]
        return str

    def get_base64_image(self):
        pass