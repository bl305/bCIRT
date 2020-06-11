#!/bin/bash
./01_clean_migrations.sh
./02_clean_media_files.sh
./03_clean_pycache_files.sh
./04_clean_db.sh
mkdir -p ./media/tmp
