
## 📡 Backend Setup (NoiseDB)

Install Docker 
`https://docs.docker.com/engine/install/ubuntu/`

1. Navigate to the `NoiseDB` directory:

```bash
cd NoiseDB
```

2. Build Docker containers:

```bash
docker compose build
```

3. Run the backend using Docker:

```bash
docker compose up
```

4. Backend will be accessible at:

```
http://localhost:8000
```

Here’s the corrected version:

---

## 📚 API Endpoints

### 5. Add User

- **Endpoint:**  
```
POST : http://0.0.0.0:8000/users
```

- **Request Body:**

```json
{
  "user_id": "User1",
  "first_name": "Temp",
  "last_name": "User"
}
```

---

## 📊 Load Data

1. Install required dependencies:

```bash
pip install -r requirements.txt
```

2. Run the script to load data from CSV to the database:

```bash
python csv_to_sql.py
```
---

## 🗺️ Frontend Setup (NoiseMap)

1. Open a new terminal and navigate to the `NoiseMap` directory:

```bash
cd NoiseMap
```

2. Install dependencies:

```bash
npm install
```

3. Run the frontend locally:

```bash
npm run dev
```

4. Frontend will be accessible at:

```
http://localhost:5173
```

---

## 🎨 Environment Variables

### Frontend (`NoiseMap`)

- Create a `.env` file in the `NoiseMap` directory with the following content:

```
VITE_GOOGLE_MAP_KEY=YOUR_GOOGLE_MAPS_API_KEY
```

---
