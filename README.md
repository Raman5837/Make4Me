
# About The Project
Make4Me is an E-Commerce application built with Python Django Framework. Some of the features of this project includes custom user model, categories and products, Carts, Incrementing, Decrementing and removing car items, Unlimited Product image gallery, Orders, Payments, after-order functionalities such as reduce the quantify of sold products, send the order received email, clearing the cart, Order completion page as well as generating an invoice for the order. Also we have a Review and Rating system with the interactive rating stars. My account functionalities for the customer who can easily edit his profile, profile pictures, change his account password, and also manage his orders and much more.

# Setup Instructions

1. Clone the repository
2. Navigrate To The Working Directory `cd Make4Me`
3. Create Virtual Environment Using Vitual-Env Or PipEnv
4. Install required packages to run the project `pip install -r requirements.txt`
5. Fill up the environment variables:
    _Your configuration should look something like this:_
    ```sh
    SECRET_KEY = A New Django Project Secret Key
    DEBUG = True
    EMAIL_HOST = smtp.gmail.com
    EMAIL_PORT = 465
    EMAIL_HOST_USER = Your Email Address
    EMAIL_HOST_PASSWORD = Password Of Your Email
    EMAIL_USE_TLS = True
    RAZORPAY_API = Your RazorPay Or Any Payment Gateway API
    ```
    _Note: If You Are Using Gmail Account, Make Sure You [ Turn ON The Less Secure Apps Feature ON For SMTP To Work ](https://myaccount.google.com/lesssecureapps)_
6. Create Database Tables
    ```sh
    python manage.py migrate
    ```
7. Create A Super User
    ```sh
    python manage.py createsuperuser
    ```
8. Run Server On LocalHost
    ```sh
    python manage.py runserver
    ```
9. Login To Admin Panel - `http://127.0.0.1:8000/secureLogin/`
10. Add Categories, Products, Add Variations, Register User, Login, Place Orders & EXPLORE SO MANY FEATURES


## Contact Me On
<p align="left">
  <a href="https://www.linkedin.com/in/aman5837/"><img alt="LinkedIn" title="LinkedIn" src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"/></a>
  <a href="mailto:amanverma5837@gmail.com"><img alt="Gmail" title="Gmail" src="https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white"/></a>
</p>

##
Made with ❤️ and Python
