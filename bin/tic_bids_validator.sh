#!/usr/bin/env bash


echo "cat .bidsignore"
echo "==============="
cat $ACTIVE_BIDS_PATH/.bidsignore;


echo "cat .bids.cfg"
echo "==============="
cat $ACTIVE_BIDS_PATH/.bids.cfg;

echo

bids-validator -c $ACTIVE_BIDS_PATH/.bids.cfg $ACTIVE_BIDS_PATH ${@}
