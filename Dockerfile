# Usa un'immagine base di conda
FROM continuumio/miniconda3:latest

# Imposta la directory di lavoro
WORKDIR /app

# Copia il file environment.yml e crea l'ambiente conda
COPY environment.yml .
RUN conda env create -f environment.yml

# Attiva l'ambiente
SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]

# Copia il codice del progetto
COPY ./eddai_EliteDangerousApiInterface/ .