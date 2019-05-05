const gulp        = require('gulp'),
      csso        = require('gulp-csso'),
      babel       = require('gulp-babel'),
      uglify      = require('gulp-uglify'),
      imagemin    = require('gulp-imagemin');

// Pulls the STATIC_ROOT and RENDEZVOUS_APPS env variables if they exists.
// Django sets these before running the gulp build process
const STATIC_ROOT = process.env.STATIC_ROOT || 'static_build';
let djangoAppsStr = process.env.RENDEZVOUS_APPS || 'mapper';
djangoApps = djangoAppsStr.split(':');


// Transpiles and minifies js files
gulp.task('js', (done) => {
  // Loop through each django app and build it seperately
  djangoApps.forEach(djangoApp => {
    srcFolder = `${STATIC_ROOT}/${djangoApp}/js`;
    gulp.src(`${srcFolder}/**/*.js`)
      .pipe(babel({
        presets: ['@babel/preset-env']
      }))
      .pipe(uglify())
      .pipe(gulp.dest(srcFolder));
  });
  // Signals that the task has completed
  return done();
})


// Autoprefixes and minifies and css
gulp.task('css', (done) => {
  // Loop through each django app and build it seperately
  djangoApps.forEach(djangoApp => {
    srcFolder = `${STATIC_ROOT}/${djangoApp}/css`;
    gulp.src(`${srcFolder}/**/*.css`)
      .pipe(csso({
        restructure: true,
        sourceMap: true
      }))
      .pipe(gulp.dest(srcFolder));
  });
  // Signals that the task has completed
  return done();
});


// Optimize the size of images
gulp.task('images', (done) => {
  // Loop through each django app and build it seperately
  djangoApps.forEach(djangoApp => {
    srcFolder = `${STATIC_ROOT}/${djangoApp}/imgs`;
    gulp.src(`${srcFolder}/**/*.png`)
      .pipe(imagemin())
      .pipe(gulp.dest(srcFolder));
  });
  // Signals that the task has completed
  return done();
});


// Default taks - runs with collect static command in Django
gulp.task('default', gulp.parallel('js', 'css', 'images'));
