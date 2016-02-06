# Test Execution Service Server

### Instructions for running
1. [Install Ruby](https://www.ruby-lang.org/en/documentation/installation/), preferably, a version
after 1.9.
1. [Download and install Python](https://www.python.org/downloads/), preferably, a Python 3 version.
If not installed, [install pip](http://pip.readthedocs.org/en/stable/installing/) additionally. Then
install the Tornado Web package with `pip install tornado` (or `pip3 install tornado`).
1. If running tests on a headless browser, [install PhantomJS](http://phantomjs.org/download.html).
1. Install gems required for testing by running `bundle install` in the test directory (you may have
to run `gem install bundle` first).
1. Add the qatserver module to PYTHONPATH by running `../scripts/qatserver_setup.sh`.
1. Still from the test directory, run `python3 -m qatserver`.


