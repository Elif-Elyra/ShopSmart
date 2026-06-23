# ShopSmart

A full-stack e-commerce marketplace where buyers and sellers transact on a single platform — built with **Django 6** and **Vue.js 3**.

Single-server architecture: Django serves the Vue.js SPA and the REST API — one command runs everything.

---

## Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Backend | Django | 6.x |
| API | Django REST Framework | 3.x |
| Auth | SimpleJWT | 5.x |
| Filtering | django-filter | 25.x |
| Payments | Stripe | 15.x |
| Email / OTP | SendGrid | — |
| Images | Pillow | 12.x |
| Frontend | Vue.js | 3.5 |
| Build Tool | Vite | 8.x |
| Router | Vue Router | 5.x |
| State | Pinia | 3.x |
| HTTP Client | Axios | 1.x |
| CSS | Bootstrap 5.3.8 + Tailwind CSS 3.x |
| Icons | Lucide Vue Next |
| Package Manager | Poetry (Python), npm (Node.js) |

---

## Project Structure

```
ShopSmart/
├── manage.py                        # Django management script
├── pyproject.toml                   # Python dependencies (Poetry)
├── db.sqlite3                       # SQLite database (development)
├── mediafiles/                      # Uploaded product images
│
├── core/                            # Django project config
│   ├── settings.py                  # All Django configuration
│   ├── urls.py                      # Root URL routing (API + SPA catch-all)
│   ├── middleware.py                # LowercaseURLMiddleware
│   ├── wsgi.py                      # WSGI entry point
│   └── asgi.py
│
├── apps/                            # All Django apps
│   ├── __init__.py
│   │
│   ├── account/                     # Users, auth, wallet, addresses, withdrawals
│   │   ├── models.py                # User, OTP, Address, Wallet, WalletTransaction, BankAccount, Withdrawal
│   │   ├── serializer.py            # Auth, profile, wallet serializers
│   │   ├── views.py                 # CBV: Register, Login, Logout, Profile, Wallet, Withdrawals
│   │   ├── signals.py               # Auto-send OTP on new user registration
│   │   ├── admin.py                 # UserAdmin, AddressAdmin, WalletAdmin, WithdrawalAdmin
│   │   ├── urls.py                  # JWT + auth + wallet endpoints
│   │   └── tests.py
│   │
│   ├── catalog/                     # Products, categories, cart
│   │   ├── models.py                # Category, Product, ProductImage, Cart, CartItem
│   │   ├── serializers.py           # List/detail serializers for all catalog models
│   │   ├── views.py                 # ViewSets for products (public & seller), cart, categories
│   │   ├── permissions.py           # IsSeller, IsOwnerOrReadOnly custom permissions
│   │   ├── services.py              # Business logic helpers
│   │   ├── admin.py                 # ModelAdmin for catalog models
│   │   ├── urls.py                  # DRF Router-based URLs
│   │   └── tests.py
│   │
│   └── orders/                      # Orders, checkout, reviews, notifications
│       ├── models.py                # Order, SubOrder, OrderItem, Review, Notification, IdempotencyKey
│       ├── serializers.py           # Order, review, notification serializers
│       ├── views.py                 # Checkout, order management, seller shipping, reviews
│       ├── services.py              # Checkout logic, Stripe payment, wallet settlement
│       ├── signals.py               # Auto-notify buyer on ship, seller on delivery
│       ├── admin.py                 # ModelAdmin for order models
│       ├── urls.py                  # Mixed router + path URLs
│       └── tests.py
│
└── shopsmart/                       # Vue.js SPA
    ├── index.html
    ├── package.json
    ├── vite.config.js
    └── src/
        └── ...                      # Vue components, router, stores, services
```

---

## Prerequisites

- **Python 3.14+**
- **Node.js 18+**
- **Poetry** (Python package manager)

---

## Quick Start

### Backend

```bash
# Clone the repo
git clone <repo-url> ShopSmart
cd ShopSmart

# Install Poetry if not already installed
pip install poetry

# Configure virtualenv in project
poetry config virtualenvs.in-project true

# Install Python dependencies
poetry install

# Activate virtualenv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# Copy and configure environment variables
cp .env.example .env               # then edit .env

# Run migrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Start Django server
python manage.py runserver
```

### Frontend

```bash
cd shopsmart

# Install Node.js dependencies
npm install

# Development (with HMR)
npm run dev

# Production build → dist/
npm run build
```

Once built, Django serves the Vue.js SPA at `/` — no separate frontend server needed.

---

## How It Works

### Single Server Architecture

1. `npm run build` compiles Vue.js into `shopsmart/dist/`
2. Django's `TEMPLATES` setting points to `shopsmart/dist/index.html`
3. Django's `STATICFILES_DIRS` includes `shopsmart/dist/assets/`
4. All `/api/*` requests are handled by Django REST Framework
5. All other requests serve `index.html` (Vue Router handles client-side routing)
6. **One command** (`python manage.py runserver`) serves everything

### Authentication Flow

- JWT-based auth via `djangorestframework-simplejwt`
- Access token (2 hours) + Refresh token (30 days)
- New users are created **inactive** — a 4-digit OTP is emailed via SendGrid
- Account is activated only after OTP verification

### Checkout & Payment Flow

- Buyer adds items to cart → hits `/api/checkout/`
- Stripe processes the card payment
- On success: `Order` + per-seller `SubOrder` records are created
- Seller's wallet is credited (minus platform fee), buyer's wallet is debited
- Idempotency keys prevent duplicate charges on retries

### Seller Workflow

