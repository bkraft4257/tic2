#!/usr/bin/env bash

echo
echo "List of participants*.tsv"
echo "--------------------------------------------------------------------------"
ls -1 $ACTIVE_BIDS_PATH/participants*.tsv
echo
echo

echo "cat participants_all.tsv"
echo "--------------------------------------------------------------------------"
cat $ACTIVE_BIDS_PATH/participants_all.tsv
echo
