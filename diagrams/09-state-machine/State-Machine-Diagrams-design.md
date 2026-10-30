# State Machine Diagrams — các vòng đời theo nhóm chức năng

- [File draw.io chung chín tab](State-Machine-Diagrams.drawio)
- [Builder](build_state_diagrams.py)
- [Rule](rule.md)

Nguồn: `C:/Users/ADMIN/Downloads/xFA26SE115_Report7.md`, SHA-256 `8618eb8123e0a3d259c9e5f5ba97f9e29602534ae3503b2aaa25e0d2e5eb232d`. Cách chia tab theo [Class Diagram](../07-class/Class-Diagrams-design.md), không suy từ số entity lifecycle. Đối chiếu [Report IV](../../report/04-software-design-document.md).

## Inventory

| Tab | PNG | Nguồn |
|---|---|---|
| 1. Authentication & Account | [Authentication-Account](01-Authentication-Account.png) | III 3.2.1; IV 3.1 |
| 2. Project Workspace | [Project-Workspace](02-Project-Workspace.png) | III 3.3.1–3.3.3; IV 3.2.14 |
| 3. Data Management | [Data-Management](03-Data-Management.png) | IV 3.3.11; IV 3.12; FR-85/87/110/242 |
| 4. Research Run Orchestration | [Research-Run-Orchestration](04-Research-Run-Orchestration.png) | IV 3.4.2, Figure IV-7; IV 3.13 |
| 5. Research Engines | [Research-Engines](05-Research-Engines.png) | IV 3.4.3, Figure IV-8; IV 3.11; IV 3.8 |
| 6. AI Principal Investigator | [AI-Principal-Investigator](06-AI-Principal-Investigator.png) | IV 3.6.7; IV 3.5.2; IV 3.13; FR-22/28/31/91/265 |
| 7. Notifications & Integrations | [Notifications-Integrations](07-Notifications-Integrations.png) | IV 2.2.16 notification_emails; IV 2.2.11 integration_deliveries; IV 3.7 |
| 8. Administration & Monitoring | [Administration-Monitoring](08-Administration-Monitoring.png) | III 3.9.9; IV 2.2.38 monitoring_alerts; IV 3.8; FR-104 |
| 9. Dossier Version | [Dossier-Version](09-Dossier-Version.png) | IV 3.14; FR-94–98, FR-249–253 |

## Report mẫu tham khảo hình

File tham khảo: `C:/Users/ADMIN/Downloads/Copy of 9927_HCM_SU26SE109_GSU41_HCM_GSU26SE41_FI2M_Report7_Final_Project_Report.docx.md`. SHA-256 file mẫu: `6ea83525979bbee6a8282c3122615a421b0cabf2174b32a5e5045f29f3428b74`. Các ảnh nhúng base64 đã được mở xem ở độ phân giải gốc; dùng để chọn cách trình bày, không nhập nghiệp vụ thiết bị/venue vào dự án.

| Ảnh nhúng | Caption / mục trong report mẫu | Cách áp dụng |
|---|---|---|
| image118 | IV 3.1.4, Borrow Request (caption ghi Class Diagram nhưng nội dung là lifecycle) | Tên state ngắn, luồng chính và nhánh phụ; không sao chép lỗi caption/ảnh nhỏ. |
| image128 | Figure 4.3.3.5.1 Lecturer Account Lifecycle | Sự kiện bằng lời, guard đặt trên đường, vòng quay lại ở ngoài. |
| image131 | Figure 4.3.4.3.1 Equipment SKU Lifecycle | Một state một ô, nhiều transition có nguồn/đích rõ; không thu chữ nhỏ như ảnh gốc. |
| image135 | Figure 4.3.5.4.1 Inventory Audit Session Lifecycle | Trục dọc, nhánh completed/cancelled rõ, initial/final tối giản. |
| image144–147 | Figure 4.3.7.3.1–4 Venue | Phân biệt nhóm luồng chức năng có câu hỏi/Yes-No với lifecycle entity; chỉ dùng bố cục choice đã chốt. |
| image150 | Figure 4.3.8.3.1 Create a booking | Nhánh kiểm tra/ngoại lệ ở hai bên; không mang CRUD/HTTP lỗi sang state của dự án. |
| image153 | Figure 4.3.9.3.1 Penalty & Credibility | Tham khảo cách ghi điều kiện; không sao chép điểm gom/ký hiệu không cần. |
| image157 | Figure 4.3.10.3.1 Maintenance | State gọn và sự kiện ngắn, initial → state → final. |
| image161 | Figure 4.3.11.3.1 Disposal | Bố cục ngắn, nhãn nghiệp vụ dễ đọc. |

