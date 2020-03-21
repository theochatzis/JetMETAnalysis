#!/bin/bash

export METANA_BASE="${PWD}"

export PATH=${PATH}:${METANA_BASE}

export PYTHONPATH="${PYTHONPATH}":"${PWD}"
export PYTHONPATH="${PYTHONPATH}":"${PWD}"/common
export PYTHONDONTWRITEBYTECODE=1
