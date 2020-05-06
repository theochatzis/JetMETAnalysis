#!/bin/bash

if [ ! -z ${JMEANA_BASE} ]; then
  echo "environment already set: JMEANA_BASE=${JMEANA_BASE}"
  return
fi

export JMEANA_BASE="${PWD}"

export PATH=${PATH}:${JMEANA_BASE}

export PYTHONPATH="${PYTHONPATH}":"${PWD}"
export PYTHONPATH="${PYTHONPATH}":"${PWD}"/common
export PYTHONDONTWRITEBYTECODE=1
