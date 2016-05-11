Feature: My Academics Enrollment Page
  User should be able to click on schedule of classes,add,drop,swap,edit classes

  Scenario: My academics enrollment card exists
  Given I login to calcentral with valid credentials
  And I navigate to my academics tab
  Then I see enrollment card is available
