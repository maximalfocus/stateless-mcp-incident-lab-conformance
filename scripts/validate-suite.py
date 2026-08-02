from pathlib import Path
import json,re,sys
root=Path(__file__).resolve().parents[1]
conf=root/'conformance'; errors=[]; warns=[]; ids={}; tests=[]
context_map=json.loads((root/'context-map.json').read_text())
valid_contexts={x['name'] for x in context_map['contexts']}
declared_placeholders=set(json.loads((root/'suite-invariants.json').read_text())['placeholders'])
allowed={'cli','http','http-html','function','property','component','interaction','metric-assertion','lint-assertion','http-contract','decision-record','workflow-assertion','state-machine','story','e2e','cross-browser-assertion','contract','structural-contract','documentation-contract','packaging-contract','cross-language-contract','transactional','signal-reactivity','reactive-form','graphql','grpc','message','websocket','sse','sql','accessibility','prompt-eval','tool-call','trace-span','webhook','visual-regression','i18n'}
for p in sorted(conf.rglob('test.json')):
  tests.append(p); rel=p.parent.relative_to(root)
  try: t=json.loads(p.read_text())
  except Exception as e: errors.append(f'{rel}: invalid test.json: {e}'); continue
  sid=t.get('spec_id');
  if not isinstance(sid,str) or not re.fullmatch(r'[A-Z]+-[0-9]{3}',sid): errors.append(f'{rel}: invalid spec_id {sid!r}')
  elif sid in ids: errors.append(f'{rel}: duplicate {sid} also {ids[sid]}')
  else: ids[sid]=rel
  for k in ('description','description_bdd','boundary','normalisation','source','consumers','providers','context','source_deps'):
    if k not in t: errors.append(f'{sid}: missing {k}')
  if t.get('boundary') not in allowed: errors.append(f'{sid}: invalid boundary')
  if t.get('context') not in valid_contexts: errors.append(f"{sid}: context {t.get('context')!r} absent from context-map.json")
  if not isinstance(t.get('source_deps'),list) or not t.get('source_deps'): errors.append(f'{sid}: source_deps must be a non-empty list')
  for f in p.parent.glob('*.json'):
    try: json.loads(f.read_text())
    except Exception as e: errors.append(f'{f.relative_to(root)} invalid JSON: {e}')
  if not (p.parent/'expected.json').exists() and not (p.parent/'expected-exit.txt').exists(): errors.append(f'{sid}: no expected')
  if t.get('boundary') in ('http','tool-call','sse','trace-span'):
    for f in ('seed.json','request.json'):
      if not (p.parent/f).exists(): errors.append(f'{sid}: missing {f}')
    request_path=p.parent/'request.json'
    if request_path.exists():
      request=json.loads(request_path.read_text())
      body=request.get('body',{}) if isinstance(request,dict) else {}
      params=body.get('params',{}) if isinstance(body,dict) else {}
      if isinstance(params,dict) and 'scenario' in params: errors.append(f'{sid}: request relies on runner-only params.scenario')
      headers=request.get('headers',{}) if isinstance(request,dict) else {}
      input_path=p.parent/'input.json'
      input_data=json.loads(input_path.read_text()) if input_path.exists() else {}
      intentional_violation=isinstance(input_data,dict) and input_data.get('intentional_request_violation') is True
      if isinstance(body,dict) and body.get('method')!='healthz' and headers.get('Mcp-Method')!=body.get('method') and not intentional_violation: errors.append(f'{sid}: Mcp-Method/body method mismatch')
  if t.get('boundary')=='function' and not (p.parent/'input.json').exists(): errors.append(f'{sid}: function missing input')
  input_path=p.parent/'input.json'
  if input_path.exists():
    input_data=json.loads(input_path.read_text())
    if isinstance(input_data,dict) and set(input_data)<= {'scenario','contract','protocol_version','providers'}: errors.append(f'{sid}: input is descriptive metadata, not replayable fixture data')
    if t.get('boundary')=='cli' and 'argv' not in input_data: errors.append(f'{sid}: CLI fixture missing argv')
  if t.get('boundary')=='property':
    prop=t.get('property',{})
    for k in ('kind','target','domain','iterations','examples'):
      if k not in prop: errors.append(f'{sid}: property missing {k}')
    if prop.get('kind')=='round_trip' and 'inverse' not in prop: errors.append(f'{sid}: round_trip missing inverse')
    if prop.get('kind')=='ordering' and 'key' not in prop: errors.append(f'{sid}: ordering missing key')
    if prop.get('kind')=='bounds' and not {'min','max'} <= prop.keys(): errors.append(f'{sid}: bounds missing min/max')
    examples=prop.get('examples',[])
    if isinstance(examples,list) and len(examples)==4 and examples[1:]==['empty','unicode','boundary']: errors.append(f'{sid}: property examples are labels, not concrete regression inputs')
  if sid and sid.startswith('ARCH-'):
    if t.get('adr')!='ADR-0001' or t.get('adr_repo')!='maximalfocus/stateless-mcp-incident-lab-architecture': errors.append(f'{sid}: bad architecture citation')
  txt='\n'.join(x.read_text() for x in p.parent.glob('*.json'))
  if 'scenario/run' in txt: errors.append(f'{sid}: fixture targets harness pseudo-RPC rather than public boundary')
  if '"..."' in txt: errors.append(f'{sid}: invalid ellipsis placeholder')
  unknown_placeholders=set(re.findall(r'\{\{[A-Z_]+\}\}',txt))-declared_placeholders
  if unknown_placeholders: errors.append(f'{sid}: undeclared placeholders {sorted(unknown_placeholders)}')
