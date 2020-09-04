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

Ipsilon is also accessible at: https://ipsilon.tinystage.test/idp

And the tiny test application for testing out OpenID Connect with ipsilon is at https://openidtest.tinystage.test/

The fas2ipa box contains a clone of the project of the same-name, pre-configured save for the FAS
username and password. Set them in fas2ipa/config.toml and run fas2ipa like this:

```
$ poetry run fas2ipa <options>
```

## TODO

* run IPA data gen script on provision (there is a bash alias to run it afterwards, just need to add it to the provisioning)
* add an actual fedora app that uses ipsilon for identity (maybe fedocal?)
* add noggin itself maybe
