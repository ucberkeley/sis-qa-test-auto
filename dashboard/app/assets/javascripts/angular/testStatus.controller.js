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
      vm.scenarioOpenMap = {};
      vm.currScenario = null;
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

        vm.test.steps.forEach(function(file) {
          file.scenarios.forEach(function(scenario) {
            vm.scenarioOpenMap[scenario.name] =
              vm.scenarioOpenMap[scenario.name] || false;
            if (scenario.steps[0][1] === 'pending') {
            } else if (scenario.steps[scenario.steps.length-1][1] === 'pending') {
              vm.currScenario = scenario;
            }
          });
        });
        if (vm.test.status === 'DONE') {
          vm.currScenario = null;
          $interval.cancel(testUpdate);
        }

      }, 200);

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
