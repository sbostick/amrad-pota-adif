#!/usr/bin/env bash
set -eu -o pipefail

QRZ_USER=$(pass qrz.com/KO6BGT.json | jq -r .username)
QRZ_PASS=$(pass qrz.com/KO6BGT.json | jq -r .password)
QRZ_ENDPOINT="https://xmldata.qrz.com/xml/current"
AGENT=ko6bgt
export QRZ_USER QRZ_PASS QRZ_ENDPOINT AGENT

curl -s "${QRZ_ENDPOINT}/?username=${QRZ_USER};password=${QRZ_PASS};agent=${AGENT}" \
    > /tmp/qrz-result.xml

QRZ_SESSION_KEY=$(grep '<Key>' /tmp/qrz-result.xml | sed -E 's#</?Key>##g;')
export QRZ_SESSION_KEY

echo "---"; curl "${QRZ_ENDPOINT}/?s=${QRZ_SESSION_KEY};callsign=aa7bq"
echo "---"; curl "${QRZ_ENDPOINT}/?s=${QRZ_SESSION_KEY};callsign=ko6bgt"
