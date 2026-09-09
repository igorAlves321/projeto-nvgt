import json, os, collections

d = json.load(open('.wf/result.json', encoding='utf-8'))

known = set()
for root in ('server', 'cliente'):
    for dp, dn, fn in os.walk(root):
        for n in fn:
            if n.endswith('.nvgt'):
                known.add(os.path.join(dp, n).replace(os.sep, '/'))

groups = collections.defaultdict(list)
unmatched = []
for s in d['systems']:
    for it in s['integration']:
        hits = [k for k in known if k in it]
        if hits:
            groups[max(hits, key=len)].append({'sistema': s['key'], 'instrucao': it})
        else:
            unmatched.append({'sistema': s['key'], 'instrucao': it})

json.dump({'groups': groups, 'unmatched': unmatched},
          open('.wf/integration.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

print('arquivos alvo:', len(groups),
      '| itens agrupados:', sum(len(v) for v in groups.values()),
      '| sem alvo:', len(unmatched))
for f, v in sorted(groups.items(), key=lambda x: -len(x[1])):
    print('  %-46s %3d' % (f, len(v)))
