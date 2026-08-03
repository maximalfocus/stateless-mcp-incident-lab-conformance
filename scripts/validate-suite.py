from pathlib import Path
import json,re,sys
root=Path(__file__).resolve().parents[1]
conf=root/'conformance'; errors=[]; warns=[]; ids={}; tests=[]
context_map=json.loads((root/'context-map.json').read_text())
valid_contexts={x['name'] for x in context_map['contexts']}
declared_placeholders=set(json.loads((root/'suite-invariants.json').read_text())['placeholders'])
operation_registry=json.loads((root/'operation-registry.json').read_text())['registries']
used_registry_names={k:set() for k in operation_registry}
policy_registry=json.loads((root/'policy-registry.json').read_text())
used_policy_checks=set()
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
  consumers=t.get('consumers'); providers=t.get('providers')
  consumer_provider={'typescript-raw':'raw','typescript-sdk':'sdk'}
  if not isinstance(consumers,list) or not consumers or set(consumers)-set(consumer_provider): errors.append(f'{sid}: invalid consumers')
  elif providers!=[consumer_provider[x] for x in consumers]: errors.append(f'{sid}: providers must exactly mirror consumers in order')
  if not isinstance(t.get('source_deps'),list) or not t.get('source_deps'): errors.append(f'{sid}: source_deps must be a non-empty list')
  for f in p.parent.glob('*.json'):
    try: json.loads(f.read_text())
    except Exception as e: errors.append(f'{f.relative_to(root)} invalid JSON: {e}')
  if not (p.parent/'expected.json').exists(): errors.append(f'{sid}: no expected.json')
  if t.get('boundary')=='cli':
    input_path=p.parent/'input.json'; exit_path=p.parent/'expected-exit.txt'; expected_path=p.parent/'expected.json'
    if input_path.exists() and json.loads(input_path.read_text()).get('fixture')!='SEEDED-DETERMINISTIC-INCIDENT-LAB': errors.append(f'{sid}: CLI input must name deterministic fixture')
    if exit_path.exists() and expected_path.exists():
      try:
        if int(exit_path.read_text().strip()) != json.loads(expected_path.read_text()).get('exit_code'): errors.append(f'{sid}: expected-exit.txt disagrees with expected.json')
      except ValueError: errors.append(f'{sid}: expected-exit.txt is not an integer')
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
      body_meta=params.get('_meta',{}) if isinstance(params,dict) else {}
      body_version=body_meta.get('io.modelcontextprotocol/protocolVersion') if isinstance(body_meta,dict) else None
      if body_version is not None and headers.get('MCP-Protocol-Version')!=body_version and not intentional_violation: errors.append(f'{sid}: MCP-Protocol-Version/body version mismatch')
      if isinstance(body,dict) and body.get('method') in ('tools/call','resources/read','prompts/get'):
        mirrored_name=params.get('name') or params.get('uri')
        header_name=headers.get('Mcp-Name')
        if isinstance(mirrored_name,str) and header_name!=mirrored_name and not intentional_violation: errors.append(f'{sid}: Mcp-Name/body name mismatch')
        arguments=params.get('arguments',{}) if isinstance(params,dict) else {}
        if params.get('name')=='query_telemetry' and isinstance(arguments,dict) and arguments.get('service') is not None:
          if headers.get('Mcp-Param-Service')!=arguments.get('service') and not intentional_violation: errors.append(f'{sid}: Mcp-Param-Service/body argument mismatch')
  if t.get('boundary')=='function' and not (p.parent/'input.json').exists(): errors.append(f'{sid}: function missing input')
  if t.get('boundary') not in ('http','tool-call','sse','trace-span'):
    dead=[name for name in ('request.json','seed.json') if (p.parent/name).exists()]
    if dead: errors.append(f'{sid}: non-executing boundary carries dead fixtures {dead}')
  input_path=p.parent/'input.json'
  if input_path.exists():
    input_data=json.loads(input_path.read_text())
    if isinstance(input_data,dict) and set(input_data)<= {'scenario','contract','protocol_version','providers'}: errors.append(f'{sid}: input is descriptive metadata, not replayable fixture data')
    if isinstance(input_data,dict) and 'state_fault' in input_data and input_data['state_fault'] not in {'tampered','expired','method_mismatch','arguments_mismatch'}: errors.append(f'{sid}: unknown state_fault')
    if isinstance(input_data,dict) and 'fixture' in input_data and input_data['fixture'] not in {'SEEDED-DETERMINISTIC-INCIDENT-LAB','fresh_process','accepted-remediation','adversarial-request'}: errors.append(f'{sid}: unknown fixture sentinel')
    if t.get('boundary')=='cli' and 'argv' not in input_data: errors.append(f'{sid}: CLI fixture missing argv')
    expected_path=p.parent/'expected.json'
    expected_data=json.loads(expected_path.read_text()) if expected_path.exists() else {}
    for key,registry_name in (('operation','operations'),('subject','subjects'),('profile','profiles')):
      name=input_data.get(key) if isinstance(input_data,dict) else None
      if name is None: continue
      registry=operation_registry[registry_name]
      if name not in registry: errors.append(f'{sid}: unknown {key} {name!r}'); continue
      used_registry_names[registry_name].add(name); contract=registry[name]
      if t.get('boundary') not in contract['boundaries']: errors.append(f'{sid}: {key} {name!r} does not allow boundary {t.get("boundary")!r}')
      missing_input=set(contract['input_required'])-set(input_data); unknown_input=set(input_data)-set(contract['input_allowed'])
      missing_expected=set(contract['expected_required'])-set(expected_data); unknown_expected=set(expected_data)-set(contract['expected_allowed'])
      if missing_input: errors.append(f'{sid}: {key} {name!r} missing input fields {sorted(missing_input)}')
      if unknown_input: errors.append(f'{sid}: {key} {name!r} unknown input fields {sorted(unknown_input)}')
      if missing_expected: errors.append(f'{sid}: {key} {name!r} missing expected fields {sorted(missing_expected)}')
      if unknown_expected: errors.append(f'{sid}: {key} {name!r} unknown expected fields {sorted(unknown_expected)}')
    checks=input_data.get('checks',[]) if isinstance(input_data,dict) else []
    if checks:
      if not isinstance(checks,list) or not all(isinstance(x,str) for x in checks): errors.append(f'{sid}: checks must be a string list')
      else:
        unknown_checks=set(checks)-set(policy_registry['checks'])
        if unknown_checks: errors.append(f'{sid}: unknown policy checks {sorted(unknown_checks)}')
        used_policy_checks.update(set(checks)-unknown_checks)
        if expected_data.get('evaluated_checks')!=checks: errors.append(f'{sid}: evaluated_checks must exactly equal input checks')
        for check in set(checks)-unknown_checks:
          if policy_registry['checks'][check]['source_spec_id']!=sid: errors.append(f'{sid}: policy check {check!r} belongs to another spec')
  if t.get('boundary')=='property':
    prop=t.get('property',{})
    for k in ('kind','target','domain','iterations','examples'):
      if k not in prop: errors.append(f'{sid}: property missing {k}')
    if prop.get('kind')=='round_trip' and 'inverse' not in prop: errors.append(f'{sid}: round_trip missing inverse')
    if prop.get('kind')=='ordering' and 'key' not in prop: errors.append(f'{sid}: ordering missing key')
    if prop.get('kind')=='bounds' and not {'min','max'} <= prop.keys(): errors.append(f'{sid}: bounds missing min/max')
    examples=prop.get('examples',[])
    if isinstance(examples,list) and len(examples)==4 and examples[1:]==['empty','unicode','boundary']: errors.append(f'{sid}: property examples are labels, not concrete regression inputs')
    target=prop.get('target'); registry=operation_registry['property_targets']
    if target not in registry: errors.append(f'{sid}: unknown property target {target!r}')
    else:
      used_registry_names['property_targets'].add(target)
      if prop.get('kind') not in registry[target]['kinds']: errors.append(f'{sid}: property target {target!r} does not allow kind {prop.get("kind")!r}')
  if sid and sid.startswith('ARCH-'):
    if t.get('adr')!='ADR-0001' or t.get('adr_repo')!='maximalfocus/stateless-mcp-incident-lab-architecture': errors.append(f'{sid}: bad architecture citation')
    expected_arch=p.parent/'expected.json'
    if expected_arch.exists():
      for assertion in json.loads(expected_arch.read_text()).get('assertions',[]):
        if assertion.get('type') in ('no_import','no_deep_import') and not str(assertion.get('from_glob','')).strip(): errors.append(f'{sid}: empty architecture glob')
  txt='\n'.join(x.read_text() for x in p.parent.glob('*.json'))
  if 'scenario/run' in txt: errors.append(f'{sid}: fixture targets harness pseudo-RPC rather than public boundary')
  if '"..."' in txt: errors.append(f'{sid}: invalid ellipsis placeholder')
  unknown_placeholders=set(re.findall(r'\{\{[A-Z_]+\}\}',txt))-declared_placeholders
  if unknown_placeholders: errors.append(f'{sid}: undeclared placeholders {sorted(unknown_placeholders)}')
