(function() {
  'use strict';

  angular.module('qat-dashboard').controller('TestStatusController', [
    '$stateParams',
    '$interval',
    'testExecutor',
    function($stateParams, $interval, testExecutor) {
      var vm = this;

      vm.test = {
        uuid: $stateParams.uuid,
        steps: [],
        counters: []
      };
      var testUpdate = $interval(function() {
        vm.test = testExecutor.all[vm.test.uuid];
      }, 1000);
    }
  ]);
})();
