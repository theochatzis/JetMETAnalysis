#!/bin/bash

./triggersForPureRate.py

for inpd in $(ls -d "${t3out}"/*); do
  outf=rates_$(basename "${inpd}").json
  rm -f "${outf}"
  ./triggerResultsCounts.py \
    -i "${inpd}"/*/job_*/out_*.root \
    -t triggersForPureRate.json \
    -l json_323775.txt \
    -o "${outf}" \
    -p HLTX \
    -v 1
done

#python mergeOutputs.py -l 1. -t 1. -p 1100
#23.31
