#!/bin/bash

###############################################################################
# Purpose of this script is to wait for completion of the wrapped
# script, and then make a tarfile of the results.
# 
# Call this script with the same arguments intended to be given to the script
# that will perform the actual work.
# 
# It requires two environment variables:
# 
# SCRIPT is the path to the actual script that was submitted by the shuttle client.
# ARCHIVE_DIR is the location in which to place the output files.
# 
###############################################################################

$SCRIPT $@
SCRIPT_EXIT=$?
sleep 1

if [[ $SCRIPT_EXIT -eq 0 ]]; then
  echo "SUCCESS"
  tar -cvzf $ARCHIVE_DIR/$JOB_ID.tgz * 1> /dev/null
else
  echo "Script exited with $SCRIPT_EXIT.  Please have a look."
fi

exit $SCRIPT_EXIT
