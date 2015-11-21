sis_env_keys = {
  :SIS_TEST_DIR => 'SIS_TEST_DIR',
  :SIS_LOGS_DIR => 'SIS_LOGS_DIR',
  :SIS_SERVER_PORT => 'SIS_SERVER_PORT',
  :SIS_DASHBOARD_PORT => 'SIS_DASHBOARD_PORT',
  :SIS_TEST_WEBDRIVER => 'SIS_TEST_WEBDRIVER'
}

dashboard_port = 3000
if ENV.key? sis_env_keys[:SIS_DASHBOARD_PORT]
  dashboard_port = ENV[sis_env_keys[:SIS_DASHBOARD_PORT]]
end
ENV[sis_env_keys[:SIS_TEST_WEBDRIVER]] = 'poltergeist'


def get_env_file_string(env_keys)
  env_keys.values.map { |key|
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
echo "Installing QATA framework"
sudo /vagrant/scripts/install.sh

echo "Setting environment variables"
# Set environment variables
cat > ~/.env << EOF
#{get_env_file_string(sis_env_keys)}

export SIS_DASHBOARD_EXTRA_ARGS='-b 0.0.0.0'
export SIS_ENV_SET=true
EOF
source ~/.profile \
  && [ -z $SIS_ENV_SET ] \
  && echo "\n# Set SIS environment variables\n. ~/.env\n" >> ~/.profile

exit 0
SCRIPT


VAGRANTFILE_API_VERSION = '2'

Vagrant.configure('2') do |config|
  # Setup resource requirements
  config.vm.provider 'virtualbox' do |v|
    v.name = 'sis-qa-test-auto'
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

  # Setup the containers when the VM is first created
  config.vm.provision 'shell', inline: $docker_setup

  config.vm.provision 'sis', type: 'shell' do |s|
    s.privileged = false
    s.inline = $sis_setup
  end
end
