(function() {
  'use strict';

  angular.module('qat-dashboard').service('testExecutor', [
    '$resource',
    function($resource) {
      var service = this;

      service.all = {};
      service.new = newTestExec;
      service.delete = deleteTestExec;

      var TestExec = $resource('/test_execs/:id', null, {
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
      var testExecUpdateIntervalPeriod = 1; // seconds

      // Populate all
      TestExec.index(null, function(testExecsList) {
        testExecsList.forEach(function(testExec) {
          service.all[testExec.uuid] = testExec;
          if (testExec.status !== 'DONE') {
            updateTestExec(testExec.uuid);
          }
        });
      });

      function newTestExec() {
        TestExec.create(null, function(testExec) {
          service.all[testExec.uuid] = testExec;
          updateTestExec(testExec.uuid);
        }, function(httpResponse) {
          console.error('error while requesting new testExec: ' + httpResponse.code);
        });
      }

      function updateTestExec(uuid) {
        var updateInterval = setInterval(function() {
          TestExec.show({id: uuid}, function(updatedTestExec) {
            if (updatedTestExec.status === 'DONE' || updatedTestExec.status === 'ERRORED') {
              clearInterval(updateInterval);
            }
            service.all[uuid] = updatedTestExec;
          });
        }, testExecUpdateIntervalPeriod * 1000);
      }

      function deleteTestExec(uuid) {
        TestExec.delete({id: uuid}, function(testExec) {
          delete service.all[testExec];
        });
      }
    }
  ]);
})();
