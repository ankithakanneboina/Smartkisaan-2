# Smart Kisaan — AI-Powered Farmer Assistance Platform

A complete production-style full-stack web application for Indian smallholder farmers.

---

## Project overview

Smart Kisaan is a digital farming platform covering the full farmer journey:
registration → profile → weather → crop & fertilizer recommendations → disease detection → profit calculator → farm plan → market prices → AI assistant → community → marketplace → government schemes → video library.

All 12 phases are complete (Phases 1–11 fully implemented and tested; Phase 12 is this final integration + README).

---

## Tech stack

| Layer | Technology |
|---|---|
| Frontend | React 18, Vite, Tailwind CSS, React Router, Axios, Recharts |
| Backend | Python, Django 5, Django REST Framework, SimpleJWT |
| Database | SQLite (dev) → swappable to MySQL via `.env` (no code change) |
| ML | `ml_models/` package — rule-based predictors (crop, fertilizer); `DiseaseDetectionPredictor` stub awaiting trained model |
| Auth | JWT (access 30min, refresh 7 days, blacklisted on logout) |
| Voice | Web Speech API (browser-native, English + Telugu) |

---

## Architecture

```
Browser (React SPA)
  │  Axios + JWT interceptors (auto-refresh on 401)
  ▼
Django REST Framework  /api/...
  │
  ├── accounts      — User, JWT auth, password reset
  ├── farmers       — FarmerProfile (1:1 with User)
  ├── weather       — WeatherRecord, MockProvider / OpenWeatherMap
  ├── activities    — FarmActivity (sowing/irrigation/fertilizer/etc.)
  ├── reminders     — Reminder, NotificationPreference
  ├── crops         — Crop catalog, CropRecommendation
  ├── fertilizers   — Fertilizer catalog, FertilizerRecommendation
  ├── market        — MarketPrice (history + trend)
  ├── profit        — ProfitCalculation
  ├── diseases      — Disease catalog, DiseaseDetection
  ├── ai_assistant  — ChatMessage, RuleBasedFAQProvider / LLMProvider
  ├── farm_plan     — CropCalendarStage, FarmPlan, FarmPlanTask
  ├── schemes       — GovernmentScheme
  ├── videos        — Video, VideoFavorite, VideoWatchHistory
  ├── marketplace   — Product, Wishlist
  ├── community     — CommunityPost, Comment, PostLike, PostReport
  └── analytics     — admin-only aggregates (no separate model)
  │
  ▼
SQLite (dev) / MySQL (prod — same Django ORM models)

ml_models/  (sibling of backend/, not a Django app)
  ├── common/              — BasePredictor, PredictionResult
  ├── crop_recommendation/ — CropRecommendationPredictor (rule-based v1)
  ├── fertilizer_recommendation/ — FertilizerRecommendationPredictor (rule-based v1)
  └── disease_detection/   — DiseaseDetectionPredictor (stub — awaits trained model)
```

---

## Folder structure

```
smart-kisaan/
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── .env.example
│   ├── config/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── exception_handler.py   ← consistent {error, detail, code} API errors
│   │   ├── wsgi.py
│   │   └── asgi.py
│   └── apps/
│       └── <16 apps, each with models/serializers/views/urls/admin>
├── frontend/
│   ├── package.json
│   └── src/
│       ├── services/      ← one module per API domain
│       ├── context/       ← AuthContext, ToastContext
│       ├── components/    ← Card, DashboardLayout, ErrorBoundary, StateComponents, ...
│       ├── hooks/         ← useVoice, useApi
│       └── pages/         ← 19 pages
└── ml_models/
    ├── common/
    ├── crop_recommendation/
    ├── fertilizer_recommendation/
    └── disease_detection/
```

---

## Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- npm

### Backend setup

```bash
cd smart-kisaan/backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
# venv\Scripts\activate         # Windows

pip install -r requirements.txt

cp .env.example .env
# Edit .env — at minimum, change DJANGO_SECRET_KEY
```

### Frontend setup

```bash
cd smart-kisaan/frontend
npm install
```

---

## Database migration

```bash
cd backend
python manage.py makemigrations
python manage.py migrate
```

---

## Seed demo data

Run each command once after migrating. All are safe to re-run (`update_or_create`):

```bash
python manage.py seed_demo_data        # 7 crops + 3 fertilizers
python manage.py seed_market_data      # 14 days price history across 9 crop+market pairs
python manage.py seed_disease_data     # 4 crop disease reference entries
python manage.py seed_crop_calendar    # 7 lifecycle stages × 7 crops = 49 rows
python manage.py seed_video_data       # 5 demo video entries (PLACEHOLDER URLs — replace via /admin/)
python manage.py seed_marketplace_data # 5 demo products (fictional — replace via /admin/)
```

**Government schemes have no seed command** — per spec §15 ("Do not invent government scheme information"), add real scheme data via `/admin/` from an official source (e.g. myscheme.gov.in).

### Create a superuser (for /admin/ and analytics page)

```bash
python manage.py createsuperuser
```

---

## Run the application

Open **two terminals**:

