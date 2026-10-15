import sys, os
sys.path.insert(0, 'scripts')
import deploy as d
env = d.load_env()
sftp, transport = d.sftp_connect(env)
for p in ['landing-pages/medications/amoxicillin','landing-pages/uti-treatment']:
    rem=f'html/{p}/index.html'; loc=f'.fix4/ship/pages/{p}/index.html'
    bk=d.sftp_backup(sftp, rem); print('backup', bk)
    sftp.put(loc, rem); assert sftp.stat(rem).st_size==os.path.getsize(loc); print('up', rem)
sftp.close(); transport.close()
