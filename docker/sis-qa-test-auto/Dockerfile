FROM ucberkeley/firefox-browser-gui

# TODO(mDibyo): Use USER root for running sudo commands and then switch back to USER developer

# sudo required since firefox-browser-gui needs specific (non-root) user to be able to use GUI
RUN sudo apt-get update && sudo apt-get install -y python3-pip
RUN sudo pip3 install selenium pytest-xdist

RUN sudo apt-get install -y curl \
    && command curl -sSL https://rvm.io/mpapis.asc | gpg --import - \
    && curl -sSL https://get.rvm.io | bash -s stable --ruby=jruby


RUN sudo sh -c 'echo "source /home/developer/.rvm/scripts/rvm" >> etc/bash.bashrc'
# RUN sudo bash -c 'echo "source /home/developer/.rvm/scripts/rvm" >> /.bashrc'
RUN bash -c "source /home/developer/.rvm/scripts/rvm && gem install bundle"

COPY execute_tests.sh /

# ENTRYPOINT exec py.test -n=$(nproc) /test

# RUN bash -c "source /home/developer/.rvm/scripts/rvm" \
#     && rvm rvmrc warning ignore /test/.rvmrc
ENTRYPOINT exec ./execute_tests.sh
