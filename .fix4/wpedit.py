import sys, json, os, time
sys.path.insert(0,'scripts'); import deploy as d
LIVE = '--live' in sys.argv
EDITS = {
 ('posts',439): [("For physicians, check the state medical board.","For other clinicians, check the state medical board.")],
 ('posts',524): [("No insurance navigating, no networks, no denied claims.","No plan paperwork, no networks, no denied claims.")],
 ('posts',305): [("Cost with insurance:","Cost with a health plan:"),("Cost without insurance:","Self-pay cost:"),
                 ("No insurance needed, no copay","Self-pay, no copay"),("(or $200+ without insurance)","(or $200+ self-pay)"),
                 ("No app, no account, no insurance needed.","No app, no account. Self-pay.")],
 ('pages',317): [("We do not bill insurance.","We do not bill third-party payers; every visit is self-pay.")],
}
env=d.load_env(); auth=d.wp_auth(env)
bdir=os.path.expanduser('~/Desktop/Chris-HQ/content-output/deploy-backups/2026-10-10/wp-content'); os.makedirs(bdir,exist_ok=True)
for (t,i),reps in EDITS.items():
    base=f"{d.SITE}/wp-json/wp/v2/{t}/{i}"
    st,cur=d.wp_req(base+"?context=edit&_fields=id,slug,link,content,modified",auth)
    if st!=200 or not cur: print(t,i,'GET failed',st); continue
    raw=cur['content']['raw']; new=raw; counts=[]
    for a,b in reps:
        c=new.count(a); counts.append(c); new=new.replace(a,b)
    print(t,i,cur['slug'],'match counts',counts)
    if not LIVE: continue
    if 0 in counts: print('  SKIP: a phrase not found in raw content'); continue
    bk=f"{bdir}/{t}-{i}-{time.strftime('%Y%m%d-%H%M%S')}.json"
    json.dump(cur,open(bk,'w')); print('  backup',bk)
    st2,res=d.wp_req(base,auth,method="POST",body={"content":new})
    print('  update',st2, 'ok' if st2==200 and res and res['content']['raw']==new else 'MISMATCH')
