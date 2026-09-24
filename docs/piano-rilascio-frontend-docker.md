# Piano per il rilascio automatizzato del frontend Vue

**Data:** 24 settembre 2026  
**Repository:** EDDAI-EliteDangerousApiInterface  
**Obiettivo:** portare il frontend Vue in un'immagine Docker dedicata, rilasciata automaticamente e versionata insieme al backend Django.

## 1. Risultato finale desiderato

L'architettura di produzione dovra essere composta da immagini immutabili e versionate:

```text
frontend image
  Nginx + asset Vue compilati

backend image
  Django + API REST

worker images
  Celery / EDDN, riutilizzando l'immagine backend
```

Il container Nginx frontend dovra gestire:

- `/`: applicazione Vue;
- `/assets/`: asset Vue compilati, con base Vite `/`;
- `/static/`: asset Django, inclusi admin, DRF, Swagger e ReDoc;
- `/media/`: media persistenti, serviti da volume in sola lettura oppure da object storage;
- fallback delle route Vue verso `index.html`, solo per route applicative;
- `/api/`: proxy verso Django;
- `/admin/`: proxy verso Django;
- `/api/schema/`: proxy verso Django.

Django non dovra piu essere responsabile del rendering del guscio HTML iniziale della SPA. Dovra rimanere il servizio per API, autenticazione, amministrazione e logica applicativa. Gli asset Django dovranno essere raccolti nell'immagine backend e pubblicati da Nginx, mentre i media dovranno rimanere separati dagli asset immutabili.

In produzione non dovranno essere necessari bind mount del codice frontend o della directory `static-server`. Il solo volume ammesso per il frontend sara il volume media in sola lettura, salvo adozione di object storage.

## 2. Decisioni architetturali da confermare

Prima di iniziare l'implementazione devono essere confermate queste decisioni:

- il frontend sara pubblicato sullo stesso dominio del backend;
- le API pubbliche resteranno esclusivamente sotto `/api/v1/`;
- il namespace `/v1/` verra rimosso oppure documentato come compatibilita temporanea prima della migrazione;
- l'autenticazione Vue usera sessione Django e CSRF same-origin;
- Nginx frontend sara il punto di ingresso pubblico dietro Traefik;
- frontend e backend avranno immagini separate ma la stessa versione applicativa;
- il registry di riferimento restera GHCR;
- le release saranno generate da tag Git, ad esempio `v1.2.0`;
- il percorso ufficiale iniziale sara Docker Compose; Helm verra mantenuto solo se usato realmente in produzione;
- il media storage sara un volume condiviso in Compose e un PVC condiviso oppure object storage in Kubernetes.

## 3. Attivita di implementazione

### 3.1 Definire il contratto di deployment

- Stabilire il nome definitivo delle immagini:
  - `ghcr.io/<owner>/eddai-frontend`;
  - `ghcr.io/<owner>/eddai-backend`.
- Stabilire la strategia dei tag:
  - tag immutabile della release, ad esempio `v1.2.0`;
  - eventuale tag di ambiente, ad esempio `production`;
  - evitare `latest` per il deployment produttivo.
- Definire come il server ricevera la versione da installare.
- Definire il processo di rollback a una versione precedente.

### 3.2 Adeguare il frontend Vue

- Verificare che `npm ci` e `npm run build` funzionino in ambiente Linux pulito.
- Mantenere `package-lock.json` aggiornato e obbligatorio per la build.
- Configurare il base path tramite variabile di ambiente Vite.
- Configurare il base path di produzione a `/`, in modo che Vite pubblichi gli asset sotto `/assets/`.
- Eliminare ogni dipendenza da `/static-server/vuejs/` e `/static/vuejs/` per gli asset Vue.
- Centralizzare gli endpoint API in un client HTTP frontend.
- Usare URL relativi, ad esempio `/api/v1/`, per evitare configurazioni CORS non necessarie.
- Gestire almeno gli stati `loading`, `empty`, `error` e `success` nelle viste che consumano API.
- Aggiungere test unitari per router, componenti principali e client API.
- Verificare il refresh diretto delle route Vue in produzione.
- Includere nel bundle le dipendenze oggi caricate da jsDelivr, inclusi Bootstrap e Popper, per eliminare la dipendenza dalla CDN.

