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
      vm.getScenarioStatusCssClass = getScenarioStatusCssClass;
      vm.getStepStatusCssClass = getStepStatusCssClass;

      var scenarioStatusCssClasses = {
        'pending': 'status-pending',
        'executing': 'status-executing',
        'done': 'status-done',
        'done-with-failed': 'status-done-with-failed'
      };
      var stepStatusCssClasses = {
        'pending': 'status-pending',
        'passed': 'status-passed',
        'skipped': 'status-skipped',
        'failed': 'status-failed'
      };

      var testUpdate = $interval(function() {
        vm.test = testExecutor.all[vm.test.uuid];
      }, 100);

      function getScenarioStatusCssClass(scenario) {
        var numPending = 0, numCompleted = 0, numFailed = 0;
        scenario.steps.forEach(function(step) {
          switch (step[1]) {
            case 'pending':
              numPending ++;
              break;
            case 'failed':
              numFailed ++;
              numCompleted ++;
              break;
            case 'passed':
              numCompleted ++;
              break;
          }
        });
        if (numCompleted === 0) {
          return scenarioStatusCssClasses['pending'];
        } else if (numPending > 0) {
          return scenarioStatusCssClasses['executing'];
        } else if (numFailed > 0) {
          return scenarioStatusCssClasses['done-with-failed'];
        } else {
          return scenarioStatusCssClasses['done'];
        }
      }

      function getStepStatusCssClass(step) {
        return stepStatusCssClasses[step[1]];
      }
    }
  ]);
})();
