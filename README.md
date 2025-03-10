# Sauce Demo Automation

This repository contains automation scripts for Sauce Labs Demo Application.

## Documentation

You can find the full documentation(Test Cases, and how to run the tests) for this project [here](https://github.com/Hadzee/Sauce-Demo-Automation/tree/master/Documentation).


## Getting Started

This project uses Playwright and Python to automate the tests. 
Below are the steps to set up the environment and run the automated tests.

First, clone the repository to your local machine if you haven't already.
If you don’t have Python installed, download and install Python from "python.org."

Once Python is installed, install the necessary libraries individually:
"pip install playwright pytest"

Once everything is set up, you can run the automated tests using pytest.
To run a specific test, for example, test_login.py, use:
"pytest tests/test_login.py"

To run all tests, simply run:
"pytest"

If Playwright can’t launch the browser, make sure the Playwright browser binaries are installed with:
"python -m playwright install"

I added __init__.py to my packages. Python packages should include an __init__.py file, even if it’s empty.
This tells Python that the directory should be treated as a package. 