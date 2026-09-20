"""Only this module talks to CUPS. Requires pycups on the Raspberry Pi."""
import time

def print_pdf(path,job,printer_name,on_submitted):
    if not printer_name:raise RuntimeError('Set CUPS_PRINTER_NAME to a local CUPS queue.')
    import cups
    conn=cups.Connection()
    if printer_name not in conn.getPrinters():raise RuntimeError('Configured CUPS printer was not found.')
    settings=job['settings']
    options={'copies':str(settings['copies']),'media':settings['paper'],'sides':'two-sided-long-edge' if settings['duplex'] else 'one-sided','number-up':str(settings['nup']),'print-color-mode':'monochrome' if settings['mode']=='bw' else 'color','Collate':'True'}
    if settings['orientation']!='auto':options['orientation-requested']='4' if settings['orientation']=='landscape' else '3'
    cups_id=conn.printFile(printer_name,str(path),job['id'],options)
    on_submitted(cups_id)
    wait_for_completion(cups_id)

def wait_for_completion(cups_id):
    import cups
    conn=cups.Connection();deadline=time.monotonic()+1800
    while time.monotonic()<deadline:
        info=conn.getJobAttributes(cups_id);state=info.get('job-state')
        if state==9:return
        if state in [7,8]:raise RuntimeError('CUPS reported a cancelled or aborted print job.')
        time.sleep(2)
    raise TimeoutError('CUPS did not confirm completion within 30 minutes. Check the printer before retrying.')
