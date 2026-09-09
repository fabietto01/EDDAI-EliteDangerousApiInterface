# EDDAI Helm Chart

Helm Chart per installare l'applicazione EDDAI (Elite Dangerous Data API Interface) su Kubernetes con tutti i componenti necessari: Django, Celery, EDDN listener, RabbitMQ, Redis e PostGIS.

## 🎯 Caratteristiche

- **Portabile**: Compatibile con qualsiasi StorageClass e IngressClass (no vendor lock-in)
- **Sicuro**: Pod non-root, capabilities droppate, NetworkPolicy, credenziali gestite tramite Secret
- **Modulare**: RabbitMQ/Redis/PostGIS possono essere sostituiti con servizi esterni
- **Production-ready**: Resource limits, health checks, security contexts configurati
- **User-managed Secrets**: Controllo completo su credenziali e configurazioni sensibili

## 📋 Componenti Deployati

| Componente | Replicas | Descrizione |
|------------|----------|-------------|
| **Django** | 1 | Server ASGI (Daphne) su porta 8080 |
| **EDDN Listener** | 1 | Recupera dati da ZMQ e li passa ai worker |
| **Celery Task** | 3 | Worker coda `default` |
| **Celery Admin** | 3 | Worker coda `admin` |
| **Celery Ed-DBSync** | 3 | Worker coda `ed_dbsync` |
| **Celery All** | 3 | Worker multi-coda |
| **Celery Beat** | 1 | Scheduler con DatabaseScheduler |
| **RabbitMQ** | 1 | Message broker (StatefulSet) |
| **Redis** | 1 | Cache e result backend (StatefulSet) |
| **PostGIS** | 1 | Database PostgreSQL + PostGIS (StatefulSet) |

**Totale: 19 Pod + 1 Job di inizializzazione database**

## 🚀 Quick Start

### 1. Crea il namespace

```bash
kubectl create namespace eddai
```

### 2. Crea i Secret richiesti

**4 Secret obbligatori** da creare manualmente prima dell'installazione:

```bash
# PostGIS
kubectl create secret generic eddai-postgis-secret -n eddai \
  --from-literal=user=postgres \
  --from-literal=password=postgres123 \
  --from-literal=database=eddai \
  --from-literal=port=5432

# RabbitMQ
kubectl create secret generic eddai-rabbitmq-secret -n eddai \
  --from-literal=user=rabbitmq \
  --from-literal=password=rabbitmq123 \
  --from-literal=vhost=/ \
  --from-literal=port=5672

# Redis
kubectl create secret generic eddai-redis-secret -n eddai \
  --from-literal=port=6379 \
  --from-literal=password=redis123

# Django Application
kubectl create secret generic eddai-app-secret -n eddai \
  --from-literal=DJANGO_SECRET_KEY='django-secret-key-change-in-production' \
  --from-literal=DJANGO_EMAIL_HOST_PASSWORD='email-password' \
  --from-literal=EDDN_USER_PASSWORD_AGENT='eddn-password'
```

### 3. Installa il Chart

**Dal repository Helm** (consigliato):
```bash
helm repo add eddai https://fabietto01.github.io/EDDAI-EliteDangerousApiInterface/
helm repo update
helm install eddai eddai/eddai -n eddai
```

**Dal repository locale clonato**:
```bash
git clone https://github.com/fabietto01/EDDAI-EliteDangerousApiInterface.git
cd EDDAI-EliteDangerousApiInterface
helm install eddai charts/eddai -n eddai
```

### 4. Verifica lo stato

```bash
kubectl get pods -n eddai
```

### 5. Accedi all'applicazione

```bash
kubectl port-forward -n eddai svc/eddai-django 8080:8080
# Visita http://localhost:8080
```

## 📚 Documentazione Dettagliata

### Struttura dei `values.yaml`

Ogni servizio ha una sezione autonoma con valori configurabili:

```yaml
# Dipendenze infrastrutturali
rabbitmq:
  enabled: true           # Deploy interno
  external: false         # O usa un servizio esterno
  credentialsSecret: "eddai-rabbitmq-secret"

redis:
  enabled: true
  external: false
  credentialsSecret: "eddai-redis-secret"

postgis:
  enabled: true
  external: false
  credentialsSecret: "eddai-postgis-secret"

# Applicazione
django:
  replicas: 1             # Limitato a 1 per RWO storage
  persistence:
    size: 5Gi

celery:
  workers:
    task:
      enabled: true
      replicas: 3
    admin:
      enabled: true
      replicas: 3
    ed-dbsync:
      enabled: true
      replicas: 3
    beat:
      enabled: true
      replicas: 1         # Beat deve avere esattamente 1 replica

eddn:
  enabled: true
  replicas: 1

app:
  env:
    DJANGO_SETTINGS_MODULE: "eddai_EliteDangerousApiInterface.settings.prod"
  credentialsSecret: "eddai-app-secret"
```