```bash
# Terminal 1 — backend
cd backend && python manage.py runserver

# Terminal 2 — frontend
cd frontend && npm run dev
```

- Frontend: http://localhost:5173
- Backend API: http://127.0.0.1:8000/api/
- Django admin: http://127.0.0.1:8000/admin/

Vite proxies `/api` to `http://127.0.0.1:8000` in dev — no CORS issues.

---

## Environment variables

See `.env.example` for the full annotated list. Key variables:

| Variable | Default | Effect when blank |
|---|---|---|
| `DJANGO_SECRET_KEY` | `change-me` | **Change this before production** |
| `DJANGO_DEBUG` | `True` | Set `False` in production — activates security headers |
| `WEATHER_API_KEY` | _(blank)_ | Uses `MockWeatherProvider` — labeled "sample data" in UI |
| `AI_API_KEY` | _(blank)_ | Uses `RuleBasedFAQProvider` — 6 farming topics, EN + TE |
| `DB_ENGINE` | `sqlite3` | Fill in `mysql` + all `DB_*` vars to switch to MySQL |

---

## API endpoints (complete reference)

### Auth  `/api/auth/`
| Method | Endpoint | Auth | Purpose |
|---|---|---|---|
| POST | `register/` | public | Returns user + JWT pair |
| POST | `login/` | public | Email + password → JWT pair |
| POST | `refresh/` | public | Refresh access token |
| POST | `logout/` | ✓ | Blacklists refresh token |
| GET/PATCH | `me/` | ✓ | Own account |
| POST | `password-reset/` | public | Issues uid+token |
| POST | `password-reset-confirm/` | public | Sets new password |

### Farmers  `/api/farmers/`
| Method | Endpoint | Auth | Purpose |
|---|---|---|---|
| GET/PATCH | `me/` | ✓ | Own farmer profile (multipart for photo) |

### Weather  `/api/weather/`
| Method | Endpoint | Auth | Purpose |
|---|---|---|---|
| GET | `current/?location=` | ✓ | Current + 7-day forecast + alerts |

### Farm Activities  `/api/farm-activities/`
| Method | Endpoint | Auth | Purpose |
|---|---|---|---|
| GET/POST | `` | ✓ | List/create own activities |
| GET/PATCH/DELETE | `<id>/` | ✓ | Single activity |
| GET | `recent/` | ✓ | Last 5 (dashboard card) |

### Reminders  `/api/reminders/`
| Method | Endpoint | Auth | Purpose |
|---|---|---|---|
| GET/POST | `` | ✓ | List/create (respects preferences) |
| GET/PATCH/DELETE | `<id>/` | ✓ | Single reminder |
| GET | `upcoming/` | ✓ | Next 5 not-done (dashboard) |
| GET/PATCH | `preferences/` | ✓ | Notification type toggles |

### Crops  `/api/crops/`
| Method | Endpoint | Auth | Purpose |
|---|---|---|---|
| GET | `` | ✓ | Crop catalog |
| POST | `recommend/` | ✓ | Rule-based crop recommendation |
| GET | `recommendations/` | ✓ | Own recommendation history |

### Fertilizers  `/api/fertilizers/`
| Method | Endpoint | Auth | Purpose |
|---|---|---|---|
| GET | `` | ✓ | Fertilizer catalog |
| POST | `recommend/` | ✓ | Rule-based fertilizer recommendation |
| GET | `recommendations/` | ✓ | Own recommendation history |

### Market  `/api/market/`
| Method | Endpoint | Auth | Purpose |
|---|---|---|---|
| GET | `prices/?crop=&market=&sort=` | ✓ | Latest price per crop+market pair |
| GET | `prices/trend/?crop=&market=` | ✓ | Historical price series (labeled as history, not prediction) |

### Profit  `/api/profit/`
| Method | Endpoint | Auth | Purpose |
|---|---|---|---|
| POST | `calculate/` | ✓ | Compute + save profit calculation |
| GET | `history/` | ✓ | Own calculation history |

### Diseases  `/api/diseases/`
| Method | Endpoint | Auth | Purpose |
|---|---|---|---|
| GET | `` | ✓ | Disease reference catalog |
| POST | `detect/` | ✓ | Upload image — returns `status: unavailable` until model trained |
| GET | `history/` | ✓ | Own detection history |

### AI Assistant  `/api/ai/`
| Method | Endpoint | Auth | Purpose |
|---|---|---|---|
| POST | `chat/` | ✓ | Send message, get structured response |
| GET | `history/` | ✓ | Full chat thread |

### Farm Plan  `/api/farm-plan/`
| Method | Endpoint | Auth | Purpose |
|---|---|---|---|
| GET | `calendar/?crop=` | ✓ | Lifecycle stages for a crop |
| POST | `generate/` | ✓ | Generate personalized plan + tasks + reminders |
| GET | `plans/` | ✓ | Own saved plans |
| GET/PATCH/DELETE | `plans/<id>/` | ✓ | Single plan |
| GET/PATCH/DELETE | `tasks/<id>/` | ✓ | Single task (check off) |

