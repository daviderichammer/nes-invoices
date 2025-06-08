#!/usr/bin/env python3
"""
NES Invoice Generator for WIP Items
Generates a new invoice for Work In Progress items from Google Sheets time tracking data.
Includes W3EVOLUTIONS logo branding.
"""

import json
import base64
import os
from datetime import datetime
from typing import List, Dict

class WIPInvoiceGenerator:
    def __init__(self):
        # WIP data extracted from Google Sheets
        self.wip_entries = [
            {
                "date": "6/4/25",
                "hours": 12,
                "category": "Enhancement",
                "task": "AAE-101 - UAT bug tracker list review, development and bug fixes",
                "persons": "BK/DH"
            },
            {
                "date": "6/5/25", 
                "hours": 12,
                "category": "Enhancement",
                "task": "AAE-101 - UAT bug tracker list review, development and bug fixes",
                "persons": "BK/DH"
            }
        ]
        
        # Invoice configuration based on NES01-5540 format
        self.config = {
            "invoice_number": "NES01-5541",
            "customer_id": "NES01",
            "bill_to": {
                "name": "National Exemption Service, LLC",
                "address": "604 Packard Ct",
                "city_state_zip": "Safety Harbor, FL 34695"
            },
            "hourly_rate": 126,  # $126/hour (discounted from $175, $49 off)
            "base_rate": 175,
            "discount": 49,
            "terms": "NET 30",
            "sales_rep": "Brandon Kozak",
            "ship_via": "Email",
            "payment_info": {
                "payable_to": "W3Evolutions Systems LLC",
                "address": "4826 Troydale Rd, Tampa FL 33615",
                "zelle": "zelle.wf@w3evolutions.com"
            }
        }
        
        # Load logo base64 data
        self.logo_base64 = self.load_logo_base64()
    
    def load_logo_base64(self) -> str:
        """Load the W3EVOLUTIONS logo as base64 string"""
        try:
            logo_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'logo_base64.txt')
            with open(logo_path, 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            # Fallback embedded logo if file not found
            return "iVBORw0KGgoAAAANSUhEUgAAAZoAAABBCAIAAABn6vVsAAAA80lEQVR4nO3UwQ3AIBDAsNL9dz6WQEJE9gR5Zc3MB/C+/3YAwBl2BkTYGRBhZ0CEnQERdgZE2BkQYWdAhJ0BEXYGRNgZEGFnQISdARF2BkTYGRBhZ0CEnQERdgZE2BkQYWdAhJ0BEXYGRNgZEGFnQISdARF2BkTYGRBhZ0CEnQERdgZE2BkQYWdAhJ0BEXYGRNgZEGFnQISdARF2BkTYGRBhZ0CEnQERdgZE2BkQYWdAhJ0BEXYGRNgZEGFnQISdARF2BkTYGRBhZ0CEnQERdgZE2BkQYWdAhJ0BEXYGRNgZEGFnQISdARF2BkTYGRBhZ0DEBs2hA39LJu9AAAAAAElFTkSuQmCC"
    
    def calculate_totals(self) -> Dict:
        """Calculate invoice totals"""
        total_hours = sum(entry["hours"] for entry in self.wip_entries)
        total_amount = total_hours * self.config["hourly_rate"]
        
        return {
            "total_hours": total_hours,
            "total_amount": total_amount,
            "subtotal": total_amount,
            "tax": 0.00,
            "balance_due": total_amount
        }
    
    def get_invoice_date(self) -> str:
        """Get invoice date (last work date)"""
        # Convert to proper date format for invoice
        last_date = self.wip_entries[-1]["date"]  # 6/5/25
        return last_date.replace("/25", "/2025")  # 6/5/2025
    
    def generate_html_invoice(self) -> str:
        """Generate invoice in HTML format with embedded logo"""
        totals = self.calculate_totals()
        invoice_date = self.get_invoice_date()
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Invoice {self.config["invoice_number"]}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            color: #333;
        }}
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 30px;
        }}
        .logo {{
            max-width: 300px;
            height: auto;
        }}
        .invoice-title {{
            font-size: 36px;
            font-weight: bold;
            color: #666;
            text-align: right;
        }}
        .bill-to {{
            margin-bottom: 20px;
        }}
        .invoice-details {{
            margin-bottom: 30px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #f5f5f5;
            font-weight: bold;
        }}
        .amount {{
            text-align: right;
        }}
        .totals {{
            float: right;
            width: 300px;
            margin-top: 20px;
        }}
        .totals table {{
            width: 100%;
        }}
        .payment-info {{
            margin-top: 40px;
            padding: 15px;
            background-color: #f9f9f9;
            border-left: 4px solid #007acc;
        }}
        .time-details {{
            margin-top: 40px;
        }}
        .clear {{
            clear: both;
        }}
    </style>
