(function() {
  'use strict';

  angular.module('qat-dashboard').controller('DashboardController', [
    '$scope',
    function($scope) {
      $scope.testText = 'new test text';
    }
  ]);
})();
