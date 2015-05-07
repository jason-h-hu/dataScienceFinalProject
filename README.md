# Overview

Don't you hate it when you're stuck somewhere in the middle of Iowa and there's nothing but Sbarro and Taco Bell for miles? Make your next road trip delicious!

We have two servers that are needed to run Road Trip. One uses AngularJS + Bootstrap as a web framework, with Gulp as the build system behind it all. But we also have an API server serving the backend python code running via Flask.

# Quick Setup & Run
To load the webapp, do the following:

1. Setup the virtual environment & npm with `./setup` (will take ~5 min. Sorry.)
2. Start the servers with `./run` (kill with ctrl-c).
3. Visit [http://localhost:8888](http://localhost:8888) and have fun!

## CLI
If you want to load the CLI instead, do the following:

1. Setup with `./setup`
2. `source backend/bin/activate`
3. `python code/app.py -h` for instructions (flags control arguments)
4. `deactivate` when finished

## Requirements
**Important:** the following packages need to be installed for our setup and run scripts to work.
- `npm`
- `virtualenv`
- On a Mac, `brew`

# Tech Overview

## Gulp

To run a task, run `gulp <taskname>` or just `gulp` for the default (dev). All functions and tasks defined in gulpfile.js. A task is a name that is associated with a function to run. They can depend on each other (square braces after the name) and can be as complicated as necessary. Globs are strings that are specific to Gulp, signifying a pattern of files to look at. It can be anything from `filename.js` to `/folder/**/*.0.*.js`, meaning all files in subfolders of "folder" that have a file name in the form of `*.0.*.js`. Globs are used in the src and dest functions, which are the built in functions that create streams (abstractions of files) and copy the streams back out to files. The watch task runs continuously, monitoring the files for changes, rerunning functions when files that match certain globs change. Just make a glob for a file and associate it with a function, or add to the ones already defined.

## Angular

The AngularJS site has [awesome documentation](https://docs.angularjs.org/guide/concepts), and there's another [güd tutorial by Glenn](http://glennstovall.com/blog/2013/06/27/angularjs-an-overview/). The main points are easy data binding between JS and HTML, models and controllers to segment code into easy sections, and routes. Services/factories are also useful to produce objects needed. We're using an extension to Angular's builtin routing called UI Router that allows for multiple named views on one webpage (header, content, footer, for example). [That documentation](https://github.com/angular-ui/ui-router/wiki) is also quite comprehensive.

## Python API

There's a second server that must be running to serve backend requests. It's built on Flask, with routes annotated in the python code itself. It will start on port 5000. We have an API that interfaces between the backend and frontend, defined as follows:
- `/journey`: with start, end locations and departure time for the journey (optional: daily departure time, lunchtime preference, dinnertime preference, and hours driven per day)
- `/restaurants`: for given mealtime and location, gives back list of restaurants

## Files Included
- `package.json`: file that tells npm what to install to make the project run
- `bower.json`: file that tells bower what to download and install to make the project frameworks respond
- `build.config.js`: a node module containing paths and globs for Gulp
- `gulpfile.js`: the build system that runs gulp
- `app`: temporary directory that appears, holding all compiled web code
- `src`: all code for web
	- `index.html`: has top level HTML and meta information, dictating where to inject links
	- `app.scss`: imports all other SASS, and has global styles
	- `assets`: all assets for the project - currently nonexistent
	- `sass`: folder with more global sass files like fonts and colors
	- `modules`: folder with angular modules inside, each with own folder dictating module
	- `views`: folder with templates inside, each in own folder - each has a scss file dictating style for this view, a template (HTML) in a .tpl.html file, and the Angular JS that runs it in the .js file. A view needs at minimum just an html template

# Notes and Tips
- Make sure to start up both servers! The Python server needs to be running to serve API requests, whereas the gulp server needs to be running to actually serve the website
- To include other SASS files, those files must be prefixed with an underscore, and can be imported with `@import folder/file` (no underscore)
- Gulp will quit itself if you modify the gulpfile while running, so you know to start it again
- To add new modules, views, or sass files, make sure to import them in the appropriate files
	- modules are imported in `src/modules/modules.js`
	- views imported in `src/views/views.js`
	- sass imported in either `src/views/_views.scss` or `src/sass/<file>` depending on what it is
