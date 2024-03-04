
# Lippia Test Manager Pytest-BDD Adapter

[![Crowdar Official Page](https://img.shields.io/badge/crowdar-official%20page-brightgreen)](https://crowdar.com.ar/)  [![Lippia Official Page](https://img.shields.io/badge/lippia-official%20page-brightgreen)](https://www.lippia.io/)

The Lippia Test Manager adapter allows to ingest pytest-bdd test results into a Lippia Test Manager instance.  
To have access to a Lippia Test Manager go to  **[Lippia.io](https://lippia.io/)**  website.

## Getting Started

### Import dependency

Add the path to install at the requiremrnt folder
``````
git+ssh://git@ssh....../pytest-bdd-7-adapter.git
``````

### Report Class

You need to create the class that implements the `TestManagerAPIAdapter` interface to handle Pytest BDD hooks. This class will utilize the `TestManagerAPIAdapter` and `TestManagerAPIClient` from the **Lippia Test Manager adapter**

### Configure the env variables

| Key                        | Concept                                                                 | Is         |  
|----------------------------|-------------------------------------------------------------------------|------------|  
| USER_KEY      | User with which the Test Manager instance will be authenticated         | Mandatory  |  
| PASS_KEY      | Password with which the Test Manager instance will be authenticated     | Mandatory  |  
| HOST_KEY      | Host to which the adapter will attempt to authenticate                  | Mandatory  |  
| TEST_MANAGER_API_PORT      | Port on which the Test Manager instance will be listening               | Optional   |  

**Local variables in the config file**

| Key                        | Concept                                                                 | Is         |  
|----------------------------|-------------------------------------------------------------------------|------------|
| RUN_NAME      | Run name, serves as identifier of the suite execution                   | Mandatory  |  
| PROJECT_CODE  | Project Code into which the adapter will attempt to inject test results | Mandatory  |