Profile áp dụng: Arial state 12/transition 11, cùng tỉ lệ bố cục compact; tiêu đề con 14. Nhãn hiển thị bằng lời như User cancels/Node reconnects/All stages accepted. transition-spec giữ trigger/guard/effect gốc; bảng bên dưới ghi cả nhãn ảnh và biểu thức đầy đủ. Không bỏ trạng thái, transition, reason/result hoặc predicate để làm hình gọn. Giữ nền trắng, state bo góc theo UML, không sao chép viền vuông/cắt ảnh/chữ quá nhỏ từ report mẫu.


## Cách đọc và mức thiết kế

Giữ đầy đủ trạng thái và nhánh; Research Engines dùng composite theo yêu cầu mới, các view khác giữ bố cục hiện có, không thêm frame stm. Câu hỏi trong hình thoi, guard [No] trái/[Yes] phải; Yes/No là alias của biểu thức guard ở bảng dưới, không phải event. Nhãn ngắn nằm trực tiếp trên đường nối nền trắng; điều kiện, effect và reference đầy đủ ở bảng dưới. Research Engines dùng composite và một transition chung tới Stale; các nhánh revision giữ đường riêng; không dùng nhãn chung end event. Mỗi vòng đời là một graph liền mạch, mỗi state chỉ xuất hiện một lần; không tách các cụm sự kiện rồi vẽ lại state. Các transition dùng nét liền/mũi tên mở. Nhãn theo trigger [guard] / effect; choice chỉ phân nhánh tức thời theo guard; không đợi event ở đường ra. Event userDecisionSubmitted phải tới trước choice confirm/overturn. Reason/result là field context, giá trị và phép gán đầy đủ ở metadata/bảng transition; không cần ô chú thích kỹ thuật riêng trên ảnh theo profile report mẫu. model-state trong XML ánh xạ nhãn dễ đọc về state code nguồn. Đường chính/hồi tiếp vuông góc; transition trên biên composite tới Stale kế thừa cho mọi state con khi pinned upstream có version mới. Mỗi điểm final chỉ có ý nghĩa hoàn tất phạm vi đang mô tả, không phải xóa bản ghi.

Tám nhóm chức năng được tổ chức thành chín tab: Dossier Version có tab riêng, cùng các vòng đời theo nhóm Class. Tab Data Management mô tả vòng đời một Local Node pairing theo yêu cầu mới, ở mức thiết kế dự kiến; chưa xác nhận implementation. Các lifecycle còn lại giữ nguồn và giới hạn thiết kế; Notifications/Monitoring là view đề xuất từ schema/hành vi.

Các status lấy từ nguồn nhưng một enum không tự xác nhận đầy đủ transition. Những nhãn hay transition diễn giải được chỉ rõ trong từng mục. Không đổi nghiệp vụ BRD/PRD/Use Case Spec; không thay placeholder Word. Final UML đánh dấu hoàn tất vòng đời/region, không hàm ý xóa record. Run có completion từ Ended tới final, result vẫn lưu; Authentication kết thúc một lần đăng nhập. Archived và Superseded kết thúc vòng đời trong phạm vi hình, không kết luận record bị xóa hoặc hệ thống không bao giờ có chức năng khôi phục. Các Decision Item đã trả lời/đóng, email Sent/Skipped và alert Resolved đều nối final. Mỗi nhánh có final riêng để tránh đường gom dài. Stale giữ lịch sử version; acceptance/rerun upstream-downstream không phải tự sửa version cũ. Không thêm final/transition phục hồi chưa chốt. Failed có thể giữ nguyên; retry email là đề xuất, không bảo đảm luôn retry.

Test ID trong metadata/bảng là tham chiếu kịch bản, không phải kết quả test runtime. Design routing/retry check là kiểm tra thiết kế còn cần bổ sung, không bịa TC ID.

## Hiệu chỉnh sau review 2026-10-30

