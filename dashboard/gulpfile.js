(function() {
  'use strict';

  var gulp = require('gulp');
  var jshint = require('gulp-jshint');
  var jshintStylish = require('jshint-stylish');
  var jscs = require('gulp-jscs');
  var jscsStylish = require('jscs-stylish');

  gulp.task('default', ['test']);

  gulp.task('test', [
    'jscs',
    'jshint'
  ]);

  gulp.task('jshint', function() {
    return gulp.src('./**/*.js')
      .pipe(jshint())
      .pipe(jshint.reporter(jshintStylish));
  });

  gulp.task('jscs', function() {
    return gulp.src('./**/*.js')
      .pipe(jscs())
      .pipe(jscs.reporter(jscsStylish));
  });
})();
