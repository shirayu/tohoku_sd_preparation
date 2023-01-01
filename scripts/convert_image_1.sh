#!/usr/bin/env bash

if [ "$1" == "" ]; then
    exit 1
fi
if [ "$2" == "" ]; then
    exit 1
fi
if [ "$3" == "" ]; then
    exit 1
fi

OUTDIR="$2/$(basename "$(dirname "$1")")"
mkdir -p "${OUTDIR}"
OUTNAME="${OUTDIR}/$(basename $1)"

convert -fuzz 5% -trim -resize "$3" -gravity center -extent "$3" "$1" "${OUTNAME}"
