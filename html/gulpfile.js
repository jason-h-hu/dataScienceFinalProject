var gulp        = require('gulp'),
    gsass       = require('gulp-sass'),
    inject      = require('gulp-inject'),
    watch       = require('gulp-watch'),
    ngHtml2Js   = require('gulp-ng-html2js'),
    minifyHtml  = require('gulp-minify-html'),
    concat      = require('gulp-concat'),
    uglify      = require('gulp-uglify'),
    csso        = require('gulp-csso'),
    del         = require('del'),

    // Meta
    gutil       = require('gulp-util')
    merge       = require('merge-stream'),
    addsrc      = require('gulp-add-src'),
    connect     = require('gulp-connect'),
    cfg         = require('./build.config.js') // A file

/////////////////////////////////////////////////////////////

/*
// gulp should be called like this :
// $ gulp --type production
.pipe(gutil.env.type === 'production' ? uglify() : gutil.noop())
*/


// Deletes build directory
function clean() {
  return del([cfg.build+'**/*', cfg.build])
}

// Compiles vendor and app sass together into one file in build dir
function sass(){
  gulp.src(cfg.app.rootSass)
    .pipe(gsass({errLogToConsole: true, style: 'compressed'}))
    .pipe(csso())
    .pipe(concat('app.min.css'))
    .pipe(gulp.dest(cfg.build+cfg.dest.css))
    .pipe(connect.reload())
  return gulp.src(cfg.vendor.css)
    .pipe(concat('vendor.min.css'))
    .pipe(gulp.dest(cfg.build+cfg.dest.css))
    .pipe(connect.reload())
}

// Copies js files into build dir
function js(){
  return gulp.src(cfg.app.js)
    // .pipe(uglify())
    .pipe(concat('app.js'))
    .pipe(gulp.dest(cfg.build+cfg.dest.js))
    .pipe(connect.reload())
}

// Copies vendor js files into build dir
function vendor(){
  return gulp.src(cfg.vendor.js)
    .pipe(concat('vendor.min.js'))
    .pipe(gulp.dest(cfg.build+cfg.dest.js))
    .pipe(connect.reload())
}

// Copies vendor font files into build dir
function fonts(){
  return gulp.src(cfg.vendor.fonts)
    .pipe(gulp.dest(cfg.build+cfg.dest.fonts))
    .pipe(connect.reload())
}

// Converts HTML partials to minified JS and copies into build dir
function partials(files){
  return gulp.src(cfg.app.tpl)
    .pipe(minifyHtml({
        empty: true,
        spare: true,
        quotes: true
    }))
    .pipe(ngHtml2Js({
        moduleName: 'app.partials'
    }))
    .pipe(concat('partials.min.js'))
    .pipe(uglify())
    .pipe(gulp.dest(cfg.build+cfg.dest.js))
    .pipe(connect.reload())
}

// Copies assets into build dir
function assets(files) {
  return gulp.src(cfg.app.assets)
    .pipe(gulp.dest(cfg.build+cfg.dest.assets))
    .pipe(connect.reload())
}

// Injects js and css files into the root HTML file
function html() {
  var js = gulp.src(['/**/*.js', '!/**/vendor.*', '!/**/partials.min.js'], {read: false, root: cfg.build})
  var css = gulp.src(['/**/*.css', '!/**/vendor.*'], {read: false, root: cfg.build})
  var combo = merge(js, css)
    .pipe(addsrc.prepend(cfg.build+'/**/partials.min.js'))
    .pipe(addsrc.prepend(cfg.build+'/**/vendor.*'))
  return gulp.src(cfg.app.rootHtml)
    .pipe(inject(combo, {ignorePath: cfg.build}))
    .pipe(gulp.dest(cfg.build))
    .pipe(connect.reload())
}

// Used in watch - prints that watch is running the function
function go(name, func) {
  gutil.log('Watch triggered for \''+gutil.colors.green(name)+'\'')
  func()
}

// Used in watch - quits with strong message
function quit(message) {
  gutil.log(gutil.colors.red('Exiting Gulp:',message))
  process.exit(1)
}

// Tasks
gulp.task('clean', clean)
gulp.task('sass', ['clean', 'vendor'], sass)
gulp.task('js', ['clean', 'vendor'], js)
gulp.task('vendor', ['clean'], vendor)
gulp.task('fonts', ['clean', 'vendor'], fonts)
gulp.task('partials', ['clean', 'vendor'], partials)
gulp.task('assets', ['clean', 'vendor'], assets)
gulp.task('html', ['vendor', 'js', 'sass', 'assets', 'partials', 'fonts'], html)
gulp.task('watch', ['build'], function () {
  connect.server({
    root: cfg.build,
    livereload: true,
		port: 8888
  })
  watch(cfg.app.sass, function(){go('sass', sass)})
  watch(cfg.app.js, function(){go('js', js)})
  watch(cfg.app.rootHtml, function(){go('html', html)})
  watch(cfg.app.tpl, function(){go('partials', partials)})
  watch(cfg.app.assets, function(){go('assets', assets)})
  watch('./*.js', function(){quit('metafile (gulpfile or config) was changed')})
})

// Metatasks
gulp.task('build', ['clean', 'html'])
gulp.task('dev', ['build', 'watch'])
gulp.task('default', ['dev'])
