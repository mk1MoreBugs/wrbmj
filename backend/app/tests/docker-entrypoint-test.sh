#!/bin/bash
set -e

export PGPASSWORD=$(cat /run/secrets/postgres_password)

cleanup() {
    # after tests:
    psql -h db -U $POSTGRES_USER \
        -c "DROP DATABASE IF EXISTS test_database;"
}

trap cleanup EXIT INT TERM

# before tests:
psql -h db -U $POSTGRES_USER \
    -c "CREATE DATABASE test_database;"

pytest . # --lf -s
