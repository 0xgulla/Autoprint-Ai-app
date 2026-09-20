"""An authenticated polling agent with a persistent submission journal.
Never retries a physical submission automatically after an ambiguous crash.
"""
import logging,sqlite3,tempfile,time,json
from pathlib import Path
import requests
import config
from printer_service import print_document
from cups_service import wait_for_completion
logging.basicConfig(level=logging.INFO,format='%(asctime)s %(levelname)s %(message)s')
client=requests.Session();client.headers['Authorization']='Bearer '+config.TOKEN

def call(path,data=None):
    r=client.request('POST' if data is not None else 'GET',config.API_URL+'/api/print-agent'+path,json=data,timeout=30);r.raise_for_status();return r

def status(id,value):
    for attempt in range(5):
        try:return call('/jobs/'+id+'/status',{'status':value})
        except requests.RequestException:
            if attempt==4:raise
            time.sleep(2+attempt)

def run():
    if not config.TOKEN:raise RuntimeError('PRINT_AGENT_TOKEN is required. Set the same token on the Flask backend.')
    config.JOURNAL.parent.mkdir(parents=True,exist_ok=True)
    db=sqlite3.connect(config.JOURNAL)
    db.execute('CREATE TABLE IF NOT EXISTS jobs(id TEXT PRIMARY KEY,state TEXT,cups_id INTEGER)');db.commit()
    for id,state,cups_id in db.execute("SELECT id,state,cups_id FROM jobs WHERE state NOT IN ('completed','failed')").fetchall():
        logging.warning('Recovering %s without resubmitting it.',id)
        try:
            if state=='submitted' and cups_id and cups_id>0:wait_for_completion(cups_id);status(id,'completed');db.execute("UPDATE jobs SET state='completed' WHERE id=?",(id,))
            else:status(id,'failed');db.execute("UPDATE jobs SET state='failed' WHERE id=?",(id,))
            db.commit()
        except Exception:logging.exception('Recovery requires operator attention');return
    while True:
        try:
            job=call('/jobs/next',{'printer_id':config.PRINTER_ID}).json().get('job')
            if not job:time.sleep(3);continue
            id=job['id']
            if job['payment_status']!='Verified' or job.get('seed'):raise RuntimeError('Refusing an unauthorized job.')
            previous=db.execute('SELECT state FROM jobs WHERE id=?',(id,)).fetchone()
            if previous:logging.warning('Refusing to resubmit previously processed job %s. Create a new order.',id);status(id,'failed');continue
            db.execute('INSERT INTO jobs VALUES(?,?,NULL)',(id,'claimed'));db.commit()
            try:
                data=call('/jobs/'+id+'/document').content
                if len(data)>10*1024*1024 or not data.startswith(b'%PDF-'):raise RuntimeError('Invalid document received.')
                with tempfile.TemporaryDirectory(prefix='autoprint-') as temp:
                    file=Path(temp)/'document.pdf';file.write_bytes(data)
                    def submitted(cups_id):
                        db.execute('UPDATE jobs SET state=?,cups_id=? WHERE id=?',('submitted',cups_id,id));db.commit();status(id,'printing')
                    print_document(file,job,config.MODE,config.PRINTER_NAME,submitted)
                status(id,'completed');db.execute('UPDATE jobs SET state=? WHERE id=?',('completed',id));db.commit();logging.info('Completed %s',id)
            except Exception:
                logging.exception('Job failed; physical submissions will not be repeated automatically')
                try:status(id,'failed')
                except requests.RequestException:logging.exception('Could not report failure. Reconcile the controller before restarting.');return
                db.execute('UPDATE jobs SET state=? WHERE id=?',('failed',id));db.commit()
        except requests.RequestException:logging.warning('Backend unavailable; retrying shortly.');time.sleep(5)
        except KeyboardInterrupt:return
if __name__=='__main__':run()