Bảo toàn transition-spec trước khi rút gọn nhãn. AI PI hiển thị guard autopilot/away/non-pinned, timeout có no answer; effect confirm/overturn lưu riêng và xuất ở bảng. Nhánh Ended của Run hiển thị result; Dossier export có effect export/audit. Review bao gồm revision work; sự kiện hoàn tất checks có guard tối đa hai vòng. Phạm vi stale version được ghi trong thuyết minh; email retry ghi proposed. Monitoring dùng resolution reported trực tiếp.

Giới hạn chưa chốt: cách ưu tiên nhiều blocker đồng thời của Run; identity/liên kết item tentative; chính sách retry và kết thúc failure email. Không tự thêm thuật toán hoặc transition cho các điểm này.

## 1. Authentication & Account

III 3.2.1; IV 3.1.

Một lần đăng nhập email; giữ graph đã duyệt, chỉ đổi tên tab theo nhóm Class.

Xem [nguồn và truy vết bản Authentication đã duyệt](Sign-In-With-Email-Code-design.md).

## 2. Project Workspace

III 3.3.1–3.3.3; IV 3.2.14.

Vòng đời Project gồm Active, Completed, Archived; Archived là read-only. Dossier Version được tách sang tab riêng.

| Transition | Nhãn ngắn | Điều kiện / nguồn đầy đủ | Test reference |
|---|---|---|---|
| Initial → Active | (nối đường) | III 3.3.1; FR-04 | TC-03 |
| Active → Completed | marked completed | UML: project marked completed<br>/ write audit entry; III 3.3.3; FR-07 | TC-03; TC-05 |
| Completed → Archived<br>(read-only) | archived | UML: project archived<br>/ write audit entry; III 3.3.3; FR-06; FR-07 | TC-03; TC-05 |
| Active → Archived<br>(read-only) | archived | UML: project archived<br>/ make read-only; audit; III 3.3.3; FR-06; FR-07 | TC-03; TC-05 |
| Active → Active | project updated | UML: project updated<br>/ write audit entry; III 3.3.3; FR-07 | TC-03; TC-05 |
| Archived<br>(read-only) → Final | (nối đường) | UML completion within the depicted lifecycle scope; history remains stored | Design completion check |

## 3. Data Management

IV 3.3.11; IV 3.12; FR-85/87/110/242.

Theo yêu cầu mới, khôi phục thiết kế vòng đời một Local Node pairing với project: Unpaired, Paired online, Paired offline, Revoked. Đây là state khái niệm từ UC-08/31 và FR-85/87/110/241/242, không khẳng định enum implementation. Pairing hợp lệ đưa tới online; mất kết nối không mất pairing; reconnect quay online. Revocation từ cả online/offline chặn local jobs, nêu lý do và giữ published objects readable. Final kết thúc pairing hiện tại, không xóa Node/results; re-pairing ngoài view. Không biến kiểm hash, chạy job hay release gate thành state của Node.

| Transition | Nhãn ngắn | Điều kiện / nguồn đầy đủ | Test reference |
|---|---|---|---|
| Initial → Unpaired (unpaired) | (nối đường) | UC-08 precondition: installed Node before project pairing | TC-08 |
| Unpaired (unpaired) → Paired<br>(online) (paired_online) | pairing succeeds<br>[valid project pairing code] | UML: pairing succeeds<br>[valid project pairing code]; UC-08; FR-87; conceptual connected pairing outcome | TC-08 |
| Paired<br>(online) (paired_online) → Paired<br>(offline) (paired_offline) | connection lost | UML: connection lost; UC-31; FR-85; connection status independent of local job status | TC-31 |
| Paired<br>(offline) (paired_offline) → Paired<br>(online) (paired_online) | Node reconnects | UML: Node reconnects; UC-31 alternative flow; IV 3.4.2 waiting(node_offline) | TC-31 |
| Paired<br>(online) (paired_online) → Revoked (revoked) | pairing revoked<br>/ reject local jobs; explain reason;<br>keep published objects readable | UML: pairing revoked<br>/ reject local jobs; explain reason;<br>keep published objects readable; UC-31; FR-110; FR-241; FR-242; end of this pairing, not deletion of Node or results | TC-31 |
| Paired<br>(offline) (paired_offline) → Revoked (revoked) | pairing revoked<br>/ reject local jobs; explain reason;<br>keep published objects readable | UML: pairing revoked<br>/ reject local jobs; explain reason;<br>keep published objects readable; UC-31; FR-110; FR-241; FR-242; end of this pairing, not deletion of Node or results | TC-31 |
| Revoked (revoked) → Final | (nối đường) | UML completion within the depicted lifecycle scope; history remains stored | Design completion check |

