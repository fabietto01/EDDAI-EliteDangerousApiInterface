# Report architettura Vue.js e Django

**Data fotografia:** 24 settembre 2026  
**Ambito:** repository EDDAI-EliteDangerousApiInterface

## Sintesi esecutiva

L'applicazione è oggi una struttura ibrida:

- Django è il punto di ingresso HTTP, serve il template HTML iniziale, espone le API REST, gestisce autenticazione, dati e logica server-side.
- Vue 3 è una SPA montata nell'elemento HTML `#app`. Gestisce il rendering dell'interfaccia, il routing client-side e le interazioni locali nel browser.
- Vite gestisce sviluppo e build. In sviluppo Django inserisce gli script dell'HMR server Vite; in produzione legge il manifest Vite e inserisce gli asset compilati.
- Le API REST sono esposte sotto `/api/v1/` e documentate tramite Swagger/ReDoc. Il frontend contiene un modulo di endpoint (`src/common/andpoints.js`), ma al momento non risultano chiamate `fetch`, Axios o XMLHttpRequest nei componenti Vue.

Quindi l'integrazione Django/Vue per il caricamento dell'interfaccia è funzionante e già predisposta per una SPA, mentre l'integrazione dati è ancora incompleta: oggi Vue non consuma effettivamente il backend API.

## 1. Come viene caricato e renderizzato Vue

Il percorso di caricamento è questo:

1. Una richiesta per la pagina web arriva a Django.
2. La route generica `re_path(r'^.*$', IndexTemplateView.as_view())` restituisce `templates/index.html`.
3. Il template estende `templates/base.html`, crea `<div id="app"></div>` e invoca il custom template tag `{% render_vite_assets %}`.
4. Il tag `render_vite_assets` sceglie gli script in base a `settings.DEBUG`:
   - in sviluppo: `http://127.0.0.1:5173/@vite/client` e `http://127.0.0.1:5173/src/main.js`;
   - in produzione: legge `static-server/vuejs/.vite/manifest.json` e genera i riferimenti agli asset compilati.
5. `src/main.js` importa il CSS globale, crea l'app Vue con `createApp(App)`, installa il router e monta l'app su `#app`.
6. `App.vue` renderizza `NavBar` e `<RouterView />`; il router seleziona il componente della pagina corrente.

### Componenti e viste attuali

- `App.vue`: shell principale dell'applicazione.
- `NavBar.vue`: barra di navigazione; `navItems` è al momento vuoto.
- `HomeView.vue`: pagina attualmente implementata, con contenuto informativo EDDAI e animazione del testo basata su `scroll`.
- `ScrollTextAnimation.vue`: caricamento lazy tramite `() => import(...)`.
- `SystemView.vue`: esiste ma non è registrata nelle route attuali e non contiene implementazione significativa.

Il rendering è principalmente client-side: Django fornisce il documento iniziale e Vue costruisce il contenuto di `#app` nel browser. Non risultano uso di SSR o rendering Vue lato server.

## 2. Struttura e integrazione Django/Vue

### Backend Django

Django svolge questi compiti:

- routing HTTP principale;
- rendering del guscio HTML tramite `IndexTemplateView`;
- esposizione delle API REST con Django REST Framework;
- serializzazione, validazione, autenticazione/autorizzazione, filtri e paginazione;
- accesso al database PostgreSQL/PostGIS e gestione dei modelli delle app di dominio;
- documentazione OpenAPI tramite `drf-spectacular`;
- processamento asincrono e sincronizzazione dati tramite Celery/EDDN, indipendentemente dal rendering Vue.

### Frontend Vue

Vue svolge questi compiti:

- rendering della UI nel browser;
- composizione di componenti e viste `.vue`;
- routing client-side con `vue-router`;
- gestione dello stato locale dei componenti;
- animazioni e comportamento interattivo della pagina.

Il frontend dipende direttamente da Vue 3 e Vue Router 4. Vite e il plugin Vue costituiscono la toolchain di sviluppo e build. Bootstrap 5 è caricato da CDN nel template HTML e fornisce parte dello stile/layout.

## 3. Comunicazione tra frontend e backend

### API disponibili

Il progetto espone due configurazioni di URL API:

- `/api/v1/`: namespace principale usato da `ed_core.api.urls`, che include le API di body, station, system, economy, mining, material, exploration e BGS;
- `/v1/`: namespace definito da `core.urls`, con un'ulteriore inclusione di `core.api.urls`.

Sono inoltre disponibili:

