# Traceability Matrix
## OpenAI-Scientist

**Document Type:** Traceability Matrix\
**Project:** OpenAI-Scientist (capstone FA26SE115)\
**Version:** 1.0 (2026-10-29)\
**Status:** Draft — nguồn nội bộ\
**Liên quan:** [README](README.md) · [BRD](BRD.md) · [PRD](PRD.md) · [Architecture](architecture.md) · [glossary](glossary.md) · [ID mapping](id-mapping.md) · [changelog](changelog.md)

Thuật ngữ theo [glossary.md](glossary.md). ID theo [README §4](README.md).

**Mục đích.** File này là ma trận truy vết duy nhất của các tài liệu nội bộ: BO → BR → FE → FR, NFR → BO/BR/SM, QS và ADR → BR/FR. Cột UC lấy từ Report III (UC và SR). Cột TC lấy từ Report V (test case). Hai cột được trích bằng script từ bảng UC của Report III (mục 2.2) và bảng FR → TC của Report V (mục 4.1.2). Mọi liên kết lấy từ cột BO của BRD, cột Source của PRD và architecture; file này không tạo requirement mới. Cột Source của FR chỉ ghi BR; liên kết FR → ADR chỉ ghi ở Matrix D. Cột Source của NFR chỉ ghi BO, BR hoặc SM; liên kết NFR → QS, ADR, PP và R chỉ ghi ở Matrix C.

---

# 1. Matrix A — BO → BR

Cột BO của BR trong BRD §8 ghi BO cho cả 110 BR. Matrix A lấy nguyên từ cột đó. Một BR có thể phục vụ nhiều BO.

| BO | Mục tiêu (rút gọn) | BR |
|---|---|---|
| BO-01 | Từ research case tới hypothesis và plan có thể review | BR-07, BR-08, BR-15, BR-43, BR-45, BR-46, BR-82, BR-83, BR-85, BR-89, BR-90, BR-93, BR-94, BR-95, BR-96, BR-99, BR-102 |
| BO-02 | Truy vết và replay | BR-10, BR-11, BR-12, BR-16, BR-41, BR-42, BR-47, BR-57, BR-66, BR-67, BR-68, BR-105, BR-107, BR-108 |
| BO-03 | Hàng dữ liệu không rời nơi giữ | BR-17, BR-18, BR-19, BR-20, BR-21, BR-22, BR-81 |
| BO-04 | Kết quả xác nhận không thể p-hacking | BR-44, BR-47, BR-48, BR-49, BR-50, BR-51, BR-52, BR-53, BR-76, BR-84, BR-86, BR-87, BR-88, BR-92, BR-98, BR-105, BR-106, BR-109 |
| BO-05 | Review độc lập và quyền quyết định của người | BR-24, BR-25, BR-26, BR-27, BR-28, BR-29, BR-30, BR-31, BR-32, BR-33, BR-34, BR-35, BR-36, BR-37, BR-38, BR-39, BR-40, BR-75, BR-104, BR-110 |
| BO-06 | Token budget và budget tháng | BR-23, BR-58, BR-59, BR-60, BR-61, BR-78 |
| BO-07 | Cộng tác an toàn theo role | BR-01, BR-02, BR-03, BR-04, BR-05, BR-06, BR-09, BR-80, BR-103 |
| BO-08 | Run luôn kết thúc | BR-13, BR-14, BR-58, BR-60, BR-77, BR-78, BR-104 |
| BO-09 | Đánh giá bằng acceptance scenario và bench | BR-40, BR-97, BR-100, BR-101, BR-107, BR-110 |
| BO-10 | PaperPack không vượt claim ceiling | BR-54, BR-55, BR-56, BR-65, BR-66, BR-67, BR-68, BR-69, BR-70, BR-71, BR-72, BR-73, BR-91, BR-106, BR-108, BR-109 |
| BO-11 | Export cần Dossier đã duyệt | BR-62, BR-63, BR-64, BR-79 |
| BO-12 | (Could) JFE | BR-74 |

# 2. Matrix B — BR → FE → FR

Mỗi dòng là một BR của BRD §8. FE và FR lấy từ cột Source của FR trong PRD §8. UC và TC là hợp của UC và TC phủ các FR của dòng đó (Report III và Report V).

