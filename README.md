# Pharma Management System 

Pharma Management is a custom Odoo module designed for **PharmaTrack Pvt. Ltd.** to manage medical representatives, doctors, medicines, and prescriptions.

## Project Structure
- `models/`: Logic for Doctors, Medicines, and Prescriptions.
- `views/`: Form, Tree, and Kanban views.
- `wizards/`: Bulk prescription creation tool.
- `reports/`: Custom professional PDF prescription reports.
- `security/`: User access rights and security groups.

##  Key Features
- **Doctor Management:** Smart buttons for prescription history and specialization tracking.
- **Medicine Catalog:** Stock monitoring and low-stock alerts.
- **Professional PDF Report:** High-quality invoice-style "Doctor Prescription Summary".
- **Bulk Action:** Wizard for logging prescriptions for multiple doctors at once.

##  Installation & Testing
1. Clone the repository into your Odoo `custom_addons` folder.
2. Update the App List and install `pharma_management`.
3. To test the report, go to **Doctor Profile** and click the **Print** button.
4. To test the wizard, open **Prescription Assistant** from the menu.
