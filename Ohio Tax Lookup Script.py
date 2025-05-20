import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import base64
import os
from datetime import datetime

class OhioTaxLookup:
    def __init__(self, root):
        self.root = root
        self.root.title("Ohio Tax Lookup Tool")
        self.root.geometry("800x650")
        
        self.create_widgets()
    
    def create_widgets(self):
        # Form Frame
        form_frame = tk.Frame(self.root, padx=20, pady=20)
        form_frame.pack(fill="x")
        
        # Address input
        tk.Label(form_frame, text="Address:").grid(row=0, column=0, sticky="w", pady=5)
        self.address_entry = tk.Entry(form_frame, width=50)
        self.address_entry.grid(row=0, column=1, sticky="w", pady=5)
        
        # Suite/Apt/Lot input
        tk.Label(form_frame, text="Suite/Apt/Lot:").grid(row=1, column=0, sticky="w", pady=5)
        self.suite_entry = tk.Entry(form_frame, width=50)
        self.suite_entry.grid(row=1, column=1, sticky="w", pady=5)
        
        # City input
        tk.Label(form_frame, text="City:").grid(row=2, column=0, sticky="w", pady=5)
        self.city_entry = tk.Entry(form_frame, width=50)
        self.city_entry.grid(row=2, column=1, sticky="w", pady=5)
        
        # Zip Code input
        tk.Label(form_frame, text="Zip Code:").grid(row=3, column=0, sticky="w", pady=5)
        self.zipcode_entry = tk.Entry(form_frame, width=15)
        self.zipcode_entry.grid(row=3, column=1, sticky="w", pady=5)
        
        # Zip+4 input (optional)
        tk.Label(form_frame, text="Zip+4 (optional):").grid(row=4, column=0, sticky="w", pady=5)
        self.zipplus_entry = tk.Entry(form_frame, width=10)
        self.zipplus_entry.grid(row=4, column=1, sticky="w", pady=5)
        
        # Tax lookup options
        lookup_frame = tk.LabelFrame(form_frame, text="Tax Lookup Options", padx=10, pady=10)
        lookup_frame.grid(row=5, column=0, columnspan=2, sticky="w", pady=10)
        
        # School District Tax option
        self.school_var = tk.BooleanVar(value=True)
        school_check = tk.Checkbutton(lookup_frame, text="School District Tax", variable=self.school_var)
        school_check.grid(row=0, column=0, sticky="w", padx=10)
        
        # Municipality Tax option
        self.municipal_var = tk.BooleanVar(value=False)
        municipal_check = tk.Checkbutton(lookup_frame, text="Municipality Tax", variable=self.municipal_var)
        municipal_check.grid(row=0, column=1, sticky="w", padx=10)
        
        # Browser and output options
        options_frame = tk.LabelFrame(form_frame, text="Options", padx=10, pady=10)
        options_frame.grid(row=6, column=0, columnspan=2, sticky="w", pady=10)
        
        # Headless mode checkbox
        self.headless_var = tk.BooleanVar(value=True)
        headless_check = tk.Checkbutton(options_frame, text="Run browser in background", variable=self.headless_var)
        headless_check.grid(row=0, column=0, sticky="w", padx=10)
        
        # Save PDF checkbox 
        self.save_pdf_var = tk.BooleanVar(value=False)
        save_pdf_check = tk.Checkbutton(options_frame, text="Save results as PDF", variable=self.save_pdf_var)
        save_pdf_check.grid(row=0, column=1, sticky="w", padx=10)
        
        # Submit button
        submit_button = tk.Button(form_frame, text="Submit", command=self.submit_form, 
                                 bg="#4CAF50", fg="white", padx=10, pady=5)
        submit_button.grid(row=7, column=0, columnspan=2, pady=15)
        
        # Results area
        results_frame = tk.Frame(self.root, padx=20, pady=10)
        results_frame.pack(fill="both", expand=True)
        
        tk.Label(results_frame, text="Results:").pack(anchor="w")
        self.result_text = scrolledtext.ScrolledText(results_frame, height=20, width=80)
        self.result_text.pack(fill="both", expand=True, pady=10)
    
    def log(self, message):
        """Add message to result text area and update UI"""
        self.result_text.insert(tk.END, message + "\n")
        self.result_text.see(tk.END)
        self.root.update()
    
    def submit_form(self):
        # Get input values
        address = self.address_entry.get().strip()
        suite = self.suite_entry.get().strip()
        city = self.city_entry.get().strip()
        zipcode = self.zipcode_entry.get().strip()
        zipplus = self.zipplus_entry.get().strip()
        
        # Check if at least one lookup option is selected
        if not self.school_var.get() and not self.municipal_var.get():
            messagebox.showerror("Error", "Please select at least one tax lookup option!")
            return
        
        # Validate input
        if not address or not city or not zipcode:
            messagebox.showerror("Error", "Address, City, and Zip Code are required!")
            return
        
        # Clear results
        self.result_text.delete(1.0, tk.END)
        self.log("Processing your request...")
        
        # Setup Chrome options
        options = webdriver.ChromeOptions()
        if self.headless_var.get():
            options.add_argument('--headless=new')
            options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        
        # REMOVED: Don't add --print-to-pdf option here
        # This was causing the error
        
        # Initialize the driver - we'll reuse it for both lookups if needed
        driver = webdriver.Chrome(options=options)
        
        try:
            results = {}
            
            # School District Tax lookup
            if self.school_var.get():
                self.log("\n--- SCHOOL DISTRICT TAX LOOKUP ---")
                school_district_tax_lookup = self.perform_lookup(
                    driver,
                    "https://thefinder.tax.ohio.gov/StreamlineSalesTaxWeb/AddressLookup/LookupByAddress.aspx?taxType=SchoolDist",
                    address, suite, city, zipcode, zipplus,
                    "School District",
                    ["lblSDName", "lblSDNum", "lblSDTaxRate", "lblDOESDNum"]
                )
                if school_district_tax_lookup:
                    fields = ['School District Name', 'School District Number', 'Income Tax Rate', 'Department of Education Number']
                    for val, field in zip(school_district_tax_lookup, fields):
                        results[field] = val
                
                # Save PDF if option is selected
                if self.save_pdf_var.get():
                    self.save_page_as_pdf(driver, f"SchoolDistrict_{address.replace(' ', '_')}_{city.replace(' ', '_')}")
            
            # Municipality Tax lookup
            if self.municipal_var.get():
                self.log("\n--- MUNICIPALITY TAX LOOKUP ---")
                municipality_lookup = self.perform_lookup(
                    driver,
                    "https://thefinder.tax.ohio.gov/StreamlineSalesTaxWeb/AddressLookup/LookupByAddress.aspx?taxType=Municipal",
                    address, suite, city, zipcode, zipplus,
                    "Municipality",
                    ["lblCountyName", "lblMuniName", "lblMuniFIPS", "lblMuniTaxRate"]
                )
                if municipality_lookup:
                    fields = ['County Name', 'Municipality Name', 'Municipality FIPS Code', 'Municipal Income Tax Rate']
                    for val, field in zip(municipality_lookup, fields):
                        results[field] = val
                
                # Save PDF if option is selected
                if self.save_pdf_var.get():
                    self.save_page_as_pdf(driver, f"Municipality_{address.replace(' ', '_')}_{city.replace(' ', '_')}")
            
            # Display summary of results
            if results:
                self.log("\n=== SUMMARY OF RESULTS ===")
                for tax_type, value in results.items():
                    self.log(f"{tax_type}: {value}")
            else:
                self.log("\nNo results were found for your lookup.")
                
        except Exception as e:
            self.log(f"An error occurred: {str(e)}")
            
        finally:
            # Clean up
            driver.quit()
            self.log("Browser closed.")
    
    def save_page_as_pdf(self, driver, filename_prefix):
        """Save the current page as PDF"""
        try:
            self.log("Saving page as PDF...")
            
            # Create a timestamp for the filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Ask user for save location
            default_filename = f"{filename_prefix}_{timestamp}.pdf"
            save_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                initialfile=default_filename
            )
            
            if not save_path:
                self.log("PDF save canceled by user.")
                return
            
            # Use CDP to print to PDF
            print_options = {
                'landscape': False,
                'displayHeaderFooter': False,
                'printBackground': True,
                'preferCSSPageSize': True,
                'scale': 1,
            }
            
            result = driver.execute_cdp_cmd("Page.printToPDF", print_options)
            
            # Convert base64 data to PDF file
            with open(save_path, 'wb') as file:
                file.write(base64.b64decode(result['data']))
            
            self.log(f"PDF saved successfully to: {save_path}")
        
        except Exception as e:
            self.log(f"Error saving PDF: {str(e)}")
            # Add more detailed error information
            import traceback
            self.log(traceback.format_exc())
            
    def perform_lookup(self, driver, url, address, suite, city, zipcode, zipplus, lookup_type, element_id):
        """Perform the lookup for a specific tax type and return the relevant value"""
        result_value = []
        
        try:
            # Navigate to the webpage
            self.log(f"Navigating to {url}")
            driver.get(url)
            
            # Wait for page to load
            self.log("Waiting for page to load...")
            time.sleep(2)
            
            # Fill in the form
            self.log("Filling out the form...")
            driver.find_element(By.NAME, "txtAddress").send_keys(address)
            driver.find_element(By.NAME, "txtAddress2").send_keys(suite)
            driver.find_element(By.NAME, "txtCity").send_keys(city)
            driver.find_element(By.NAME, "txtZip").send_keys(zipcode)
            if zipplus:
                driver.find_element(By.NAME, "txtZipPlus").send_keys(zipplus)
            
            # Submit the form - trying multiple possible button identifiers
            try:
                # First try to find a submit button by name
                submit_btn = driver.find_element(By.ID, "btnLookup")
                submit_btn.click()
            except NoSuchElementException:
                # Try to find all buttons and click one that seems relevant
                buttons = driver.find_elements(By.TAG_NAME, "button")
                submit_clicked = False
                for button in buttons:
                    text = button.text.lower()
                    if any(word in text for word in ["submit", "search", "lookup", "find"]):
                        button.click()
                        submit_clicked = True
                        break
                
                if not submit_clicked:
                    inputs = driver.find_elements(By.TAG_NAME, "input")
                    for input_elem in inputs:
                        input_type = input_elem.get_attribute("type")
                        input_value = input_elem.get_attribute("value")
                        if input_type == "submit" or (input_value and any(word in input_value.lower() for word in ["submit", "search", "lookup", "find"])):
                            input_elem.click()
                            submit_clicked = True
                            break
                
                if not submit_clicked:
                    self.log("Could not find submit button automatically. Taking screenshot for debugging...")
                    driver.save_screenshot(f"{lookup_type.lower().replace(' ', '_')}_form_screenshot.png")
                    self.log(f"Screenshot saved as '{lookup_type.lower().replace(' ', '_')}_form_screenshot.png'.")
                    raise Exception("Unable to find submit button")
            
            # Wait for results
            self.log("Waiting for results...")
            try:
                # Wait for the specific element with the ID we're looking for
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, element_id[0])))
            except TimeoutException:
                self.log(f"Timeout waiting for {element_id[0]} element. Continuing anyway...")
                time.sleep(5)  # Give additional time
            
            # Try to get the value from each span element
            for elements in element_id:
                try:
                    element = driver.find_element(By.ID, elements)
                    result_value.append(element.text.strip())
                    self.log(f"Found {elements}: {element.text.strip()}")
                except NoSuchElementException:
                    self.log(f"Element with ID '{elements}' not found on the page.")
                    result_value.append("Not found")
                    
                    # Take a screenshot for debugging if this is the first element (main one)
                    if elements == element_id[0]:
                        driver.save_screenshot(f"{lookup_type.lower().replace(' ', '_')}_results_screenshot.png")
                        self.log(f"Screenshot saved as '{lookup_type.lower().replace(' ', '_')}_results_screenshot.png' for debugging.")
                        
                        # Save page source for further debugging if needed
                        with open(f"{lookup_type.lower().replace(' ', '_')}_results_page.html", "w", encoding="utf-8") as f:
                            f.write(driver.page_source)
                        self.log(f"Saved page source to '{lookup_type.lower().replace(' ', '_')}_results_page.html' for debugging")
        
        except Exception as e:
            self.log(f"An error occurred during {lookup_type} lookup: {str(e)}")
            
            # Take a screenshot if possible
            try:
                driver.save_screenshot(f"{lookup_type.lower().replace(' ', '_')}_error_screenshot.png")
                self.log(f"Error screenshot saved as '{lookup_type.lower().replace(' ', '_')}_error_screenshot.png'")
            except:
                pass
        
        return result_value

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = OhioTaxLookup(root)
    root.mainloop()