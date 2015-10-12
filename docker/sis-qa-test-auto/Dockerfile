FROM ucberkeley/firefox-browser-gui

MAINTAINER Dibyo Majumdar <dibyo.majumdar@gmail.com>

USER root
RUN apt-get update && apt-get install -y curl \
    && command curl -sSL https://rvm.io/mpapis.asc | gpg --import - \
    && curl -sSL https://get.rvm.io | bash -s stable --ruby=jruby
RUN usermod -a -G rvm developer

RUN apt-get update && apt-get install -y python3-pip \
    && pip3 install tornado

USER developer

COPY Gemfile Gemfile.lock ${HOME}/
RUN bash -c "\
    source /etc/profile.d/rvm.sh \
    && cd ${HOME} \
    && gem install bundle \
    && bundle install"

EXPOSE 8421

COPY server /server/
COPY run_server.sh /
ENTRYPOINT ["/run_server.sh"]