if len(tests)!=197: errors.append(f'test count {len(tests)} != 197')
expected_cats={'protocol','versioning','transport','discovery','primitives','incidents','mrtr','streaming','cache','cli','interoperability','properties','security','observability','performance','architecture','infra','cicd','dependencies'}
cats={p.relative_to(conf).parts[0] for p in tests}
if cats!=expected_cats: errors.append(f'categories mismatch {cats^expected_cats}')
for sub in ('dependencies','boundaries'):
  if not any((conf/'architecture'/sub).rglob('test.json')): errors.append(f'architecture/{sub} empty')
# Disk ⇔ coverage bijection: coverage must enumerate each ID individually.
coverage=(root/'coverage-tracking.md').read_text()
doc_ids=re.findall(r'`([A-Z]+-[0-9]{3})`',coverage)
if len(doc_ids)!=len(set(doc_ids)): errors.append('coverage-tracking.md contains duplicate spec IDs')
if set(doc_ids)!=set(ids):
  errors.append(f'coverage bijection mismatch: disk-only={sorted(set(ids)-set(doc_ids))}, doc-only={sorted(set(doc_ids)-set(ids))}')
if '197/197 planned test directories structurally present' not in coverage: errors.append('coverage summary count is stale')
# WORKITEM closure, sizing, and ordered acyclic DAG.
wi=(root/'WORKITEMS.md').read_text()
wi_ids=re.findall(r'\*\*(WI-[0-9]{3})\*\*',wi)
wi_deps=re.findall(r'Depends on: (WI-[0-9]{3}|none)',wi)
wi_counts=list(map(int,re.findall(r'\(([0-9]+) tests\)',wi)))
wi_paths=re.findall(r'`(conformance/[^`]+)`',wi)
expected_paths={str(p.parent.relative_to(root)) for p in tests}
if len(wi_ids)!=len(set(wi_ids)) or len(wi_ids)!=len(wi_deps): errors.append('WORKITEM IDs/dependencies malformed')
if wi_counts and (min(wi_counts)<2 or max(wi_counts)>5 or sum(wi_counts)!=len(tests)): errors.append('WORKITEM sizing/count invalid')
if set(wi_paths)!=expected_paths or len(wi_paths)!=len(set(wi_paths)): errors.append('WORKITEM test-path bijection invalid')
for i,dep in enumerate(wi_deps):
  want='none' if i==0 else wi_ids[i-1]
  if dep!=want: errors.append(f'{wi_ids[i]} dependency {dep} != ordered predecessor {want}')
# Agent wrapper leakage in shipped artifacts.
for p in root.rglob('*'):
  if '.git' in p.parts or not p.is_file() or p.suffix not in ('.md','.json','.yaml','.yml'): continue
  if re.search(r'^\s*</(?:content|invoke|parameter)>\s*$',p.read_text(errors='ignore'),re.M): errors.append(f'{p.relative_to(root)} leaked agent wrapper tag')
# Every expected contract assertion must carry the exact authoritative test description.
for p in tests:
  t=json.loads(p.read_text())
  expected_path=p.parent/'expected.json'
  if not expected_path.exists(): continue
  e=json.loads(expected_path.read_text())
  if not isinstance(e,dict) or not e: errors.append(f"{t['spec_id']}: expected.json must be a non-empty object")
  if t.get('boundary')!='property':
    assertions=e.get('assertions',[])
    known_assertions={'no_import','no_deep_import','strict_http_shape','contract'}
    unknown=[a.get('type') for a in assertions if a.get('type') not in known_assertions]
    if unknown: errors.append(f"{t['spec_id']}: unknown assertion types {unknown}")
    contracts=[a for a in assertions if a.get('type')=='contract']
    if contracts: errors.append(f"{t['spec_id']}: prose-only contract assertion is not executable")
    if any(a.get('type')=='strict_http_shape' for a in assertions) and not {'status','headers','body'} <= e.keys(): errors.append(f"{t['spec_id']}: strict_http_shape has no complete status/headers/body expectation")
    if t.get('boundary')=='state-machine' and not {'states','transitions'} <= e.keys(): errors.append(f"{t['spec_id']}: state-machine expected lacks states/transitions")
print(f'{len(tests)} tests, {len(cats)} categories, {len(ids)} unique spec IDs')
if errors:
  print('\n'.join('ERROR '+x for x in errors)); sys.exit(1)
print('PASS recursive structure, JSON, metadata, fixture, placeholder, property, architecture, and cross-file contract checks')
