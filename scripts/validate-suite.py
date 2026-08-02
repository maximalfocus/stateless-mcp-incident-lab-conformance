from pathlib import Path
import json,re,sys
root=Path('/Users/focus/personal/stateless-mcp-incident-lab-conformance')
conf=root/'conformance'; errors=[]; warns=[]; ids={}; tests=[]
allowed={'cli','http','http-html','function','property','component','interaction','metric-assertion','lint-assertion','http-contract','decision-record','workflow-assertion','state-machine','story','e2e','cross-browser-assertion','contract','structural-contract','documentation-contract','packaging-contract','cross-language-contract','transactional','signal-reactivity','reactive-form','graphql','grpc','message','websocket','sse','sql','accessibility','prompt-eval','tool-call','trace-span','webhook','visual-regression','i18n'}
for p in sorted(conf.rglob('test.json')):
  tests.append(p); rel=p.parent.relative_to(root)
  try: t=json.loads(p.read_text())
  except Exception as e: errors.append(f'{rel}: invalid test.json: {e}'); continue
  sid=t.get('spec_id');
  if not isinstance(sid,str) or not re.fullmatch(r'[A-Z]+-[0-9]{3}',sid): errors.append(f'{rel}: invalid spec_id {sid!r}')
  elif sid in ids: errors.append(f'{rel}: duplicate {sid} also {ids[sid]}')
  else: ids[sid]=rel
  for k in ('description','description_bdd','boundary','normalisation','source','consumers','providers','context'):
    if k not in t: errors.append(f'{sid}: missing {k}')
  if t.get('boundary') not in allowed: errors.append(f'{sid}: invalid boundary')
  for f in p.parent.glob('*.json'):
    try: json.loads(f.read_text())
    except Exception as e: errors.append(f'{f.relative_to(root)} invalid JSON: {e}')
  if not (p.parent/'expected.json').exists() and not (p.parent/'expected-exit.txt').exists(): errors.append(f'{sid}: no expected')
  if t.get('boundary') in ('http','tool-call','sse','trace-span'):
    for f in ('seed.json','request.json'):
      if not (p.parent/f).exists(): errors.append(f'{sid}: missing {f}')
  if t.get('boundary')=='function' and not (p.parent/'input.json').exists(): errors.append(f'{sid}: function missing input')
  if t.get('boundary')=='property':
    prop=t.get('property',{})
    for k in ('kind','target','domain','iterations','examples'):
      if k not in prop: errors.append(f'{sid}: property missing {k}')
    if prop.get('kind')=='round_trip' and 'inverse' not in prop: errors.append(f'{sid}: round_trip missing inverse')
    if prop.get('kind')=='ordering' and 'key' not in prop: errors.append(f'{sid}: ordering missing key')
    if prop.get('kind')=='bounds' and not {'min','max'} <= prop.keys(): errors.append(f'{sid}: bounds missing min/max')
  if sid and sid.startswith('ARCH-'):
    if t.get('adr')!='ADR-0001' or t.get('adr_repo')!='maximalfocus/stateless-mcp-incident-lab-architecture': errors.append(f'{sid}: bad architecture citation')
  txt='\n'.join(x.read_text() for x in p.parent.glob('*.json'))
  if 'scenario/run' in txt: errors.append(f'{sid}: fixture targets harness pseudo-RPC rather than public boundary')
  if '"..."' in txt: errors.append(f'{sid}: invalid ellipsis placeholder')
if len(tests)!=197: errors.append(f'test count {len(tests)} != 197')
expected_cats={'protocol','versioning','transport','discovery','primitives','incidents','mrtr','streaming','cache','cli','interoperability','properties','security','observability','performance','architecture','infra','cicd','dependencies'}
cats={p.relative_to(conf).parts[0] for p in tests}
if cats!=expected_cats: errors.append(f'categories mismatch {cats^expected_cats}')
for sub in ('dependencies','boundaries'):
  if not any((conf/'architecture'/sub).rglob('test.json')): errors.append(f'architecture/{sub} empty')
# Every expected contract assertion must carry the exact authoritative test description.
for p in tests:
  t=json.loads(p.read_text()); e=json.loads((p.parent/'expected.json').read_text())
  if t.get('boundary')!='property':
    contracts=[a for a in e.get('assertions',[]) if a.get('type')=='contract']
    if not t['spec_id'].startswith('ARCH-') and (len(contracts)!=1 or contracts[0].get('must')!=t['description']): errors.append(f"{t['spec_id']}: expected contract/description drift")
print(f'{len(tests)} tests, {len(cats)} categories, {len(ids)} unique spec IDs')
if errors:
  print('\n'.join('ERROR '+x for x in errors)); sys.exit(1)
print('PASS recursive structure, JSON, metadata, fixture, placeholder, property, architecture, and cross-file contract checks')
