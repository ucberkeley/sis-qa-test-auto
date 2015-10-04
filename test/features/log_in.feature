Feature: Login
  User should be able to log in Campus Solutions systems with
  the correct credentials.

  Scenario: Try logging in with correct credentials
    Given I visit the Campus Solutions website
    And I fill in the username field
    And I fill in the password field
    When I press the 'Log In' button
    Then I should be logged in