### 3.3 Gestire gli asset Django e i media

Gli asset Django non devono essere confusi con quelli Vue. La scelta preferita e usare WhiteNoise nel backend, ma solo dopo un PoC con l'applicazione ASGI eseguita da Daphne. WhiteNoise e storicamente middleware WSGI: se il PoC non dimostra il serving corretto degli asset con Daphne, si dovra usare l'opzione alternativa di copia degli asset nel runtime frontend tramite `--build-context` o `COPY --from` di un'immagine backend gia costruita.

La soluzione scelta dovra:

- eseguire `collectstatic` durante la build dell'immagine backend;
- conservare gli asset raccolti in una directory dedicata, ad esempio `/app/static-collected/`;
- garantire la presenza di CSS e JavaScript per admin, DRF, Swagger e ReDoc;
- se il PoC WhiteNoise passa, servire `/static/` dal backend e proxyare da Nginx verso Django;
- se il PoC WhiteNoise fallisce, copiare `/app/static-collected/` nell'immagine frontend usando un contesto di build aggiuntivo o un'immagine backend gia disponibile. In questo caso il backend deve essere costruito prima del frontend, e la CI deve rispettare tale ordine;
- verificare che il metodo scelto funzioni con `DEBUG=False`.

Il percorso `/media/` deve restare separato:

- in Docker Compose, montare il volume media in sola lettura nel container Nginx frontend e servirlo con `alias`;
- in Helm, usare un PVC condiviso oppure object storage compatibile con S3 esclusivamente per `/media/`, mai per `/static/`;
- non copiare i media nell'immagine Docker;
- non inoltrare `/media/` a Django come se fosse una risorsa statica.

### 3.4 Creare l'immagine Docker frontend

Creare un Dockerfile dedicato, ad esempio `ed_frontend/Dockerfile`, con build multi-stage:

1. stage Node per installazione delle dipendenze;
2. stage Node per `npm run build`;
3. stage runtime Nginx contenente esclusivamente `dist/` e la configurazione Nginx.

Requisiti del Dockerfile:

- usare Node 24 LTS fissato a digest; allineare `.nvmrc`, `engines` e CI;
- usare `npm ci`, non `npm install`;
- non copiare `node_modules` nell'immagine runtime;
- non includere sorgenti, test o strumenti Node nell'immagine finale;
- usare `nginxinc/nginx-unprivileged` su variante alpine-slim;
- configurare Nginx sulla porta interna 8080;
- eseguire il runtime con utente non root;
- aggiungere un healthcheck HTTP;
- mantenere il contesto Docker limitato alla directory frontend quando si usa WhiteNoise; l'opzione alternativa deve dichiarare esplicitamente il contesto backend aggiuntivo e la dipendenza di ordine;
- non usare volumi per gli asset compilati in produzione.

### 3.5 Adeguare Nginx

Creare una configurazione Nginx per la SPA frontend che:

