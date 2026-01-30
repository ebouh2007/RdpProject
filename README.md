# RdpProject

Local HTTPS API server for desktop workflows using C# and Kestrel.

## Prerequisites
- .NET 8 SDK
- Trusted dev certificate for HTTPS on localhost

```bash
dotnet dev-certs https --trust
```

## Run
```bash
dotnet run
```

The server listens on `https://localhost:5001`.

## Endpoints
- `GET /health`
  - Returns `{ "status": "ok" }`
- `POST /echo`
  - Body: `{ "message": "hello" }`
  - Returns the same payload

### Example
```bash
curl -k https://localhost:5001/health
curl -k https://localhost:5001/echo \
  -H "Content-Type: application/json" \
  -d '{"message":"hello"}'
```
