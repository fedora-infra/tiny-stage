# tiny-stage

tiny-stage is a way to create a development / testing environment for Fedora Infrastrucure applications.
Testing and developing Fedora Infra applications can be  tedious without having access to the Accounts, SSO, and Fedora Messaging infrastructure, so tiny stage is pre-configured to set all this up.

As a minimum, tiny-stage creates the following machines, and configures them to talk to each other:

* FreeIPA, with the FreeIPA FAS extensions installed: https://ipa.tinystage.test/
* FASJSON (the Fedora Accounts API): http://fasjson.tinystage.test/fasjson/
* Ipsilon: https://ipsilon.tinystage.test/idp
* Fedora Messages

There are also many additional machines for development and testing purposes that are not created by default. these are:

* elections
* fas2ipa
* mirrormanager2
* noggin
* nonbot (zodbot)
* oidctest
* openidtest


## Getting Started

tiny-stage uses Vagrant to create and manage machines. Prepare your machine to run tiny-stage with the commands:

```
$ sudo dnf install ansible ansible-freeipa libvirt vagrant-libvirt vagrant-sshfs vagrant-hostmanager
$ sudo systemctl enable libvirtd
$ sudo systemctl start libvirtd
```

Then run vagrant to create the 4 default machines (freeipa, fasjson, ipsilon, fedora-messages):

```
$ vagrant up
```

This process will take a while, but when complete you will then be able to access the 4 default machines.

To create a non default machine, simply run the vagrant up command with the name of the machine. For example, to create the elections application, run the command:

```
vagrant up elections
```

be sure to read the doc/ folder for details on working with each machine


## Getting the status

To check what machines are currently running, use the command:

```
$ vagrant status
Current machine states:

freeipa                   running (libvirt)
fasjson                   running (libvirt)
ipsilon                   running (libvirt)
oidctest                  not created (libvirt)
openidtest                not created (libvirt)
fas2ipa                   not created (libvirt)
noggin                    not created (libvirt)
elections                 running (libvirt)
mirrormanager2            not created (libvirt)
ipaclient                 not created (libvirt)
nonbot                    not created (libvirt)
fedora-messaging          running (libvirt)

This environment represents multiple VMs. The VMs are all listed
above with their current state. For more information about a specific
VM, run `vagrant status NAME`.
```

## Accessing machines

To gain shell access to any of the running machines, use the vagrant ssh command, for example:

```
vagrant ssh elections
```

## Users and Passwords

Tiny Stage populates the IPA database with many users, and for ease of use, they all have `password` as the password.
