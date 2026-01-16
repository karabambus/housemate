# CORS Configuration Documentation

## Overview

CORS (Cross-Origin Resource Sharing) allows controlled access to resources from different domains. HouseMate implements a restrictive, secure-by-default CORS configuration to prevent unauthorized cross-domain access while allowing legitimate requests.

## What is CORS?

CORS is a browser security feature that prevents malicious websites from accessing data from your application without permission. By default, browsers block requests from one domain accessing resources on another domain.

### Same-Origin vs Cross-Origin

**Same-Origin**: `http://localhost:5000`
- `http://localhost:5000/bills` ✅ Same origin
- `http://localhost:5000/login` ✅ Same origin

**Cross-Origin**: `http://localhost:5000`
- `http://example.com/data` ❌ Different domain
- `http://localhost:3000/data` ❌ Different port
- `https://localhost:5000/data` ❌ Different protocol

---

## Current CORS Configuration

### Allowed Origins

```python
CORS_CONFIG = {
    'origins': [
        'http://localhost:5000',      # Main application
        'http://127.0.0.1:5000',      # Localhost alternative
        'http://localhost:3000',      # Frontend development (if separate)
    ],
    'methods': ['GET', 'POST', 'OPTIONS'],
    'allow_headers': ['Content-Type', 'Authorization', 'X-CSRF-Token'],
    'supports_credentials': True,
    'max_age': 3600,                  # 1 hour
    'send_wildcard': False,           # Never use '*'
}
```

### Configuration Explained

| Setting | Value | Purpose |
|---------|-------|---------|
| `origins` | Specific domains | Only these domains can make cross-origin requests |
| `methods` | GET, POST, OPTIONS | Only these HTTP methods allowed |
| `allow_headers` | Content-Type, etc. | Only these headers can be sent |
| `supports_credentials` | True | Allow cookies/auth headers in requests |
| `max_age` | 3600 | Cache preflight responses for 1 hour |
| `send_wildcard` | False | **NEVER use '*' for origins** |

---

## Security Principles

### ❌ NEVER DO THIS

```python
# INSECURE: Allows ANY domain to access your API
CORS(app, resources={r"/*": {"origins": "*"}})
```

**Why it's dangerous**:
- Malicious websites can access user data
- No authentication validation
- Exposes sensitive information to attackers
- Violates CORS security model

### ✅ DO THIS INSTEAD

```python
# SECURE: Only specific, trusted domains allowed
CORS(app, resources={
    r"/*": {
        "origins": [
            "https://yourdomain.com",
            "https://app.yourdomain.com"
        ]
    }
})
```

---

## CORS in Action: Preflight Requests

When a browser makes a cross-origin request with certain conditions, it first sends a preflight request:

### Step 1: Browser sends OPTIONS preflight

```
OPTIONS /bills HTTP/1.1
Host: housemate.app
Origin: http://localhost:3000
Access-Control-Request-Method: POST
Access-Control-Request-Headers: Content-Type
```

### Step 2: Server responds with permissions

```
HTTP/1.1 200 OK
Access-Control-Allow-Origin: http://localhost:3000
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization, X-CSRF-Token
Access-Control-Max-Age: 3600
```

### Step 3: Browser sends actual request

```
POST /bills HTTP/1.1
Host: housemate.app
Origin: http://localhost:3000
Content-Type: application/json
[Request body...]
```

### Step 4: Server processes and responds

```
HTTP/1.1 200 OK
Access-Control-Allow-Origin: http://localhost:3000
Content-Type: application/json
[Response body...]
```

---

## Configuring CORS for Different Environments

### Development

For local development with separate frontend:

```python
if DEBUG:
    CORS_CONFIG = {
        'origins': [
            'http://localhost:3000',    # React dev server
            'http://localhost:5000',    # Flask dev server
            'http://127.0.0.1:5000',
        ],
        'methods': ['GET', 'POST', 'DELETE', 'PUT', 'OPTIONS'],
    }
```

### Staging

```python
elif ENVIRONMENT == 'staging':
    CORS_CONFIG = {
        'origins': [
            'https://staging.housemate.app',
            'https://staging-ui.housemate.app',
        ],
        'methods': ['GET', 'POST', 'DELETE', 'PUT', 'OPTIONS'],
    }
```

### Production

```python
elif ENVIRONMENT == 'production':
    CORS_CONFIG = {
        'origins': [
            'https://housemate.app',
            'https://www.housemate.app',
        ],
        'methods': ['GET', 'POST', 'DELETE', 'PUT', 'OPTIONS'],
    }
```

---

## Allowed HTTP Methods

Current configuration allows:
- **GET**: Retrieve resources
- **POST**: Create/submit data
- **OPTIONS**: Preflight checks

### Adding More Methods

If you need other methods (PUT, DELETE, PATCH):

```python
'methods': ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS']
```

⚠️ **Security Note**: Only enable methods you actually need.

---

## Headers Configuration

### Currently Allowed

