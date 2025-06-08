# NES Invoice Management System - User Guide

## Overview

The NES Invoice Management System is a comprehensive solution for organizing, analyzing, and managing invoice data from W3Evolutions. The system includes automated data extraction, analytics, and a modern web interface.

## System Components

### 1. File Organization
- **PDF Invoices**: 95 invoice files in `invoices/pdf/`
- **DOCX Invoices**: 90 invoice files in `invoices/docx/`
- **Special Cases**: 5 files in `invoices/special/` (unbilled, corrected, email files)

### 2. Data Processing
- **Extraction Script**: `scripts/extract_invoice_data.py`
- **Analytics Script**: `scripts/generate_analytics.py`
- **Database**: CSV and JSON formats in `data/`

### 3. Web Interface
- **React Dashboard**: Modern, responsive interface in `invoice-dashboard/`
- **Features**: Search, filtering, analytics visualization, detailed reports

## Getting Started

### Prerequisites
```bash
# Python dependencies
pip install -r requirements.txt

# Node.js dependencies (for web interface)
cd invoice-dashboard
npm install
```

### Data Extraction
```bash
# Extract data from all PDF invoices
python3 scripts/extract_invoice_data.py

# Generate analytics and reports
python3 scripts/generate_analytics.py
```

### Web Interface
```bash
# Development mode
cd invoice-dashboard
npm run dev

# Production build
npm run build
```

## Features

### Data Analysis
- **Total Revenue**: $913,850 across 95 invoices
- **Total Hours**: 4,777 billable hours
- **Average Rate**: $191.30/hour effective rate
- **Date Range**: February 2023 to June 2024

### Analytics Dashboard
- Monthly revenue and hours trends
- Hourly rate distribution analysis
- Invoice amount distribution
- Performance metrics and insights

### Search and Filtering
- Search by invoice number, date, or amount
- Filter by date ranges and amounts
- Sort by various criteria
- Export capabilities

## Data Quality

### Validation Results
- **94/95** invoices have valid invoice numbers
- **95/95** invoices have valid dates
- **94/95** invoices have positive amounts
- **69/95** invoices have positive hours (some are $0 invoices)

### Known Issues
- 1 invoice missing invoice number
- 1 invoice with $0 amount
- 26 invoices with 0 hours (likely administrative or $0 invoices)

## File Structure

```
nes-invoices/
├── invoices/
│   ├── pdf/           # 95 PDF invoice files
│   ├── docx/          # 90 DOCX invoice files
│   └── special/       # 5 special case files
├── data/
│   ├── invoice_database.csv
│   ├── invoice_database.json
│   ├── invoice_summary.json
│   ├── analytics_report.md
│   └── invoice_analytics_dashboard.png
├── scripts/
│   ├── extract_invoice_data.py
│   └── generate_analytics.py
├── invoice-dashboard/  # React web application
├── docs/              # Documentation
└── requirements.txt   # Python dependencies
```

## Usage Examples

### Search Invoices
```javascript
// In the web interface
- Search "5500" to find invoice NES01-5500
- Search "2024" to find all 2024 invoices
- Search "15000" to find invoices around $15,000
```

### Data Analysis
```python
# Load and analyze data
import pandas as pd
df = pd.read_csv('data/invoice_database.csv')

# Monthly totals
monthly = df.groupby(df['date'].str[:7])['total_amount'].sum()

# Average rates by period
rates = df[df['unit_price'] > 0]['unit_price'].describe()
```

### Export Data
```bash
# CSV export is already available
# Additional formats can be generated:
python3 -c "
import pandas as pd
df = pd.read_csv('data/invoice_database.csv')
df.to_excel('invoice_export.xlsx', index=False)
"
```

## Troubleshooting

### Common Issues

1. **PDF Extraction Errors**
   - Ensure `pdftotext` is installed: `sudo apt-get install poppler-utils`
   - Check file permissions on PDF files

2. **Web Interface Not Loading**
   - Verify Node.js dependencies: `npm install`
   - Check port availability (default: 5173/5174)

3. **Data Inconsistencies**
   - Re-run extraction script: `python3 scripts/extract_invoice_data.py`
   - Check PDF file integrity

### Performance Tips

1. **Large Dataset Handling**
   - Use pagination in web interface for better performance
   - Consider database backend for very large datasets

2. **Analytics Generation**
   - Analytics are pre-generated for faster loading
   - Re-generate when new invoices are added

## Maintenance

### Adding New Invoices
1. Place PDF files in `invoices/pdf/`
2. Place DOCX files in `invoices/docx/`
3. Run extraction script: `python3 scripts/extract_invoice_data.py`
4. Regenerate analytics: `python3 scripts/generate_analytics.py`
5. Rebuild web interface if needed

### Backup Procedures
```bash
# Backup all data
tar -czf nes_invoices_backup_$(date +%Y%m%d).tar.gz \
  invoices/ data/ docs/ scripts/

# Backup database only
cp data/invoice_database.csv backups/
cp data/invoice_summary.json backups/
```

## Support

For technical support or questions:
1. Check this user guide
2. Review the analytics report in `data/analytics_report.md`
3. Examine the todo list in `docs/todo.md` for development status
4. Contact the repository maintainer

## License

This system is part of the NES Invoice Management repository. See repository license for terms of use.

