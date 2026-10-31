# State Machine Diagrams — các vòng đời theo nhóm chức năng

- [File draw.io chung tám tab](State-Machine-Diagrams.drawio)
- [Builder](build_state_diagrams.py)
- [Rule](rule.md)

Nguồn: `C:/Users/ADMIN/Downloads/FA26SE115_Report7 (1).md`. Cách chia tab theo [Class Diagram](../07-class/Class-Diagrams-design.md), không suy từ số entity lifecycle. Đối chiếu [Report IV](../../report/04-software-design-document.md).

## Inventory

| Tab | PNG | Nguồn |
|---|---|---|
| 1. Authentication & Account | [Authentication-Account](01-Authentication-Account.png) | III 3.9.1; IV 2.2.1 |
| 2. Project Workspace | [Project-Workspace](02-Project-Workspace.png) | III 3.3.1–3.3.3; IV 3.2.14 |
| 3. Data Management | [Data-Management](03-Data-Management.png) | III 3.4.1, 3.4.4, 3.4.5; FR-09 |
| 4. Research Run Orchestration | [Research-Run-Orchestration](04-Research-Run-Orchestration.png) | IV 3.4.2, Figure IV-7; IV 3.13 |
| 5. Research Engines | [Research-Engines](05-Research-Engines.png) | IV 3.4.3, Figure IV-8; IV 3.11; IV 3.8 |
| 6. AI Principal Investigator | [AI-Principal-Investigator](06-AI-Principal-Investigator.png) | IV 3.6.7; IV 3.5.2; IV 3.13; FR-22/28/31/91/265 |
| 7. Notifications & Integrations | [Notifications-Integrations](07-Notifications-Integrations.png) | III 3.8.4; IV 2.2.14 |
| 8. Administration & Monitoring | [Administration-Monitoring](08-Administration-Monitoring.png) | III 3.9.9; IV 2.2.38 monitoring_alerts; IV 3.8; FR-104 |

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

Giữ đầy đủ trạng thái và nhánh; Research Engines và Research Run dùng state phẳng, các transition chung được vẽ riêng từ từng state; các view khác giữ bố cục hiện có. Câu hỏi trong hình thoi, guard [No] trái/[Yes] phải; Yes/No là alias của biểu thức guard ở bảng dưới, không phải event. Nhãn ngắn nằm trực tiếp trên đường nối nền trắng; điều kiện, effect và reference đầy đủ ở bảng dưới. Research Engines có transition riêng từ từng state tới Stale; các nhánh revision giữ đường riêng; không dùng nhãn chung end event. Mỗi vòng đời là một graph liền mạch, mỗi state chỉ xuất hiện một lần; không tách các cụm sự kiện rồi vẽ lại state. Các transition dùng nét liền và đầu mũi tên mặc định có tô. Nhãn theo trigger [guard] / effect; choice chỉ phân nhánh tức thời theo guard; không đợi event ở đường ra. Event userDecisionSubmitted phải tới trước choice confirm/overturn. Reason/result là field context, giá trị và phép gán đầy đủ ở metadata/bảng transition; không cần ô chú thích kỹ thuật riêng trên ảnh theo profile report mẫu. model-state trong XML ánh xạ nhãn dễ đọc về state code nguồn. Đường chính/hồi tiếp vuông góc; transition tới Stale áp dụng khi pinned upstream có version mới. Final đánh dấu kết thúc phạm vi mô tả; tác động lưu trữ phải đọc theo transition và nguồn của từng đối tượng.

Tám tab thể hiện một đối tượng chính cho mỗi nhóm. Dataset available và notification unread/read là cách diễn giải vòng đời, không phải enum xác nhận trong schema. Nhánh Local Node trong Run vẫn là thiết kế dự kiến.

Các status lấy từ nguồn nhưng một enum không tự xác nhận đầy đủ transition. Những nhãn hay transition diễn giải được chỉ rõ trong từng mục. Không đổi nghiệp vụ BRD/PRD/Use Case Spec; không thay placeholder Word. Final UML đánh dấu hoàn tất vòng đời/region; với Dataset, transition vào final là xóa được cho phép, còn ý nghĩa lưu trữ sau xóa chưa được đặc tả. Run có completion từ Ended tới final, result vẫn lưu; Email Code Sign-In kết thúc một lần đăng nhập. Archived và Superseded kết thúc vòng đời trong phạm vi hình, không kết luận record bị xóa hoặc hệ thống không bao giờ có chức năng khôi phục. Các Decision Item đã trả lời/đóng, email Sent/Skipped và alert Resolved đều nối final. Decision Item gom đường vẽ các transition hoàn tất về một final chung; các view khác có thể dùng final riêng. Stale giữ lịch sử version; acceptance/rerun upstream-downstream không phải tự sửa version cũ. Không thêm final/transition phục hồi chưa chốt. Failed có thể giữ nguyên; retry email là đề xuất, không bảo đảm luôn retry.

