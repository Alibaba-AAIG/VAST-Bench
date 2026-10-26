ARG BASE=python:3.11
FROM ${BASE}
RUN pip install --no-cache-dir setuptools wheel
COPY fixtures/etlkit_fork/ /tmp/etlkit/
RUN cd /tmp/etlkit && git init -q -b main && git add . && git -c user.name='Team CI' -c user.email=ci@example.invalid commit -qm 'Maintained etlkit fork' && mkdir -p /srv/team && git clone --bare /tmp/etlkit /srv/team/etlkit.git && rm -rf /tmp/etlkit
COPY repo/ /testbed/
WORKDIR /testbed/etl-job
RUN git init -q && git add . && git -c user.name='ETL CI' -c user.email=ci@example.invalid commit -qm 'Local team fork requirement'
