# Student Data Dashboard

Project for Data Base class 2025

Create student info database from given data and display it.

by:
- Ziad Parawansa (F1B02310149)
- Nabiel Zahiddin (F1B02310138)
- Muhammad Amri Al jabbar (F1B02310126)
## Project Structure

```
DATA-Share/
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   ├── crud.py
│   ├── schemas.py
│   ├── requirements.txt
│   ├── data/
│   │   └── sample_students.csv
│   └── .env.example
└── frontend/
    ├── src/
    │   ├── App.svelte
    │   ├── app.css
    │   ├── main.js
    │   ├── lib/api.js
    │   └── components/
    │       ├── SearchBar.svelte
    │       ├── StudentCard.svelte
    │       └── StudentDetailModal.svelte
    ├── package.json
    ├── tailwind.config.js
    └── index.html
```

## Prerequisites

- Python 3.10+
- Node.js 18+
- MySQL 8.x (local installation or Docker)

## Backend Setup

1. **Create and activate a virtual environment**

   ```bash
   cd /home/$USER/DATA-Share-2025/DATA-Share/backend
   python -m venv .venv
   source .venv/bin/activate
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure MySQL credentials**

   ```bash
   cp .env.example .env
   ```

   Update `.env` with your MySQL credentials. Expected keys:

   ```
   DB_USER=root
   DB_PASS=yourpassword
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=student_db
   ```

4. **Create the database**

   ```sql
   CREATE DATABASE IF NOT EXISTS student_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

5. **Place data files**

   Copy any `.csv`, `.xlsx`, or `.json` files containing student information into `/backend/data/`. Use `sample_students.csv` as a reference for required columns:

   ```
   nim,name,program_studi,angkatan,ipk,email,phone
   ```

   The importer will attempt to normalise common variations such as `nama`, `prodi`, `gpa`, etc. Records are de-duplicated by `nim`.

6. **Start the API server**

   ```bash
   uvicorn main:app --reload
   ```

   The API will be available at <http://localhost:8000>.

## Frontend Setup (Svelte + Tailwind)

1. **Install dependencies**

   ```bash
   cd /home/$USER/DATA-Share-2025/DATA-Share/frontend
   npm install
   ```

2. **Configure the backend URL (optional)**

   Create a `.env` file in `frontend/` if you need to override the default API URL:

   ```
   VITE_API_URL=http://localhost:8000
   ```

   The Vite dev server proxies `/api` requests to the backend based on this value.

3. **Run the development server**

   ```bash
   npm run dev
   ```

   Access the frontend at <http://localhost:5173>.

## Usage Workflow

1. Place new data files in `backend/data/`.
2. Start the backend (`uvicorn`) and ensure it connects to MySQL.
3. Launch the frontend (`npm run dev`).
4. Open the dashboard in your browser.
5. Click **Sync Data** to invoke the `/sync` endpoint and import the latest files.
6. Use the search bar to filter students by name and click **View Detail** for additional information.