Test ID trong metadata/bảng là tham chiếu kịch bản, không phải kết quả test runtime. Design routing/retry check là kiểm tra thiết kế còn cần bổ sung, không bịa TC ID.

## Hiệu chỉnh sau review 2026-10-30

Bảo toàn transition-spec trước khi rút gọn nhãn. Nhãn AI PI [eligible] là alias của guard autopilot and away and not pinned; guard đầy đủ, timeout và effect confirm/overturn lưu trong metadata và bảng. Result của Run được giữ trong metadata và bảng. Review bao gồm revision work; sự kiện hoàn tất checks có guard tối đa hai vòng. Phạm vi stale version được ghi trong thuyết minh; email retry ghi proposed. Monitoring dùng resolution reported trực tiếp.

Giới hạn chưa chốt: cách ưu tiên nhiều blocker đồng thời của Run; identity/liên kết item tentative; chính sách retry và kết thúc failure email. Không tự thêm thuật toán hoặc transition cho các điểm này.

## 1. Authentication & Account

III 3.9.1; IV 2.2.1.

Vòng đời account active/suspended; initial active là diễn giải thiết kế, không xác nhận runtime.

| Transition | Nhãn ngắn | Điều kiện / nguồn đầy đủ | Test reference |
|---|---|---|---|
| Initial → Active account (active) | (nối đường) | III 3.2.1; IV 2.2.1 users; initial active is a design interpretation | Design entry check |
| Active account (active) → Suspended account (suspended) | admin suspends account | UML: admin suspends account; III 3.9.1; IV 2.2.1 users status active/suspended | Design transition check |
| Suspended account (suspended) → Active account (active) | admin reactivates account | UML: admin reactivates account; III 3.9.1; IV 2.2.1 users status active/suspended | Design transition check |

## 2. Project Workspace

III 3.3.1–3.3.3; IV 3.2.14.

Vòng đời khái niệm Project gồm Active, Completed, Archived; Archived là read-only. Schema IV 2.2.6 dùng status draft/data_ready/researching/needs_review/completed và archived_at; quan hệ giữa hai cách biểu diễn chưa được đặc tả. Không coi Active/Archived là enum schema. Dossier không thuộc tám hình chính.

| Transition | Nhãn ngắn | Điều kiện / nguồn đầy đủ | Test reference |
|---|---|---|---|
| Initial → Active | (nối đường) | III 3.3.1; FR-04 | TC-03 |
| Active → Completed | marked completed | UML: project marked completed<br>/ write audit entry; III 3.3.3; FR-07 | TC-03; TC-05 |
| Completed → Archived<br>(read-only) | archived | UML: project archived<br>/ write audit entry; III 3.3.3; FR-06; FR-07 | TC-03; TC-05 |
| Active → Archived<br>(read-only) | archived | UML: project archived<br>/ make read-only; audit; III 3.3.3; FR-06; FR-07 | TC-03; TC-05 |
| Active → Active | project updated | UML: project updated<br>/ write audit entry; III 3.3.3; FR-07 | TC-03; TC-05 |
| Archived<br>(read-only) → Final | (nối đường) | UML completion within the depicted lifecycle scope; history remains stored | Design completion check |

## 3. Data Management

III 3.4.1, 3.4.4, 3.4.5; FR-09.

Vòng đời Dataset ở mức khái niệm: tồn tại, thêm version immutable và kết thúc khi xóa được cho phép. Available không phải enum schema; điều kiện xóa chưa được đặc tả đầy đủ.

| Transition | Nhãn ngắn | Điều kiện / nguồn đầy đủ | Test reference |
|---|---|---|---|
| Initial → Dataset available (conceptual_available) | / create first version with hash | UML: / create first version with hash; III 3.4.1; FR-09; IV 3.3; upload or import; conceptual lifecycle not a status enum | Design entry check |
| Dataset available (conceptual_available) → Dataset available (conceptual_available) | new version<br>/ retain prior versions | UML: new version<br>/ retain prior versions; III 3.4.5; FR-09; immutable DatasetVersion | Design transition check |
| Dataset available (conceptual_available) → Final | authorized deletion confirmed | UML: authorized deletion confirmed; III 3.4.4; deletion constraints unspecified | Design transition check |

