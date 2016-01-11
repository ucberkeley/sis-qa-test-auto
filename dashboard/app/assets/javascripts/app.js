(function() {
  angular.module('qat-dashboard', ['ui.router'])
    .config([
      '$stateProvider',
      '$urlRouterProvider',
      function($stateProvider, $urlRouterProvider) {
        $stateProvider
          .state('home', {
            url: '/home',
            templateUrl: '/home.html',
            controller: 'MainCtrl'
          });

        $urlRouterProvider.otherwise('home');
      }
    ])
    .controller('MainCtrl', [
      '$scope',
      function($scope) {
        $scope.testText = 'test text';
      }
    ]);
})();
