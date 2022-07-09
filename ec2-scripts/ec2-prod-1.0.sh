#!/usr/bin/bash

export IMAGE_GALLERY_SCRIPT_VERSION="1.0"



yum -y update
yum install -y emacs-nox tree python3
yum install -y git

cd /home/ec2-user
git clone git@github.com:madola20/python-image-gallery.git
chown -R ec2-user:ec2-user python-image-gallery

su ec2-user -l -c "cd ~/python-image-gallery && pip3 install -r requirements.txt --user"

su ec2-user -l -c "cd ~/python-image-gallery && ./start">/var/log/image_gallery.log 2>&1 &


systemctl stop postfix
systemctl disable postfix
