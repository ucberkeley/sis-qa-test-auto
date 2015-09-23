require 'selenium-webdriver'


Given 'I visit website $website' do |website|
  $driver.navigate.to website
end

Given 'I fill in $username in the username field' do |username|
  element = $driver.find_element(:id, 'email')
  element.send_keys username
end

Given 'I fill in $password in the password field' do |password|
  element = $driver.find_element(:id, 'pass')
  element.send_keys password
end

When 'I press the \'$button_value\' button' do |button_value|
  element = $driver.find_element(:xpath, "//input[@value='%s']" % button_value)
  element.click
end

Then 'I should be logged in' do
  true
end