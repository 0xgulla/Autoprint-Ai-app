from pathlib import Path
from dotenv import load_dotenv
import os,secrets
ROOT=Path(__file__).resolve().parent
load_dotenv(ROOT.parent/'.env')
DATA=Path(os.getenv('DATA_DIR',str(ROOT/'data')));DATA.mkdir(parents=True,exist_ok=True)
UPLOADS=DATA/'uploads';UPLOADS.mkdir(exist_ok=True)
secret_file=DATA/'session-secret'
if not secret_file.exists():secret_file.write_text(secrets.token_hex(32))
SECRET_KEY=os.getenv('SECRET_KEY') or secret_file.read_text()
DB_PATH=str(DATA/'autoprint.sqlite3')
DEMO_MODE=os.getenv('DEMO_MODE','true').lower()=='true'
SIMULATION=os.getenv('PRINT_MODE','simulation')=='simulation'
AGENT_TOKEN=os.getenv('PRINT_AGENT_TOKEN','')
ADMIN_TOKEN=os.getenv('ADMIN_TOKEN','')