- **Content-Type**: Data format (JSON, form data, etc.)
- **Authorization**: Authentication tokens/credentials
- **X-CSRF-Token**: CSRF protection token

### Adding Custom Headers

If your frontend sends custom headers:

```python
'allow_headers': [
    'Content-Type',
    'Authorization',
    'X-CSRF-Token',
    'X-Custom-Header',  # Add your header here
]
```

---

## Credentials (Cookies & Auth)

### With Credentials Support

```python
'supports_credentials': True
```

**What this allows**:
- Sending cookies with cross-origin requests
- Including Authorization headers
- Preserving user sessions across origins

**Required on client side**:

```javascript
// Must include credentials in fetch
fetch('http://localhost:5000/api/bills', {
    method: 'GET',
    credentials: 'include',  // Send cookies
    headers: {
        'Authorization': 'Bearer token...'
    }
})
```

### Without Credentials

```python
'supports_credentials': False
```

**Use when**:
- No authentication needed
- Public data only
- More restrictive security

---

## Testing CORS Configuration

### Using curl

```bash
# Test simple GET request
curl -i http://localhost:5000/bills

# Test preflight request
curl -i -X OPTIONS http://localhost:5000/bills \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type"
```

### Using Browser DevTools

1. Open **Console** in Developer Tools
2. Run JavaScript:

```javascript
fetch('http://localhost:5000/bills', {
    credentials: 'include'
})
.then(r => r.json())
.then(data => console.log(data))
.catch(err => console.error('CORS Error:', err))
```

### Check Response Headers

```bash
curl -i http://localhost:5000/ | grep -i "access-control"
```

Look for headers:
- `Access-Control-Allow-Origin`
- `Access-Control-Allow-Methods`
- `Access-Control-Allow-Headers`
- `Access-Control-Max-Age`

---

## Common CORS Errors and Solutions

### Error: "No 'Access-Control-Allow-Origin' header"

**Cause**: Domain not in allowed origins list

**Solution**:
```python
CORS_CONFIG['origins'].append('https://yourdomain.com')
```

---

### Error: "Access-Control-Allow-Methods does not allow method POST"

**Cause**: POST not enabled for this endpoint

**Solution**:
```python
'methods': ['GET', 'POST', 'OPTIONS']
```

---

### Error: "The value of 'Access-Control-Allow-Credentials' is ''"

**Cause**: Credentials enabled but header not set correctly

**Solution**: Ensure Flask-CORS is properly initialized with `supports_credentials: True`

---

## Monitoring CORS Requests

### Log CORS Activity

```python
@app.before_request
def log_cors_request():
    origin = request.headers.get('Origin')
    if origin:
        print(f"Cross-origin request from: {origin}")
```

### Check Request Headers

```python
@app.route('/debug/cors')
def debug_cors():
    return {
        'origin': request.headers.get('Origin'),
        'method': request.method,
        'headers': dict(request.headers),
    }
```

---

## Production Best Practices

1. **Use HTTPS only** in production
   ```python
   'origins': ['https://yourdomain.com']  # Not http://
   ```

2. **Use specific domain names**, not wildcards
   ```python
   'origins': ['https://api.yourdomain.com']  # Good
   # NOT 'https://*.yourdomain.com'
   ```

3. **Minimize allowed methods**
   ```python
   'methods': ['GET', 'POST', 'OPTIONS']  # Only what's needed
   ```

4. **Validate Origin header** in sensitive endpoints
   ```python
   @app.route('/sensitive')
   def sensitive_endpoint():
       if request.headers.get('Origin') not in config.CORS_CONFIG['origins']:
           return 'Unauthorized', 403
       # Process request
   ```

5. **Monitor for suspicious origins** in logs
   ```python
   origin = request.headers.get('Origin')
   if origin and origin not in allowed_origins:
       log_security_event(f"Suspicious origin: {origin}")
   ```

---

## Relationship with Other Security Headers

### CORS + Content-Security-Policy

- **CSP** `connect-src`: Controls what the page can connect to
- **CORS** `Access-Control-Allow-Origin`: Allows browser to accept response

Both should be aligned:

```python
CSP_DIRECTIVES = {
    'connect-src': ["'self'", 'http://localhost:3000'],  # Allowed connections
}

CORS_CONFIG = {
    'origins': [
        'http://localhost:5000',
        'http://localhost:3000',  # Match CSP connect-src
    ]
}
```

### CORS + CSRF Protection

- **CORS**: Controls which domains can send requests
- **CSRF Token**: Validates the request came from your form

Both work together for complete protection.

---

## References

- [MDN: CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- [Flask-CORS Documentation](https://flask-cors.readthedocs.io/)
- [OWASP: CORS](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Origin_Resource_Sharing_CheatSheet.html)
- [Mozilla: Web Security Guidelines](https://infosec.mozilla.org/guidelines/web_security)

---

**Last Updated**: 2026-01-16
**Status**: ✅ Implemented
**Environment**: Development
