# 🤖 Agentic AI System Guide

## Overview

The Ghost Detection system includes a sophisticated **Agentic AI framework** that enables autonomous AI agents to monitor, analyze, and respond to paranormal activity without constant human intervention.

## What is Agentic AI?

Agentic AI refers to autonomous AI systems that can:
- **Make decisions** independently based on predefined policies
- **Take actions** without human intervention (within approved boundaries)
- **Learn** from outcomes and adjust behavior
- **Communicate** with humans and other agents
- **Coordinate** complex multi-step workflows

## System Architecture

### 5 Core AI Agents

#### 1. **ThreatWatch AI** (Monitoring Agent)
- **Role**: Real-time threat detection and alerting
- **Authority Level**: Execute-Low-Risk
- **Capabilities**:
  - Monitor all ghost sightings continuously
  - Detect emerging threat patterns
  - Generate automatic alerts for extreme threats
  - Track ghost activity levels
- **Trigger**: Runs every 30 minutes
- **Example Action**: "Detected 3 extreme-threat ghosts active in last 24 hours → Send urgent alert to all investigators"

```sql
-- Manually run ThreatWatch
CALL APP.AGENT_MONITOR_THREATS();
```

#### 2. **InvestigatorAI** (Analysis Agent)
- **Role**: Evidence analysis and ghost classification
- **Authority Level**: Suggest
- **Capabilities**:
  - Analyze new evidence automatically
  - Classify ghost types using Cortex AI
  - Identify behavior patterns
  - Generate detailed investigation reports
- **Trigger**: Runs every hour
- **Example Action**: "New sighting detected → Analyze description → Classify as 'Class IV Poltergeist' → Recommend containment team"

```sql
-- Manually run InvestigatorAI
CALL APP.AGENT_ANALYZE_NEW_SIGHTINGS();
```

#### 3. **ResponseCoordinator AI** (Response Agent)
- **Role**: Team coordination and resource allocation
- **Authority Level**: Execute-Low-Risk
- **Capabilities**:
  - Match investigators to cases based on skills
  - Balance team workload
  - Schedule investigations
  - Allocate equipment and resources
- **Trigger**: On-demand
- **Example Action**: "New high-priority case → Match to investigator with EMF expertise → Check workload → Recommend assignment"

```sql
-- Manually run ResponseCoordinator
CALL APP.AGENT_ASSIGN_INVESTIGATORS();
```

#### 4. **CommunicationAI** (Communication Agent)
- **Role**: Information distribution and reporting
- **Authority Level**: Execute-All
- **Capabilities**:
  - Send alerts and notifications
  - Generate daily/weekly reports
  - Answer investigator questions
  - Provide status updates
- **Trigger**: Daily at 08:00 UTC + on-demand
- **Example Action**: "Generate daily summary of all ghost activity → Format report → Distribute to all investigators"

```sql
-- Generate daily summary
CALL APP.AGENT_DAILY_SUMMARY();
```

#### 5. **PredictiveAI** (Forecasting Agent)
- **Role**: Predictive analytics and pattern recognition
- **Authority Level**: Suggest
- **Capabilities**:
  - Forecast future ghost activity
  - Identify emerging hotspots
  - Predict ghost behavior patterns
  - Risk assessment and modeling
- **Trigger**: On-demand
- **Example Action**: "Analyze last 30 days of data → Predict 5 high-risk locations for next week → Recommend monitoring"

```sql
-- Generate predictions
CALL APP.AGENT_GENERATE_PREDICTIONS();
```

## Agent Components

### 1. Agent Definitions (AI_AGENTS Table)

Each agent has:
- **Unique ID and Name**
- **Type** (Monitoring, Analysis, Response, etc.)
- **Role Description**
- **Capabilities List**
- **Authority Level** (what actions it can take autonomously)
- **LLM Model** (default: mistral-large2)
- **System Prompt** (defines agent personality and behavior)

```sql
SELECT * FROM APP.AI_AGENTS WHERE is_active = TRUE;
```

### 2. Agent Actions (AGENT_ACTIONS Table)

Records every decision and action:
- **Action Type**: Analyze, Alert, Recommend, Execute, Communicate
- **Decision Reasoning**: AI's explanation for why it took this action
- **Risk Level**: Low, Medium, High, Critical
- **Approval Status**: Auto-Approved, Pending, Approved, Rejected
- **Confidence Score**: AI's confidence in the decision (0-1)

```sql
-- View recent agent actions
SELECT * FROM APP.AGENT_ACTIONS 
ORDER BY created_date DESC 
LIMIT 20;
```

### 3. Agent Policies (AGENT_POLICIES Table)

Rules governing agent behavior:
- **Safety Policies**: Prevent dangerous autonomous actions
- **Efficiency Policies**: Optimize resource usage
- **Communication Policies**: Ensure timely information flow
- **Quality Policies**: Maintain high standards

```sql
-- View active policies
SELECT * FROM APP.AGENT_POLICIES 
WHERE is_active = TRUE 
ORDER BY priority;
```

