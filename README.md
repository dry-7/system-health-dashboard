# System Health Dashboard API

## About the Project

I built this project as part of my DevOps training to practise working with Flask, Git, Docker, automated testing and Jenkins.

The application is a simple API that lets you check whether it's running, which version is being used and what environment it's running in.

The main focus of the project was learning how to test an application, run it inside a Docker container and automate the process using Jenkins.

## Technologies Used

- **Python and Flask** – Built the API and its endpoints.
- **pytest** – Used to test the endpoints.
- **Git and GitHub** – Managed branches, commits and pull requests.
- **Docker** – Packaged the application into a container.
- **Jenkins** – Automated testing and Docker builds.
- **VS Code** – Used to write and manage the code.

## API Endpoints

The application has three endpoints:

| Endpoint | What it does |
|---|---|
| `/health` | Checks the application's health status |
| `/version` | Shows the current application version |
| `/environment` | Shows which environment the application is running in |

Example responses:

- `/health` → `{"status": "UP"}`
- `/version` → `{"version": "1.0.0"}`
- `/environment` → `{"environment": "development"}`

The environment is controlled by the `APP_ENV` variable. If no environment is specified, it defaults to `development`.

## Running the Project Locally

You will need Python, Git and the dependencies listed in `requirements.txt`.

These commands are for Windows PowerShell.

**1. Clone the repository**

`git clone https://github.com/dry-7/system-health-dashboard.git`

`cd system-health-dashboard`

**2. Create a virtual environment**

`py -m venv .venv`

**3. Install the required packages**

`.\.venv\Scripts\python.exe -m pip install -r requirements.txt`

**4. Set the environment**

`$env:APP_ENV = "development"`

**5. Start the application**

`.\.venv\Scripts\python.exe app.py`

Once the application is running, you can access the endpoints through your browser:

- http://localhost:5000/health
- http://localhost:5000/version
- http://localhost:5000/environment

## Automated Testing

I used pytest to test the three endpoints. The tests are stored in `tests/test_app.py`.

The tests check that:

- The health endpoint returns `UP` with status code 200.
- The version endpoint returns the correct version.
- The environment endpoint reads the configured environment variable.

To run the tests:

`.\.venv\Scripts\python.exe -m pytest -q`

All three tests should pass.

I also created a separate branch called `feature/ci-failure-demo` to show what happens when a test fails.

For this demonstration, I changed the health test to expect `DOWN` instead of `UP`. Since the application actually returns `UP`, the test failed.

I used this to demonstrate that Jenkins detects a failed test and stops the pipeline before moving on to the Docker build.

## Docker

I used Docker to run the application inside a container instead of relying on my local Python setup.

The `Dockerfile` uses a Python base image, installs the required packages and starts the Flask application.

I also included a `.dockerignore` file to keep unnecessary files out of the Docker image.

**Build the Docker image:**

`docker build -t system-health-dashboard:v1.0 .`

**Run the container:**

`docker run -d --name health-dashboard -p 5000:5000 -e APP_ENV=production system-health-dashboard:v1.0`

**Check that it's running:**

`docker ps`

Once the container starts, the application is available on port 5000.

For example, visiting http://localhost:5000/environment should now return:

`{"environment": "production"}`

This is because I passed `APP_ENV=production` when starting the container, without needing to change the application code.

To stop and remove the container:

`docker stop health-dashboard`

`docker rm health-dashboard`

## Jenkins Pipeline

I used Jenkins to automate the steps I had previously been running manually.

The pipeline is defined in the `Jenkinsfile` and has six stages.

| Stage | What happens |
|---|---|
| Checkout | Gets the project code from GitHub |
| Install | Sets up Python and installs the dependencies |
| Test | Runs the automated tests |
| Build | Builds the Docker image |
| Tag | Tags the image with the Jenkins build number |
| Health Check | Runs the container and checks the health endpoint |

The pipeline only continues if the previous stages succeed.

For example, if one of the pytest tests fails, Jenkins stops the pipeline and doesn't build the Docker image.

### My Jenkins Setup

I ran Jenkins locally using Docker Desktop.

At first, the Jenkins container didn't have everything needed to run my pipeline, so I created `Dockerfile.jenkins` to install Python and Docker CLI tools.

I built the custom image using:

`docker build -f Dockerfile.jenkins -t my-jenkins:python-docker .`

My local Jenkins setup uses Docker socket access so it can build and run containers through Docker Desktop. This is suitable for my local training setup, but I would use a more secure configuration in a production environment.

I configured Jenkins to retrieve the project from GitHub and use the `Jenkinsfile` on the `develop` branch.

Jenkins can be accessed locally at http://localhost:8080 when the container is running.

### Successful Pipeline

After fixing the setup issues, I managed to get the full pipeline running successfully.

Jenkins Build #4 completed successfully on the `develop` branch.

It:

- Retrieved the project from GitHub.
- Installed the Python dependencies.
- Passed all three automated tests.
- Built the Docker image.
- Tagged the image as `system-health-dashboard:4`.
- Ran the container and checked the `/health` endpoint.

The final build status was `SUCCESS`.

I also kept screenshots of the Jenkins results as evidence.

## Git and GitHub Workflow

I used a Git branching workflow to keep different parts of the project separate while developing them.

My main branches were:

- `main` – The final version of the project.
- `develop` – Where I combined completed features.
- `feature/api-endpoints` – Flask endpoints.
- `feature/automated-tests` – pytest tests.
- `feature/docker-container` – Docker configuration.
- `feature/jenkins-pipeline` – Jenkins automation.
- `feature/ci-failure-demo` – Demonstrating a test failure.

I worked on separate feature branches and merged changes into `develop` using GitHub pull requests.

I then merged the completed work into `main`.

This helped me practise using branches and pull requests rather than making every change directly on `main`.

## Problems I Ran Into

I had a few issues while working on the project.

**GitHub authentication**

I initially had trouble pushing changes to GitHub because password authentication wasn't supported. I used GitHub CLI to authenticate and continue pushing my code.

**Python setup**

I ran into an issue creating a Python virtual environment on Ubuntu. I fixed this by installing the required virtual environment package.

**Jenkins setup**

This was probably the main challenge. My Jenkins container was missing Python and Docker tools, which meant the pipeline couldn't run properly.

I created a custom Jenkins image with the tools needed for the pipeline.

I also had an issue with the Git configuration in Jenkins, which I fixed before rerunning the pipeline.

After making these changes, I was able to run the complete pipeline successfully.

## What I Learned

This project helped me understand how different DevOps tools work together.

Before building it, I had mainly been learning about these tools individually. Working on this project gave me a better idea of how Git, automated testing, Docker and Jenkins fit into one workflow.

One thing I found useful was seeing how Jenkins handles a failed test. Instead of continuing to build an image with failing tests, the pipeline stops and reports the problem.

I also got more practice troubleshooting issues with Docker, Python dependencies and Jenkins configuration.

If I were to improve this project further, I would add more tests, build a basic visual dashboard and look into using Prometheus and Grafana for monitoring.

## AI Assistance

I used AI tools during the project to help explain concepts I was unfamiliar with, troubleshoot errors and assist with parts of the code and documentation.

This included guidance with Flask, pytest, Docker and Jenkins configuration.

I ran the application, tested the endpoints, worked through setup issues and checked the Jenkins pipeline during development.