## 4. Research Run Orchestration

IV 3.4.2, Figure IV-7; IV 3.13.

Một state machine liền mạch, chỉ ba state Running/Waiting/Ended theo enum RunState của Class Diagram và FR-21. Waiting có reason decision/node_offline/budget_review; node_offline khi Node offline và local job chặn việc; reconnect đưa về running, independent work và một combined notice theo FR-237/238; Ended có result complete/with_gaps/failed_technical/cancelled. Đây là field của state, không phải nhiều state trùng tên. Các transition riêng thể hiện đủ nguyên nhân/điều kiện và phép gán reason/result. Từ running: all stages accepted, token exhaustion, cancel, technical failure; từ waiting(decision): pinned deadline unanswered, token exhaustion, cancel, technical failure; từ waiting(budget_review): spending decline/expiry, token exhaustion, cancel, technical failure. Không lặp state hay tách các cụm tình huống rời; mỗi transition là nét liền có trigger [guard] / effect khi cần. Tên event/effect là ký hiệu thiết kế từ hành vi, không chốt event/API implementation. Chỉ complete khi tất cả stage accepted. Cancel chỉ bởi Project Manager hoặc creating Researcher. Pinned item không hết hạn trước wait deadline. Khôi phục nhánh node_offline theo yêu cầu mới như thiết kế dự kiến; không khẳng định Local Node đã triển khai.

| Transition | Nhãn ngắn | Điều kiện / nguồn đầy đủ | Test reference |
|---|---|---|---|
| Initial → Running (running) | (nối đường) | IV 3.4.1; FR-14; FR-21 | TC-09 |
| Running (running) → Waiting (waiting) | Decision blocks work [present or pinned] | UML: decisionBlocked [present or pinned] /<br>reason := decision; IV 3.4.2; FR-262; no independent work; user present or pinned | TC-16; TC-98 |
| Running (running) → Waiting (waiting) | Local job blocks work [Node offline] | UML: localJobBlocked [Node offline] /<br>reason := node_offline; IV 3.4.2; FR-85; FR-237; FR-238; offline Node and blocking local job; independent work continues; one combined notice | TC-31 |
| Running (running) → Waiting (waiting) | Monthly budget reaches 100% | UML: monthlyBudgetReached [usage >= 100%] /<br>reason := budget_review; IV 3.4.2; FR-90; monthly budget 100%; create spending item | TC-33 |
| Waiting (waiting) → Running (running) | User answers [decision] | UML: answerReceived [reason = decision]; IV 3.4.2; corresponding waiting reason resumes running | TC-16 |
| Waiting (waiting) → Running (running) | Node reconnects [node offline] | UML: nodeReconnected [reason = node_offline]; IV 3.4.2; corresponding waiting reason resumes running | TC-31 |
| Waiting (waiting) → Running (running) | Extra spend approved [budget review] | UML: extraSpendApproved [reason = budget_review]; IV 3.4.2; corresponding waiting reason resumes running | TC-33 |
| Running (running) → Ended (ended) | All stages accepted<br>/ result := complete | UML: allStagesAccepted /<br>result := complete; IV 3.4.2; IV 3.4.1 step 10 | TC-09 |
| Running (running) → Ended (ended) | User cancels [authorized]<br>/ result := cancelled | UML: cancel [authorized] /<br>result := cancelled; IV 3.4.2; FR-22; Project Manager or creating Researcher; close pending items; audit | TC-13 |
| Running (running) → Ended (ended) | Unrecoverable technical error<br>/ result := failed_technical | UML: fatalError /<br>result := failed_technical; IV 3.4.2; FR-103; unrecoverable error or missing model/credential; no sample output | TC-12 |
| Running (running) → Ended (ended) | Run token budget exhausted<br>/ result := with_gaps | UML: tokenBudgetExhausted /<br>result := with_gaps; IV 3.4.2; FR-262; publish best output with gaps | TC-32 |
| Waiting (waiting) → Ended (ended) | User cancels [authorized]<br>/ result := cancelled | UML: cancel [authorized] /<br>result := cancelled; IV 3.4.2; FR-22 | TC-13 |
| Waiting (waiting) → Ended (ended) | Run token budget exhausted<br>/ result := with_gaps | UML: tokenBudgetExhausted /<br>result := with_gaps; IV 3.4.2; FR-262; any waiting reason | TC-32 |
| Waiting (waiting) → Ended (ended) | Pinned wait expires [unanswered]<br>/ result := with_gaps | UML: waitDeadlinePassed [reason = decision and pinned item unanswered] /<br>result := with_gaps; IV 3.4.2; FR-262; FR-265; close pinned item unanswered | TC-98; TC-100 |
| Waiting (waiting) → Ended (ended) | Spending declined or expired [budget review]<br>/ result := with_gaps | UML: spendingDeclinedOrExpired [reason = budget_review] /<br>result := with_gaps; IV 3.4.2; FR-245; FR-91 | TC-33 |
| Waiting (waiting) → Ended (ended) | Unrecoverable technical error<br>/ result := failed_technical | UML: fatalError /<br>result := failed_technical; IV 3.4.2; FR-103; unrecoverable error or missing model/credential | TC-12 |
| Ended (ended) → Final | (nối đường) | Completion of Run lifecycle; result remains stored; no record deletion | Design completion check |

