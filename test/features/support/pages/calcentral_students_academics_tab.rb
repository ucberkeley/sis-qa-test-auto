class CalcentralStudentsAcademicsTab < SitePrism::Page

  set_url $config['calcentralAcademicsTab']

  # TODO: Add link following to 'My academics' tab

  element :pause, 'nothing'
  element :enrollment_card, 'div.cc-enrollment-card-head'

  def initialize
    self.load
  end
end