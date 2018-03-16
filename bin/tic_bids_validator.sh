#!/usr/bin/env bash

echo
echo

echo "cat .bidsignore"
echo "==============="
cat $ACTIVE_BIDS_PATH/.bidsignore;


echo
echo
echo "cat .bids.cfg"
echo "==============="
cat $ACTIVE_BIDS_PATH/.bids.cfg;

echo
echo
echo "-----------------------------------------------------------------------------------------------------------------"
echo

bids-validator -c $ACTIVE_BIDS_PATH/.bids.cfg $ACTIVE_BIDS_PATH ${@}
