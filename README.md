This project contains the content for the Study Guide for CMPT 165 at [Simon Fraser University](http://www.sfu.ca/).

## Building the Guide

In an Ubuntu/Debian system, you can install the build dependencies: `apt-get install python-jinja2 ruby-sass inkscape graphicsmagick optipng pngquant python-scour python-html5lib`

Or you can use [VirtualBox](https://www.virtualbox.org/) and [Vagrant](http://www.vagrantup.com/) (and the Vagrantfile in the project) to create a box that's ready to go.

Run the command `make`. Open the file `_site/index.html`.

## Viewing Drafts

I am regularly uploading the Guide as I work on it to [http://www.cs.sfu.ca/~ggbaker/165-draft/](http://www.cs.sfu.ca/~ggbaker/165-draft/) (temporarly location). If you just want to see what's in here, that will be easier than building the whole thing.
