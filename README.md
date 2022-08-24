# Stack Orchestrator

Stack Orchestrator allows building and deployment of a Laconic stack on a single machine with minimial prerequisites.

## Setup
### Developer Mode
Developer mode runs the orchestrator from a cloned git repository.
#### Prerequisites
Stack Orchestrator is a Python3 CLI tool that runs on any OS with Python3 and Docker. Tested on: Ubuntu 20/22.

Ensure that the following are already installed:

1. Python3 (the version 3.8 available in Ubuntu 20/22 works)
   ```
   $ python3 --version
   Python 3.8.10
   ```
1. Docker (Install a current version from dockerco, don't use the version from any Linux distro)
   ```
   $ docker --version
   Docker version 20.10.17, build 100c701
   ```
#### Install
1. Clone this repository:
   ```
   $ git clone (https://github.com/cerc-io/stack-orchestrator.git
   ```
1. Enter the project directory:
   ```
   $ cd stack-orchestrator
   ```
1. Create and activate a venv:
   ```
   $ python3 -m venv venv
   $ source ./venv/bin/activate
   (venv) $
   ```
1. Install the cli in edit mode:
   ```
   $ pip install --editable .
   ```
1. Verify installation:
   ```
   (venv) $ laconic-so
   Usage: laconic-so [OPTIONS] COMMAND [ARGS]...

    Laconic Stack Orchestrator

   Options:
    --quiet
    --verbose
    --dry-run
    -h, --help  Show this message and exit.

   Commands:
    build-containers    build the set of containers required for a complete...
    deploy-system       deploy a stack
    setup-repositories  git clone the set of repositories required to build...
   ```
### CI Mode
_write-me_

## Usage
There are three sub-commands: `setup-repositories`, `build-containers` and `deploy-system` that are generally run in order:
### Setup Repositories
Clones the set of git repositories necessary to build a system.

Note: the use of `ssh-agent` is recommended in order to avoid entering your ssh key passphrase for each repository.
```
$ laconic-so --verbose setup-repositories
```
### Build Containers
Builds the set of docker container images required to run a system. It takes around 10 minutes to build all the containers from cold.
```
$ laconic-so --verbose build-containers
```
### Deploy System
Uses `docker compose` to deploy a system.

Use `---include <list of components>` to deploy a subset of all containers:
```
$ laconic-so --verbose deploy-system --include db-sharding,contract,ipld-eth-server,go-ethereum-foundry up
```
```
$ laconic-so --verbose deploy-system --include db-sharding,contract,ipld-eth-server,go-ethereum-foundry down
```
## Implementation
The orchestrator's operation is driven by files shown below. `repository-list.txt` container the list of git repositories; `container-image-list.txt` contains
the list of container image names, while `clister-list.txt` specifies the set of compose components (corresponding to individual docker-compose-xxx.yml files which may in turn specify more than one container).
Files required to build each container image are stored under `./container-build/<container-name>`
Files required at deploy-time are stored under `./config/<component-name>`
```
├── cluster-list.txt
├── compose
│   ├── docker-compose-contract.yml
│   ├── docker-compose-db-sharding.yml
│   ├── docker-compose-db.yml
│   ├── docker-compose-eth-statediff-fill-service.yml
│   ├── docker-compose-go-ethereum-foundry.yml
│   ├── docker-compose-ipld-eth-beacon-db.yml
│   ├── docker-compose-ipld-eth-beacon-indexer.yml
│   ├── docker-compose-ipld-eth-server.yml
│   ├── docker-compose-lighthouse.yml
│   └── docker-compose-prometheus-grafana.yml
├── config
│   └── ipld-eth-server
├── container-build
│   ├── cerc-eth-statediff-fill-service
│   ├── cerc-go-ethereum
│   ├── cerc-go-ethereum-foundry
│   ├── cerc-ipld-eth-beacon-db
│   ├── cerc-ipld-eth-beacon-indexer
│   ├── cerc-ipld-eth-db
│   ├── cerc-ipld-eth-server
│   ├── cerc-lighthouse
│   └── cerc-test-contract
├── container-image-list.txt
├── repository-list.txt
```

_write-more-of-me_
