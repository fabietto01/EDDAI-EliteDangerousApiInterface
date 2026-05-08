import axiox from 'axios';

axiox.defaults.xsrfCookieName = 'csrftoken';
axiox.defaults.xsrfHeaderName = 'X-CSRFToken';
axiox.defaults.headers.common['Accept'] = 'application/json';

export { axiox };