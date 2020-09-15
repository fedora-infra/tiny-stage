# .bashrc

alias elections-start="sudo systemctl start elections.service && echo 'elections is running on https://elections.tinystage.test/'"
alias elections-logs="sudo journalctl -u elections.service"
alias elections-restart="sudo systemctl restart elections.service && echo 'elections is running on https://elections.tinystage.test/'"
alias elections-stop="sudo systemctl stop elections.service && echo 'elections service stopped'"
