# Student Data Dashboard

Project for Data Base course 2025

Create student info database from given data and display it.

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

## Backend Setup (FastAPI)

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

5. **Run database migrations (table auto-creation)**

   Tables are auto-created at runtime. No additional migration tooling is required.

6. **Place data files**

   Copy any `.csv`, `.xlsx`, or `.json` files containing student information into `/backend/data/`. Use `sample_students.csv` as a reference for required columns:

   ```
   nim,name,program_studi,angkatan,ipk,email,phone
   ```

   The importer will attempt to normalise common variations such as `nama`, `prodi`, `gpa`, etc. Records are de-duplicated by `nim`.

7. **Start the API server**

   ```bash
   uvicorn main:app --reload
   ```

   The API will be available at <http://localhost:8000>.

## Frontend Setup (Svelte + Tailwind)

1. **Install dependencies**

   ```bash
   cd /home/nero/DATA-Share-2025/DATA-Share/frontend
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

## API Endpoints

- `GET /students` – list all students with optional `skip`, `limit`, and `search` query parameters.
- `GET /students/{id}` – fetch a student by numeric ID.
- `GET /students/search?name=xyz` – search by name (case-insensitive).
- `POST /sync` – re-import data files from `/backend/data/`.
- `GET /health` – simple health check.

## Optional Enhancements

- Tailwind-based loading shimmer placeholders while data is fetched.
- Toast notifications for sync success/failure.
- Dark-themed UI with responsive cards and modal detail view.

## Testing Tips

- Run `curl http://localhost:8000/students` to confirm the API is reachable.
- Use the included `sample_students.csv` to validate ingestion.
- Extend `Sample_students.csv` or add more files to verify merging logic and duplicate handling.

