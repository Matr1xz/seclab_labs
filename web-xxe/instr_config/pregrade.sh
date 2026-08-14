#!/bin/bash
<<<<<<< HEAD
: <<'END'
This software was created by United States Government employees at 
The Center for Cybersecurity and Cyber Operations (C3O) 
at the Naval Postgraduate School NPS.  Please note that within the 
United States, copyright protection is not available for any works 
created  by United States Government employees, pursuant to Title 17 
United States Code Section 105.   This software is in the public 
domain and is not subject to copyright. 
END
#
# Script to run prior to grading a student's lab.  It is intended
# for two potential purposes:
# 1) Create solution artifacts to campare against student artifacts;
# 2) Process student artifacts into a different form, e.g., extracting
#    browser sqlite data as in the default instance of this file below.
# 
# 
#
homedir=$1
# destdir includes the container 
destdir=$2
dbg=/tmp/pregrade.log
cd $homedir/$destdir
is_sqlite=`which sqlite3`
if [ ! -z $is_sqlite ]; then
   #echo $is_sqlite
   here=`pwd`
   places=$here/.mozilla/firefox/*default/places.sqlite
   for fname in $(ls $places 2> /dev/null); do
     if [[ -f $fname ]]; then
        outpath=$here/.local/result
        outfile=$outpath/moz_places.txt
        mkdir -p "$outpath"
        sqlite3 "$fname" "SELECT moz_places.* FROM moz_places;" >"$outfile"
     fi
   done
fi

#
#  Add other processing below.
#
=======
# Record the required student-side report artifact before grading.
homedir="$1"
destdir="$2"
here="$homedir/$destdir"

if [ -f "$here/report_zap.html" ] || [ -f "$here/report_zap" ]; then
    mkdir -p "$here/.local/result"
    printf 'report_zap=present\n' > "$here/.local/result/report_status.txt"
fi

exit 0
>>>>>>> 935e6ccb8c624a081a7bfd33d47ad04fe2097d21
