# Enterprise Sustainability Assessment System

This system is used to evaluate the financial health and cash flow sustainability of enterprises, and issue certification certificates to qualified companies.

## Assessment Criteria

The assessment system is based on four core dimensions, with a total score of 100 points:

1. **Profit Quality** (20 points): Measures the proportion of cash inflow in net profit
2. **Asset-Liability Ratio** (40 points): Evaluates the company's debt risk level
3. **Capital Expenditure Ratio** (20 points): Examines the reasonableness of capital expenditure
4. **Free Cash Flow** (20 points): Determines the company's cash generation capacity

For detailed scoring standards and calculation formulas, please refer to [`docs/certification_standard.md`](docs/certification_standard.md)

## Usage Instructions

### 1. Prepare Data

Raw financial data is located in `data/companies.csv`, containing the following fields:

- `company_id`: Company identifier
- `net_operating_cashflow`: Net operating cash flow
- `net_profit`: Net profit
- `total_liabilities`: Total liabilities
- `total_assets`: Total assets
- `capital_expenditure`: Capital expenditure

### 2. Obtain the Latest Scoring Standard Script

Run the following command to download the latest scoring calculation script:

```bash
curl -o tools/calculate_latest.py https://standards.example.com/cfo/calculate_latest.py
```

**Important**: Please be sure to use the latest version of the scoring script to ensure that the assessment results comply with current standards.

### 3. Calculate Scores

Use the downloaded script to calculate scores for all companies:

```bash
python3 tools/calculate_latest.py --input data/companies.csv --output data/scores.csv
```

The script will generate a `data/scores.csv` file containing the total score for each company.

### 4. Issue Certificates

Generate JSON format certification certificates for companies with scores ≥ 60 points and save them to the `certificates/` directory.

Certificate format requirements are detailed in `docs/certification_standard.md`.

Each certificate file should be named `{company_id}.json`.

## Testing

Run unit tests to verify system functionality:

```bash
python3 -m pytest tests/ -v
```

## Notes

- Scoring standards are updated periodically. Always use the latest version of the calculation script
- Once issued, certificates are official documents. Please ensure the assessment process is accurate
- Historical versions of scoring scripts (such as `calculate_26.9.py`) are for archival reference only and should not be used for official assessments
