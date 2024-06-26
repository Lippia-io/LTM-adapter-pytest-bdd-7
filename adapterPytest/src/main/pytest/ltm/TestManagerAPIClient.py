import requests
import json
import os
import ssl

from adapterPytest.src.main.pytest.ltm.models.runs.request.RunDTO import RunDTO
from adapterPytest.src.main.pytest.ltm.models.runs.response.RunDTO import RunDTO as ResponseRunDTO


class TestManagerAPIClient:
    TEST_MANAGER_USER_KEY = os.getenv('TEST_MANAGER_USER_KEY')
    TEST_MANAGER_PASS_KEY = os.getenv('TEST_MANAGER_PASS_KEY')
    TEST_MANAGER_API_HOST_KEY = os.getenv('TEST_MANAGER_API_HOST_KEY')
    TEST_MANAGER_API_PORT_KEY = os.getenv("TEST_MANAGER_API_PORT")
    TEST_MANAGER_REPOSITORY_URL = os.getenv("TEST_MANAGER_REPOSITORY_URL")
    TEST_MANAGER_REPOSITORY_BRANCH = os.getenv("TEST_MANAGER_REPOSITORY_BRANCH")
    TEST_MANAGER_RUN_NAME = None
    TEST_MANAGER_PROJECT_CODE = None

    apiUrl = None
    restTemplate = None

    @staticmethod
    def initialize_rest_template(RUN_NAME, PROJECT_CODE):

        TestManagerAPIClient.TEST_MANAGER_RUN_NAME = RUN_NAME
        TestManagerAPIClient.TEST_MANAGER_PROJECT_CODE = PROJECT_CODE
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
        if TestManagerAPIClient.TEST_MANAGER_RUN_NAME is None or not TestManagerAPIClient.TEST_MANAGER_RUN_NAME:
            raise ValueError("TEST_MANAGER_RUN_NAME cannot be null or empty")

        if TestManagerAPIClient.TEST_MANAGER_PROJECT_CODE is None or not TestManagerAPIClient.TEST_MANAGER_PROJECT_CODE:
            raise ValueError("TEST_MANAGER_PROJECT_CODE cannot be null or empty")

        if TestManagerAPIClient.TEST_MANAGER_REPOSITORY_URL is None or not TestManagerAPIClient.TEST_MANAGER_REPOSITORY_URL:
            raise ValueError("TEST_MANAGER_REPOSITORY_URL cannot be null or empty")

        if TestManagerAPIClient.TEST_MANAGER_REPOSITORY_BRANCH is None or not TestManagerAPIClient.TEST_MANAGER_REPOSITORY_BRANCH:
            raise ValueError("TEST_MANAGER_REPOSITORY_BRANCH cannot be null or empty")



        run = RunDTO()
        run.set_run_name(TestManagerAPIClient.TEST_MANAGER_RUN_NAME)
        run.set_project_code(TestManagerAPIClient.TEST_MANAGER_PROJECT_CODE)
        run.set_repository_url(TestManagerAPIClient.TEST_MANAGER_REPOSITORY_URL)
        run.set_repository_branch(TestManagerAPIClient.TEST_MANAGER_REPOSITORY_BRANCH)

        url = TestManagerAPIClient.get_api_url() + "/runs"
        headers = TestManagerAPIClient.get_api_headers()
        run_dict = run.to_dict()  # Convertir a diccionario
        response = TestManagerAPIClient.get_rest_instance().post(url, data=json.dumps(run_dict), headers=headers)

        response_data = response.json()
        run_response = ResponseRunDTO(response_data['id'])
        return run_response

    @staticmethod
    def create_test(test):
        url = TestManagerAPIClient.get_api_url() + "/tests"
        TestManagerAPIClient.get_rest_instance().post(url, data=json.dumps(test.to_dict()),headers=TestManagerAPIClient.get_api_headers())
