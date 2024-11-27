FROM python:3.11.5-alpine
LABEL maintainer="Tombo H."

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apk add --no-cache git gcc musl-dev libffi-dev

WORKDIR /src

# Clone le projet depuis le dépôt Git
RUN git clone --depth 1 https://github.com/manda2006/DSA_site_validator.git


WORKDIR /src/DSA_site_validator

# Installer les dépendances
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR /src/DSA_site_validator/validator

# Ajouter l'entrée
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

# Lancer l'entrée
ENTRYPOINT ["/entrypoint.sh"]
