# AI Zakaat Calculator

## Overview

AI Zakaat Calculator is a local AI-powered financial tool that helps Muslims calculate their annual Zakaat based on Islamic principles.

The application automatically calculates Nisab using real-time gold and silver prices and provides an AI-generated explanation of the calculation.

This project was built to explore:

* AI integration with Python
* Financial calculation logic
* Local LLM usage
* SQLite database storage
* Streamlit UI development

---

## Features

* Zakaat calculation based on Islamic rules
* Automatic Nisab calculation
* Gold and Silver Nisab standards
* AI-generated explanation using local LLM (Ollama)
* Zakaat history tracking with SQLite
* Interactive web interface built with Streamlit

---

## Tech Stack

Python
Streamlit
SQLite
Ollama (Local LLM)
Requests API

---

## Project Structure

```
zakaat_ai_app/
│
├── app.py
├── calculator.py
├── ai_explainer.py
├── database.py
├── gold_silver_price.py
├── requirements.txt
├── README.md
└── zakaat.db
```

---

## Installation

Clone the repository:

```
git clone https://github.com/YOUR_USERNAME/ai-zakaat-calculator.git
cd ai-zakaat-calculator
```

Create virtual environment:

```
python -m venv venv
```

Activate environment:

Windows:

```
venv\Scripts\activate
```

Install dependencies:

```
pip install -r requirements.txt
```

---

## Running the Application

```
streamlit run app.py
```

---

## Future Improvements

* Cloud deployment
* User authentication
* Persistent cloud database
* Mobile app version
* Financial visualization dashboard
* Automated Nisab updates