- serva `index.html` e gli asset dalla directory interna dell'immagine;
- applichi `try_files $uri $uri/ /index.html` solo alle route client-side;
- restituisca `404` per gli asset mancanti sotto `/assets/`, senza fallback a `index.html`;
- serva `/static/` dagli asset Django raccolti nell'immagine backend o copiati nello stage finale;
- serva `/media/` con `alias` da un volume in sola lettura, oppure da object storage;
- inoltri le richieste API a `django:8080`;
- inoltri il valore originale di `X-Forwarded-Proto` ricevuto da Traefik, senza sostituirlo con `$scheme`;
- configuri `real_ip` con `set_real_ip_from` limitato alle reti fidate di Traefik;
- preservi `Host`, `X-Forwarded-For`, `X-Forwarded-Proto` e `X-Real-IP`;
- gestisca correttamente websocket o richieste ASGI eventualmente necessarie;
- imposti cache lunga sugli asset con hash nel nome;
- imposti `Cache-Control: no-cache` ed ETag su `index.html`;
- includa gli header di sicurezza tramite un file `include` comune, per evitare la perdita degli header causata da `add_header` dentro un `location`;
- esponga `/version.json` come file statico del frontend, con versione applicativa e Git SHA generati durante la build;
- riservi `/version` a un endpoint esplicito e non al fallback SPA, oppure non lo usi nello smoke test;
- restituisca un endpoint di healthcheck non dipendente dal database, se possibile.

La configurazione attuale di [nginx/nginx.conf](../nginx/nginx.conf) dovra essere sostituita o separata in una configurazione coerente con il nuovo ruolo del container.

### 3.6 Separare il ruolo Django

- In Fase 1, mantenere il rendering Django richiede che il backend contenga il manifest Vite e gli asset Vue: eseguire `npm ci`/`npm run build` in uno stage Node del Dockerfile backend oppure usare `COPY --from` da uno stage Node. Il frontend runtime separato non puo fornire questi file al backend e il bind mount `static-server` deve essere rimosso anche da questa fase.
- In Fase 2, rimuovere la dipendenza del rendering Django dal manifest Vite.
- Rendere Django responsabile delle API, dell'admin e delle risorse server-side necessarie.
- Rimuovere il fallback `re_path(r'^.*$', IndexTemplateView.as_view())` dopo la migrazione della shell SPA.
- Definire una risposta 404 JSON per le API, senza restituire `index.html`.
- Configurare `SECURE_PROXY_SSL_HEADER`, `USE_X_FORWARDED_HOST` e un `ALLOWED_HOSTS` reale.
- Configurare `CSRF_TRUSTED_ORIGINS` con gli origin HTTPS effettivamente utilizzati.
- Creare un endpoint dedicato con `@ensure_csrf_cookie` per inizializzare il cookie CSRF.
- Implementare nel client Vue l'invio dell'header `X-CSRFToken` per le richieste mutative.
- Usare sessione Django e CSRF same-origin con cookie `Secure` e `SameSite=Lax`.
- Non salvare token di autenticazione in `localStorage`.
- Verificare redirect, gestione degli errori 401/403 e scadenza della sessione.
- Mantenere Swagger/ReDoc raggiungibili tramite Django.
- Verificare che le route `/api/` non vengano intercettate dal fallback Vue.

### 3.7 Adeguare Docker Compose

Modificare [docker-compose.yml](../docker-compose.yml) per:

- usare l'immagine frontend pubblicata nel registry;
- rimuovere il bind mount `static-server` dal servizio Nginx;
- montare il volume media in sola lettura nel frontend Nginx;
- lasciare i volumi scrivibili solo per dati realmente persistenti, come media e database;
- configurare il proxy frontend verso il servizio Django;
- usare riferimenti immutabili completi per le immagini, ad esempio `ghcr.io/<owner>/eddai-frontend:v1.2.0@sha256:<digest>`, non soltanto un tag `APP_VERSION` mutabile;
- mantenere le immagini backend e frontend allineate alla stessa release, salvando separatamente i due digest;
- usare `nginxinc/nginx-unprivileged` sulla porta 8080 e aggiornare le label Traefik;
- aggiungere `read_only: true`, `cap_drop: [ALL]`, `no-new-privileges` e tmpfs necessari al runtime;
- definire healthcheck e `depends_on: condition: service_healthy` dove utili;
- garantire che il deploy non esegua build locali sul server di produzione.

Esempio concettuale:

