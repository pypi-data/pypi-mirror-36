<H1 align='center'> Featuren </H1>
<p align="center">
<a href="https://travis-ci.org/jairojair/featuren">
    <img src="https://travis-ci.org/jairojair/featuren.svg?branch=master" alt="Build Status">
</a>
<a href='https://coveralls.io/github/jairojair/featuren?branch=master'><img src='https://coveralls.io/repos/github/jairojair/featuren/badge.svg?branch=master&service=github' alt='Coverage Status' /></a>
</p>
<p align="center">
    <em>A simple application for managing your features in production.</em>
</p>

### Introduction

Feature flags give a software organization the power to reduce risk, iterate quicker, and gain more control. Feature flags allow you to decouple feature rollout from code deployment. This separation allows you unprecedented control of who sees what when, independent of release. And the “you” can be anyone in your organization – from developers, ops, designers, product managers, or marketers. Allowing control over a release unlocks the true power of your software.

More details about: http://featureflags.io


The main goal for this project is to create a simple and open source application for managing your features in production.

### Getting Started

*Requirement*

- [Docker](https://www.docker.com/products/docker-desktop)


##### Project setup

	docker-compose build
	docker-compose run app make migrate

##### Run standalone

	docker-compose up

Access: http://0.0.0.0:8000


### Development tips

- REST API Framework we're use [APIStar](https://github.com/encode/apistar)

- Database management we're use [Orator ORM](https://orator-orm.com)

- Test we're use [Pytest](https://docs.pytest.org/en/latest/)

---


Firstly, run the command below to go inside the container.

	docker-compose run --service-ports app /bin/sh

##### Run in migrations

	make migrate

##### Run tests

	make tests

##### Python code linter

	make lint


##### Python format code.

	make fmt


##### Run application

	make


##### Install new Python dependency

This way you can install a new Python dependency without rebuild docker image.

	make deps

##### Project clean

	make clean
