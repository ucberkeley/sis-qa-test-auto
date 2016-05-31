require 'json'
require 'pathname'

require 'capybara/cucumber'


SIS_TESTING_ENV_ENV = 'SIS_TESTING_ENV'
if ENV.has_key? SIS_TESTING_ENV_ENV
  testing_env = ENV[SIS_TESTING_ENV_ENV]
else
  testing_env = 'dev'
end

SIS_TEST_DIR_ENV = 'SIS_TEST_DIR'
if ENV.has_key? SIS_TEST_DIR_ENV
  test_dir = Pathname.new(ENV[SIS_TEST_DIR_ENV])
else
  test_dir = Pathname.new(__FILE__).dirname.dirname.dirname
end
$config = JSON.parse(test_dir.join('.config.json').read)[testing_env]
$usernames = JSON.parse(test_dir.join('.usernames.json').read)
$passwords = JSON.parse(test_dir.join('.passwords.json').read)

SIS_TEST_WEBDRIVER_ENV = 'SIS_TEST_WEBDRIVER'
if ENV.has_key? SIS_TEST_WEBDRIVER_ENV and ENV[SIS_TEST_WEBDRIVER_ENV].downcase == 'poltergeist'
  Bundler.require(:default, :webdriver_poltergeist)
  require 'capybara/poltergeist'
  Capybara.default_driver = :poltergeist
else
  Bundler.require(:default, :webdriver_selenium)
  require 'selenium/webdriver'
  Capybara.default_driver = :selenium
end

SitePrism.configure do |config|
  config.use_implicit_waits = true
end

Capybara.ignore_hidden_elements = true
Capybara.default_max_wait_time = 2
SolidAssert.enable_assertions

