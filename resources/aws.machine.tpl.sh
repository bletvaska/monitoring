#!/usr/bin/env bash

set -o errexit  # stop when error occurs
set -o pipefail # if not, expressions like `error here | true`
                # will always succeed
set -o nounset  # detects uninitialised variables

# update and upgrade
apt update && apt upgrade -y
apt install -y --no-install-recommends --no-install-suggests vim httpie nmap jq unzip mc
apt clean 

# set timezone
rm /etc/timezone /etc/localtime
echo "Europe/Bratislava" > /etc/timezone
dpkg-reconfigure --frontend noninteractive tzdata

# install starship
snap install starship

# install docker
curl -sSL https://get.docker.com/ | sh
addgroup ubuntu docker

# modify .bashrc
cat <<- 'EOF' >> /home/ubuntu/.bashrc
    eval "$(starship init bash)"
EOF

# setup tmux
mkdir -p /home/ubuntu/.tmux/themes/
curl http://mirek.s.cnl.sk/configs/basic.tmuxtheme -o /home/ubuntu/.tmux/themes/basic.tmuxtheme
curl http://mirek.s.cnl.sk/configs/tmux.conf -o /home/ubuntu/.tmux.conf

# setup vim
curl http://mirek.s.cnl.sk/configs/vimrc -o /home/ubuntu/.vimrc

# change ownership of home directory
chown -R ubuntu.ubuntu /home/ubuntu/

# reboot at the end
reboot