for registry_name,registry in operation_registry.items():
  unused=set(registry)-used_registry_names[registry_name]
  if unused: errors.append(f'operation-registry.json has unused {registry_name}: {sorted(unused)}')
unused_policy_checks=set(policy_registry['checks'])-used_policy_checks
if unused_policy_checks: errors.append(f'policy-registry.json has unused checks: {sorted(unused_policy_checks)}')
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
# Multi-implementation WORKITEM closure, per-lane sizing, and ordered acyclic DAG.
wi=(root/'WORKITEMS.md').read_text()
lane_matches=list(re.finditer(r'^## Lane: ([a-z]+)$',wi,re.M))
expected_lane_order=['raw','sdk','integration','infrastructure','cicd']
lanes={}; seen_wi=[]
for index,lane_match in enumerate(lane_matches):
  lane=lane_match.group(1); end=lane_matches[index+1].start() if index+1<len(lane_matches) else len(wi)
  section=wi[lane_match.end():end]; entries=[]
  pattern=r'^- \[([ x~!])\] \*\*(WI-[0-9]{3})\*\* .*?\(([0-9]+) tests\)\n  - Tests: (.*?)\n  - Scope: (.*?)\n  - Depends on: (.*?)$'
  for m in re.finditer(pattern,section,re.M):
    paths=re.findall(r'`(conformance/[^`]+)`',m.group(4)); deps=[] if m.group(6)=='none' else [x.strip() for x in m.group(6).split(',')]
    entries.append({'id':m.group(2),'count':int(m.group(3)),'paths':paths,'scope':m.group(5),'deps':deps})
  lanes[lane]=entries; seen_wi.extend(entries)
  target_tokens={'raw':'stateless-mcp-incident-lab-typescript-raw','sdk':'stateless-mcp-incident-lab-typescript-sdk','integration':'stateless-mcp-incident-lab-prd','infrastructure':'stateless-mcp-incident-lab-infrastructure','cicd':'stateless-mcp-incident-lab-cicd'}
  target_line=re.search(r'^Target: (.+)$',section,re.M)
  if not target_line or target_tokens.get(lane) not in target_line.group(1): errors.append(f'WORKITEM lane {lane} has no concrete owning repository')
