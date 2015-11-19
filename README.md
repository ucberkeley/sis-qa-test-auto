# QA Test Automation (QATA) framework
for UC Berkeley Student Information Systems (SIS) Campus Solutions

[![Build Status](https://travis-ci.org/ucberkeley/sis-qa-test-auto.svg)](https://travis-ci.org/ucberkeley/sis-qa-test-auto)


## Environment variables
* `SIS_TEST_DIR=<project-dir>/test`: If using external test directory, set to location of
external test directory.
* `SIS_LOGS_DIR=<project-dir>/logs`: If using external logs directory, set to location of
external logs directory.
* `SIS_SERVER_PORT=8421`: Set to port number that server should listen on.
* `SIS_DASHBOARD_PORT=3000`: Set to port number that dashboard should be available on.
number.
* `SIS_TEST_WEBDRIVER=selenium`: Selenium WebDriver runs test on the graphical Firefox browser.
If deploying in an environment wihtout a graphical interface (for example, a remote server), set
`SIS_TEST_WEBDRIVER=poltergeist`. The framework will then use Poltergeist WebDriver on PhantomJS
headless browser.


## Instructions for running
1. [Install Docker Engine](https://docs.docker.com/installation/).
1. Install the QATA framework with `scripts/install.sh`. This will create a symlink to the server
script in /usr/bin.
1. Check section on [Setting Environment variables](#setting-environment-variables).
1. Add file test/.config.json with the following information:

    ```json
    {
        "website_url": "<Campus Solutions Test Instance URL>",
        "userid": "<User ID for Test Instance>",
        "password": "<Password for Test Instance>",
        "title": "Berkeley Student Information System"
    }
    ```

1. Run the Test Framework service with `qata start` (may required sudo. If using external test
and/or logs directory, run as `sudo -E qata start` to pass in environment variables). The first
run will take longer since the docker container will be downloaded and then run.
1. When required, stop the service with `qata stop`, or restart with `qata restart`
1. If required, attach to the service with `qata attach`.


### Alternate instructions for running (using Docker Compose)
1. [Install Docker Compose](https://docs.docker.com/compose/install/) (in addition to [Docker
Engine](https://docs.docker.com/installation/)).
1. In the project directory, run `docker compose up` (may require sudo. If using external test
and/or logs directory, run as `sudo -E docker compose up` to pass in environment variables). The
first run will take longer since the Docker containers will be built and then run.


## Additional notes
1. Keep the test execution server files and Gemfile (and Gemfile.lock) in docker/sis-qa-test-auto
in sync with corresponding file(s) in the server directory and the test directory by running
`scripts/sync.sh`. The up-to-date Gemfile will ensure that all required gems are installed when
the sis-qa-test-auto docker container is being built. Though all dependencies are checked for
during test execution, and installed if not satisfied, having them pre-installed will speed up
test execution considerably.
1. You can clean up the logs folder by running `scripts/cleanup.sh`.