- Any user can upgrade to seller via `POST /api/me/become-seller/`
- Sellers manage their own products under `/api/seller/products/`
- Sellers mark sub-orders as shipped, buyers confirm delivery
- Django signals auto-notify the relevant party at each status change

---

## Environment Variables

Create a `.env` file in the project root:

```env
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True
BASE_URL=http://127.0.0.1:8000
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

SENDGRID_API_KEY=your-sendgrid-api-key
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

STRIPE_SECRET_KEY=your-stripe-secret-key
```

---

## API Endpoints

All routes are prefixed with `/api/`.

### Authentication (`/api/auth/`)

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `auth/register/` | POST | — | Register new user (sends OTP) |
| `auth/login/` | POST | — | Log in, receive JWT token pair |
| `auth/logout/` | POST | ✓ | Blacklist refresh token |
| `auth/token/refresh/` | POST | — | Refresh access token |
| `auth/verify-otp/` | POST | — | Activate account with OTP |
| `auth/resend-otp/` | POST | — | Re-send OTP to email |
| `auth/reset-password/` | POST | — | Reset password via OTP |

### User & Wallet (`/api/me/`, `/api/wallet/`)

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `me/` | GET / PATCH | ✓ | View or update own profile |
| `me/become-seller/` | POST | ✓ | Upgrade account to seller |
| `wallet/` | GET | ✓ | View wallet balance |
| `wallet/transactions/` | GET | ✓ | Paginated transaction history |
| `addresses/` | CRUD | ✓ | Manage delivery addresses |
| `bank-accounts/` | CRUD | ✓ | Manage bank accounts for withdrawals |
| `withdrawals/` | CRUD | ✓ | Request and track withdrawals |

### Catalog (`/api/products/`, `/api/categories/`, `/api/cart/`)

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `categories/` | GET | — | List all categories (with children) |
| `categories/<id>/products/` | GET | — | Products filtered by category |
| `analytics/category-click/` | POST | — | Log category click for analytics |
| `products/` | GET | — | Browse all active products (search, filter, order) |
| `products/<id>/` | GET | — | Product detail with images |
| `seller/products/` | CRUD | ✓ Seller | Manage own product listings |
| `cart/` | GET | ✓ | View cart with line totals |
| `cart/items/` | CRUD | ✓ | Add, update quantity, or remove cart items |

### Orders (`/api/orders/`, `/api/checkout/`)

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `checkout/` | POST | ✓ | Create order from cart, process Stripe payment |
| `orders/` | GET | ✓ | Buyer's order list |
| `orders/<id>/` | GET | ✓ | Order detail with sub-orders and items |
| `orders/<id>/cancel/` | POST | ✓ | Cancel a pending order |
| `seller/orders/` | GET | ✓ Seller | Incoming sub-orders for the seller |
| `seller/orders/<id>/ship/` | POST | ✓ Seller | Mark sub-order as shipped |
| `seller/orders/<id>/deliver/` | POST | ✓ Seller | Confirm delivery of sub-order |
| `reviews/` | CRUD | ✓ | Post and manage product reviews (1–5 stars) |
| `notifications/` | GET | ✓ | User notification feed |

---

## Data Models

### `account` app

| Model | Description |
|-------|-------------|
| `User` | Custom user (AbstractUser) — email as USERNAME_FIELD, `is_seller` flag |
| `OTP` | 4-digit email verification codes with expiry |
| `Address` | Delivery addresses (Punjab cities), one default per user |
| `Wallet` | One wallet per user — tracks cached balance |
| `WalletTransaction` | Credit/debit ledger (topup, sale proceeds, refund, withdrawal, etc.) |
| `BankAccount` | Encrypted external bank accounts for cash-out |
| `Withdrawal` | Withdrawal request lifecycle: pending → approved → settled |

### `catalog` app

| Model | Description |
|-------|-------------|
| `Category` | Self-referencing tree (parent/children), slug-based |
| `Product` | Listings with price, stock, SKU, condition, status; owned by a seller |
| `ProductImage` | Multiple images per product; first image auto-sets thumbnail |
| `Cart` | One cart per user |
| `CartItem` | Product + quantity + price snapshot at time of adding |

### `orders` app

| Model | Description |
|-------|-------------|
| `Order` | Parent order per checkout — buyer, total, shipping address, card snapshot |
| `SubOrder` | Per-seller slice of an order — tracks shipping and delivery independently |
| `OrderItem` | Line item snapshot (title, SKU, price, quantity, line total) |
| `Review` | One review per user per product, rating 1–5 |
| `Notification` | JSON-payload notification feed per user |
| `IdempotencyKey` | Prevents duplicate Stripe charges on retry |

---

## Custom Permissions

| Permission | Description |
|------------|-------------|
| `IsSeller` | View-level — only authenticated users with `is_seller=True` |
| `IsOwnerOrReadOnly` | Object-level — read-only for all, write only for the owning seller |

---

## Signals

| Signal | Trigger | Action |
|--------|---------|--------|
| `send_otp_on_register` | New `User` saved (inactive) | Generates OTP and sends verification email |
| `suborder_status_notification` | `SubOrder` status → `shipped` | Notifies buyer with tracking code |
| `suborder_status_notification` | `SubOrder` status → `delivered` | Notifies seller of confirmed delivery |

---

## Admin

The Django admin panel is available at `/admin/`.

| App | Registered Models |
|-----|-------------------|
| `account` | User, Address, Wallet, WalletTransaction, BankAccount, Withdrawal |
| `catalog` | Category, Product, ProductImage, Cart, CartItem |
| `orders` | Order, SubOrder, OrderItem, Review, Notification |

Log in with the superuser credentials created during setup.

---

## Running Tests

```bash
python manage.py test apps.account apps.catalog apps.orders
```
