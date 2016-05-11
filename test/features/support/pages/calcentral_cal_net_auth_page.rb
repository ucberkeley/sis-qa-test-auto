class CalcentralCalNetAuthPage < SitePrism::Page

  set_url $config['calcentralCalNetAuthPageUrl']

  element :username_field, 'input[id="username"]'
  element :password_field, 'input[id="password"]'
  element :submit_button, 'input[value="Sign In"]'

  def initialize
    self.load
  end

  def login(username, password)
    if self.has_username_field?
      self.username_field.set username
      self.password_field.set password
      self.submit_button.click
    end
  end
end