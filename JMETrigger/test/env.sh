#!/bin/bash

if [ ! -d ${JMEANA_BASE} ]; then
  return
fi

export JMEANA_BASE="${PWD}"

export PATH=${PATH}:${JMEANA_BASE}

export PYTHONPATH="${PYTHONPATH}":"${PWD}"
export PYTHONPATH="${PYTHONPATH}":"${PWD}"/common
export PYTHONDONTWRITEBYTECODE=1
