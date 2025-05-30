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

1. **Clone the repository:**
   ```sh
   git clone <repository-url>
   cd InmoPlus
   ```

2. **Create and activate a virtual environment:**
   ```sh
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Create a `.env` file in the root directory with at least:**
   ```
   SECRET_KEY=your_secret_key
   ```

5. **Apply migrations:**
   ```sh
   python manage.py migrate
   ```

6. **(Optional) Load test data:**
   ```sh
   python seed.py
   ```

7. **Run the development server:**
   ```sh
   python manage.py runserver
   ```

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

- Swagger UI: [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)
- Redoc: [http://localhost:8000/api/redoc/](http://localhost:8000/api/redoc/)

## 📝 License

This project is licensed under the MIT License.

## 👨‍💻 About Me

Developed by [Your Name] — Backend Web Developer.  
📧 [youremail@example.com] | 💼 [LinkedIn] | 💻 [GitHub]

---

_Replace the placeholders like `<repository-url>`, `[Your Name]`, and your LinkedIn/GitHub/email links with your actual info._