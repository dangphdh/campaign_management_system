# Campaign Management System

## Table of Contents
1. [Project Overview](#project-overview)
2. [Project Structure](#project-structure)
3. [Setup Instructions](#setup-instructions)
4. [Usage Guide](#usage-guide)
5. [Future Enhancements](#future-enhancements)

## Project Overview

The Campaign Management System is a web-based application designed to help users organize and track marketing campaigns. It allows users to create campaign groups, add campaigns to these groups, and record conversions for each campaign. The system uses a SQLite database to store information and provides a user-friendly web interface for data input and visualization.

Key features:
- Create and manage campaign groups
- Add campaigns with associated products and target audiences
- Record conversions for each campaign
- View all data in a hierarchical structure

## Project Structure

```
campaign_management_system/
│
├── app.py                 # Main Flask application
├── models.py              # SQLAlchemy database models
├── requirements.txt       # Python dependencies
│
├── static/
│   └── style.css          # CSS for styling the web interface
│
├── templates/
│   ├── layout.html        # Base template for all pages
│   ├── index.html         # Home page template
│   ├── add_group.html     # Template for adding campaign groups
│   ├── add_campaign.html  # Template for adding campaigns
│   └── add_conversion.html # Template for adding conversions
│
└── README.md              # This documentation file
```

## Setup Instructions

1. Ensure you have Python 3.7 or higher installed on your system.

2. Clone the repository or download the project files to your local machine.

3. Open a terminal/command prompt and navigate to the project directory.

4. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

5. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

6. Run the Flask application:
   ```
   python app.py
   ```

7. Open a web browser and navigate to `http://localhost:5000` to access the web interface.

## Usage Guide

### Home Page
- The home page displays all campaign groups, campaigns, and conversions in a hierarchical structure.
- Navigate to other pages using the links in the header.

### Adding a Campaign Group
1. Click on "Add Group" in the navigation menu.
2. Enter the name for the new campaign group.
3. Click "Add Group" to create the group.

### Adding a Campaign
1. Click on "Add Campaign" in the navigation menu.
2. Fill in the campaign details:
   - Campaign Name
   - Product Name
   - Target Audience
   - Select the Campaign Group from the dropdown
3. Click "Add Campaign" to create the campaign.

### Adding a Conversion
1. Click on "Add Conversion" in the navigation menu.
2. Fill in the conversion details:
   - Product Name
   - Action (e.g., "Purchase", "Sign-up")
   - Select the associated Campaign from the dropdown
3. Click "Add Conversion" to record the conversion.

## Future Enhancements

1. Edit and Delete Functionality
   - Implement features to edit and delete existing campaign groups, campaigns, and conversions.

2. User Authentication and Authorization
   - Add user accounts and login functionality.
   - Implement role-based access control for different user types (e.g., admin, manager, viewer).

3. Advanced Reporting and Analytics
   - Create detailed reports on campaign performance.
   - Implement data visualization features (e.g., charts, graphs) to better represent campaign data.

4. API Integration
   - Develop a RESTful API to allow integration with other marketing tools and platforms.

5. Improved User Interface
   - Enhance the frontend with JavaScript frameworks (e.g., React, Vue.js) for a more dynamic and responsive user experience.

6. Data Export and Import
   - Add functionality to export campaign data in various formats (e.g., CSV, JSON).
   - Implement data import features to allow bulk uploading of campaign information.

7. Automated Testing
   - Develop a comprehensive test suite for both backend and frontend components to ensure reliability and ease of maintenance.

By implementing these enhancements, the Campaign Management System can evolve into a more robust and feature-rich tool for marketing professionals.