## 4. Research Run Orchestration

IV 3.4.2, Figure IV-7; IV 3.13.

Một state machine liền mạch, chỉ ba state Running/Waiting/Ended theo enum RunState của Class Diagram và FR-21. Waiting có reason decision/node_offline/budget_review; node_offline khi Node offline và local job chặn việc; reconnect đưa về running, independent work và một combined notice theo FR-237/238; Ended có result complete/with_gaps/failed_technical/cancelled. Đây là field của state, không phải nhiều state trùng tên. Bố cục dọc đặt Running trên Waiting; các transition sang Waiting đi thẳng xuống và các nhánh tiếp tục đi bên phải. Không dùng composite; cancel, fatal error và token exhaustion có transition riêng từ Running và Waiting. Các nhánh chỉ áp dụng Running hoặc Waiting giữ riêng. Metadata và bảng giữ đầy đủ điều kiện và phép gán reason/result. Từ running: all stages accepted, token exhaustion, cancel, technical failure; từ waiting(decision): pinned deadline unanswered, token exhaustion, cancel, technical failure; từ waiting(budget_review): spending decline/expiry, token exhaustion, cancel, technical failure. Không lặp state hay tách các cụm tình huống rời; mỗi transition là nét liền có trigger [guard] / effect khi cần. Tên event/effect là ký hiệu thiết kế từ hành vi, không chốt event/API implementation. Chỉ complete khi tất cả stage accepted. Cancel chỉ bởi Project Manager hoặc creating Researcher. Pinned item không hết hạn trước wait deadline. Khôi phục nhánh node_offline theo yêu cầu mới như thiết kế dự kiến; không khẳng định Local Node đã triển khai.

| Transition | Nhãn ngắn | Điều kiện / nguồn đầy đủ | Test reference |
|---|---|---|---|
| Initial → Running (running) | (nối đường) | IV 3.4.1; FR-14; FR-21 | TC-09 |
| Running (running) → Waiting (waiting) | Decision blocks work | UML: decisionBlocked [present or pinned] /<br>reason := decision; IV 3.4.2; FR-262; no independent work; user present or pinned | TC-16; TC-98 |
| Running (running) → Waiting (waiting) | Node offline | UML: localJobBlocked [Node offline] /<br>reason := node_offline; IV 3.4.2; FR-85; FR-237; FR-238; offline Node and blocking local job; independent work continues; one combined notice | TC-31 |
| Running (running) → Waiting (waiting) | Monthly budget reached | UML: monthlyBudgetReached [usage >= 100%] /<br>reason := budget_review; IV 3.4.2; FR-90; monthly budget 100%; create spending item | TC-33 |
| Waiting (waiting) → Running (running) | Decision answered | UML: answerReceived [reason = decision]; IV 3.4.2; corresponding waiting reason resumes running | TC-16 |
| Waiting (waiting) → Running (running) | Node reconnects | UML: nodeReconnected [reason = node_offline]; IV 3.4.2; corresponding waiting reason resumes running | TC-31 |
| Waiting (waiting) → Running (running) | Extra spend approved | UML: extraSpendApproved [reason = budget_review]; IV 3.4.2; corresponding waiting reason resumes running | TC-33 |
| Running (running) → Ended (ended) | All stages accepted | UML: allStagesAccepted /<br>result := complete; IV 3.4.2; IV 3.4.1 step 10 | TC-09 |
| Waiting (waiting) → Ended (ended) | Pinned wait expires | UML: waitDeadlinePassed [reason = decision and pinned item unanswered] /<br>result := with_gaps; IV 3.4.2; FR-262; FR-265; close pinned item unanswered | TC-98; TC-100 |
| Waiting (waiting) → Ended (ended) | Spending declined or expired | UML: spendingDeclinedOrExpired [reason = budget_review] /<br>result := with_gaps; IV 3.4.2; FR-245; FR-91 | TC-33 |
| Ended (ended) → Final | (nối đường) | Completion of Run lifecycle; result remains stored; no record deletion | Design completion check |
| Running (running) → Ended (ended) | Run cancelled | UML: cancel [authorized] /<br>result := cancelled; IV 3.4.2; FR-22; Project Manager or creating Researcher; close pending items; audit; applies in Running and Waiting | TC-13 |
| Waiting (waiting) → Ended (ended) | Run cancelled | UML: cancel [authorized] /<br>result := cancelled; IV 3.4.2; FR-22; Project Manager or creating Researcher; close pending items; audit; applies in Running and Waiting | TC-13 |
| Running (running) → Ended (ended) | Technical failure | UML: fatalError /<br>result := failed_technical; IV 3.4.2; FR-103; unrecoverable error or missing model/credential; no sample output; applies in Running and Waiting | TC-12 |
| Waiting (waiting) → Ended (ended) | Technical failure | UML: fatalError /<br>result := failed_technical; IV 3.4.2; FR-103; unrecoverable error or missing model/credential; no sample output; applies in Running and Waiting | TC-12 |
| Running (running) → Ended (ended) | Token budget exhausted | UML: tokenBudgetExhausted /<br>result := with_gaps; IV 3.4.2; FR-262; publish best output with gaps; applies in Running and Waiting | TC-32 |
| Waiting (waiting) → Ended (ended) | Token budget exhausted | UML: tokenBudgetExhausted /<br>result := with_gaps; IV 3.4.2; FR-262; publish best output with gaps; applies in Running and Waiting | TC-32 |

