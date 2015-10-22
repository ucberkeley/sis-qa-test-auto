SIS_TEST_DIR_ENV = 'SIS_TEST_DIR'
SIS_TEST_SERVER_PORT_ENV = 'SIS_TEST_SERVER_PORT'

# Check and set (if required) environment variables
unless ENV.key? SIS_TEST_DIR_ENV
  ENV[SIS_TEST_DIR_ENV] = Pathname.new(__FILE__).dirname.dirname.dirname.join('logs')
end
unless ENV.key? SIS_TEST_SERVER_PORT_ENV
  ENV[SIS_TEST_SERVER_PORT_ENV] = 8421
end


# Load the Rails application.
require File.expand_path('../application', __FILE__)

# Initialize the Rails application.
Rails.application.initialize!
