import http.client
import socket
import json
import os.path

import pytest

from selenium import webdriver
from selenium.webdriver.remote.command import Command
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0


CONFIG_FILE = os.path.join(os.path.dirname(__file__), ".config.json")


_driver = None
_config = None


def new_driver():
    return webdriver.Firefox()


def setup_module(module):
    global _driver
    _driver = new_driver()


def teardown_module(module):
    global _driver
    if not has_quit(_driver):
        _driver.quit()


@pytest.fixture(scope='function')
def driver():
    global _driver
    if has_quit(_driver):
        _driver = new_driver()
    return _driver


@pytest.fixture(scope='function')
def config():
    global _config
    if _config is None:
        _config = json.load(open(CONFIG_FILE))
    return _config


def has_quit(driver):
    try:
        driver.execute(Command.STATUS)
        return False
    except (socket.error, http.client.CannotSendRequest):
        return True


def test_driver(driver):
    query = "cheese!"

    driver.get("http://www.google.com")
    assert driver.title == 'Google'

    # find the element that's name attribute is q (the google search box)
    input_element = driver.find_element_by_name("q")
    # type in the search
    input_element.send_keys(query)
    # submit the form (although google automatically searches now without submitting)
    input_element.submit()

    # we have to wait for the page to refresh, the last thing that seems to be updated is the title
    WebDriverWait(driver, 10).until(EC.title_contains(query))
    assert driver.title == "{} - Google Search".format(query)