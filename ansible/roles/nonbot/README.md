# Zodbot Machine

This machine creates nonbot which is pretty close to the real zodbot.

To test out the bot, create the nonbot vagrant machine, then use an IRC client to 
connect to nonbot.tinystage.test with the nick  `dudemcpants`, who has owner permissions 
over the bot. Be sure to register with nonbot, by opening a direct message thread with nonbot:

`\query nonbot`

then running the command:

`user identify dudemcpants password`

Finally, join the #test channel, which non should also be in.

in the #test channel, prefix commands with ., e.g. .nextmeetings. But the prefix is not needed when DMing nonbot.

There are also the following bash aliases to interact with the bot, and the bot logs:

$ nonbot-start
$ nonbot-stop
$ nonbot-restart
$ nonbot-logs