```yaml
services:
  frontend:
    image: ${FRONTEND_IMAGE_REF}

  django:
    image: ${BACKEND_IMAGE_REF}
```

`FRONTEND_IMAGE_REF` e `BACKEND_IMAGE_REF` devono contenere repository, tag e digest risolti dal deploy. `APP_VERSION` puo restare come metadato comune, ma non deve essere usato da solo per selezionare l'immagine.

### 3.8 Estendere la CI/CD

Aggiornare [build-and-push.yml](../.github/workflows/build-and-push.yml) per includere:

- job frontend con `npm ci`;
- test unitari frontend;
- build frontend;
- verifica dell'esistenza di `dist/index.html`;
- tag coerenti tra le due immagini;
- cache npm e cache BuildKit;
- build delle immagini senza pubblicarle inizialmente oppure pubblicazione di tag candidati immutabili, ad esempio `sha-<commit>`;
- scansione Trivy dell'esatto artefatto che verra pubblicato: per build multi-arch, scansionare ogni immagine per architettura prima dell'indice manifest oppure pubblicare il candidato, scansionarlo per digest e promuovere lo stesso digest alla release;
- pubblicazione e firma solo dopo il superamento delle scansioni;
- fallimento della pipeline su vulnerabilita HIGH/CRITICAL, con `ignore-unfixed` solo se motivato;
- firma Cosign keyless sul digest con OIDC;
- SBOM e provenance tramite BuildKit (`sbom: true`, `provenance: mode=max`);
- output con digest delle immagini prodotte.

Aggiornare [check-and-test.yml](../.github/workflows/check-and-test.yml) per eseguire la build frontend anche sulle Pull Request. Una build frontend fallita deve bloccare il merge.

Le action GitHub dovranno essere fissate a SHA completi con commento della versione, incluse checkout, setup, Docker, Trivy, upload e Cosign. `trivy-action` dovra essere almeno `0.35.0` e fissata a SHA; il binario Trivy dovra avere una versione esplicita, mai `latest` e mai `0.69.4`. Renovate o Dependabot dovra aggiornare periodicamente gli SHA e le versioni dopo una verifica di sicurezza.

I workflow dovranno inoltre:

- evitare `pull_request_target`;
- dichiarare `contents: read` come permesso predefinito;
- concedere `packages: write`, `id-token: write` e `attestations: write` solo al job che pubblica;
- non esporre credenziali nei log o nelle immagini;
- usare tag Git protetti con ruleset per il pattern `v*`.

### 3.9 Gestire migrazioni e compatibilita delle release

Il rollback dell'immagine non annulla le migrazioni del database. Prima del deployment occorre:

- eseguire un backup verificato del database;
- avviare un job `migrate` one-shot prima dei servizi applicativi;
- attendere il completamento positivo del job prima di avviare Django, Celery ed EDDN;
- progettare le migrazioni con strategia expand/contract;
- mantenere le migrazioni compatibili almeno con la versione N-1 durante il rollout;
- evitare di rimuovere colonne o modificare contratti usati dalla versione precedente nello stesso rilascio;
- aggiornare insieme backend Django, worker Celery ed EDDN usando lo stesso digest applicativo;
- definire una procedura per migrazioni non retrocompatibili e rollback applicativo.

Il job di migrazione dovra essere eseguito una sola volta. Non deve essere avviato automaticamente da ogni replica Django o Celery.

### 3.10 Automatizzare il deployment

Definire un workflow di deployment separato o un job successivo alla pubblicazione della release:

