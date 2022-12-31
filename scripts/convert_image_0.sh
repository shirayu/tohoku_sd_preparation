#!/usr/bin/env bash

if [ "$1" == "" ]; then
    exit 1
fi
if [ "$2" == "" ]; then
    exit 1
fi

OUTDIR="$2/$(dirname $1)"
mkdir -p "${OUTDIR}"
OUTNAME="$2/$1"

PROC=1
MAXSIZE=2048
MAX_MEMORY="20480MB"

# Only minimize (not enlarge)

convert -limit memory ${MAX_MEMORY} -background white -alpha remove -alpha off -fuzz 5% -trim -resize ${MAXSIZE}x${MAXSIZE}^ -gravity center "$1" "${OUTNAME}"
# -extent ${MAXSIZE}x${MAXSIZE}
