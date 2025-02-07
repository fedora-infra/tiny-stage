#!/bin/bash
set -e
if [ ! -f /etc/ipsilon/ipsilon.conf ]; then
	bash /usr/local/bin/install.sh
fi
# mkdir -p /run/log /data/log/journal
# ln -s /data/log/journal /run/log/journal
#exec /usr/sbin/init
exec /usr/sbin/httpd -DNO_DETACH -DFOREGROUND
