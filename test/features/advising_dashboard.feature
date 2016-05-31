Feature: Advisor My Dashboard Page
  As an advisor, I should be able to do student lookup searching students by name,SID,UID.


  Scenario: Student Lookup card exists
    Given I login to calcentral with valid advisor credentials & navigate to my dashboard
    Then I should see Student Lookup card
