// Client HTTP centralizzato: sessione Django same-origin + CSRF via cookie/header.
const API_BASE_URL = '/api/v1/';
const CSRF_COOKIE_NAME = 'csrftoken';
const CSRF_HEADER_NAME = 'X-CSRFToken';
const SAFE_METHODS = new Set(['GET', 'HEAD', 'OPTIONS', 'TRACE']);

function getCookie(name) {
  const match = document.cookie
    .split('; ')
    .find((row) => row.startsWith(`${name}=`));
  return match ? decodeURIComponent(match.split('=')[1]) : null;
}

/**
 * Assicura che il cookie CSRF sia inizializzato lato browser.
 */
async function ensureCsrfCookie() {
  if (!getCookie(CSRF_COOKIE_NAME)) {
    await request('csrf/', { method: 'GET' });
  }
}

async function request(path, { method = 'GET', body, headers = {}, ...rest } = {}) {
  const finalHeaders = { Accept: 'application/json', ...headers };

  if (!SAFE_METHODS.has(method.toUpperCase())) {
    const token = getCookie(CSRF_COOKIE_NAME);
    if (token) {
      finalHeaders[CSRF_HEADER_NAME] = token;
    }
  }

  if (body !== undefined && !(body instanceof FormData)) {
    finalHeaders['Content-Type'] = 'application/json';
    body = JSON.stringify(body);
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    method,
    headers: finalHeaders,
    credentials: 'include',
    body,
    ...rest,
  });

  if (!response.ok) {
    const error = new Error(`Richiesta fallita: ${response.status}`);
    error.status = response.status;
    try {
      error.data = await response.json();
    } catch {
      error.data = null;
    }
    throw error;
  }

  if (response.status === 204) {
    return null;
  }
  return response.json();
}

export { request, ensureCsrfCookie, getCookie };
