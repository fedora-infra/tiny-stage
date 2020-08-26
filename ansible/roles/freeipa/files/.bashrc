# .bashrc
alias tinystage-ipa-resetdb="sudo ipa-restore /var/lib/ipa/backup/backup-clean -p adminPassw0rd!"
alias tinystage-ipa-populatedb="poetry run python /vagrant/devel/create-test-data.py"
