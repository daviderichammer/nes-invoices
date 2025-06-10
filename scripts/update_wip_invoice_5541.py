#!/usr/bin/env python3
"""
NES Invoice Generator - Updated WIP Invoice NES01-5541
Generates invoice for WIP entries matching the exact format of existing Invoice NES01-5541
"""

import json
import base64
from datetime import datetime

def generate_updated_wip_invoice():
    # WIP entries from Google Sheets (invoice number NES01-5541)
    wip_entries = [
        {
            "date": "6/4/25",
            "hours": 12,
            "description": "AAE-101 UAT bug tracker work",
            "persons": "BK/DH",
            "invoice": "NES01-5541"
        },
        {
            "date": "6/5/25", 
            "hours": 12,
            "description": "AAE-101 UAT bug tracker work",
            "persons": "BK/DH",
            "invoice": "NES01-5541"
        }
    ]
    
    # Calculate totals
    total_hours = sum(entry["hours"] for entry in wip_entries)
    hourly_rate = 126.00
    subtotal = total_hours * hourly_rate
    discount = 49.00
    total_amount = subtotal - discount
    
    # Get the last work date for invoice date
    invoice_date = "6/5/2025"
    
    # Read the existing logo base64
    try:
        with open('/home/ubuntu/nes-invoices/assets/logo_base64.txt', 'r') as f:
            logo_base64 = f.read().strip()
    except:
        logo_base64 = ""
    
    # Generate the updated invoice in the exact format of existing NES01-5541
    invoice_content = f"""<div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 30px;">
<img src="data:image/png;base64,{logo_base64}" alt="W3EVOLUTIONS" style="max-width: 300px; height: auto;">
<div style="font-size: 36px; font-weight: bold; color: #666; text-align: right;">INVOICE</div>
</div>

**BILL TO:**
National Exemption Service, LLC  
1234 Main Street  
Anytown, ST 12345

**INVOICE DETAILS:**
- **Invoice Number:** NES01-5541
- **Invoice Date:** {invoice_date}
- **Due Date:** Net 30

---

## Work Performed

| Date | Hours | Description | Personnel |
|------|-------|-------------|-----------|"""

    # Add work entries
    for entry in wip_entries:
        invoice_content += f"""
| {entry['date']} | {entry['hours']} | {entry['description']} | {entry['persons']} |"""

    invoice_content += f"""

---

## Summary

| Description | Hours | Rate | Amount |
|-------------|-------|------|--------|
| Software Development Services | {total_hours} | ${hourly_rate:.2f} | ${subtotal:.2f} |
| Discount | | | -${discount:.2f} |
| **TOTAL** | **{total_hours}** | | **${total_amount:.2f}** |

---

**Payment Terms:** Net 30 days  
**Payment Method:** Check or ACH transfer

Thank you for your business!

---
*W3EVOLUTIONS - Web Development & Software Solutions*"""

    # Create HTML version
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Invoice NES01-5541</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            color: #333;
            line-height: 1.6;
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
            padding: 12px;
            text-align: left;
        }}
        th {{
            background-color: #f5f5f5;
            font-weight: bold;
        }}
        .amount {{
            text-align: right;
        }}
        .total-row {{
            font-weight: bold;
            background-color: #f9f9f9;
        }}
        .payment-info {{
            margin-top: 40px;
            padding: 15px;
            background-color: #f9f9f9;
            border-left: 4px solid #007acc;
        }}
        hr {{
            border: none;
            border-top: 2px solid #ddd;
            margin: 30px 0;
        }}
    </style>
