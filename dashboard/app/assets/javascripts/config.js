(function() {
  'use strict';

  angular.module('qat-dashboard').config([
    '$stateProvider',
    '$urlRouterProvider',
    '$mdThemingProvider',
    function($stateProvider, $urlRouterProvider, $mdThemingProvider) {
      $stateProvider
        .state('home', {
          url: '/home',
          templateUrl: '/home.html',
          controller: 'DashboardController',
          controllerAs: 'vm'
        });

      $urlRouterProvider.otherwise('home');

      $mdThemingProvider.theme('default')
        .primaryPalette('deep-purple')
        .accentPalette('red');
    }
  ]);
})();
