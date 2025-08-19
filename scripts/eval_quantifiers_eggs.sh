#!/bin/bash

for eval_type in normal flip loc_thailand loc_usa; do
    python scripts/eval.py \
        --concept quantifiers_eggs \
        --eval_type $eval_type
done
