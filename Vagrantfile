# Commands required to setup working docker environment
$setup = <<SCRIPT
# Stop and remove any existing containers
[[ $(docker ps -a -q) ]] \
  && docker stop $(docker ps -a -q) \
  || docker rm $(docker ps -a -q)

# Build docker containers
./vagrant/scripts/build.sh all

SCRIPT

SIS_DASHBOARD_PORT_ENV = 'SIS_DASHBOARD_PORT'

dashboard_port = 3000
if ENV.key? SIS_DASHBOARD_PORT_ENV
  dashboard_port = ENV[SIS_DASHBOARD_PORT_ENV]
end


VAGRANTFILE_API_VERSION = "2"

Vagrant.configure("2") do |config|

  # Setup resource requirements
  config.vm.provider "virtualbox" do |v|
    v.memory = 2048
    v.cpus = 2
    v.gui = false
  end

  # Ubuntu
  config.vm.box = "ubuntu/trusty64"

  # Forward dashboard port
  config.vm.network :forwarded_port, guest: dashboard_port, host: dashboard_port

  # Install latest docker
  config.vm.provision "docker"

  config.vm.synced_folder "./test", "/test"

  # Setup the containers when the VM is first
  # created
  config.vm.provision "shell", inline: $setup

end
