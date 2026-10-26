# app-server full local build

Initialize vendor/pbstubs with `git submodule update --init`, then run `make build` and `./build/app.bin`. /srv/pbstubs.git is a local normal codegen repository; its recorded gitlink identifies the required revision. The build script generates the C descriptor for appserver.v1 AppServer with GetStatus, GetConfig and Ping, then the application prints it. No network is used.
