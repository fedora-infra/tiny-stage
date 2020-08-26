# tiny-stage

An attempt to set up freeipafas, fasjson and noggin so we can test auth without stage.

```
$ sudo dnf install ansible libvirt vagrant-libvirt vagrant-sshfs vagrant-hostmanager
$ sudo systemctl enable libvirtd
$ sudo systemctl start libvirtd
```

then run vagrant with:

```
$ vagrant up
```

IPA will be at http://ipa.tinystage.test/ and fasjson at http://fasjson.tinystage.test/fasjson


## TODO

* add ipsilon
* run IPA data gen script on provision (there is a bash alias to run it afterwards, just need to add it to the provisioning)
* add another app that uses ipsilon for identity
* add noggin itself maybe
