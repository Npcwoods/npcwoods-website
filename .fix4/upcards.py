import sys, os
sys.path.insert(0, 'scripts')
import deploy as d
env = d.load_env()
sftp, transport = d.sftp_connect(env)
d.sftp_mkdirs(sftp, 'html/assets/img/share')
n=0
for f in sorted(os.listdir('.fix4/ship/share')):
    rem='html/assets/img/share/'+f
    sftp.put('.fix4/ship/share/'+f, rem)
    assert sftp.stat(rem).st_size==os.path.getsize('.fix4/ship/share/'+f); n+=1
print('uploaded',n)
sftp.close(); transport.close()
