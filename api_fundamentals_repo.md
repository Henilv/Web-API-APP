---
# tests.yaml
version: "1.0"
service: "api-example"
base_url: "https://api.example.com"

tests:
  - id: TC-001
    name: "Create user - happy path"
    description: "Create a new user with valid payload; expect 201 Created and Location header."
    method: POST
    path: /api/v1/users
    headers:
      Content-Type: application/json
      Accept: application/json
      Authorization: "ApiKey {{API_KEY}}"
    body_ref: payloads.create_user_valid
    expected_status: 201
    expected_headers:
      - "Location: /api/v1/users/"
      - "Content-Type: application/json; charset=utf-8"
    notes: "Server should return Location header pointing to new resource and a JSON body with 'id'."

  - id: TC-002
    name: "Create user - missing required field"
    description: "Missing 'email' should produce 400 and validation errors in body."
    method: POST
    path: /api/v1/users
    headers:
      Content-Type: application/json
      Accept: application/json
      Authorization: "ApiKey {{API_KEY}}"
    body_ref: payloads.create_user_missing_email
    expected_status: 400
    expected_headers:
      - "Content-Type: application/problem+json"
    notes: "Follow RFC 7807 style problem details."

  - id: TC-003
    name: "Create user - SQLi attempt"
    description: "Payload contains SQL meta-characters to verify server input sanitization."
    method: POST
    path: /api/v1/users
    headers:
      Content-Type: application/json
      Accept: application/json
      Authorization: "ApiKey {{API_KEY}}"
    body_ref: payloads.create_user_sqli
    expected_status: 422
    expected_headers:
      - "Content-Type: application/json"
    notes: "Server should treat payload as data and either validate/reject; must not return DB errors."

# ...additional tests TC-004 to TC-030 included as per previous example...

---
# payloads.yaml
create_user_valid:
  name: "Alice Example"
  email: "alice@example.com"
  password: "Str0ngP@ssw0rd!"
  meta:
    signup_source: "web"

create_user_missing_email:
  name: "Bob"
  password: "abc123"
  meta:
    signup_source: "web"

create_user_sqli:
  name: "Mallory"
  email: "mallory@example.com'); DROP TABLE users; --"
  password: "irrelevant"

login_valid:
  username: "alice@example.com"
  password: "Str0ngP@ssw0rd!"

update_item_valid:
  title: "Updated title"
  description: "Corrected description"
  price: 19.95
  tags:
    - "tools"
    - "dev"

patch_invalid_field:
  unknown_field: "some-data"

large_payload_10mb: |
  # generate JSON array with repeated pattern until ~10MB; for test harness, generate programmatically.

binary_disguised_exe:
  filename: "avatar.png"
  content_description: "binary stream with exe header"

trailing_commas: |
  { "a": 1, "b": 2, }

graphql_introspection:
  query: "{ __schema { types { name } } }"

ssrf_internal_metadata:
  url: "http://169.254.169.254/latest/meta-data/iam/security-credentials/"

unicode_homoglyphs:
  username: "аlіce"   # uses Cyrillic a, Cyrillic i (homoglyph attack)

# generators for large values
very_long_value:
  pattern: "A"
  repeat: 32768

---
# configs.yaml
nginx_proxy_tls_rate_limit:
  description: "Nginx snippet to enforce TLS, HSTS, basic rate-limiting and header hardening."
  snippet: |
    server {
        listen 80;
        server_name api.example.com;
        return 308 https://$host$request_uri;
    }

    server {
        listen 443 ssl;
        server_name api.example.com;

        ssl_certificate /etc/ssl/certs/api.example.com.crt;
        ssl_certificate_key /etc/ssl/private/api.example.com.key;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_prefer_server_ciphers on;

        add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
        add_header X-Frame-Options DENY;
        add_header X-Content-Type-Options nosniff;
        add_header Referrer-Policy "no-referrer";

        # rate limiting
        limit_req_zone $binary_remote_addr zone=api_rl:10m rate=10r/s;
        limit_req zone=api_rl burst=20 nodelay;

        location / {
            proxy_pass http://upstream_api;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }

openapi_minimal:
  description: "Minimal OpenAPI fragment with security schemes and example endpoint."
  snippet: |
    openapi: 3.0.3
    info:
      title: API Example
      version: "1.0.0"
    servers:
      - url: https://api.example.com
    components:
      securitySchemes:
        ApiKeyAuth:
          type: apiKey
          in: header
          name: X-API-Key
        BearerAuth:
          type: http
          scheme: bearer
          bearerFormat: JWT
    paths:
      /api/v1/users:
        post:
          summary: Create user
          requestBody:
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/UserCreate'
          responses:
            '201':
              description: Created

cors_config:
  allowedOrigins:
    - "https://app.example.com"
  allowedMethods:
    - GET
    - POST
    - PUT
    - PATCH
    - DELETE
  allowedHeaders:
    - Content-Type
    - Authorization
  allowCredentials: true

