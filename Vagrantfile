# -*- mode: ruby -*-
# vi: set ft=ruby :

ENV['VAGRANT_NO_PARALLEL'] = 'yes'

domain = "tinystage.test"

machines = {
  "ipa": {
    "hostmanager.aliases": ["kerberos"],
    "autostart": true,
    "libvirt.memory": 2048,
  },
  "auth": {
    "hostmanager.aliases": ["fasjson", "ipsilon"],
    "autostart": true,
    "libvirt.memory": 1536,
    "libvirt.machine_virtual_size": 10,
  },
  "elections": {},
  "mirrormanager2": {},
  "ipaclient": {},
  "tinystage": {
    "autostart": true,
  },
  "fedocal": {},
  "src": {},
  "datagrepper": {},
  "pagure": {
        "synced_folder": "/srv/pagure/",
        "libvirt.memory": 2048,
  },
}

Vagrant.configure(2) do |config|
  config.hostmanager.enabled = true
  config.hostmanager.manage_host = true
  config.hostmanager.manage_guest = true

  machines.each do |mname, mdef|
    autostart = mdef.fetch(:autostart, false)
    mdef.delete(:autostart)
    operatingsystem = mdef.fetch(:operatingsystem, "fedora")
    mdef.delete(:operatingsystem)
    synced_folder = mdef.fetch(:synced_folder, "/vagrant")
    mdef.delete(:synced_folder)
    config.vm.define mname, autostart: autostart do |machine|
      machine.vm.box_url = "https://download.fedoraproject.org/pub/fedora/linux/releases/43/Cloud/x86_64/images/Fedora-Cloud-Base-Vagrant-libvirt-43-1.6.x86_64.vagrant.libvirt.box"
      machine.vm.box = "f43-cloud-libvirt"
      machine.vm.hostname = "#{mname}.#{domain}"

      libvirt_def = {
        "cpus": 2,
        "memory": 1024,
      }

      mdef.each do |prop, value|
        prop = prop.to_s

        if prop == "hostmanager.aliases"
          value = value.map {|n| "#{n}.#{domain}"}.compact
        end

        prop_elems = prop.split(".")

        if prop_elems[0] == "libvirt"
          dct = libvirt_def
          prop_elems[1..-2].each do |key|
            dct = dct[key]
          end
          dct[prop_elems[-1]] = value
        else
          obj = machine
          prop_elems[..-2].each do |elem_prop|
            obj = obj.send("#{elem_prop}")
          end
          obj.send("#{prop_elems[-1]}=", value)
        end
      end

      machine.vm.synced_folder ".", "/vagrant", disabled: true
      machine.vm.synced_folder "synced_folders/#{mname}", synced_folder, type: "sshfs", create: true

      machine.vm.provider :libvirt do |libvirt|
        libvirt_def.each do |prop, value|
          libvirt.send("#{prop}=", value)
        end
      end

      machine.vm.provision "ansible" do |ansible|
        ansible.playbook = "ansible/#{mname}.yml"
        ansible.config_file = "ansible/ansible.cfg"
        ansible.verbose = true
      end


    end
  end
end
