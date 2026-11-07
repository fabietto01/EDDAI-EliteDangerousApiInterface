# ed_frontend

This template should help get you started developing with Vue 3 in Vite.

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Customize configuration

See [Vite Configuration Reference](https://vite.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
# EDDAI Frontend

Standalone Vue application, built with Node 24 and served by non-root Nginx.
It does not read Django templates, its manifest or any shared static volume.
Bootstrap and Popper are bundled through npm, not loaded from a CDN.

## Development

Run Django separately on `127.0.0.1:8080`, then run in this directory:

```sh
npm ci
npm run dev
```

Open `http://127.0.0.1:5173`. Vite proxies `/api`, `/users`, `/admin`, `/static`
and `/healthz` to Django, preserving the browser origin for sessions and CSRF.
For a backend on port 8000, set `DJANGO_DEV_UPSTREAM` before starting Vite:

```powershell
$env:DJANGO_DEV_UPSTREAM = 'http://127.0.0.1:8000'
npm run dev
```

```sh
DJANGO_DEV_UPSTREAM=http://127.0.0.1:8000 npm run dev
```

Use the development Django settings over HTTP; production settings require
secure cookies and the HTTPS hostname configured in Compose.

## Build and Tests

```sh
npm run test:unit
npm run build
```

The build writes only to `dist/`. `npm run test:watch` runs interactive tests.
`src/common/http.js` exports `apiFetch`, which sends same-origin cookies and
initializes CSRF through `/api/v1/csrf/` before unsafe requests when needed.
It returns the Fetch response so callers can handle status codes and JSON.

## Container

From the repository root:

```sh
docker build -t eddai-frontend:local eddai_EliteDangerousApiInterface/ed_frontend
docker run --rm --read-only --cap-drop ALL --security-opt no-new-privileges \
	--tmpfs /tmp:rw,noexec,nosuid,size=32m,mode=1777 \
	-p 127.0.0.1:8081:8080 eddai-frontend:local
```

The standalone container serves the UI at `http://127.0.0.1:8081`, but does not
proxy API or login requests. In production, Traefik routes those paths directly
to the backend on the same hostname. `/healthz` checks the frontend server.
Hashed assets are cacheable; HTML is revalidated and missing files return 404.
See the root README for deployment, image versions and independent scaling.
