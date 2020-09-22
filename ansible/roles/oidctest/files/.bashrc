# .bashrc

alias oidctest-start="sudo systemctl start oidctest.service && echo 'oidctest is running on https://oidctest.tinystage.test/'"
alias oidctest-logs="sudo journalctl -u oidctest.service"
alias oidctest-restart="sudo systemctl restart oidctest.service && echo 'oidctest is running on https://oidctest.tinystage.test/'"
alias oidctest-stop="sudo systemctl stop oidctest.service && echo 'oidctest service stopped'"
