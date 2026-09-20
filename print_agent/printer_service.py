import time
from cups_service import print_pdf,wait_for_completion

def print_document(path,job,mode,printer_name,on_submitted):
    if mode=='simulation':on_submitted(-1);time.sleep(6);return
    if mode!='real':raise ValueError('AGENT_MODE must be simulation or real.')
    print_pdf(path,job,printer_name,on_submitted)
