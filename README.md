# Bitlify 🔗🚀

**Bitlify** is a high-performance, open-source URL shortener API built for scalability and speed.  
It features asynchronous processing, real-time analytics, geo-tracking, and enterprise-grade security features like malware scanning and PIN protection.

Built with **FastAPI, Redis, PostgreSQL, and MongoDB**, Bitlify uses a **Write-Behind Caching architecture** to handle high-throughput traffic with minimal latency.

---

## 🌟 Key Features

### 🔗 Link Management
- **Custom Aliases** – Create vanity URLs (e.g., `bitlify.com/my-brand`)
- **Smart Redirection** – Sub-millisecond redirects served directly from Redis cache
- **Expiration Dates** – Auto-expire links at a specific time
- **QR Codes** – *(Planned)* Generate QR codes for any link

---

### 🛡️ Security & Safety
- **PIN Protection** – Secure sensitive links with a 4-digit PIN
- **Malware Scanning** – Scans original URLs using Google Safe Browsing API
- **Rate Limiting** – User/IP-based limits to prevent abuse

---

### 📊 Advanced Analytics
- **Real-Time Dashboard** – Live click tracking (updates every few seconds)
- **Historical Insights** – Hourly/daily trends stored in MongoDB
- **Rich Metadata** – Browser, OS, Referer, Country, City
- **Privacy-Focused** – Anonymized aggregation using HyperLogLog (concept)

---

## 🏗️ Architecture

Bitlify uses a **hybrid database architecture** for maximum performance:

- **FastAPI** – Async REST API backend
- **PostgreSQL** – Stores users and URL mappings
- **Redis**
  - Hot URL cache for instant redirects
  - Analytics event buffer (write-heavy)
- **MongoDB** – Time-series analytics storage
- **Background Worker** – Flushes analytics from Redis to MongoDB
- **Docker Compose** – Orchestrates the entire stack

---

## 🛠️ Tech Stack

- **Language:** Python 3.11+
- **Framework:** FastAPI
- **Databases:** PostgreSQL, MongoDB
- **Caching:** Redis
- **Task Queue:** APScheduler (AsyncIO)

### Libraries
- `sqlalchemy` – ORM
- `pymongo` – Async MongoDB driver
- `geoip2` – Geolocation
- `user_agents` – Device parsing
- `pydantic` – Data validation

---

## 🚀 Getting Started

### Prerequisites
- Docker & Docker Compose
- Google Safe Browsing API Key *(optional)*
- MaxMind **GeoLite2-City.mmdb** placed in `backend/app/`

---

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/bitlify.git
cd bitlify
```
## 2️⃣ Environment Configuration

Create a `.env` file in the `backend/` directory:

```env
# Database Credentials
DB_USER=postgres
DB_PASSWORD=password123
DB_NAME=bitlify_db
DB_HOST=db

# Redis & Mongo
REDIS_URL=redis://redis:6379/0
MONGO_URL=mongodb://admin:password@mongo:27017/bitlify_analytics

# Security
SECRET_KEY=super_secret_key
SAFE_BROWSING_KEY=your_google_api_key

# OAuth (Google)
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret
```

## 3️⃣ Run with Docker

Build and start the services:

```bash
cd backend
docker-compose up --build
```
The API will be available at `http://localhost:8000`.

## 📡 API Endpoints
### URLs
- `POST /shorten` - Shorten a new link.

  - Body: `{"original_url": "https://google.com", "custom_alias": "goog", "pin": 1234}`

- `GET /{short_code}` - Redirect to the original URL.

- `POST /{short_code}/verify` - Verify PIN for protected links.

### Analytics
- `GET /{short_code}/analytics/live` - Get real-time stats from Redis (current hour).

- `GET /{short_code}/analytics/history` - Get historical stats from MongoDB.

### Auth
- `GET /login/google` - Initiate OAuth login.

- `GET /auth/callback` - OAuth callback handler.

## 📂 Project Structure
bitlify/
├── backend/
│   ├── app/
│   │   ├── routers/        # API Routes (URLs, Auth)
│   │   ├── auth.py         # JWT & OAuth Logic
│   │   ├── models.py       # SQL Database Models
│   │   ├── schemas.py      # Pydantic Response Models
│   │   ├── task.py         # Background Workers (Redis -> Mongo)
│   │   ├── utils.py        # Helpers (Snowflake ID, GeoIP, Parsing)
│   │   ├── main.py         # App Entrypoint
│   │   └── ...
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── requirements.txt
└── todo.txt

## 🤝 Contributing
Contributions are welcome! Please open an issue or submit a pull request for any bugs or feature enhancements.

## 📄 License
MIT License.
