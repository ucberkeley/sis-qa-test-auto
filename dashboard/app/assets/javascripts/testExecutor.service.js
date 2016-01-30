(function() {
  'use strict';

  angular.module('qat-dashboard').service('testExecutor', [
    'testExecsFactory',
    function(testExecsFactory) {
      var service = this;

      service.all = {};
      service.new = newTestExec;
      service.delete = deleteTestExec;

      var testExecUpdateIntervalPeriod = 5; // seconds

      // Populate all
      testExecsFactory.index(null, function(testExecsList) {
        testExecsList.forEach(function(testExec) {
          service.all[testExec.uuid] = testExec;
          if (testExec.status !== 'DONE') {
            updateTestExec(testExec.uuid);
          }
        });
      });

      function newTestExec() {
        testExecsFactory.create(null, function(testExec) {
          service.all[testExec.uuid] = testExec;
          updateTestExec(testExec.uuid);
        }, function(httpResponse) {
          console.error('error while requesting new testExec: ' + httpResponse.code);
        });
      }

      function updateTestExec(uuid) {
        var updateInterval = setInterval(function() {
          testExecsFactory.show({id: uuid}, function(updatedTestExec) {
            if (updatedTestExec.status === 'DONE') {
              clearInterval(updateInterval);
            }
            service.all[uuid] = updatedTestExec;
          });
        }, testExecUpdateIntervalPeriod * 1000);
      }

      function deleteTestExec(uuid) {
        testExecsFactory.delete({id: uuid}, function(testExec) {
          delete service.all[testExec];
        });
      }
    }
  ]);

  angular.module('qat-dashboard').factory('testExecsFactory', [
    '$resource',
    function($resource) {
      return $resource('/test_execs/:id', null, {
        'index': {
          method: 'GET',
          isArray: true
        },
        'create': {
          method: 'POST'
        },
        'show': {
          method: 'GET'
        },
        'delete': {
          method: 'DELETE'
        }
      });
    }
  ]);
})();
