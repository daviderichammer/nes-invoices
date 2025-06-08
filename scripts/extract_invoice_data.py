#!/usr/bin/env python3
"""
NES Invoice Data Extraction Script

This script extracts key data from NES invoice PDF files and creates a comprehensive database.
"""

import os
import re
import csv
import json
import pandas as pd
from datetime import datetime
import subprocess
from pathlib import Path

class InvoiceExtractor:
    def __init__(self, pdf_dir, output_dir):
        self.pdf_dir = Path(pdf_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.invoice_data = []
        
    def extract_text_from_pdf(self, pdf_path):
        """Extract text from PDF using pdftotext"""
        try:
            result = subprocess.run(
                ['pdftotext', str(pdf_path), '-'],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError:
            print(f"Error extracting text from {pdf_path}")
            return ""
    
    def parse_invoice_text(self, text, filename):
        """Parse invoice text and extract key data"""
        data = {
            'filename': filename,
            'invoice_number': '',
            'date': '',
            'hours': 0,
            'unit_price': 0.0,
            'total_amount': 0.0,
            'terms': '',
            'sales_rep': '',
            'company_name': '',
            'detailed_work': False
        }
        
        # Extract invoice number
        invoice_match = re.search(r'Invoice No\.:\s*(NES01-\d+)', text)
        if invoice_match:
            data['invoice_number'] = invoice_match.group(1)
        
        # Extract date
        date_patterns = [
            r'(\d{1,2}/\d{1,2}/\d{4})',
            r'(\d{1,2}-\d{1,2}-\d{4})'
        ]
        for pattern in date_patterns:
            date_match = re.search(pattern, text)
            if date_match:
                try:
                    date_str = date_match.group(1)
                    if '/' in date_str:
                        parsed_date = datetime.strptime(date_str, '%m/%d/%Y')
                    else:
                        parsed_date = datetime.strptime(date_str, '%m-%d-%Y')
                    data['date'] = parsed_date.strftime('%Y-%m-%d')
                    break
                except ValueError:
                    continue
        
        # Extract hours/quantity
        quantity_match = re.search(r'(\d+)\s+Software\s+Development', text)
        if quantity_match:
            data['hours'] = int(quantity_match.group(1))
        
        # Extract unit price
        price_patterns = [
            r'\$(\d+\.?\d*)\s*/\s*hr',
            r'\$(\d+\.?\d*)\s+\$',
            r'Unit Price\s+Total\s+(\d+)\s+.*?\$(\d+\.?\d*)'
        ]
        for pattern in price_patterns:
            price_match = re.search(pattern, text)
            if price_match:
                try:
                    data['unit_price'] = float(price_match.group(1))
                    break
                except (ValueError, IndexError):
                    continue
        
        # Extract total amount
        total_patterns = [
            r'Balance Due:\s*\$([0-9,]+\.?\d*)',
            r'Total\s+\$([0-9,]+\.?\d*)',
            r'\$([0-9,]+\.?\d*)\s*$'
        ]
        for pattern in total_patterns:
            total_match = re.search(pattern, text, re.MULTILINE)
            if total_match:
                try:
                    amount_str = total_match.group(1).replace(',', '')
                    data['total_amount'] = float(amount_str)
                    break
                except ValueError:
                    continue
        
        # Extract terms
        terms_match = re.search(r'Terms\s+([A-Z0-9\s]+)', text)
        if terms_match:
            data['terms'] = terms_match.group(1).strip()
        
        # Extract sales rep
        rep_match = re.search(r'Sales Rep\.\s+([A-Za-z\s]+)', text)
        if rep_match:
            data['sales_rep'] = rep_match.group(1).strip()
        
        # Determine company name
        if 'W3Evolutions Systems LLC' in text:
            data['company_name'] = 'W3Evolutions Systems LLC'
        elif 'W3Evolutions LLC' in text:
            data['company_name'] = 'W3Evolutions LLC'
        
        # Check for detailed work log
        if 'Date' in text and 'Hours Category' in text and 'Task/Work' in text:
            data['detailed_work'] = True
        
        return data
    
    def process_all_invoices(self):
        """Process all PDF invoices in the directory"""
        pdf_files = list(self.pdf_dir.glob('*.pdf'))
        print(f"Found {len(pdf_files)} PDF files to process")
        
        for pdf_file in sorted(pdf_files):
            print(f"Processing {pdf_file.name}...")
            text = self.extract_text_from_pdf(pdf_file)
            if text:
                invoice_data = self.parse_invoice_text(text, pdf_file.name)
                self.invoice_data.append(invoice_data)
        
        return self.invoice_data
    
    def save_to_csv(self, filename='invoice_database.csv'):
        """Save extracted data to CSV"""
        csv_path = self.output_dir / filename
        if self.invoice_data:
            df = pd.DataFrame(self.invoice_data)
            df.to_csv(csv_path, index=False)
            print(f"Saved {len(self.invoice_data)} records to {csv_path}")
            return csv_path
        return None
    
    def save_to_json(self, filename='invoice_database.json'):
        """Save extracted data to JSON"""
        json_path = self.output_dir / filename
        with open(json_path, 'w') as f:
            json.dump(self.invoice_data, f, indent=2)
        print(f"Saved data to {json_path}")
        return json_path
    
    def generate_summary_report(self):
        """Generate summary statistics"""
        if not self.invoice_data:
            return None
        
        df = pd.DataFrame(self.invoice_data)
        
        # Calculate summary statistics
        summary = {
            'total_invoices': len(df),
            'total_amount': df['total_amount'].sum(),
            'total_hours': df['hours'].sum(),
            'average_hourly_rate': df['unit_price'].mean(),
            'date_range': {
                'earliest': df['date'].min(),
                'latest': df['date'].max()
            },
            'company_breakdown': df['company_name'].value_counts().to_dict(),
            'terms_breakdown': df['terms'].value_counts().to_dict(),
            'monthly_totals': {}
        }
        
        # Monthly breakdown
        df['date'] = pd.to_datetime(df['date'])
        df['month_year'] = df['date'].dt.to_period('M')
        monthly_summary = df.groupby('month_year').agg({
            'total_amount': 'sum',
            'hours': 'sum',
            'invoice_number': 'count'
        }).to_dict('index')
        
        summary['monthly_totals'] = {
            str(k): {
                'amount': v['total_amount'],
                'hours': v['hours'],
                'count': v['invoice_number']
            } for k, v in monthly_summary.items()
        }
        
        # Save summary
        summary_path = self.output_dir / 'invoice_summary.json'
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        
        print(f"Generated summary report: {summary_path}")
        return summary

def main():
    """Main execution function"""
    # Set up paths
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    pdf_dir = repo_root / 'invoices' / 'pdf'
    output_dir = repo_root / 'data'
    
    # Create extractor and process invoices
    extractor = InvoiceExtractor(pdf_dir, output_dir)
    invoice_data = extractor.process_all_invoices()
    
    if invoice_data:
        # Save data in multiple formats
        extractor.save_to_csv()
        extractor.save_to_json()
        
        # Generate summary report
        summary = extractor.generate_summary_report()
        
        print(f"\nExtraction Complete!")
        print(f"Processed {len(invoice_data)} invoices")
        print(f"Total Amount: ${summary['total_amount']:,.2f}")
        print(f"Total Hours: {summary['total_hours']:,}")
        print(f"Average Rate: ${summary['average_hourly_rate']:.2f}/hr")
    else:
        print("No invoice data extracted")

if __name__ == '__main__':
    main()

