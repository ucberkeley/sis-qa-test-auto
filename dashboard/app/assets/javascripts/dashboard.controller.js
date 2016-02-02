(function() {
  'use strict';

  angular.module('qat-dashboard').controller('DashboardController', [
    'testExecutor',
    function(testExecutor) {
      var vm = this;

      vm.testExecsMap = testExecutor.all;
      vm.requestTestExec = requestTestExec;

      testExecutor.addUpdateCallback(function(updatedTestExec) {
        console.log('updating Test Exec', updatedTestExec.uuid);
      });

      function requestTestExec() {
        testExecutor.new();
      }
    }
  ]);
})();
