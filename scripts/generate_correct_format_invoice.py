#!/usr/bin/env python3
"""
NES Invoice Generator - Correct Format for NES01-5541
Uses the EXACT format from the user's image with all the proper tables and sections
"""

import json
from datetime import datetime

def generate_correct_format_invoice():
    # Use the NEW WIP data I found earlier (102 hours total)
    wip_entries = [
        {"date": "6/4/25", "hours": 17, "description": "AAE-101 UAT bug tracker list review, development and bug fixes", "persons": "BK/DH"},
        {"date": "6/5/25", "hours": 15, "description": "AAE-101 UAT bug tracker list review, development and bug fixes", "persons": "BK/DH"},
        {"date": "6/6/25", "hours": 16, "description": "AAE-101 UAT bug tracker + ERV2 prod issues, bandaid fixes for stage-qa", "persons": "BK/DH"},
        {"date": "6/7/25", "hours": 9, "description": "AAE-101 UAT bug tracker list review, development and bug fixes", "persons": "BK/DH"},
        {"date": "6/8/25", "hours": 10, "description": "AAE-101 UAT bug tracker list review, development and bug fixes", "persons": "BK/DH"},
        {"date": "6/9/25", "hours": 17, "description": "AAE-101 UAT bug tracker list review, development and bug fixes", "persons": "BK/DH"},
        {"date": "6/10/25", "hours": 18, "description": "AAE-101 UAT bug tracker list review, development and bug fixes", "persons": "BK/DH"}
    ]
    
    # Calculate totals
    total_hours = sum(entry["hours"] for entry in wip_entries)
    hourly_rate = 126.00
    discount_per_hour = 49.00
    effective_rate = hourly_rate  # The discount is shown separately
    subtotal = total_hours * hourly_rate
    total_discount = discount_per_hour  # Fixed discount amount
    balance_due = subtotal - total_discount
    
    # Invoice date is the last work date
    invoice_date = "6/10/2025"
    
    # Read the logo base64
    try:
        with open('/home/ubuntu/nes-invoices/assets/logo_base64.txt', 'r') as f:
            logo_base64 = f.read().strip()
    except:
        logo_base64 = ""
    
    # Create HTML with EXACT format from the image
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
            line-height: 1.4;
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
            font-size: 48px;
            font-weight: bold;
            color: #666;
            text-align: right;
        }}
        .invoice-info {{
            margin-bottom: 20px;
        }}
        .invoice-info div {{
            margin-bottom: 8px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }}
        th, td {{
            border: 1px solid #ccc;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #f0f0f0;
            font-weight: bold;
        }}
        .amount {{
            text-align: right;
        }}
        .payment-info {{
            margin: 20px 0;
            line-height: 1.6;
        }}
        .totals-table {{
            width: 300px;
            float: right;
            margin-top: 20px;
        }}
        .time-details {{
            clear: both;
            margin-top: 40px;
        }}
        .time-details h2 {{
            font-size: 24px;
            margin-bottom: 15px;
            color: #333;
        }}
    </style>
