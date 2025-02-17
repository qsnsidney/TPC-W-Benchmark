# Instructions on UG

## 1.0 Postgres

### Install Postgres
```bash
./configure --prefix=/groups/qlhgrp/postgres
make
make install
```

### Start the Postgres
```bash
postgres -D ../data2 -h 127.0.0.1 -p 33333 &
```

### Create a new database
```bash
# ../data2 is the storage dir for database
initdb -D ../data2 -U qinsinin
# must specify the host, port and username
createdb -U qinsinin -h 127.0.0.1 -p 33333 tpcw
```

### Connect to Postgres
```
psql -U qinsinin -h 127.0.0.1 -p 33333 tpcw
```

### Notes
1. admin user name: qinsinin
2. password is leave empty
3. each database must have a separate storage (ie. ../data2, or ../data3)


## 2.0 TPCW

### Modify tpcw.properties
```conf
# set the JDBC parameters
jdbc.driver=org.postgresql.Driver
jdbc.path=jdbc:postgresql://localhost:33333/tpcw?user=qinsinin
jdbc.connPoolMax=50
```

### Generate data
```bash
ant clean
ant mksrc
ant build
ant dist
ant inst
ant gendb
```

## 3.0 o2versioner

### Update rust compiler
```bash
rustup update
```

### Compile
```bash
# Dev mode
cargo build

# Release mode
cargo build --release
```

### Run (Ordered)
```bash
cd dv-in-rust

cargo run --release -- -c ./confug.toml --dbproxy 0
cargo run --release -- -c ./confug.toml --dbproxy 1
# ...
cargo run --release -- -c ./confug.toml --sequencer
cargo run --release -- -c ./confug.toml --scheduler
```

### Dump perf
```bash
netcat 127.0.0.1 19999
perf
```

### Analyze the result
Single run analysis
```bash
python3 -m analyzer single ./perf/xx
```
Multi run analysis
```bash
python3 -m analyzer multi ./perf
```

## 4.0 Launch scripts
Single client  
```
python3 client.py --c_id <any non-negative int> --mix <0-4> --port 2077 --ip <default remote> 
optional (default 0): 
  --debug 1 or 0: on/off logging to stdout
  --mock_db 1 or 0: on/off reading from database response
  --ssh 1 or 0: on/off using remote script path
```
Multiple clients on the same machine
```
python3 launcher.py --range <two arguments, e.g. 0 40> --mix <0-4> --port 2077 --ip <default remote>
optional (default off; adding turns on):
  --debug: on/off logging to stdout
  --mock_db: on/off reading from database response
  --ssh: on/off using remote script path
```
Multiple clients over multiple machine
```
python3 ssh_launcher.py --password <...> --client_num <total number> --mix <0-4>
optional (default off; adding turns on):
  --debug: on/off logging to stdout
  --mock_db: on/off reading from database response
```
Multiple dbproxy
```
python3 ssh_db_launcher.py --password <...> --db_num <total number> 
```

## 5.0 Auto Launcher script

### 5.1 Single Auto Launcher
(Auto Perf) Launch Scheduler + Sequencer + Dbproxies + Client Launcher from conf.toml
```bash
# Scheduler + Sequencer: on current machine, ignoring toml setting
# Dbproxies: follows toml setting
# remove_dv: absolute path points to any dv-in-rust
# duration: Total time to run the system, auto-perf at the end.
# Need to run on ug machine
python3 launcher/master.py --conf=confug.toml --remote_dv=/groups/qlhgrp/liuli15/dv-in-rust --username= --password= --duration=300 --client_num=100 --client_mix=2 --perf_logging=./perf
```

### 5.2 Multi Auto Launcher
Sweeps dbproxy_nums, client_nums, client_mixes
```bash
python3 launcher/planner.py --conf=confug.toml --remote_dv=/groups/qlhgrp/liuli15/dv-in-rust --username= --password= --duration=300 --client_nums 100 200 --client_mixes 2 3 --dbproxy_nums 2 3 --perf_logging=./perf
 ```

## OLD
Refer to: [README.MD](README.old.md)
