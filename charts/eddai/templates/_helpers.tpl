{{/*
Nome base del chart/release
*/}}
{{- define "eddai.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "eddai.fullname" -}}
{{- printf "%s" .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "eddai.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Common labels
*/}}
{{- define "eddai.labels" -}}
helm.sh/chart: {{ include "eddai.chart" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/part-of: {{ include "eddai.fullname" . }}
{{- with .Values.global.labels }}
{{ toYaml . }}
{{- end }}
{{- end -}}

{{/*
Selector labels: uso "component" per distinguere ogni sotto-servizio
(rabbitmq, redis, postgis, django, celery-worker-task, ...)
*/}}
{{/*
Uso: {{ include "eddai.selectorLabels" (dict "ctx" . "component" "django") }}
*/}}
{{- define "eddai.selectorLabels" -}}
app.kubernetes.io/name: {{ include "eddai.name" .ctx }}
app.kubernetes.io/instance: {{ .ctx.Release.Name }}
app.kubernetes.io/component: {{ .component }}
{{- end -}}

{{- define "eddai.componentLabels" -}}
{{ include "eddai.labels" .ctx }}
{{ include "eddai.selectorLabels" . }}
{{- end -}}

{{/*
ServiceAccount name
*/}}
{{- define "eddai.serviceAccountName" -}}
{{- if .Values.serviceAccount.create -}}
{{- default (include "eddai.fullname" .) .Values.serviceAccount.name -}}
{{- else -}}
{{- default "default" .Values.serviceAccount.name -}}
{{- end -}}
{{- end -}}

{{/*
Risolve la StorageClass da usare: priorita' all'override puntuale del
servizio, poi global.storageClass, altrimenti "" (default del cluster).
Uso: {{ include "eddai.storageClass" (dict "local" .Values.rabbitmq.persistence.storageClass "global" .Values.global.storageClass) }}
*/}}
{{- define "eddai.storageClass" -}}
{{- if .local -}}
{{ .local }}
{{- else if .global -}}
{{ .global }}
{{- end -}}
{{- end -}}

{{/*
Logica comune enabled/external per le 3 dipendenze infra:
- enabled=true  & external=false -> il chart distribuisce lo StatefulSet interno
- enabled=false & external=true  -> nessuna risorsa interna, si usa un Secret
                                     esterno gia' presente nel namespace
- external=true prevale sempre su enabled per la scelta del Secret
- "active" = la dipendenza e' effettivamente disponibile per django/celery
             (o interna o esterna). Se enabled=false & external=false la
             dipendenza e' del tutto assente dall'envFrom applicativo.
*/}}
{{- define "eddai.rabbitmq.deployInternal" -}}
{{- and .Values.rabbitmq.enabled (not .Values.rabbitmq.external) -}}
{{- end -}}
{{- define "eddai.rabbitmq.active" -}}
{{- or .Values.rabbitmq.enabled .Values.rabbitmq.external -}}
{{- end -}}

{{- define "eddai.redis.deployInternal" -}}
{{- and .Values.redis.enabled (not .Values.redis.external) -}}
{{- end -}}
{{- define "eddai.redis.active" -}}
{{- or .Values.redis.enabled .Values.redis.external -}}
{{- end -}}

{{- define "eddai.postgis.deployInternal" -}}
{{- and .Values.postgis.enabled (not .Values.postgis.external) -}}
{{- end -}}
{{- define "eddai.postgis.active" -}}
{{- or .Values.postgis.enabled .Values.postgis.external -}}
{{- end -}}

{{/*
Nome del Secret con le credenziali fornite dall'utente.
Ora il Secret e' sempre fornito dall'utente, indipendentemente se
il componente e' interno (enabled=true) o esterno (external=true).
*/}}
{{- define "eddai.rabbitmq.secretName" -}}
{{ required "rabbitmq.credentialsSecret e' obbligatorio" .Values.rabbitmq.credentialsSecret }}
{{- end -}}

{{- define "eddai.redis.secretName" -}}
{{ required "redis.credentialsSecret e' obbligatorio" .Values.redis.credentialsSecret }}
{{- end -}}

{{- define "eddai.postgis.secretName" -}}
{{ required "postgis.credentialsSecret e' obbligatorio" .Values.postgis.credentialsSecret }}
{{- end -}}

{{/*
Nome del Secret con le variabili sensibili applicative (django/celery)
*/}}
{{- define "eddai.app.secretName" -}}
{{ required "app.credentialsSecret e' obbligatorio" .Values.app.credentialsSecret }}
{{- end -}}

{{/*
Helper per generare le env di RabbitMQ mappando le chiavi del Secret utente.
Se enabled=true, l'host viene sovrascritto con il Service interno.
*/}}
{{- define "eddai.rabbitmq.env" -}}
- name: CELERY_BROKER_HOST
{{- if .Values.rabbitmq.enabled }}
  value: {{ printf "%s-rabbitmq" (include "eddai.fullname" .) | quote }}
{{- else }}
  valueFrom:
    secretKeyRef:
      name: {{ include "eddai.rabbitmq.secretName" . }}
      key: host
{{- end }}
- name: CELERY_BROKER_PORT
  valueFrom:
    secretKeyRef:
      name: {{ include "eddai.rabbitmq.secretName" . }}
      key: port
- name: CELERY_BROKER_USER
  valueFrom:
    secretKeyRef:
      name: {{ include "eddai.rabbitmq.secretName" . }}
      key: user
- name: CELERY_BROKER_PASSWORD
  valueFrom:
    secretKeyRef:
      name: {{ include "eddai.rabbitmq.secretName" . }}
      key: password
- name: CELERY_BROKER_VHOST
  valueFrom:
    secretKeyRef:
      name: {{ include "eddai.rabbitmq.secretName" . }}
      key: vhost
{{- end -}}

{{/*
Helper per generare le env di Redis mappando le chiavi del Secret utente.
Se enabled=true, l'host viene sovrascritto con il Service interno.
*/}}
{{- define "eddai.redis.env" -}}
- name: DJANGO_CACHES_HOST
{{- if .Values.redis.enabled }}
  value: {{ printf "%s-redis" (include "eddai.fullname" .) | quote }}
{{- else }}
  valueFrom:
    secretKeyRef:
      name: {{ include "eddai.redis.secretName" . }}
      key: host
{{- end }}
- name: DJANGO_CACHES_PORT
  valueFrom:
    secretKeyRef:
      name: {{ include "eddai.redis.secretName" . }}
      key: port
- name: CELERY_RESULT_BACKEND_HOST
{{- if .Values.redis.enabled }}
  value: {{ printf "%s-redis" (include "eddai.fullname" .) | quote }}
{{- else }}
  valueFrom:
    secretKeyRef:
      name: {{ include "eddai.redis.secretName" . }}
      key: host
{{- end }}
- name: CELERY_RESULT_BACKEND_PORT
  valueFrom:
    secretKeyRef:
      name: {{ include "eddai.redis.secretName" . }}
      key: port
{{- if .Values.redis.auth.enabled }}
- name: REDIS_PASSWORD
  valueFrom:
    secretKeyRef:
      name: {{ include "eddai.redis.secretName" . }}
      key: password
{{- end }}
{{- end -}}

{{/*
Helper per generare le env di PostGIS mappando le chiavi del Secret utente.
Se enabled=true, l'host viene sovrascritto con il Service interno.
*/}}
{{- define "eddai.postgis.env" -}}
- name: POSTGIS_HOST
{{- if .Values.postgis.enabled }}
  value: {{ printf "%s-postgis" (include "eddai.fullname" .) | quote }}
{{- else }}
  valueFrom:
    secretKeyRef:
      name: {{ include "eddai.postgis.secretName" . }}
      key: host
{{- end }}
- name: POSTGIS_PORT
  valueFrom:
    secretKeyRef:
      name: {{ include "eddai.postgis.secretName" . }}
      key: port
- name: POSTGIS_USER
  valueFrom:
    secretKeyRef:
      name: {{ include "eddai.postgis.secretName" . }}
      key: user
- name: POSTGIS_PASSWORD
  valueFrom:
    secretKeyRef:
      name: {{ include "eddai.postgis.secretName" . }}
      key: password
- name: POSTGIS_DB
  valueFrom:
    secretKeyRef:
      name: {{ include "eddai.postgis.secretName" . }}
      key: database
{{- end -}}

{{/*
env comuni a django + tutti i celery: mappa i Secret con chiavi corrette
*/}}
{{- define "eddai.app.env" -}}
{{- if eq (include "eddai.rabbitmq.active" .) "true" }}
{{- include "eddai.rabbitmq.env" . }}
{{- end }}
{{- if eq (include "eddai.redis.active" .) "true" }}
{{- include "eddai.redis.env" . | nindent 0 }}
{{- end }}
{{- if eq (include "eddai.postgis.active" .) "true" }}
{{- include "eddai.postgis.env" . | nindent 0 }}
{{- end }}
{{- end -}}

{{/*
envFrom comune a django + tutti i celery: configmap + secret app
*/}}
{{- define "eddai.app.envFrom" -}}
- configMapRef:
    name: {{ include "eddai.fullname" . }}-app-config
- secretRef:
    name: {{ include "eddai.app.secretName" . }}
{{- end -}}

{{/*
Genera un Deployment Celery (worker o beat) unificato.
Uso: {{ include "eddai.celery.deployment" (dict "ctx" . "name" "task" "config" .Values.celery.workers.task) }}
*/}}
{{- define "eddai.celery.deployment" -}}
{{- if .config.enabled }}
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "eddai.fullname" .ctx }}-celery-{{ .name }}
  namespace: {{ .ctx.Release.Namespace }}
  labels:
    {{- include "eddai.componentLabels" (dict "ctx" .ctx "component" (printf "celery-%s" .name)) | nindent 4 }}
spec:
  replicas: {{ .config.replicas }}
  {{- if eq .config.type "beat" }}
  strategy:
    type: Recreate
  {{- end }}
  selector:
    matchLabels:
      {{- include "eddai.selectorLabels" (dict "ctx" .ctx "component" (printf "celery-%s" .name)) | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "eddai.componentLabels" (dict "ctx" .ctx "component" (printf "celery-%s" .name)) | nindent 8 }}
      {{- with .config.podAnnotations }}
      annotations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
    spec:
      serviceAccountName: {{ include "eddai.serviceAccountName" .ctx }}
      automountServiceAccountToken: {{ .ctx.Values.serviceAccount.automountServiceAccountToken }}
      {{- with .ctx.Values.global.imagePullSecrets }}
      imagePullSecrets:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      securityContext:
        {{- toYaml .ctx.Values.podSecurityContext | nindent 8 }}
      {{- with .config.nodeSelector }}
      nodeSelector:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .config.tolerations }}
      tolerations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .config.affinity }}
      affinity:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      containers:
        - name: celery-{{ .name }}
          image: "{{ .ctx.Values.image.repository }}:{{ .ctx.Values.image.tag }}"
          imagePullPolicy: {{ .ctx.Values.image.pullPolicy }}
          securityContext:
            {{- toYaml .ctx.Values.securityContext | nindent 12 }}
          command:
            {{- toYaml .config.command | nindent 12 }}
          envFrom:
            {{- include "eddai.app.envFrom" .ctx | nindent 12 }}
          env:
            {{- include "eddai.app.env" .ctx | nindent 12 }}
          resources:
            {{- toYaml .config.resources | nindent 12 }}
{{- end }}
{{- end -}}
