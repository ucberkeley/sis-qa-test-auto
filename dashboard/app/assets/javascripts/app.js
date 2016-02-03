(function() {
  'use strict';

  angular.module('qat-dashboard', [
    'ngResource',
    'ui.router',
    'ngMaterial'
  ]);

  require('./config');
  require('./dashboard.controller');
  require('./testExecutor.service');
  require('./toArray.filter');
})();
