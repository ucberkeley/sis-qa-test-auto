(function() {
  'use strict';

  angular.module('qat-dashboard').controller('DashboardController', [
    'testExecsFactory',
    function(testExecsFactory) {
      var vm = this;

      vm.testExecsMap = {};
      vm.requestTestExecs = function() {
        testExecsFactory.create(null, function(testExec) {
          vm.testExecsMap[testExec.uuid] = testExec;
        });
      };

      testExecsFactory.index(null, function(testExecsList) {
        testExecsList.forEach(function(testExec) {
          vm.testExecsMap[testExec.uuid] = testExec;
        });
      });
    }
  ]);
})();
