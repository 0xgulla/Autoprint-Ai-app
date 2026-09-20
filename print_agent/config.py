from pathlib import Path
from dotenv import load_dotenv
import os
load_dotenv(Path(__file__).resolve().parent.parent/'.env')
API_URL=os.getenv('AGENT_API_URL','http://127.0.0.1:5000').rstrip('/')
TOKEN=os.getenv('PRINT_AGENT_TOKEN','')
PRINTER_ID=os.getenv('PRINT_AGENT_PRINTER_ID','pi-01')
PRINTER_NAME=os.getenv('CUPS_PRINTER_NAME','')
MODE=os.getenv('AGENT_MODE','simulation')
JOURNAL=Path(os.getenv('AGENT_JOURNAL',str(Path(__file__).resolve().parent/'agent-state.sqlite3')))
