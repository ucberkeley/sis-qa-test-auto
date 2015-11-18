FROM ruby:2.2.3

MAINTAINER Dibyo Majumdar <dibyo.majumdar@gmail.com>

COPY . /dashboard/

RUN cd /dashboard \
    && bundle install  --jobs 4 --retry 3

EXPOSE 3000

WORKDIR /dashboard
ENTRYPOINT ["bin/rails", "server"]
