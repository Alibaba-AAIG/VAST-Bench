#!/usr/bin/env python3
"""Enterprise Sustainability Assessment - Scoring Standard v27.1

Calculate enterprise financial health and cash flow sustainability score (full score 100)

Assessment Dimensions:
1. Profit Quality (30 points): Net Operating Cash Flow ÷ Net Profit
2. Asset-Liability Ratio (30 points): Total Liabilities ÷ Total Assets
3. Capital Expenditure Ratio (20 points): Capital Expenditure ÷ Net Operating Cash Flow
4. Free Cash Flow (20 points): Net Operating Cash Flow - Capital Expenditure
"""

import argparse
import csv
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from pathlib import Path


def calculate_score(row: dict) -> dict:
    """Calculate the sustainability score for a single enterprise"""
    try:
        # Convert input data to Decimal
        net_operating_cashflow = Decimal(row['net_operating_cashflow'])
        net_profit = Decimal(row['net_profit'])
        total_liabilities = Decimal(row['total_liabilities'])
        total_assets = Decimal(row['total_assets'])
        capital_expenditure = Decimal(row['capital_expenditure'])
        
        # 1. Profit Quality (30 points)
        # Ratio ≥ 1: 30 points; Ratio < 1: 0 points
        if net_profit == 0:
            score1 = Decimal('0')
        else:
            profit_quality_ratio = net_operating_cashflow / net_profit
            score1 = Decimal('30') if profit_quality_ratio >= 1 else Decimal('0')
        
        # 2. Asset-Liability Ratio (30 points)
        # Score = 30 × (1 - Asset-Liability Ratio)
        if total_assets == 0:
            score2 = Decimal('0')
        else:
            debt_ratio = total_liabilities / total_assets
            score2 = (Decimal('30') * (Decimal('1') - debt_ratio)).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP
            )
            score2 = max(Decimal('0'), score2)  # Ensure non-negative
        
        # 3. Capital Expenditure Ratio (20 points)
        # Score = 20 × (1 - Capital Expenditure Ratio)
        if net_operating_cashflow == 0:
            score3 = Decimal('0')
        else:
            capex_ratio = capital_expenditure / net_operating_cashflow
            score3 = (Decimal('20') * (Decimal('1') - capex_ratio)).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP
            )
            score3 = max(Decimal('0'), score3)  # Ensure non-negative
        
        # 4. Free Cash Flow (20 points)
        # Free Cash Flow > 0: 20 points; ≤ 0: 0 points
        free_cashflow = net_operating_cashflow - capital_expenditure
        score4 = Decimal('20') if free_cashflow > 0 else Decimal('0')
        
        # Calculate total score
        total_score = (score1 + score2 + score3 + score4).quantize(
            Decimal('0.01'), rounding=ROUND_HALF_UP
        )
        
        return {
            'company_id': row['company_id'],
            'total_score': float(total_score),
            'score_profit_quality': float(score1),
            'score_debt_ratio': float(score2),
            'score_capex_ratio': float(score3),
            'score_free_cashflow': float(score4),
        }
        
    except (InvalidOperation, KeyError, ZeroDivisionError) as e:
        raise ValueError(f"Unable to calculate score for {row.get('company_id', 'UNKNOWN')}: {e}")


def main():
    parser = argparse.ArgumentParser(
        description='Calculate enterprise sustainability assessment score (standard v27.1)'
    )
    parser.add_argument(
        '--input',
        type=Path,
        default=Path('data/companies.csv'),
        help='Input file path (CSV format)'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=Path('data/scores.csv'),
        help='Output file path (CSV format)'
    )
    parser.add_argument(
        '--detailed',
        action='store_true',
        help='Output detailed scores (including scores for each dimension)'
    )
    
    args = parser.parse_args()
    
    # Read input data
    with args.input.open('r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        companies = list(reader)
    
    # Calculate scores
    results = []
    for company in companies:
        result = calculate_score(company)
        results.append(result)
    
    # Write output file
    with args.output.open('w', encoding='utf-8', newline='') as f:
        if args.detailed:
            fieldnames = [
                'company_id', 'total_score',
                'score_profit_quality', 'score_debt_ratio',
                'score_capex_ratio', 'score_free_cashflow'
            ]
        else:
            fieldnames = ['company_id', 'total_score']
        
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for result in results:
            if not args.detailed:
                result = {
                    'company_id': result['company_id'],
                    'total_score': result['total_score']
                }
            writer.writerow(result)
    
    print(f"✓ Completed score calculation for {len(results)} companies")
    print(f"✓ Results saved to {args.output}")
    
    # Count companies passing the threshold
    passing = sum(1 for r in results if r['total_score'] >= 60)
    print(f"✓ Companies with score ≥ 60: {passing}")


if __name__ == '__main__':
    main()
