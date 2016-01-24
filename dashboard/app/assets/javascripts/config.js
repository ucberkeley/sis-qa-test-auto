(function() {
  'use strict';

  angular.module('qat-dashboard').config([
    '$stateProvider',
    '$urlRouterProvider',
    function($stateProvider, $urlRouterProvider) {
      $stateProvider
        .state('home', {
          url: '/home',
          templateUrl: '/home.html',
          controller: 'DashboardController',
          controllerAs: 'vm'
        });

      $urlRouterProvider.otherwise('home');
    }
  ]);
})();
