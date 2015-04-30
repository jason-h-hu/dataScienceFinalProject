# Overview

We're using AngularJS + Bootstrap as a web framework, with Gulp as the build system behind it all.

# Getting Started

Install npm if not already installed. Then, install gulp globally with 'npm install -g gulp'. Then, in this directory, run 'npm install'. It should take a really long time to download everything. Once that's done, run 'bower install'. With those steps, you should have a working system.

Test it by running 'gulp'. There should be a column of text showing each of the steps it's executed, the last lines showing that a server started on a given port. If not, troubleshoot!

# Gulp

To run a task, run gulp <taskname> or just gulp for the default (dev). All functions and tasks defined in gulpfile.js. A task is a name that is associated with a function to run. They can depend on each other (square braces after the name) and can be as complicated as necessary. Globs are strings that are specific to Gulp, signifying a pattern of files to look at. It can be anything from "filename.js" to "/folder/**/*.0.*.js", meaning all files in subfolders of "folder" that have a file name in the form *.0.*.js. They are used in the src and dest functions, the built in functions that create streams (abstractions of files) and copy the streams back out to file. The watch task is special, since it runs continuously and reruns functions when certain files change. Just make a glob for a file and associate it with a function.

# Angular

Details needed here.

# Files Included
- package.json: file that tells npm what to install to make the project run
- bower.json: file that tells bower what to download and install to make the project frameworks respond
- build.config.js: a node module containing paths and globs for Gulp
- gulpfile.js: the build system that runs gulp
- app: temporary directory that appears, holding all compiled web code
- src: all code for web
	- index.html: has top level HTML and meta information, dictating where to inject links
	- app.scss: imports all other SASS, and has global styles
	- sass: folder with more global sass files like fonts and colors
	- modules: folder with angular modules inside, each with own folder dictating module
	- views: folder with templates inside, each in own folder
		- each has a scss file dictating style for this view, a template (HTML) in a .tpl.html file, and the Angular JS that runs it in the .js file. A view needs at minimum just an html template

# Important Notes
- To include other SASS files, those files must be prefixed with an underscore
- Gulp will selfdestruct and quit if you modify the gulpfile while running
- To add assets, create a new folder in src called assets and put your files inside
- To add new modules, views, or sass files, make sure to import them in the appropriate file (modules in modules/modules.js, views in views/views.js, sass in views/_views.scss or sass/*)
