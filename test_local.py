from engine import evaluate, tool_run, approve_task
import json
r=evaluate()
assert len(r)==10
assert next(x for x in r if x['project_id']=='P-101')['escalation_required']
assert next(x for x in r if x['project_id']=='P-108')['escalation_required'] is False
assert 'PMO-2026-01' in tool_run('get_policy',{})
assert json.loads(tool_run('prepare_escalation',{'project_id':'P-101','action':'Escalate'}))['prepared_only']
print('PASS: 10 projects, escalation rules, policy retrieval, draft-only action')
