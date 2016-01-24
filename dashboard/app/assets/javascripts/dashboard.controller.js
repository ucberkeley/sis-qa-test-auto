(function() {
  'use strict';

  angular.module('qat-dashboard').controller('DashboardController', [
    'testExecs',
    function(testExecs) {
      var vm = this;

      vm.testText = 'new test text';
    }
  ]);
})();
