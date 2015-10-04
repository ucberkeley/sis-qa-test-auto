require 'json'
require 'pathname'

require 'selenium-webdriver'


SIS_TEST_DIR_ENV = 'SIS_TEST_DIR'
if ENV.has_key? SIS_TEST_DIR_ENV
  $config = JSON.parse(Pathname.new(ENV[SIS_TEST_DIR_ENV]).join('.config.json').read)
else
  $config = JSON.parse(Pathname.new(__FILE__).dirname.dirname.dirname.join('.config.json').read)
end

Before do
  $driver = Selenium::WebDriver.for :firefox
  $driver.manage.timeouts.implicit_wait = 3
end

After do
  $driver.quit
end