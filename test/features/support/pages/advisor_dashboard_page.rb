class AdvisorDashboardPage < SitePrism::Page

  set_url $config['calcentralAdvisorDashboardTab']
  element :student_lookup_card, :xpath, '//div[@data-ng-include="\'widgets/toolbox/user_search.html\'"]'
end