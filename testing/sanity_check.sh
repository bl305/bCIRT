#!/bin/bash

FILELIST=$(find ../ -name models.py)
TABLELIST=""
for FILEPATH in ${FILELIST}; do
    TABLENAME=$(cat ${FILEPATH}|grep '^class'|cut -d" " -f2|cut -d "(" -f1)
    TABLELIST=${TABLELIST}" "${TABLENAME}
done
echo ${TABLELIST}

EXPORTTABLES=$(grep "tablename = '" ../invs/management/commands/dbexport.py |cut -d"'" -f2)
#echo ${EXPORTTABLES}
for ONETABLE in ${TABLELIST}; do
  MATCHFOUND=0
  for ONEEXPTABLE in ${EXPORTTABLES}; do
    if [[ ${ONETABLE} == ${ONEEXPTABLE} ]]; then
#      echo "MATCH: ${ONETABLE}"
      MATCHFOUND=$((MATCHFOUND+1))
    fi
#  echo ${MATCHFOUND}
  done
  if [[ ${MATCHFOUND} -eq 1 ]]; then
    echo "OK: $ONETABLE - $MATCHFOUND"
  else
    echo "MISSING: $ONETABLE - $MATCHFOUND"
  fi
  MATCHFOUND=0
done
#if [[ $EXPORTTABLES == *"Evidence"* ]]; then
#  echo "FOUND"
#else
#  echo "NOT FOUND"
#fi



#echo ${TABLELIST}