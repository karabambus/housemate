# Security Headers Documentation

## Overview

HouseMate implements industry-standard security headers to protect against common web vulnerabilities. All responses from the application include comprehensive HTTP security headers.

## Headers Implemented

### 1. Content-Security-Policy (CSP)

**Purpose**: Prevent Cross-Site Scripting (XSS), clickjacking, and other code injection attacks.

**Implementation**:
```
default-src 'self'                                    # Only allow resources from same origin
script-src 'self' cdn.jsdelivr.net                    # Scripts from self or CDN
style-src 'self' 'unsafe-inline' cdn.jsdelivr.net     # Styles from self, inline, or CDN
img-src 'self' data: https:                           # Images from self, data URIs, or HTTPS
font-src 'self' cdn.jsdelivr.net                      # Fonts from self or CDN
connect-src 'self'                                    # AJAX/WebSocket to same origin only
frame-ancestors 'none'                                # Cannot be framed by other sites
base-uri 'self'                                       # Base URL must be from same origin
form-action 'self'                                    # Form submissions to same origin only
```

**Protection Against**:
- XSS attacks via script injection
- Malicious inline scripts
- Resource hijacking
- Data exfiltration

---

### 2. X-Content-Type-Options: nosniff

**Purpose**: Prevent MIME type sniffing attacks.

**How it Works**: Instructs browsers to follow the declared Content-Type and not guess based on content.

**Protection Against**:
- Drive-by downloads
- MIME type confusion attacks
- Execution of unexpected file types

---

### 3. X-Frame-Options: DENY

**Purpose**: Prevent clickjacking attacks.

**How it Works**: Prevents the application from being embedded in an iframe on other sites.

**Protection Against**:
- Clickjacking/UI redressing
- Session hijacking through frame overlays
- Malicious iframe embedding

---

### 4. X-XSS-Protection: 1; mode=block

**Purpose**: Enable XSS filter in older browsers (legacy support).

**How it Works**: Activates built-in XSS filters in legacy browsers and blocks the page if XSS is detected.

**Note**: Modern browsers rely on CSP; this is for backwards compatibility.

**Protection Against**:
- Basic XSS attacks (in older browsers)
- Reflected XSS

---

### 5. Referrer-Policy: strict-origin-when-cross-origin

**Purpose**: Control how much referrer information is shared.

**How it Works**:
- Same-origin requests: Send full URL
- Cross-origin requests: Send only origin (no path/query)

**Protection Against**:
- Information leakage about internal URLs
- Sensitive data in referrer headers

---

### 6. Permissions-Policy (formerly Feature-Policy)

**Purpose**: Disable potentially dangerous browser features.

**Disabled Features**:
- `geolocation()` - Location access
- `microphone()` - Microphone access
- `camera()` - Camera access
- `payment()` - Payment handler registration
- `usb()` - USB device access
- `magnetometer()` - Device motion sensors
- `gyroscope()` - Device orientation
- `accelerometer()` - Device acceleration

**Protection Against**:
- Unauthorized access to hardware features
- Privacy violations
- Device fingerprinting

---

## Configuration

All CSP directives are configurable in `config.py`:

```python
CSP_DIRECTIVES = {
    'default-src': ["'self'"],
    'script-src': ["'self'", 'cdn.jsdelivr.net'],
    # ... other directives
}
```

### Modifying CSP for Development

If you need to allow additional resources during development:

```python
# Temporarily add in development
if DEBUG:
    CSP_DIRECTIVES['script-src'].append('http://localhost:8080')
```

**⚠️ WARNING**: Only modify CSP in development. Production CSP should be strict.

---

## Testing Security Headers

### Using curl

```bash
curl -i http://localhost:5000/
```

Look for these headers in the response:
- `Content-Security-Policy`
- `X-Content-Type-Options`
- `X-Frame-Options`
- `X-XSS-Protection`
- `Referrer-Policy`
- `Permissions-Policy`

### Using Online Tools

- [Security Headers Scanner](https://securityheaders.com/)
- [Mozilla Observatory](https://observatory.mozilla.org/)

---

## CSP Violations

If users encounter CSP violations:

1. **Check Browser Console**: Developer tools show CSP violations
2. **Common Issues**:
   - Inline scripts not in CSP: Move to separate `.js` files
   - External resources from non-whitelisted domains: Add domain to CSP
   - Unsafe JavaScript operations: Use safer APIs

---

## Production Considerations

### Before Deployment

1. **Test Thoroughly**: Ensure all resources load correctly
2. **Monitor Reports**: Use CSP report-uri in production
3. **Update Whitelist**: Add any new external resources to CSP

### Adding Report-URI (Optional)

For monitoring CSP violations in production:

```python
csp += "report-uri /security/csp-report; "
```

Then handle the report endpoint:

```python
@app.route('/security/csp-report', methods=['POST'])
def csp_report():
    # Log CSP violation
    report = request.get_json()
    # Send alert if needed
    return '', 204
```

---

## Compliance Standards

These headers align with:
- **OWASP Top 10** (A06:2021 - Vulnerable and Outdated Components)
- **NIST Cybersecurity Framework**
- **CWE-16** (Configuration)
- **CAPEC-209** (XSS through DOM Manipulation)

---

## Related Security Measures

This application also implements:
- ✅ CSRF Token Protection (Flask-WTF)
- ✅ Session Security
- ✅ Input Validation
- ✅ SQL Injection Prevention (SQLAlchemy ORM)
- ✅ Secure Password Hashing (bcrypt)

---

## References

- [MDN: Content-Security-Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy)
- [OWASP: Content Security Policy](https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html)
- [Web Fundamentals: Content Security Policy](https://developers.google.com/web/fundamentals/security/csp)
- [Mozilla: Web Security Guidelines](https://infosec.mozilla.org/guidelines/web_security)

---

**Last Updated**: 2026-01-16
**Status**: ✅ Implemented
