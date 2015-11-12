(function(){
  var gulp = require('gulp'),
    jshint = require('gulp-jshint'),
    stylish = require('jshint-stylish');

  gulp.task('default', ['test']);

  gulp.task('test', ['jshint']);

  gulp.task('jshint', function() {
    return gulp.src('./**/*.js')
      .pipe(jshint())
      .pipe(jshint.reporter(stylish));
  });
})();