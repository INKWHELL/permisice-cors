# 5.3 Permissive CORS Configuration — Evidence Project

This project reproduces the Build, Break, Fix and Evaluation steps in 5.3
end-to-end, so you can capture real screenshots instead of describing the
expected output.

**Note on ports:** your current draft's Fix section allow-lists
`http://localhost:5500`, but that is the same port used as the *attacker's*
origin in your Break section. In this project the attacker runs on `5500`
(unchanged, so it matches your existing Break text) and the trusted frontend
runs on `5501`. Update the Fix section's `CORS_ALLOWED_ORIGINS` value to
`5501` to remove the contradiction, or swap the ports below to match
whatever you'd rather keep in the write-up.

## Project layout

```
cors-demo/
├── manage.py
├── requirements.txt
├── config/          Django project settings + urls
├── api/             the /api/login/ and /api/profile/ endpoints
├── frontend/         legit.html — the trusted frontend (port 5501)
└── attacker/         attacker.html — the malicious page (port 5500)
```

## One-time setup

```bash
cd cors-demo
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo_user   # creates joe / testpass123
```

You'll run **three servers** at once, each in its own terminal:

```bash
# Terminal 1 — the Django API
python manage.py runserver 7999

# Terminal 2 — the trusted frontend
cd frontend && python -m http.server 5501

# Terminal 3 — the attacker's page
cd attacker && python -m http.server 5500
```

Use Chrome for all of this — it treats `http://localhost` as a secure
context, so the `Secure` session cookie still gets set without needing
HTTPS. Other browsers may not.

---

## Capturing the Build / Break evidence (vulnerable state)

`config/settings.py` is vulnerable by default (`CORS_ALLOW_ALL_ORIGINS = True`).

1. **Get a victim session.** Visit `http://localhost:5501/legit.html`
   (the trusted frontend) and click **Log in as joe**. Open DevTools →
   Application → Cookies → `http://localhost:7999` and screenshot the
   `sessionid` cookie now present — this is your "before" evidence that the
   cookie belongs to the API's domain, tagged `SameSite=None; Secure`.

2. **Open the attacker's page** at `http://localhost:5500/attacker.html`,
   with DevTools open on **Console** and **Network**.
   - Screenshot the **Console**, showing the stolen JSON logged via
     `console.log` and rendered on the page.
   - Screenshot the **Network** tab, expanding the `/api/profile/` request:
     - *Request Headers* → `Origin: http://localhost:5500`, `Cookie: sessionid=...`
     - *Response Headers* → `access-control-allow-origin: http://localhost:5500`,
       `access-control-allow-credentials: true`

These three screenshots are the evidence for Build/Break.

---

## Capturing the Fix / Evaluation evidence (fixed state)

3. **Apply the fix.** In `config/settings.py`, comment out the two
   `CORS_ALLOW_ALL_ORIGINS` / `CORS_ALLOW_CREDENTIALS` lines and uncomment
   the `CORS_ALLOWED_ORIGINS` block underneath it. Save, then stop and
   restart the Django server (Ctrl+C, then `python manage.py runserver 7999`
   again — Django does not hot-reload settings changes reliably).

4. **Reload the attacker's page** (`http://localhost:5500/attacker.html`,
   same tab, no other changes).
   - Screenshot the **Console**, now showing a CORS error instead of the
     stolen data (something like *"has been blocked by CORS policy..."*).
   - Screenshot the **Network** tab for the same request: still `200 OK`
     from the server, but with **no** `access-control-allow-origin` header
     in the response. This is the evidence for the point made in your
     Evaluation section — the server still processes and returns the data;
     the browser is what withholds it from the script.

5. **Confirm the legitimate frontend still works.** Go back to
   `http://localhost:5501/legit.html` and click **Get profile**.
   Screenshot the profile data rendering normally — this proves the fix
   didn't break the application's own cross-origin functionality.

That's five screenshots covering every claim made in Build, Break, Fix and
Evaluation, with nothing invented.

## Resetting between attempts

```bash
rm db.sqlite3
python manage.py migrate
python manage.py seed_demo_user
```
