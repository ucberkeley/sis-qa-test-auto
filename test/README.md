# Sample Test Setup

### Required files

Add files with the following information to the `SIS_TEST_DIR` (by default, this
is the current directory).

1. `${SIS_TEST_DIR}/.usernames.json`:

  ```json
  {
     "advisor": "<advisor username>",
     "ugrad_student": "<undergraduate student username>",
     "grad_student": "<graduate student username>",
     "faculty": "<faculty member username>"
  }
  ```
1. `${SIS_TEST_DIR}/.passwords.json`:

  ```json
  {
      "advisor": "<advisor password>",
      "ugrad_student": "<undergraduate student password>",
      "grad_student": "<graduate student password>",
      "faculty": "<faculty member password>"
  }
  ```
1. `${SIS_TEST_DIR}/.config.json` in the format:

  ```json
  {
      "<environment name>": {"<page name>": "<url>"}
  }

  ```