</head>
<body>
    <div class="header">
        <img src="data:image/png;base64,{self.logo_base64}" alt="W3EVOLUTIONS Logo" class="logo">
        <div class="invoice-title">INVOICE</div>
    </div>
    
    <div class="bill-to">
        <strong>Bill To:</strong><br>
        {self.config["bill_to"]["name"]}<br>
        {self.config["bill_to"]["address"]}<br>
        {self.config["bill_to"]["city_state_zip"]}
    </div>
    
    <div class="invoice-details">
        <strong>Invoice No.:</strong> {self.config["invoice_number"]}<br>
        <strong>Customer ID:</strong> {self.config["customer_id"]}
    </div>
    
    <table>
        <tr>
            <th>Date</th>
            <th>Invoice No.</th>
            <th>Sales Rep.</th>
            <th>Ship Via</th>
            <th>Terms</th>
            <th>Date Due</th>
        </tr>
        <tr>
            <td>{invoice_date}</td>
            <td>{self.config["invoice_number"]}</td>
            <td>{self.config["sales_rep"]}</td>
            <td>{self.config["ship_via"]}</td>
            <td>{self.config["terms"]}</td>
            <td>-</td>
        </tr>
    </table>
    
    <table>
        <tr>
            <th>Quantity</th>
            <th>Item</th>
            <th>Description</th>
            <th>Discount</th>
            <th>Taxable</th>
            <th>Unit Price</th>
            <th>Total</th>
        </tr>
        <tr>
            <td>{totals["total_hours"]}</td>
            <td>Enhancement</td>
            <td>See attached</td>
            <td>${self.config["discount"]} / hr off ${self.config["base_rate"]} / hr</td>
            <td>No</td>
            <td class="amount">${self.config["hourly_rate"]}</td>
            <td class="amount">${totals["total_amount"]:,}</td>
        </tr>
        <tr>
            <td>-</td>
            <td>New Development</td>
            <td>See attached</td>
            <td>${self.config["discount"]} / hr off ${self.config["base_rate"]} / hr</td>
            <td>No</td>
            <td class="amount">${self.config["hourly_rate"]}</td>
            <td class="amount">-</td>
        </tr>
    </table>
    
    <div class="totals">
        <table>
            <tr>
                <td><strong>Subtotal:</strong></td>
                <td class="amount"><strong>${totals["subtotal"]:,}</strong></td>
            </tr>
            <tr>
                <td><strong>Tax:</strong></td>
                <td class="amount"><strong>{totals["tax"]:.2f}</strong></td>
            </tr>
            <tr>
                <td><strong>Balance Due:</strong></td>
                <td class="amount"><strong>${totals["balance_due"]:,}</strong></td>
            </tr>
        </table>
    </div>
    
    <div class="clear"></div>
    
    <div class="payment-info">
        <strong>Please make all checks payable to:</strong> {self.config["payment_info"]["payable_to"]}<br>
        <strong>Please send checks to:</strong> {self.config["payment_info"]["address"]}<br>
        <strong>Zelle:</strong> {self.config["payment_info"]["zelle"]}
    </div>
    
    <div class="time-details">
        <h3>Time Entry Details</h3>
        <table>
            <tr>
                <th>Date</th>
                <th>Hours</th>
                <th>Category</th>
                <th>Task/Work</th>
                <th>Persons</th>
            </tr>"""
        
        # Add time entries
        for entry in self.wip_entries:
            html += f"""
            <tr>
                <td>{entry['date']}</td>
                <td>{entry['hours']}</td>
                <td>{entry['category']}</td>
                <td>{entry['task']}</td>
                <td>{entry['persons']}</td>
            </tr>"""
        
        html += """
        </table>
    </div>
</body>
</html>"""
        
        return html
    
    def generate_markdown_invoice(self) -> str:
        """Generate invoice in Markdown format with logo"""
        totals = self.calculate_totals()
        invoice_date = self.get_invoice_date()
        
        markdown = f"""<div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 30px;">
<img src="data:image/png;base64,{self.logo_base64}" alt="W3EVOLUTIONS Logo" style="max-width: 300px; height: auto;">
<h1 style="font-size: 36px; color: #666; margin: 0;">INVOICE</h1>
</div>

**Invoice No.:** {self.config["invoice_number"]}

**Bill To:** {self.config["bill_to"]["name"]}  
{self.config["bill_to"]["address"]}  
{self.config["bill_to"]["city_state_zip"]}

**Customer ID:** {self.config["customer_id"]}

| Date | Invoice No. | Sales Rep. | Ship Via | Terms | Date Due |
|------|-------------|------------|----------|-------|----------|
| {invoice_date} | {self.config["invoice_number"]} | {self.config["sales_rep"]} | {self.config["ship_via"]} | {self.config["terms"]} | - |

| Quantity | Item | Description | Discount | Taxable | Unit Price | Total |
|----------|------|-------------|----------|---------|------------|-------|
| {totals["total_hours"]} | Enhancement | See attached | ${self.config["discount"]} / hr off ${self.config["base_rate"]} / hr | No | ${self.config["hourly_rate"]} | ${totals["total_amount"]:,} |
| - | New Development | See attached | ${self.config["discount"]} / hr off ${self.config["base_rate"]} / hr | No | ${self.config["hourly_rate"]} | - |

