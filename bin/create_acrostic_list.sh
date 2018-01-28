#!/usr/bin/env bash

# This command will create a new acrostic list for the active BIDS directory.

find $ACTIVE_BIDS_PATH -maxdepth 1 -type d -name "sub-*" | \
rev | \
cut -d '/' -f 1 | \
rev | \
cut -c 5- | \
sort > $ACTIVE_BIDS_PATH/acrostic.list


# 1.  Create a list of the directories in the BIDS directory starting with sub. The find command is used instead of ls
#     so we can ensure that only directories starting with sub- are listed.
#
#     >>> find $ACTIVE_BIDS_PATH -maxdepth 1 -type d -name "sub-*"
#
#     /gandg/hfpef//bids/sub-hfs070
#     /gandg/hfpef//bids/sub-hfu044
#     /gandg/hfpef//bids/sub-hfu052
#     /gandg/hfpef//bids/sub-hfs085
#
# 2.  Reverse the list with the rev command
#
#     >>> find $ACTIVE_BIDS_PATH -maxdepth 1 -type d -name "sub-*" | rev
#
#     070sfh-bus/sdib//fepfh/gdnag/
#     440ufh-bus/sdib//fepfh/gdnag/
#     250ufh-bus/sdib//fepfh/gdnag/
#     580sfh-bus/sdib//fepfh/gdnag/
#     370ufh-bus/sdib//fepfh/gdnag/
#     770sfh-bus/sdib//fepfh/gdnag/
#
# 3. Cut list by the delimiter / and take the first field.
#
#
#      >>> find $ACTIVE_BIDS_PATH -maxdepth 1 -type d -name "sub-*" | rev | cut -d '/' -f 1
#
#      070sfh-bus
#      440ufh-bus
#      250ufh-bus
#      580sfh-bus
#      370ufh-bus
#
# 4. Reverse the result again
#
#     >>> find $ACTIVE_BIDS_PATH -maxdepth 1 -type d -name "sub-*" | rev | cut -d '/' -f 1  | rev
#
#     sub-hfs070
#     sub-hfu044
#     sub-hfu052
#     sub-hfs085
#     sub-hfu073
#     sub-hfs077
#
# 5. Cut and sort the results.
#
#   >>> find $ACTIVE_BIDS_PATH -maxdepth 1 -type d -name "sub-*" | rev | cut -d '/' -f 1 | rev | cut -c 5- | sort
#
#    hfs070
#    hfs072
#    hfs073
#    hfs076
#    hfs077
#
# 6. Write results to acrostic.list in the Active BIDS directory
#
#  >>> find $ACTIVE_BIDS_PATH -maxdepth 1 -type d -name "sub-*" | rev | cut -d '/' -f 1 | rev | cut -c 5- | sort  \
#      $ACTIVE_BIDS_DIR/acrostic.list


