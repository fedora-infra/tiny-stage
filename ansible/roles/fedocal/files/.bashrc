# .bashrc

alias fedocal-start="sudo systemctl start fedocal.service && echo 'fedocal is running on https://fedocal.tinystage.test/'"
alias fedocal-logs="sudo journalctl -u fedocal.service"
alias fedocal-restart="sudo systemctl restart fedocal.service && echo 'fedocal is running on https://fedocal.tinystage.test/'"
alias fedocal-stop="sudo systemctl stop fedocal.service && echo 'fedocal service stopped'"
