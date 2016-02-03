(function() {
  'use strict';

  angular.module('qat-dashboard').controller('DashboardController', [
    'testExecutor',
    function(testExecutor) {
      var vm = this;

      vm.testExecsMap = testExecutor.all;
      vm.requestTestExec = requestTestExec;
      vm.extractDateFromUuid = extractDateFromUuid;
      vm.statusCssClass = {
        'QUEUED': 'status-queued',
        'DRYRUN': 'status-dryrun',
        'EXECUTING': 'status-executing',
        'DONE': 'status-done',
        'ERROR': 'status-error'
      };

      function requestTestExec() {
        testExecutor.new();
      }

      function extractDateFromUuid(uuid) {
        var year = parseInt(uuid.substring(0, 4));
        var month = parseInt(uuid.substring(4, 6));
        var day = parseInt(uuid.substring(6, 8));
        var hour = parseInt(uuid.substring(8, 10));
        var minute = parseInt(uuid.substring(10, 12));
        var second = parseInt(uuid.substring(12, 14));
        var millisecond = parseInt(uuid.substring(14, 17));
        return new Date(year, month, day, hour, minute, second, millisecond);
      }
    }
  ]);
})();
