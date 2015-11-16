require 'json'

# require '../support/hooks'

Given 'I visit the Campus Solutions website' do
  visit $config['website_url']
end

Given 'I fill in the username field' do
  fill_in 'userid', :with => $config['userid']
end

Given 'I fill in the password field' do
  fill_in 'pwd', :with => $config['password']
end

When 'I press the \'$button_value\' button' do |button_value|
  click_button button_value
end

Then 'I should be logged in' do
  page.title.equal? $config['title']
end
