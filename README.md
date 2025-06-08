# NES Invoice Management System

A comprehensive system for managing and analyzing NES invoices from W3Evolutions.

## Repository Structure

```
nes-invoices/
├── invoices/           # Invoice files organized by type
│   ├── pdf/           # PDF invoice files (95 files)
│   ├── docx/          # DOCX invoice files (90 files)
│   └── special/       # Special cases (unbilled, corrected, email files)
├── docs/              # Documentation and analysis
├── scripts/           # Data processing and utility scripts
├── data/              # Extracted data and databases
├── web/               # Web interface for invoice management
└── README.md          # This file
```

## Invoice Collection Overview

- **Total Invoices:** 185+ invoice documents
- **Invoice Range:** NES01-5448 to NES01-5540
- **Date Range:** April 2023 to July 2024
- **Client:** National Exemption Service, LLC
- **Vendor:** W3Evolutions LLC / W3Evolutions Systems LLC
- **Service Type:** Software Development

## Key Features

### 1. Organized File Structure
- PDF and DOCX files separated for easy access
- Special cases (unbilled, corrected invoices) in dedicated folder
- Consistent naming convention maintained

### 2. Data Analysis Tools
- Invoice data extraction and parsing
- Summary reports and analytics
- Time tracking and billing analysis

### 3. Web Interface
- Search and filter invoices
- View invoice details and attachments
- Generate reports and summaries
- Dashboard with key metrics

## Invoice Data Structure

Each invoice typically contains:
- **Invoice Number:** NES01-XXXX format
- **Date:** Invoice date
- **Hours:** Time worked
- **Rate:** Hourly billing rate
- **Total:** Total amount due
- **Work Details:** Task descriptions and time logs
- **Payment Terms:** NET 30 or DOD (Due on Delivery)

## Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/daviderichammer/nes-invoices.git
   cd nes-invoices
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   npm install
   ```

3. **Run data extraction:**
   ```bash
   python scripts/extract_invoice_data.py
   ```

4. **Start web interface:**
   ```bash
   python web/app.py
   ```

## Usage

### Viewing Invoices
- Browse invoices by date, number, or amount
- View both PDF and DOCX versions
- Search by keywords or date ranges

### Analytics
- Total billing amounts by month/year
- Average hourly rates over time
- Work category breakdowns
- Payment status tracking

### Data Export
- Export invoice data to CSV/Excel
- Generate summary reports
- Create custom analytics

## Development

The system is built with:
- **Backend:** Python with Flask
- **Frontend:** HTML, CSS, JavaScript
- **Data Processing:** pandas, PyPDF2
- **Database:** SQLite for extracted data

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

[Add license information here]

## Contact

For questions or support, please contact the repository maintainer.

