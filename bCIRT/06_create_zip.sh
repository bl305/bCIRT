#!/bin/bash
echo "Backup file name (without .zip):"
read zipfile
zip -r /home/bali/CloudBackup/GoogleShare/Backup_Sync/Programming/$zipfile.zip ./*
