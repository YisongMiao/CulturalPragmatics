#!/bin/bash

for eval_type in normal flip loc_thailand loc_usa; do
    python scripts/eval.py \
        --concept time_googlegen \
        --eval_type $eval_type
done
