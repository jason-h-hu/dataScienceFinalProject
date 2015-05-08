/**
 * This file/module contains all configuration for the build process.
 */
module.exports = {
  build: 'app/',

  // File patterns for app code
  app: {
    js: ['src/**/*.js', 'src/app.js'],
    assets: ['src/assets/**/*'],
    tpl: ['src/**/*.tpl.html'],
    rootHtml: 'src/index.html',
    sass: ['src/**/*.scss'],
    rootSass: 'src/app.scss'
  },

  // Folders to build into
  dest: {
    js: 'js/',
    css: 'css/',
    assets: 'assets/'
  },

  // Vendor code for the build process (Angular + Bootstrap)
  vendor: {
    js: [
      'bower_components/**/angular.min.js',
      'bower_components/**/ui-bootstrap.min.js',
      'bower_components/**/ui-bootstrap-tpls.min.js',
      'bower_components/**/release/angular-ui-router.min.js',
      'bower_components/**/ui-utils.min.js',
			'bower_components/**/angular-progress-arc.min.js',
      'bower_components/**/angular-google-maps.min.js',
      'bower_components/**/lodash.underscore.min.js'
    ],
    css:[
      'bower_components/**/bootstrap.min.css'
    ]
  }
};
