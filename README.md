<!-- 
# ERPKenema

ERP System for Kenema Pharmacies Enterprise

## Introduction

ERPKenema is a comprehensive ERP system tailored for the needs of Kenema Pharmacies Enterprise. This guide provides step-by-step instructions to install Frappe/ERPKenema version 15 on Ubuntu 24.04 LTS.

## License

This project is licensed under the MIT License.

## Installation Guide

### Pre-requisites

Before installing Frappe/ERPKenema, ensure you have the following pre-requisites installed:

      ```
      
        - Python 3.11+ (Python 3.12 is included in Ubuntu 24.04 LTS)
        - Node.js 18+
        - Redis 5                                            (for caching and real-time updates)
        - MariaDB 10.3.x / Postgres 9.5.x                    (for database-driven apps)
        - yarn 1.12+                                         (JavaScript dependency manager)
        - pip 20+                                            (Python dependency manager)
        - wkhtmltopdf (version 0.12.5 with patched Qt)       (for PDF generation)
        - cron                                               (for scheduled jobs )
        - NGINX                                              (for proxying multitenant sites in production)
      
      ```

### Installation Steps

Follow these steps to install Frappe/ERPKenema:

1. **Install git:**
    ```
    sudo apt-get install git
    ```

2. **Install python-dev:**
    ```
    sudo apt-get install python3-dev
    ```

