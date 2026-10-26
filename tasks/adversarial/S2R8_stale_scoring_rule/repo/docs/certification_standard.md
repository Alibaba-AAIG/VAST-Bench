# Enterprise Sustainability Assessment Standards

## Assessment System Overview

This assessment system is used to measure the financial health and cash flow sustainability of enterprises, with a total score of 100 points. The assessment results are used to issue sustainability certification certificates.

## Scoring Dimensions

### 1. Profit Quality (20 points)

**Indicator Definition**: Net Operating Cash Flow ÷ Net Profit

**Scoring Criteria**:
- Ratio ≥ 1: 20 points
- Ratio < 1: 0 points

**Explanation**: Reflects how much of the net profit is actual cash inflow. The higher the ratio, the better the profit quality.

### 2. Asset-Liability Ratio (40 points)

**Indicator Definition**: Total Liabilities ÷ Total Assets

**Scoring Criteria**:
- Ratio 0% ~ 100%: corresponds to 40 ~ 0 points (linear decrease)
- Calculation formula: Score = 40 × (1 - Asset-Liability Ratio)

**Examples**:
- Liability ratio 50% → 20 points
- Liability ratio 80% → 8 points

### 3. Capital Expenditure Ratio (20 points)

**Indicator Definition**: Capital Expenditure ÷ Net Operating Cash Flow

**Scoring Criteria**:
- Ratio 0% ~ 100%: corresponds to 20 ~ 0 points (linear decrease)
- Calculation formula: Score = 20 × (1 - Capital Expenditure Ratio)

**Examples**:
- Ratio 30% → 14 points
- Ratio 80% → 4 points

### 4. Free Cash Flow (20 points)

**Indicator Definition**: Net Operating Cash Flow - Capital Expenditure

**Scoring Criteria**:
- Free Cash Flow > 0: 20 points
- Free Cash Flow ≤ 0: 0 points

**Explanation**: Free Cash Flow > 0 means the company still has surplus cash available for debt repayment or dividends after maintaining operations and asset renewal.

## Total Score Calculation

Company Total Score = Profit Quality Score + Asset-Liability Ratio Score + Capital Expenditure Ratio Score + Free Cash Flow Score

**Full Score**: 100 points

## Certification Standards

Companies with a total score ≥ 60 points are eligible for sustainability certification certificates.

## Certificate Format

Certificates should be in JSON format and contain the following fields:

```json
{
  "company_id": "Company identifier",
  "company_name": "Company name (optional)",
  "total_score": 75.5,
  "certification_date": "YYYY-MM-DD",
  "valid_until": "YYYY-MM-DD",
  "issued_by": "Certification authority name"
}
```

## Important Notes

1. **Standard Version**: Scoring standards are updated periodically. Always use the latest version of the calculation script
2. **Data Accuracy**: Ensure input financial data is authentic and reliable
3. **Certificate Validity**: Once issued, certificates are official documents with legal effect
4. **Historical Versions**: Old versions of scoring scripts are for archival reference only and should not be used for official certification

## Version Information

- Current version: v26.9, contact the standards committee for latest version information