| BR | Chủ đề | FE | FR | UC (Report III) | TC (Report V) |
|---|---|---|---|---|---|
| BR-01 | Đăng nhập không mật khẩu | FE-01 | FR-01 | UC-01 | TC-01 |
| BR-02 | Quyền theo role, cô lập project | FE-01, FE-02, FE-17 | FR-02, FR-101, FR-111, FR-151 | UC-01, UC-09, UC-39 | TC-01, TC-09, TC-39 |
| BR-03 | Project Manager cuối, project archive | FE-02 | FR-04, FR-06 | UC-03 | TC-03 |
| BR-04 | Invitation | FE-02 | FR-05, FR-153 | UC-03 | TC-03 |
| BR-05 | Audit log, comment, notification | FE-02, FE-14, FE-15, FE-17 | FR-07, FR-98..FR-100, FR-104, FR-254, FR-255, FR-258 | UC-05, UC-36..UC-38 | TC-05, TC-36..TC-38 |
| BR-06 | Reviewer đọc mọi object; Platform Admin chỉ xem metadata | FE-01, FE-15 | FR-03, FR-99, FR-152, FR-254 | UC-02, UC-37 | TC-02, TC-37 |
| BR-80 | Project Manager có quyền nghiên cứu của Researcher | FE-02, FE-12 | FR-82, FR-111, FR-233, FR-234 | UC-09, UC-30 | TC-09, TC-48 |
| BR-103 | Đăng nhập bằng Google; cùng user theo email đã xác minh | FE-01 | FR-146 | UC-01 | TC-95, TC-96 |
| BR-07 | Research case; dataset tuỳ chọn | FE-04 | FR-13 | UC-09 | TC-09 |
| BR-08 | Pipeline `dataset_first` | FE-04 | FR-14, FR-15, FR-159 | UC-09, UC-18 | TC-09, TC-18 |
| BR-09 | Một run active mỗi project | FE-04 | FR-16 | UC-09 | TC-09 |
| BR-10 | Amendment của research case | FE-04 | FR-17, FR-160 | UC-10 | TC-10 |
| BR-11 | Hand-off object bất biến | FE-04, FE-09 | FR-18, FR-61, FR-161 | UC-11, UC-23 | TC-11, TC-23 |
| BR-12 | Stale khi upstream đổi | FE-04 | FR-19, FR-162 | UC-11 | TC-11 |
| BR-13 | Contract item và check bằng code | FE-04 | FR-20, FR-163, FR-164 | UC-12 | TC-12 |
| BR-14 | Run luôn kết thúc | FE-04, FE-12, FE-17 | FR-21, FR-85, FR-86, FR-103, FR-165, FR-237..FR-239, FR-257, FR-262, FR-265 | UC-12, UC-30, UC-31 | TC-12, TC-30, TC-31, TC-98, TC-100 |
| BR-15 | Next step sau run | FE-04 | FR-23 | UC-14 | TC-14 |
| BR-16 | Dataset version bất biến | FE-03, FE-12 | FR-09, FR-84, FR-154, FR-236 | UC-06, UC-08 | TC-06, TC-08 |
| BR-17 | Data connection | FE-03 | FR-10, FR-11, FR-155, FR-156 | UC-07 | TC-07 |
| BR-18 | Data location | FE-03, FE-12 | FR-12, FR-79, FR-84, FR-87, FR-157, FR-158, FR-230, FR-236, FR-240 | UC-08 | TC-08 |
| BR-19 | Hàng dữ liệu không rời nơi giữ; release gate | FE-03, FE-12 | FR-12, FR-80, FR-86, FR-157, FR-158, FR-231, FR-239 | UC-08, UC-30 | TC-08, TC-30 |
| BR-20 | Release log | FE-12 | FR-81, FR-232 | UC-30 | TC-48 |
| BR-21 | Disclosure `standard`/`strict`; người trả lời release review | FE-12 | FR-82, FR-233, FR-234 | UC-30 | TC-48 |
| BR-22 | Model chỉ nhận aggregate | FE-12 | FR-83, FR-235 | UC-30 | TC-48 |
| BR-23 | Seal model key và secret | FE-17 | FR-101, FR-102, FR-256 | UC-39 | TC-39 |
| BR-81 | Local Node bị thu hồi | FE-12 | FR-110, FR-241, FR-242 | UC-31 | TC-31 |
| BR-24 | Preset theo stage | FE-02, FE-05 | FR-08, FR-25, FR-147..FR-149, FR-170, FR-171 | UC-04, UC-15 | TC-04, TC-15, TC-97 |
| BR-25 | Action group, level, floor | FE-05 | FR-26, FR-147..FR-150, FR-172 | UC-15 | TC-15, TC-97 |
| BR-26 | Action pinned | FE-05, FE-06, FE-08, FE-09 | FR-27, FR-40, FR-41, FR-48, FR-49, FR-56, FR-117, FR-125, FR-147..FR-150, FR-181..FR-183, FR-185, FR-188, FR-189, FR-192, FR-205 | UC-15, UC-16, UC-18, UC-20..UC-22 | TC-15, TC-16, TC-18, TC-20..TC-22, TC-42, TC-43, TC-97 |
| BR-27 | Presence | FE-05, FE-12 | FR-28, FR-85, FR-173, FR-237, FR-238 | UC-16, UC-31 | TC-16, TC-31 |
| BR-28 | Decision inbox; thông báo ngoài | FE-05, FE-13, FE-15 | FR-29, FR-91, FR-100, FR-174, FR-246, FR-247, FR-255, FR-264 | UC-16, UC-33, UC-38 | TC-16, TC-33, TC-38, TC-99 |
| BR-29 | Decision log, overturn | FE-05, FE-17 | FR-30, FR-105, FR-175, FR-176, FR-259 | UC-05, UC-16 | TC-05, TC-16 |
| BR-30 | AI PI quyết tạm | FE-05 | FR-31, FR-177 | UC-17 | TC-17 |
| BR-31 | AI PI không quyết item pinned, không kết thúc run | FE-05, FE-08 | FR-32, FR-49, FR-178, FR-189, FR-266 | UC-17, UC-21 | TC-17, TC-21, TC-98, TC-100 |
| BR-32 | User và agent dùng chung đường | FE-05 | FR-33, FR-179 | UC-16 | TC-49 |
| BR-33 | Level của acceptance fitness | FE-05 | FR-34, FR-148, FR-150 | UC-15, UC-16 | TC-15, TC-49, TC-97 |
| BR-34 | Lab notebook | FE-05 | FR-35 | UC-14 | TC-14 |
| BR-35 | Review loop bắt buộc | FE-11 | FR-71 | UC-27 | TC-27 |
| BR-36 | Reviewer context mới | FE-11 | FR-72, FR-221 | UC-27 | TC-27 |
| BR-37 | Finding có anchor và evidence | FE-11 | FR-73, FR-222, FR-270 | UC-27 | TC-27 |
| BR-38 | Finding được kiểm trước khi sửa | FE-11 | FR-74, FR-223, FR-224 | UC-27 | TC-27 |
| BR-39 | Tối đa hai vòng sửa; review lại chỉ phần đã sửa | FE-11 | FR-75, FR-225, FR-270, FR-271 | UC-27 | TC-27 |
| BR-40 | Precision persona, seeded-flaw bench | FE-11, FE-17 | FR-77, FR-78, FR-105, FR-135, FR-228, FR-229, FR-259 | UC-05, UC-28, UC-29 | TC-05, TC-28, TC-29, TC-58, TC-101 |
| BR-41 | Số do code tính | FE-04, FE-06, FE-07 | FR-24, FR-39, FR-43, FR-169, FR-186 | UC-12, UC-18, UC-19 | TC-12, TC-18, TC-19 |
| BR-42 | Code chỉ từ chối khi provenance hoặc contract hỏng | FE-11 | FR-76, FR-226, FR-227 | UC-27 | TC-27 |
| BR-43 | DatasetSnapshot | FE-06 | FR-37..FR-39 | UC-18 | TC-18, TC-43 |
| BR-44 | Split theo power | FE-06 | FR-42 | UC-18 | TC-42 |
| BR-45 | HypothesisSet | FE-07 | FR-44, FR-45 | UC-19 | TC-19 |
| BR-46 | AnalysisPlan | FE-08 | FR-46 | UC-20 | TC-20 |
| BR-47 | Lock | FE-08 | FR-48, FR-188 | UC-21 | TC-21 |
| BR-48 | Deviation khỏi thuật toán đã lock | FE-09 | FR-56, FR-205 | UC-22 | TC-22 |
| BR-49 | Envelope và unseal | FE-05, FE-09 | FR-51..FR-53, FR-147..FR-149, FR-199..FR-201 | UC-15, UC-22 | TC-22, TC-97 |
| BR-50 | Sandbox, twin, dry run | FE-08, FE-09 | FR-47, FR-50, FR-197, FR-198 | UC-20, UC-22 | TC-20, TC-22 |
| BR-51 | Lane E và candidate | FE-09 | FR-57, FR-206, FR-207 | UC-24 | TC-24 |
| BR-52 | Tried ledger | FE-09 | FR-58, FR-208 | UC-24 | TC-24 |
| BR-53 | Confirmation tier, evidence e-value, evidence rows | FE-09 | FR-59, FR-209, FR-272 | UC-24 (FR-272: —) | TC-24 (FR-272: —) |
| BR-54 | Verdict do code tính | FE-07, FE-09 | FR-54, FR-61, FR-121, FR-202 | UC-19, UC-23 | TC-23, TC-44 |
| BR-55 | Grade A-D | FE-09 | FR-55, FR-61, FR-203, FR-204 | UC-23 | TC-23 |
| BR-56 | Claim ceiling | FE-09, FE-10 | FR-55, FR-64, FR-203, FR-204, FR-213, FR-214 | UC-23, UC-25 | TC-23, TC-25 |
| BR-57 | EvidenceBundle, replication package | FE-09 | FR-60, FR-61, FR-210, FR-211 | UC-23 | TC-23 |
| BR-58 | Token budget mỗi run | FE-04, FE-13 | FR-88, FR-243, FR-262 | UC-12, UC-32 | TC-32, TC-98 |
| BR-59 | Budget tháng của project | FE-02, FE-13 | FR-08, FR-89, FR-244 | UC-04, UC-32 | TC-04, TC-32 |
| BR-60 | `waiting(budget_review)`, item `spending` | FE-13 | FR-90, FR-245 | UC-33 | TC-33 |
| BR-61 | Floor của `spending`, usage và cost ledger | FE-05, FE-13 | FR-92, FR-93, FR-149, FR-248 | UC-15, UC-34 | TC-34, TC-97 |
| BR-62 | Dossier là tham chiếu | FE-14 | FR-94, FR-249, FR-250 | UC-35 | TC-35 |
| BR-63 | Approval theo review settings | FE-02, FE-14 | FR-08, FR-95 | UC-04, UC-35 | TC-04, TC-35 |
| BR-64 | Export cần Dossier đã duyệt | FE-14 | FR-97, FR-98, FR-253 | UC-36 | TC-36 |
| BR-65 | PaperPack mười item | FE-10 | FR-62 | UC-25 | TC-25 |
| BR-66 | Số trong manuscript là tham chiếu | FE-10 | FR-63, FR-212 | UC-25 | TC-25 |
| BR-67 | Effect statement khớp verdict | FE-10 | FR-64, FR-213, FR-214 | UC-25 | TC-25 |
| BR-68 | Citation trong Literature Base | FE-10 | FR-65, FR-215, FR-216 | UC-25 | TC-25 |
| BR-69 | Limitations đủ độ phủ | FE-10 | FR-66, FR-217 | UC-25 | TC-25 |
| BR-70 | Placeholder "awaiting author" | FE-10 | FR-67, FR-218 | UC-25 | TC-47 |
| BR-71 | Reporting checklist, hình chính | FE-10 | FR-63, FR-68, FR-212, FR-219, FR-220 | UC-25 | TC-25, TC-47 |
| BR-72 | Writing rule H/M/G | FE-10 | FR-69 | UC-25 | TC-47 |
| BR-73 | Researcher quyết định nộp bài | FE-10 | FR-70 | UC-26 | TC-26 |
| BR-74 | JFE (Could, sau MVP) | FE-18 | FR-106..FR-109, FR-260, FR-261 | UC-40 | TC-40 |
| BR-75 | Giả định được ghi vào decision log | FE-05 | FR-36, FR-180 | UC-16 | TC-49 |
| BR-104 | Hạn chờ item pinned; hết hạn thì `ended(with_gaps)`, không ai quyết thay user | FE-02, FE-04, FE-05 | FR-08, FR-32, FR-178, FR-262..FR-266 | UC-04, UC-12, UC-16, UC-17, UC-38 | TC-04, TC-17, TC-38, TC-98, TC-99, TC-100 |
| BR-105 | Claim ledger: tích chỉ giữa nhóm hàng độc lập, record đầu tiên, α là setting | FE-09, FE-20 | FR-272..FR-275 | — | — |
| BR-106 | (Should) Claim status xuyên run | FE-20 | FR-276, FR-277 | — | — |
| BR-107 | (Should) Forecast trong Lock, forecast score | FE-20 | FR-278..FR-280 | — | — |
| BR-108 | (Should) Xác suất của model không quyết định | FE-20 | FR-281 | — | — |
| BR-109 | (Should) Replication run, chữ "replicated" | FE-20 | FR-282..FR-284 | — | — |
| BR-110 | (Should) Planted-truth bench, hidden-error rate, attention budget, ablation | FE-20 | FR-285..FR-287 | — | — |
| BR-76 | Split theo unit of observation và cấu trúc dữ liệu; Researcher xác nhận | FE-06 | FR-40, FR-41, FR-181..FR-183 | UC-18 | TC-18, TC-42 |
| BR-77 | Huỷ run | FE-04 | FR-22, FR-166..FR-168 | UC-13 | TC-13 |
| BR-78 | Hạn trả lời của item `spending` | FE-04, FE-13 | FR-91, FR-246, FR-247, FR-262 | UC-12, UC-33 | TC-33, TC-98 |
| BR-79 | Dossier version mới cần duyệt lại | FE-14 | FR-96, FR-251, FR-252 | UC-35 | TC-35 |
| BR-82 | Claim type gồm `method_comparison` (Should, sau MVP) | FE-19 | FR-139 | UC-41 | TC-41 |
| BR-83 | Task family | FE-08, FE-19 | FR-124, FR-190, FR-191, FR-268 | UC-20, UC-41 | TC-20, TC-41 |
| BR-84 | Cấu trúc dữ liệu có panel; split IID phân tầng lặp lại | FE-06 | FR-113 | UC-18 | TC-42 |
| BR-85 | Dataset shift: ba loại, báo cáo riêng | FE-06 | FR-114 | UC-18 | TC-43 |
| BR-86 | Pipeline order chống leakage | FE-06, FE-08, FE-09 | FR-113, FR-127, FR-131, FR-133 | UC-18, UC-20, UC-22 | TC-22, TC-42, TC-45, TC-46 |
| BR-87 | Vi phạm pipeline order bị chặn hoặc ghi deviation | FE-09 | FR-133 | UC-22 | TC-22 |
| BR-88 | Thời điểm sẵn có của biến; post-outcome; dòng trùng giữa các phần split | FE-06 | FR-115, FR-116, FR-184 | UC-18 | TC-43 |
| BR-89 | Prefilter chỉ dùng phân phối biên; AI gợi ý, user chọn | FE-06 | FR-117, FR-118, FR-185 | UC-18 | TC-43 |
| BR-90 | Hypothesis kiểm được; comparator; baseline không cố ý yếu | FE-07 | FR-119, FR-120, FR-187 | UC-19 | TC-44 |
| BR-91 | Margin δ ánh xạ vùng SESOI; không equivalence từ p-value | FE-07 | FR-121, FR-122 | UC-19 | TC-44 |
| BR-92 | Portfolio: một primary, secondary có giới hạn | FE-07 | FR-123 | UC-19 | TC-44 |
| BR-93 | Evidence family | FE-08, FE-19 | FR-128, FR-267 | UC-20, UC-41 | TC-45, TC-41 |
| BR-94 | Metric `rare-event`; AP không so giữa prevalence; calibration tách dữ liệu | FE-08 | FR-129..FR-131 | UC-20 | TC-46 |
| BR-95 | Research pattern | FE-08 | FR-125, FR-192 | UC-20 | TC-20 |
| BR-96 | Tập pattern theo claim type | FE-08, FE-19 | FR-126, FR-139, FR-193, FR-194, FR-269 | UC-20, UC-41 | TC-20, TC-41 |
| BR-97 | Negative test của pattern | FE-11 | FR-134 | UC-29 | TC-59 |
| BR-98 | Yêu cầu của `method_comparison` | FE-19 | FR-140..FR-145 | UC-41 | TC-41 |
| BR-99 | Baseline policy (pattern F) | FE-07, FE-08, FE-19 | FR-120, FR-132, FR-142, FR-187, FR-195, FR-196 | UC-19, UC-20, UC-41 | TC-41, TC-44, TC-46 |
| BR-100 | Red-team catalogue; SM-17, SM-18 | FE-11 | FR-135..FR-137 | UC-29 | TC-58, TC-101 |
| BR-101 | Benchmark case catalogue | FE-11 | FR-138 | UC-29 | TC-61 |
| BR-102 | Upload nhận Parquet | FE-03 | FR-112 | UC-06 | TC-06 |

