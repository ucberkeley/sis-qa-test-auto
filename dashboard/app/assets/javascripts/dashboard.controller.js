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

      var uuidDateRe = /(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})(\d{3})/;
      var statusCssClasses = {
        'QUEUED': 'status-queued',
        'DRYRUN': 'status-dryrun',
        'EXECUTING': 'status-executing',
        'DONE': 'status-done',
        'DONE_WITH_FAILED': 'status-done-with-failed',
        'ERRORED': 'status-errored'
      };

      function requestTestExec() {
        testExecutor.new();
      }

      function getDate(testExec) {
        var dateArgs = uuidDateRe.exec(testExec.uuid).slice(1, 8).map(function(arg) {
          return parseInt(arg, 10);
        });
        dateArgs[1] -= 1;
        /*jshint -W058 */
        return new (Function.prototype.bind.apply(Date, [null].concat(dateArgs)));
        /*jshint +W058 */
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
