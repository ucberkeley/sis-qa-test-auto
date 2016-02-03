(function() {
  'use strict';

  angular.module('qat-dashboard').controller('DashboardController', [
    'testExecutor',
    function(testExecutor) {
      var vm = this;

      vm.testExecsMap = testExecutor.all;
      vm.requestTestExec = requestTestExec;
      vm.getDate = getDate;
      vm.getStatusCssClass = getStatusCssClass;

      var statusCssClasses = {
        'QUEUED': 'status-queued',
        'DRYRUN': 'status-dryrun',
        'EXECUTING': 'status-executing',
        'DONE': 'status-done',
        'DONE_WITH_FAILED': 'status-done-with-failed',
        'ERROR': 'status-error'
      };

      function requestTestExec() {
        testExecutor.new();
      }

      function getDate(testExec) {
        var uuid = testExec.uuid;

        var year = parseInt(uuid.substring(0, 4));
        var month = parseInt(uuid.substring(4, 6));
        var day = parseInt(uuid.substring(6, 8));
        var hour = parseInt(uuid.substring(8, 10));
        var minute = parseInt(uuid.substring(10, 12));
        var second = parseInt(uuid.substring(12, 14));
        var millisecond = parseInt(uuid.substring(14, 17));
        return new Date(year, month, day, hour, minute, second, millisecond);
      }

      function getStatusCssClass(testExec) {
        var status = testExec.status;
        if (status === 'DONE' && testExec.counters.failed > 0) {
          status = 'DONE_WITH_FAILED';
        }
        return statusCssClasses[status];
      }
    }
  ]);
})();
