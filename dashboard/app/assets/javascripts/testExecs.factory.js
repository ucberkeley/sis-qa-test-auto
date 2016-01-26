(function() {
  'use strict';

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
