#!/bin/bash

# before tests:
docker exec -it wrbmj-db-1 \
        psql -U postgres \
        -c "CREATE DATABASE test_database;"

pytest . -s --lf

# after tests:
docker exec -it wrbmj-db-1 \
        psql -U postgres \
        -c "DROP DATABASE test_database;"