Example Policies:
1. **Extreme Threat Auto-Alert** (Priority 1)
   - Any Extreme threat with recent activity → Immediate alert
2. **Require Approval for Containment** (Priority 1)
   - Containment actions → Must get human approval
3. **Investigator Workload Balance** (Priority 75)
   - Max 5 active cases per investigator

### 4. Agent Learning (AGENT_LEARNING Table)

Feedback loop for continuous improvement:
- Records outcomes of agent actions
- Stores feedback scores (-1 to 1)
- Documents lessons learned
- Tracks behavioral adjustments

```sql
-- Log agent learning
INSERT INTO APP.AGENT_LEARNING (
    learning_id, agent_id, scenario_description,
    action_taken, outcome_result, feedback_score,
    lessons_learned
) VALUES (
    'LEARN_001', 'AGENT_001', 
    'Extreme threat alert sent for dormant ghost',
    'Sent urgent alert', 'Partial',
    -0.3,
    'Check ghost status before alerting. Dormant ghosts are lower priority.'
);
```

### 5. Agent Communications (AGENT_COMMUNICATIONS Table)

All agent-to-agent and agent-to-human messages:
- Message type and priority
- Sender and recipient
- Full message content
- Response tracking

```sql
-- View agent communications
SELECT * FROM APP.VW_AGENT_COMMUNICATIONS_LOG
LIMIT 50;
```

## Running Agents

### Manual Execution

Run individual agents:

```sql
-- Run specific agent
CALL APP.AGENT_MONITOR_THREATS();
CALL APP.AGENT_ANALYZE_NEW_SIGHTINGS();
CALL APP.AGENT_ASSIGN_INVESTIGATORS();
CALL APP.AGENT_GENERATE_PREDICTIONS();
CALL APP.AGENT_DAILY_SUMMARY();

-- Run all agents at once
CALL APP.RUN_ALL_AGENTS();
```

### Scheduled Execution

Enable automated agent execution:

```sql
-- Enable threat monitoring (every 30 minutes)
ALTER TASK APP.TASK_AGENT_MONITOR RESUME;

-- Enable sighting analysis (every hour)
ALTER TASK APP.TASK_AGENT_ANALYZE RESUME;

-- Enable daily summary (08:00 UTC)
ALTER TASK APP.TASK_AGENT_DAILY_SUMMARY RESUME;
```

### Disable Scheduled Execution

```sql
-- Disable tasks
ALTER TASK APP.TASK_AGENT_MONITOR SUSPEND;
ALTER TASK APP.TASK_AGENT_ANALYZE SUSPEND;
ALTER TASK APP.TASK_AGENT_DAILY_SUMMARY SUSPEND;
```

## Monitoring Agent Performance

### Agent Performance Dashboard

```sql
SELECT * FROM APP.VW_AGENT_PERFORMANCE;
```

Shows for each agent:
- Total actions taken
- Auto-approved vs human-approved actions
- Rejection rate
- Average confidence score
- Last action date

### Recent Agent Activity

```sql
SELECT 
    agent_name,
    action_type,
    action_description,
    risk_level,
    approval_status,
    confidence_score,
    executed_date
FROM APP.AGENT_ACTIONS aa
JOIN APP.AI_AGENTS a ON aa.agent_id = a.agent_id
WHERE executed_date >= DATEADD(day, -7, CURRENT_TIMESTAMP())
ORDER BY executed_date DESC;
```

## Authority Levels Explained

### 1. Read-Only
- Agent can only query and observe
- Cannot take any actions
- All output is informational only

### 2. Suggest
- Agent can make recommendations
- All actions require human approval
- Example: InvestigatorAI suggests ghost classifications

### 3. Execute-Low-Risk
- Agent can execute safe, routine actions autonomously
- No risk to safety or data integrity
- Example: ThreatWatch sends alerts, analyzes data

### 4. Execute-All
- Agent has full autonomy within its role
- Can take any action it's capable of
- Example: CommunicationAI sends all communications autonomously

## Safety Features

### 1. Approval Workflow

High-risk actions require approval:

```sql
-- View actions pending approval
SELECT * FROM APP.AGENT_ACTIONS
WHERE requires_approval = TRUE
AND approval_status = 'Pending';

-- Approve an action
UPDATE APP.AGENT_ACTIONS
SET approval_status = 'Approved',
    executed_date = CURRENT_TIMESTAMP()
WHERE action_id = 'ACT_12345';

-- Reject an action
UPDATE APP.AGENT_ACTIONS
SET approval_status = 'Rejected'
WHERE action_id = 'ACT_12345';
```

### 2. Policy Enforcement

Policies automatically govern agent behavior:

```sql
-- Add new safety policy
INSERT INTO APP.AGENT_POLICIES (
    policy_id, policy_name, policy_category,
    policy_rule, applies_to_agents, priority
) VALUES (
    'POL_006', 'No Autonomous Containment', 'Safety',
    'Agents must never initiate ghost containment without human approval',
    ARRAY_CONSTRUCT('AGENT_001', 'AGENT_002', 'AGENT_003'),
    1  -- Highest priority
);
```

### 3. Audit Trail