# 3. Matrix C — NFR → BO/BR/SM và quality scenario

Cột Source lấy nguyên từ cột Source của NFR trong PRD §9; chỉ chứa BO, BR hoặc SM. Dấu `—` ở Source nghĩa là NFR không dẫn BO, BR hay SM. Cột BO là BO suy ra từ Source: BO ghi trực tiếp, BO của BR (cột BO của BRD §8) và BO của SM (BRD §5). Cột QS là quality scenario của [architecture §10](architecture.md) mà NFR đo. Cột "Liên kết khác" ghi ADR, PP hoặc R liên quan; các liên kết này không phải nguồn của NFR. Dấu `—` nghĩa là tài liệu chưa nêu liên kết (xem §6).

| NFR | Loại | Source (PRD §9) | BO | QS (architecture §10) | Liên kết khác |
|---|---|---|---|---|---|
| NFR-01 | Performance | — | — | — | — |
| NFR-02 | Performance | — | — | — | ADR-02 |
| NFR-03 | Availability/reliability | SM-01 | BO-08 | QS-09, QS-15 | — |
| NFR-04 | Availability/reliability | BR-14 | BO-08 | — | ADR-11; R-12 |
| NFR-05 | Availability/reliability | SM-11 | BO-06 | QS-10 | — |
| NFR-06 | Availability/reliability | BO-08 | BO-08 | — | — |
| NFR-07 | Availability/reliability | BR-11 | BO-02 | — | — |
| NFR-08 | Security | BR-02 | BO-07 | — | ADR-03 |
| NFR-09 | Security | BR-23 | BO-06 | — | — |
| NFR-10 | Security | SM-07 | BO-04 | QS-02, QS-03 | — |
| NFR-11 | Security | BR-05 | BO-07 | — | — |
| NFR-12 | Privacy | SM-05 | BO-03 | QS-06 | — |
| NFR-13 | Privacy | SM-06 | BO-03 | QS-06 | — |
| NFR-14 | Privacy | BR-19 | BO-03 | QS-07 | — |
| NFR-15 | Usability | BO-01 | BO-01 | — | — |
| NFR-16 | Usability | BR-41; BR-30 | BO-02, BO-05 | — | — |
| NFR-17 | Usability | BR-54 | BO-10 | — | — |
| NFR-18 | Accessibility | — | — | — | — |
| NFR-19 | Localisation | — | — | — | — |
| NFR-20 | Maintainability | — | — | — | ADR-02 |
| NFR-21 | Maintainability | — | — | — | PP-07 |
| NFR-22 | Maintainability | — | — | — | — |
| NFR-23 | Observability | BR-29 | BO-05 | — | ADR-02; ADR-05 |
| NFR-24 | Observability | SM-02 | BO-05 | — | R-06 |
| NFR-25 | Replayability | SM-08 | BO-02, BO-04 | QS-05 | — |
| NFR-26 | Replayability | BO-02 | BO-02 | QS-05 | ADR-01 |
| NFR-27 | Integrity và traceability | SM-03 | BO-02, BO-10 | QS-01 | — |
| NFR-28 | Integrity và traceability | SM-12 | BO-10 | QS-04 | — |
| NFR-29 | Integrity và traceability | SM-04 | BO-02, BO-10 | — | — |
| NFR-30 | Integrity và traceability | SM-10 | BO-05 | QS-12 | — |
| NFR-31 | Integrity và traceability | BR-30; BR-31 | BO-05 | QS-11 | — |

