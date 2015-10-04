require 'selenium-webdriver'
require 'json'

Given 'I visit the Campus Solutions website' do
  $driver.navigate.to $config['website_url']
end

Given 'I fill in the username field' do
  element = $driver.find_element(:id, 'email')
  element.send_keys $config['userid']
end

Given 'I fill in the password field' do
  element = $driver.find_element(:id, 'pass')
  element.send_keys $config['password']
end

When 'I press the \'$button_value\' button' do |button_value|
  element = $driver.find_element(:xpath, "//input[@value='%s']" % button_value)
  element.click
end

Then 'I should be logged in' do
  true
end