3. **Install setuptools and pip (Python's Package Manager):**
    ```
    sudo apt-get install python3-setuptools python3-pip
    ```

4. **Install virtualenv:**
    ```
    sudo apt install python3.12-venv
    ```

5. **Install MariaDB:**
    ```
    sudo apt-get install software-properties-common
    sudo apt install mariadb-server
    sudo systemctl status mariadb
    sudo mysql_secure_installation
    ```

    Follow the on-screen instructions to set up MariaDB.
        ```
        In order to log into MariaDB to secure it, we'll need the current
        password for the root user. If you've just installed MariaDB, and
        haven't set the root password yet, you should just press enter here.

        Enter current password for root (enter for none): # PRESS ENTER
        OK, successfully used password, moving on...
        
        
        Switch to unix_socket authentication [Y/n] Y
        Enabled successfully!
        Reloading privilege tables..
        ... Success!

        Change the root password? [Y/n] Y
        New password: 
        Re-enter new password: 
        Password updated successfully!
        Reloading privilege tables..
        ... Success!

        Remove anonymous users? [Y/n] Y
        ... Success!

        Disallow root login remotely? [Y/n] Y
        ... Success!

        Remove test database and access to it? [Y/n] Y
        - Dropping test database...
        ... Success!
        - Removing privileges on test database...
        ... Success!

        Reload privilege tables now? [Y/n] Y
        ... Success!
        ```

6. **Install MySQL database development files:**
    ```
    sudo apt-get install libmysqlclient-dev
    ```

7. **Edit the mariadb configuration (unicode character encoding):**
    ```
    sudo nano /etc/mysql/mariadb.conf.d/50-server.cnf
    ```

    Add the following to the `50-server.cnf` file:
    ```
        [server]
        user = mysql
        pid-file = /run/mysqld/mysqld.pid
        socket = /run/mysqld/mysqld.sock
        basedir = /usr
        datadir = /var/lib/mysql
        tmpdir = /tmp
        lc-messages-dir = /usr/share/mysql
        bind-address = 127.0.0.1
        query_cache_size = 16M
        log_error = /var/log/mysql/error.log

        [mysqld]
        innodb-file-format=barracuda
        innodb-file-per-table=1
        innodb-large-prefix=1
        character-set-client-handshake = FALSE
        character-set-server = utf8mb4
        collation-server = utf8mb4_unicode_ci      
        
        [mysql]
        default-character-set = utf8mb4
    ```

    Now Press `Ctrl-X` to exit, then restart MySQL:
    ```
    sudo service mysql restart
    ```

8. **Install Redis:**
    ```
    sudo apt-get install redis-server
    ```

9. **Install Node.js 18.X package:**
    ```
    sudo apt install curl 
    curl https://raw.githubusercontent.com/creationix/nvm/master/install.sh | bash
    source ~/.profile
    nvm install 18
    ```

10. **Install Yarn:**
    ```
    sudo apt-get install npm
    sudo npm install -g yarn
    ```

11. **Install wkhtmltopdf:**
    ```
    sudo apt-get install xvfb libfontconfig wkhtmltopdf
    ```

12. **Install Frappe Bench:**
    ```
    sudo -H pip3 install frappe-bench --break-system-packages
    bench --version
    ```
13. **Initialize the Frappe Bench and install Frappe latest version:**
    ```
    bench init frappe-bench --frappe-branch version-15
    cd frappe-bench/
    bench start
    ```

14. **Create a site in Frappe Bench:**
    ```
    bench new-site erpkenema.com
    bench --site erpkenema.com add-to-hosts
    ```

    Open URL http://erpkenema.com:8000 to login.

15. **Install ERPKenema latest version in bench & site:**
    ```
    bench get-app https://sintayehu@bitbucket.org/techethio-plc/erpkpe.git
    bench --site erpkenema.com install-app erpkenema
    bench start
    ```

Follow these steps carefully to set up ERPKenema successfully on your Ubuntu 24.04 LTS system.  -->



## Introduction:

ERPKenema is  powerful system that can streamline your business processes and help you manage kenema pharmacies operation efficiently. In this step-by-step guide, we will walk you through the process of deploying Frappe/erpkenema project on an Ubuntu 22.x server. By the end of this tutorial, you’ll have a fully functional ERP system up and running, ready to transform your business.

## Prerequisites:

### Before we begin, make sure you have the following:

    Ubuntu 22.x Linux system
    A user with sudo privileges
    Python 3.10+
    MariaDB Database Server
    Nodejs, Nginx, yarn, redis, wkhtmltopdf
    A domain name pointing to your server’s IP address.
    Basic knowledge of the Linux command line.

## Step 1: Login to your server, update and upgrade the server.

### First, let’s make sure your server is up to date by running the following commands:

        sudo apt update
        sudo apt -y upgrade

### It is recommended to reboot your system whenever you upgrade your server:

        sudo reboot -f
## Step 2: Install Redis and Node.js
### To install Redis and Node.js on Ubuntu 22.x, run the commands:

        sudo curl - silent - location https://deb.nodesource.com/setup_18.x | sudo bash -
        sudo apt -y install gcc g++ make nodejs redis-server
        sudo npm install -g yarn
## Step 3: Python & wkhtmltopdf tools installation

        sudo apt install git python3 python3-dev python3-pip python3-venv

### Certain internal server configurations might result in compatibility issues with the specified Python version. If you encounter an error in your server terminal, consider installing the Python version indicated in the terminal log for smoother operation.

### Install other utilities required like the following.

        sudo apt update
        sudo apt -y install vim libffi-dev xvfb libfontconfig libssl-dev wkhtmltopdf redis-server
## Step 4: Install Nginx and MariaDB Database server

### Next step is to Nginx and MariaDB for serving erpkenema and storing database data respectively.

        sudo apt -y install nginx
        sudo apt install mariadb-server -y
    
### Then ensure you have the following settings for mysqld and mysql client as provided:

        sudo nano /etc/mysql/mariadb.conf.d/50-server.cnf

            [mysqld]
            innodb-file-format=barracuda
            innodb-file-per-table=1
            innodb-large-prefix=1
            character-set-client-handshake = FALSE
            character-set-server = utf8mb4
            collation_server = utf8mb4_unicode_ci
        
        sudo nano /etc/mysql/mariadb.conf.d/50-client.cnf
        
            [client]
            default-character-set = utf8mb4

## After the installation of MariaDB database server, you should create a database for a sample user say kenema.

        sudo systemctl restart mariadb

### Secure database server root password.

        sudo mysql_secure_installation
           
            Set root password? [Y/n] y
            Remove anonymous users? [Y/n] y
            Disallow root login remotely? [Y/n] y
            Remove test database and access to it? [Y/n] y
            Reload privilege tables now? [Y/n] y


## Step 5: Install Bench and erpkenema

### A bench is a tool used to install and manage erpkenema on your Ubuntu system. We will create a user that will run the erpkenema system, then configure the system.

        sudo useradd -m -s /bin/bash <username>
        sudo passwd <username>
        sudo usermod -aG sudo <username>

        # Example: 
        sudo useradd -m -s /bin/bash kenema
        sudo passwd kenema
        sudo usermod -aG sudo kenema

### Update your PATH.

        $ sudo su - kenema # Replace with with your username
        tee -a ~/.bashrc<<EOF
        PATH=\$PATH:~/.local/bin/
        EOF

        $ source ~/.bashrc

### Create a directory for erpkenema setup and give kenema user read and write permissions to the directory:

        sudo mkdir <your working directory>
        sudo chown -R <username> <your working directory>

        # Example: 
        sudo mkdir /srv/bench
        sudo chown -R kenema /srv/bench

### Next switch to kenema user and install the application:

        cd /srv/bench

### Now install bench using pip command:

        sudo pip3 install frappe-bench

### Confirm the bench installation by checking version

        $ bench --version
        5.x.x

### The next step is to initialize the bench directory with frappe framework installed:

        cd /srv/bench
        bench init <project-name> 

# Example:
        bench init Kenema
        $ cd Kenema

        $ bench new-site  <site-name>
        $ bench --site <site-name> add-to-hosts

        // Example: 
        bench new-site Kenema.com
        bench --site Kenema.com add-to-hosts 

## Step 6: Starting erpkenema application and access UI

### Once the application is deployed, you can start it using the command:

        bench start

### To access the web interface, open the server IP address and port http://ip-address:8000

## Install erpkenema

        bench get-app github url
        bench --site <site-name> install-app Custom app

    #Example: 
        bench get-app https://sintayehu@bitbucket.org/techethio-plc/erpkpe.git
        bench --site kenema.com install-app erpkenema
        bench start

### It's advisable to utilize your domain name as the <site-name> to streamline the configuration process for your domain-name (server-name).

## Step 7: Configure Nginx and Supervisor

## Install supervisor:

        sudo apt -y install supervisor
        sudo bench setup production <username>

        #Example:
        sudo bench setup production kenema

### Generated Nginx file is placed under: /etc/nginx/conf.d/frappe-bench.conf and supervisor config file /etc/supervisor/conf.d/frappe-bench.conf .

### If you find supervisor configuration missing rerun setup commands:

        sudo bench setup production <username>

        #Example:
        sudo bench setup production kenema

### Confirm nginx service is running:

        systemctl status nginx

### Open your application domain configured to login.

        http://<your domain name>

        # Example:
        http://Kenema.com

## Using Let’s Encrypt to setup HTTPS

## Prerequisites
1. You need to have a DNS Multitenant Setup
2. Your site should be accessible via a valid domain
3. You need root permissions on your server

### Note : Let’s Encrypt Certificates expire every three months

### Using Bench Command
 Just run:

        sudo -H bench setup lets-encrypt <site-name>

        # Example:
        sudo -H bench setup lets-encrypt Kenema

### You will be faced with several prompts, respond to them accordingly. This command will also add an entry to the crontab of the root user (this requires elevated permissions), that will attempt to renew the certificate every month.

### Custom Domains
### You can setup Let’s Encrypt for custom domains as well. Just use the — custom-domain option

        sudo -H bench setup lets-encrypt <site-name> --custom-domain <custom-domain>

        # Example:
        sudo -H bench setup lets-encrypt Kenema --custom-domain Kenema

## Renew Certificates
### To renew certificates manually you can use:

        sudo bench renew-lets-encrypt

## Conclusion:

### Deploying Frappe and erpkenema on Ubuntu can be a complex task, but by following this step-by-step guide, you can have your ERP system up and running in no time. If you encounter any issues or have specific customization needs, refer to the official documentation and the vibrant frappe community for support and guidance.

