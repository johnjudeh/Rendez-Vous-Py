const gulp        = require('gulp'),
      csso        = require('gulp-csso'),
      babel       = require('gulp-babel'),
      uglify      = require('gulp-uglify'),
      imagemin    = require('gulp-imagemin');

// Defines the Django app dirs used to find and
// build static assets and their destination
const STATIC_DEST = 'static_build';
let djangoAppDirs = [
  'mapper/',
  'users/',
  ''
];

// Add the static subfolder to each Django app dir
djangoStaticDirs = djangoAppDirs.map(djangoAppDir => {
    return `${djangoAppDir}static`;
});


// Transpiles and minifies js files
gulp.task('js', (done) => {
  // Loop through each django static dir and build it seperately
  djangoStaticDirs.forEach(staticDir => {
    gulp.src(`${staticDir}/**/*.js`)
      .pipe(babel({
        presets: ['@babel/preset-env']
      }))
      .pipe(uglify())
      .pipe(gulp.dest(STATIC_DEST));
  });
  // Signals that the task has completed
  return done();
});


// Autoprefixes and minifies and css
gulp.task('css', (done) => {
  // Loop through each django static dir and build it seperately
  djangoStaticDirs.forEach(staticDir => {
    gulp.src(`${staticDir}/**/*.css`)
      .pipe(csso({
        restructure: true,
        sourceMap: true
      }))
      .pipe(gulp.dest(STATIC_DEST));
  });
  // Signals that the task has completed
  return done();
});


// Optimize the size of images
gulp.task('images', (done) => {
  // Loop through each django static dir and build it seperately
  djangoStaticDirs.forEach(staticDir => {
    gulp.src(`${staticDir}/**/*.png`)
      .pipe(imagemin())
      .pipe(gulp.dest(STATIC_DEST));
  });
  // Signals that the task has completed
  return done();
});


// Default taks - runs with collect static command in Django
gulp.task('default', gulp.parallel('js', 'css', 'images'));
