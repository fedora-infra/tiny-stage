# .bashrc

alias nonbot-start="sudo systemctl start nonbot.service; sudo systemctl status nonbot.service"
alias nonbot-logs="sudo journalctl -u nonbot.service"
alias nonbot-restart="sudo systemctl restart nonbot.service; sudo systemctl status nonbot.service"
alias nonbot-stop="sudo systemctl stop nonbot.service; sudo systemctl status nonbot.service"

cd /vagrant
