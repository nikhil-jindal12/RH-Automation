# Ohio Tax Lookup Tool

## Overview
The Ohio Tax Lookup Tool is a desktop application that allows users to quickly retrieve Ohio tax information for any address in Ohio. The tool can look up:

1. **School District Tax Information** - Retrieves the school district name, district number, income tax rate, and Department of Education number
2. **Municipality Tax Information** - Retrieves the county name, municipality name, FIPS code, and municipal income tax rate

## Features
- Simple graphical user interface
- Ability to look up school district tax, municipality tax, or both at once
- Option to run the browser in the background (headless mode)
- Functionality to save results as PDF files
- Detailed logging of the lookup process

## Requirements

### If using the EXE file:
- Windows operating system
- Google Chrome browser installed
- Internet connection

### If using the Python script:
- Python 3.6 or higher
- Google Chrome browser installed
- Chrome WebDriver (matching your Chrome version)
- Required Python packages:
  - tkinter
  - selenium
  - base64
  - datetime

## Installation

### Option 1: Using the EXE file (Recommended for most users)
1. Simply download the EXE file
2. Double-click to run the application
3. No installation needed

### Option 2: Using the Python script

#### Step 1: Install Python (if not already installed)
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. **Important:** Check the box "Add Python to PATH" during installation
4. Complete the installation

#### Step 2: Install required packages
Open Command Prompt (cmd) and run:
```
pip install selenium
```
Note: tkinter comes pre-installed with Python

#### Step 3: Set up Chrome WebDriver
1. Check your Chrome version (Open Chrome → Menu → Help → About Google Chrome)
2. Download the matching ChromeDriver from [ChromeDriver Downloads](https://chromedriver.chromium.org/downloads)
3. Extract the chromedriver.exe file to a location on your computer
4. Add the ChromeDriver location to your system PATH, or place it in the same folder as the script

#### Step 4: Run the script
Navigate to the folder containing the script and run:
```
python ohio_tax_lookup.py
```

## How to Use

1. **Enter Address Information**
   - Address (required)
   - Suite/Apt/Lot (optional)
   - City (required)
   - Zip Code (required)
   - Zip+4 (optional)

2. **Select Lookup Options**
   - School District Tax (checked by default)
   - Municipality Tax

3. **Additional Options**
   - Run browser in background (checked by default) - hides the browser window during lookup
   - Save results as PDF - saves webpage results as a PDF file

4. **Click Submit**
   - The tool will navigate to the Ohio Department of Taxation website
   - Enter the address information
   - Retrieve the requested tax information
   - Display results in the application window
   - Save PDFs if requested

5. **Review Results**
   - School District information includes: District Name, District Number, Income Tax Rate, DOE Number
   - Municipality information includes: County Name, Municipality Name, FIPS Code, Income Tax Rate
   - A summary of all results is displayed at the end

## Troubleshooting

- **Submit button not found**: The application will attempt multiple methods to find and click the submit button. If all methods fail, it will save a screenshot for debugging.
- **Results not found**: If the lookup fails to find specific elements, the application will display "Not found" for those fields and save debugging information.
- **PDF saving errors**: If errors occur during PDF generation, check if you have write permission to the selected save location.
- **Browser errors**: Ensure Chrome is properly installed on your system. The application requires Chrome to function.

## Technical Details

The application works by:
1. Using Selenium WebDriver to control Chrome browser
2. Navigating to the Ohio Department of Taxation website
3. Automatically filling out the address form
4. Submitting the form and waiting for results
5. Extracting specific elements from the results page
6. Using Chrome's DevTools Protocol to generate PDFs when requested

## Privacy and Data

This application:
- Does not store or transmit your address information beyond sending it to the official Ohio Department of Taxation website
- Only saves data to your computer when you explicitly choose to save PDF results
- Creates temporary debug files (screenshots and HTML) in the application folder if errors occur

## Acknowledgments

This tool interacts with the Ohio Department of Taxation's [The Finder](https://thefinder.tax.ohio.gov) service to retrieve tax information.

## Disclaimer

This tool is provided for convenience and is not affiliated with or endorsed by the State of Ohio or the Ohio Department of Taxation. All tax information is sourced directly from the official Ohio Department of Taxation website.