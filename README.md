# RdpProject

Local HTTPS API server for development/testing.

## Setup
1. Generate a self-signed certificate (one-time):

```bash
openssl req -x509 -newkey rsa:2048 -nodes -keyout key.pem -out cert.pem -days 365 -subj "/CN=localhost"
```

2. Start the server:

```bash
python3 server.py
```

The server listens on `https://0.0.0.0:8443`.

## Endpoints
- `GET /health` → `{ "status": "ok" }`
- `POST /echo` with JSON body → `{ "received": <payload> }`

Example:

```bash
curl -k https://localhost:8443/health
curl -k https://localhost:8443/echo -H "Content-Type: application/json" -d '{"hello": "world"}'
```
