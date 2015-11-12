(function() {
  'use strict';

  var teuElement = $('#test-exec-uuid');
  var tesElement = $('#test-exec-status');
  var tecElement = $('#test-exec-counters');
  var testExecUUID = teuElement.html();

  function updateTestExec(testExec) {
    tesElement.html(testExec.status);
    if ('total' in testExec.counters) {
      var counters = testExec.counters;
      var countersString = '';
      // passed
      for (var i = 0; i < counters.passed; i++) {
        countersString += '+';
      }
      // failed
      for (i = 0; i < counters.failed; i++) {
        countersString += '*';
      }
      // skipped
      for (i = 0; i < counters.skipped; i++) {
        countersString += '-';
      }
      // rest adding up to total
      for (i = countersString.length; i < counters.total; i++) {
        countersString += '.';
      }
      tecElement.html(countersString);
    }
  }

  if (teuElement.length) {
    if (tesElement.html() !== 'DONE') {
      var updateFreq = 5;
      var updateInterval = setInterval(function() {
        if (!$('#test-exec-uuid').length || tesElement.html() === 'DONE') {
          clearInterval(updateInterval);
          return;
        }
        $.ajax({
          url: '/test_execs/' + testExecUUID,
          dataType: 'json'
        }).done(updateTestExec);
      }, updateFreq * 1000);
    }

    updateTestExec($('#test-exec-info').data('testExec'));
  }
})();
