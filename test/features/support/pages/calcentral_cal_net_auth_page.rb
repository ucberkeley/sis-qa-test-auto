class CalcentralCalNetAuthPage < SitePrism::Page

  set_url $config['calcentralCalNetAuthPageUrl']

  element :username_field, :xpath, '//input[@id="username"]'
  element :password_field, :xpath, '//input[@id="password"]'
  element :submit_button, :xpath, '//input[@value="Sign In"]'
  element :log_out_button, :xpath, '//button[contains(text(), "Log out")]'
  element :settings_button, :xpath, '//button[@title="Settings"]'

  def initialize
    self.load
  end

  def login(username, password)
    unless self.has_username_field?
      self.settings_button.click
      self.log_out_button.click
      sleep 1
      self.load
    end
    self.username_field.set username
    self.password_field.set password
    self.submit_button.click
  end
end