import sys, os, difflib
sys.path.insert(0,'scripts'); import deploy as d
env=d.load_env(); sftp,t=d.sftp_connect(env)
for p in open('.fix4/manifest2.txt').read().split():
    os.makedirs(f'.fix4/srv/{p}',exist_ok=True); sftp.get(f'html/{p}/index.html',f'.fix4/srv/{p}/index.html')
    a=open(f'.fix4/srv/{p}/index.html').read().splitlines(); b=open(f'.fix4/edit2/{p}/index.html').read().splitlines()
    diff=[l for l in difflib.unified_diff(a,b,n=0,lineterm='') if l[:1] in '+-' and not l.startswith(('+++','---'))]
    print(p,'diff lines vs server:',len(diff))
    for l in diff: print('   ',l[:150])
sftp.close(); t.close()