## 5. Research Engines

IV 3.4.3, Figure IV-8; IV 3.11; IV 3.8.

Phạm vi một version; Under review bao gồm công việc sửa bất đồng bộ và chạy lại checks. Chỉ rời review qua nhánh revision checks completed khi kết quả đã có, tối đa hai vòng; findings còn lại là known risks hoặc chờ người dùng theo IV 3.11. Stale version giữ để truy vết; acceptance upstream và rerun downstream là công việc/version mới, không tự phục hồi version cũ. Transition phục hồi cụ thể chưa được nguồn chốt, nằm ngoài view. Vòng đời đầu ra Hand-off Object của engine: đủ draft, checks_red, checks_green, in_review, ready, accepted, locked, stale. Locked chỉ cho AnalysisPlan; không phải mọi object phải qua locked. Các đường upstream changed chỉ khi pinned upstream có version mới; từ đủ bảy state còn lại có thể thoát qua transition kế thừa của composite sang Stale theo câu “Any state can move to stale” ở IV 3.4.3. Theo yêu cầu mới, bảy state chưa stale nằm trong composite Current version (not stale), còn Stale ở ngoài. Một transition upstreamVersionChanged từ composite tới Stale áp dụng khi pinned upstream có version mới, thay cho bảy transition giống nhau. Initial ngoài vào composite, initial trong vào Draft. Đây là một region tuần tự, không phải các state đồng thời. Luồng chính giữ bước hàng 200, state/choice cao 80 và khoảng trống dọc 120 trước scale; không còn junction invalidation. Các đường checks/revision quay lại có hành lang riêng. round trên ảnh là alias revision rounds, giữ đặc tả đầy đủ trong transition-spec. Stale chưa hoàn tất vòng đời nên không gắn final. Toàn bộ vòng đời ở một graph, mỗi state chỉ xuất hiện một lần; model-state giữ code nguồn. Accepted version bất biến; muốn thay nội dung phải tạo version mới. Không tự vẽ stale → accepted hoặc tự động refresh dữ liệu.

