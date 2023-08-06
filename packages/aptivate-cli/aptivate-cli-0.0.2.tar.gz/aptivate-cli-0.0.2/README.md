[![pipeline status](https://git.coop/aptivate/internal-tools/aptivate-cli/badges/master/pipeline.svg)](https://git.coop/aptivate/internal-tools/aptivate-cli/commits/master)
[![coverage report](https://git.coop/aptivate/internal-tools/aptivate-cli/badges/master/coverage.svg)](https://git.coop/aptivate/internal-tools/aptivate-cli/commits/master)
[![PyPI version](https://badge.fury.io/py/aptivate-cli.svg)](https://badge.fury.io/py/aptivate-cli)

# aptivate-cli

Fully automated luxury Aptivate command line interface.

## Install It

```bash
$ pip3 install --user aptivate-cli
```

## Supported Features

  * Only Django deployments.
  * Only Django new style project structures.

## The Tao of aptivate-cli

> Writing Less Code Is Good.
>
> Writing No Code Is Even Better.

## Hack On It

Install Python 3.7 safely with [pyenv] by following [the installation guide] and then running:

[pyenv]: https://github.com/pyenv/pyenv
[the installation guide]: https://github.com/pyenv/pyenv#basic-github-checkout

```bash
$ pyenv init
$ pyenv install 3.7.0
$ pyenv shell 3.7.0
```

Then get a copy of the tool with:

```bash
$ git clone git@git.coop:aptivate/aptivate-cli.git
$ cd aptivate-cli
$ pipenv install --dev --python 3.7
```

Then start to run commands with:

```bash
$ pipenv run pip install --editable .
$ pipenv run aptivate-cli --help
```

## Release It

```bash
$ make test-publish  # assure things are right first
$ make publish       # run the real thing
```
