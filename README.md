# ansible-docker-deployment-example
Run Containers with Ansible

## Purpose

This is a example on how to use ansible to deploy docker containers using the [docker_container](https://docs.ansible.com/ansible/2.5/modules/docker_container_module.html) module.

## Context

The `playbook.yml` was set to only deploy the docker container when running my target host using the local ansible connection, this was done for testing purposes, but if you are deploying against a linux server, it can install docker and deploy the container.

The default variables is defined in `custom.yml`, and for example the docker image tag is set to `docker_tag: ansible`, but in a case where the build and push process happens through CI, you can override this using `ansible-playbook --extra-vars docker_tag=$IMAGE_TAG [..]` etc.

The role has a template which generates the `.env` file for the container and loads it into the environment.

## Demonstration

Create a python virtual environment and install the dependencies:

```bash
$ virtualenv .venv -p python3
$ pip install ansible==4.10.0
$ pip install docker
```

To run this example, we can build our image:

```bash
docker build -t ruanbekker/flask-demo-app:ansible .
```

Then we can deploy our docker container (in this case to our laptop locally - as defined in the `inventory.ini`):

```bash
$ ansible-playbook playbook.yml --limit=my.laptop
...
PLAY RECAP *********************************
my.laptop                  : ok=5    changed=2    unreachable=0    failed=0    skipped=14   rescued=0    ignored=0
```

Then we can verify that the container is running:

```bash
$ docker ps
CONTAINER ID   IMAGE                               COMMAND           CREATED          STATUS          PORTS                              NAMES
d4841dd1f623   ruanbekker/flask-demo-app:ansible   "python app.py"   45 seconds ago   Up 43 seconds   0.0.0.0:5000->5000/tcp             flask-application
```

And we can test if our aplication is up:

```bash
$ curl -I http://localhost:5000/health
HTTP/1.0 204 NO CONTENT
Content-Type: text/html; charset=utf-8
Server: Werkzeug/1.0.1 Python/3.8.13
Date: Thu, 11 Aug 2022 21:17:52 GMT
```

To delete the container and cleanup the .env file:

```bash
$ ansible-playbook reset.yml --limit=my.laptop
...
PLAY RECAP ***************************
my.laptop                  : ok=4    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

## Taking this further

For non-local environments, you can install docker on the target host, and deploy the container on the target host.


## Directory Structure

```bash
.
├── Dockerfile
├── README.md
├── ansible.cfg
├── custom.yml
├── docker-compose.yml
├── handlers
│   └── main.yml
├── inventory.ini
├── playbook.yml
├── reset.yml
├── roles
│   ├── docker
│   │   ├── tasks
│   │   │   └── main.yml
│   │   └── vars
│   │       └── Ubuntu.yml
│   ├── docker-flask-app
│   │   ├── tasks
│   │   │   └── main.yml
│   │   └── templates
│   │       └── env.j2
│   ├── system
│   │   └── tasks
│   │       ├── essential.yml
│   │       ├── main.yml
│   │       └── user.yml
│   └── undeploy
│       └── tasks
│           └── main.yml
└── src
    ├── __init__.py
    ├── app.py
    ├── handlers
    │   ├── __init__.py
    │   └── routes.py
    ├── requirements.txt
    ├── templates
    │   └── index.html
    └── tests
        ├── __init__.py
        └── test_app.py

16 directories, 25 files
```