- `/api/v1/auth/` per le API di autenticazione DRF basate su sessione;
- `/api/schema/` per lo schema OpenAPI;
- `/api/schema/swagger-ui/` per Swagger UI;
- `/api/schema/redoc/` per ReDoc.

Le impostazioni DRF definiscono session authentication e token authentication, permessi predefiniti `IsAuthenticatedOrReadOnly`, paginazione a 500 elementi e filtri Django. In produzione il renderer REST è limitato a JSON.

### Stato effettivo della comunicazione Vue -> Django

Nel codice frontend:

- `src/common/andpoints.js` definisce `baseEndpoint = '/api/v1/'` e gli endpoint `systems` (`getAll`, `getById`);
- non sono presenti chiamate `fetch`, Axios, XMLHttpRequest o un client HTTP equivalente nei sorgenti Vue analizzati;
- `HomeView.vue` contiene solo un link browser verso Swagger (`/api/schema/swagger-ui/`), non una richiesta API per caricare dati;
- non esiste ancora un livello dedicato per gestione loading/error, parsing delle risposte, cache, store globale o refresh dei dati.

Il flusso dati previsto è:

```text
Vue -> richiesta HTTP /api/v1/... -> Django REST Framework
Vue <- risposta JSON serializzata    <- Django/DB
```

Ma il flusso non è ancora attivato dalle viste Vue attuali. Le risposte API sono comunque utilizzabili da client esterni e possono essere esplorate tramite Swagger.

## 4. Gestione di dati, richieste e risposte

Nel backend, DRF applica il contratto API: URL versionati, serializer, filtri, paginazione, autenticazione e permessi. Django legge i dati dal database PostGIS e li restituisce in JSON; le operazioni di acquisizione/sincronizzazione dati più pesanti sono demandate ai processi Celery e al servizio EDDN.

Nel frontend attuale i dati sono quasi esclusivamente statici nel template dei componenti. `HomeView` mantiene stato locale per posizione dello scroll, opacità e trasformazione del testo. Non sono presenti store, modelli client-side o trasformazioni di payload API.

Non risultano quindi implementati nel frontend: stati `loading`, `success`, `empty` ed `error`, retry/abort delle richieste, persistenza del token, cache dei dati o trattamento comune degli errori HTTP.

## 5. Sviluppo (dev)

Il frontend si avvia dalla directory `eddai_EliteDangerousApiInterface/ed_frontend` con:

```sh
npm install
npm run dev
```

Vite ascolta su `127.0.0.1:5173`, con polling del filesystem abilitato. Con `DEBUG=True`, il template Django carica direttamente il client HMR e `src/main.js` dal server Vite. Django continua a servire la pagina HTML iniziale e le API, tipicamente tramite `python manage.py runserver` sulla porta `8000`.

In sviluppo il browser carica quindi:

```text
Browser -> Django:8000 -> index.html e API
Browser -> Vite:5173   -> main.js, HMR e moduli Vue
```

Il README raccomanda Dev Containers per PostgreSQL/PostGIS, RabbitMQ, Redis e dipendenze Python. In alternativa, il backend può essere avviato manualmente e i servizi infrastrutturali con Docker.

## 6. Produzione

La build Vue si esegue con:

```sh
npm run build
```

Vite genera il manifest e gli asset in `../static-server/vuejs/`. La configurazione usa come base `/static-server/vuejs/`; il template Django pubblica però gli asset attraverso `STATIC_URL = '/static/'`, quindi il percorso pubblico finale degli asset è `/static/vuejs/...` e viene risolto dal mapping statico di Nginx.

In produzione il compose avvia Django con Daphne/ASGI sulla porta interna `8080`, Nginx sulla porta `80` davanti a Django, worker Celery, Celery Beat ed EDDN. Nginx inoltra le richieste applicative a `django:8080`, serve `/static/` da `/app/static-server/` e `/media/` da `/app/media-server/`. Il dominio pubblico è terminato da Traefik davanti al container Nginx, secondo le label presenti in `docker-compose.yml`.

### Dipendenza operativa importante

Il `.dockerignore` esclude `ed_frontend/` e `static-server/`. Inoltre il Dockerfile backend non esegue `npm install` né `npm run build`. La pubblicazione degli asset Vue in produzione dipende quindi da una build frontend eseguita separatamente e dalla presenza/condivisione di `static-server/vuejs` (nel compose è montata dal filesystem host).

Se manifest o asset non sono presenti, il template Django in produzione solleva un'eccezione durante `render_vite_assets` e l'interfaccia non viene caricata. Questo deve essere garantito esplicitamente dalla pipeline CI/CD oppure risolto con una build multi-stage che compili Vue prima dell'immagine runtime.