</head>
<body>
    <div class="header">
        <img src="data:image/png;base64,{logo_base64}" alt="W3EVOLUTIONS" class="logo">
        <div class="invoice-title">INVOICE</div>
    </div>

    <div class="invoice-info">
        <div><strong>Invoice No.:</strong> NES01-5541</div>
        <div><strong>Bill To:</strong> National Exemption Service, LLC</div>
        <div>604 Packard Ct</div>
        <div>Safety Harbor, FL 34695</div>
        <div><strong>Customer ID:</strong> NES01</div>
    </div>

    <table>
        <thead>
            <tr>
                <th>Date</th>
                <th>Invoice No.</th>
                <th>Sales Rep.</th>
                <th>Ship Via</th>
                <th>Terms</th>
                <th>Date Due</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>{invoice_date}</td>
                <td>NES01-5541</td>
                <td>Brandon Kozak</td>
                <td>Email</td>
                <td>NET 30</td>
                <td>-</td>
            </tr>
        </tbody>
    </table>

    <table>
        <thead>
            <tr>
                <th>Quantity</th>
                <th>Item</th>
                <th>Description</th>
                <th>Discount</th>
                <th>Taxable</th>
                <th>Unit Price</th>
                <th>Total</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>{total_hours}</td>
                <td>Enhancement</td>
                <td>See attached</td>
                <td>${total_discount} / hr off<br>${hourly_rate} / hr</td>
                <td>No</td>
                <td>${effective_rate}</td>
                <td>${balance_due:,.0f}</td>
            </tr>
            <tr>
                <td>-</td>
                <td>New Development</td>
                <td>See attached</td>
                <td>${total_discount} / hr off<br>${hourly_rate} / hr</td>
                <td>No</td>
                <td>${effective_rate}</td>
                <td>-</td>
            </tr>
        </tbody>
    </table>

    <div class="payment-info">
        <strong>Please make all checks payable to:</strong> W3Evolutions Systems LLC<br>
        <strong>Please send checks to:</strong> 4826 Troydale Rd, Tampa FL 33615<br>
        <strong>Zelle:</strong> zelle.wf@w3evolutions.com
    </div>

    <table class="totals-table">
        <tbody>
            <tr>
                <td><strong>Subtotal:</strong></td>
                <td class="amount">${subtotal:,.0f}</td>
            </tr>
            <tr>
                <td><strong>Tax:</strong></td>
                <td class="amount">0.00</td>
            </tr>
            <tr>
                <td><strong>Balance Due:</strong></td>
                <td class="amount">${balance_due:,.0f}</td>
            </tr>
        </tbody>
    </table>

    <div class="time-details">
        <h2>Time Entry Details</h2>
        <table>
            <thead>
                <tr>
                    <th>Date</th>
                    <th>Hours</th>
                    <th>Category</th>
                    <th>Task/Work</th>
                    <th>Persons</th>
                </tr>
            </thead>
            <tbody>"""

    # Add all time entries
    for entry in wip_entries:
        html_content += f"""
                <tr>
                    <td>{entry['date']}</td>
                    <td>{entry['hours']}</td>
                    <td>Enhancement</td>
                    <td>{entry['description']}</td>
                    <td>{entry['persons']}</td>
                </tr>"""

    html_content += """
            </tbody>
        </table>
    </div>
</body>
</html>"""

    # Create JSON data
    json_data = {
        "invoice_number": "NES01-5541",
        "invoice_date": invoice_date,
        "bill_to": {
            "company": "National Exemption Service, LLC",
            "address": "604 Packard Ct",
            "city_state_zip": "Safety Harbor, FL 34695"
        },
        "customer_id": "NES01",
        "sales_rep": "Brandon Kozak",
        "terms": "NET 30",
        "work_entries": wip_entries,
        "summary": {
            "total_hours": total_hours,
            "hourly_rate": hourly_rate,
            "subtotal": subtotal,
            "discount": total_discount,
            "balance_due": balance_due
        },
        "payment_info": {
            "payable_to": "W3Evolutions Systems LLC",
            "address": "4826 Troydale Rd, Tampa FL 33615",
            "zelle": "zelle.wf@w3evolutions.com"
        }
    }

    # Write files
    with open('Invoice-NES01-5541-CORRECT-FORMAT.html', 'w') as f:
        f.write(html_content)
    
    with open('Invoice-NES01-5541-CORRECT-FORMAT.json', 'w') as f:
        json.dump(json_data, f, indent=2)

    print(f"✅ Invoice NES01-5541 generated with CORRECT FORMAT!")
    print(f"📊 Total Hours: {total_hours}")
    print(f"💰 Subtotal: ${subtotal:,.0f}")
    print(f"💰 Balance Due: ${balance_due:,.0f}")
    print(f"📅 Invoice Date: {invoice_date}")
    print(f"📄 Files generated:")
    print(f"   - Invoice-NES01-5541-CORRECT-FORMAT.html")
    print(f"   - Invoice-NES01-5541-CORRECT-FORMAT.json")

if __name__ == "__main__":
    generate_correct_format_invoice()

