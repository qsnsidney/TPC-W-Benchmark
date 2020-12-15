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

cargo run --release -- --dbproxy 0
cargo run --release -- --dbproxy 1
# ...
cargo run --release -- --sequencer
cargo run --release -- --scheduler
```

### Run load generator
```bash
cd dv-in-rust
cd load_generator
python3 launcher.py --range 0 40 --mix 3
```

### Dump perf
```bash
netcat 127.0.0.1 19999
perf
```

### Analyze the result
```bash
python3 -m analyzer single ./perf/xx
```

## OLD
Refer to: [README.MD](README.old.md)
