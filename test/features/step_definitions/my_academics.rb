Given 'I login to calcentral with valid student credentials' do
  auth_page = CalcentralCalNetAuthPage.new
  auth_page.login $usernames['ugrad_student'], $passwords['ugrad_student']
end

Then 'I navigate to my academics tab' do
  @academics_tab = CalcentralAcademicsTab.new
end

Then 'I see enrollment card is available' do
  assert @academics_tab.has_enrollment_card?
end
