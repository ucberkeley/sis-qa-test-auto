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
        'pending': 'scenario-status-pending',
        'executing': 'scenario-status-executing',
        'done': 'scenario-status-done',
        'done-with-failed': 'scenario-status-done-with-failed'
      };
      var stepStatusCssClasses = {
        'pending': 'step-status-pending',
        'passed': 'step-status-passed',
        'skipped': 'step-status-skipped',
        'failed': 'step-status-failed'
      };

      var testUpdateInterval = 0.2; // seconds
      var testUpdate = $interval(function() {
        vm.test = testExecutor.all[vm.test.uuid];
        if (vm.test.status === 'DONE') {
          vm.currScenario = null;
          $interval.cancel(testUpdate);
          return;
        }

        vm.test.steps.forEach(function(file) {
          file.scenarios.forEach(function(scenario) {
            vm.scenarioOpenMap[scenario.name] =
              vm.scenarioOpenMap[scenario.name] || false;
            if (scenario.steps[0].status === 'pending') {
              return;
            }
            if (scenario.steps[scenario.steps.length - 1].status === 'pending') {
              vm.currScenario = scenario;
            }
          });
        });

      }, testUpdateInterval * 1000);

      function getScenarioStatusCssClass(scenario) {
        var numPending = 0, numCompleted = 0, numFailed = 0;
        scenario.steps.forEach(function(step) {
          switch (step.status) {
            case 'pending':
              numPending++;
              break;
            case 'failed':
              numFailed++;
              numCompleted++;
              break;
            case 'passed':
              numCompleted++;
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
        return stepStatusCssClasses[step.status];
      }
    }
  ]);
})();
