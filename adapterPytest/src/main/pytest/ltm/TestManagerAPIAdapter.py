from collections import deque
from threading import local

import pytest

from adapterPytest.src.main.pytest.ltm.TestManagerAPIClient import TestManagerAPIClient
from adapterPytest.src.main.pytest.ltm.models.runs.request.StepDTO import StepDTO
from adapterPytest.src.main.pytest.ltm.models.runs.request.TestDTO import TestDTO
from adapterPytest.src.main.pytest.ltm.screenshots.SSConfig import SSConfig
from adapterPytest.src.main.pytest.ltm.screenshots.Strategy import Strategy


class TestManagerAPIAdapter:
    runResponseDTO = None
    steps = local()

    def __init__(self):
        self.screenshotConfig = SSConfig.load()
        self.runResponseDTO = TestManagerAPIClient.create_run()
        self.steps = local()

    @staticmethod
    def pytest_bdd_after_scenario(request, feature, scenario):
        title = scenario.name
        status = "failed" if scenario.failed else "passed"
        status = status.upper()[:len(status) - 2]
        feature_name = feature.name
        test = TestDTO(title, TestManagerAPIAdapter.runResponseDTO.get_id(), status, feature_name, "SCENARIO", scenario.tags, TestManagerAPIAdapter.steps.get())
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
            TestManagerAPIAdapter.steps.set(deque())
        screenshot_config = SSConfig.load()
        if screenshot_config.contains(Strategy.ON_EACH_STEP):
            TestManagerAPIAdapter.get_base64_image()
        elif screenshot_config.contains(Strategy.ON_FAILURE) and status == "FAILED":
            TestManagerAPIAdapter.get_base64_image()
            stack_trace = TestManagerAPIAdapter.truncate(step_func_args.result.error.message, 5)
        TestManagerAPIAdapter.steps.get().append(StepDTO(step_text, stack_trace, base64_image, status))

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
        if TestManagerAPIAdapter.steps.get() is not None:
            TestManagerAPIAdapter.steps.remove()

    @staticmethod
    def truncate(string, length):
        if len(string) <= length:
            return string[:length]
        return string

    @staticmethod
    def get_base64_image():
        pass


if __name__ == "__main__":
    pytest.main()