## 5. Research Engines

IV 3.4.3, Figure IV-8; IV 3.11; IV 3.8.

Một version của Hand-off Object gồm draft, checks_red, checks_green, in_review, ready, accepted, locked và stale. Mỗi state chưa stale có transition riêng sang Stale khi pinned upstream có version mới; không dùng composite. Locked chỉ áp dụng AnalysisPlan. Revision tối đa hai vòng; Stale giữ lịch sử, không tự phục hồi. Điều kiện, effect và nguồn đầy đủ nằm trong metadata và bảng transition.

| Transition | Nhãn ngắn | Điều kiện / nguồn đầy đủ | Test reference |
|---|---|---|---|
| Initial → Draft (draft) | / round := 0 | UML: / revision rounds := 0; IV 3.4.3 | TC-11 |
| Draft (draft) → Are all contract<br>items green? | checks completed | UML: checks completed; IV 3.4.3 | TC-11; TC-27 |
| Are all contract<br>items green? → Checks failed (checks_red) | [No] | UML: [No]; IV 3.4.3; guard: at least one contract item red | TC-11; TC-27 |
| Are all contract<br>items green? → Checks passed (checks_green) | [Yes] | UML: [Yes]; IV 3.4.3; guard: all contract items green | TC-11; TC-27 |
| Checks failed (checks_red) → Are all contract<br>items green? | Checks rerun | UML: object revised; checks rerun; IV 3.4.3; IV review loop | TC-27 |
| Checks passed (checks_green) → Are all contract<br>items green? | contract check changed | UML: contract check changed; IV 3.4.3 | TC-11; TC-27 |
| Checks passed (checks_green) → Under review (in_review) | review started | UML: review started; IV 3.4.3; IV review loop | TC-27 |
| Under review (in_review) → Are all contract<br>items green? | Revision checked [round < 2] | UML: revision checks completed [revision rounds < 2]<br>/ revision rounds += 1; IV 3.11 steps 6-8; FR-75; completed revision and checks, at most two revision rounds per version | TC-27 |
| Under review (in_review) → Ready for acceptance (ready) | review completed | UML: review completed; IV 3.4.3 | TC-27 |
| Ready for acceptance (ready) → Accepted (accepted) | Object accepted | UML: object accepted<br>/ freeze version and hash; IV 3.4.3; FR-161 | TC-11 |
| Accepted (accepted) → Locked (AnalysisPlan) (locked) | Plan locked [AnalysisPlan] | UML: plan locked<br>[AnalysisPlan only]; IV 3.4.3; IV 3.8 | TC-21 |
| Draft (draft) → Stale (stale) | New upstream version | UML: upstreamVersionChanged; IV 3.4.3; FR-19; inherited by draft, checks_red, checks_green, in_review, ready, accepted and locked when pinned upstream version changes; guard: pinned upstream object has a new version | TC-11 |
| Checks failed (checks_red) → Stale (stale) | New upstream version | UML: upstreamVersionChanged; IV 3.4.3; FR-19; inherited by draft, checks_red, checks_green, in_review, ready, accepted and locked when pinned upstream version changes; guard: pinned upstream object has a new version | TC-11 |
| Checks passed (checks_green) → Stale (stale) | New upstream version | UML: upstreamVersionChanged; IV 3.4.3; FR-19; inherited by draft, checks_red, checks_green, in_review, ready, accepted and locked when pinned upstream version changes; guard: pinned upstream object has a new version | TC-11 |
| Under review (in_review) → Stale (stale) | New upstream version | UML: upstreamVersionChanged; IV 3.4.3; FR-19; inherited by draft, checks_red, checks_green, in_review, ready, accepted and locked when pinned upstream version changes; guard: pinned upstream object has a new version | TC-11 |
| Ready for acceptance (ready) → Stale (stale) | New upstream version | UML: upstreamVersionChanged; IV 3.4.3; FR-19; inherited by draft, checks_red, checks_green, in_review, ready, accepted and locked when pinned upstream version changes; guard: pinned upstream object has a new version | TC-11 |
| Accepted (accepted) → Stale (stale) | New upstream version | UML: upstreamVersionChanged; IV 3.4.3; FR-19; inherited by draft, checks_red, checks_green, in_review, ready, accepted and locked when pinned upstream version changes; guard: pinned upstream object has a new version | TC-11 |
| Locked (AnalysisPlan) (locked) → Stale (stale) | New upstream version | UML: upstreamVersionChanged; IV 3.4.3; FR-19; inherited by draft, checks_red, checks_green, in_review, ready, accepted and locked when pinned upstream version changes; guard: pinned upstream object has a new version | TC-11 |

