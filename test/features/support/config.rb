require 'json'
require 'pathname'

require 'capybara/cucumber'


SIS_TEST_DIR_ENV = 'SIS_TEST_DIR'
if ENV.has_key? SIS_TEST_DIR_ENV
  $config = JSON.parse(Pathname.new(ENV[SIS_TEST_DIR_ENV]).join('.config.json').read)
else
  $config = JSON.parse(Pathname.new(__FILE__).dirname.dirname.dirname.join('.config.json').read)
end


SIS_TEST_WEBDRIVER_ENV = 'SIS_TEST_WEBDRIVER'
if ENV.has_key? SIS_TEST_WEBDRIVER_ENV and ENV[SIS_TEST_WEBDRIVER_ENV].downcase == 'selenium'
  Bundler.require(:default, :webdriver_selenium)
  require 'selenium/webdriver'
  Capybara.default_driver = :selenium
else
  Bundler.require(:default, :webdriver_poltergeist)
  require 'capybara/poltergeist'
  Capybara.default_driver = :poltergeist
end

Capybara.default_wait_time = 5

