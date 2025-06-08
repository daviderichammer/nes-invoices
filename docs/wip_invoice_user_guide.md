# WIP Invoice Generation Script - User Guide

## Quick Start

### Generate Branded WIP Invoice
```bash
cd /home/ubuntu/nes-invoices
python3 scripts/generate_wip_invoice.py
```

This will generate **5 branded formats**:
- `Invoice-NES01-5541.html` - Professional HTML with W3EVOLUTIONS logo
- `Invoice-NES01-5541.md` - Logo-enhanced Markdown source
- `Invoice-NES01-5541.txt` - Text format  
- `Invoice-NES01-5541.pdf` - Professional PDF with branding
- `Invoice-NES01-5541.json` - Structured data

### Current WIP Invoice Details
- **Invoice Number**: NES01-5541
- **Total Hours**: 24 hours
- **Total Amount**: $3,024
- **Date Range**: 6/4/25 to 6/5/25
- **Work**: AAE-101 - UAT bug tracker list review, development and bug fixes
- **Branding**: W3EVOLUTIONS logo included in all formats

## 🎨 Logo Integration Features

### **Automatic Branding**
- **W3EVOLUTIONS Logo**: Extracted from existing invoices
- **Professional Layout**: Logo positioned in header alongside "INVOICE" title
- **Responsive Design**: Logo scales appropriately across formats
- **Consistent Styling**: Matches original invoice design

### **Logo Assets**
- **Source**: `assets/w3evolutions_logo.png` (410×65 pixels)
- **Embedded**: Base64 encoded for HTML/Markdown
- **Fallback**: Embedded backup if asset files missing
- **Quality**: High-resolution extraction from PDF source

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

### Logo Customization

#### **Update Logo**
1. Replace `assets/w3evolutions_logo.png` with new logo
2. Update `assets/logo_base64.txt` with new base64 encoding:
```bash
base64 -w 0 assets/new_logo.png > assets/logo_base64.txt
```

#### **Logo Positioning**
Modify CSS in the `generate_html_invoice()` method:
```css
.logo {
    max-width: 300px;  /* Adjust size */
    height: auto;
}
.header {
    display: flex;
    justify-content: space-between;  /* Logo left, title right */
    align-items: flex-start;
}
```

### Output Directory
By default, files are saved to current directory. To specify location:
```python
files = generator.save_invoice_files("/path/to/output")
```

## File Formats

### HTML (.html) - **NEW ENHANCED**
- **Professional layout** with embedded W3EVOLUTIONS logo
- **CSS styling** for print and web display
- **Responsive design** adapts to different screen sizes
- **Ready for email** or web publishing

### Markdown (.md) - **LOGO ENHANCED**
- **Logo embedded** as base64 image with styling
- **Human-readable** source format
- **Easy to edit** and customize
- **Converts to PDF** using `manus-md-to-pdf`

### Text (.txt)
- **Plain text** format matching PDF structure
- **Logo reference** in header
- **Good for email** or simple viewing

### PDF (.pdf)
- **Professional invoice** document with logo
- **Ready for client delivery**
- **Generated automatically** from Markdown

### JSON (.json)
- **Structured data** format
- **Contains all invoice details** including logo references
- **Useful for integration** with other systems

## Validation

The script includes built-in validation:
- ✅ **Calculation verification** (hours × rate = total)
- ✅ **Data completeness** check
- ✅ **Format consistency** validation
- ✅ **Logo integration** verification
- ✅ **File generation** confirmation

## Integration with Existing System

### Repository Structure
```
nes-invoices/
├── assets/                         # NEW: Logo assets
│   ├── w3evolutions_logo.png       # Extracted logo
│   ├── logo_base64.txt             # Base64 encoded logo
│   └── logo_context.png            # Reference context
├── scripts/
│   └── generate_wip_invoice.py     # ENHANCED: Logo integration
├── generated_invoices/             # Output directory
│   ├── Invoice-NES01-5541.html    # NEW: Branded HTML
│   ├── Invoice-NES01-5541.md      # ENHANCED: Logo included
│   ├── Invoice-NES01-5541.txt
│   ├── Invoice-NES01-5541.pdf     # ENHANCED: Branded PDF
│   └── Invoice-NES01-5541.json
└── docs/
    ├── logo_integration_summary.md # NEW: Logo documentation
    └── wip_invoice_user_guide.md   # UPDATED: This guide
```

### Workflow Integration
1. **Identify WIP items** in Google Sheets
2. **Update script** with WIP data
3. **Run script** to generate branded invoice
4. **Review generated files** (especially HTML/PDF)
5. **Send to client** (professional branded invoice)
6. **Update Google Sheets** status to "Billed"

## Troubleshooting

### Common Issues

**Script not executable:**
```bash
chmod +x scripts/generate_wip_invoice.py
```

**Logo not displaying:**
- Check `assets/w3evolutions_logo.png` exists
- Verify `assets/logo_base64.txt` contains valid base64 data
- Script includes fallback logo if files missing

**PDF generation fails:**
```bash
# Ensure manus-md-to-pdf is available
manus-md-to-pdf generated_invoices/Invoice-NES01-5541.md generated_invoices/Invoice-NES01-5541.pdf
```

**HTML logo issues:**
- Logo embedded as base64, should work offline
- Check browser console for any image loading errors
- Verify base64 data is valid

### Logo Asset Management

**Extract logo from new invoice:**
```python
from PIL import Image
img = Image.open('new_invoice.png')
logo = img.crop((50, 85, 460, 150))  # Adjust coordinates as needed
logo.save('assets/w3evolutions_logo.png')
```

**Generate new base64:**
```bash
base64 -w 0 assets/w3evolutions_logo.png > assets/logo_base64.txt
```

### Support
For issues or customization needs, refer to:
- `docs/logo_integration_summary.md` - Complete logo integration documentation
- `docs/wip_invoice_generation_summary.md` - Original project documentation
- `generated_invoices/Invoice-NES01-5541.json` - Example structured data
- Existing invoice files for format reference

## 🎯 Key Benefits

### **Professional Branding**
- ✅ **W3EVOLUTIONS logo** automatically included
- ✅ **Consistent design** matches existing invoices
- ✅ **Client confidence** through professional presentation
- ✅ **Brand recognition** in all communications

### **Enhanced Automation**
- ✅ **One command** generates 5 branded formats
- ✅ **No manual work** required for logo insertion
- ✅ **Quality assurance** through automated validation
- ✅ **Future-proof** design for easy updates

The enhanced WIP invoice generation script now provides complete professional branding while maintaining all the efficiency and accuracy of the original automation.

