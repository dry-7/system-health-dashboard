# System Health Dashboard API

## 1. Project Overview

The objective is to build a lightweight System Health Dashboard API using Python Flask and demonstrate a DevOps workflow involving Git, automated testing, Docker containerisation and Jenkins CI/CD automation.

The application provides three endpoints that allow engineers to check the application's health status, version and environment.

## 2. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application development |
| Flask | Creating REST API endpoints |
| pytest | Automated endpoint testing |
| Git and GitHub | Version control and branch management |
| Docker | Application containerisation |
| Jenkins | CI/CD pipeline automation |
| VS Code | Development environment |

## 3. API Endpoints

The Flask application provides three HTTP GET endpoints:

| Endpoint | Description | Example response |
|---|---|---|
| `/health` | Returns the application's health status | `{"status": "UP"}` |
| `/version` | Returns the current application version | `{"version": "1.0.0"}` |
| `/environment` | Returns the environment configured through an environment variable | `{"environment": "development"}` |

Each endpoint returns HTTP status code 200 when functioning correctly.

The environment is read from the `APP_ENV` environment variable, with `development` as the default.

## 4. Prerequisites

To run the project locally, the following are required:

- Python 3 with pip and virtual environment support
- Git
- Docker Desktop or a compatible Docker Engine
- Jenkins with Git, Python and Docker access for CI/CD execution

The following local setup commands are for Windows PowerShell.

## 5. Running the Flask Application

Clone the repository:

`git clone https://github.com/dry-7/system-health-dashboard.git`

Enter the project folder:

`cd system-health-dashboard`

Create a Python virtual environment:

`py -m venv .venv`

Install the dependencies:

`.\.venv\Scripts\python.exe -m pip install -r requirements.txt`

Set the environment variable:

`$env:APP_ENV = "development"`

Start the application:

`.\.venv\Scripts\python.exe app.py`

The API can then be accessed at:

- `http://localhost:5000/health`
- `http://localhost:5000/version`
- `http://localhost:5000/environment`

## 6. Automated Testing

Automated tests are implemented using pytest in `tests/test_app.py`.

Three tests verify the following:

1. The `/health` endpoint returns HTTP 200 and the expected UP status.
2. The `/version` endpoint returns the expected application version.
3. The `/environment` endpoint correctly reads the environment variable.

Run the complete test suite using:

`.\.venv\Scripts\python.exe -m pytest -q`

The expected successful result is:

`3 passed`

An intentional testing failure was also demonstrated using a separate `feature/ci-failure-demo` branch, in which the test expected DOWN instead of the application's actual UP response.

This demonstrated how automated tests detect incorrect expectations and provided a scenario for validating Jenkins failure handling.

## 7. Docker Containerisation

The application is containerised using Docker.

The `Dockerfile` specifies the Python base image, installs dependencies and configures the Flask application to run inside the container.

The `.dockerignore` file excludes unnecessary files, including local virtual environments, Git metadata and generated Python cache files.

Build a versioned Docker image:

`docker build -t system-health-dashboard:v1.0 .`

Run the container:

`docker run -d --name health-dashboard -p 5000:5000 -e APP_ENV=production system-health-dashboard:v1.0`

Verify that the container is running:

`docker ps`

The application can then be tested through the same three endpoints on port 5000.

For example, accessing `/environment` should return:

`{"environment": "production"}`

This demonstrates that configuration can be supplied externally without changing the source code.

Stop and remove the container when testing is complete:

`docker stop health-dashboard`

`docker rm health-dashboard`

## 8. Jenkins CI/CD Pipeline

The Jenkins automation is defined in the `Jenkinsfile` and consists of six stages:

| Stage | Description |
|---|---|
| Checkout | Retrieves the specified branch from GitHub |
| Install | Creates a Python virtual environment and installs dependencies |
| Test | Executes the pytest test suite |
| Build | Builds the Docker image |
| Tag | Tags the Docker image using the Jenkins build number |
| Health Check | Starts a container and verifies the `/health` endpoint |

If automated testing fails, the pipeline does not proceed to the Docker build and subsequent stages.

Jenkins is run locally in a Docker container. A customised Jenkins image is defined in `Dockerfile.jenkins` to provide Python and Docker CLI support.

To build the customised Jenkins image:

`docker build -f Dockerfile.jenkins -t my-jenkins:python-docker .`

The local Jenkins instance uses Docker socket access to communicate with Docker Desktop. This is intended for a trusted local training environment and should not be used unchanged in production because it grants extensive Docker access.

To configure the Jenkins job, select **Pipeline script from SCM**, configure the GitHub repository, use branch `*/develop` and set the script path to `Jenkinsfile`.

The Jenkins dashboard is accessed at:

`http://localhost:8080`

### Successful Pipeline Verification

Jenkins Build #4 completed successfully on the `develop` branch.

The pipeline:

- Retrieved the application from GitHub.
- Installed the Python dependencies.
- Passed all three automated tests.
- Built the Docker image.
- Created the image tag `system-health-dashboard:4`.
- Started the container and verified its health endpoint.

The pipeline finished with `SUCCESS`.

A screenshot of the successful Jenkins pipeline is retained as submission evidence.

## 9. Git Branching Workflow

The project uses Git branches to separate development work from the final application.

- `main` — Final reviewed application.
- `develop` — Integration branch for completed functionality.
- `feature/api-endpoints` — Flask API implementation.
- `feature/automated-tests` — Automated endpoint tests.
- `feature/docker-container` — Docker configuration.
- `feature/jenkins-pipeline` — Jenkins CI/CD implementation.
- `feature/ci-failure-demo` — Isolated demonstration of failed automated testing.

Feature changes are committed with descriptive commit messages and merged into `develop`.

The intended final workflow is to request a peer or facilitator review through a pull request from `develop` to `main` before the final merge.

## 10. Challenges and Lessons Learned

Several practical challenges were encountered during development.

**GitHub Authentication**

GitHub did not accept password authentication when pushing changes. GitHub CLI was used to authenticate Git operations.

**Python Virtual Environments**

An initial virtual environment setup issue was encountered on Ubuntu. The required Python virtual environment package was installed before continuing.

**Docker Configuration**

The application was successfully packaged into a Docker image and tested using externally supplied environment variables.

**Jenkins Environment**

The initial Jenkins container did not include Python and Docker CLI tools. A customised Jenkins image was created to install the required dependencies and allow the pipeline to execute successfully.

These challenges helped reinforce the importance of troubleshooting, dependency management and repeatable automation in DevOps workflows.

## 11. Further Improvements

Possible improvements include a graphical dashboard for displaying API status, additional test coverage and more comprehensive application monitoring.

These are optional enhancements beyond the core mini project requirements.

## 12. AI Assistance

AI assistance was used to help explain DevOps concepts, troubleshoot setup issues and draft portions of the Flask application, automated tests, Docker configuration, Jenkins pipeline and documentation.

The application, automated tests, Docker container and Jenkins pipeline were executed and verified during development.