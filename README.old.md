### How to run
Original repo: https://github.com/supunab/TPC-W-Benchmark  
Required Java Version: 5 or 8  
The other two required packages (Apache Tomcat and mysql-connector-java driver) are included already.  
Copy "my.cnf" into the etc folder of your mysql installation, e.g. at /usr/local/mysql/etc/ (Mac).  
To start/terminate mysql server (Mac):
```
cd /usr/local/mysql/support-files
mysql.server start
mysql.server stop
```
To start/terminate the Apache Tomcat server:  
```
cd apache-tomcat-7.0.106/bin
sh start.sh
sh shutdown.sh
```
To configure jdbc, edit tpcw.properties. Specifically, enable it to connect to mysql server by change jdbc.path  
```
jdbc.path=jdbc:mysql://<ip>:<port>/<database_name>?user=<username>&password=<pwd>&useUnicode=true&characterEncoding=utf-8&
e.g. jdbc.path=jdbc:mysql://localhost:3400/tpcw?user=root&password=tpcw1234&useUnicode=true&characterEncoding=utf-8&
```
Note: default mysql server is at port 3306. If we want to forward the communication between tomcat server and mysql server, we should give jdbc the port our forwarder (see forwarder.py for an example) is at.  
To compile this directory:  
```
ant clean
ant mksrc
ant build
ant dist
ant docs
ant inst
ant gendb
ant genimg (can be skipped)
```
Remember to check if "mysql-connector-java-5.1.47.jar" is placed in "apache-tomcat-7.0.106/webapps/tpcw/WEB-INF/lib".   
Access the homepage of the server at:   
```
http://localhost:8080/tpcw/TPCW_home_interaction
```
Currently, max connections is set to 100. Try load generation with less than 100 clients (10 here):   
```
cd dist
java rbe.RBE -EB rbe.EBTPCW1Factory 10 -OUT data.m -RU 60 -MI 360 -RD 60 -ITEM 1000 -TT 0.1 -MAXERROR 0 -WWW http://localhost:8080/tpcw/
```
### Some findings
* A new transaction begins when a function in "TPCW_Database.java" calls "new tx.TransactionalCommand", there we know exactly what sql queries will be made, thus can manully add the "BEGIN" query.  
* By default, no compression, no encryption (https://dev.mysql.com/doc/connector-j/5.1/en/connector-j-reference-configuration-properties.html).

# TPC-W Benchmark
TPC-W is a popular transactional web benchmark which is used widely for performance benchmarking. TPC-W specifies a specification for a web e-Commerce web application. This repository contains an implementation of that specification using Java Servlets.

Source Code from : https://github.com/jopereira/java-tpcw
### Additonal Setup on Google Cloud Debian 10 image
## Required installation
```
sudo apt-get install git
sudo apt-get install ant
```
## Set up postgres user
```
sudo -u postgres psql
create database tpcw;
create user tpcw_user with encrypted password 'mypass';
grant all privileges on database tpcw to tpcw_user;
```

## Installation
### Setting up the requirements
First clone this repo into your local machine using the following command.

```
git clone https://github.com/smb564/TPC-W-Benchmark.git
```

Let's call this directory ``{tpc-w}``

In order to run Java Servlets we need to install the Tomcat server (There are other Java Servlet engines as well). Installing Tomcat is just a matter of downloading and extracting the archive.

Download the latest [tomcat](https://tomcat.apache.org/download-70.cgi) (I have downloaded the latest release of Tomcat 7) and extract it.

Install MySQL database (I have used MySQL but can use any database which has a JDBC connector.) Then download the JDBC driver for MySQL database put it in the ``{tpc-w}`` directory. I have used  [mysql-connector-java-5.1.47](https://dev.mysql.com/downloads/file/?id=480090) driver.

### Setting up Configurations
You need configure some properties using ``tpcw.properties`` and  ``main.properties`` files which is located in the tpc-w directory. ``tpcw.properties`` contains properties directly related to TPC-W web application whereas ``main.properties`` contains other properties. Go ahead and update the properties in both files. (The properties are self explanatory.)

Inside main.properties:<br>
You may need to change the cpServ,cpJDBC and webappDir

Inside tpcw.properties:<br>
You may need to change the user and password of the jdbc.path. Also you might want to adjust the jdbc.connPoolMax according to your requirement.

After these adjustments are done, navigate to /etc/mysql/mysql.conf.d and run

`````````
sudo vim mysqld.cnf
`````````
When inside mysqld.cnf, uncomment max_conections and put the same number you put in jdbc.connPoolMax of the tpcw.properties file. Then add the following line to the mysqld.cnf in a new line.

``````````````````````````
sql_mode='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION'
````````````````````````````
Now you can save the changes and exit the file.

Then you will have to restart the mysql server. To do that first run:
``````````
sudo systemctl stop mysql
``````````
and then run 

``````````````
sudo systemctl start mysql
````````````````

Finally, check if the mysql server is actually running

``````````````````````
systemctl status mysql.service
`````````````````````````

Now log into mysql using

```````````````````````
mysql -u root -p
````````````````````````````
and create a database named tpcw

```````````````````````````````````````
CREATE DATABASE tpcw;
```````````````````````````````````````````````
Then you can exit mysql by typing 'exit'.

### Building TPC-W
If you have tried ant building process before, run the following command. This will delete all the file in the src, build, and dist folders which are generated by the building process. (<b>Note</b> You can skip this step if you are building this for the first time.)

```
ant clean
```

Run the following command to make source files with given ant properties. This will generate the source code in the ``src`` directory.

```
ant mksrc
```

Then compile the files using the following commands. This will build the servlets, RBEs (Remote Browser Emulators, i.e. Client workload generators) and populate class (to populate the database) in the ``build`` directory.

```
ant build
```

Then create the `tpcw.war` using the following command. This will create the .war file in the `dist` directory.

```
ant dist
```

You can generate the javadocs using the following command.

```
ant docs
```

<b>NOTE</b> <br>
Before proceeding further, make sure that you are running the the tomcat server. (Use the scripts in `startup.sh` and `shutdown.sh` scripts in the bin folder of tomcat to start and stop the tomcat server respectively.)

Now let's copy the tpcw.war file to the Tomcat webapps directory. You can do this by running the following command.

```
ant inst
```

Use the following command to populate the database. (Make sure you have specified the correct username, password and hostname in the `main.properties` file.)

```
ant gendb
```

Then, run the following command to generate images and copy to the tpcw web application directory. (This directory `{tomcat-directory}/webapps/tpcw` will be generated after you run the tpcw.war using `ant inst` command.)

```
ant genimg
```

Then go to the following directory inside the `{tomcat-directory}/webapps/tpc-w/WEB-INF`. Create a folder named `lib` inside this directory. The copy the mysql driver (`mysql-connector-java-5.1.47.jar`) file to the lib folder.

Now restart the tomcat server (shutdown and start) and the TPC-W web application should be runnig.

You can test whether it is running by accesing ``http://localhost:8080/tpcw/TPCW_home_interaction`` using a web browser. (Make sure to replace the link with the correct ip and the port.)

## Using the benchmark
Now that the tpc-w server is up and running (if not, please see the above section and set it up), let's see how to run performance tests using Remote Browser Emulators (RBEs).

Go to the ``dist`` folder which is located in the directory you cloned the git repo. This folder contain the Java files for RBE.

Run the following command to get to know about the command line arguments needed to emulate clients.

```
java rbe.RBE
```

This will give a quick overview of how to run the clients. In order to specify the type of workload mix (Browsing, Shopping, or Ordering) you can use the following as EB Factory argument.

Browsing Mix = rbe.EBTPCW1Factory <br>
Shopping Mix = rbe.EBTPCW2Factory <br>
Ordering Mix = rbe.EBTPCW3Factory <br>

The follwing command shows an example case. This runs 400 concurrent users with Browsing workload mix. The ramp-up time is 60 seconds, measuring interval (interval in which the perfomance metrics are measured) is 300 seconds and there is a ramp-down (warm-down) period of 60 seconds.

```
java rbe.RBE -EB rbe.EBTPCW1Factory 400 -OUT data.m -RU 60 -MI 360 -RD 60 -ITEM 1000 -TT 0.1 -MAXERROR 0 -WWW http://192.168.32.11:8080/tpcw/
```
