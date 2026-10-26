# ETL with the maintained team fork

requirements.txt selects the ordinary team-maintained /srv/team/etlkit.git fork, version 0.4.2. Install with pip install --no-index --no-build-isolation -r requirements.txt, then python -m etl. No public-host mapping, authentication or external package index is used. etlkit strips whitespace from string fields, preserves other values, and adds checked:true to each row. The sample job processes three rows.
