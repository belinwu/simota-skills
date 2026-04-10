# Approval Flow Patterns

**Purpose:** 承認フロー設計のパターン集。
**Read when:** 多段承認、エスカレーション、委任ルールの設計が必要な時。

---

## Approval Flow Types

| Type | Description | Use Case |
|------|-------------|----------|
| Sequential | 順番に承認者を回る | 経費申請（上長→部長→経理） |
| Parallel | 全承認者に同時に回す | 多部門合意（営業＋法務＋技術） |
| Quorum | N人中M人の承認で通過 | 委員会決議（5人中3人） |
| Conditional | 条件に応じて承認ルート分岐 | 金額別承認（10万未満→上長、10万以上→部長） |
| Hierarchical | 組織階層に沿って段階的 | 稟議書 |

---

## Sequential Approval Template

```yaml
APPROVAL_FLOW:
  name: "ExpenseApproval"
  type: sequential
  trigger:
    event: "expense_submitted"
    condition: "amount > 0"
  levels:
    - level: 1
      name: "Direct Manager"
      approvers:
        type: role
        value: "submitter.manager"
      quorum: 1
      timeout: "24h"
      timeout_action: escalate
      escalation_target: "level:2"
    - level: 2
      name: "Department Head"
      condition: "amount >= 50000"  # 5万円以上のみ
      approvers:
        type: role
        value: "submitter.department_head"
      quorum: 1
      timeout: "48h"
      timeout_action: escalate
      escalation_target: "cfo"
    - level: 3
      name: "CFO"
      condition: "amount >= 500000"  # 50万円以上のみ
      approvers:
        type: user
        value: "cfo@company.com"
      quorum: 1
      timeout: "72h"
      timeout_action: notify_and_wait
  on_approved:
    actions:
      - "process_payment"
      - "notify_submitter(approved)"
  on_rejected:
    actions:
      - "notify_submitter(rejected, reason)"
      - "allow_resubmission"
```

---

## Parallel Approval Template

```yaml
APPROVAL_FLOW:
  name: "ContractApproval"
  type: parallel
  trigger:
    event: "contract_submitted"
  approvers:
    - group: "Legal"
      role: "legal_reviewer"
      quorum: 1
      timeout: "72h"
    - group: "Finance"
      role: "finance_reviewer"
      quorum: 1
      timeout: "72h"
    - group: "Technical"
      role: "tech_lead"
      quorum: 1
      timeout: "48h"
  completion_rule: "all"  # all | any | quorum(N)
  on_any_rejection: "halt_and_notify"
```

---

## Delegation Rules

```yaml
DELEGATION:
  rules:
    - type: "absence"
      condition: "approver.status == 'out_of_office'"
      delegate_to: "approver.delegate"
      auto: true
    - type: "manual"
      condition: "approver requests delegation"
      delegate_to: "selected_delegate"
      requires:
        - "delegate has same or higher role"
        - "delegation logged for audit"
    - type: "escalation_timeout"
      condition: "approval_pending > timeout"
      delegate_to: "approver.manager"
      auto: true
  constraints:
    max_delegation_depth: 2
    audit_trail: required
    original_approver_notified: true
```

---

## Recall and Amendment

```yaml
RECALL:
  allowed_states: ["pending_approval"]
  not_allowed_states: ["approved", "rejected", "processing"]
  on_recall:
    actions:
      - "cancel_pending_approvals"
      - "return_to_draft"
      - "notify_approvers(recalled)"
    audit_log: true

AMENDMENT:
  allowed_states: ["rejected", "draft"]
  on_amend:
    actions:
      - "create_new_version"
      - "link_to_previous"
      - "restart_approval_flow"
    version_tracking: true
```

---

## State Machine for Approval

```yaml
STATE_MACHINE:
  name: ApprovalStateMachine
  initial: draft
  states:
    draft:
      on:
        SUBMIT: { target: pending_approval }
    pending_approval:
      on:
        APPROVE:
          - target: next_level
            guard: hasMoreLevels
          - target: approved
            guard: isFinalLevel
        REJECT: { target: rejected }
        RECALL: { target: draft }
        TIMEOUT:
          - target: escalated
            guard: escalationConfigured
          - target: pending_approval
            actions: [sendReminder]
    next_level:
      entry: [advanceLevel, notifyNextApprovers]
      always: { target: pending_approval }
    escalated:
      entry: [notifyEscalationTarget]
      on:
        APPROVE: { target: approved }
        REJECT: { target: rejected }
    approved:
      type: final
      entry: [executeApprovedActions, notifySubmitter]
    rejected:
      on:
        AMEND: { target: draft, actions: [createNewVersion] }
      entry: [notifySubmitter]
```

---

## Audit Trail Schema

```yaml
AUDIT_ENTRY:
  id: uuid
  flow_id: uuid
  timestamp: ISO8601
  actor:
    user_id: string
    role: string
    acted_as: string  # delegation の場合
  action: "approve | reject | recall | delegate | escalate | timeout"
  level: number
  comment: string
  metadata:
    ip_address: string
    user_agent: string
  previous_state: string
  new_state: string
```
