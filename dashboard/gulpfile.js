(function() {
  'use strict';

  var gulp = require('gulp');
  var browserify = require('browserify');
  var source = require('vinyl-source-stream');
  var jshint = require('gulp-jshint');
  var jscs = require('gulp-jscs');

  gulp.task('default', ['all']);

  gulp.task('all', function(callback) {
    var runSequence = require('run-sequence');

    runSequence(
      'test',
      'build',
      callback
    );
  });

  gulp.task('test', ['jscs', 'jshint']);

  gulp.task('build', ['browserify']);

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

  gulp.task('browserify', function() {
    return browserify([
      './app/assets/javascripts/app.js',
      './app/assets/javascripts/config.js',
      './app/assets/javascripts/dashboard.controller.js',
      './app/assets/javascripts/testExecutor.service.js',
      './app/assets/javascripts/toArray.filter.js'
    ], {
      debug: true,
      extensions: ['js']
    })
      .bundle()
      .pipe(source('app.js'))
      .pipe(gulp.dest('public/assets/javascript'));
  });
})();