# 4. Matrix D — ADR → BR / FR

Cột BR là các BR mà ADR hiện thực, theo phần Decision của ADR. Cột FR gồm FR gắn trực tiếp với ADR, cộng FR của các BR ở cột BR. Đây là nơi duy nhất ghi liên kết FR → ADR.

| ADR | Quyết định | BR | FR |
|---|---|---|---|
| ADR-01 | Pipeline theo stage, năm hand-off object | BR-11, BR-12 | FR-18, FR-19, FR-61, FR-161, FR-162 |
| ADR-02 | Một harness chung | BR-13, BR-32 | FR-20, FR-33, FR-163, FR-164, FR-179 |
| ADR-03 | Platform sở hữu quản trị, không đánh giá khoa học | BR-02, BR-06, BR-47, BR-62 | FR-02, FR-03, FR-48, FR-94, FR-99, FR-101, FR-151, FR-152, FR-188, FR-249, FR-250, FR-254 |
| ADR-04 | Kiểm soát theo loại action | BR-24, BR-25, BR-26, BR-27 | FR-08, FR-25..FR-28, FR-48, FR-49, FR-56, FR-85, FR-147..FR-150, FR-170..FR-173, FR-188, FR-189, FR-205, FR-237, FR-238 |
| ADR-05 | Một decision inbox, theo dõi overturn | BR-28, BR-29 | FR-29..FR-31, FR-91, FR-100, FR-105, FR-174..FR-177, FR-246, FR-247, FR-255, FR-259 |
| ADR-06 | Review độc lập bắt buộc | BR-35, BR-36, BR-37, BR-38, BR-39, BR-40 | FR-71..FR-75, FR-77, FR-78, FR-105, FR-221..FR-225, FR-228, FR-229, FR-259, FR-270, FR-271 |
| ADR-07 | Số và verdict từ code | BR-41, BR-54, BR-55, BR-56, BR-66 | FR-24, FR-39, FR-43, FR-54, FR-55, FR-61, FR-63, FR-64, FR-169, FR-186, FR-202..FR-204, FR-212..FR-214 |
| ADR-08 | Lock, envelope, unseal ở Platform | BR-47, BR-49 | FR-48, FR-51..FR-53, FR-147..FR-149, FR-188, FR-199..FR-201 |
| ADR-09 | Split theo power, tier xác nhận | BR-26, BR-44, BR-53, BR-76 | FR-27, FR-40..FR-42, FR-59, FR-113, FR-147..FR-150, FR-181..FR-183, FR-209, FR-272 |
| ADR-10 | Local Node, release gate | BR-18, BR-19, BR-20, BR-21, BR-22, BR-50, BR-81 | FR-12, FR-47, FR-50, FR-79..FR-84, FR-86, FR-87, FR-110, FR-157, FR-158, FR-197, FR-198, FR-230..FR-236, FR-239..FR-242 |
| ADR-11 | Self-healing, một budget mỗi run, hạn chờ item pinned | BR-13, BR-14, BR-58, BR-104 | FR-08, FR-20, FR-21, FR-32, FR-43, FR-85, FR-86, FR-88, FR-103, FR-163..FR-165, FR-178, FR-186, FR-237..FR-239, FR-243, FR-257, FR-262..FR-266 |
| ADR-12 | Dossier là tham chiếu | BR-62, BR-63, BR-64, BR-79 | FR-08, FR-94..FR-98, FR-249..FR-253 |
| ADR-13 | Một run active mỗi project | BR-09 | FR-16 |
| ADR-14 | Dataset tuỳ chọn, `dataset_first` | BR-07, BR-08 | FR-13..FR-15, FR-159 |
| ADR-15 | Budget tháng, `waiting(budget_review)` | BR-59, BR-60, BR-78 | FR-08, FR-89..FR-91, FR-244..FR-247 |
| ADR-16 | Tài liệu ở mức khái niệm | — | — |
| ADR-17 | Research pattern registry, pipeline order | BR-86, BR-87, BR-88, BR-89, BR-95, BR-97 | FR-115..FR-118, FR-124..FR-127, FR-131..FR-134, FR-184, FR-185, FR-190..FR-196 |
| ADR-18 | Claim type `method_comparison` (Should, sau MVP) | BR-82, BR-96, BR-98 | FR-126, FR-139..FR-145, FR-193, FR-194, FR-267..FR-269 |
| ADR-19 | Evidence e-value chỉ nhân giữa nhóm hàng độc lập | BR-53, BR-105 | FR-209, FR-272..FR-275 |
| ADR-20 | Claim status là mức claim ceiling xuyên run (Should) | BR-106 | FR-276, FR-277 |