| Transition | Nhãn ngắn | Điều kiện / nguồn đầy đủ | Test reference |
|---|---|---|---|
| Initial → Draft (draft) | / round := 0 | UML: / revision rounds := 0; IV 3.4.3 | TC-11 |
| Draft (draft) → Are all contract<br>items green? | checks completed | UML: checks completed; IV 3.4.3 | TC-11; TC-27 |
| Are all contract<br>items green? → Checks failed (checks_red) | [No] | UML: [No]; IV 3.4.3; guard: at least one contract item red | TC-11; TC-27 |
| Are all contract<br>items green? → Checks passed (checks_green) | [Yes] | UML: [Yes]; IV 3.4.3; guard: all contract items green | TC-11; TC-27 |
| Checks failed (checks_red) → Are all contract<br>items green? | Checks rerun | UML: object revised; checks rerun; IV 3.4.3; IV review loop | TC-27 |
| Checks passed (checks_green) → Are all contract<br>items green? | contract check changed | UML: contract check changed; IV 3.4.3 | TC-11; TC-27 |
| Checks passed (checks_green) → Under review (in_review) | review started | UML: review started; IV 3.4.3; IV review loop | TC-27 |
| Under review (in_review) → Are all contract<br>items green? | Revision checked [round < 2]<br>/ round += 1 | UML: revision checks completed [revision rounds < 2]<br>/ revision rounds += 1; IV 3.11 steps 6-8; FR-75; completed revision and checks, at most two revision rounds per version | TC-27 |
| Under review (in_review) → Ready for acceptance (ready) | review completed | UML: review completed; IV 3.4.3 | TC-27 |
| Ready for acceptance (ready) → Accepted (accepted) | Object accepted | UML: object accepted<br>/ freeze version and hash; IV 3.4.3; FR-161 | TC-11 |
| Accepted (accepted) → Locked (AnalysisPlan) (locked) | Plan locked [AnalysisPlan] | UML: plan locked<br>[AnalysisPlan only]; IV 3.4.3; IV 3.8 | TC-21 |
| Initial → Current version (not stale) | (nối đường) | Diagram scope entry; see page source | Design entry check |
| Current version (not stale) → Stale (stale) | New upstream version | UML: upstreamVersionChanged; IV 3.4.3; FR-19; inherited by draft, checks_red, checks_green, in_review, ready, accepted and locked when pinned upstream version changes; guard: pinned upstream object has a new version | TC-11 |

## 6. AI Principal Investigator

IV 3.6.7; IV 3.5.2; IV 3.13; FR-22/28/31/91/265.

Đủ nhánh human answer, AI PI tentative decision, user confirm/overturn, pinned timeout, spending timeout, cancel khi còn pending/awaiting user review. AI PI chỉ được tentative ở autopilot + away + non-pinned. Overturn undo dependent work, đánh dấu affected objects stale và ghi decision log. Confirm cũng ghi log. Timeout pinned đóng unanswered, end run with gaps, không ai quyết định thay user. Nhãn Pending/Answered/Confirmed/Overturned/Closed là thiết kế từ hành vi, không khẳng định enum implementation.

| Transition | Nhãn ngắn | Điều kiện / nguồn đầy đủ | Test reference |
|---|---|---|---|
| Initial → Pending user decision | (nối đường) | IV 3.5.2; FR-28 | TC-16 |
| Pending user decision → Answered | authorized user answers | UML: authorized user answers<br>/ record decision; IV 3.5.2 step 3; FR-28 | TC-16 |
| Pending user decision → Tentatively decided<br>(awaiting user review) | AI PI decides<br>[autopilot; away; non-pinned] | UML: AI PI decides<br>[autopilot; away; non-pinned]; IV 3.5.2 step 5; FR-31; guard: autopilot and away and not pinned | TC-17 |
| Tentatively decided<br>(awaiting user review) → Does the user<br>confirm? | User confirms or overturns | UML: userDecisionSubmitted; IV 3.5.2 step 6; FR-31 | TC-17 |
| Does the user<br>confirm? → Confirmed | [Yes] | UML: [Yes]; effect: record confirmation in decision log; IV 3.5.2 step 6; FR-31; guard: submitted decision is confirm | TC-17 |
| Does the user<br>confirm? → Overturned | [No] | UML: [No]; effect: undo dependent work; mark affected objects stale; record overturn in decision log; IV 3.5.2 step 6; FR-31; guard: submitted decision is overturn | TC-17 |
| Pending user decision → Closed unanswered<br>(pinned wait deadline) | pinned deadline passed<br>[no answer] | UML: pinned wait deadline passed<br>[no answer]<br>/ end run with gaps; IV 3.5.2 step 4; FR-265; guard: pinned item and no answer | TC-98; TC-100 |
| Pending user decision → Expired unanswered<br>(spending deadline) | spending deadline passed<br>[no answer] | UML: spending deadline passed<br>[no answer]<br>/ end run with gaps; IV 3.13; FR-91; guard: spending item and no answer | TC-33 |
| Pending user decision → Closed<br>(run cancelled) | run cancelled | UML: run cancelled; IV 3.4.1 alternative flow; FR-22; still pending | TC-13 |
| Tentatively decided<br>(awaiting user review) → Closed<br>(run cancelled) | run cancelled | UML: run cancelled; IV 3.4.1 alternative flow; FR-22; awaiting user review | TC-13 |
| Answered → Final | (nối đường) | UML completion within the depicted lifecycle scope; history remains stored | Design completion check |
| Closed unanswered<br>(pinned wait deadline) → Final | (nối đường) | UML completion within the depicted lifecycle scope; history remains stored | Design completion check |
| Expired unanswered<br>(spending deadline) → Final | (nối đường) | UML completion within the depicted lifecycle scope; history remains stored | Design completion check |
| Confirmed → Final | (nối đường) | UML completion within the depicted lifecycle scope; history remains stored | Design completion check |
| Overturned → Final | (nối đường) | UML completion within the depicted lifecycle scope; history remains stored | Design completion check |
| Closed<br>(run cancelled) → Final | (nối đường) | UML completion within the depicted lifecycle scope; history remains stored | Design completion check |

