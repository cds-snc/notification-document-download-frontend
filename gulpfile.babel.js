// GULPFILE
// - - - - - - - - - - - - - - -
// This file processes all of the assets in the "src" folder
// and outputs the finished files in the "dist" folder.

// 1. LIBRARIES
// - - - - - - - - - - - - - - -
import gulp from 'gulp';
import gulpSass from "gulp-sass";
import nodeSass from "node-sass"
import loadPlugins from 'gulp-load-plugins';
import stylish from 'jshint-stylish';

const sassPlugin = gulpSass(nodeSass);
const plugins = loadPlugins();

// 2. CONFIGURATION
// - - - - - - - - - - - - - - -
const paths = {
  src: 'app/assets/',
  dist: 'app/static/',
  templates: 'app/templates/',
  npm: 'node_modules/',
  template: 'node_modules/@cdssnc/cds_template_jinja/',
  toolkit: 'node_modules/govuk_frontend_toolkit/'
};

// 3. TASKS
// - - - - - - - - - - - - - - -

// Move GOV.UK template resources

gulp.task('copy:notification_template:template', () => gulp.src(paths.template + 'views/layouts/notification_template.html')
  .pipe(gulp.dest(paths.templates))
);

gulp.task('copy:notification_template:css', () => gulp.src(paths.template + 'assets/stylesheets/**/*.css')
  .pipe(sassPlugin({
    outputStyle: 'compressed'
  }))
  .on('error', sassPlugin.logError)
  .pipe(plugins.cssUrlAdjuster({
    prependRelative: '/static/',
  }))
  .pipe(gulp.dest(paths.dist + 'stylesheets/'))
);

gulp.task('copy:notification_template:js', () => gulp.src(paths.template + 'assets/javascripts/**/*.js')
  .pipe(plugins.uglify())
  .pipe(gulp.dest(paths.dist + 'javascripts/'))
);

gulp.task('copy:notification_template:images', () => gulp.src(paths.template + 'assets/stylesheets/images/**/*')
  .pipe(gulp.dest(paths.dist + 'images/'))
);

gulp.task('copy:notification_template:fonts', () => gulp.src(paths.template + 'assets/stylesheets/fonts/**/*')
  .pipe(gulp.dest(paths.dist + 'fonts/'))
);

gulp.task('sass', () => gulp
  .src(paths.src + '/stylesheets/main*.scss')
  .pipe(plugins.prettyerror())
  .pipe(sassPlugin({
    outputStyle: 'compressed',
    includePaths: [
      paths.npm + 'govuk-elements-sass/public/sass/',
      paths.toolkit + 'stylesheets/'
    ]
  }))
  .pipe(plugins.base64({baseDir: 'app'}))
  .pipe(gulp.dest(paths.dist + 'stylesheets/'))
);


// Copy images

gulp.task('images', () => gulp
  .src([
    paths.src + 'images/**/*',
    paths.toolkit + 'images/**/*',
    paths.template + 'assets/images/**/*'
  ])
  .pipe(gulp.dest(paths.dist + 'images/'))
);

gulp.task('copy:notification_template:error_page', () => gulp.src(paths.src + 'error_pages/**/*')
  .pipe(gulp.dest(paths.dist + 'error_pages/'))
);


// Watch for changes and re-run tasks
gulp.task('watchForChanges', function() {
  gulp.watch(paths.src + 'javascripts/**/*', ['javascripts']);
  gulp.watch(paths.src + 'stylesheets/**/*', ['sass']);
  gulp.watch(paths.src + 'images/**/*', ['images']);
  gulp.watch('gulpfile.babel.js', ['default']);
});

gulp.task('lint:sass', () => gulp
  .src([
    paths.src + 'stylesheets/*.scss',
    paths.src + 'stylesheets/components/*.scss',
    paths.src + 'stylesheets/views/*.scss',
  ])
    .pipe(plugins.sassLint())
    .pipe(plugins.sassLint.failOnError())
);

gulp.task('lint:js', () => gulp
  .src(paths.src + 'javascripts/**/*.js')
    .pipe(plugins.jshint())
    .pipe(plugins.jshint.reporter(stylish))
    .pipe(plugins.jshint.reporter('fail'))
);

gulp.task('lint', gulp.series('lint:sass', 'lint:js'));

// Default: compile everything
gulp.task('default',
  gulp.series(
    'copy:notification_template:template',
    'copy:notification_template:images',
    'copy:notification_template:fonts',
    'copy:notification_template:css',
    'copy:notification_template:js',
    'copy:notification_template:error_page',
    'sass',
    'images'
  )
);

// Optional: recompile on changes
gulp.task('watch',
  gulp.series('default', 'watchForChanges')
);

