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
          templateUrl: '/dashboard.html',
          controller: 'DashboardController',
          controllerAs: 'vm',
          css: 'assets/css/dashboard.css'
        });

      $urlRouterProvider.otherwise('dashboard');

      $mdThemingProvider.theme('default')
        .primaryPalette('deep-purple')
        .accentPalette('red');
    }
  ]);
})();
