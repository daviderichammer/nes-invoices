# WIP Invoice Generation Script - User Guide

## Quick Start

### Generate WIP Invoice
```bash
cd /home/ubuntu/nes-invoices
python3 scripts/generate_wip_invoice.py
```

This will generate:
- `Invoice-NES01-5541.md` - Markdown source
- `Invoice-NES01-5541.txt` - Text format  
- `Invoice-NES01-5541.pdf` - Professional PDF
- `Invoice-NES01-5541.json` - Structured data

### Current WIP Invoice Details
- **Invoice Number**: NES01-5541
- **Total Hours**: 24 hours
- **Total Amount**: $3,024
- **Date Range**: 6/4/25 to 6/5/25
- **Work**: AAE-101 - UAT bug tracker list review, development and bug fixes

## Script Customization

### For Future WIP Invoices

1. **Update WIP Data** in `scripts/generate_wip_invoice.py`:
```python
self.wip_entries = [
    {
        "date": "NEW_DATE",
        "hours": NEW_HOURS,
        "category": "Enhancement",  # or "New Development"
        "task": "TASK_DESCRIPTION",
        "persons": "BK/DH"  # or other team members
    }
    # Add more entries as needed
]
```

2. **Update Invoice Number**:
```python
"invoice_number": "NES01-XXXX",  # Increment as needed
```

3. **Update Rates** (if changed):
```python
"hourly_rate": 126,  # Current discounted rate
"base_rate": 175,    # Base rate
"discount": 49,      # Discount amount
```

### Output Directory
By default, files are saved to current directory. To specify location:
```python
files = generator.save_invoice_files("/path/to/output")
```

## File Formats

### Markdown (.md)
- Human-readable source format
- Easy to edit and customize
- Can be converted to PDF using `manus-md-to-pdf`

### Text (.txt)
- Plain text format matching PDF structure
- Good for email or simple viewing

### PDF (.pdf)
- Professional invoice document
- Ready for client delivery
- Generated automatically from Markdown

### JSON (.json)
- Structured data format
- Contains all invoice details
- Useful for integration with other systems

## Validation

The script includes built-in validation:
- ✅ Calculation verification (hours × rate = total)
- ✅ Data completeness check
- ✅ Format consistency validation

## Integration with Existing System

### Repository Structure
```
nes-invoices/
├── scripts/
│   └── generate_wip_invoice.py    # WIP invoice generator
├── generated_invoices/            # Output directory
│   ├── Invoice-NES01-5541.md
│   ├── Invoice-NES01-5541.txt
│   ├── Invoice-NES01-5541.pdf
│   └── Invoice-NES01-5541.json
└── docs/
    └── wip_invoice_generation_summary.md
```

### Workflow Integration
1. Identify WIP items in Google Sheets
2. Update script with WIP data
3. Run script to generate invoice
4. Review generated PDF
5. Send to client
6. Update Google Sheets status to "Billed"

## Troubleshooting

### Common Issues

**Script not executable:**
```bash
chmod +x scripts/generate_wip_invoice.py
```

**PDF generation fails:**
```bash
# Ensure manus-md-to-pdf is available
manus-md-to-pdf Invoice-NES01-5541.md Invoice-NES01-5541.pdf
```

**Calculation errors:**
- Check hourly rate and hours in script
- Verify WIP data accuracy
- Run validation function

### Support
For issues or customization needs, refer to:
- `docs/wip_invoice_generation_summary.md` - Complete project documentation
- `Invoice-NES01-5541.json` - Example structured data
- Existing invoice files for format reference

