(function() {
  'use strict';

  angular.module('qat-dashboard').config([
    '$stateProvider',
    '$urlRouterProvider',
    '$mdThemingProvider',
    function($stateProvider, $urlRouterProvider, $mdThemingProvider) {
      $stateProvider
        .state('dashboard', {
          url: '/dashboard',
          templateUrl: 'html/dashboard.html',
          controller: 'DashboardController',
          controllerAs: 'vm'
        })
        .state('testStatus', {
          url: '/status/{uuid}',
          templateUrl: 'html/test_status.html',
          controller: 'TestStatusController',
          controllerAs: 'vm'
        });

      $urlRouterProvider.otherwise('dashboard');

      $mdThemingProvider.theme('default')
        .primaryPalette('deep-purple')
        .accentPalette('red');
    }
  ]);
})();