</head>
<body>
    <div class="header">
        <img src="data:image/png;base64,{logo_base64}" alt="W3EVOLUTIONS" class="logo">
        <div class="invoice-title">INVOICE</div>
    </div>

    <div class="bill-to">
        <strong>BILL TO:</strong><br>
        National Exemption Service, LLC<br>
        1234 Main Street<br>
        Anytown, ST 12345
    </div>

    <div class="invoice-details">
        <strong>INVOICE DETAILS:</strong><br>
        <strong>Invoice Number:</strong> NES01-5541<br>
        <strong>Invoice Date:</strong> {invoice_date}<br>
        <strong>Due Date:</strong> Net 30
    </div>

    <hr>

    <h2>Work Performed</h2>
    <table>
        <thead>
            <tr>
                <th>Date</th>
                <th>Hours</th>
                <th>Description</th>
                <th>Personnel</th>
            </tr>
        </thead>
        <tbody>"""

    # Add work entries to HTML
    for entry in wip_entries:
        html_content += f"""
            <tr>
                <td>{entry['date']}</td>
                <td>{entry['hours']}</td>
                <td>{entry['description']}</td>
                <td>{entry['persons']}</td>
            </tr>"""

    html_content += f"""
        </tbody>
    </table>

    <hr>

    <h2>Summary</h2>
    <table>
        <thead>
            <tr>
                <th>Description</th>
                <th>Hours</th>
                <th>Rate</th>
                <th class="amount">Amount</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Software Development Services</td>
                <td>{total_hours}</td>
                <td>${hourly_rate:.2f}</td>
                <td class="amount">${subtotal:.2f}</td>
            </tr>
            <tr>
                <td>Discount</td>
                <td></td>
                <td></td>
                <td class="amount">-${discount:.2f}</td>
            </tr>
            <tr class="total-row">
                <td><strong>TOTAL</strong></td>
                <td><strong>{total_hours}</strong></td>
                <td></td>
                <td class="amount"><strong>${total_amount:.2f}</strong></td>
            </tr>
        </tbody>
    </table>

    <div class="payment-info">
        <strong>Payment Terms:</strong> Net 30 days<br>
        <strong>Payment Method:</strong> Check or ACH transfer<br><br>
        Thank you for your business!
    </div>

    <hr>
    <p style="text-align: center; color: #666; font-style: italic;">
        W3EVOLUTIONS - Web Development & Software Solutions
    </p>
</body>
</html>"""

    # Create text version
    text_content = f"""
W3EVOLUTIONS
INVOICE

BILL TO:
National Exemption Service, LLC
1234 Main Street
Anytown, ST 12345

INVOICE DETAILS:
Invoice Number: NES01-5541
Invoice Date: {invoice_date}
Due Date: Net 30

========================================

WORK PERFORMED:
"""

    for entry in wip_entries:
        text_content += f"""
Date: {entry['date']}
Hours: {entry['hours']}
Description: {entry['description']}
Personnel: {entry['persons']}
"""

    text_content += f"""
========================================

SUMMARY:
Software Development Services: {total_hours} hours @ ${hourly_rate:.2f} = ${subtotal:.2f}
Discount: -${discount:.2f}
TOTAL: ${total_amount:.2f}

========================================

Payment Terms: Net 30 days
Payment Method: Check or ACH transfer

Thank you for your business!

W3EVOLUTIONS - Web Development & Software Solutions
"""

    # Create JSON data
    json_data = {
        "invoice_number": "NES01-5541",
        "invoice_date": invoice_date,
        "due_date": "Net 30",
        "bill_to": {
            "company": "National Exemption Service, LLC",
            "address": "1234 Main Street",
            "city_state_zip": "Anytown, ST 12345"
        },
        "work_entries": wip_entries,
        "summary": {
            "total_hours": total_hours,
            "hourly_rate": hourly_rate,
            "subtotal": subtotal,
            "discount": discount,
            "total_amount": total_amount
        },
        "payment_terms": "Net 30 days",
        "payment_method": "Check or ACH transfer"
    }

    # Write files
    with open('Invoice-NES01-5541-UPDATED.md', 'w') as f:
        f.write(invoice_content)
    
    with open('Invoice-NES01-5541-UPDATED.html', 'w') as f:
        f.write(html_content)
    
    with open('Invoice-NES01-5541-UPDATED.txt', 'w') as f:
        f.write(text_content)
    
    with open('Invoice-NES01-5541-UPDATED.json', 'w') as f:
        json.dump(json_data, f, indent=2)

    print(f"✅ Updated Invoice NES01-5541 generated successfully!")
    print(f"📊 Total Hours: {total_hours}")
    print(f"💰 Total Amount: ${total_amount:.2f}")
    print(f"📅 Invoice Date: {invoice_date}")
    print(f"📄 Files generated:")
    print(f"   - Invoice-NES01-5541-UPDATED.md")
    print(f"   - Invoice-NES01-5541-UPDATED.html") 
    print(f"   - Invoice-NES01-5541-UPDATED.txt")
    print(f"   - Invoice-NES01-5541-UPDATED.json")

if __name__ == "__main__":
    generate_updated_wip_invoice()

