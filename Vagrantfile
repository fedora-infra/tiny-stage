# -*- mode: ruby -*-
# vi: set ft=ruby :
ENV['VAGRANT_NO_PARALLEL'] = 'yes'

Vagrant.configure(2) do |config|
  config.hostmanager.enabled = true
  config.hostmanager.manage_host = true
  config.hostmanager.manage_guest = true

  config.vm.define "freeipa" do |freeipa|
    freeipa.vm.box_url = "https://download.fedoraproject.org/pub/fedora/linux/releases/32/Cloud/x86_64/images/Fedora-Cloud-Base-Vagrant-32-1.6.x86_64.vagrant-libvirt.box"
    freeipa.vm.box = "f32-cloud-libvirt"
    freeipa.vm.hostname = "ipa.tinystage.test"
    freeipa.hostmanager.aliases = ("kerberos.tinystage.test")
    freeipa.vm.synced_folder ".", "/vagrant", disabled: true
    freeipa.vm.provider :libvirt do |libvirt|
      libvirt.cpus = 2
      libvirt.memory = 2048
    end

    freeipa.vm.provision "ansible" do |ansible|
      ansible.playbook = "ansible/freeipa.yml"
    end
  end

  config.vm.define "fasjson" do |fasjson|
    fasjson.vm.box_url = "https://download.fedoraproject.org/pub/fedora/linux/releases/32/Cloud/x86_64/images/Fedora-Cloud-Base-Vagrant-32-1.6.x86_64.vagrant-libvirt.box"
    fasjson.vm.box = "f32-cloud-libvirt"
    fasjson.vm.hostname = "fasjson.tinystage.test"
    fasjson.vm.synced_folder ".", "/vagrant", disabled: true

    fasjson.vm.provider :libvirt do |libvirt|
      libvirt.cpus = 2
      libvirt.memory = 2048
    end

    fasjson.vm.provision "ansible" do |ansible|
      ansible.playbook = "ansible/fasjson.yml"
    end
  end

  config.vm.define "ipsilon" do |ipsilon|
    ipsilon.vm.box_url = "https://download.fedoraproject.org/pub/fedora/linux/releases/32/Cloud/x86_64/images/Fedora-Cloud-Base-Vagrant-32-1.6.x86_64.vagrant-libvirt.box"
    ipsilon.vm.box = "f32-cloud-libvirt"
    ipsilon.vm.hostname = "ipsilon.tinystage.test"
    ipsilon.vm.synced_folder ".", "/vagrant", disabled: true

    ipsilon.vm.provider :libvirt do |libvirt|
      libvirt.cpus = 2
      libvirt.memory = 2048
    end

    ipsilon.vm.provision "ansible" do |ansible|
      ansible.playbook = "ansible/ipsilon.yml"
    end
  end

  config.vm.define "openidtest" do |openidtest|
    openidtest.vm.box_url = "https://download.fedoraproject.org/pub/fedora/linux/releases/32/Cloud/x86_64/images/Fedora-Cloud-Base-Vagrant-32-1.6.x86_64.vagrant-libvirt.box"
    openidtest.vm.box = "f32-cloud-libvirt"
    openidtest.vm.hostname = "openidtest.tinystage.test"
    openidtest.vm.synced_folder ".", "/vagrant", disabled: true

    openidtest.vm.provider :libvirt do |libvirt|
      libvirt.cpus = 2
      libvirt.memory = 2048
    end

    openidtest.vm.provision "ansible" do |ansible|
      ansible.playbook = "ansible/openidtest.yml"
    end
  end

end
