# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.define "tribes" do |c|
    c.vm.box = "ttmb-box"
    c.vm.box_url = "http://cloud-images.ubuntu.com/vagrant/precise/current/precise-server-cloudimg-amd64-vagrant-disk1.box"
    c.vm.network :private_network, ip: "192.168.69.200"
    c.vm.network "forwarded_port", guest: 8080, host: 8080

    c.vm.provision "ansible" do |ansible|
      ansible.playbook = "ansible/vagrant.yml"
      ansible.inventory_path = "ansible/inventory/vagrant"
      ansible.sudo = true
      ansible.verbose = 'vvvv'
      ansible.host_key_checking = false
      ansible.limit = 'all'
    end
    c.vm.provider :virtualbox do |vb|
      vb.customize ["modifyvm", :id, "--memory", "512"]
      vb.customize ["modifyvm", :id, "--cpus", "1"]
    end
  end
end
