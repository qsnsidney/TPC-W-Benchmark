# TPC-W Benchmark
TPC-W is a popular transactional web benchmark which is used widely for performance benchmarking. TPC-W specifies a specification for a web e-Commerce web application. This repository contains an implementation of that specification using Java Servlets.

Source Code from : https://github.com/jopereira/java-tpcw

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
There are two resource files you need to put your configurations. ``tpcw.properties`` contains properties directly related to TPC-W web application whereas ``main.properties`` contains other properties. Go ahead and update the properties in both files. (The properties are self explanatory.)

### Building TPC-W
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