**Please make all checks payable to:** {self.config["payment_info"]["payable_to"]}  
**Please send checks to:** {self.config["payment_info"]["address"]}  
**Zelle:** {self.config["payment_info"]["zelle"]}

| | |
|---|---|
| **Subtotal:** | ${totals["subtotal"]:,} |
| **Tax:** | {totals["tax"]:.2f} |
| **Balance Due:** | ${totals["balance_due"]:,} |

## Time Entry Details

| Date | Hours | Category | Task/Work | Persons |
|------|-------|----------|-----------|---------|
"""
        
        # Add time entries
        for entry in self.wip_entries:
            markdown += f"| {entry['date']} | {entry['hours']} | {entry['category']} | {entry['task']} | {entry['persons']} |\n"
        
        return markdown
    
    def generate_text_invoice(self) -> str:
        """Generate invoice in plain text format matching PDF structure"""
        totals = self.calculate_totals()
        invoice_date = self.get_invoice_date()
        
        text = f"""W3EVOLUTIONS - YOUR BUSINESS EVOLVED

INVOICE
Invoice No.: {self.config["invoice_number"]}

Bill To: {self.config["bill_to"]["name"]}
{self.config["bill_to"]["address"]}
{self.config["bill_to"]["city_state_zip"]}

Customer ID: {self.config["customer_id"]}

Date            Invoice No.     Sales Rep.      Ship Via        Terms           Date Due
{invoice_date:<15} {self.config["invoice_number"]:<15} {self.config["sales_rep"]:<15} {self.config["ship_via"]:<15} {self.config["terms"]:<15} -

Quantity        Item            Description     Discount        Taxable         Unit Price      Total
{totals["total_hours"]:<15} Enhancement     See attached    ${self.config["discount"]} / hr off ${self.config["base_rate"]} / hr    No              ${self.config["hourly_rate"]:<15} ${totals["total_amount"]:,}
-               New Development See attached    ${self.config["discount"]} / hr off ${self.config["base_rate"]} / hr    No              ${self.config["hourly_rate"]:<15} -

Please make all checks payable to: {self.config["payment_info"]["payable_to"]}
Please send checks to: {self.config["payment_info"]["address"]}
Zelle: {self.config["payment_info"]["zelle"]}

                                                                Subtotal:       ${totals["subtotal"]:,}
                                                                Tax:            {totals["tax"]:.2f}
                                                                Balance Due:    ${totals["balance_due"]:,}

Date            Hours   Category        Task/Work                                               Persons
"""
        
        # Add time entries
        for entry in self.wip_entries:
            text += f"{entry['date']:<15} {entry['hours']:<7} {entry['category']:<15} {entry['task']:<55} {entry['persons']}\n"
        
        return text
    
    def save_invoice_files(self, output_dir: str = "."):
        """Save invoice in multiple formats"""
        import os
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate content
        html_content = self.generate_html_invoice()
        markdown_content = self.generate_markdown_invoice()
        text_content = self.generate_text_invoice()
        
        # Save files
        html_file = os.path.join(output_dir, f"Invoice-{self.config['invoice_number']}.html")
        markdown_file = os.path.join(output_dir, f"Invoice-{self.config['invoice_number']}.md")
        text_file = os.path.join(output_dir, f"Invoice-{self.config['invoice_number']}.txt")
        json_file = os.path.join(output_dir, f"Invoice-{self.config['invoice_number']}.json")
        
        with open(html_file, 'w') as f:
            f.write(html_content)
        
        with open(markdown_file, 'w') as f:
            f.write(markdown_content)
        
        with open(text_file, 'w') as f:
            f.write(text_content)
        
        # Save structured data as JSON
        invoice_data = {
            "invoice_number": self.config["invoice_number"],
            "invoice_date": self.get_invoice_date(),
            "customer": self.config["bill_to"],
            "totals": self.calculate_totals(),
            "entries": self.wip_entries,
            "config": self.config
        }
        
        with open(json_file, 'w') as f:
            json.dump(invoice_data, f, indent=2)
        
        return {
            "html": html_file,
            "markdown": markdown_file,
            "text": text_file,
            "json": json_file
        }

def main():
    """Main function to generate WIP invoice"""
    print("Generating NES Invoice for WIP Items with W3EVOLUTIONS Logo...")
    
    # Create generator
    generator = WIPInvoiceGenerator()
    
    # Calculate and display totals
    totals = generator.calculate_totals()
    print(f"Total Hours: {totals['total_hours']}")
    print(f"Total Amount: ${totals['total_amount']:,}")
    print(f"Invoice Number: {generator.config['invoice_number']}")
    print(f"Invoice Date: {generator.get_invoice_date()}")
    
    # Save files
    files = generator.save_invoice_files()
    print(f"\nInvoice files generated:")
    for format_type, filepath in files.items():
        print(f"  {format_type.upper()}: {filepath}")
    
    print(f"\nInvoice {generator.config['invoice_number']} generated successfully with W3EVOLUTIONS branding!")
    return files

if __name__ == "__main__":
    main()

