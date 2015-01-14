# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/trusty64"
  #config.vm.box_url = "https://vagrantcloud.com/ubuntu/boxes/trusty64/versions/14.04/provider/virtualbox.box"

  config.vm.synced_folder "./", "/home/vagrant/guide"

  config.vm.provision :chef_solo do |chef|
    chef.cookbooks_path = "./_chef-cookbooks"
    chef.add_recipe "guide"
  end
end
