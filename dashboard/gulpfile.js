(function() {
  'use strict';

  var gulp = require('gulp');
  var jshint = require('gulp-jshint');
  var jscs = require('gulp-jscs');

  gulp.task('default', ['test']);

  gulp.task('test', [
    'jscs',
    'jshint'
  ]);

  gulp.task('jshint', function() {
    return gulp.src('./**/*.js')
      .pipe(jshint())
      .pipe(jshint.reporter('jshint-stylish'))
      .pipe(jshint.reporter('fail'));
  });

  gulp.task('jscs', function() {
    return gulp.src('./**/*.js')
      .pipe(jscs())
      .pipe(jscs.reporter('jscs-stylish'))
      .pipe(jscs.reporter('fail'));
  });
})();
