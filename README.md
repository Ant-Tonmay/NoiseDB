
## 📡 Backend Setup (NoiseDB)

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
