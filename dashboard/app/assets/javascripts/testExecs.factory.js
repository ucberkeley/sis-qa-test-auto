(function() {
  'use strict';

  angular.module('qat-dashboard').factory('testExecs', [
    '$resource',
    function($resource) {
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

      TestExec.create(null, function(testExec) {
        console.log('created', testExec);

        var updateFreq = 5; // seconds
        var updateInterval = setInterval(function() {
          TestExec.show({id: testExec.uuid}, function(te) {
            console.log('updated', te);
            if (te.status === 'DONE') {
              clearInterval(updateInterval);
            }
          });
        }, updateFreq * 1000);
      });

      return TestExec;
    }
  ]);
})();
