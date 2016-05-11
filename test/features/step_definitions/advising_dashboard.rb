Given 'I login to calcentral with valid advisor credentials & navigate to my dashboard' do
  auth_page = CalcentralCalNetAuthPage.new
  auth_page.login $usernames['advisor'], $passwords['advisor']
end

Then 'I should see Student Lookup card' do
  @advisor_dashboard =  CalcentralAdvisorDashboardTab.new
  assert @advisor_dashboard.has_student_lookup_card?
end

