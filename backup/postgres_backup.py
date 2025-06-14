import os
import subprocess
from backup.config import POSTGRES_CONF, BACKUP_BASE_DIR, TIMESTAMP

def backup_postgres():
    folder = os.path.join(BACKUP_BASE_DIR, 'postgresql', TIMESTAMP)
    os.makedirs(folder, exist_ok=True)

    os.environ['PGPASSWORD'] = POSTGRES_CONF['password']

    dump_file = os.path.join(folder, 'schema_backup.sql')
    cmd = [
        "pg_dump",
        "-h", POSTGRES_CONF["host"],
        "-p", str(POSTGRES_CONF["port"]),
        "-U", POSTGRES_CONF["user"],
        "-d", POSTGRES_CONF["db"],
        "--schema", POSTGRES_CONF["schema"],
        "-f", dump_file
    ]

    try:
        result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return dump_file
    except subprocess.CalledProcessError as e:
        print("❌ pg_dump failed with the following error:")
        print(f"Command: {' '.join(cmd)}")
        print(f"stderr: {e.stderr.decode().strip()}")
        raise
