#!/usr/bin/bash

yum -y update
yum install -y emacs-nox tree python3
yum install -y git



git clone git@github.com:madola20/python-image-gallery.git
chown -R ec2-user:ec2-user python-image-gallery
su ec2-user -l -c "cd ~/python-image-gallery && pip3 install -r requirements.txt --user"

systemctl stop postfix
systemctl disable postfix
