(function() {
  'use strict';

  angular.module('qat-dashboard').controller('TestStatusController', [
    '$stateParams',
    '$interval',
    'testExecutor',
    function($stateParams, $interval, testExecutor) {
      var vm = this;

      vm.test = {};
      var testUpdate = $interval(function() {
        vm.test = testExecutor.all[$stateParams.uuid];
      }, 1000);
    }
  ]);
})();
