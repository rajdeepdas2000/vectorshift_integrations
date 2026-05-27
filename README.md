# HubSpot CRM Integration Platform

A lightweight integration platform built with **FastAPI**, **React**, and **Redis** that supports OAuth-based third-party integrations and data loading workflows.

Currently supported integrations:

- Airtable
- Notion
- HubSpot

The application allows users to:
- Authenticate with external platforms using OAuth 2.0
- Securely retrieve and temporarily store credentials
- Fetch platform-specific data
- Normalize external resources into common `IntegrationItem` objects

---

# Tech Stack

## Backend
- Python
- FastAPI
- Redis
- HTTPX
- Requests

## Frontend
- React
- Material UI
- Axios

---

# Features

## OAuth 2.0 Integration Flow
Supports OAuth-based authentication for:
- HubSpot
- Airtable
- Notion

The backend:
- Generates authorization URLs
- Handles OAuth callbacks
- Exchanges authorization codes for access tokens
- Stores credentials temporarily in Redis

---

## HubSpot Integration

Implemented HubSpot integration using HubSpot CRM APIs.

### Supported Flow
- Connect HubSpot account
- Authenticate using OAuth 2.0
- Retrieve access token
- Load CRM contact data

### HubSpot Data Loaded
Currently fetches:
- CRM Contacts

Each contact is mapped into a normalized `IntegrationItem` structure.

# Environment Setup

Create a `.env` file inside the `backend` directory:

```env
HUBSPOT_CLIENT_ID=your_client_id
HUBSPOT_CLIENT_SECRET=your_client_secret
```

Refer to `backend/.env.example` for the format.

---

# Running the Platform

## 1. Start Redis

Make sure Redis is running locally on port `6379`.

Example:

```bash
redis-server
```

---

## 2. Run Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app
```

Backend runs on:

```text
http://localhost:8000
```

---

## 3. Run Frontend

```bash
cd frontend
npm install
npm start
```

Frontend runs on:

```text
http://localhost:3000
```

---

# HubSpot App Configuration

Create a HubSpot app and configure:

## Redirect URL

```text
http://localhost:8000/integrations/hubspot/oauth2callback
```

## Required Scopes

```text
crm.objects.contacts.read
crm.objects.companies.read
crm.objects.deals.read
```

---

# API Flow Overview

## OAuth Authorization

```text
Frontend
   ↓
Backend generates OAuth URL
   ↓
User authenticates with HubSpot
   ↓
HubSpot redirects to callback endpoint
   ↓
Backend exchanges authorization code for access token
   ↓
Credentials stored temporarily in Redis
```

---

## Data Loading

```text
Frontend requests data load
   ↓
Backend uses stored access token
   ↓
HubSpot CRM APIs queried
   ↓
Results transformed into IntegrationItem objects
   ↓
Data returned to frontend
```

---

# Notes

- Redis is used for temporary credential and OAuth state storage.
- HubSpot credentials are loaded securely using environment variables.


- ‼️‼️‼️Some random ling ling approached me with this but never acknowledged my submission, if you ever encounter them, avoid them like the plague.