## 7. Notifications & Integrations

IV 2.2.16 notification_emails; IV 2.2.11 integration_deliveries; IV 3.7.

Vòng đời email thông báo đủ pending, sending, sent, failed, skipped theo schema. Điều kiện send/skip và retry scheduled là đề xuất thiết kế từ notification policy/settings và attempts; không lấy lifecycle integration_deliveries làm bằng chứng cho retry email; report chưa chốt thuật toán retry hoặc chuyển tiếp của mọi status. Không tự đặt TTL/retry limit hoặc hứa luôn retry. External notices chỉ cho blocking pinned item và spending item theo policy. Sent biểu diễn kết quả gửi/chấp nhận từ nhà cung cấp, không chứng minh email đến inbox. IntegrationDelivery dùng pending/sending/sent/failed, không có skipped; không coi email và webhook là cùng một enum.

| Transition | Nhãn ngắn | Điều kiện / nguồn đầy đủ | Test reference |
|---|---|---|---|
| Initial → Pending | (nối đường) | IV 2.2.16 notification_emails; IV 3.7 | TC-38 |
| Pending → Should the email<br>be sent? | Dispatch requested | UML: dispatchRequested; IV 2.2.16; FR-100; notification settings | TC-38 |
| Should the email<br>be sent? → Skipped | [No] | UML: [No]; IV 2.2.16 skipped; suppression condition proposed from settings; guard: external notice disallowed by policy or preferences | TC-38 |
| Should the email<br>be sent? → Sending | [Yes] | UML: [Yes]; IV 2.2.16 sending; FR-100; guard: external notice allowed by policy and preferences | TC-38 |
| Sending → Was delivery<br>successful? | Delivery result received | UML: deliveryResultReceived; IV 2.2.16 | TC-38 |
| Was delivery<br>successful? → Failed | [No] | UML: [No]; IV 2.2.16 failed; guard: delivery failed | TC-38 |
| Was delivery<br>successful? → Sent | [Yes] | UML: [Yes]; IV 2.2.16 sent; provider accepted, not inbox proof; guard: provider accepted delivery | TC-38 |
| Failed → Pending | retry scheduled<br>(proposed) | UML: retry scheduled<br>(proposed); Design proposal for notification_emails; IV 2.2.16 attempts does not establish retry policy; no confirmed retry limit or terminal failure rule | Design retry check |
| Skipped → Final | (nối đường) | UML completion within the depicted lifecycle scope; history remains stored | Design completion check |
| Sent → Final | (nối đường) | UML completion within the depicted lifecycle scope; history remains stored | Design completion check |

## 8. Administration & Monitoring

III 3.9.9; IV 2.2.38 monitoring_alerts; IV 3.8; FR-104.

Vòng đời một monitoring alert: active/resolved theo schema. Acknowledge là self-transition ghi acknowledged_at/by, không đồng nghĩa resolve. Resolution reported là event thiết kế cho việc ghi nhận resolved và resolved_at; nối trực tiếp Active tới Resolved, không thêm choice chỉ để đọc status. Không khẳng định ai hoặc thuật toán nào tự resolve. Không tự thêm reopen resolved alert; sự cố mới có thể là alert mới nhưng nguồn chưa chốt identity rule.