## 6. AI Principal Investigator

IV 3.6.7; IV 3.5.2; IV 3.13; FR-22/28/31/91/265.

Đủ nhánh human answer, AI PI tentative decision, user confirm/overturn, pinned timeout, spending timeout, cancel khi còn pending/awaiting user review. AI PI chỉ được tentative ở autopilot + away + non-pinned. Overturn undo dependent work, đánh dấu affected objects stale và ghi decision log. Confirm cũng ghi log. Timeout pinned đóng unanswered, end run with gaps, không ai quyết định thay user. Closed khi run cancelled nằm bên phải; các transition hoàn tất dùng chung đường vẽ tới một final, không có junction. Nhãn Pending/Answered/Confirmed/Overturned/Closed là thiết kế từ hành vi, không khẳng định enum implementation.

| Transition | Nhãn ngắn | Điều kiện / nguồn đầy đủ | Test reference |
|---|---|---|---|
| Initial → Pending user decision | (nối đường) | IV 3.5.2; FR-28 | TC-16 |
| Pending user decision → Answered | authorized user answers | UML: authorized user answers<br>/ record decision; IV 3.5.2 step 3; FR-28 | TC-16 |
| Pending user decision → Tentatively decided<br>(awaiting user review) | AI PI decides [eligible] | UML: AI PI decides<br>[autopilot; away; non-pinned]; IV 3.5.2 step 5; FR-31; guard: autopilot and away and not pinned | TC-17 |
| Tentatively decided<br>(awaiting user review) → Does the user<br>confirm? | Decision submitted | UML: userDecisionSubmitted; IV 3.5.2 step 6; FR-31 | TC-17 |
| Does the user<br>confirm? → Confirmed | [Yes] | UML: [Yes]; effect: record confirmation in decision log; IV 3.5.2 step 6; FR-31; guard: submitted decision is confirm | TC-17 |
| Does the user<br>confirm? → Overturned | [No] | UML: [No]; effect: undo dependent work; mark affected objects stale; record overturn in decision log; IV 3.5.2 step 6; FR-31; guard: submitted decision is overturn | TC-17 |
| Pending user decision → Closed unanswered<br>(pinned wait deadline) | Pinned deadline expires | UML: pinned wait deadline passed<br>[no answer]<br>/ end run with gaps; IV 3.5.2 step 4; FR-265; guard: pinned item and no answer | TC-98; TC-100 |
| Pending user decision → Expired unanswered<br>(spending deadline) | Spending deadline expires | UML: spending deadline passed<br>[no answer]<br>/ end run with gaps; IV 3.13; FR-91; guard: spending item and no answer | TC-33 |
| Pending user decision → Closed<br>(run cancelled) | run cancelled | UML: run cancelled; IV 3.4.1 alternative flow; FR-22; still pending | TC-13 |
| Tentatively decided<br>(awaiting user review) → Closed<br>(run cancelled) | run cancelled | UML: run cancelled; IV 3.4.1 alternative flow; FR-22; awaiting user review | TC-13 |
| Answered → Final | (nối đường) | Completion of Decision Item lifecycle; history remains stored | Design completion check |
| Expired unanswered<br>(spending deadline) → Final | (nối đường) | Completion of Decision Item lifecycle; history remains stored | Design completion check |
| Closed unanswered<br>(pinned wait deadline) → Final | (nối đường) | Completion of Decision Item lifecycle; history remains stored | Design completion check |
| Overturned → Final | (nối đường) | Completion of Decision Item lifecycle; history remains stored | Design completion check |
| Confirmed → Final | (nối đường) | Completion of Decision Item lifecycle; history remains stored | Design completion check |
| Closed<br>(run cancelled) → Final | (nối đường) | Completion of Decision Item lifecycle; history remains stored | Design completion check |