Complete audit trail of all agent actions:

```sql
-- Audit trail
SELECT 
    a.agent_name,
    aa.action_type,
    aa.decision_reasoning,
    aa.risk_level,
    aa.approval_status,
    aa.executed_date,
    aa.execution_result
FROM APP.AGENT_ACTIONS aa
JOIN APP.AI_AGENTS a ON aa.agent_id = a.agent_id
ORDER BY aa.created_date DESC;
```

## Use Cases

### Use Case 1: Autonomous Threat Detection

**Scenario**: Ghost becomes extremely active overnight

**Agent Response**:
1. ThreatWatch AI detects spike in activity
2. Analyzes threat level (Extreme)
3. Generates urgent alert
4. CommunicationAI distributes to all investigators
5. ResponseCoordinator recommends team deployment
6. Logs all actions for audit

**Human Intervention**: None required for alert, approval needed for team deployment

### Use Case 2: Evidence Processing Pipeline

**Scenario**: 50 new ghost sightings reported

**Agent Response**:
1. InvestigatorAI detects unprocessed sightings
2. Analyzes each using Cortex AI
3. Classifies ghost types
4. Generates summary report
5. Identifies 3 high-priority cases
6. ResponseCoordinator assigns to appropriate investigators

**Human Intervention**: Review and approve high-priority assignments

### Use Case 3: Predictive Monitoring

**Scenario**: Weekly planning session

**Agent Response**:
1. PredictiveAI analyzes last 30 days of data
2. Identifies emerging hotspots
3. Predicts high-risk locations for next week
4. Calculates probability scores
5. Recommends monitoring strategy
6. CommunicationAI includes in weekly report

**Human Intervention**: Review predictions and adjust monitoring plans

## Best Practices

### 1. Start Conservative
- Begin with all agents in "Suggest" mode
- Review actions for 1-2 weeks
- Gradually increase authority levels

### 2. Monitor Confidence Scores
```sql
-- Track low-confidence actions
SELECT * FROM APP.AGENT_ACTIONS
WHERE confidence_score < 0.7
ORDER BY executed_date DESC;
```

### 3. Review and Approve Regularly
```sql
-- Daily approval review
SELECT * FROM APP.AGENT_ACTIONS
WHERE requires_approval = TRUE
AND approval_status = 'Pending'
AND created_date >= CURRENT_DATE();
```

### 4. Provide Feedback
```sql
-- Give feedback on agent actions
INSERT INTO APP.AGENT_LEARNING (
    learning_id, agent_id, scenario_description,
    action_taken, outcome_result, feedback_score,
    lessons_learned
) VALUES (...);
```

### 5. Update Policies
- Review agent performance monthly
- Adjust policies based on outcomes
- Add new policies as needed

## Advanced Features

### Multi-Agent Coordination

Agents can communicate with each other:

```sql
-- Agent-to-agent communication
INSERT INTO APP.AGENT_COMMUNICATIONS (
    communication_id, from_agent_id, to_agent_id,
    message_type, message_content, priority
) VALUES (
    'COMM_' || UUID_STRING(),
    'AGENT_001',  -- ThreatWatch
    'AGENT_003',  -- ResponseCoordinator
    'Request',
    'Extreme threat detected at Museum. Request immediate team deployment.',
    'Urgent'
);
```

### Custom Agent Creation

Add your own agents:

```sql
INSERT INTO APP.AI_AGENTS (
    agent_id, agent_name, agent_type, agent_role,
    capabilities, authority_level, system_prompt
) VALUES (
    'AGENT_006',
    'CostOptimizer AI',
    'Efficiency',
    'Optimize resource usage and reduce investigation costs',
    ARRAY_CONSTRUCT('Analyze Costs', 'Optimize Resources', 'Recommend Savings'),
    'Suggest',
    'You are CostOptimizer AI. Your role is to help reduce costs while maintaining effectiveness. Analyze resource usage and recommend optimizations.'
);
```

## Troubleshooting

### Agent Not Taking Actions

1. **Check if agent is active**:
```sql
SELECT * FROM APP.AI_AGENTS WHERE agent_id = 'AGENT_001';
```

2. **Check task status**:
```sql
SHOW TASKS LIKE 'TASK_AGENT%';
```

3. **Review recent errors**:
```sql
SELECT * FROM APP.AGENT_ACTIONS
WHERE execution_result:status = 'error'
ORDER BY executed_date DESC;
```

### Low Confidence Scores

If agents consistently show low confidence:
- Review and improve system prompts
- Provide more training data
- Adjust policies to be more specific
- Consider using different LLM models

### Too Many Pending Approvals

- Review authority levels (might be too restrictive)
- Adjust policies to auto-approve more low-risk actions
- Set up approval delegation workflow

## Integration with MCP

Agents can be triggered via MCP server:

```python
# Via MCP
result = await mcp_client.call_tool(
    "run_agent",
    {"agent_id": "AGENT_001", "action": "monitor_threats"}
)
```

See [MCP_GUIDE.md](MCP_GUIDE.md) for details.

---

**The future of ghost detection is autonomous!** 🤖👻

