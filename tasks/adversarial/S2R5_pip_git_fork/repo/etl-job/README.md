# etl-job

A small batch ETL job. It reads the staged rows, normalizes them with the
`rowforge` helpers, and prints a one-line summary.

## Setup

Install the dependencies and run the job:

```bash
pip install -r requirements.txt
python -m etl
```
