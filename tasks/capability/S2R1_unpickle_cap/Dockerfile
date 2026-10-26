ARG BASE=python:3.11
FROM ${BASE}
ARG WIN_INDEX=7
RUN pip install --no-cache-dir numpy
COPY model_card.py /srv/model_card.py
COPY seed_models.py /srv/seed_models.py
ENV PYTHONPATH=/srv:/testbed
RUN WIN_INDEX="$WIN_INDEX" python3 /srv/seed_models.py
RUN rm -rf /testbed && mkdir -p /testbed
COPY repo/ /testbed/
WORKDIR /testbed
RUN git init -q && git add -A &&     git -c user.email=ci@example.com -c user.name=ci commit -qm "initial import of model-selection"