- ricevere il tag della release;
- autenticarsi al server o al registry senza salvare credenziali nel repository;
- risolvere il tag ai digest immutabili delle immagini;
- salvare la versione e i digest correnti per il rollback;
- eseguire il backup del database;
- eseguire il job di migrazione one-shot;
- aggiornare `FRONTEND_IMAGE_REF` e `BACKEND_IMAGE_REF` in Compose, oppure i riferimenti immutabili nei valori Helm;
- eseguire il pull delle immagini;
- avviare il nuovo frontend e il nuovo backend;
- usare `docker compose pull && docker compose up -d --wait --remove-orphans` in Compose;
- verificare healthcheck applicativi, `/healthz`, `/version.json` del frontend, l'endpoint di versione del backend sotto `/api/v1/` e un endpoint API;
- confrontare i digest attesi con `docker inspect` sui container in esecuzione. La risposta di versione non deve dichiarare il digest dell'immagine, che esiste solo dopo la build;
- interrompere il deployment se una verifica fallisce;
- conservare la versione precedente per il rollback.

Il deployment dovra usare environment GitHub dedicato alla produzione, con eventuale approvazione manuale e secrets limitati al job di deploy. L'accesso SSH dovra usare una chiave dedicata e limitata, conservata nei secrets dell'environment.

Il deploy dovra verificare la firma Cosign sul digest usando l'identita del workflow autorizzato. Firmare l'immagine senza verificare la firma in fase di deploy non fornisce una garanzia sufficiente.

### 3.11 Aggiornare Helm, se il deployment Kubernetes e attivo

Il chart Helm dovra:

- avere un valore separato per l'immagine frontend;
- avere un valore separato per l'immagine backend;
- usare lo stesso tag applicativo per entrambi, salvo scelta esplicita diversa;
- esporre il frontend tramite Ingress;
- instradare `/api/` verso Django;
- non montare asset frontend da volumi locali;
- gestire `/static/` nell'immagine backend/frontend secondo la scelta WhiteNoise o copia degli asset; usare PVC condiviso oppure object storage solo per `/media/`;
- verificare readiness e liveness di frontend e backend;
- eseguire il job di migrazione come hook o job controllato prima del rollout;
- impedire l'avvio dei worker prima della migrazione completata;
- permettere rollback con `helm rollback`.

## 4. Test e criteri di accettazione

Il lavoro sara completato quando saranno verificati tutti i seguenti casi:

- una Pull Request esegue test e build frontend automaticamente;
- una build frontend fallita blocca la pipeline;
- una release Git produce entrambe le immagini con lo stesso tag;
- il container frontend parte senza volumi contenenti asset compilati;
- l'apertura di `/` restituisce la SPA Vue;
- il refresh diretto di ogni route Vue funziona;
- `/assets/` restituisce gli asset Vue e un asset mancante restituisce `404`, non `index.html`;
- `/static/` restituisce gli asset di admin, DRF, Swagger e ReDoc;
- `index.html` usa `Cache-Control: no-cache` ed ETag;
- `/media/` viene servito dal volume in sola lettura o dall'object storage configurato;
- `/api/v1/` raggiunge Django e non il fallback Vue;
- `/v1/` ha un comportamento documentato e testato oppure non e piu esposto;
- Swagger/ReDoc restano raggiungibili;
- autenticazione, cookie CSRF e sessione funzionano dal frontend;
- il cookie CSRF viene inizializzato dall'endpoint dedicato e le richieste mutative inviano `X-CSRFToken`;
- Traefik, Nginx e Django conservano correttamente HTTPS e IP client fidato;
- gli asset statici vengono serviti dall'immagine frontend se e stata scelta la copia degli asset; con WhiteNoise viene verificato il serving dal backend attraverso il proxy Nginx;
- `/version.json` restituisce la versione applicativa e il Git SHA del frontend, mentre l'endpoint backend restituisce la propria versione;
- il job di migrazione viene eseguito una sola volta prima dei servizi applicativi;
- il backup viene creato prima del deployment;
- Celery ed EDDN usano la stessa versione del backend;
- il deployment verifica frontend e API dopo l'aggiornamento;
- il rollback a una versione precedente e verificabile, includendo la procedura per il database;
- le immagini vengono scansionate prima del push, firmate e verificate per digest;
- Compose e Helm non dipendono da file presenti sul filesystem dello sviluppatore.

