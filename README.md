\# 🏥 MIRA – Medical Intelligence Robotic Automation



An AI-powered health prediction system that analyses patient blood test results and generates intelligent health assessments.



\## Features

\- Full CRUD Operations (Create, Read, Update, Delete)

\- AI Health Predictions based on Glucose, Haemoglobin and Cholesterol

\- Search patients by name or email

\- Dashboard with health metrics overview

\- Input validation for all fields

\- SQLite persistent storage



\## Tech Stack

\- Frontend: Streamlit (Python)

\- Backend: Python 3.13

\- Database: SQLite

\- AI/ML: Rule-based prediction engine + Anthropic Claude API



\## How to Run

1\. Clone the repository

2\. Create virtual environment: `python -m venv venv`

3\. Activate: `venv\\Scripts\\activate`

4\. Install dependencies: `pip install -r requirements.txt`

5\. Create `.env` file from `.env.example` and add your API key

6\. Run: `streamlit run app.py`



\## Normal Blood Value Ranges

| Test | Normal Range | Unit |

|------|-------------|------|

| Glucose | 70–99 (fasting) | mg/dL |

| Haemoglobin | 12.0–17.5 | g/dL |

| Cholesterol | Below 200 | mg/dL |



\## Disclaimer

This application is for educational purposes only and is not a substitute for professional medical advice.

