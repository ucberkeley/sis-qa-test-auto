task :travis do
  puts 'Running JSHint - detect errors and potential problems in JavaScript code'
  system ('jshint .')
  raise "JSHint failed with error status #{$?.exitstatus}!" unless $?.exitstatus == 0
end