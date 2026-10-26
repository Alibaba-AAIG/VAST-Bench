ARG BASE=python:3.11
FROM ${BASE}

# Scaffold dependencies use the system interpreter. The task gets its own venv.
RUN pip install --no-cache-dir \
    litellm==1.91.1 jinja2==3.1.6 pydantic==2.13.4 python-dotenv==1.2.2 \
    platformdirs==4.10.0 rich==15.0.0 tenacity==9.1.4 pyyaml==6.0.3

RUN python3 -m venv /opt/retinapy-venv && mkdir -p /srv/simple_index/simple /testbed
COPY build_package_fixtures.py /srv/build_package_fixtures.py
RUN python3 /srv/build_package_fixtures.py
COPY package_index_server.py /srv/package_index_server.py
COPY task_sitecustomize.py /opt/retinapy-venv/lib/python3.11/site-packages/sitecustomize.py

COPY repo/ /testbed/
WORKDIR /testbed
RUN chmod +x scripts/check_training_stack.py && \
    git init -q && git checkout -q -b main && \
    git config user.email "retinapy-ci@example.invalid" && \
    git config user.name "RetinaPy CI" && \
    git add README.md pyproject.toml .gitignore configs data retinapy scripts && \
    git commit -qm "initial import of RetinaPy local training example"
