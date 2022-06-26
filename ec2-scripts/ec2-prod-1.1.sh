#!/usr/bin/bash

export IMAGE_GALLERY_SCRIPT_VERSION="1.1"



yum -y update
yum install -y emacs-nox tree python3
yum install -y postgresql-devel gcc python3-devel
yum install -y git
amazon-linux-extras install -y nginx1


cd /home/ec2-user
git clone git@github.com:madola20/python-image-gallery.git
chown -R ec2-user:ec2-user python-image-gallery

su ec2-user -l -c "cd ~/python-image-gallery && pip3 install -r requirements.txt --user"


aws s3 cp s3://image-gallery-config/nginx/nginx.conf /etc/nginx
aws s3 cp s3://image-gallery-config/nginx/default.d/image_gallery.conf /etc/nginx/default.d

su ec2-user -l -c "cd ~/python-image-gallery && ./start">/var/log/image_gallery.log 2>&1 &


systemctl stop postfix
systemctl disable postfix
systemctl start nginx
systemctl enable nginx
