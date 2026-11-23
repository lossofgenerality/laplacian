import sys, json
sys.path.insert(0, '/home/claude/laplacian/tools/manual')
import spec_lab as S
from build_manual import build
from hand_lab import HAND
res = {}
for t in ['L1', 'L2', 'L3']:
    ids = json.load(open(f'/tmp/verify_{t}.json', encoding='utf-8'))
    lines = [l for l in open(f'/tmp/out/{t}.txt', encoding='utf-8').read().split('\n') if l.strip()]
    assert len(ids) == len(lines), t
    for i, l in zip(ids, lines): res[i] = l.split(' | ', 1)[1]
json.dump(res, open('outputs_lab.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print(build(S, S.SOURCES, res, {'stepscol': 'img/stepscol.png'}, '/home/claude/laplacian-lab/manual.html', 'CCN', HAND))