### Storage e Volumi Persistenti

**StorageClass configurazione**:
```yaml
global:
  storageClass: "standard"  # Default per tutti i PVC

# Override per singolo servizio
django:
  persistence:
    storageClass: "fast-ssd"
```

**Volumi creati automaticamente**:
| Componente | Path | Size | AccessMode |
|------------|------|------|------------|
| Django media | `/app/media-server` | 5Gi | ReadWriteOnce |
| PostGIS | `/var/lib/postgresql/data` | 10Gi | ReadWriteOnce |
| RabbitMQ | `/var/lib/rabbitmq` | 5Gi | ReadWriteOnce |
| Redis | `/data` | 2Gi | ReadWriteOnce |

Compatibile con StorageClass: `rancher.io/local-path`, `longhorn`, `ceph-rbd`, ecc.

### Ingress

Abilita Ingress per esporre Django esternamente:

```yaml
ingress:
  enabled: true
  className: "nginx"  # o "traefik", "haproxy", ecc.
  host: eddai.example.com
  path: /
  tls:
    enabled: true
    secretName: eddai-tls-cert
```

### Usare Servizi Esterni

Per usare RabbitMQ/Redis/PostGIS esterni anziché deployment interni:

```yaml
rabbitmq:
  enabled: false          # Disabilita deployment interno
  external: true
  credentialsSecret: "eddai-rabbitmq-secret"  # Secret con host, port, user, password, vhost

redis:
  enabled: false
  external: true
  credentialsSecret: "eddai-redis-secret"     # Secret con host, port, password

postgis:
  enabled: false
  external: true
  credentialsSecret: "eddai-postgis-secret"   # Secret con host, port, user, password, database
```

## ✅ Verifica e Testing

**Validare il template prima dell'installazione**:
```bash
# Visualizza i manifest generati
helm template eddai charts/eddai -n eddai | less

# Dry-run con debug
helm install eddai charts/eddai -n eddai --dry-run --debug

# Lint del chart
helm lint charts/eddai
```

**Verificare lo stato del deployment**:
```bash
# Stato di tutti i pod
kubectl get pods -n eddai

# Eventi recenti
kubectl get events -n eddai --sort-by='.lastTimestamp'

# Log di un componente specifico
kubectl logs -n eddai deployment/eddai-django --tail=50
kubectl logs -n eddai deployment/eddai-celery-task --tail=50
kubectl logs -n eddai deployment/eddai-eddn --tail=50

# Verifica Secret e ConfigMap
kubectl get secret,configmap -n eddai
```

## ⚠️ Note e Limitazioni

### Django - Single Replica Limitation

**Situazione attuale**:
- Django è configurato con **1 replica** e PVC con `accessMode: ReadWriteOnce`
- Questo garantisce compatibilità con StorageClass standard come `rancher.io/local-path`

**Perché solo 1 replica?**:
- Il volume media (`/app/media-server`) deve essere condiviso tra tutte le repliche Django
- StorageClass `local-path` supporta solo ReadWriteOnce (RWO)
- Con RWO, solo un pod può montare il volume alla volta

**Soluzioni per scalare Django**:
- **Opzione 1**: Usare StorageClass con RWX (ReadWriteMany) come Longhorn, CephFS, NFS
- **Opzione 2**: Configurare Django per usare S3, MinIO o Azure Blob per i media files

### Celery Beat - Single Instance Only

- **Celery Beat** deve avere esattamente **1 replica**
- Deployment strategy è `Recreate` per evitare duplicazione durante gli aggiornamenti
- Avere più istanze di beat scheduler causa task duplicati

### EDDN Listener - Health Checks

**Limitazione attuale**:
- Il processo `python eddn.py` **non espone endpoint HTTP** per health checks
- Kubernetes verifica solo che il processo sia in esecuzione

**Miglioramento futuro**:
Implementare endpoint HTTP `/health` e `/ready` nel codice `eddn.py` per abilitare liveness/readiness probes.

## 📞 Supporto e Contributi

- **Repository**: [github.com/fabietto01/EDDAI-EliteDangerousApiInterface](https://github.com/fabietto01/EDDAI-EliteDangerousApiInterface)
- **Issues**: Segnala bug o richieste di funzionalità tramite GitHub Issues
- **Pull Requests**: Contributi benvenuti!

---

Per la versione completa del chart Helm con tutte le opzioni avanzate, consulta il repository:
[EDDAI-EliteDangerousApiInterface/helm](https://github.com/EDDAI-EliteDangerousApiInterface/helm)
