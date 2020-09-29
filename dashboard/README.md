# Test Execution Service Dashboard

## Instructions for running
1. [Install Ruby](https://www.ruby-lang.org/en/documentation/installation/), preferably, a version after 1.9.
1. Run `bundle install` in this directory (you may have to run `gem install bundle` first).
1. Run `npm install --production` in this directory, followed by `gulp build`.
1. Run `bin/rails server` in this directory.
1. Visit `http://localhost:3000` in the browser to start using the dashboard.

### Issues with LibV8 LibV8 and TheRubyRacer Gem

If you're having issues running 'bundle install' run:

```shell
gem install bundler --version="1.3.6"
bundle config build.libv8 --with-system-v8
bundle config build.therubyracer --with-v8-dir=$(brew --prefix v8@3.15)
bundle _1.3.6_ install
```

## Note
The dashboard will not function without the [qatserver](../qatserver/README.md).
