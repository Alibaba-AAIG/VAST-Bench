FROM local-python-base:current
COPY register.py /opt/register.py
ONBUILD RUN --mount=type=secret,id=registry_token,required=true --mount=type=secret,id=build_config,required=true python3 /opt/register.py