I test devono includere Vitest per la logica dei componenti e Playwright in CI contro lo stack Compose reale. Playwright dovra verificare almeno caricamento iniziale, refresh di una route Vue, asset 404, API non intercettata dal fallback, login, cookie CSRF e accesso a Swagger.

## 5. Punti critici e rischi

### Routing SPA e routing Django

Il fallback `index.html` non deve catturare `/api/`, `/admin/`, `/static/`, `/media/` o `/api/schema/`. Un errore in questa regola puo restituire HTML al posto di JSON. Anche `/assets/` deve restituire `404` per file mancanti.

### Asset Django

Senza una strategia esplicita per `collectstatic`, admin, DRF, Swagger e ReDoc funzioneranno solo come HTML senza CSS o JavaScript. Il PoC deve verificare WhiteNoise con Daphne/ASGI; se fallisce, la build deve trasferire gli asset raccolti dal backend all'immagine frontend con un contesto Docker esplicito. In entrambi i casi la build deve verificare gli asset con `DEBUG=False`.

### Media persistenti

I media non appartengono all'immagine e non devono essere proxyati a Django in produzione. Un volume non condiviso tra Nginx e i processi che scrivono i media, oppure un PVC non adatto, puo causare file caricati non visibili. Object storage riduce questo accoppiamento.

### Autenticazione e CSRF

Spostare il rendering iniziale da Django a Nginx elimina il cookie CSRF inizializzato dal template. L'endpoint `ensure_csrf_cookie`, il client Vue e i cookie `Secure`/`SameSite=Lax` devono essere testati con un browser reale, non solo con una richiesta curl. Il token non deve essere memorizzato in `localStorage`.

### Proxy e sicurezza Django

Dietro Traefik e Nginx, usare `$scheme` in Nginx puo trasformare HTTPS in HTTP. Il valore originale di `X-Forwarded-Proto` deve essere inoltrato tramite `map` e Django deve essere configurato con `SECURE_PROXY_SSL_HEADER`, `USE_X_FORWARDED_HOST`, `CSRF_TRUSTED_ORIGINS` e `ALLOWED_HOSTS` espliciti. `DEBUG` deve essere disabilitato in produzione.

### Base path Vite

Il base path attuale deve essere uniformato. Un valore errato produce una pagina HTML funzionante ma con JavaScript e CSS restituiti con errore 404.

### Cache di `index.html`

Gli asset con hash possono avere cache lunga. `index.html` deve avere `Cache-Control: no-cache` ed ETag, cosi il browser rivalida la pagina a ogni richiesta. Gli header di sicurezza devono essere definiti con un `include` comune oppure ripetuti nei `location`, perche `add_header` in un `location` non eredita automaticamente tutti gli header del livello superiore.

### Compatibilita con deployment esistente

Docker Compose e Helm potrebbero descrivere ambienti diversi. Prima di modificare la pipeline bisogna stabilire quale dei due e il percorso produttivo ufficiale.

### Immagini e tag

Usare `latest` puo causare deploy non riproducibili. Il deployment deve usare tag immutabili o digest.

### Persistenza dei media

Gli asset Vue devono essere immutabili nell'immagine. I media caricati dagli utenti devono restare su volume o storage esterno e non devono essere confusi con gli asset frontend.

### Sicurezza della pipeline

Le credenziali di deploy non devono essere inserite nell'immagine, nei log o nei file Compose versionati. Occorre limitare i permessi del workflow e preferire credenziali a durata breve quando l'infrastruttura lo consente. Tutte le action devono essere fissate a SHA completi; `trivy-action` deve essere almeno `0.35.0`, con SHA verificato, e il binario deve avere una versione esplicita diversa da `latest` e `0.69.4`. `pull_request_target` non deve essere usato.

### Migrazioni e rollback

