import requests
import json
import os
import ssl


class TestManagerAPIClient:
    TEST_MANAGER_USER_KEY = os.getenv("TEST_MANAGER_USERNAME")
    TEST_MANAGER_PASS_KEY = os.getenv("TEST_MANAGER_PASSWORD")
    TEST_MANAGER_API_HOST_KEY = os.getenv("TEST_MANAGER_API_HOST")
    TEST_MANAGER_API_PORT_KEY = os.getenv("TEST_MANAGER_API_PORT")
    TEST_MANAGER_RUN_NAME = os.getenv("TEST_MANAGER_RUN_NAME")
    TEST_MANAGER_PROJECT_CODE = os.getenv("TEST_MANAGER_PROJECT_CODE")

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
        if not TestManagerAPIClient.rest_template:
            TestManagerAPIClient.initialize_rest_template()
        return TestManagerAPIClient.rest_template

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

        run = {
            "name": TestManagerAPIClient.TEST_MANAGER_RUN_NAME,
            "project_code": TestManagerAPIClient.TEST_MANAGER_PROJECT_CODE
        }

        url = TestManagerAPIClient.get_api_url() + "/runs"
        response = TestManagerAPIClient.get_rest_instance().post(url, data=json.dumps(run), headers=TestManagerAPIClient.get_api_headers())
        return response.json()

    @staticmethod
    def create_test(test):
        url = TestManagerAPIClient.get_api_url() + "/tests"
        TestManagerAPIClient.get_rest_instance().post(url, data=json.dumps(test), headers=TestManagerAPIClient.get_api_headers())