## 7. Confini della logica applicativa

### Django/backend

Regole di dominio e persistenza; accesso e sincronizzazione dati Elite Dangerous; autenticazione e autorizzazione; API, serializzazione e validazione; paginazione e filtri; task asincroni e integrazioni EDDN/CAPI; documentazione OpenAPI.

### Vue/frontend

Struttura e rendering della schermata; navigazione client-side; stato locale e animazioni; futura orchestrazione delle richieste API.

La logica di dominio è quindi concentrata nel backend; il frontend attuale è soprattutto una shell/presentazione e non contiene ancora una vera esperienza di consultazione dati via API.

## 8. Punti di integrazione, dipendenze e criticità

### Punti di integrazione

- template Django e custom tag `render_vite_assets`;
- directory condivisa `static-server` tra Django/Nginx e host/container;
- API REST versionate e schema OpenAPI;
- URL relativi (`/api/v1/`) che permettono di evitare una configurazione CORS quando frontend e backend sono pubblicati sullo stesso dominio;
- session/token authentication già configurate in DRF.

### Criticità e rischi

1. **Frontend API non ancora collegato:** gli endpoint dichiarati in `andpoints.js` non sono usati; la UI non rappresenta dati backend.
2. **Pipeline asset implicita:** Docker esclude i sorgenti e gli asset frontend; il deploy può rompersi se la build Vue non viene eseguita prima della pubblicazione.
3. **Incoerenza/duplicazione dei namespace API:** coesistono `/v1/` e `/api/v1/`; il frontend usa il secondo, ma la duplicazione può creare ambiguità.
4. **Routing SPA e fallback:** Nginx non definisce un fallback separato per le route client-side. Il comportamento dipende dal passaggio della richiesta a Django e dal fallback Django; va verificato con un refresh diretto di ogni route Vue.
5. **Base path non centralizzato:** Vite usa base diverse tra dev e produzione, mentre router e API hanno stringhe hardcoded.
6. **Gestione errori frontend assente:** non sono visibili confini comuni per errori HTTP, autenticazione scaduta, timeout o risposte paginate.
7. **Dipendenza CDN:** Bootstrap, Popper e Bootstrap JavaScript arrivano da jsDelivr; un problema di rete o di Content Security Policy può alterare l'interfaccia.
8. **Debug di default:** `settings/default.py` imposta `DEBUG = True` e `ALLOWED_HOSTS = []`; la configurazione di produzione corregge `DEBUG`, ma la scelta del modulo settings deve essere garantita in ogni deployment.

## 9. Raccomandazioni operative

1. Rendere la build frontend una fase esplicita della CI/CD o del Dockerfile multi-stage e verificare la presenza del manifest prima del deploy.
2. Introdurre un client HTTP Vue centralizzato, con base URL, gestione errori, timeout e autenticazione coerenti.
3. Implementare almeno una vista reale, ad esempio la ricerca sistemi, usando `GET /api/v1/systems` e gestendo paginazione/loading/error.
4. Scegliere e documentare un solo namespace API pubblico, preferibilmente `/api/v1/`, oppure dichiarare formalmente la differenza tra i due.
5. Aggiungere test frontend per rendering, chiamate API e stati di errore, oltre ai test DRF già presenti.
6. Verificare con test end-to-end dev e prod: apertura `/`, refresh diretto di `/ScrollTextAnimation`, caricamento degli asset, risposta Swagger e richieste API autenticata/non autenticata.

## Riferimenti principali nel codice

- [ed_frontend/src/main.js](../eddai_EliteDangerousApiInterface/ed_frontend/src/main.js)
- [ed_frontend/src/App.vue](../eddai_EliteDangerousApiInterface/ed_frontend/src/App.vue)
- [ed_frontend/src/router/index.js](../eddai_EliteDangerousApiInterface/ed_frontend/src/router/index.js)
- [ed_frontend/vite.config.js](../eddai_EliteDangerousApiInterface/ed_frontend/vite.config.js)
- [ed_core/templatetags/render_vite_assets.py](../eddai_EliteDangerousApiInterface/ed_core/templatetags/render_vite_assets.py)
- [templates/index.html](../eddai_EliteDangerousApiInterface/templates/index.html)
- [ed_core/urls.py](../eddai_EliteDangerousApiInterface/ed_core/urls.py)
- [docker-compose.yml](../docker-compose.yml)
- [nginx/nginx.conf](../nginx/nginx.conf)
