#!/bin/bash

USER="dmikes"
HOST="ssh.eu.pythonanywhere.com"
REMOTE_DIR="~/wish/"
WSGI_FILE="/var/www/dmikes_eu_pythonanywhere_com_wsgi.py"

exclude_patterns=(
    '__pycache__'
    '.git'
    '*.pyc'
    '.env'
    'venv/'
    '.vscode'
    '*.log'
    'instance/'
    '*.sqlite3'
    'node_modules'
    '.DS_Store'
    '*.tmp'
)

rsync_cmd=("rsync" "-avz")
for pattern in "${exclude_patterns[@]}"; do
    rsync_cmd+=("--exclude=$pattern")
done

rsync_cmd+=("./" "${USER}@${HOST}:${REMOTE_DIR}")

echo "🔄 Syncing files to PythonAnywhere ..."
"${rsync_cmd[@]}"

echo "🚀 Reloading web application ..."
ssh "${USER}@${HOST}" "touch ${WSGI_FILE}"

echo "✅ Deployment completed successfully!"
