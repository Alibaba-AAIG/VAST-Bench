# tallyd local CI

The local runner account executes the standard-library tallyd pipeline. ci/run.sh runs unittest and compilation. The controller key pair is generated exclusively for this local image, with public input controller.pub and private controller identity /opt/controller/id. sshd listens only on 127.0.0.1:2222.
