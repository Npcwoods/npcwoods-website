import sys, os
sys.path.insert(0, 'scripts')
import deploy as d
env = d.load_env()
sftp, transport = d.sftp_connect(env)
out = '.fix4/remote'
got, miss = 0, []
for p in open('.fix4/pullpaths.txt').read().split():
    rem = f'html/{p}/index.html'
    loc = f'{out}/{p}/index.html'
    os.makedirs(os.path.dirname(loc), exist_ok=True)
    try:
        sftp.get(rem, loc); got += 1
    except IOError:
        miss.append(p)
print('got', got); print('missing', ' '.join(miss))
sftp.close(); transport.close()
