# Invoice Analysis Summary

## File Collection Overview
- **Total Files:** 191 files
- **PDF Files:** 96 invoices
- **DOCX Files:** 92 invoices  
- **EML Files:** 1 email file
- **Invoice Range:** NES01-5448 to NES01-5540
- **Special Files:** 
  - Invoice-NES01-5452-UNBILLED.docx
  - Invoice-NES01-5496corrected.docx/pdf
  - Invoice-NES01-5537.eml[1].eml/pdf

## Invoice Structure Analysis

### Standard Fields Identified:
1. **Invoice Number:** NES01-XXXX format
2. **Bill To:** National Exemption Service, LLC, 604 Packard Ct, Safety Harbor, FL 34695
3. **Customer ID:** NES01
4. **Date:** Invoice date
5. **Sales Rep:** Brandon Kozak
6. **Ship Via:** Email
7. **Terms:** DOD or NET 30
8. **Date Due:** Varies
9. **Item:** Software Development
10. **Quantity:** Hours worked
11. **Unit Price:** Hourly rate (varies, often discounted from $175/hr)
12. **Total Amount:** Calculated total
13. **Payment Info:** W3Evolutions LLC/Systems LLC payment details

### Sample Invoice Data:
- **Invoice 5450 (04/12/2023):** 10 hours @ $143.50/hr = $1,435.00
- **Invoice 5500 (07/25/2024):** 122 hours @ $126/hr = $15,372.00

### Key Patterns:
- All invoices are for software development services
- Hourly rates vary (discounted from base $175/hr)
- Detailed time tracking with task descriptions in later invoices
- Payment methods include checks and Zelle
- Two company names: W3Evolutions LLC and W3Evolutions Systems LLC

### Data Extraction Schema:
- Invoice Number
- Date
- Hours/Quantity
- Hourly Rate
- Total Amount
- Terms
- Due Date
- Detailed Work Log (when available)
- Company Name (W3Evolutions variant)

