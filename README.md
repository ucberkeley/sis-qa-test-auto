# QA Test Automation (QATA) framework
for UC Berkeley SIS Campus Solutions


### Instructions for running
1. [Install Docker](https://docs.docker.com/installation/).
1. Install the QATA framework with `./install.sh`. This will create a symlink to the server script
in /usr/bin.
1. If using external test directory, set `$SIS_TEST_DIR` to location of external test directory.
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
directory, run as `sudo -E qata start` to pass in environment variables). The first run will take
longer since the docker container will be downloaded and then run.
1. When required, stop the service with `qata stop`, or restart with `qata restart`
1. If required, attach to the service with `qata attach`.

### Additional notes
1. Keep docker/sis-qa-test-auto/Gemfile (and docker/sis-qa-test-auto/Gemfile.lock) in sync with
corresponding file(s) in in test directory by running `sync.sh`. This will ensure that all required
gems are installed when the sis-qa-test-auto docker container is being built. Though all
dependencies are checked for during test execution, and installed if not satisfied, having them
pre-installed will speed up test execution considerably.
