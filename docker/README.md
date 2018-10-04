# Using Dr. Scratch via Docker
This directory contains `Dockerfile` to make it easy to build and running drScratch environment.

## Installing Docker


## Running the container

We use `Makefile` to simmplify docker commands.
	$ make build

Run the containers of db and web application..
	$ make up

Run Django task to migrate tables of db.
	$ make migrate
