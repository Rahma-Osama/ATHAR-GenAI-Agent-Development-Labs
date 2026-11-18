# Week 01 – Python Fundamentals 🐍

This folder contains the practical work for **Week 01** of the **ATHAR – Generative AI & Agent Development** training.

The lab focuses on applying fundamental Python concepts through a practical application that consumes data from a public REST API.

---

## 🧪 Lab: NASA Astronomy Explorer

A simple Python application that connects to NASA's Astronomy Picture of the Day (APOD) service, retrieves astronomy-related information, and presents it in a clear and organized way.

The application was developed as a practical exercise to apply Python fundamentals in a real-world API integration scenario.

---

## 🎯 Learning Objectives

The lab focuses on practicing:

- Python classes and objects
- Working with environment variables
- Making HTTP requests using Python
- Consuming REST APIs
- Parsing JSON responses
- Accessing and handling API data
- Handling optional JSON fields
- Formatting and displaying retrieved data
- Basic error handling and input validation

---

## 🚀 Application Features

The **NASA Astronomy Explorer** application can:

- Connect to the NASA astronomy API.
- Retrieve astronomy picture data.
- Display the picture title and date.
- Display the media type and description.
- Show the image URL.
- Display copyright information when available.
- Allow the retrieved data to be handled as Python objects.
- Download and save astronomy images.
- Save picture information as JSON.
- Open the image directly in a web browser.

---

## 🔌 API

The application uses the NASA Astronomy Picture API endpoint:

```text
https://science.nasa.gov/wp-json/wp/v2/apod-basic/
```

The API response is returned in JSON format and contains information about astronomy pictures and related metadata.

---

## 🛠️ Technologies

- **Python**
- **Requests**
- **python-dotenv**
- **REST API**
- **JSON**

---

## 📁 Project Structure

```text
NASA-Astronomy-Explorer/
│
├── main.py
├── .env
├── .gitignore
├── requirements.txt
│
└── data/
    ├── images/
    └── saved_pictures/
```

> The `.env` file is used to store the API key and should not be committed to the repository.

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/Rahma-Osama/ATHAR-GenAI-Agent-Development-Labs.git
```

### 2. Navigate to the lab

```bash
cd ATHAR-GenAI-Agent-Development-Labs
cd "week01-Python fundametals/NASA-Astronomy-Explorer"
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure the API key

Create a `.env` file:

```env
NASA_API_KEY=your_api_key_here
```

### 6. Run the application

```bash
python main.py
```

---

## 📌 Notes

This project is part of the practical exercises for the **ATHAR Generative AI & Agent Development** training.

The implementation may be extended and improved as the training progresses.

---

##  Author

**Rahma Osama**

Teaching Assistant | Computer Science

**ATHAR Initiative – Generative AI & Agent Development**