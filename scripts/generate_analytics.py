#!/usr/bin/env python3
"""
Invoice Analytics and Visualization Script

Generates comprehensive analytics and visualizations from the invoice database.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
from pathlib import Path
from datetime import datetime
import numpy as np

class InvoiceAnalytics:
    def __init__(self, data_dir):
        self.data_dir = Path(data_dir)
        self.df = None
        self.summary = None
        self.load_data()
    
    def load_data(self):
        """Load invoice data and summary"""
        csv_path = self.data_dir / 'invoice_database.csv'
        summary_path = self.data_dir / 'invoice_summary.json'
        
        if csv_path.exists():
            self.df = pd.read_csv(csv_path)
            self.df['date'] = pd.to_datetime(self.df['date'])
            print(f"Loaded {len(self.df)} invoice records")
        
        if summary_path.exists():
            with open(summary_path, 'r') as f:
                self.summary = json.load(f)
    
    def create_monthly_analysis(self):
        """Create monthly billing analysis"""
        if self.df is None:
            return
        
        # Set up the plotting style
        plt.style.use('default')
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('NES Invoice Analytics Dashboard', fontsize=16, fontweight='bold')
        
        # Monthly revenue trend
        monthly_data = self.df.groupby(self.df['date'].dt.to_period('M')).agg({
            'total_amount': 'sum',
            'hours': 'sum',
            'invoice_number': 'count'
        })
        
        monthly_data.index = monthly_data.index.to_timestamp()
        
        ax1.plot(monthly_data.index, monthly_data['total_amount'], marker='o', linewidth=2, markersize=6)
        ax1.set_title('Monthly Revenue Trend', fontweight='bold')
        ax1.set_ylabel('Revenue ($)')
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(True, alpha=0.3)
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
        
        # Monthly hours trend
        ax2.bar(monthly_data.index, monthly_data['hours'], alpha=0.7, color='orange')
        ax2.set_title('Monthly Hours Billed', fontweight='bold')
        ax2.set_ylabel('Hours')
        ax2.tick_params(axis='x', rotation=45)
        ax2.grid(True, alpha=0.3)
        
        # Hourly rate distribution
        valid_rates = self.df[self.df['unit_price'] > 0]['unit_price']
        ax3.hist(valid_rates, bins=20, alpha=0.7, color='green', edgecolor='black')
        ax3.set_title('Hourly Rate Distribution', fontweight='bold')
        ax3.set_xlabel('Hourly Rate ($)')
        ax3.set_ylabel('Frequency')
        ax3.grid(True, alpha=0.3)
        
        # Invoice amount distribution
        ax4.boxplot(self.df['total_amount'], vert=True)
        ax4.set_title('Invoice Amount Distribution', fontweight='bold')
        ax4.set_ylabel('Invoice Amount ($)')
        ax4.grid(True, alpha=0.3)
        ax4.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
        
        plt.tight_layout()
        
        # Save the plot
        output_path = self.data_dir / 'invoice_analytics_dashboard.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Analytics dashboard saved to {output_path}")
        return output_path
    
    def create_summary_report(self):
        """Create a comprehensive summary report"""
        if self.df is None or self.summary is None:
            return
        
        report_lines = [
            "# NES Invoice Analytics Report",
            f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## Executive Summary",
            f"- **Total Invoices:** {self.summary['total_invoices']:,}",
            f"- **Total Revenue:** ${self.summary['total_amount']:,.2f}",
            f"- **Total Hours:** {self.summary['total_hours']}",
            f"- **Average Hourly Rate:** ${self.summary['average_hourly_rate']:.2f}",
            f"- **Date Range:** {self.summary['date_range']['earliest']} to {self.summary['date_range']['latest']}",
            "",
            "## Key Metrics",
            "",
            "### Revenue Analysis",
            f"- Highest single invoice: ${self.df['total_amount'].max():,.2f}",
            f"- Lowest single invoice: ${self.df['total_amount'].min():,.2f}",
            f"- Average invoice amount: ${self.df['total_amount'].mean():,.2f}",
            f"- Median invoice amount: ${self.df['total_amount'].median():,.2f}",
            "",
            "### Time Analysis", 
            f"- Most hours in single invoice: {self.df['hours'].max()}",
            f"- Average hours per invoice: {self.df['hours'].mean():.1f}",
            f"- Median hours per invoice: {self.df['hours'].median():.1f}",
            "",
            "### Rate Analysis",
            f"- Highest hourly rate: ${self.df[self.df['unit_price'] > 0]['unit_price'].max():.2f}",
            f"- Lowest hourly rate: ${self.df[self.df['unit_price'] > 0]['unit_price'].min():.2f}",
            f"- Most common rate: ${self.df[self.df['unit_price'] > 0]['unit_price'].mode().iloc[0]:.2f}",
            "",
            "## Company Breakdown",
        ]
        
        for company, count in self.summary['company_breakdown'].items():
            if company:
                report_lines.append(f"- **{company}:** {count} invoices")
        
        report_lines.extend([
            "",
            "## Payment Terms Breakdown",
        ])
        
        for terms, count in self.summary['terms_breakdown'].items():
            if terms:
                report_lines.append(f"- **{terms}:** {count} invoices")
        
        report_lines.extend([
            "",
            "## Monthly Performance",
            "",
            "| Month | Revenue | Hours | Invoices | Avg Rate |",
            "|-------|---------|-------|----------|----------|"
        ])
        
        for month, data in self.summary['monthly_totals'].items():
            if data['hours'] > 0:
                avg_rate = data['amount'] / data['hours']
                report_lines.append(
                    f"| {month} | ${data['amount']:,.0f} | {data['hours']} | {data['count']} | ${avg_rate:.2f} |"
                )
        
        # Save report
        report_path = self.data_dir / 'analytics_report.md'
        with open(report_path, 'w') as f:
            f.write('\n'.join(report_lines))
        
        print(f"Analytics report saved to {report_path}")
        return report_path

def main():
    """Main execution function"""
    script_dir = Path(__file__).parent
    data_dir = script_dir.parent / 'data'
    
    analytics = InvoiceAnalytics(data_dir)
    
    # Generate visualizations
    dashboard_path = analytics.create_monthly_analysis()
    
    # Generate summary report
    report_path = analytics.create_summary_report()
    
    print("\nAnalytics generation complete!")
    print(f"Dashboard: {dashboard_path}")
    print(f"Report: {report_path}")

if __name__ == '__main__':
    main()