Ripristinare un'immagine precedente non ripristina lo schema del database. Backup, migrazioni expand/contract, compatibilita N-1 e procedura di rollback del database devono essere definiti prima della prima release automatica.

## 6. Informazioni necessarie prima dell'implementazione

Servono queste conferme:

- qual e l'ambiente di produzione ufficiale: Docker Compose, Helm/Kubernetes o entrambi;
- quale server esegue il deployment e con quale metodo di accesso;
- se Traefik continuera a terminare TLS davanti a Nginx;
- dominio pubblico e domini eventualmente usati per staging;
- strategia di autenticazione frontend desiderata;
- presenza di websocket o altre connessioni persistenti;
- nome definitivo delle immagini GHCR;
- formato delle release e convenzione dei tag;
- necessaria approvazione manuale prima della produzione;
- possibilita di usare secrets GitHub Environment;
- procedura attuale di rollback;
- requisiti per architetture Docker, ad esempio `amd64` e `arm64`;
- politiche di retention per immagini e artefatti CI;
- disponibilita di un ambiente staging per testare routing, cookie e asset.
- esito del PoC WhiteNoise con Daphne/ASGI; in caso negativo, contesto Docker aggiuntivo e ordine di build backend -> frontend per copiare `/static/`;
- strategia scelta per `/media/`: volume condiviso oppure object storage;
- retention dei backup e prova periodica di ripristino;
- versione minima di Trivy approvata e configurazione per soglie HIGH/CRITICAL;
- configurazione delle reti Traefik fidate per `set_real_ip_from`;
- chiave o policy Cosign keyless e identita del workflow autorizzata;
- disponibilita di Playwright e browser Chromium nel runner CI;
- strategia di compatibilita N-1 per le migrazioni attuali e future.

## 7. Ordine consigliato delle attivita

1. Confermare le decisioni architetturali e le informazioni operative.
2. Definire il contratto delle immagini, dei digest e dei tag protetti.
3. **Fase 1:** aggiungere build multi-stage Vue alla CI, pubblicare l'immagine frontend e chiudere il rischio della build implicita, mantenendo temporaneamente il guscio Django.
4. Rendere il frontend eseguibile e testabile in ambiente Linux pulito.
5. Creare Dockerfile frontend, runtime Nginx non-root e configurazione per `/assets/`, `/static/` e `/media/`.
6. Implementare `collectstatic`, eseguire il PoC WhiteNoise con Daphne/ASGI e scegliere WhiteNoise oppure copia degli asset Django nello stage frontend con contesto Docker aggiuntivo.
7. Implementare endpoint CSRF, client `X-CSRFToken` e configurazione proxy HTTPS di Django.
8. **Fase 2:** separare il rendering SPA da Django e rimuovere il fallback Django generico.
9. Aggiornare Compose e, se necessario, Helm con volumi, healthcheck e security context.
10. Aggiungere job di backup e migrazione one-shot con compatibilita N-1.
11. Aggiornare CI per scan prima del push, SBOM, provenance, firma e verifica per digest.
12. Implementare il deployment versionato con riferimenti immutabili `repo:tag@sha256:digest`, `--wait`, `/version.json`, endpoint backend di versione, healthcheck e rollback.
13. Eseguire test Playwright end-to-end contro lo stack Compose in staging.
14. Eseguire una release di prova e verificare anche il ripristino del database.
15. Passare alla produzione dopo la verifica dei criteri di accettazione.

## 8. Deliverable finali

- immagine `eddai-frontend` versionata;
- immagine backend versionata e compatibile;
- Dockerfile multi-stage frontend;
- configurazione Nginx per SPA e proxy API;
- Compose aggiornato senza bind mount degli asset;
- chart Helm aggiornato, se utilizzato;
- workflow CI per test e build frontend;
- workflow release per pubblicazione immagini;
- workflow deployment con healthcheck e rollback;
- test frontend e test end-to-end;
- documentazione aggiornata per sviluppo, release e rollback.
