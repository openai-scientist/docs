# State Machine Diagrams — Mermaid

Mỗi khối bên dưới là một state diagram độc lập, tương ứng một tab trong [file draw.io](State-Machine-Diagrams.drawio). Sao chép từng khối vào trình hỗ trợ Mermaid để vẽ. Mermaid tự sắp xếp nên vị trí đường nối có thể khác ảnh gốc.

Các nhãn được giữ ngắn như hình; nhánh choice ghi điều kiện đầy đủ. Chi tiết guard, effect, reason/result và giới hạn thiết kế xem [thuyết minh và bảng transition](State-Machine-Diagrams-design.md). Dataset available và notification unread/read là trạng thái khái niệm. Local Node và email retry là thiết kế dự kiến, không xác nhận runtime.

## 1. Authentication & Account

```mermaid
stateDiagram-v2
    state "Active account" as active
    state "Suspended account" as suspended
    [*] --> active
    active --> suspended : admin suspends account
    suspended --> active : admin reactivates account
```

## 2. Project Workspace

```mermaid
stateDiagram-v2
    direction TB
    state "Active" as s_active
    state "Completed" as s_completed
    state "Archived (read-only)" as s_archived
    [*] --> s_active
    s_active --> s_completed : marked completed
    s_completed --> s_archived : archived
    s_active --> s_archived : archived
    s_active --> s_active : project updated
    s_archived --> [*]
```

## 3. Data Management

```mermaid
stateDiagram-v2
    state "Dataset available" as available
    [*] --> available : create first version with hash
    available --> available : new version; retain prior versions
    available --> [*] : authorized deletion confirmed
```

## 4. Research Run Orchestration

```mermaid
stateDiagram-v2
    direction TB
    state "Running" as s_running
    state "Waiting" as s_waiting
    state "Ended" as s_ended
    [*] --> s_running
    s_running --> s_waiting : Decision blocks work
    s_running --> s_waiting : Node offline
    s_running --> s_waiting : Monthly budget reached
    s_waiting --> s_running : Decision answered
    s_waiting --> s_running : Node reconnects
    s_waiting --> s_running : Extra spend approved
    s_running --> s_ended : All stages accepted
    s_waiting --> s_ended : Pinned wait expires
    s_waiting --> s_ended : Spending declined or expired
    s_ended --> [*]
    s_running --> s_ended : Run cancelled
    s_waiting --> s_ended : Run cancelled
    s_running --> s_ended : Technical failure
    s_waiting --> s_ended : Technical failure
    s_running --> s_ended : Token budget exhausted
    s_waiting --> s_ended : Token budget exhausted
```

## 5. Research Engines

```mermaid
stateDiagram-v2
    direction TB
    state "Draft" as s_draft
    state s_checks <<choice>>
    state "Checks failed" as s_red
    state "Checks passed" as s_green
    state "Under review" as s_review
    state "Ready for acceptance" as s_ready
    state "Accepted" as s_accepted
    state "Locked (AnalysisPlan)" as s_locked
    state "Stale" as s_stale
    [*] --> s_draft : / round := 0
    s_draft --> s_checks : checks completed
    s_checks --> s_red : [at least one contract item red]
    s_checks --> s_green : [all contract items green]
    s_red --> s_checks : Checks rerun
    s_green --> s_checks : contract check changed
    s_green --> s_review : review started
    s_review --> s_checks : Revision checked [round < 2]
    s_review --> s_ready : review completed
    s_ready --> s_accepted : Object accepted
    s_accepted --> s_locked : Plan locked [AnalysisPlan]
    s_draft --> s_stale : New upstream version
    s_red --> s_stale : New upstream version
    s_green --> s_stale : New upstream version
    s_review --> s_stale : New upstream version
    s_ready --> s_stale : New upstream version
    s_accepted --> s_stale : New upstream version
    s_locked --> s_stale : New upstream version
```

## 6. AI Principal Investigator

```mermaid
stateDiagram-v2
    direction TB
    state "Pending user decision" as s_pending
    state "Tentatively decided (awaiting user review)" as s_tentative
    state s_confirms <<choice>>
    state "Confirmed" as s_confirmed
    state "Overturned" as s_overturned
    state "Answered" as s_answered
    state "Closed unanswered (pinned wait deadline)" as s_unanswered
    state "Expired unanswered (spending deadline)" as s_spending_expired
    state "Closed (run cancelled)" as s_closed_cancelled
    [*] --> s_pending
    s_pending --> s_answered : authorized user answers
    s_pending --> s_tentative : AI PI decides [eligible]
    s_tentative --> s_confirms : Decision submitted
    s_confirms --> s_confirmed : [submitted decision is confirm]
    s_confirms --> s_overturned : [submitted decision is overturn]
    s_pending --> s_unanswered : Pinned deadline expires
    s_pending --> s_spending_expired : Spending deadline expires
    s_pending --> s_closed_cancelled : run cancelled
    s_tentative --> s_closed_cancelled : run cancelled
    s_answered --> [*]
    s_unanswered --> [*]
    s_spending_expired --> [*]
    s_confirmed --> [*]
    s_overturned --> [*]
    s_closed_cancelled --> [*]
```

## 7. Notifications & Integrations

```mermaid
stateDiagram-v2
    state "Unread" as unread
    state "Read" as read
    [*] --> unread
    unread --> read : recipient marks as read; record read_at
```

## 8. Administration & Monitoring

```mermaid
stateDiagram-v2
    direction TB
    state "Active alert" as s_active
    state "Resolved alert" as s_resolved
    [*] --> s_active
    s_active --> s_active : acknowledged
    s_active --> s_resolved : Resolution reported
    s_resolved --> [*]
```
