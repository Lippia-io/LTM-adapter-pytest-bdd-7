from collections import deque
import threading

import pytest

from adapterPytest.src.main.pytest.ltm.TestManagerAPIClient import TestManagerAPIClient
from adapterPytest.src.main.pytest.ltm.models.runs.request.StepDTO import StepDTO
from adapterPytest.src.main.pytest.ltm.models.runs.request.TestDTO import TestDTO
from adapterPytest.src.main.pytest.ltm.screenshots.SSConfig import SSConfig
from adapterPytest.src.main.pytest.ltm.screenshots.Strategy import Strategy


class TestManagerAPIAdapter:
    runResponseDTO = None
    steps = deque()

    def __init__(self):
        self.screenshotConfig = SSConfig.load()
     #   self.runResponseDTO = TestManagerAPIClient.create_run()

    @staticmethod
    def pytest_bdd_after_scenario(feature, scenario):
        if TestManagerAPIAdapter.runResponseDTO is None:
            TestManagerAPIAdapter.runResponseDTO = TestManagerAPIClient.create_run()
        title = scenario.name
        status = "passed"
        for step in TestManagerAPIAdapter.steps:
            if step.status == "FAIL":
                status = "failed"
                break
        status = status.upper()[:len(status) - 2]
        feature_name = feature.name
        test = TestDTO(title, TestManagerAPIAdapter.runResponseDTO.get_id(), status, feature_name, "SCENARIO", scenario.tags,TestManagerAPIAdapter.steps)
        TestManagerAPIClient.create_test(test)
        TestManagerAPIAdapter.clean_steps()

    @staticmethod
    def pytest_bdd_after_step(step,step_func_args):
        step_text = TestManagerAPIAdapter.get_step_text(step)
        status= "failed" if step.failed else "passed"
        status = status.upper()[:len(status) - 2]
        base64_image = None
        stack_trace = None
        if TestManagerAPIAdapter.steps is None:
            TestManagerAPIAdapter.steps = deque()
        screenshot_config = SSConfig.load()
        if screenshot_config.contains(Strategy.ON_EACH_STEP):
            base64_image = TestManagerAPIAdapter.get_base64_image()
        elif step.failed and status == "FAIL":
            base64_image = TestManagerAPIAdapter.get_base64_image()
            stack_trace = TestManagerAPIAdapter.truncate(step_func_args.result.error.message, 5)

        step_info = StepDTO(step_text, stack_trace, base64_image, status)
        TestManagerAPIAdapter.steps.append(step_info)


    @staticmethod
    def pytest_bdd_step_error(step, exception):
        step_text = TestManagerAPIAdapter.get_step_text(step)
        status = "failed"
        status = status.upper()[:len(status) - 2]
        base64_image = None
        stack_trace = None
        if TestManagerAPIAdapter.steps is None:
            TestManagerAPIAdapter.steps = deque()
        screenshot_config = SSConfig.load()
        if screenshot_config.contains(Strategy.ON_EACH_STEP):
            base64_image = TestManagerAPIAdapter.get_base64_image()
        elif status == "FAIL":
            stack_trace = TestManagerAPIAdapter.truncate(str(exception), 5)

        step_info = StepDTO(step_text, stack_trace, base64_image, status)
        TestManagerAPIAdapter.steps.append(step_info)


    @staticmethod
    def get_step_text(step):
        step_text_builder = step.keyword + " " + step.name
        return step_text_builder

    @staticmethod
    def clean_steps():
        if TestManagerAPIAdapter.steps:
            TestManagerAPIAdapter.steps.popleft()

    @staticmethod
    def truncate(string, length):
        if len(string) <= length:
            return string[:length]
        return string

    @staticmethod
    def get_base64_image():
        pass