### Schemes  `/api/schemes/`
| Method | Endpoint | Auth | Purpose |
|---|---|---|---|
| GET | `?search=&category=` | ✓ | Search/filter schemes |
| GET | `<id>/` | ✓ | Scheme detail |

### Videos  `/api/videos/`
| Method | Endpoint | Auth | Purpose |
|---|---|---|---|
| GET | `?search=&category=` | ✓ | Search/filter videos |
| GET | `favorites/` | ✓ | Favorited videos |
| GET | `history/` | ✓ | Watch history |
| POST | `<id>/favorite/` | ✓ | Toggle favorite |
| POST | `<id>/watch/` | ✓ | Log a watch event |

### Marketplace  `/api/marketplace/`
| Method | Endpoint | Auth | Purpose |
|---|---|---|---|
| GET | `products/?search=&category=` | ✓ | Search/filter products |
| GET | `products/<id>/` | ✓ | Product detail |
| POST | `products/<id>/wishlist/` | ✓ | Toggle wishlist |
| GET | `wishlist/` | ✓ | Wishlisted products |

### Community  `/api/community/`
| Method | Endpoint | Auth | Purpose |
|---|---|---|---|
| GET/POST | `posts/?search=&category=` | ✓ | List/create posts |
| GET/PATCH/DELETE | `posts/<id>/` | ✓ | Detail (edit/delete: author only) |
| GET/POST | `posts/<id>/comments/` | ✓ | List/add comments |
| POST | `posts/<id>/like/` | ✓ | Toggle like |
| POST | `posts/<id>/report/` | ✓ | Report for admin review |

### Analytics  `/api/analytics/`
| Method | Endpoint | Auth | Purpose |
|---|---|---|---|
| GET | `summary/` | admin only | Farmer counts, popular crops, feature usage |

---

## How frontend connects to backend

`src/services/api.js` is a single Axios instance (`baseURL: /api`, Vite proxies to Django). Request interceptor attaches `Authorization: Bearer <access>`. Response interceptor catches one 401, silently calls `/api/auth/refresh/`, retries the original request, and only redirects to `/login` if the refresh fails.

All API error responses are shaped `{error: true, detail: "...", code: "..."}` by `config/exception_handler.py`. The frontend reads `err.response.data.detail` uniformly.

---

## Demo credentials

After running all seed commands:

| Role | Email | Password |
|---|---|---|
| Admin | admin@example.com | AdminPass123! |
| Farmer | _(register via /register)_ | _(your choice)_ |

---

## Testing registration/login

```bash
# Register
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","email":"demo@example.com","phone_number":"9999999999","password":"StrongPass123!","password2":"StrongPass123!"}'

# Or open http://localhost:5173/register in your browser
```

---

## Production checklist

- [ ] Set `DJANGO_SECRET_KEY` to a 50+ character random string
- [ ] Set `DJANGO_DEBUG=False`
- [ ] Set `DJANGO_ALLOWED_HOSTS` to your domain
- [ ] Configure `DB_*` vars for MySQL
- [ ] Set `CORS_ALLOWED_ORIGINS` to your frontend domain
- [ ] Run `python manage.py collectstatic`
- [ ] Put Django behind Nginx/Gunicorn
- [ ] Serve React build (`npm run build` → `dist/`) via Nginx
- [ ] Set `WEATHER_API_KEY` (OpenWeatherMap) for live weather
- [ ] Set `AI_API_KEY` (Anthropic) for open-ended AI answers
- [ ] Replace placeholder video/product entries via `/admin/`
- [ ] Add real government scheme data via `/admin/`

---

## ML models — current status

| Predictor | Status | Notes |
|---|---|---|
| `CropRecommendationPredictor` | ✅ Rule-based v1 | Transparent scoring over 7 crops; swappable for trained scikit-learn model |
| `FertilizerRecommendationPredictor` | ✅ Rule-based v1 | NPK-gap analysis; swappable |
| `DiseaseDetectionPredictor` | ⏳ Stub | Returns `NotImplementedError`; API says `status: unavailable` honestly — no fake diagnosis |

To plug in a real trained model: implement `predict()` in the relevant `ml_models/<domain>/predictor.py` — Django views and frontend don't change.

---

## Future improvements

- Real disease detection model (TensorFlow/PyTorch image classification, PlantVillage dataset or similar)
- Email/SMS delivery for password reset and reminders (Phase 11 placeholders already in `PasswordResetRequestView`)
- IoT sensor data ingestion architecture (per §37 — interfaces/architecture ready, no fake sensors)
- PWA / offline support (§37)
- Dark mode (§37)
- Data export — farmer activity reports as CSV/PDF (§37)
- Crop profitability comparison across crops (§37)
- Smart Farm Health Score (§37)
- Crop Risk Score based on weather + market trends (§37)
- Real payment gateway integration for marketplace (architecture ready, payment flow is a clean addition)
- Redis-backed rate limiting (throttle keys already in DRF settings — one-line activation)
- Sentry/error monitoring integration (`ErrorBoundary.componentDidCatch` is the hook point)
