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
    def pytest_bdd_after_scenario(request, feature, scenario):
        if TestManagerAPIAdapter.runResponseDTO is None:
            TestManagerAPIAdapter.runResponseDTO = TestManagerAPIClient.create_run()
        title = scenario.name
        status = "passed"  # Por defecto, asumimos que el escenario ha pasado
        for step in scenario.steps:
            if step.failed:
                status = "failed"
                break
        status = status.upper()[:len(status) - 2]
        feature_name = feature.name
        steps = [StepDTO(title=step.name, description=step.full_name) for step in scenario.steps]
        test = TestDTO(title, TestManagerAPIAdapter.runResponseDTO.get_id(), status, feature_name, "SCENARIO", scenario.tags,steps)
        TestManagerAPIClient.create_test(test)
        TestManagerAPIAdapter.clean_steps()

    @staticmethod
    def pytest_bdd_after_step(feature, scenario, step, step_func, step_func_args):
        step_text = TestManagerAPIAdapter.get_step_text(step)
        status = step_func.status
        status = status.upper()[:len(status) - 2]
        base64_image = None
        stack_trace = None
        if TestManagerAPIAdapter.steps.get() is None:
            TestManagerAPIAdapter.steps = deque()

        screenshot_config = SSConfig.load()
        if screenshot_config.contains(Strategy.ON_EACH_STEP):
            TestManagerAPIAdapter.get_base64_image()
        elif screenshot_config.contains(Strategy.ON_FAILURE) and status == "FAILED":
            TestManagerAPIAdapter.get_base64_image()
            stack_trace = TestManagerAPIAdapter.truncate(step_func_args.result.error.message, 5)

        step_info = StepDTO(step_text, stack_trace, base64_image, status)
        TestManagerAPIAdapter.steps.append(step_info)

    @staticmethod
    def get_step_text(step):
        step_text_builder = ""
        step_text_builder += step.prefix + " "
        step_text_builder += step.name
        if step.doc_string is not None:
            step_text_builder += step.doc_string
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