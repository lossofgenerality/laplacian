import sys; sys.path.insert(0,'.')
import curvature_lab as m
sec=int(sys.argv[1]); idx=[int(x) for x in sys.argv[2].split(',')]; keys=sys.argv[3].split(',') if len(sys.argv)>3 and sys.argv[3] else []
secs,cur={},None
for s,t in m.CELLS:
    if s=='Section': cur=int(t.split('.')[0]); secs[cur]=[]
    elif s=='Input' and cur is not None: secs[cur].append(t)
tail=sys.argv[4] if len(sys.argv)>4 else ''
code='\n'.join([m.page_data(keys) if keys else '', m.HELPERS]+[secs[sec][i-1] for i in idx])+'\n'+tail
open('/tmp/dbg.wl','w').write(code)
