#!/bin/sh
set -e

# MySQL env variables
MYSQL_HOST=${MYSQL_HOST:-db}
MYSQL_PORT=${MYSQL_PORT:-3306}
MYSQL_USER=${MYSQL_USER:-driverslicence}
MYSQL_PASSWORD=${MYSQL_PASSWORD:-DriversLicence88}
MYSQL_DATABASE=${MYSQL_DATABASE:-driverslicence}

# Wait for MySQL to be ready
echo "Waiting for MySQL at ${MYSQL_HOST}:${MYSQL_PORT} ..."
MAX_ATTEMPTS=60
attempt=1
until python - <<PY
import sys, os, pymysql
host=os.environ.get("MYSQL_HOST","db")
port=int(os.environ.get("MYSQL_PORT","3306"))
user=os.environ.get("MYSQL_USER")
passwd=os.environ.get("MYSQL_PASSWORD")
db=os.environ.get("MYSQL_DATABASE")
try:
    conn = pymysql.connect(host=host, port=port, user=user, password=passwd, database=db)
    conn.close()
    sys.exit(0)
except Exception as e:
    sys.stderr.write(str(e))
    sys.exit(1)
PY
do
  if [ $attempt -ge $MAX_ATTEMPTS ]; then
    echo "Timed out waiting for MySQL after $attempt attempts"
    exit 1
  fi
  attempt=$((attempt+1))
  printf '.'
  sleep 1
done

echo "MySQL is reachable."

# Check if DB already has tables
TABLE_COUNT=$(python - <<PY
import sys, os, pymysql
host = os.environ.get("MYSQL_HOST","db")
port = int(os.environ.get("MYSQL_PORT","3306"))
user = os.environ.get("MYSQL_USER")
passwd = os.environ.get("MYSQL_PASSWORD")
db = os.environ.get("MYSQL_DATABASE")
try:
    conn = pymysql.connect(host=host, port=port, user=user, password=passwd)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema=%s", (db,))
    res = cur.fetchone()
    conn.close()
    print(res[0] if res else 0)
except Exception as e:
    sys.stderr.write("ERROR_CHECKING_TABLES: " + str(e))
    sys.exit(2)
PY
)

if [ -z "$TABLE_COUNT" ] || [ "$TABLE_COUNT" -eq 0 ]; then
  echo "DB empty, running init_db and populate_db..."
  export FLASK_APP=app:flask_app
  flask init_db
  flask populate_db
  echo "DB initialized."
else
  echo "DB already initialized, skipping init."
fi

exec "$@"
