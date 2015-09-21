# sis-qa-test-auto

QA Test Automation framework for SIS Campus Solutions.


### Instructions for running
1. [Install Docker](https://docs.docker.com/installation/).
2. If using external test directory, set `$CC_TEST_DIR` to location of external test directory.
4. Add file test/.config.json with the following information:
```json
{
    "website_url": "<Campus Solutions Test Instance URL>",
    "userid": "<User ID for Test Instance>",
    "password": "<Password for Test Instance>",
    "title": "Berkeley Student Information System"
}
```
3. Run `run.sh` (may required sudo. If using external test directory, run as `sudo -E ./run.sh` to 
pass in environment variables). The first run will take longer since the docker container will be 
downloaded and then run.
