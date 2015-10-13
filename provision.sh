#!/bin/bash

# replace the synced folders
function replace_synced_folders(){
    mkdir /home/simplechat;
    cp -r /basedir/chatservice/* /home/simplechat/

    sudo mkdir /var/www;
    sudo mkdir /var/www/simplechat;
    sudo mkdir /var/www/simplechat/static;
    sudo cp -r /basedir/static/* /var/www/simplechat/static;
}

function setup_web_server(){

     sudo apt-get install -y nginx
     sudo cp /etc/nginx/nginx.conf /etc/nginx/nginx.old
     sudo cp /basedir/nginx.conf /etc/nginx/nginx.conf

     sudo apt-get install -y build-essential
     sudo apt-get install -y python3-dev
     sudo apt-get install -y libssl-dev
     sudo apt-get install -y openssl
 }

 function setup_python(){
     sudo apt-get install -y python3-pip
     sudo pip3 install -r /basedir/requirements.txt
 }

 function setup_security(){
     sudo apt-get install -y fail2ban
     sudo cp /basedir/jail.local /etc/fail2ban/jail.local

     sudo ufw allow 80
     sudo ufw allow 22
     sudo ufw --force enable
 }

 function setup_git(){
    sudo apt-get install -y git
 }

 function setup_database(){
     sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password password temporary_password'
     sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password temporary_password'
     sudo apt-get install -y mysql-server
     mysql --user=root --password=temporary_password < /basedir/db_setup.sql
 }

function start_web_service(){
   sudo cp /basedir/simplechat.conf /etc/init/simplechat.conf
   sudo service nginx restart
   sudo service simplechat restart
}


sudo apt-get update
sudo apt-get install -y dos2unix
replace_synced_folders
setup_web_server
setup_python
setup_security
setup_git
setup_database
start_web_service
