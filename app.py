import json
import streamlit as st
from engine import ask, evaluate, portfolio, policy_text, approve_task, DATA, TODAY

st.set_page_config(page_title='AI Portfolio Analyst | MIT PE Demo',page_icon='📊',layout='wide')
st.title('📊 AI Project Portfolio Analyst')
st.caption(f'MIT Professional Education • Agentic AI demonstration • Synthetic data • Scenario date: {TODAY}')
with st.sidebar:
    st.header('Demo controls')
    st.write('Model: Microsoft Foundry deployment')
    if st.button('Clear conversation'):
        st.session_state.history=[]
        st.session_state.trace=[]
        st.session_state.proposal=None
        st.rerun()
    st.info('All projects and policies are fictional. Approved tasks are stored locally only.')
if 'history' not in st.session_state: st.session_state.history=[]
if 'trace' not in st.session_state: st.session_state.trace=[]
if 'proposal' not in st.session_state: st.session_state.proposal=None

chat, data, governance, audit = st.tabs(['💬 Ask the agent','📁 Portfolio','📜 Governance policy','🔍 Agent trace & audit'])
with chat:
    st.write('Try: **Which projects need attention?** or **Prepare an escalation for P-101.**')
    for item in st.session_state.history:
        with st.chat_message(item['role']): st.markdown(item['content'])
    question=st.chat_input('Ask about the portfolio...')
    if question:
        with st.chat_message('user'): st.write(question)
        with st.chat_message('assistant'):
            try:
                with st.spinner('Consulting portfolio tools...'):
                    answer,trace=ask(question,st.session_state.history)
                st.markdown(answer)
                st.session_state.history.extend([{'role':'user','content':question},{'role':'assistant','content':answer}])
                st.session_state.trace.extend(trace)
                proposals=[x for x in trace if x['tool']=='prepare_escalation']
                if proposals:
                    draft=json.loads(proposals[-1]['result'])
                    if draft.get('prepared_only'): st.session_state.proposal=draft
            except Exception as e:
                st.error(f'Foundry call failed: {e}')
    if st.session_state.proposal:
        draft=st.session_state.proposal
        st.divider()
        st.subheader('🔐 Human approval required')
        st.write(f"**Project:** {draft['project_id']} — {draft['project_name']}")
        st.write(f"**Proposed action:** {draft['requested_action']}")
        st.write('**Evidence:** '+ '; '.join(draft['justification']))
        approver=st.text_input('Approver name',value='Office Hour Facilitator')
        a,b=st.columns(2)
        if a.button('Approve and create local task',type='primary'):
            try:
                task=approve_task(draft['project_id'],draft['requested_action'],approver)
                st.success(f"Created {task['task_id']} in the LOCAL DEMO audit log (no external system updated).")
                st.session_state.proposal=None
            except Exception as e: st.error(str(e))
        if b.button('Reject proposed action'):
            st.session_state.proposal=None
            st.info('Proposal rejected. No task created.')
with data:
    df=portfolio()
    a,b,c=st.columns(3)
    a.metric('Projects',len(df))
    b.metric('Policy escalations',sum(x['escalation_required'] for x in evaluate()))
    c.metric('Projects with findings',sum(bool(x['findings']) for x in evaluate()))
    st.dataframe(df,use_container_width=True,hide_index=True)
    st.download_button('Download synthetic portfolio CSV',(DATA/'projects.csv').read_bytes(),'projects.csv','text/csv')
with governance:
    st.markdown(policy_text())
    st.caption('Local document retrieval is demonstrated by the get_policy tool; this is not vector-search RAG.')
with audit:
    st.subheader('Actual tool calls')
    if not st.session_state.trace: st.info('Ask the agent a question to populate the trace.')
    for idx,entry in enumerate(st.session_state.trace,1):
        with st.expander(f"{idx}. {entry['tool']}"):
            st.json(entry['arguments'])
            try: st.json(json.loads(entry['result']))
            except Exception: st.code(entry['result'])
    st.subheader('Approved local tasks')
    path=DATA/'approved_tasks.jsonl'
    if path.exists():
        for line in path.read_text(encoding='utf-8').splitlines():
            if line.strip(): st.json(json.loads(line))
    else: st.caption('No tasks approved yet.')
