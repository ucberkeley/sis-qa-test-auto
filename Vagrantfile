# Commands required to setup working docker environment
$setup = <<SCRIPT
# Stop and remove any existing containers
[[ $(docker ps -a -q) ]] \
  && docker stop $(docker ps -a -q) \
  || docker rm $(docker ps -a -q)

docker pull ucberkeley/sis-qa-test-auto

SCRIPT

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure("2") do |config|

  # Setup resource requirements
  config.vm.provider "virtualbox" do |v|
    v.memory = 2048
    v.cpus = 2
    v.gui = true
  end

  # Ubuntu
  config.vm.box = "ubuntu/trusty64"

  # Install latest docker
  config.vm.provision "docker"

  config.vm.synced_folder "./test", "/test"

  # Setup the containers when the VM is first
  # created
  config.vm.provision "shell", inline: $setup

end