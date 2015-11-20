SIS_TEST_DIR_ENV = 'SIS_TEST_DIR'
SIS_LOGS_DIR_ENV = 'SIS_LOGS_DIR'
SIS_SERVER_PORT_ENV = 'SIS_SERVER_PORT'
SIS_DASHBOARD_PORT_ENV = 'SIS_DASHBOARD_PORT'
SIS_TEST_WEBDRIVER_ENV = 'SIS_TEST_WEBDRIVER'

sis_env_keys = [
  SIS_TEST_DIR_ENV,
  SIS_LOGS_DIR_ENV,
  SIS_SERVER_PORT_ENV,
  SIS_DASHBOARD_PORT_ENV,
  SIS_TEST_WEBDRIVER_ENV
]

dashboard_port = 3000
if ENV.key? SIS_DASHBOARD_PORT_ENV
  dashboard_port = ENV[SIS_DASHBOARD_PORT_ENV]
end
ENV[SIS_TEST_WEBDRIVER_ENV] = 'poltergeist'


def get_env_file_string(env_keys)
  env_keys.map { |key|
    if ENV.key? key
      "export #{key}=#{ENV[key]}"
    else
      "unset #{key}"
    end
  }.join("\n")
end


$docker_setup = <<SCRIPT
# Stop and remove any existing containers
[[ $(docker ps -a -q) ]] \
  && docker stop $(docker ps -a -q) \
  || docker rm $(docker ps -a -q)

# Build docker containers
/vagrant/scripts/build.sh all
SCRIPT

$sis_setup = <<SCRIPT
# Install QATA framework
# sudo /vagrant/scripts/install.sh

# Set environment variables
cat > ~/.env << EOF
#{get_env_file_string(sis_env_keys)}
SIS_ENV_SET=true
EOF

source ~/.profile \
  && [ -z $SIS_ENV_SET ] \
  && echo "source ~/.env" >> ~/.profile
SCRIPT


VAGRANTFILE_API_VERSION = '2'

Vagrant.configure('2') do |config|
  # Setup resource requirements
  config.vm.provider 'virtualbox' do |v|
    v.memory = 2048
    v.cpus = 2
    v.gui = false
  end

  # Ubuntu
  config.vm.box = 'ubuntu/trusty64'

  # Forward dashboard port
  config.vm.network :forwarded_port, guest: dashboard_port, host: dashboard_port

  # Install latest docker
  config.vm.provision 'docker'

  config.vm.synced_folder './test', '/test'

  # config.ssh.shell = 'bash -c "BASH_ENV=/etc/profile exec bash"'
  config.vm.provision "fix-no-tty", type: "shell" do |s|
    s.privileged = false
    s.inline = "sudo sed -i '/tty/!s/mesg n/tty -s \\&\\& mesg n/' /root/.profile"
  end

  # Setup the containers when the VM is first created
  # config.vm.provision 'shell', inline: $docker_setup
  config.vm.provision 'shell', inline: $sis_setup
end
