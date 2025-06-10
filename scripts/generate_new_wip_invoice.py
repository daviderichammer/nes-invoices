#!/usr/bin/env python3
"""
NES Invoice Generator for New WIP Items
Generates Invoice NES01-5542 for the latest WIP entries from Google Sheets

This script creates a new invoice for WIP items found in the time tracking data:
- 102 hours of AAE-101 UAT bug tracker work
- Date range: 6/4/25 to 6/10/25
- Workers: BK/DH
- Total amount: $12,803 (102 hours × $126/hour - $49 discount)
"""

import json
import base64
from datetime import datetime

class WIPInvoiceGenerator:
    def __init__(self):
        self.invoice_number = "NES01-5542"
        self.hourly_rate = 126
        self.discount = 49
        
        # New WIP entries from Google Sheets
        self.wip_entries = [
            {"date": "6/4/25", "hours": 17, "description": "AAE-101 - UAT bug tracker list review, development and bug fixes", "workers": "BK/DH"},
            {"date": "6/5/25", "hours": 15, "description": "AAE-101 - UAT bug tracker list review, development and bug fixes", "workers": "BK/DH"},
            {"date": "6/6/25", "hours": 16, "description": "AAE-101 - UAT bug tracker list review, development and bug fixes Issues with ERV2 on prod - introduced bandaid fixes needs to be merged into stage-qa for A2", "workers": "BK/DH"},
            {"date": "6/7/25", "hours": 9, "description": "AAE-101 - UAT bug tracker list review, development and bug fixes", "workers": "BK/DH"},
            {"date": "6/8/25", "hours": 10, "description": "AAE-101 - UAT bug tracker list review, development and bug fixes", "workers": "BK/DH"},
            {"date": "6/9/25", "hours": 17, "description": "AAE-101 - UAT bug tracker list review, development and bug fixes", "workers": "BK/DH"},
            {"date": "6/10/25", "hours": 18, "description": "AAE-101 - UAT bug tracker list review, development and bug fixes", "workers": "BK/DH"}
        ]
        
        self.total_hours = sum(entry["hours"] for entry in self.wip_entries)
        self.subtotal = self.total_hours * self.hourly_rate
        self.total_amount = self.subtotal - self.discount
        
        # Load W3EVOLUTIONS logo
        try:
            with open('/home/ubuntu/nes-invoices/assets/logo_base64.txt', 'r') as f:
                self.logo_base64 = f.read().strip()
        except FileNotFoundError:
            self.logo_base64 = ""
            print("Warning: Logo file not found")

    def generate_html_invoice(self):
        """Generate professional HTML invoice with W3EVOLUTIONS branding"""
        
        # Generate line items HTML
        line_items_html = ""
        for entry in self.wip_entries:
            line_items_html += f"""
            <tr>
                <td style="padding: 8px; border-bottom: 1px solid #eee;">{entry['date']}</td>
                <td style="padding: 8px; border-bottom: 1px solid #eee;">{entry['hours']}</td>
                <td style="padding: 8px; border-bottom: 1px solid #eee;">{entry['description']}</td>
                <td style="padding: 8px; border-bottom: 1px solid #eee; text-align: right;">${entry['hours'] * self.hourly_rate:,.2f}</td>
            </tr>"""

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Invoice {self.invoice_number}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
            color: #333;
        }}
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #2c5aa0;
        }}
        .logo {{
            max-height: 80px;
            max-width: 300px;
        }}
        .invoice-title {{
            font-size: 2.5em;
            font-weight: bold;
            color: #2c5aa0;
        }}
        .invoice-info {{
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
        }}
        .invoice-details {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 30px;
        }}
        .bill-to, .invoice-meta {{
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
        }}
        .section-title {{
            font-weight: bold;
            color: #2c5aa0;
            margin-bottom: 10px;
            font-size: 1.1em;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 30px;
            background-color: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        th {{
            background-color: #2c5aa0;
            color: white;
            padding: 12px 8px;
            text-align: left;
            font-weight: bold;
        }}
        th:last-child, td:last-child {{
            text-align: right;
        }}
        .totals {{
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-top: 20px;
        }}
        .total-line {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
        }}
        .total-final {{
            font-weight: bold;
            font-size: 1.2em;
            color: #2c5aa0;
            border-top: 2px solid #2c5aa0;
            padding-top: 10px;
            margin-top: 10px;
        }}
        .payment-terms {{
            background-color: #e3f2fd;
            padding: 15px;
            border-radius: 8px;
            margin-top: 30px;
            border-left: 4px solid #2c5aa0;
        }}
        @media (max-width: 600px) {{
            .header {{
                flex-direction: column;
                text-align: center;
            }}
            .invoice-details {{
                grid-template-columns: 1fr;
            }}
            .invoice-title {{
                font-size: 2em;
                margin-top: 15px;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <img src="data:image/png;base64,{self.logo_base64}" alt="W3EVOLUTIONS" class="logo">
        <div class="invoice-title">INVOICE</div>
    </div>

    <div class="invoice-info">
        <div style="text-align: center; font-size: 1.2em; font-weight: bold; color: #2c5aa0;">
            Invoice #{self.invoice_number}
        </div>
    </div>

    <div class="invoice-details">
        <div class="bill-to">
            <div class="section-title">BILL TO:</div>
            <div>
                <strong>National Exemption Service, LLC</strong><br>
                1981 Marcus Ave<br>
                Suite C-114<br>
                Lake Success, NY 11042
            </div>
        </div>
        
        <div class="invoice-meta">
            <div class="section-title">INVOICE DETAILS:</div>
            <div><strong>Invoice Date:</strong> {self.wip_entries[-1]['date']}</div>
            <div><strong>Due Date:</strong> Upon Receipt</div>
            <div><strong>Total Hours:</strong> {self.total_hours}</div>
            <div><strong>Period:</strong> {self.wip_entries[0]['date']} - {self.wip_entries[-1]['date']}</div>
        </div>
    </div>

    <table>
        <thead>
            <tr>
                <th>Date</th>
                <th>Hours</th>
                <th>Description</th>
                <th>Amount</th>
            </tr>
        </thead>
        <tbody>
            {line_items_html}
        </tbody>
    </table>

    <div class="totals">
        <div class="total-line">
            <span>Subtotal ({self.total_hours} hours × ${self.hourly_rate}/hour):</span>
            <span>${self.subtotal:,.2f}</span>
        </div>
        <div class="total-line">
            <span>Discount:</span>
            <span>-${self.discount:.2f}</span>
        </div>
        <div class="total-line total-final">
            <span>TOTAL:</span>
            <span>${self.total_amount:,.2f}</span>
        </div>
    </div>

    <div class="payment-terms">
        <div class="section-title">PAYMENT TERMS:</div>
        <p>Payment is due upon receipt. Please remit payment to the address above or contact us for electronic payment options.</p>
        <p><strong>Thank you for your business!</strong></p>
    </div>
</body>
</html>"""
        
        return html_content

    def generate_markdown_invoice(self):
        """Generate Markdown invoice"""
        
        # Generate line items
        line_items = ""
        for entry in self.wip_entries:
            line_items += f"| {entry['date']} | {entry['hours']} | {entry['description']} | ${entry['hours'] * self.hourly_rate:,.2f} |\n"

        markdown_content = f"""# INVOICE

![W3EVOLUTIONS Logo](assets/w3evolutions_logo.png)

## Invoice #{self.invoice_number}

**BILL TO:**
National Exemption Service, LLC
1981 Marcus Ave
Suite C-114
Lake Success, NY 11042

**INVOICE DETAILS:**
- **Invoice Date:** {self.wip_entries[-1]['date']}
- **Due Date:** Upon Receipt
- **Total Hours:** {self.total_hours}
- **Period:** {self.wip_entries[0]['date']} - {self.wip_entries[-1]['date']}

## Services Provided

| Date | Hours | Description | Amount |
|------|-------|-------------|--------|
{line_items}

## Summary

- **Subtotal ({self.total_hours} hours × ${self.hourly_rate}/hour):** ${self.subtotal:,.2f}
- **Discount:** -${self.discount:.2f}
- **TOTAL:** ${self.total_amount:,.2f}

## Payment Terms

Payment is due upon receipt. Please remit payment to the address above or contact us for electronic payment options.

**Thank you for your business!**
"""
        
        return markdown_content

    def generate_text_invoice(self):
        """Generate plain text invoice"""
        
        # Generate line items
        line_items = ""
        for entry in self.wip_entries:
            line_items += f"{entry['date']:<10} {entry['hours']:>5} hours  {entry['description']:<60} ${entry['hours'] * self.hourly_rate:>8,.2f}\n"

        text_content = f"""
W3EVOLUTIONS
                                    INVOICE

Invoice #{self.invoice_number}

BILL TO:
National Exemption Service, LLC
1981 Marcus Ave
Suite C-114
Lake Success, NY 11042

INVOICE DETAILS:
Invoice Date: {self.wip_entries[-1]['date']}
Due Date: Upon Receipt
Total Hours: {self.total_hours}
Period: {self.wip_entries[0]['date']} - {self.wip_entries[-1]['date']}

SERVICES PROVIDED:
Date       Hours  Description                                                     Amount
{'-'*90}
{line_items}
{'-'*90}

SUMMARY:
Subtotal ({self.total_hours} hours × ${self.hourly_rate}/hour):     ${self.subtotal:>10,.2f}
Discount:                                      -${self.discount:>10.2f}
                                              {'-'*15}
TOTAL:                                         ${self.total_amount:>10,.2f}

PAYMENT TERMS:
Payment is due upon receipt. Please remit payment to the address above 
or contact us for electronic payment options.

Thank you for your business!
"""
        
        return text_content

    def generate_json_data(self):
        """Generate JSON data for the invoice"""
        
        invoice_data = {
            "invoice_number": self.invoice_number,
            "invoice_date": self.wip_entries[-1]['date'],
            "due_date": "Upon Receipt",
            "bill_to": {
                "company": "National Exemption Service, LLC",
                "address": "1981 Marcus Ave",
                "suite": "Suite C-114",
                "city_state_zip": "Lake Success, NY 11042"
            },
            "period": {
                "start_date": self.wip_entries[0]['date'],
                "end_date": self.wip_entries[-1]['date']
            },
            "line_items": [
                {
                    "date": entry['date'],
                    "hours": entry['hours'],
                    "description": entry['description'],
                    "workers": entry['workers'],
                    "rate": self.hourly_rate,
                    "amount": entry['hours'] * self.hourly_rate
                }
                for entry in self.wip_entries
            ],
            "summary": {
                "total_hours": self.total_hours,
                "hourly_rate": self.hourly_rate,
                "subtotal": self.subtotal,
                "discount": self.discount,
                "total_amount": self.total_amount
            },
            "payment_terms": "Payment is due upon receipt. Please remit payment to the address above or contact us for electronic payment options."
        }
        
        return json.dumps(invoice_data, indent=2)

    def generate_all_formats(self):
        """Generate invoice in all formats"""
        
        print(f"Generating Invoice {self.invoice_number}...")
        print(f"Total Hours: {self.total_hours}")
        print(f"Total Amount: ${self.total_amount:,.2f}")
        
        # Generate all formats
        html_content = self.generate_html_invoice()
        markdown_content = self.generate_markdown_invoice()
        text_content = self.generate_text_invoice()
        json_content = self.generate_json_data()
        
        # Write files
        with open(f'{self.invoice_number}.html', 'w') as f:
            f.write(html_content)
        
        with open(f'{self.invoice_number}.md', 'w') as f:
            f.write(markdown_content)
        
        with open(f'{self.invoice_number}.txt', 'w') as f:
            f.write(text_content)
        
        with open(f'{self.invoice_number}.json', 'w') as f:
            f.write(json_content)
        
        print(f"\nInvoice files generated:")
        print(f"- {self.invoice_number}.html (Professional web format)")
        print(f"- {self.invoice_number}.md (Markdown format)")
        print(f"- {self.invoice_number}.txt (Plain text format)")
        print(f"- {self.invoice_number}.json (Structured data)")
        
        # Validation
        print(f"\nValidation:")
        print(f"✓ Invoice Number: {self.invoice_number}")
        print(f"✓ Total Hours: {self.total_hours}")
        print(f"✓ Hourly Rate: ${self.hourly_rate}")
        print(f"✓ Subtotal: ${self.subtotal:,.2f}")
        print(f"✓ Discount: ${self.discount:.2f}")
        print(f"✓ Total Amount: ${self.total_amount:,.2f}")
        print(f"✓ Calculation Check: {self.total_hours} × ${self.hourly_rate} - ${self.discount} = ${self.total_amount:,.2f}")

if __name__ == "__main__":
    generator = WIPInvoiceGenerator()
    generator.generate_all_formats()

