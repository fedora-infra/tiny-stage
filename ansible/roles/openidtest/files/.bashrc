# .bashrc

alias openidtest-start="sudo systemctl start openidtest.service && echo 'openidtest is running on https://openidtest.tinystage.test/'"
alias openidtest-logs="sudo journalctl -u openidtest.service"
alias openidtest-restart="sudo systemctl restart openidtest.service && echo 'openidtest is running on https://openidtest.tinystage.test/'"
alias openidtest-stop="sudo systemctl stop openidtest.service && echo 'openidtest service stopped'"
