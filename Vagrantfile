# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|

  config.vm.box = "ubuntu/trusty64"
  config.vm.network "forwarded_port", guest: 80, host: 80
  config.vm.network "private_network", ip: "192.168.33.10"

  config.vm.synced_folder "./chatservice", "/home/simplechat/"
  config.vm.synced_folder "./static", "/var/www/simplechat/static"
  config.vm.synced_folder ".", "/basedir"

  config.vm.provider "virtualbox" do |vb|
     # Display the VirtualBox GUI when booting the machine
     # vb.gui = true

     # Customize the amount of memory on the VM:
     vb.memory = "512"
  end

  config.vm.provision "shell", path: "provision.sh"
end
