(function() {
  var teuElement = $('#test-exec-uuid');
  var tesElement = $('#test-exec-status');
  var tecElement = $('#test-exec-counters');
  var testExecUUID = teuElement.html();
  
  function updateTestExec(testExec) {
      tesElement.html(testExec.status);
      if ('total' in testExec.counters) {
          var counters = testExec.counters;
          var counters_string = '';
          // passed
          for (var i = 0; i < counters.passed; i++) { counters_string += '+'; }
          // failed
          for (i = 0; i < counters.failed; i++) { counters_string += '*'; }
          // skipped
          for (i = 0; i < counters.skipped; i++) { counters_string += '-'; }
          // rest adding up to total
          for (i = counters_string.length; i < counters.total; i++) { counters_string += '.'; }
          tecElement.html(counters_string);
      }
  }
  
  if (teuElement.length) {
      if (tesElement.html() !== 'DONE') {
          var updateFreq = 5;
          var updateInterval = setInterval(function () {
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
