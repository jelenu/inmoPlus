# InmoPlus 🏡

**InmoPlus** is a real estate management platform developed as a portfolio project to showcase backend development skills using **Django** and **Django REST Framework**. It provides a complete system for managing properties, contracts, clients, visits, users, and contact forms. The platform includes JWT authentication and an admin dashboard with statistics.

## 🚀 Key Features

- ✅ Role-based user management: **admin**, **agent**, and **viewer**.
- 🏘️ Full CRUD for properties with image support.
- 👥 Client management linked to agents.
- 📄 Creation and tracking of **rental** and **sales** contracts.
- 📅 Property visit scheduling and tracking.
- ✉️ Contact forms and favorites system for viewers.
- 📊 Admin dashboard with real-time statistics.
- 📚 Fully documented API using **Swagger** and **Redoc**.

## 🧩 Project Structure

- `accounts/` – User authentication and role management.
- `clients/` – Client module.
- `properties/` – Property and image management.
- `contracts/` – Real estate contracts.
- `visits/` – Property visit tracking.
- `dashboard/` – Stats and dashboard endpoints.
- `interactions/` – Favorites and contact forms.
- `seed.py` – Script to populate the database with test data.

## ⚙️ Installation

Follow these steps to deploy InmoPlus on a Linux server (Ubuntu/Debian):

1. **Update and install dependencies:**
   ```sh
   sudo apt update
   sudo apt upgrade -y
   sudo apt install python3 python3-pip python3-venv git nginx -y
   ```

2. **Clone the repository:**
   ```sh
   cd /srv/
   git clone https://github.com/jelenu/inmoplus.git myproject
   cd myproject
   ```

3. **Create and activate a virtual environment:**
   ```sh
   python3 -m venv env
   source env/bin/activate
   ```

4. **Install Python dependencies:**
   ```sh
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. **Install and configure PostgreSQL:**
   ```sh
   sudo apt install postgresql postgresql-contrib -y
   sudo -u postgres psql
   ```
   In the PostgreSQL shell, run:
   ```sql
   CREATE DATABASE inmoplusdb;
   CREATE USER inmoplususer WITH PASSWORD 'your_secure_password';
   ALTER ROLE inmoplususer SET client_encoding TO 'utf8';
   ALTER ROLE inmoplususer SET default_transaction_isolation TO 'read committed';
   ALTER ROLE inmoplususer SET timezone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE inmoplusdb TO inmoplususer;

   \c inmoplusdb
   GRANT ALL ON SCHEMA public TO inmoplususer;
   ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO inmoplususer;
   GRANT CONNECT ON DATABASE inmoplusdb TO inmoplususer;
   GRANT CREATE ON DATABASE inmoplusdb TO inmoplususer;
   ALTER SCHEMA public OWNER TO inmoplususer;
   \q
   ```

6. **Configure Django database settings (`settings.py`):**
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': config('DB_NAME'),
           'USER': config('DB_USER'),
           'PASSWORD': config('DB_PASSWORD'),
           'HOST': config('DB_HOST', default='localhost'),
           'PORT': config('DB_PORT', default='5432'),
       }
   }
   ```

7. **Create a `.env` file:**
   ```
   DB_NAME="inmoplusdb"
   DB_USER="inmoplususer"
   DB_PASSWORD="your_secure_password"
   SECRET_KEY="your_secret_key"
   ```

8. **Install PostgreSQL driver:**
   ```sh
   pip install psycopg2-binary
   ```

9. **Apply migrations and load data:**
   ```sh
   python manage.py migrate
   python seed.py
   python manage.py createsuperuser
   ```

10. **Configure static files in `settings.py`:**
    ```python
    STATIC_ROOT = BASE_DIR / 'staticfiles'
    ```

    Then collect static files:
    ```sh
    python manage.py collectstatic
    ```

11. **Install Gunicorn:**
    ```sh
    pip install gunicorn
    ```

12. **Create Gunicorn systemd service (`/etc/systemd/system/gunicorn.service`):**
    ```
    [Unit]
    Description=gunicorn daemon for Django project
    After=network.target

    [Service]
    User=www-data
    Group=www-data
    WorkingDirectory=/srv/myproject
    ExecStart=/srv/myproject/env/bin/gunicorn --access-logfile - --workers 3 --bind unix:/srv/myproject/gunicorn.sock inmoPlus.wsgi:application
    Environment="DJANGO_SETTINGS_MODULE=inmoPlus.settings"
    EnvironmentFile=/srv/myproject/.env

    [Install]
    WantedBy=multi-user.target
    ```

    Then enable and start Gunicorn:
    ```sh
    sudo systemctl daemon-reexec
    sudo systemctl start gunicorn
    sudo systemctl enable gunicorn
    ```

13. **Configure Nginx (`/etc/nginx/sites-available/inmoplus`):**
    ```
    server {
        listen 80;
        server_name inmoplus.yourdomain.com;

        location = /favicon.ico { access_log off; log_not_found off; }
        location /static/ {
            alias /srv/myproject/staticfiles/;
        }

        location / {
            include proxy_params;
            proxy_pass http://unix:/srv/myproject/gunicorn.sock;
        }
    }
    ```
    Enable the site and restart Nginx:
    ```sh
    sudo ln -s /etc/nginx/sites-available/inmoplus /etc/nginx/sites-enabled/
    sudo nginx -t
    sudo systemctl restart nginx
    sudo chown -R www-data:www-data /srv/myproject
    ```

14. **Set production settings in `settings.py`:**
    ```python
    DEBUG = False
    ALLOWED_HOSTS = ['inmoplus.yourdomain.com', 'your_server_ip', 'localhost', '127.0.0.1']
    ```

15. **(Optional) Enable HTTPS with Certbot:**
    ```sh
    sudo apt install certbot python3-certbot-nginx
    sudo certbot --nginx -d inmoplus.yourdomain.com
    ```

Now you can access your deployment at `https://inmoplus.yourdomain.com`.

> **Note:** Replace all placeholder values (`yourdomain.com`, `your_secure_password`, etc.) with your actual configuration. Remove or change any sensitive data before publishing.

## 🧪 Testing

Run tests using:

```sh
pytest
```

## 🔐 Authentication

This project uses JWT for authentication.

- Obtain a token at: `/api/accounts/token/`
- Use the token in requests by setting the header:
  ```
  Authorization: Bearer <token>
  ```

## 📘 API Documentation

- Swagger UI: [https://inmoplus.jesusleon-portfolio.com/api/docs/](https://inmoplus.jesusleon-portfolio.com/api/docs/)
- Redoc: [https://inmoplus.jesusleon-portfolio.com/api/redoc/](https://inmoplus.jesusleon-portfolio.com/api/docs/)

## 📝 License

This project is licensed under the MIT License.

## 👨‍💻 About Me

Developed by Jesús León Núñez — Backend Web Developer.  
📧 [jesusleon2700@gmail.com] | 💼 [LinkedIn] | 💻 [GitHub]

---