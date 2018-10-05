# Using Dr. Scratch via Docker
This directory contains `Dockerfile` to make it easy to build and running drScratch environment via [Docker](https://www.docker.com/).

## Installing Docker
General instructions to install Docker can be followed in the next links:
[Install Docker](https://docs.docker.com/install/).
[Install Docker Compose](https://docs.docker.com/compose/install/).

## Running the container

We use `Makefile` to simplify docker-compose commands.

Build Docker images of db and web application.
```bash
$ make build
```

Run the containers of db and web application.
```bash
$ make up
```

Run Django task to migrate tables of db.
```bash
$ make migrate
```