if [m.group(1) for m in lane_matches]!=expected_lane_order: errors.append('WORKITEM lane order/names malformed')
wi_ids=[x['id'] for x in seen_wi]
if len(wi_ids)!=len(set(wi_ids)) or wi_ids!=[f'WI-{i:03d}' for i in range(1,len(wi_ids)+1)]: errors.append('WORKITEM IDs must be unique and sequential')
known=set()
for entry in seen_wi:
  if not 2<=entry['count']<=5 or entry['count']!=len(entry['paths']): errors.append(f"{entry['id']} sizing/count invalid")
  if not entry['scope'].strip(): errors.append(f"{entry['id']} scope missing")
  unknown_deps=set(entry['deps'])-known
  if unknown_deps: errors.append(f"{entry['id']} has unknown or forward dependencies {sorted(unknown_deps)}")
  known.add(entry['id'])
all_paths={str(p.parent.relative_to(root)) for p in tests}
def paths_for(*categories): return {p for p in all_paths if p.split('/')[1] in categories}
implementation_categories={'architecture','protocol','versioning','transport','discovery','primitives','incidents','mrtr','streaming','cache','cli','properties','security','dependencies','observability'}
implementation_paths=paths_for(*implementation_categories)
metadata={p:json.loads((root/p/'test.json').read_text()) for p in implementation_paths}
raw_expected={p for p,t in metadata.items() if 'typescript-raw' in t.get('consumers',[])}
sdk_expected={p for p,t in metadata.items() if 'typescript-sdk' in t.get('consumers',[])}
lane_expected={'raw':raw_expected,'sdk':sdk_expected,'integration':paths_for('interoperability','performance'),'infrastructure':paths_for('infra'),'cicd':paths_for('cicd')}
for lane,expected in lane_expected.items():
  assigned=[p for entry in lanes.get(lane,[]) for p in entry['paths']]
  if len(assigned)!=len(set(assigned)) or set(assigned)!=expected:
    errors.append(f'WORKITEM lane {lane} assignment mismatch: missing={sorted(expected-set(assigned))}, extra={sorted(set(assigned)-expected)}')
if set().union(*lane_expected.values())!=all_paths: errors.append('WORKITEM lanes do not cover every golden')
# Cited ADR must exist and remain Accepted when the sibling architecture repo is checked out.
arch_adr=root.parent/'stateless-mcp-incident-lab-architecture'/'adr'/'0001-independent-raw-sdk-realizations.md'
if not arch_adr.exists() or not re.search(r'^Status:\s*Accepted\s*$',arch_adr.read_text(),re.M): errors.append('ADR-0001 citation is missing or stale')
# Golden auto-update code is forbidden across shipped scripts, including multiline writes.
for p in root.rglob('*'):
  if '.git' in p.parts or 'node_modules' in p.parts or not p.is_file() or p.suffix not in ('.py','.ts','.js','.mjs','.sh'): continue
  if p.name.startswith('test_') or '.test.' in p.name: continue
  text='\n'.join(line for line in p.read_text(errors='ignore').splitlines() if 'prohibited golden auto-update behavior' not in line)
  writes=r'(?:write_text|writeFile(?:Sync)?|open\s*\()'
  if re.search(rf'expected(?:\.json)?.{{0,300}}{writes}|{writes}.{{0,300}}expected(?:\.json)?',text,re.I|re.S): errors.append(f'{p.relative_to(root)} contains prohibited golden auto-update behavior')
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
