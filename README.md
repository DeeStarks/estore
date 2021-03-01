# EStore Online Marketplace

This is an Ecommerce web app using Python (Django).

Feel free to make changes. And if you love the project, do ADD a STAR ⭐️.

## Features of this Project

### A. Seller

1. Buy and Sell Products
2. View and Review Products
3. Checkout from shopping cart
4. Like and add products to wishlist

### B. Customer:

1. Buy Products
2. View and Review Products
3. Checkout from shopping cart
4. Like and add products to wishlist

### C. Guest:

1. View Products


## Installation/Running

### Pre-Requisites:

1. Install <a href="https://git-scm.com/">Git Version Control</a>

2. Install <a href="https://www.python.org/downloads/">Python Latest Version</a>

3. Install Pip <a href="https://pip.pypa.io/en/stable/installing/">Package Manager</a>

*Homebrew can also be used as an alternative to pip*

### Installation

**1. Create a Virtual Environment and Activate**

Install Virtual Environment
```
$  pip install virtualenv
```

Create Virtual Environment

```
$  virtualenv venv
```

Activate Virtual Environment

For Windows
```
$  cd venv/scripts&&activate
```

For Mac/Linux
```
$  source venv/bin/activate
```

**2. Navigate to the project's base directory**

**3. Install Requirements from 'requirements.txt'**
```python
$  pip install -r requirements.txt
```


**4. Run Server**

NB: Before running server, `python manage.py migrate` to add all models into database schema if not yet added.

```python
$ python manage.py runserver
```
Server will run on `http://127.0.0.1:8000/`

