# tiny-stage

tiny-stage is a way to create a development / testing environment for Fedora Infrastrucure applications.
Testing and developing Fedora Infra applications can be  tedious without having access to the Accounts, SSO, and Fedora Messaging infrastructure, so tiny stage is pre-configured to set all this up.

As a minimum, tiny-stage creates the following machines, and configures them to talk to each other:

* The `auth` VM, including:
  * FreeIPA, with the FreeIPA FAS extensions installed: https://ipa.tinystage.test/
  * FASJSON (the Fedora Accounts API): http://fasjson.tinystage.test/fasjson/
  * Ipsilon: https://ipsilon.tinystage.test/idp
  * Noggin: https://auth.tinystage.test/noggin
  * Test-Auth: https://auth.tinystage.test/test-auth
* The `tinystage` VM, including:
  * The Fedora Messaging broker (RabbitMQ)
  * Sendria, a SMTP collector

There are also many additional machines for development and testing purposes that are not created by default. these are:

* elections
* mirrormanager2
* nonbot (zodbot)
* fedocal
* src


## Getting Started

tiny-stage uses Vagrant to create and manage machines. Prepare your machine to run tiny-stage with the commands:

```
$ sudo dnf install ansible ansible-freeipa libvirt vagrant-libvirt vagrant-sshfs vagrant-hostmanager python3-jmespath
$ sudo systemctl enable libvirtd
$ sudo systemctl start libvirtd
```

Then run vagrant to create the 3 default machines (ipa, auth, tinystage):

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

ipa                       running (libvirt)
auth                      running (libvirt)
elections                 running (libvirt)
mirrormanager2            not created (libvirt)
ipaclient                 not created (libvirt)
nonbot                    not created (libvirt)
fedocal                   not created (libvirt)
src                       not created (libvirt)
tinystage                 running (libvirt)

This environment represents multiple VMs. The VMs are all listed
above with their current state. For more information about a specific
VM, run `vagrant status NAME`.
```

## Accessing machines

To gain shell access to any of the running machines, use the vagrant ssh command, for example:

```
vagrant ssh elections
```

Kerberos-authenticated requests can be made using the provided `krb5.conf` file:

```
$ echo password | KRB5_CONFIG=krb5.conf kinit admin
$ KRB5_CONFIG=krb5.conf curl --cacert ./synced_folders/ipa/ca.crt -u : --negotiate https://fasjson.tinystage.test/fasjson/v1/me/
```

### HTTPS

The web UIs are using IPA's certificate, you need to trust the certificate. In Firefox, just browse to one of the web interfaces, such as [Ipsilon](https://ipsilon.tinystage.test), and accept the certificate.
In Chromium, you have two options. Option 1 is to add the certificate on the system:

```
$ sudo cp synced_folders/ipa/ca.crt /etc/pki/ca-trust/source/anchors/tinystage.pem
$ sudo update-ca-trust 
```

and restart Chromium. Option 2 is to go to `chrome://certificate-manager/localcerts/usercerts`, click "Import", browse to your `tiny-stage/synced_folders/ipa/ca.crt` file and import it.


## Users and Passwords

Tiny Stage populates the IPA database with many users, and for ease of use, they all have `password` as the password.

## Seeing users and Groups in the IPA admin webUI

Since it's your tinystage, you have access to the IPA WebUI as admin. Go to https://ipa.tinystage.test/ and log in with the username `admin` and the password `password` and you can view all the users and groups, and change any details.
![image](https://user-images.githubusercontent.com/592259/122032526-11025c80-ce13-11eb-9a21-66c9047c232e.png)

## Access to ipalib's API

No need to start all the VMs, the `ipa` one is enough:

```
vagrant up ipa
vagrant ssh ipa
```

The ipalib API is accessible from the python console. It's necessary to pass envvars KRB5_CONFIG and IPA_CONFDIR:

```
KRB5_CONFIG=krb5.conf IPA_CONFDIR=<path_to>/synced_folders/ipa/ipa ipython
```

Inside the console initialize API access:
```
from ipalib import api
api.bootstrap(context="custom")
api.finalize()
```
Create a connection:

```
api.Backend.rpcclient.connect()
```

Run the ipalib API commads:
```
api.Command.user_find()
```
More information in the freeipa guide: https://freeipa.readthedocs.io/en/latest/api/basic_usage.html

