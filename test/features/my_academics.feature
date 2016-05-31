Feature: My Academics Enrollment Page
  As a student (with no holds on my account) should be able to click on schedule of classes and, add/drop/swap/edit
  classes

  Scenario: My academics enrollment card exists
    Given I login to calcentral with valid student credentials
    And I navigate to my academics tab
    Then I see enrollment card is available
