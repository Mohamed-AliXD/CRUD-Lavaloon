# CRUD Table App

A simple Flask + MySQL app for managing products (Create, Read, Update, Delete).

## Structure

```
app.py
database_setup.sql
templates/
├── index.html
├── add_product.html
└── edit_product.html
static/
└── style.css
```

## Setup

1. Run `database_setup.sql` in MySQL to create the database and table.
2. Open `app.py` and replace `YOUR_PASSWORD` with your MySQL password.
3. Install dependencies:

```bash
pip install flask pymysql
```

## Run

```bash
python app.py
```

Open `http://127.0.0.1:5000/` in your browser.

## Routes

- `/` — view all products
- `/add` — add a new product
- `/edit/<id>` — edit a product
- `/delete/<id>` — delete a product