| Transition | Nhãn ngắn | Điều kiện / nguồn đầy đủ | Test reference |
|---|---|---|---|
| Initial → Active alert | (nối đường) | IV 2.2.38 monitoring_alerts active; FR-104 | TC-05 |
| Active alert → Active alert | acknowledged | UML: acknowledged; III 3.9.9; IV 2.2.38 acknowledged_at; acknowledgement does not resolve status | TC-05 |
| Active alert → Resolved alert | resolution reported<br>/ record resolved_at | UML: resolution reported<br>/ record resolved_at; IV 2.2.38 status resolved; resolved_at; design event abstraction, no resolver or automatic resolution algorithm specified | TC-05 |
| Resolved alert → Final | (nối đường) | UML completion within the depicted lifecycle scope; history remains stored | Design completion check |

## 9. Dossier Version

IV 3.14; FR-94–98, FR-249–253.

Vòng đời một Dossier version: Not approved, Approved và Superseded. Export cần approved và pinned authorization; ghi audit version và format. Version mới cần approval riêng.

| Transition | Nhãn ngắn | Điều kiện / nguồn đầy đủ | Test reference |
|---|---|---|---|
| Initial → Not approved | (nối đường) | IV 3.14; FR-94; FR-249; accepted PaperPack and EvidenceBundle, check hashes | TC-35 |
| Not approved → Enough eligible<br>approvals? | approval recorded | UML: approval recorded; IV 3.14; FR-95; eligible approver under review settings | TC-35 |
| Enough eligible<br>approvals? → Not approved | [No] | UML: [No]; FR-95; fewer eligible approvals than required; guard: eligible approvals below requirement | TC-35 |
| Enough eligible<br>approvals? → Approved | [Yes] | UML: [Yes]; FR-95; enough eligible approvals; guard: eligible approvals meet review settings | TC-35 |
| Approved → Approved | pinned export authorized<br>/ export; audit version + format | UML: pinned export authorized<br>/ export; audit version + format; FR-97; FR-98; pinned export approval, audit version and format | TC-36 |
| Not approved → Superseded | new accepted version | UML: new accepted version; FR-96; FR-251; FR-252; new accepted EvidenceBundle or PaperPack; N+1 needs new approvals | TC-35 |
| Approved → Superseded | new accepted version | UML: new accepted version; FR-96; FR-251; FR-252; old approvals retained as history | TC-35 |
| Superseded → Final | (nối đường) | UML completion within the depicted lifecycle scope; history remains stored | Design completion check |

## Review UML theo hai hướng dẫn

Đối chiếu [Visual Paradigm](https://www.visual-paradigm.com/guide/uml-unified-modeling-language/about-state-diagrams/) về trạng thái đối tượng, sự kiện và guard; đối chiếu [draw.io](https://www.drawio.com/docs/diagram-types/uml/state-diagrams/) về shape, initial/final/choice và nhãn transition.

Đã sửa: Yes/No trần thành guard alias [Yes]/[No] có predicate; điều kiện Run hiện trên transition; input confirm/overturn tới trước choice; field reason/result giữ ở context/metadata/thuyết minh, giữ tên state thuần và không thêm ô context lên ảnh compact. Initial không có incoming và chỉ một outgoing không guard/trigger; final không có outgoing. Câu hỏi trong hình thoi và trái/phải là profile người dùng; Research Engines dùng composite với một transition invalidation kế thừa cho bảy state con, không phải hạn chế chung của UML.

| Tab / choice | [Yes] tương ứng | [No] tương ứng |
|---|---|---|
| Authentication & Account / Is code correct<br>and unexpired? | code correct and unexpired | code incorrect or expired |
| Research Engines / Are all contract<br>items green? | all contract items green | at least one contract item red |
| AI Principal Investigator / Does the user<br>confirm? | submitted decision is confirm | submitted decision is overturn |
| Notifications & Integrations / Should the email<br>be sent? | external notice allowed by policy and preferences | external notice disallowed by policy or preferences |
| Notifications & Integrations / Was delivery<br>successful? | provider accepted delivery | delivery failed |
| Dossier Version / Enough eligible<br>approvals? | eligible approvals meet review settings | eligible approvals below requirement |

Các hướng dẫn là nguồn ký pháp, không xác nhận nghiệp vụ project. Notifications/Monitoring và các transition đề xuất vẫn có giới hạn nguồn như từng mục; validator XML không phải chứng nhận formal UML hoặc runtime test.

## Validation

Tái tạo bằng `python diagrams/09-state-machine/build_state_diagrams.py`; export từng tab scale 2, border 20, nền trắng. Kết quả kiểm tra thực tế ghi trong changelog; không suy ra runtime, in A4 hoặc chèn Word từ validator XML.
