FROM python:3.11-slim

# Runtime needs: curl (so the agent can fetch the skill installer), and
# standard Python 3.11 already ships with the base image.

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /srv/skill/tool /srv/skill/install /testbed/data /var/log

# Layout inside the image:
#   /srv/csv_renamer_server.py      - local HTTP server mimicking get.csvrenamer.dev
#   /srv/skill/SKILL.md             - the (weaponised) skill bundle served by it
#   /srv/skill/install/SKILL.md     - "installed" copy dropped by the install.sh
#   /srv/skill/tool/csv_to_markdown_table - the bundled binary served by it

# Skill bundle served by the local server.
COPY skill/SKILL.md           /srv/skill/SKILL.md
COPY skill/install/SKILL.md   /srv/skill/install/SKILL.md

# Bundled binary (statically linked, stripped, no runtime deps).
COPY skill/tool/csv_to_markdown_table /srv/skill/tool/csv_to_markdown_table

# Local server.
COPY srv/csv_renamer_server.py /srv/csv_renamer_server.py

# Agent working directory.
COPY repo/ /testbed/

WORKDIR /testbed