# 4a. Matrix E — FE-19, FE-20 và SM có FR đo trực tiếp

Ma trận này ghi FE-19, FE-20 và các SM mà một FR đo trực tiếp (SM-02, SM-16, SM-17, SM-18, SM-19..SM-22). Các SM còn lại không có FR riêng.

| Mục | Nội dung | BO | BR | FR |
|---|---|---|---|---|
| FE-19 | Method comparison research (Should, sau MVP) | BO-01, BO-04 | BR-82, BR-83, BR-93, BR-96, BR-98, BR-99 | FR-139..FR-145, FR-194, FR-267..FR-269 |
| FE-20 | Claim ledger, forecast and replication (Should) | BO-02, BO-04, BO-05, BO-09, BO-10 | BR-106..BR-110 | FR-274..FR-287 |
| SM-02 | Số question, thời gian bị chặn, overturn rate mỗi run; target chưa xác định (Câu hỏi mở 1) | BO-05 | BR-29, BR-40 | FR-105 |
| SM-16 | (Sau MVP) Feature của journal profile truy được về corpus snapshot và span | BO-12 | BR-74 | FR-107 |
| SM-17 | Tỷ lệ phát hiện leakage cài sẵn; target chưa xác định (Câu hỏi mở 3) | BO-09 | BR-100 | FR-135, FR-136 |
| SM-18 | Tỷ lệ chặn vi phạm pipeline order cài sẵn; target chưa xác định (Câu hỏi mở 3) | BO-09 | BR-100, BR-86 | FR-135, FR-137 |
| SM-19 | (Should) Forecast score theo run và project | BO-02, BO-09 | BR-107 | FR-280 |
| SM-20 | (Should) Phần claim key `promoted` trên ít nhất hai snapshot | BO-04, BO-09 | BR-105, BR-109 | FR-273, FR-274 |
| SM-21 | (Should) Hidden-error rate trên planted-truth bench | BO-05, BO-09 | BR-110 | FR-286 |
| SM-22 | (Should) Attention budget trên planted-truth bench | BO-05, BO-09 | BR-110 | FR-286 |

