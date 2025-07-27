# Python Selenium Final Project

This is my final project for HackerU's **Automation Developer Course for Software Testers**.

For my project, I developed a web-based automation testing framework using **Python**, **Selenium WebDriver**, and **Pytest**, along with optional **Allure** reporting. It is designed to automate frontend functionality testing on the [Booking.com](https://www.booking.com) website.

---

## Features

- Web automation tests using Selenium WebDriver
- Clear project structure using Page Object Model
- Test organization with Pytest framework
- Test reporting with Allure

---

## 🔧 Technologies Used

- Python 3.13.3  
- Selenium  
- Pytest  
- Allure (for reporting)   
- Requests

---

## 📁 Project Structure
```
finalProject/
├── pages/ # Page Object classes
│ └── base_page.py # Base Page class with shared Selenium functions
├── tests/ # Test configuration and test files
│ ├── conftest.py # Pytest fixtures and setup
│ └── pytest.ini # Pytest configuration file
├── requirements.txt # Python dependencies
├── pyproject.toml # Project metadata and config
└── README.md # Project documentation
```

## ▶️ How to Run Tests

1. **Install dependencies**  
   *(Run this in the project folder where requirements.txt is located)*

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the tests**

   ```bash
    pytest
   ```

3. **(Optional) Generate Allure Report**

   ```bash
    pytest --alluredir=reports/
    allure serve reports/
   ```

---
## ⚙️ Pytest Configuration
Pytest is configured in pyproject.toml with:

- -v for verbose output
- testpaths = ["tests"] to limit discovery to the tests/ folder

---
## 🧪 Requirements
- Python 3.10 or higher
- Google Chrome browser
- Internet connection for WebDriver downloads

You can view all other required dependencies in requirements.txt or install them with:
   ```bash
    pip install -r requirements.txt
   ```
---
## 📌 Notes
- Further tests may still be added to the tests/ folder.
- Make sure your browser and ChromeDriver are compatible.
- Allure is optional but recommended for professional test reporting.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).  
© 2025 Chana Poch. You are free to use and modify this project, but please provide attribution.
