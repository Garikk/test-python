import sys
import psycopg2
import os

try:
    psycopg2.connect(os.environ['DATABASE_URL'])
except psycopg2.OperationalError:
    sys.exit(-1)

sys.exit(0)