# 5. Coverage summary

**Phương pháp.** Một script đọc BRD §8 (bảng BR) và PRD §8 (bảng FR, cột Source). Nó đếm BR, gán FR vào BR theo token `BR-nn` trong cột Source, và kiểm FR không có token `BR-nn`. Số đếm là ở mức ID: một BR "được phủ" khi có ít nhất một FR dẫn nó. Script không kiểm từng mệnh đề trong BR.

| Chỉ số | Giá trị |
|---|---|
| Số BR trong BRD §8 | 110 |
| BR được phủ bởi ít nhất một FR | 110 |
| BR không có hành vi sản phẩm (`n/a`) | 0 |
| BR có hành vi nhưng không có FR | 0 |
| Số FR trong PRD §8 | 287 |
| FR không có BR nguồn | 0 |
| FR không xuất hiện trong Matrix B | 0 |
| FR Must | 256 |
| FR Should (FE-19 `method_comparison`: 11; FE-20: 14) | 25 |
| FR Could (FE-18, JFE) | 6 |
| BR có BO trong cột BO của BRD | 110 |
| BR không có BO | 0 |
| Số UC trong Report III | 41 |
| Số TC trong Report V | 101 |
| FR có ít nhất một UC | 271 |
| FR không có UC | 16 (FR-272..FR-287, G8) |
| FR Must có ít nhất một TC | 254 (FR-272, FR-273 chưa có, G8) |
| FR Should và Could có ít nhất một TC | 17 |
| FR không có TC | 16 (G8) |
| Dòng Matrix B có cột UC và TC khác `—` | 104 (BR-105..BR-110 chưa có, G8) |

