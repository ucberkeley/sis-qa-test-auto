FROM ruby:2.2.3

MAINTAINER Dibyo Majumdar <dibyo.majumdar@gmail.com>

# Install node.js
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    nodejs-legacy \
    npm

EXPOSE 3000

COPY . /dashboard/
RUN cd /dashboard \
    && bundle install --jobs 4 --retry 3 \
    && npm install

ENTRYPOINT ["/dashboard/run_dashboard.sh"]
