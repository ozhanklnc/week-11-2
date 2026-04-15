# COMP 3304: Fundamentals of Software Engineering - CI/CD Pipeline Lab
## Project Overview

This repository contains the laboratory assignment for setting up a Continuous Integration (CI) pipeline using GitHub Actions. The application under test is a Python-based shopping cart system (`cart.py`), which includes deliberate bugs from the last week's assignment and missing implementations (such as the `get_item_count` method) to test the robustness of our CI/CD pipeline.

## Features & CI Pipeline Requirements

Our automated pipeline is designed to act as a strict quality gate, enforcing the following behaviors:

* **Automated Triggers:** The GitHub Actions workflow is configured to trigger automatically on every `push` to the `develop` branch.
* **Code Quality Gate (Linting & Formatting):** Before running tests, the pipeline enforces style and quality standards using linters and formatters (e.g., `flake8` and `black`) as an additional gate. If the code violates these standards, the pipeline fails early.
* **Automated Testing:** The pipeline runs the full test suite automatically using `pytest` to catch functional bugs in `cart.py`.
* **Branch Protection:** The `main` branch is safeguarded using GitHub's Branch Protection Rules. Pull requests and merges to `main` are strictly blocked if any of the required status checks (testing or linting) fail. 

## Repository Structure

```text
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions pipeline configuration
├── src/
│   └── cart.py             # The buggy shopping cart application
├── tests/
│   └── test_cart.py        # Test suite for the shopping cart
├── requirements.txt        # Python dependencies (pytest, flake8, black)
└── README.md               # Project documentation
