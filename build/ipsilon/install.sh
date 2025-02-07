#!/bin/bash

set -e

if [ -z "${IPA_ADMIN_PASSWORD}" ]; then
	echo "You must set the IPA_ADMIN_PASSWORD environment variable to the IPA admin's password."
	exit 1
fi

set -x

# if [ ! -f /etc/ipa/default.conf ]; then
# 	ipa-client-install \
# 		--domain `hostname -d` \
# 		--realm `hostname -d | tr a-z A-Z` \
# 		--server ipa.`hostname -d` \
# 		-p admin \
# 		-w ${IPA_ADMIN_PASSWORD} \
# 		--no-nisdomain \
# 		-U -N --force-join
# fi

# mkdir /etc/ipsilon/certs
# ipa-getcert -f /etc/ipsilon/certs/ipsilon.crt -k /etc/ipsilon/certs/ipsilon.key 

set +x

if [ -f /etc/ipsilon/ipsilon-server-install-options ]; then
	install_options="`cat /etc/ipsilon/ipsilon-server-install-options`"
else
		# --ipa yes \
		# --gssapi yes \
		# --gssapi-httpd-keytab /etc/ipsilon/ipsilon.keytab \
		# --info-sssd yes \
		# --pam yes \
	install_options='
		--root-instance
		--secure no
		--testauth yes
		--testauth-groups fedora-contributors,packager
		--openid yes 
		--openidc yes
		--openid-extensions insecureAPI,Teams,CLAs
		--openidc-extensions fedora-account,waiverdb
		--openidc-default-attribute-mapping [["*","*"],["_groups","groups"],[["_extras","cla"],"cla"],["fullname","name"],["_username","nickname"],["_username","preferred_username"],["fasIRCNick","ircnick"],["fasLocale","locale"],["fasTimeZone","zoneinfo"],["fasTimeZone","timezone"],["fasWebsiteURL","website"],["fasGPGKeyId","gpg_keyid"],["ipaSshPubKey","ssh_key"],["fasIsPrivate","privacy"],["fullname","human_name"]]
	'
fi

set -x

ipsilon-server-install $install_options
