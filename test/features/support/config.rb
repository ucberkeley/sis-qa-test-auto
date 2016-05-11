require 'json'
require 'pathname'

require 'capybara/cucumber'


SIS_TEST_DIR_ENV = 'SIS_TEST_DIR'

if ENV.has_key? SIS_TEST_DIR_ENV
  $config = JSON.parse(Pathname.new(ENV[SIS_TEST_DIR_ENV]).join('.config.json').read)
  $usernames = JSON.parse(Pathname.new(ENV[SIS_TEST_DIR_ENV]).join('.usernames.json').read)
  $passwords = JSON.parse(Pathname.new(ENV[SIS_TEST_DIR_ENV]).join('.passwords.json').read)
else
  $config = JSON.parse(Pathname.new(__FILE__).dirname.dirname.dirname.join('.config.json').read)
  $usernames = JSON.parse(Pathname.new(__FILE__).dirname.dirname.dirname.join('.usernames.json').read)
  $passwords = JSON.parse(Pathname.new(__FILE__).dirname.dirname.dirname.join('.passwords.json').read)
end


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

