#!/usr/bin/env python3
"""
NES Invoice Generator for WIP Items
Generates a new invoice for Work In Progress items from Google Sheets time tracking data.
"""

import json
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
    
    def generate_markdown_invoice(self) -> str:
        """Generate invoice in Markdown format matching NES format"""
        totals = self.calculate_totals()
        invoice_date = self.get_invoice_date()
        
        markdown = f"""# INVOICE

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
            # Convert date format from 6/4/25 to 6/4/25 (keep as is for consistency)
            markdown += f"| {entry['date']} | {entry['hours']} | {entry['category']} | {entry['task']} | {entry['persons']} |\n"
        
        return markdown
    
    def generate_text_invoice(self) -> str:
        """Generate invoice in plain text format matching PDF structure"""
        totals = self.calculate_totals()
        invoice_date = self.get_invoice_date()
        
        text = f"""INVOICE
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
        markdown_content = self.generate_markdown_invoice()
        text_content = self.generate_text_invoice()
        
        # Save files
        markdown_file = os.path.join(output_dir, f"Invoice-{self.config['invoice_number']}.md")
        text_file = os.path.join(output_dir, f"Invoice-{self.config['invoice_number']}.txt")
        json_file = os.path.join(output_dir, f"Invoice-{self.config['invoice_number']}.json")
        
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
            "markdown": markdown_file,
            "text": text_file,
            "json": json_file
        }

def main():
    """Main function to generate WIP invoice"""
    print("Generating NES Invoice for WIP Items...")
    
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
    
    print(f"\nInvoice {generator.config['invoice_number']} generated successfully!")
    return files

if __name__ == "__main__":
    main()

