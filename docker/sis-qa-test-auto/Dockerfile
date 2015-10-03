FROM ucberkeley/firefox-browser-gui

# TODO(mDibyo): Use USER root for running sudo commands and then switch back to USER developer

# sudo required since firefox-browser-gui needs specific (non-root) user to be able to use GUI
RUN sudo apt-get update && sudo apt-get install -y python3-pip
RUN sudo pip3 install selenium pytest-xdist

RUN sudo apt-get install -y curl \
    && command curl -sSL https://rvm.io/mpapis.asc | gpg --import - \
    && curl -sSL https://get.rvm.io | bash -s stable --ruby=jruby

COPY Gemfile ${HOME}/Gemfile
RUN bash -c "\
    cd ${HOME} \
    && source /home/developer/.rvm/scripts/rvm \
    && gem install bundle \
    && bundle install"

COPY execute_tests.sh /
ENTRYPOINT exec ./execute_tests.sh
