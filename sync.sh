#!/bin/bash

USER="dmikes"
HOST="ssh.eu.pythonanywhere.com"
REMOTE_DIR="~/wish/"
WSGI_FILE="/var/www/dmikes_eu_pythonanywhere_com_wsgi.py"

exclude_patterns=(
    'instance/'
    'node_modules/'
    '.DS_Store'
    '.venv/'
    '.vscode/'
    '__pycache__'
    # '.env'
    '.git'
    '*.log'
    '*.pyc'
    '*.sqlite3'
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