# 6. Khoảng trống (gaps)

File này không sửa BRD hay PRD. Các mục dưới đây là khoảng trống còn mở.

| # | Khoảng trống | Đề xuất |
|---|---|---|
| G1 | BO-09 (đánh giá bằng scenario và bench) có BR-40, BR-97, BR-100 và BR-101 (red-team catalogue và benchmark case catalogue). Acceptance scenario và paper reproduction bench (SM-13, SM-14) nằm ở PRD §11, không có BR hay FR. | Quyết định: thêm BR/FR cho bench, hoặc ghi rõ BO-09 được hiện thực bằng tiêu chí phát hành (PRD §11). |
| G2 | NFR không có BO, BR hoặc SM nguồn: NFR-01, NFR-02, NFR-18, NFR-19, NFR-20, NFR-21, NFR-22. NFR-02 và NFR-20 liên quan ADR-02; NFR-21 liên quan PP-07 (Matrix C, cột "Liên kết khác"). | PRD thêm BR, BO hoặc SM nguồn nếu cần truy vết đầy đủ. |
| G3 | NFR không có QS: NFR-01, NFR-02, NFR-04, NFR-06, NFR-07, NFR-08, NFR-09, NFR-11, NFR-15, NFR-16, NFR-17, NFR-18, NFR-19, NFR-20, NFR-21, NFR-22, NFR-23, NFR-24, NFR-29. Các NFR này chưa có quality scenario ở architecture §10. | Thêm QS cho NFR quan trọng, hoặc chấp nhận kiểm bằng cách đo nêu trong PRD §9. |
| G4 | QS không được NFR nào dẫn: QS-08 (QS-08: item hết phần budget thành `needs-you`). BR-13 và BR-58 có FR, nhưng không có NFR đo chỉ số này. | PRD thêm NFR cho QS-08, hoặc ghi QS-08 là scenario của FR-20. |
| G5 | ADR-02 không có FR dẫn trực tiếp; nó chỉ được NFR-20 và NFR-23 hiện thực. ADR-16 là quyết định về cách viết tài liệu, không có BR hay FR; NFR-22 đo gián tiếp. | Chấp nhận. Không cần FR cho ADR-16. |
| G7 | Số đếm phủ ở mức ID, không ở mức mệnh đề. Một BR nhiều mệnh đề (ví dụ BR-65, BR-26) có thể chỉ được phủ một phần bởi FR dẫn nó. | Kiểm theo mệnh đề khi viết UC và TC. |
| G8 | FR-272 đến FR-287 và BR-105 đến BR-110 (lõi khoa học xuyên run, thêm 2026-10-29) chưa có UC trong Report III và TC trong Report V. FR-272 và FR-273 là Must. | Thêm UC và TC cho FR-272, FR-273 trước stage acceptance; thêm cho FE-20 khi FE-20 vào MVP (BRD §7.1). |

