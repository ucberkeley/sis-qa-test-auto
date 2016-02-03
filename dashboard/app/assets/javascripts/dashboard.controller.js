(function() {
  'use strict';

  angular.module('qat-dashboard').controller('DashboardController', [
    'testExecutor',
    function(testExecutor) {
      var vm = this;

      vm.testExecsMap = testExecutor.all;
      vm.requestTestExec = requestTestExec;
      vm.statusCssClass = {
        'QUEUED': 'status-queued',
        'DRYRUN': 'status-dryrun',
        'EXECUTING': 'status-executing',
        'DONE': 'status-done',
        'ERROR': 'status-error'
      };

      testExecutor.addUpdateCallback(function(updatedTestExec) {
        console.log('updating Test Exec', updatedTestExec.uuid);
      });

      function requestTestExec() {
        testExecutor.new();
      }
    }
  ]);
})();
