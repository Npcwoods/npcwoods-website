import sys, os, stat
sys.path.insert(0, 'scripts')
import deploy as d
env = d.load_env()
sftp, transport = d.sftp_connect(env)
have=set(open('.fix4/pullpaths.txt').read().split())
SKIP={'wp-admin','wp-includes','wp-content','assets','.well-known','cgi-bin','node_modules','.git','fonts','img','images','css','js'}
found=[]
def walk(rel, depth):
    if depth>4: return
    try: ents=sftp.listdir_attr('html/'+rel if rel else 'html')
    except IOError: return
    for e in ents:
        if stat.S_ISDIR(e.st_mode):
            if e.filename in SKIP or e.filename.startswith('.'): continue
            walk((rel+'/' if rel else '')+e.filename, depth+1)
        elif e.filename=='index.html' and rel:
            found.append(rel)
walk('',0)
new=[p for p in found if p not in have]
print('total index.html',len(found),'new',len(new))
os.makedirs('.fix4/remote2',exist_ok=True)
for p in new:
    loc=f'.fix4/remote2/{p}/index.html'; os.makedirs(os.path.dirname(loc),exist_ok=True)
    sftp.get(f'html/{p}/index.html',loc)
print('downloaded',len(new))
sftp.close(); transport.close()