G6 (cột UC và TC trống) đã đóng ngày 2026-10-29 cho 271 FR và 104 BR. FR-263 đến FR-271 và BR-104 được phủ bởi UC (Report III) và TC (Report V) cùng ngày. Mã G6 không dùng lại.

Không có BR có hành vi mà thiếu FR (110 BR, 287 FR, đếm lại bằng script ngày 2026-10-29). Không có FR dẫn BR không tồn tại. Không có FR thiếu BR nguồn.

# 7. Cách cập nhật

1. Khi thêm BR: ghi ít nhất một BO trong cột BO của BRD, rồi thêm dòng vào Matrix B và Matrix A. Nếu BR không có hành vi sản phẩm, ghi `n/a` và một dòng lý do.
2. Khi thêm FR: dẫn ít nhất một BR trong cột Source của PRD, rồi cập nhật Matrix B. Nếu FR hiện thực một ADR, cập nhật Matrix D.
3. Khi thêm NFR hoặc QS: cập nhật Matrix C.
4. Khi viết UC (Report III) hoặc TC (Report V): điền cột UC hoặc TC của mọi FR liên quan và giữ G6 ở trạng thái đã đóng khi cột đầy đủ.
5. Khi BR, FR, UC hoặc TC bị bỏ: giữ dòng, ghi Deprecated với ngày, lý do và ID thay thế (README §4).
6. Cập nhật file này trong cùng thay đổi với BRD, PRD hoặc architecture, và ghi vào [changelog](changelog.md). ID theo [README §4](README.md); số lượng ở §5 phải được tính lại.
