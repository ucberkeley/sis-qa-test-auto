(function() {
  'use strict';

  var gulp = require('gulp');
  var browserify = require('browserify');
  var source = require('vinyl-source-stream');
  var scss = require('gulp-scss');
  var jshint = require('gulp-jshint');
  var jscs = require('gulp-jscs');
  var sassLint = require('gulp-sass-lint');

  var paths = {
    self: 'gulpfile.js',
    src: {
      js: 'app/assets/javascripts/*.js',
      scss: 'app/assets/stylesheets/*.scss'
    },
    dest: {
      js: 'public/js',
      css: 'public/css'
    }
  };

  gulp.task('default', ['all']);

  gulp.task('all', function(callback) {
    var runSequence = require('run-sequence');
    runSequence(
      'test',
      'build',
      callback
    );
  });

  gulp.task('test', ['jscs', 'jshint', 'sass-lint']);

  gulp.task('build', ['browserify', 'scss']);

  gulp.task('jshint', function() {
    return gulp.src([paths.self, paths.src.js])
      .pipe(jshint())
      .pipe(jshint.reporter('jshint-stylish'))
      .pipe(jshint.reporter('fail'));
  });

  gulp.task('jscs', function() {
    return gulp.src([paths.self, paths.src.js])
      .pipe(jscs())
      .pipe(jscs.reporter('jscs-stylish'))
      .pipe(jscs.reporter('fail'));
  });

  gulp.task('sass-lint', function() {
    gulp.src(paths.src.scss)
      .pipe(sassLint())
      .pipe(sassLint.format())
      .pipe(sassLint.failOnError());
  });

  gulp.task('browserify', function() {
    return browserify(['app/assets/javascripts/app.js'], {
      debug: true
    })
      .bundle()
      .pipe(source('app.js'))
      .pipe(gulp.dest(paths.dest.js));
  });

  gulp.task('scss', function() {
    return gulp.src('app/assets/stylesheets/app.scss')
      .pipe(scss())
      .pipe(gulp.dest(paths.dest.css));
  });
})();
