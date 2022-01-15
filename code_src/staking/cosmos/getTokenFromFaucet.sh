#!/bin/bash
address=$1
$'{"address":\'\$address\'"}'
curl -X POST -d '{"address": "'$address'"}' https://faucet.testnet.cosmos.network