require 'json'
require 'pathname'

require 'capybara/cucumber'
require 'capybara/poltergeist'


SIS_TEST_DIR_ENV = 'SIS_TEST_DIR'
if ENV.has_key? SIS_TEST_DIR_ENV
  $config = JSON.parse(Pathname.new(ENV[SIS_TEST_DIR_ENV]).join('.config.json').read)
else
  $config = JSON.parse(Pathname.new(__FILE__).dirname.dirname.dirname.join('.config.json').read)
end

Capybara.default_driver = :poltergeist
Capybara.default_wait_time = 5

