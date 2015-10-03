FROM ucberkeley/firefox-browser-gui

MAINTAINER Dibyo Majumdar <dibyo.majumdar@gmail.com>

USER root
RUN apt-get update && apt-get install -y curl \
    && command curl -sSL https://rvm.io/mpapis.asc | gpg --import - \
    && curl -sSL https://get.rvm.io | bash -s stable --ruby=jruby
RUN usermod -a -G rvm developer

USER developer

COPY Gemfile ${HOME}/Gemfile
RUN bash -c "\
    source /etc/profile.d/rvm.sh \
    && cd ${HOME} \
    && gem install bundle \
    && bundle install"

COPY execute_tests.sh /
ENTRYPOINT ["/execute_tests.sh"]
