import requests
import json
import os
import ssl

from adapterPytest.src.main.pytest.ltm.models.runs.request.RunDTO import RunDTO


class TestManagerAPIClient:
    TEST_MANAGER_USER_KEY = "GenericUserLTM"
    TEST_MANAGER_PASS_KEY = "GenericUserLTM"
    TEST_MANAGER_API_HOST_KEY = "https://runs.crowdaracademy.lippia.io/runs"
    TEST_MANAGER_API_PORT_KEY = os.getenv("TEST_MANAGER_API_PORT")
    TEST_MANAGER_RUN_NAME = "aut sample #12"
    TEST_MANAGER_PROJECT_CODE = "PPC"

    apiUrl = None
    restTemplate = None

    @staticmethod
    def initialize_rest_template():
        TestManagerAPIClient.apiUrl = TestManagerAPIClient.get_api_url()

        if TestManagerAPIClient.apiUrl.startswith("https://"):
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            TestManagerAPIClient.restTemplate = requests.Session()
        else:
            TestManagerAPIClient.restTemplate = requests.Session()

    @staticmethod
    def get_rest_instance():
        if not TestManagerAPIClient.restTemplate:
            TestManagerAPIClient.initialize_rest_template()
        return TestManagerAPIClient.restTemplate

    @staticmethod
    def get_api_headers():
        if not TestManagerAPIClient.TEST_MANAGER_USER_KEY:
            raise ValueError("TEST_MANAGER_USERNAME must not be null")

        if not TestManagerAPIClient.TEST_MANAGER_PASS_KEY:
            raise ValueError("TEST_MANAGER_PASSWORD must not be null")

        headers = {
            "Content-Type": "application/json",
            "username": TestManagerAPIClient.TEST_MANAGER_USER_KEY,
            "password": TestManagerAPIClient.TEST_MANAGER_PASS_KEY
        }
        return headers

    @staticmethod
    def get_api_url():
        if TestManagerAPIClient.apiUrl:
            return TestManagerAPIClient.apiUrl

        uri = TestManagerAPIClient.TEST_MANAGER_API_HOST_KEY

        if TestManagerAPIClient.TEST_MANAGER_API_PORT_KEY:
            uri += ":" + TestManagerAPIClient.TEST_MANAGER_API_PORT_KEY

        return uri

    @staticmethod
    def create_run():
        if not TestManagerAPIClient.TEST_MANAGER_RUN_NAME:
            raise ValueError("TEST_MANAGER_RUN_NAME cannot be null")

        if not TestManagerAPIClient.TEST_MANAGER_PROJECT_CODE:
            raise ValueError("TEST_MANAGER_PROJECT_CODE cannot be null")

        run = RunDTO()
        run.set_run_name(TestManagerAPIClient.TEST_MANAGER_RUN_NAME)
        run.set_project_code(TestManagerAPIClient.TEST_MANAGER_PROJECT_CODE)

        url = TestManagerAPIClient.get_api_url() + "/runs"
        headers = TestManagerAPIClient.get_api_headers()
        run_dict = run.to_dict()  # Convertir a diccionario
        response = TestManagerAPIClient.get_rest_instance().post(url, data=json.dumps(run_dict), headers=headers)

        run_response = RunDTO(response['name'], response['project_code'])
        return run_response

    @staticmethod
    def create_test(test):
        url = TestManagerAPIClient.get_api_url() + "/tests"
        TestManagerAPIClient.get_rest_instance().post(url, data=json.dumps(test), headers=TestManagerAPIClient.get_api_headers())