## 7. Notifications & Integrations

III 3.8.4; IV 2.2.14.

Vòng đời notification trong ứng dụng theo read_at: unread và read là diễn giải, không phải enum. Email delivery không thuộc tám hình chính.

| Transition | Nhãn ngắn | Điều kiện / nguồn đầy đủ | Test reference |
|---|---|---|---|
| Initial → Unread (read_at is null) | (nối đường) | IV 2.2.14 notifications read_at; conceptual lifecycle | Design entry check |
| Unread (read_at is null) → Read (read_at is set) | recipient marks as read<br>/ record read_at | UML: recipient marks as read<br>/ record read_at; III 3.8.4; IV 2.2.14 notifications | Design transition check |

## 8. Administration & Monitoring

III 3.9.9; IV 2.2.38 monitoring_alerts; IV 3.8; FR-104.

Vòng đời một monitoring alert: active/resolved theo schema. Acknowledge là self-transition ghi acknowledged_at/by, không đồng nghĩa resolve. Resolution reported là event thiết kế cho việc ghi nhận resolved và resolved_at; nối trực tiếp Active tới Resolved, không thêm choice chỉ để đọc status. Không khẳng định ai hoặc thuật toán nào tự resolve. Không tự thêm reopen resolved alert; sự cố mới có thể là alert mới nhưng nguồn chưa chốt identity rule.

| Transition | Nhãn ngắn | Điều kiện / nguồn đầy đủ | Test reference |
|---|---|---|---|
| Initial → Active alert | (nối đường) | IV 2.2.38 monitoring_alerts active; FR-104 | TC-05 |
| Active alert → Active alert | acknowledged | UML: acknowledged; III 3.9.9; IV 2.2.38 acknowledged_at; acknowledgement does not resolve status | TC-05 |
| Active alert → Resolved alert | Resolution reported | UML: resolution reported<br>/ record resolved_at; IV 2.2.38 status resolved; resolved_at; design event abstraction, no resolver or automatic resolution algorithm specified | TC-05 |
| Resolved alert → Final | (nối đường) | UML completion within the depicted lifecycle scope; history remains stored | Design completion check |

## Review UML theo hai hướng dẫn

Đối chiếu [Visual Paradigm](https://www.visual-paradigm.com/guide/uml-unified-modeling-language/about-state-diagrams/) về trạng thái đối tượng, sự kiện và guard; đối chiếu [draw.io](https://www.drawio.com/docs/diagram-types/uml/state-diagrams/) về shape, initial/final/choice và nhãn transition.

Đã sửa: Yes/No trần thành guard alias [Yes]/[No] có predicate; điều kiện Run được lưu trong metadata và bảng transition; input confirm/overturn tới trước choice; field reason/result giữ ở context/metadata/thuyết minh, giữ tên state thuần và không thêm ô context lên ảnh compact. Initial không có incoming và chỉ một outgoing không guard/trigger; final không có outgoing. Câu hỏi trong hình thoi và trái/phải là profile người dùng; Research Engines dùng bảy transition invalidation riêng, không phải hạn chế chung của UML.

| Tab / choice | [Yes] tương ứng | [No] tương ứng |
|---|---|---|
| Research Engines / Are all contract<br>items green? | all contract items green | at least one contract item red |
| AI Principal Investigator / Does the user<br>confirm? | submitted decision is confirm | submitted decision is overturn |

Các hướng dẫn là nguồn ký pháp, không xác nhận nghiệp vụ project. Notifications/Monitoring và các transition đề xuất vẫn có giới hạn nguồn như từng mục; validator XML không phải chứng nhận formal UML hoặc runtime test.

## Validation

Tái tạo bằng `python diagrams/09-state-machine/build_state_diagrams.py`; export từng tab scale 2, border 20, nền trắng. Kết quả kiểm tra thực tế ghi trong changelog; không suy ra runtime, in A4 hoặc chèn Word từ validator XML.
