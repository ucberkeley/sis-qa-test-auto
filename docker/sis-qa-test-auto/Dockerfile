FROM firefox-browser-gui

# sudo required since firefox-browser-gui needs specific (non-root) user to be able to use GUI
RUN sudo apt-get update && sudo apt-get install -y python3-pip # ipython
RUN sudo pip3 install selenium pytest-xdist

ENTRYPOINT exec py.test -n=$(nproc) /test
