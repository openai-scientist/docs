const pptxgen = require("pptxgenjs");
const path = require("path");
const ROOT = path.resolve(__dirname, "../..");
const OUT = path.join(ROOT, "docs/slides/FA26SE115_Review2.pptx");
const A = (f) => path.join(ROOT, "docs/slides/assets", f);
const I = (f) => path.join(ROOT, "docs/slides/assets/icons", f + ".png");
const TI = (f) => path.join(ROOT, "docs/slides/assets/tech", f + ".png");
const D = (p) => path.join(ROOT, p);

/* Design tokens lifted from Review 1 - Capstone.pptx */
const T = {
  ink: "111827", ink2: "1F2937", body: "475467", muted: "667085", faint: "98A2B3",
  line: "E4E4E0", line2: "EDEDEA", surf: "F7F7F5", peach: "FDEBD3", peachSoft: "FFF4E6",
  amber: "8A4B08", orange: "E38B29", white: "FFFFFF",
  /* nền sáng thay cho khối tối: xanh xám nhạt cho phần do code xử lý */
  soft: "EEF2F6", softLine: "C9D2DE",
};
const HEAD = "Be Vietnam Ultra-Bold";
const BODY = "Be Vietnam";

/* 20" x 11.25" canvas, same as Review 1 */
const W = 20, H = 11.25, MX = 1.33, CW = 17.85;

const pres = new pptxgen();
pres.defineLayout({ name: "R1", width: W, height: H });
pres.layout = "R1";
pres.theme = { headFontFace: HEAD, bodyFontFace: BODY };
pres.author = "GFA26SE78";
pres.title = "OpenAI-Scientist - Review 2";

/* ---------- chrome ---------- */
function chrome(s, opts = {}) {
  s.addImage({ path: A("corner-swirl.png"), x: 13.9, y: -1.25, w: 7.2, h: 6.72, transparency: 45, objectName: "deco-tr" });
  s.addImage({ path: A("wave-a.png"), x: -0.95, y: -0.5, w: 5.0, h: 2.09, transparency: 45, objectName: "deco-tl" });
  s.addImage({ path: A("corner-swirl.png"), x: -1.6, y: 7.4, w: 5.6, h: 5.22, transparency: 50, objectName: "deco-bl" });
  s.addImage({ path: A("fpt-university.png"), x: 17.4, y: 0.38, w: 1.78, h: 0.7, objectName: "logo-fpt" });
  /* Lockup sản phẩm: mark cộng tên hệ thống, đặt sát mép trái */
  s.addImage({ path: A("product-mark.png"), x: MX, y: 0.3, w: 0.86, h: 0.86, objectName: "logo-mark" });
  s.addText("OpenAI Scientist", { x: MX + 1.02, y: 0.3, w: 3.6, h: 0.86, isTextBox: true, margin: 0, valign: "middle", fontSize: 21, bold: true, color: T.ink, fontFace: HEAD });
  if (!opts.noNumber) s.addText(String(opts.n), { x: 18.2, y: 10.15, w: 0.98, h: 0.4, isTextBox: true, margin: 0, align: "right", fontSize: 18, color: T.muted, fontFace: BODY });
}

let N = 0;
function slide(sectionTitle, eyebrow, title, opts = {}) {
  N += 1;
  const s = pres.addSlide({ sectionTitle });
  s.background = { color: T.white };
  chrome(s, { n: N });
  /* Eyebrow là title chính, title dài cũ chỉ còn trong tham số và không vẽ ra */
  if (eyebrow)
    s.addText(eyebrow.toUpperCase(), { x: MX, y: 1.45, w: CW, h: 0.9, isTextBox: true, margin: 0, fontSize: opts.titleSize || 40, bold: true, charSpacing: 2, color: T.ink, fontFace: HEAD, valign: "middle" });
  return s;
}
/* small uppercase column label, as on Review 1 slide 5 */
function colLabel(s, text, x, y, w, color) {
  s.addText(text.toUpperCase(), { x, y, w, h: 0.34, isTextBox: true, margin: 0, fontSize: 16, bold: true, charSpacing: 1.8, color: color || T.ink2, fontFace: HEAD });
}
/* card: rounded surface with optional heading + body */
function card(s, o) {
  const fill = o.fill || T.white;
  s.addShape(pres.ShapeType.roundRect, {
    x: o.x, y: o.y, w: o.w, h: o.h, fill: { color: fill }, rectRadius: 0.12,
    line: { color: o.border || (fill === T.white ? T.line : fill), width: 1 }, objectName: o.name || "card",
  });
  const runs = [];
  if (o.n) runs.push({ text: o.n + "   ", options: { fontSize: o.nSize || 22, bold: true, color: T.faint, fontFace: HEAD } });
  if (o.h1) runs.push({ text: o.h1, options: { fontSize: o.h1Size || 20, bold: true, color: o.h1Color || T.ink, fontFace: HEAD, breakLine: !!o.b } });
  if (o.b) runs.push({ text: o.b, options: { fontSize: o.bSize || 16.5, color: o.bColor || T.body, fontFace: BODY } });
  s.addText(runs, { x: o.x + 0.3, y: o.y + 0.18, w: o.w - 0.6, h: o.h - 0.36, isTextBox: true, margin: 0, valign: o.valign || "top", lineSpacingMultiple: 1.12 });
}
function cardGrid(s, items, o) {
  const { x = MX, y, w = CW, h, cols = 3, gapX = 0.35, gapY = 0.3 } = o;
  const cw = (w - gapX * (cols - 1)) / cols;
  items.forEach((it, i) => {
    card(s, Object.assign({}, it, {
      x: x + (i % cols) * (cw + gapX), y: y + Math.floor(i / cols) * (h + gapY), w: cw, h, name: `card-${i}`,
    }));
  });
}
/* danh sách đánh số: trang chỉ cần vài ý, không cần card */
function numbered(s, items, o = {}) {
  const y0 = o.y || 3.3, step = o.step || 2.05, size = o.size || 24;
  items.forEach((t, i) => {
    const y = y0 + i * step;
    s.addText(String(i + 1), { x: MX, y, w: 0.75, h: 0.6, isTextBox: true, margin: 0, fontSize: size + 2, bold: true, color: T.orange, fontFace: HEAD });
    s.addText(t, { x: MX + 0.85, y, w: CW - 1.6, h: step - 0.2, isTextBox: true, margin: 0, fontSize: size, color: T.ink, fontFace: BODY, lineSpacingMultiple: 1.25, valign: "top" });
  });
}
/* bottom callout bar, like Review 1 slide 5 */
function callout(s, text, y, tone) {
  const fill = tone === "peach" ? T.peachSoft : T.surf;
  s.addShape(pres.ShapeType.roundRect, { x: MX, y, w: CW, h: 0.82, fill: { color: fill }, rectRadius: 0.12, line: { color: fill }, objectName: "callout" });
  s.addText(text, { x: MX + 0.45, y: y + 0.06, w: CW - 0.9, h: 0.7, isTextBox: true, margin: 0, fontSize: 19, color: tone === "peach" ? T.amber : T.ink2, fontFace: BODY, valign: "middle" });
}
/* light table in the Review 1 palette */
function table(s, rows, o) {
  if (o && o.fillTo) { o = Object.assign({}, o); o.rowH = (o.fillTo - o.y) / rows.length; delete o.fillTo; }
  const opts = Object.assign({ x: MX, w: CW, fontSize: 15, color: T.body, fontFace: BODY, valign: "middle", autoPage: false,
    border: { type: "solid", color: T.line, pt: 0.75 } }, o);
  const head = rows[0].map((t) => ({ text: t, options: { bold: true, color: T.ink2, fill: { color: T.surf }, fontSize: opts.fontSize, fontFace: HEAD } }));
  const body = rows.slice(1).map((r) =>
    r.map((t, ci) => ({ text: t, options: { color: ci === 0 ? T.ink : T.body, bold: ci === 0, fill: { color: T.white } } }))
  );
  s.addTable([head, ...body], opts);
}
function note(s, text, y, color) {
  s.addText(text, { x: MX, y: y || 10.15, w: 15.5, h: 0.46, isTextBox: true, margin: 0, fontSize: 18, color: color || T.muted, fontFace: BODY, valign: "top" });
}

/* box có chữ căn giữa, dùng cho sơ đồ vẽ bằng shape gốc */
function box(s, x, y, w, h, text, o = {}) {
  s.addShape(pres.ShapeType.roundRect, { x, y, w, h, fill: { color: o.fill || T.white }, rectRadius: o.r || 0.1, line: { color: o.border || o.fill || T.line, width: 1 }, objectName: o.name || "box" });
  s.addText(text, { x: x + 0.1, y, w: w - 0.2, h, isTextBox: true, margin: 0, align: o.align || "center", valign: "middle", fontSize: o.size || 17, bold: o.bold !== false, color: o.color || T.ink, fontFace: o.bold === false ? BODY : HEAD, lineSpacingMultiple: 1.05 });
}
function arrow(s, x, y, w, h, color) {
  /* PowerPoint không nhận kích thước âm: đổi sang flip để mũi tên hướng lên hoặc sang trái vẫn đúng chiều */
  const flipV = h < 0, flipH = w < 0;
  if (flipV) { y += h; h = -h; }
  if (flipH) { x += w; w = -w; }
  s.addShape(pres.ShapeType.line, { x, y, w, h, flipV, flipH, line: { color: color || T.faint, width: 1.75, endArrowType: "triangle" }, objectName: "arrow" });
}
/* ảnh giữ đúng tỉ lệ, căn giữa trong khung */
function fitImage(s, p, pxW, pxH, bx, by, bw, bh) {
  const r = Math.min(bw / pxW, bh / pxH), w = pxW * r, h = pxH * r;
  s.addImage({ path: p, x: bx + (bw - w) / 2, y: by + (bh - h) / 2, w, h });
}
const STAGES = [
  ["Dataset", "hiểu dữ liệu", "DatasetSnapshot"],
  ["Hypothesis", "đặt giả thuyết", "HypothesisSet"],
  ["Experiment Design", "lập kế hoạch", "AnalysisPlan + Lock"],
  ["Execution", "chạy phân tích", "EvidenceBundle"],
  ["Paper", "viết bài", "PaperPack"],
];

/* ======================= 1. TITLE ======================= */
pres.addSection({ title: "Mở đầu" });
{
  N = 1;
  const s = pres.addSlide({ sectionTitle: "Mở đầu" });
  s.background = { color: T.white };
  chrome(s, { noNumber: true });
  s.addText("ĐỒ ÁN CAPSTONE, REVIEW 2, HỌC KỲ FALL 2026", { x: MX, y: 1.33, w: 12, h: 0.4, isTextBox: true, margin: 0, fontSize: 19, bold: true, charSpacing: 2.4, color: T.ink, fontFace: HEAD });
  s.addText("Thiết kế và Đánh giá Tác nhân AI Hỗ trợ Phân tích Dữ liệu Tự động trên Dữ liệu do Người dùng Cung cấp",
    { x: MX, y: 2.5, w: 10.6, h: 2.1, isTextBox: true, margin: 0, fontSize: 40, bold: true, color: T.ink, fontFace: HEAD, lineSpacingMultiple: 1.08 });
  s.addText("Design and Evaluation of an AI Data Agent for Automated Data Analysis Using User-Provided Datasets",
    { x: MX, y: 4.8, w: 10.2, h: 1.0, isTextBox: true, margin: 0, fontSize: 23, color: T.body, fontFace: BODY, lineSpacingMultiple: 1.15 });
  [["FA26SE115", 0, 2.7], ["GFA26SE78", 2.95, 2.9]].forEach(([t, dx, w], i) => {
    s.addShape(pres.ShapeType.roundRect, { x: MX + dx, y: 6.15, w, h: 0.72, fill: { color: T.surf }, rectRadius: 0.36, line: { color: T.surf }, objectName: `chip-${i}` });
    s.addText(t, { x: MX + dx, y: 6.15, w, h: 0.72, isTextBox: true, margin: 0, align: "center", valign: "middle", fontSize: 19, color: T.ink2, fontFace: BODY });
  });
  s.addText([
    { text: "GVHD   ", options: { bold: true, fontSize: 19, charSpacing: 1.5, color: T.amber, fontFace: HEAD } },
    { text: "Lâm Hữu Khánh Phương và Trần Trọng Huỳnh", options: { fontSize: 22, color: T.ink, fontFace: BODY } },
  ], { x: MX, y: 7.4, w: 10.6, h: 0.55, isTextBox: true, margin: 0 });
  s.addShape(pres.ShapeType.line, { x: MX, y: 8.1, w: 10.2, h: 0, line: { color: T.line, width: 1 }, objectName: "rule" });
  [["Lê Vũ Phương Hòa", "Nhóm trưởng"], ["Ngô Thành Đạt", "Thành viên"], ["Trần Phú Thịnh", "Thành viên"], ["Uông Tuấn Vũ", "Thành viên"]].forEach((r, i) => {
    const y = 8.45 + Math.floor(i / 2) * 0.82, x = MX + (i % 2) * 5.3;
    s.addText(r[0], { x, y, w: 3.6, h: 0.5, isTextBox: true, margin: 0, fontSize: 21, bold: true, color: T.ink, fontFace: HEAD });
    s.addText(r[1], { x: x + 3.6, y: y + 0.05, w: 1.6, h: 0.45, isTextBox: true, margin: 0, fontSize: 18, color: T.amber, fontFace: BODY });
  });
  /* Panel pipeline: shape gốc để sửa trực tiếp trong PowerPoint. */
  const PX = 12.5, PY = 2.5;
  s.addShape(pres.ShapeType.roundRect, { x: PX, y: PY, w: 6.3, h: 7.75, fill: { color: T.surf }, rectRadius: 0.035, line: { color: T.line2, width: 1 }, objectName: "panel" });
  s.addText("NĂM STAGE NGHIÊN CỨU", { x: PX + 0.44, y: PY + 0.28, w: 5.3, h: 0.34, isTextBox: true, margin: 0, fontSize: 16, bold: true, charSpacing: 2.2, color: T.amber, fontFace: HEAD });
  s.addShape(pres.ShapeType.roundRect, { x: PX + 0.44, y: PY + 0.68, w: 0.42, h: 0.04, fill: { color: T.orange }, rectRadius: 0.02, line: { color: T.orange }, objectName: "accent" });
  const CY0 = PY + 1.42, STEP = 1.04, SPINE = PX + 0.76;
  s.addShape(pres.ShapeType.line, { x: SPINE, y: CY0, w: 0, h: STEP * 4, line: { color: T.line, width: 1.5 }, objectName: "spine" });
  STAGES.forEach(([name, , art], i) => {
    const cy = CY0 + i * STEP;
    s.addShape(pres.ShapeType.roundRect, { x: PX + 1.04, y: cy - 0.38, w: 4.82, h: 0.76, fill: { color: T.white }, rectRadius: 0.08, line: { color: T.line, width: 1 }, objectName: `st-${i}` });
    s.addShape(pres.ShapeType.ellipse, { x: SPINE - 0.17, y: cy - 0.17, w: 0.34, h: 0.34, fill: { color: T.peach }, line: { color: T.orange, width: 1.5 }, objectName: `badge-${i}` });
    s.addText(String(i + 1), { x: SPINE - 0.17, y: cy - 0.17, w: 0.34, h: 0.34, isTextBox: true, margin: 0, align: "center", valign: "middle", fontSize: 16, bold: true, color: T.amber, fontFace: HEAD });
    s.addText(name, { x: PX + 1.26, y: cy - 0.37, w: 4.4, h: 0.38, isTextBox: true, margin: 0, valign: "bottom", fontSize: 19, bold: true, color: T.ink, fontFace: HEAD });
    s.addText(art, { x: PX + 1.26, y: cy + 0.02, w: 4.4, h: 0.3, isTextBox: true, margin: 0, valign: "top", fontSize: 16, color: T.muted, fontFace: BODY });
  });
  const LAST = CY0 + STEP * 4;
  s.addShape(pres.ShapeType.line, { x: SPINE, y: LAST + 0.17, w: 0, h: PY + 6.64 - (LAST + 0.17) - 0.06, line: { color: T.orange, width: 1.5, endArrowType: "triangle" }, objectName: "arrow-gate" });
  s.addShape(pres.ShapeType.roundRect, { x: PX + 0.44, y: PY + 6.64, w: 5.42, h: 0.72, fill: { color: T.peach }, rectRadius: 0.1, line: { color: T.peach }, objectName: "gate" });
  s.addText("Research Dossier", { x: PX + 0.44, y: PY + 6.72, w: 5.42, h: 0.32, isTextBox: true, margin: 0, align: "center", valign: "middle", fontSize: 18, bold: true, color: T.amber, fontFace: HEAD });
  s.addText("chỉ xuất ra ngoài project sau khi được duyệt", { x: PX + 0.44, y: PY + 7.02, w: 5.42, h: 0.3, isTextBox: true, margin: 0, align: "center", valign: "middle", fontSize: 16, color: T.amber, fontFace: BODY });
  s.addNotes("Chào hội đồng. Giới thiệu mã đề tài FA26SE115, nhóm GFA26SE78 và hai GVHD. Nêu ai trình bày phần nào.\n\nPanel bên phải là xương sống của hệ thống: năm stage, mỗi stage bàn giao đúng một artifact (DatasetSnapshot, HypothesisSet, AnalysisPlan + Lock, EvidenceBundle, PaperPack). Kết thúc là Research Dossier, chỉ xuất ra ngoài project sau khi được duyệt.");
}

/* ======================= 2. AGENDA ======================= */
{
  const s = slide("Mở đầu", "Nội dung", "Nội dung trình bày");
  [
    ["01", "Bối cảnh", "Bối cảnh, vấn đề, giải pháp, phạm vi sau Review 1"],
    ["02", "Phương pháp", "Năm stage nghiên cứu"],
    ["03", "Yêu cầu", "Actors, tính năng chính"],
    ["04", "Thiết kế", "Kiến trúc tổng thể, harness, công nghệ"],
    ["05", "Demo", "Danh sách workflow demo cho Hội đồng 1.1"],
    ["06", "Tình trạng", "Tiến độ, kết quả kiểm thử, rủi ro, kế hoạch"],
  ].forEach((it, i) => {
    const y = 3.15 + i * 1.2;
    s.addShape(pres.ShapeType.line, { x: MX, y: y + 1.1, w: CW, h: 0, line: { color: T.line2, width: 1 }, objectName: `agenda-rule-${i}` });
    s.addText(it[0], { x: MX, y, w: 1.5, h: 1.1, isTextBox: true, margin: 0, valign: "middle", fontSize: 36, bold: true, color: T.orange, fontFace: HEAD });
    s.addText(it[1], { x: MX + 1.75, y, w: 6.4, h: 1.1, isTextBox: true, margin: 0, valign: "middle", fontSize: 30, bold: true, color: T.ink, fontFace: HEAD });
    s.addText(it[2], { x: MX + 8.3, y, w: 10.0, h: 1.1, isTextBox: true, margin: 0, valign: "middle", fontSize: 20, color: T.body, fontFace: BODY });
  });
  s.addNotes("Năm phần, theo thứ tự hướng dẫn chuẩn bị Review. Phần yêu cầu và thiết kế có thêm sơ đồ trực quan vì hệ thống có nhiều cơ chế kiểm soát.");
}

/* ======================= BỐI CẢNH VÀ VẤN ĐỀ ======================= */
pres.addSection({ title: "Bối cảnh" });
/* Danh sách đánh số, chữ lớn, mỗi ý một đoạn */
function listSlide(title, items, notes) {
  const s = slide("Bối cảnh", title, "");
  s.addText(items.map((t, i) => ({ text: t, options: { bullet: { type: "number", numberStartAt: i + 1 }, breakLine: i < items.length - 1, paraSpaceAfter: 14 } })),
    { x: MX + 1.2, y: 2.4, w: CW - 2.4, h: 7.6, isTextBox: true, margin: 0, valign: "middle", fontSize: 28, color: T.ink, fontFace: BODY, lineSpacingMultiple: 1.2 });
  s.addNotes(notes);
}
listSlide("Bối cảnh", [
  "Sinh viên và người mới nghiên cứu đã học về câu hỏi nghiên cứu, giả thuyết, phương pháp phân tích và cách viết bài. Khi bắt tay vào một dự án thật, họ vẫn khó biết bắt đầu từ đâu.",
  "Ngày càng có nhiều công cụ AI để tìm tài liệu, phân tích dữ liệu và viết bài. Mỗi công cụ chỉ lo một phần của quá trình nghiên cứu.",
  "LLM và agentic AI làm được nhiều việc trong số này. Đề xuất, trích dẫn và phản biện của AI chỉ có giá trị khoa học khi kiểm chứng được và được người nghiên cứu xem xét.",
], "Nguồn: Report 7 phần I §2 Product Background, đoạn mở đầu (biết định nghĩa không có nghĩa là biết áp dụng), ý Fragmentation (công cụ AI cho từng hoạt động) và đoạn về LLM (automation alone does not establish scientific validity).");
listSlide("Vấn đề", [
  "Người mới có sẵn bảng dữ liệu mà chưa biết nên hỏi câu gì. Họ dễ chọn sai phương pháp, gặp data leakage hoặc kết luận vượt quá bằng chứng.",
  "Đọc tài liệu, phân tích và viết bài nằm ở nhiều công cụ khác nhau, làm đứt liên kết giữa câu hỏi, quyết định phân tích, kết quả, trích dẫn và claim trong bài.",
  "Người mới ít kinh nghiệm phản biện, khó nhận ra điểm yếu về phương pháp trong một câu trả lời AI nghe có vẻ hợp lý.",
  "Quyết định, phiên bản dữ liệu, kết quả và trích dẫn nằm rải rác ở nhiều nơi, khiến người khác khó kiểm tra lại và tái lập kết quả.",
], "Nguồn: Report 7 phần I §2, bốn khó khăn Difficulty Starting from Existing Data, Fragmentation Across Research Activities, Limited Critical Review Experience, Difficulty Maintaining Verifiable Research Records. Khó khăn Gap Between Research Concepts and Practice nằm ở slide Bối cảnh.");


/* ======================= 5. PROPOSED SOLUTION ======================= */
{
  const s = slide("Bối cảnh", "Giải pháp đề xuất", "");
  s.addText("Hệ thống chia một lượt nghiên cứu thành năm stage. Mỗi stage xử lý một nhóm lỗi hay gặp, và người nghiên cứu duyệt kết quả trước khi sang stage sau.",
    { x: MX, y: 2.15, w: CW, h: 0.55, isTextBox: true, margin: 0, valign: "middle", fontSize: 19, color: T.ink2, fontFace: BODY });
  /* Năm cột màu nhạt, mỗi cột: số, tên stage, stage là gì, giải quyết vấn đề gì */
  const COLS = [
    ["Dataset", "Hiểu dữ liệu", "Đọc và kiểm tra bảng dữ liệu trước khi đặt câu hỏi", ["Tránh đọc sai giá trị thiếu hoặc xoá nhầm dòng", "Biết rõ mẫu đại diện cho ai"], "1F3A5F", "EAF0F7"],
    ["Hypothesis", "Đặt giả thuyết", "Tìm tài liệu liên quan rồi đặt giả thuyết kiểm chứng được", ["Tránh trích dẫn bài không ủng hộ kết luận", "Biết câu hỏi đã có người làm hay chưa"], "2B6CB0", "E8F1FB"],
    ["Experiment Design", "Lập kế hoạch", "Chốt cách phân tích trước khi thấy kết quả", ["Tránh thấy kết quả rồi mới chọn cách phân tích", "Bảo đảm kế hoạch đủ power để kết luận"], "C2611A", "FDEFE3"],
    ["Execution", "Chạy phân tích", "Chạy đúng kế hoạch đã khoá, code tính mọi con số", ["Tránh chạy lại tới khi ra kết quả đẹp", "Phân biệt có ý nghĩa thống kê với hiệu ứng đủ lớn"], "2F7D32", "EAF5EA"],
    ["Paper", "Viết bài", "Viết bài báo chỉ từ bằng chứng đã kiểm", ["Tránh kết luận mạnh hơn bằng chứng", "Giữ mọi số liệu và trích dẫn kiểm lại được"], "5B6573", "F0F1F3"],
  ];
  const G = 0.2, w = (CW - 4 * G) / 5, Y = 2.95, H = 7.0;
  COLS.forEach(([en, vi, what, solves, ac, bg], i) => {
    const x = MX + i * (w + G);
    s.addShape(pres.ShapeType.rect, { x, y: Y, w, h: H, fill: { color: bg }, line: { color: bg }, objectName: `col-${i}` });
    s.addText(String(i + 1), { x, y: Y + 0.05, w, h: 1.15, isTextBox: true, margin: 0, align: "center", valign: "middle", fontSize: 60, bold: true, color: ac, fontFace: HEAD });
    s.addShape(pres.ShapeType.rect, { x, y: Y + 1.2, w, h: 1.05, fill: { color: ac }, line: { color: ac }, objectName: `band-${i}` });
    s.addText([{ text: en.toUpperCase(), options: { fontSize: 18, bold: true, charSpacing: 0.5, color: T.white, fontFace: HEAD, breakLine: true } },
      { text: vi, options: { fontSize: 17, color: T.white, fontFace: BODY } }],
      { x: x + 0.1, y: Y + 1.2, w: w - 0.2, h: 1.05, isTextBox: true, margin: 0, align: "center", valign: "middle" });
    const bx = x + 0.28, bw = w - 0.5;
    /* Câu mô tả stage, đường kẻ mảnh, rồi hai lỗi stage chặn */
    s.addText(what, { x: bx, y: Y + 2.5, w: bw, h: 1.45, isTextBox: true, margin: 0, valign: "middle", fontSize: 19.5, bold: true, color: T.ink, fontFace: HEAD, lineSpacingMultiple: 1.05 });
    s.addShape(pres.ShapeType.line, { x: bx, y: Y + 4.1, w: bw, h: 0, line: { color: ac, width: 1, transparency: 50 }, objectName: `rule-${i}` });
    solves.forEach((t, k) => {
      const yy = Y + 4.35 + k * 1.2;
      s.addShape(pres.ShapeType.ellipse, { x: bx, y: yy + 0.1, w: 0.18, h: 0.18, fill: { color: ac }, line: { color: ac }, objectName: `dot-${i}-${k}` });
      s.addText(t, { x: bx + 0.32, y: yy, w: bw - 0.32, h: 1.1, isTextBox: true, margin: 0, valign: "top", fontSize: 18, color: T.body, fontFace: BODY });
    });
  });
  s.addNotes("Nguồn: Report 7 phần I §2 và §5, mô tả năm stage ở phần III, docs/example/2026-11-03-method-design.md (lỗi đã tái lập ở từng stage). Mỗi cột nói stage đó là gì và nhóm lỗi nó chặn, các slide Stage 1 đến 5 đi vào từng step. Cuối mỗi stage, người nghiên cứu duyệt artifact: DatasetSnapshot, HypothesisSet, AnalysisPlan và Lock, EvidenceBundle, PaperPack.");
}

/* ======================= 6. SCOPE UPDATES ======================= */
{
  const s = slide("Bối cảnh", "Thay đổi phạm vi sau Review 1", "Phạm vi thay đổi sau Review 1");
  table(s, [
    ["#", "Thay đổi phạm vi", "Ảnh hưởng"],
    ["1", "Năm stage cố định, mỗi stage bàn giao một artifact", "Thêm stage Execution và Paper"],
    ["2", "Review độc lập bắt buộc cho mọi artifact version", "Thêm vòng review"],
    ["3", "Kiểm soát theo nhóm hành động, một Decision Inbox", "Thay chế độ kiểm soát chung của cả lượt"],
    ["4", "Dữ liệu local ở lại máy qua Local Node", "Thêm Local Node"],
    ["5", "Research Dossier có version, export phải được duyệt", "Thêm bước duyệt Dossier"],
    ["6", "Chỉ hỗ trợ dữ liệu dạng bảng", "Không phân tích ảnh, văn bản hay tín hiệu"],
    ["7", "ML Method Comparison ở mức Should, Journal Fingerprint và Claim Ledger ở mức Could", "Làm sau MVP, MVP không đổi"],
  ], { y: 3.1, colW: [1.1, 10.4, 6.35], fontSize: 19, fillTo: 9.4 });
  note(s, "MVP cam kết 16 tính năng Must, còn tính năng Should và Could làm sau MVP. Tên đề tài và bốn thành viên giữ nguyên, kế hoạch 190 man-day (180 cộng 10 dự phòng) trong 12 tuần.", 9.7);
  s.addNotes("Mỗi dòng tương ứng một thay đổi trong Record of Changes. Số liệu kế hoạch lấy theo WBS ở phần II: 180 man-day công việc cộng 10 man-day dự phòng.\n\nJournal Fingerprint Extraction và Claim Ledger ở mức Could, ML Method Comparison ở mức Should.");
}

pres.addSection({ title: "Phương pháp" });

/* ======================= CHI TIẾT TỪNG STAGE ======================= */
/* Mỗi bước gắn một vai: AI Engine đề xuất, Code tính và kiểm tra, Người quyết pinned action */
const ROLE = {
  AI: { fill: T.white, border: T.line, tag: "AI ENGINE", tagC: T.muted, c: T.ink },
  Code: { fill: T.soft, border: T.softLine, tag: "CODE", tagC: T.muted, c: T.ink },
  Người: { fill: T.peach, border: T.orange, tag: "NGƯỜI", tagC: T.amber, c: T.ink },
};
function stageSlide(i, d) {
  const s = slide("Phương pháp", `Stage ${i + 1} · ${STAGES[i][0]}`, d.title);
  /* dải định vị: stage đang nói được tô cam */
  const cw = (CW - 4 * 0.12) / 5;
  STAGES.forEach(([en], j) => box(s, MX + j * (cw + 0.12), 2.95, cw, 0.5, `${j + 1}  ${en}`,
    { fill: j === i ? T.orange : T.surf, color: j === i ? T.white : T.faint, size: 16.5 }));
  /* luồng: đầu vào → các bước → artifact */
  const Y = 3.7, HH = 3.3, IW = 1.75, OW = 1.95, G = 0.22;
  box(s, MX, Y, IW, HH, "", { fill: T.surf });
  s.addText([{ text: "ĐẦU VÀO", options: { fontSize: 16.5, bold: true, charSpacing: 1.5, color: T.faint, fontFace: HEAD, breakLine: true } },
    { text: d.input, options: { fontSize: 16, bold: true, color: T.ink, fontFace: HEAD } }],
    { x: MX + 0.05, y: Y, w: IW - 0.1, h: HH, isTextBox: true, margin: 0, valign: "middle", align: "center" });
  const n = d.steps.length, sx = MX + IW + G, sw = (CW - IW - OW - G * (n + 1)) / n;
  arrow(s, MX + IW + 0.02, Y + HH / 2, G - 0.04, 0);
  d.steps.forEach(([role, h, b, tag], k) => {
    const R = ROLE[role], x = sx + k * (sw + G);
    s.addShape(pres.ShapeType.roundRect, { x, y: Y, w: sw, h: HH, fill: { color: R.fill }, rectRadius: 0.1, line: { color: R.border, width: 1.25 }, objectName: `step-${k}` });
    /* tag tuỳ chọn khi một bước có nhiều bên cùng làm, màu theo bên quyết định */
    s.addText(`${k + 1}  ${tag || R.tag}`, { x: x + 0.15, y: Y + 0.12, w: sw - 0.3, h: 0.36, isTextBox: true, margin: 0, fontSize: 16, bold: true, charSpacing: 0, color: R.tagC, fontFace: HEAD });
    s.addText([{ text: h, options: { fontSize: 18, bold: true, color: R.c, fontFace: HEAD, breakLine: true } },
      { text: b, options: { fontSize: 16.5, color: T.body, fontFace: BODY } }],
      { x: x + 0.15, y: Y + 0.58, w: sw - 0.3, h: HH - 0.7, isTextBox: true, margin: 0, valign: "top", lineSpacingMultiple: 1.05, paraSpaceAfter: 3 });
    arrow(s, x + sw + 0.02, Y + HH / 2, G - 0.04, 0, k === n - 1 ? T.orange : T.faint);
  });
  const ox = MX + CW - OW;
  s.addShape(pres.ShapeType.flowChartDocument, { x: ox, y: Y, w: OW, h: HH, fill: { color: T.peachSoft }, line: { color: T.orange, width: 1.5 }, objectName: "artifact" });
  s.addText([{ text: "BÀN GIAO", options: { fontSize: 16.5, bold: true, charSpacing: 1.5, color: T.amber, fontFace: HEAD, breakLine: true } },
    { text: STAGES[i][2].replace(" + ", "\n+ "), options: { fontSize: 17, bold: true, color: T.ink, fontFace: HEAD } }],
    { x: ox + 0.04, y: Y, w: OW - 0.08, h: HH - 0.35, isTextBox: true, margin: 0, valign: "middle", align: "center" });
  if (d.lane) s.addText(d.lane, { x: MX, y: Y + HH + 0.12, w: CW, h: 0.4, isTextBox: true, margin: 0, fontSize: 16, color: T.amber, fontFace: BODY });
  /* ba thẻ: vấn đề, phương pháp, kiểm tra */
  const CY = 7.65, CH = 2.3, w3 = (CW - 2 * 0.3) / 3;
  [["Giải quyết vấn đề gì", d.problem, T.surf, T.ink2], ["Dựa trên phương pháp", d.method, T.surf, T.ink2], [d.checkHead || "Kiểm tra trước khi accept", d.check, T.peachSoft, T.amber]].forEach(([h, items, f, hc], k) => {
    const x = MX + k * (w3 + 0.3);
    s.addShape(pres.ShapeType.roundRect, { x, y: CY, w: w3, h: CH, fill: { color: f }, rectRadius: 0.1, line: { color: f === T.surf ? T.surf : T.peach }, objectName: `info-${k}` });
    s.addText(h.toUpperCase(), { x: x + 0.3, y: CY + 0.2, w: w3 - 0.6, h: 0.34, isTextBox: true, margin: 0, fontSize: 16, bold: true, charSpacing: 1.5, color: hc, fontFace: HEAD });
    s.addText(items.map((t) => ({ text: t, options: { bullet: { indent: 14 }, breakLine: true } })),
      { x: x + 0.3, y: CY + 0.6, w: w3 - 0.6, h: CH - 0.7, isTextBox: true, margin: 0, valign: "top", fontSize: 16.5, color: T.ink2, fontFace: BODY, lineSpacingMultiple: 1.05, paraSpaceAfter: 3 });
  });
  s.addNotes(d.notes);
}

/* Slide stage: mỗi stage chia thành các layer. Mỗi layer ghi các bước làm gì, vấn đề layer giải quyết
   và phương pháp nghiên cứu làm nền. Dải trên định vị stage, dải dưới ghi phần người nghiên cứu quyết định. */
function stageLayers(i, d) {
  const s = slide("Phương pháp", `Stage ${i + 1} · ${STAGES[i][0]}`, d.title);
  const cw = (CW - 4 * 0.12) / 5;
  STAGES.forEach(([en], j) => box(s, MX + j * (cw + 0.12), 2.45, cw, 0.5, `${j + 1}  ${en}`,
    { fill: j === i ? T.orange : T.surf, color: j === i ? T.white : T.faint, size: 16.5 }));
  /* đầu vào và bàn giao của stage */
  const io = (x, w, lab, val, out) => {
    s.addShape(pres.ShapeType.roundRect, { x, y: 3.1, w, h: 0.55, fill: { color: out ? T.peachSoft : T.surf }, rectRadius: 0.08, line: { color: out ? T.orange : T.surf } });
    s.addText([{ text: lab + "   ", options: { fontSize: 16, bold: true, charSpacing: 1.5, color: out ? T.amber : T.faint, fontFace: HEAD } },
      { text: val, options: { fontSize: 17, bold: true, color: T.ink, fontFace: HEAD } }],
      { x: x + 0.25, y: 3.1, w: w - 0.5, h: 0.55, isTextBox: true, margin: 0, valign: "middle" });
  };
  const hw = (CW - 0.9) / 2;
  io(MX, hw, "ĐẦU VÀO", d.input, false);
  arrow(s, MX + hw + 0.15, 3.375, 0.6, 0, T.orange);
  io(MX + hw + 0.9, hw, "BÀN GIAO", d.output || STAGES[i][2], true);
  /* các layer */
  const n = d.layers.length, G = 0.25, w = (CW - G * (n - 1)) / n, Y = 3.9, H = 5.3;
  d.layers.forEach(([name, steps, prob, meth], k) => {
    const x = MX + k * (w + G), human = d.humanLayers && d.humanLayers.includes(k);
    s.addShape(pres.ShapeType.roundRect, { x, y: Y, w, h: H, fill: { color: T.white }, rectRadius: 0.1, line: { color: T.line, width: 1.25 }, objectName: `layer-${k}` });
    s.addShape(pres.ShapeType.roundRect, { x, y: Y, w, h: 0.95, fill: { color: T.peach }, rectRadius: 0.1, line: { color: T.peach } });
    s.addShape(pres.ShapeType.rect, { x, y: Y + 0.6, w, h: 0.35, fill: { color: T.peach }, line: { color: T.peach } });
    s.addText([{ text: `LAYER ${k + 1}`, options: { fontSize: 16, bold: true, charSpacing: 1.5, color: T.amber, fontFace: HEAD, breakLine: true } },
      { text: name, options: { fontSize: 19, bold: true, color: T.ink, fontFace: HEAD } }],
      { x: x + 0.22, y: Y + 0.05, w: w - 0.44, h: 0.85, isTextBox: true, margin: 0, valign: "middle" });
    const tx = x + 0.22, tw = w - 0.44, lab = (y, t, c) => s.addText(t, { x: tx, y, w: tw, h: 0.3, isTextBox: true, margin: 0, fontSize: 16, bold: true, charSpacing: 1.2, color: c || T.faint, fontFace: HEAD });
    lab(Y + 1.1, "CÁC BƯỚC");
    s.addText(steps.map((t, j) => ({ text: t, options: { bullet: { indent: 14 }, breakLine: j < steps.length - 1 } })),
      { x: tx, y: Y + 1.42, w: tw, h: 1.55, isTextBox: true, margin: 0, valign: "top", fontSize: 18.5, color: T.ink2, fontFace: BODY, lineSpacingMultiple: 1.0, paraSpaceAfter: 5 });
    s.addShape(pres.ShapeType.line, { x: tx, y: Y + 3.05, w: tw, h: 0, line: { color: T.line, width: 1 } });
    lab(Y + 3.15, "GIẢI QUYẾT");
    s.addText(prob, { x: tx, y: Y + 3.47, w: tw, h: 1.15, isTextBox: true, margin: 0, valign: "top", fontSize: 18, color: T.body, fontFace: BODY, lineSpacingMultiple: 1.0 });
    lab(Y + 4.7, "PHƯƠNG PHÁP", T.amber);
    s.addText(meth, { x: tx, y: Y + 4.98, w: tw, h: 0.3, isTextBox: true, margin: 0, valign: "top", fontSize: 17, bold: true, color: T.amber, fontFace: BODY });
  });
  /* phần người nghiên cứu quyết định */
  s.addShape(pres.ShapeType.roundRect, { x: MX, y: 9.4, w: CW, h: 0.7, fill: { color: T.surf }, rectRadius: 0.08, line: { color: T.surf } });
  s.addText([{ text: "NGƯỜI NGHIÊN CỨU QUYẾT ĐỊNH   ", options: { fontSize: 16, bold: true, charSpacing: 1.5, color: T.amber, fontFace: HEAD } },
    { text: d.decide, options: { fontSize: 17, color: T.ink2, fontFace: BODY } }],
    { x: MX + 0.3, y: 9.4, w: CW - 0.6, h: 0.7, isTextBox: true, margin: 0, valign: "middle" });
  s.addNotes(d.notes);
}
const MNOTE = "Nguồn: docs/example/2026-11-03-method-design.md, thiết kế phương pháp đích cho từng stage. Mỗi layer gom các step cùng mục đích, ghi lỗi người mới hay mắc mà layer chặn và phương pháp làm nền. Tài liệu ghi rõ đây là thiết kế đích, phần dự kiến còn chờ bench kiểm tra.\n\n";
stageLayers(0, {
  title: "Hiểu dữ liệu trước khi đặt câu hỏi", input: "Research Case và dataset version",
  layers: [
    ["Đọc đúng dữ liệu", ["Xác định giá trị nào là thiếu", "Xác định mỗi dòng ứng với ai", "Xử lý dòng trùng"], "Đọc nhầm \"None\" thành giá trị thiếu hoặc xoá nhầm người thật", "Schmidt 2021, Kapoor 2023"],
    ["Kiểm tra chất lượng", ["Tìm giá trị bất thường như mã 99 hoặc đơn vị lệch", "Tìm biến lộ thông tin của kết quả"], "Tin mọi giá trị và dùng biến sinh ra từ outcome", "Schmidt 2021, Kapoor 2023"],
    ["Ghi lại và chia mẫu", ["Ghi lại mọi bước làm sạch", "Chia mẫu theo người, không theo dòng"], "Làm sạch không để lại dấu vết và dữ liệu rò rỉ giữa các phần", "STRATOS IDA, group split"],
    ["Đánh giá độ phù hợp", ["Mô tả mẫu đại diện cho ai", "Ghi giới hạn khi dùng dữ liệu"], "Không biết kết luận áp dụng được cho nhóm người nào", "Datasheets for Datasets"],
  ],
  decide: "Giá trị nào là thiếu, mỗi dòng ứng với ai và mẫu đại diện cho ai.",
  notes: MNOTE + "Step gốc: token thiếu, đơn vị quan sát, dòng trùng, chất lượng, leakage, recipe, chia mẫu, fitness. Phương pháp chung: STRATOS IDA (Baillie 2022), Schmidt 2021 (DQI-1003, DQI-1008), TARMOS, Datasheets, Kapoor và Narayanan 2023, group split. Audit cũ: code tự xoá người trả lời thật, 3000 dòng còn 464; \"None\" bị đọc thành missing.",
});
stageLayers(1, {
  title: "Từ tài liệu tới giả thuyết bác bỏ được", input: "DatasetSnapshot",
  layers: [
    ["Đặt câu hỏi", ["Viết câu hỏi theo PECO", "Gắn mỗi khái niệm với biến có trong dữ liệu"], "Gom quá nhiều biến vào một khái niệm", "PECO (Morgan 2018)"],
    ["Tìm tài liệu", ["Tìm ở nhiều cơ sở dữ liệu", "Dừng tìm theo tiêu chí định trước", "Loại bài đã bị rút"], "Tìm một nguồn rồi cho là đủ và trích bài đã bị rút", "PRISMA-S, Cochrane"],
    ["Đọc và trích bằng chứng", ["Sàng lọc mỗi bài hai lần", "Trích số liệu vào thẻ bằng chứng", "Xếp mức tin cậy của bằng chứng"], "Lấy nhầm số và coi bài yếu như bài mạnh", "Cochrane 2024, GRADE"],
    ["Chốt giả thuyết", ["Xác định khoảng trống nghiên cứu", "Kiểm logic của giả thuyết", "Ghi lại mọi thay đổi tiêu chí"], "Không tìm thấy thì cho là chưa ai làm", "PRISMA 2020"],
  ],
  decide: "Câu hỏi nghiên cứu và giả thuyết được chọn, kể cả khi hệ thống đã cảnh báo.",
  notes: MNOTE + "Step gốc: câu hỏi, search, dừng search, sàng lọc, retraction, evidence card, claim, khoảng trống, certainty, kiểm logic, amendment. Phương pháp chung: Cochrane Rapid Reviews 2024 (Garritty), PRISMA 2020, PRISMA-S, PECO (Morgan 2018), GRADE. Audit cũ: dẫn 30 effect nhưng chỉ 1 effect ủng hộ claim.",
});
stageLayers(2, {
  title: "Chốt cách phân tích trước khi thấy kết quả", input: "HypothesisSet",
  layers: [
    ["Xác định cần ước tính gì", ["Nói rõ đại lượng cần ước tính", "Giới hạn mức kết luận nhân quả"], "Kết luận A gây ra B khi chỉ có dữ liệu quan sát", "ICH E9(R1), target trial"],
    ["Chọn cách phân tích", ["Chọn biến cần điều chỉnh", "Chọn phương pháp hợp với cấu trúc dữ liệu"], "Điều chỉnh nhầm biến trung gian và bỏ qua quan sát lặp lại", "VanderWeele 2019"],
    ["Đặt ngưỡng và kiểm power", ["Đặt ngưỡng hiệu ứng có ý nghĩa", "Hiệu chỉnh khi chạy nhiều test", "Mô phỏng power"], "Ước tính power cao hơn thực tế", "Lakens 2017, ADEMP"],
    ["Khoá kế hoạch", ["Thêm biến đối chứng âm", "Ghi lại điều đã biết trước", "Khoá kế hoạch phân tích"], "Sửa kế hoạch sau khi đã xem dữ liệu", "Van den Akker 2021"],
  ],
  decide: "Đại lượng cần ước tính, biến điều chỉnh, ngưỡng hiệu ứng và thời điểm khoá kế hoạch.",
  notes: MNOTE + "Step gốc: estimand, causal claim, biến điều chỉnh, phương pháp, margin, đa kiểm định, power, negative control, kiến thức trước, khoá. Phương pháp chung: ICH E9(R1), Hernán và Robins, VanderWeele 2019, Van den Akker 2021, Gamble 2017, ADEMP (Morris 2019), Lakens 2017, Lipsitch 2010, Cameron và Miller 2015. Audit cũ: power báo 0.935 nhưng tính lại chỉ 0.388.",
});
stageLayers(3, {
  title: "Chạy phân tích kín, code tính verdict", input: "AnalysisPlan đã khoá",
  layers: [
    ["Chạy đúng kế hoạch", ["Giữ riêng một phần dữ liệu để kiểm tra", "Ghi lại mọi lần chạy lại"], "Chạy lại tới khi ra kết quả đẹp", "Blind analysis, Patel 2010"],
    ["Kiểm định đúng cách", ["Kiểm định tương đương", "Hiệu chỉnh khi có nhiều giả thuyết", "So đúng thước đo với ngưỡng"], "Nhầm có ý nghĩa thống kê với hiệu ứng đủ lớn", "TOST, Holm"],
    ["Kiểm độ vững", ["Hoán vị dữ liệu để loại tín hiệu giả", "Xếp mức tin cậy của kết quả", "Kiểm power sau khi mở dữ liệu"], "Tin cả tín hiệu giả do nhiễu", "Phipson và Smyth 2010"],
    ["Ra kết luận", ["Code tính verdict", "Kèm câu giải thích cho người đọc"], "Hiểu supported là hiệu ứng đủ lớn", "Lakens 2017"],
  ],
  decide: "Đọc verdict kèm giải thích và duyệt mọi thay đổi lệch khỏi kế hoạch đã khoá.",
  notes: MNOTE + "Step gốc: verdict, trivial, tương đương, sai metric, không reserve, chạy lại, tier, permutation, grade, sau khi mở. Phương pháp chung: blind analysis (Klein và Roodman 2005), Holm, TOST, ICEMAN v1.1, Patel 2010, Phipson và Smyth 2010, Sterne 2009. Audit cũ: test tương đương nằm ngoài Holm, sai 34% ở 8 giả thuyết.",
});
stageLayers(4, {
  title: "Viết bài báo từ bằng chứng đã kiểm", input: "Kết quả thực nghiệm, references",
  layers: [
    ["Kiểm nguồn và số liệu", ["Xác nhận từng reference", "Tính lại mọi con số"], "Trích nguồn không có thật hoặc số không kiểm được", "Crossref, DataCite"],
    ["Dựng lập luận", ["Tranh luận từng claim", "Chỉ giữ claim thắng phản biện"], "Viết claim chưa qua phản biện thành kết luận", "Toulmin, ASPIC+"],
    ["Viết bài", ["Lập dàn ý", "Viết từng phần từ claim đã khoá"], "Model tự gõ con số vào bài", "IMRaD"],
    ["Kiểm bản thảo", ["Đọc ngược từ bài về lập luận", "Review và sửa theo góp ý"], "Câu kết luận mạnh hơn bằng chứng", "Đọc ngược, rubric"],
    ["Ký và xuất", ["Tác giả ký bản thảo", "Ghi rõ bản nháp hay bản hoàn chỉnh"], "AI tự điền phần của tác giả", "REFORMS, TRIPOD+AI"],
  ],
  decide: "Claim được giữ lại, bản viết của từng phần và chữ ký trên bản thảo cuối.",
  notes: "Nguồn: code writing engine nhánh feat/writing (repo logos, stages/writing): engine.py (24 bước chia năm pha Data, Argue, Write, Verify, Export, tương ứng năm layer; gate G1 khoá claim, gate G3 người ký), tokens.py (mark {{A1}}), sources.py (tra DOI ở Crossref, DataCite, OpenAlex), package/reporting.py (REFORMS, TRIPOD+AI), steps/readback.py, steps/journal_fit.py, steps/draft.py, steps/review.py. Step gốc: intake, data report, evidence ledger, gán nhãn, tranh luận, Toulmin, argument graph, khoá claim, journal merge, outline, contracts, viết section, chỉnh văn, đọc ngược, peer review, sửa theo issue, ký, xuất.",
});


/* AI trong hệ thống: ba vai trò AI, AI hỗ trợ gì ở từng stage, mức tự chủ. Nguồn: Report 7 phần I–II. */
{
  const s = slide("Phương pháp", "AI trong hệ thống", "AI đề xuất và phản biện, người nghiên cứu duyệt và chịu trách nhiệm");
  const label = (y, t) => s.addText(t, { x: MX, y, w: CW, h: 0.34, isTextBox: true, margin: 0, fontSize: 16, bold: true, charSpacing: 1.5, color: T.amber, fontFace: HEAD });
  label(2.4, "BA VAI TRÒ CỦA AI");
  const ROLES = [
    ["AI Engine", "Một engine cho mỗi stage", "Soạn đề xuất và bản nháp cho stage đang chạy. Code kiểm tra từng đề xuất trước khi đưa cho người nghiên cứu."],
    ["AI PI", "Điều phối cả Research Run", "Gợi ý bước nghiên cứu tiếp theo khi một run kết thúc. Ghi dự đoán kết quả trước khi khoá kế hoạch để đối chiếu về sau."],
    ["AI Reviewer", "Phản biện độc lập", "Đặt câu hỏi về giả định, chỉ ra rủi ro phương pháp và gợi ý góc nhìn khác. Người nghiên cứu xem xét các góp ý này."],
  ];
  const G3 = 0.3, w3 = (CW - 2 * G3) / 3, RY = 2.8, RH = 2.55;
  ROLES.forEach(([name, tag, body], k) => {
    const x = MX + k * (w3 + G3);
    s.addShape(pres.ShapeType.roundRect, { x, y: RY, w: w3, h: RH, fill: { color: T.peachSoft }, rectRadius: 0.1, line: { color: T.peach, width: 1.25 }, objectName: `ai-role-${k}` });
    s.addText([{ text: name, options: { fontSize: 21, bold: true, color: T.ink, fontFace: HEAD, breakLine: true } },
      { text: tag, options: { fontSize: 16.5, bold: true, color: T.amber, fontFace: BODY } }],
      { x: x + 0.3, y: RY + 0.2, w: w3 - 0.6, h: 0.85, isTextBox: true, margin: 0, valign: "top" });
    s.addText(body, { x: x + 0.3, y: RY + 1.1, w: w3 - 0.6, h: RH - 1.25, isTextBox: true, margin: 0, valign: "top", fontSize: 17.5, color: T.ink2, fontFace: BODY, lineSpacingMultiple: 1.05 });
  });
  label(5.6, "AI HỖ TRỢ TỪNG STAGE");
  const HELP = [
    "Phân tích cấu trúc và chất lượng dữ liệu, gợi ý cách làm sạch và chia mẫu",
    "Tìm và tổng hợp tài liệu, đề xuất giả thuyết kiểm chứng được",
    "Gợi ý phương pháp, baseline, metric và chỉ ra rủi ro của kế hoạch",
    "Chạy phân tích theo kế hoạch đã khoá trong môi trường kiểm soát",
    "Soạn bản thảo IMRaD từ kết quả đã kiểm và kiểm tra trích dẫn",
  ];
  const G5 = 0.2, w5 = (CW - 4 * G5) / 5, SY = 6.0, SH = 2.45;
  HELP.forEach((t, k) => {
    const x = MX + k * (w5 + G5);
    s.addShape(pres.ShapeType.roundRect, { x, y: SY, w: w5, h: SH, fill: { color: T.white }, rectRadius: 0.1, line: { color: T.line, width: 1.25 }, objectName: `ai-stage-${k}` });
    s.addText(`${k + 1}  ${STAGES[k][0]}`, { x: x + 0.2, y: SY + 0.15, w: w5 - 0.4, h: 0.4, isTextBox: true, margin: 0, fontSize: 17, bold: true, color: T.ink, fontFace: HEAD });
    s.addShape(pres.ShapeType.line, { x: x + 0.2, y: SY + 0.62, w: w5 - 0.4, h: 0, line: { color: T.orange, width: 1.5 } });
    s.addText(t, { x: x + 0.2, y: SY + 0.75, w: w5 - 0.4, h: SH - 0.85, isTextBox: true, margin: 0, valign: "top", fontSize: 17, color: T.body, fontFace: BODY, lineSpacingMultiple: 1.05 });
  });
  s.addShape(pres.ShapeType.roundRect, { x: MX, y: 8.7, w: CW, h: 1.35, fill: { color: T.surf }, rectRadius: 0.08, line: { color: T.surf } });
  s.addText([{ text: "MỨC TỰ CHỦ", options: { fontSize: 16, bold: true, charSpacing: 1.5, color: T.amber, fontFace: HEAD, breakLine: true } },
    { text: "Người nghiên cứu chọn Co-work, Milestones hoặc Autopilot. Ở mọi mức, chọn giả thuyết, xác nhận cấu trúc dữ liệu và khoá kế hoạch vẫn cần người duyệt. Khi chạy Autopilot, AI PI ra quyết định tạm thời và người nghiên cứu xác nhận hoặc đổi lại trong Decision Log.", options: { fontSize: 17, color: T.ink2, fontFace: BODY } }],
    { x: MX + 0.3, y: 8.7, w: CW - 0.6, h: 1.35, isTextBox: true, margin: 0, valign: "middle", lineSpacingMultiple: 1.05 });
  s.addNotes("Nguồn: Report 7 phần I–II. Business Opportunity (Supporting critical reflection): AI review agent đặt câu hỏi về giả định, chỉ ra rủi ro phương pháp, gợi ý góc nhìn khác, góp ý cần người đánh giá. Product Vision: AI agent gợi ý hướng nghiên cứu, hỗ trợ thực thi, nêu câu hỏi phản biện; researcher chịu trách nhiệm chọn giả thuyết, chấp nhận phương pháp, diễn giải kết quả. FE-04.5 gợi ý bước tiếp theo. FE-05.1 ba mức Co-work, Milestones, Autopilot. FE-05.2 quyết định bắt buộc người duyệt. FE-05.4 AI PI quyết định tạm thời khi Autopilot. FE-05.5 Decision Log. FE-06 đến FE-10 phần AI hỗ trợ từng stage. FE-11.2 AI reviewer chuyên biệt. Dự đoán của AI PI trước khi khoá kế hoạch theo use case Record and evaluate AI forecasts. Luồng kiểm soát chi tiết của mỗi đề xuất AI nằm ở slide Harness engineering.");
}

/* ======================= 8-11. MAIN ACTORS ======================= */
pres.addSection({ title: "Yêu cầu" });
[
  {
    name: "Platform Admin", icon: "actor-admin", kind: "Phạm vi toàn hệ thống", mark: "01",
    rows: [
      ["Vai trò", "Quản trị toàn nền tảng, không tham gia nội dung nghiên cứu."],
      ["Cấu hình", "Cấu hình tài khoản, model, key và ngân sách mặc định."],
      ["Giám sát", "Theo dõi audit log và tình trạng hệ thống."],
      ["Giới hạn", "Chỉ thấy metadata của project, không đọc nội dung bên trong."],
    ],
    note: "Platform Admin không đọc được nội dung project. Đây là ranh giới quyền hội đồng hay hỏi.",
  },
  {
    name: "Project Manager", icon: "actor-pm", kind: "Phạm vi project", mark: "02",
    rows: [
      ["Vai trò", "Chủ project, có đủ quyền nghiên cứu của Researcher."],
      ["Quản lý", "Quản lý thành viên, settings, dataset và các Research Run trong project."],
      ["Ngân sách", "Duyệt chi thêm khi lượt nghiên cứu chờ duyệt ngân sách."],
      ["Phát hành", "Duyệt Research Dossier trước khi xuất ra ngoài project."],
    ],
    note: "Project Manager là người mở lại lượt nghiên cứu đang chờ duyệt ngân sách. Project Manager hoặc người tạo lượt nghiên cứu có quyền huỷ nó.",
  },
  {
    name: "Researcher", icon: "actor-researcher", kind: "Phạm vi project", mark: "03",
    rows: [
      ["Vai trò", "Người đưa ra các quyết định dành riêng cho con người."],
      ["Chạy nghiên cứu", "Tạo Research Run và đưa nó qua năm stage."],
      ["Quyết định", "Trả lời Decision Inbox, chấp nhận artifact, khoá kế hoạch."],
      ["Kết quả", "Xuất kết quả sau khi Research Dossier được duyệt."],
    ],
    note: "Pinned action không ai trả lời trước hạn chờ thì lượt nghiên cứu kết thúc ở trạng thái complete with gaps, không ai quyết thay.",
  },
  {
    name: "Reviewer", icon: "actor-reviewer", kind: "Phạm vi project", mark: "04",
    rows: [
      ["Vai trò", "Người review độc lập, tách khỏi người tạo artifact."],
      ["Đọc", "Xem và bình luận mọi artifact version trong project."],
      ["Review", "Mỗi stage có một lượt review độc lập."],
      ["Duyệt", "Duyệt Research Dossier theo review settings của project."],
    ],
    note: "Review độc lập ở mọi stage là cơ chế chống việc AI tự duyệt kết quả của chính nó.",
  },
].forEach((a, k, all) => {
  /* Bốn actor trên một slide, mỗi actor một cột */
  if (k > 0) return;
  const s = slide("Yêu cầu", "Các actor chính", "Bốn actor và quyền hạn");
  const w = (CW - 3 * 0.3) / 4;
  all.forEach((b, i) => {
    const x = MX + i * (w + 0.3);
    card(s, { x, y: 3.0, w, h: 7.0, fill: T.peachSoft, border: T.peach, name: `actor-${i}` });
    s.addImage({ path: I(b.icon), x: x + 0.35, y: 3.3, w: 0.95, h: 0.95, objectName: `actor-icon-${i}` });
    s.addText(b.mark, { x: x + w - 1.6, y: 3.25, w: 1.3, h: 0.9, isTextBox: true, margin: 0, align: "right", fontSize: 40, bold: true, color: T.peach, fontFace: HEAD });
    s.addText(b.name, { x: x + 0.35, y: 4.4, w: w - 0.7, h: 0.55, isTextBox: true, margin: 0, fontSize: 23, bold: true, color: T.ink, fontFace: HEAD });
    s.addText(b.kind, { x: x + 0.35, y: 4.95, w: w - 0.7, h: 0.4, isTextBox: true, margin: 0, fontSize: 16.5, color: T.amber, fontFace: BODY });
    b.rows.forEach((r, ri) => {
      const y = 5.55 + ri * 1.1;
      s.addText([{ text: r[0], options: { bold: true, fontSize: 16.5, color: T.amber, fontFace: HEAD, breakLine: true } }, { text: r[1], options: { fontSize: 16.5, color: T.ink2, fontFace: BODY } }],
        { x: x + 0.35, y, w: w - 0.7, h: 1.05, isTextBox: true, margin: 0, valign: "top", lineSpacingMultiple: 1.05 });
    });
  });
  s.addNotes(all.map((b) => b.name + ": " + b.note).join("\n\n") + "\n\nNguồn: Report 7 phần III mục 2.1 Actors. Hệ thống chỉ có bốn actor này.");
});

/* ======================= MAIN FEATURES ======================= */
{
  const s = slide("Yêu cầu", "Tính năng chính", "Tính năng chính");
  table(s, [
    ["Tính năng", "Mô tả", "Actor chính"],
    ["Tài khoản và truy cập", "Đăng nhập email không mật khẩu hoặc Google", "Tất cả"],
    ["Project và thành viên", "Quản lý thành viên, settings và audit log của project", "Project Manager"],
    ["Quản lý dữ liệu", "Lưu dataset version bất biến trên platform hoặc trên máy local", "Researcher"],
    ["Quản lý Research Run", "Điều phối năm stage, theo dõi trạng thái, huỷ lượt nghiên cứu", "Researcher"],
    ["Kiểm soát của người", "Chọn preset, trả lời pinned action qua Decision Inbox, ghi decision log", "Researcher"],
    ["Vòng review độc lập", "Review độc lập mọi artifact version", "Reviewer"],
    ["Local Node", "Giữ dữ liệu local trên máy, chỉ gửi số liệu tổng hợp", "Researcher"],
    ["Ngân sách và chi phí", "Đặt ngân sách theo lượt nghiên cứu và theo tháng", "Project Manager"],
    ["Research Dossier và export", "Tạo Dossier có version, duyệt theo review settings", "Researcher"],
    ["ML Method Comparison", "So sánh phương pháp học máy, làm sau MVP", "Researcher"],
    ["Journal Fingerprint và Claim Ledger", "Làm sau MVP", "Researcher"],
  ], { y: 3.0, colW: [5.9, 8.0, 3.95], fontSize: 16, fillTo: 9.5 });
  note(s, "Năm stage nghiên cứu đã trình bày ở phần Phương pháp. Hai dòng cuối nằm ngoài cam kết của Review 2.", 9.75, T.amber);
  s.addNotes("Danh sách lấy từ phần I mục 6.1. Năm stage nghiên cứu không lặp lại ở đây vì đã có slide riêng.\n\nJournal Fingerprint Extraction ở mức Could, ML Method Comparison ở mức Should, Claim Ledger tạm xếp mức Could.");
}

/* ======================= 17. SYSTEM ARCHITECTURE ======================= */
pres.addSection({ title: "Thiết kế" });
{
  const s = slide("Thiết kế", "Kiến trúc hệ thống", "Kiến trúc tổng thể");
  fitImage(s, D("diagrams/04-system-overview/System-Architecture-Diagram.png"), 3725, 2053, MX, 2.9, CW, 7.6);
  s.addNotes("Năm stage engine chạy trên cùng một AI Engine runtime, chỉ khác cấu hình. Đây là cách nhóm bốn người làm được năm stage.\n\nPlatform giữ danh tính, project, lượt nghiên cứu, ngân sách, key, audit, Lock, disclosure và Research Dossier. Platform không phán xét nội dung khoa học.\n\nRanh giới tin cậy giải thích ở slide sau.");
}

/* ======================= HARNESS ENGINEERING ======================= */
{
  const s = slide("Thiết kế", "Harness engineering", "Mỗi việc AI làm đều đi qua cùng một lớp kiểm soát trước khi tới tay người nghiên cứu");
  /* Hai hàng thẳng cột: hàng trên là việc harness làm, hàng dưới là lợi ích cho người nghiên cứu */
  const LW = 2.4, G = 0.3, FX = MX + LW + 0.1, FW = CW - LW - 0.1, PAD = 0.25, X0 = FX + PAD, nw = (FW - 2 * PAD - 5 * G) / 6;
  const FY = 2.85, NY = FY + 0.75, NH = 1.9, RY = NY + NH + 0.45, FH = RY + 0.35 - FY, BY = FY + FH + 0.35, BH = 1.75;
  /* Khung harness bọc sáu bước, hàng đầu khung cho biết năm stage nào dùng nó */
  s.addShape(pres.ShapeType.roundRect, { x: FX, y: FY, w: FW, h: FH, fill: { color: T.peachSoft }, rectRadius: 0.06, line: { color: T.orange, width: 1.75 }, objectName: "harness" });
  s.addText("AI ENGINE RUNTIME (HARNESS)", { x: X0, y: FY + 0.12, w: 3.9, h: 0.45, isTextBox: true, margin: 0, valign: "middle", fontSize: 16.5, bold: true, charSpacing: 0.5, color: T.amber, fontFace: HEAD });
  s.addText("Dùng chung cho cả năm stage, từ Dataset tới Paper", { x: FX + FW - PAD - 7.5, y: FY + 0.12, w: 7.5, h: 0.45, isTextBox: true, margin: 0, align: "right", valign: "middle", fontSize: 16.5, bold: true, color: T.amber, fontFace: BODY });
  s.addText("Harness là lớp code bao quanh AI. Mỗi đề xuất của AI đi qua sáu bước rồi mới thành kết quả.", { x: MX, y: 2.2, w: CW, h: 0.5, isTextBox: true, margin: 0, valign: "middle", fontSize: 19, color: T.ink2, fontFace: BODY });
  const STEPS = [
    ["AI đề xuất", "AI", "Tạo hành động hoặc bản nháp cho stage", "llm", "Nhận sẵn bản nháp và gợi ý bước tiếp"],
    ["GUARD", "CODE", "Xếp mức kiểm soát và chặn bước sai thứ tự", "gate", "Được hỏi trước ở Decision Inbox khi bước đó cần người quyết"],
    ["Thực thi", "CODE", "Chạy phân tích trong sandbox trên data twin", "code", "Giữ dữ liệu gốc an toàn trong lúc AI thử phân tích"],
    ["CHECK", "CODE", "Kiểm contract và để code tính mọi con số", "gate", "Tính lại được mọi con số trong kết quả"],
    ["REVIEW", "AI", "Cho reviewer có context mới đọc lại artifact", "gate", "Thấy lỗi phương pháp trước khi nhận kết quả"],
    ["TRACE", "CODE", "Ghi lại mọi bước và quyết định", "trace", "Chạy lại ra cùng kết quả cho người khác kiểm tra"],
  ];
  const label = (y, h, t) => s.addText(t, { x: MX, y, w: LW, h, isTextBox: true, margin: 0, valign: "middle", fontSize: 16, bold: true, charSpacing: 1.2, color: T.amber, fontFace: HEAD });
  label(NY, NH, "HARNESS LÀM GÌ");
  label(BY, BH, "NGƯỜI NGHIÊN CỨU ĐƯỢC GÌ");
  const cx = (i) => X0 + i * (nw + G) + nw / 2;
  STEPS.forEach(([h, who, d, k, gain], i) => {
    const x = X0 + i * (nw + G);
    const st = { llm: [T.white, T.ink2], gate: [T.peach, T.orange], code: [T.soft, T.softLine], trace: [T.white, T.softLine] }[k];
    s.addShape(k === "gate" ? pres.ShapeType.hexagon : pres.ShapeType.roundRect, { x, y: NY, w: nw, h: NH, fill: { color: st[0] }, rectRadius: 0.1, line: { color: st[1], width: k === "llm" ? 2 : 1.5, dashType: k === "trace" ? "dash" : "solid" }, objectName: `node-${i}` });
    s.addText([{ text: `${i + 1}  ${who}`, options: { fontSize: 16, bold: true, color: who === "AI" ? T.ink2 : T.muted, fontFace: HEAD, breakLine: true } },
      { text: h, options: { fontSize: 18, bold: true, color: k === "gate" ? T.amber : T.ink, fontFace: HEAD, breakLine: true } },
      { text: d, options: { fontSize: 16, color: T.body, fontFace: BODY } }],
      { x: x + (k === "gate" ? 0.3 : 0.15), y: NY, w: nw - (k === "gate" ? 0.6 : 0.3), h: NH, isTextBox: true, margin: 0, align: "center", valign: "middle", paraSpaceAfter: 2 });
    if (i < 4) arrow(s, x + nw + 0.02, NY + NH / 2, G - 0.04, 0, T.ink2);
    /* Lợi ích thẳng cột với bước tạo ra nó */
    s.addShape(pres.ShapeType.roundRect, { x, y: BY, w: nw, h: BH, fill: { color: T.peachSoft }, rectRadius: 0.08, line: { color: T.orange, width: 1 }, objectName: `gain-${i}` });
    s.addText(gain, { x: x + 0.18, y: BY, w: nw - 0.36, h: BH, isTextBox: true, margin: 0, valign: "middle", fontSize: 18, color: T.ink, fontFace: BODY });
  });
  /* Vòng sửa: Check không đạt thì quay về AI */
  s.addShape(pres.ShapeType.line, { x: cx(3), y: NY + NH, w: 0, h: RY - NY - NH, line: { color: T.orange, width: 1.5 }, objectName: "ret-v" });
  s.addShape(pres.ShapeType.line, { x: cx(0), y: RY, w: cx(3) - cx(0), h: 0, line: { color: T.orange, width: 1.5 }, objectName: "ret-h" });
  arrow(s, cx(0), RY, 0, -(RY - NY - NH - 0.03), T.orange);
  s.addText("Check không đạt thì AI sửa lại, tối đa hai vòng", { x: cx(0) + 0.8, y: RY - 0.2, w: cx(3) - cx(0) - 1.6, h: 0.4, isTextBox: true, margin: 0, align: "center", valign: "middle", fontSize: 16.5, bold: true, color: T.amber, fontFace: BODY, fill: { color: T.peachSoft } });
  /* Phân vai ở cuối slide */
  const VY = BY + BH + 0.4;
  s.addShape(pres.ShapeType.roundRect, { x: MX, y: VY, w: CW, h: 0.8, fill: { color: T.surf }, rectRadius: 0.08, line: { color: T.line }, objectName: "roles" });
  s.addText([{ text: "PHÂN VAI   ", options: { bold: true, fontSize: 16.5, charSpacing: 1.2, color: T.amber, fontFace: HEAD } },
    { text: "AI đề xuất và review. Code tính số và chặn bước sai. Người nghiên cứu quyết định và chịu trách nhiệm.", options: { fontSize: 17, color: T.ink, fontFace: BODY } }],
    { x: MX + 0.3, y: VY, w: CW - 0.6, h: 0.8, isTextBox: true, margin: 0, valign: "middle" });
  s.addNotes("Nguồn: Report 7 phần IV §1.1.1 (mọi stage engine chạy trên một AI Engine runtime), §1.1.3 Trust boundaries (TB2, TB3, TB5), ADR-02, ADR-05, ADR-06, ADR-07, ADR-08, NFR-20 gọi runtime chung là harness, FR-26 (ba mức Auto, Do Then Review, Must Ask), FR-29, FR-30, FR-50, FR-71 đến FR-75, FR-133, FR-169, FR-197, FR-199, NFR-26.\n\nCách đọc: hàng trên là việc harness làm với mỗi đề xuất của AI, hàng dưới là điều người nghiên cứu nhận được từ bước đó. Guard quyết định hành động được tự làm, làm rồi người xem lại, hay phải hỏi người trước qua Decision Inbox. LLM chỉ nhận text và schema, không thấy dữ liệu thật. Artifact qua đủ các bước thì được accept, có version và hash, rồi Platform lưu Lock và Dossier. Trace ghi lại toàn bộ để chạy lại ra cùng hash.\n\nĐộ tin cậy của AI reviewer: FR-77 đo precision từng persona trên seeded-flaw benchmark, FR-229 chỉ bật persona khi bắt được lỗi mà persona khác bỏ sót, FR-135 đến FR-137 cài lỗi data, experiment và inference.");
}

/* ======================= 20. TECHNOLOGY ======================= */
{
  const s = slide("Thiết kế", "Công nghệ", "Công nghệ và môi trường");
  /* Mỗi hàng: nhóm công nghệ bên trái, các lựa chọn kèm logo bên phải.
     Hàng nhiều lựa chọn được chia thành hai dòng để chữ không bị nhỏ. */
  const ROWS = [
    ["Front-end", [
      [["nextdotjs", "Next.js 16"], ["react", "React 19"], ["typescript", "TypeScript"], ["tailwindcss", "Tailwind CSS"], ["shadcnui", "shadcn/ui"], ["radixui", "Radix UI"]],
      [["reactquery", "TanStack Query"], ["redux", "Redux Toolkit"], [null, "Zustand"], ["reacthookform", "React Hook Form"], ["zod", "Zod"], ["axios", "Axios"]],
    ]],
    ["Back-end", [[["python", "Python 3.12"], ["fastapi", "FastAPI"]]]],
    ["Cơ sở dữ liệu và lưu trữ", [[["postgresql", "PostgreSQL 16"], ["cloudflare", "Cloudflare R2"]]]],
    ["AI và tài liệu khoa học", [[[null, "OpenAI"], ["googlegemini", "Google Gemini"], ["openrouter", "OpenRouter"], ["openaccess", "OpenAlex"], ["arxiv", "arXiv"], ["semanticscholar", "Semantic Scholar"]]]],
    ["Hạ tầng và DevOps", [
      [["traefikproxy", "Traefik"], [null, "Dokploy"], ["docker", "Docker Hub"], ["github", "GitHub"], ["githubactions", "GitHub Actions"]],
      [["vitest", "Vitest"], ["biome", "Biome"], [null, "Husky"], ["resend", "Resend"], ["google", "Google sign-in"]],
    ]],
  ];
  const LX = MX, LW = 4.0, RX = MX + 4.35, RW = CW - 4.35, GAP = 0.1, H1 = 0.92, LINE = 0.62;
  let y = 2.95;
  ROWS.forEach((row, r) => {
    const lines = row[1], h = lines.length === 1 ? H1 : H1 + LINE;
    card(s, { x: LX, y, w: LW, h, fill: T.peachSoft, border: T.peach, name: `cat-${r}` });
    s.addText(row[0], { x: LX + 0.35, y, w: LW - 0.7, h, isTextBox: true, margin: 0, valign: "middle", fontSize: 19, bold: true, color: T.amber, fontFace: HEAD });
    card(s, { x: RX, y, w: RW, h, fill: T.white, border: T.line, name: `tech-${r}` });
    lines.forEach((items, li) => {
      const ly = lines.length === 1 ? y : y + li * LINE + 0.08, lh = lines.length === 1 ? h : LINE;
      const iw = (RW - 0.7) / items.length;
      items.forEach((it, k) => {
        const x = RX + 0.35 + k * iw;
        if (it[0]) s.addImage({ path: TI(it[0]), x, y: ly + (lh - 0.42) / 2, w: 0.42, h: 0.42, objectName: `logo-${r}-${li}-${k}` });
        s.addText(it[1], { x: x + (it[0] ? 0.55 : 0), y: ly, w: iw - (it[0] ? 0.62 : 0.1), h: lh, isTextBox: true, margin: 0, valign: "middle", fontSize: 16.5, color: T.ink2, fontFace: BODY });
      });
    });
    y += h + GAP;
  });
  /* Hàng môi trường: hai môi trường đang chạy, một môi trường mới đặc tả */
  card(s, { x: LX, y, w: LW, h: H1, fill: T.peachSoft, border: T.peach, name: "cat-env" });
  s.addText("Môi trường", { x: LX + 0.35, y, w: LW - 0.7, h: H1, isTextBox: true, margin: 0, valign: "middle", fontSize: 19, bold: true, color: T.amber, fontFace: HEAD });
  card(s, { x: RX, y, w: RW, h: H1, fill: T.white, border: T.line, name: "tech-env" });
  [["Development", "đang chạy", false], ["Production", "đang chạy", false], ["Staging", "đã đặc tả, chưa deploy", true]].forEach((e, k) => {
    const w = (RW - 0.7) / 3, x = RX + 0.35 + k * w;
    s.addText(e[0], { x, y: y + 0.1, w: w - 0.2, h: 0.4, isTextBox: true, margin: 0, fontSize: 17, bold: true, color: e[2] ? T.amber : T.ink, fontFace: HEAD });
    s.addText(e[1], { x, y: y + 0.48, w: w - 0.2, h: 0.36, isTextBox: true, margin: 0, fontSize: 16, color: e[2] ? T.amber : T.muted, fontFace: BODY });
  });
  s.addNotes("Danh sách thư viện front-end lấy từ package.json của repo sản phẩm. Back-end và hạ tầng lấy theo System Architecture Diagram.\n\nCode được quản lý bằng Git và pull request. Nhánh release chỉ nhận thay đổi khi CI chạy qua. Husky và lint-staged kiểm tra trước khi commit, Biome lo lint và format, Vitest chạy unit test front-end.\n\nKey của model do Platform Admin cấu hình. Hệ thống chỉ dùng tài liệu open-access. Literature API còn có Crossref, nhưng không có logo nên không đưa lên slide.\n\nLocal Node chạy cạnh dữ liệu trên máy người dùng và chỉ gửi số liệu tổng hợp qua release gate.\n\nStaging đã đặc tả nhưng chưa deploy. Đây là câu hỏi nhóm xin hội đồng quyết: buổi demo Hội đồng 1.1 chạy trên staging hay production.");
}

/* ======================= 21. DEMO WORKFLOWS ======================= */
pres.addSection({ title: "Workflow và demo" });
{
  const s = slide("Workflow và demo", "Workflow demo cho Hội đồng 1.1", "Danh sách workflow sẽ demo");
  table(s, [
    ["Workflow", "Actor", "Mô tả"],
    ["Lập project và đăng ký dữ liệu", "Project Manager, Researcher", "Tạo project, mời thành viên, đăng ký dataset version"],
    ["Stage Dataset và Hypothesis", "Researcher, Reviewer", "Chạy hai stage đầu, chấp nhận DatasetSnapshot và HypothesisSet"],
    ["Lock, chạy và disclosure", "Researcher", "Khoá kế hoạch, chạy phân tích, mở kết quả sau Lock"],
    ["Gửi số liệu từ Local Node", "Researcher, Reviewer", "Dữ liệu ở lại máy, chỉ số liệu tổng hợp đi qua release gate"],
    ["Duyệt và export Research Dossier", "Researcher, Reviewer, Project Manager", "Export bị chặn trước khi duyệt và mở sau khi duyệt"],
  ], { y: 3.1, colW: [5.4, 5.0, 7.45], fontSize: 18, fillTo: 8.9 });
  callout(s, "Tổng thời lượng 18 phút. Seed data được nạp bằng script trước buổi demo. Nếu thiếu thời gian, nhóm bỏ workflow đầu tiên trước.", 9.15, "peach");
  s.addNotes("Kết quả hội đồng sẽ thấy ở từng workflow:\nWF-01: dataset version xuất hiện và thành viên thấy project.\nWF-02: hai artifact được chấp nhận và decision log có dữ liệu.\nWF-03: verdict và mức kết luận do code tính, kết quả chỉ mở sau Lock.\nWF-04: dữ liệu local không rời máy, chỉ số liệu tổng hợp đi qua release gate.\nWF-05: export bị chặn trước khi duyệt và mở sau khi duyệt.\n\nKhông cắt WF-03 và WF-04, vì hai workflow này mang đúng hai luận điểm của đề tài.");
}

/* ======================= 22. PROGRESS ======================= */
pres.addSection({ title: "Tình trạng" });
{
  const s = slide("Tình trạng", "Tiến độ và phân công", "Tiến độ và đóng góp");
  [["190", "man-day kế hoạch"], ["16", "tính năng Must"], ["65", "use case"], ["58", "system test case"]].forEach((st, i) => {
    const w = (CW - 3 * 0.35) / 4, x = MX + i * (w + 0.35);
    s.addShape(pres.ShapeType.roundRect, { x, y: 2.95, w, h: 1.6, fill: { color: i === 0 ? T.peachSoft : T.surf }, rectRadius: 0.12, line: { color: i === 0 ? T.peach : T.surf }, objectName: `stat-${i}` });
    s.addText(st[0], { x: x + 0.45, y: 3.05, w: w - 0.9, h: 0.85, isTextBox: true, margin: 0, fontSize: 44, bold: true, color: i === 0 ? T.amber : T.ink, fontFace: HEAD });
    s.addText(st[1], { x: x + 0.45, y: 3.9, w: w - 0.9, h: 0.5, isTextBox: true, margin: 0, fontSize: 18, color: i === 0 ? T.amber : T.muted, fontFace: BODY });
  });
  /* Thanh kết quả system test vòng 3: 48 Passed, 9 Pending, 1 Failed */
  colLabel(s, "System test vòng 3", MX, 4.85, 6);
  const BX = MX, BY = 5.3, BW = CW, BH = 0.7, TOT = 58;
  let bx = BX;
  [[48, "48 Passed", T.surf, T.ink], [9, "9 Pending", T.peach, T.amber], [1, "1 Failed", T.ink, T.white]].forEach(([n, t, f, c], i) => {
    const w = BW * n / TOT;
    s.addShape(pres.ShapeType.rect, { x: bx, y: BY, w, h: BH, fill: { color: f }, line: { color: T.white, width: 1 }, objectName: `bar-${i}` });
    if (i < 2) s.addText(t, { x: bx + 0.2, y: BY, w: Math.max(w - 0.3, 2), h: BH, isTextBox: true, margin: 0, valign: "middle", fontSize: 16, bold: true, color: c, fontFace: HEAD });
    bx += w;
  });
  s.addText("1 Failed", { x: BX + BW - 2.0, y: BY + BH + 0.05, w: 2.0, h: 0.35, isTextBox: true, margin: 0, align: "right", fontSize: 16, color: T.ink, fontFace: BODY });
  s.addText("Các case Pending cần LLM provider để chạy Research Run. Unit test bao phủ 40 hàm.", { x: BX, y: BY + BH + 0.05, w: 12, h: 0.35, isTextBox: true, margin: 0, fontSize: 16, color: T.muted, fontFace: BODY });
  /* bằng chứng khả thi lấy từ repo code */
  s.addShape(pres.ShapeType.roundRect, { x: MX, y: 6.5, w: CW, h: 0.62, fill: { color: T.peachSoft }, rectRadius: 0.08, line: { color: T.peach }, objectName: "feasible" });
  s.addText([{ text: "BẰNG CHỨNG KHẢ THI   ", options: { bold: true, fontSize: 16.5, charSpacing: 1.2, color: T.amber, fontFace: HEAD } }, { text: "Cả năm stage engine đã có code và test. Bench của critic có 13 lỗi cài sẵn và 13 case đánh giá có gold references.", options: { fontSize: 16.5, color: T.ink2, fontFace: BODY } }],
    { x: MX + 0.3, y: 6.5, w: CW - 0.6, h: 0.62, isTextBox: true, margin: 0, valign: "middle" });
  table(s, [
    ["Thành viên", "Vai trò", "Chịu trách nhiệm chính"],
    ["Lê Vũ Phương Hòa", "Leader, Backend", "Lập kế hoạch, Platform backend và database, deployment"],
    ["Ngô Thành Đạt", "Backend, AI", "Requirements và use case, stage contract, research stage và AI PI"],
    ["Trần Phú Thịnh", "Frontend", "UI/UX, workspace và trang admin, run studio"],
    ["Uông Tuấn Vũ", "Test", "Testing và defect management, hỗ trợ deployment"],
  ], { y: 7.35, colW: [4.0, 3.6, 10.25], fontSize: 17, fillTo: 9.95 });
  s.addNotes("Kế hoạch 190 man-day gồm 180 man-day công việc và 10 man-day dự phòng, trong 12 tuần. Phân bổ cho requirements và thiết kế 6, backend 53, AI Research 73, frontend 29, testing 16, deployment 3.\n\nSystem test vòng 3 có 58 case: 48 Passed, 9 Pending, 1 Failed. 9 case Pending thuộc Research Run Orchestration vì cần LLM provider. Case Failed thuộc Administration và đã có defect.\n\nBảng thành viên theo RACI ở phần II.\n\nBằng chứng khả thi lấy từ repo logos: stages/dataset, stages/hypothesis, stages/experiment-design (nhánh dev), stages/execution có bench riêng và stages/paper (nhánh feat/stage-harness), stages/writing (nhánh feat/writing); eval/flaws/flaws.yaml có 13 lỗi cài sẵn (leakage, selective reporting, statistics, metric validity, baseline, benchmark choice) và eval/cases có 13 case với gold references từ OpenAlex. Các engine đang ở nhiều nhánh và còn phải gộp, việc này nằm trong kế hoạch tuần 12 đến 15.");
}

/* ======================= 23. RISKS ======================= */
{
  const s = slide("Tình trạng", "Rủi ro", "Rủi ro gắn với thiết kế");
  table(s, [
    ["ID", "Rủi ro", "Cách xử lý"],
    ["R-02", "Suy luận từ nhiều số liệu tổng hợp có thể lộ dữ liệu cá nhân", "Áp ngưỡng small-cell, giới hạn số lần truy vấn và ghi release log"],
    ["R-03", "Data twin khác dữ liệu thật", "Chạy dry run để đối chiếu data twin trước khi Lock"],
    ["R-04", "Platform là điểm tin cậy duy nhất cho disclosure", "Phân quyền, dùng audit log chỉ ghi thêm và code review"],
    ["R-13, R-14", "Nhóm nhỏ, thời gian cố định và phạm vi dễ phình", "Dùng chung một AI Engine runtime và đẩy hai tính năng mở rộng sang sau MVP"],
  ], { y: 3.1, colW: [2.2, 8.15, 7.5], fontSize: 19, fillTo: 9.6 });
  s.addNotes("Phần II có 15 rủi ro dự án. Slide chọn những rủi ro gắn với thiết kế.\n\nR-04: thiết kế không chặn được người sửa được code Platform. Nhóm chấp nhận rủi ro này và ghi bằng văn bản.");
}

/* ======================= 24. PLAN ======================= */
{
  const s = slide("Tình trạng", "Kế hoạch tới tuần 15", "Các mốc bàn giao còn lại");
  [
    ["Tuần 10", "Phân tích dữ liệu và giả thuyết", "Stage Dataset, Hypothesis"],
    ["Tuần 12 và 13", "Thiết kế thí nghiệm, chạy phân tích, bằng chứng", "Stage Experiment Design, Execution"],
    ["Tuần 13", "Chạy lại system test", "Đóng 9 case Pending và 1 case Failed"],
    ["Tuần 14", "Review, bản thảo, Research Dossier", "Stage Paper, Research Dossier và Hội đồng 1.1"],
    ["Tuần 15", "Hệ thống tích hợp hoàn chỉnh", "Bàn giao"],
  ].forEach((it, i) => {
    const y = 3.2 + i * 1.4, hot = i >= 3;
    s.addShape(pres.ShapeType.ellipse, { x: MX, y: y + 0.1, w: 0.8, h: 0.8, fill: { color: hot ? T.peach : T.surf }, line: { color: hot ? T.peach : T.line }, objectName: `step-${i}` });
    s.addText(String(i + 1), { x: MX, y: y + 0.1, w: 0.8, h: 0.8, isTextBox: true, margin: 0, align: "center", valign: "middle", fontSize: 21, bold: true, color: hot ? T.amber : T.faint, fontFace: HEAD });
    if (i < 4) s.addShape(pres.ShapeType.line, { x: MX + 0.4, y: y + 0.95, w: 0, h: 0.5, line: { color: T.line, width: 1.5 }, objectName: `step-line-${i}` });
    s.addText(it[0], { x: MX + 1.2, y: y + 0.2, w: 3.0, h: 0.55, isTextBox: true, margin: 0, fontSize: 19, bold: true, charSpacing: 1.2, color: T.amber, fontFace: HEAD });
    s.addText(it[1], { x: MX + 4.4, y: y + 0.12, w: 7.4, h: 0.75, isTextBox: true, margin: 0, fontSize: 25, bold: true, color: T.ink, fontFace: HEAD });
    s.addText(it[2], { x: MX + 12.0, y: y + 0.22, w: 5.85, h: 0.6, isTextBox: true, margin: 0, fontSize: 19, color: T.body, fontFace: BODY });
  });
  note(s, "Đã bàn giao thiết kế (tuần 3), user, project và platform (tuần 5), dữ liệu và xử lý local (tuần 7), workflow AI (tuần 9).", 10.2);
  s.addNotes("Các mốc lấy từ bảng deliverables ở phần II. Mốc tuần 13 chạy lại system test là việc cần làm để đóng các case Pending và Failed.");
}

/* ======================= 25. THANK YOU ======================= */
{
  N += 1;
  const s = pres.addSlide({ sectionTitle: "Tình trạng" });
  s.background = { color: T.white };
  chrome(s, { n: N });
  /* Khối chính: lời cảm ơn và Q&A, canh trái theo lề chung của deck */
  s.addText("CẢM ƠN HỘI ĐỒNG ĐÃ LẮNG NGHE", { x: MX, y: 2.9, w: CW, h: 0.5, isTextBox: true, margin: 0, fontSize: 20, bold: true, charSpacing: 3, color: T.amber, fontFace: HEAD });
  s.addText("Q&A", { x: MX - 0.08, y: 3.45, w: 10, h: 2.6, isTextBox: true, margin: 0, valign: "middle", fontSize: 150, bold: true, color: T.ink, fontFace: HEAD });
  s.addShape(pres.ShapeType.rect, { x: MX, y: 6.25, w: 1.6, h: 0.08, fill: { color: T.orange }, line: { color: T.orange }, objectName: "qa-rule" });
  s.addText("Nhóm rất mong nhận được câu hỏi và góp ý của Hội đồng.", { x: MX, y: 6.55, w: CW, h: 0.6, isTextBox: true, margin: 0, fontSize: 24, color: T.ink2, fontFace: BODY });
  /* Dải thông tin cuối trang, ngăn bằng một đường mảnh */
  const IY = 8.35;
  s.addShape(pres.ShapeType.line, { x: MX, y: IY, w: CW, h: 0, line: { color: T.line, width: 1 }, objectName: "qa-line" });
  /* Theo hướng dẫn Review 2 mục 7.1: liên hệ nhóm trưởng, repository và hệ thống demo */
  [
    ["Liên hệ nhóm trưởng", "Lê Vũ Phương Hòa", "hoalvpse181951@fpt.edu.vn", "mailto:hoalvpse181951@fpt.edu.vn"],
    ["Kho mã nguồn", "github.com/openai-scientist", "Mã nguồn và tài liệu dự án", "https://github.com/openai-scientist"],
    ["Hệ thống demo", "scientist.beyond8.io.vn", "Tài khoản demo cho từng role", "https://scientist.beyond8.io.vn/"],
  ].forEach(([h, v, sub, url], i) => {
    const w = CW / 3, x = MX + i * w;
    s.addText([{ text: h.toUpperCase(), options: { fontSize: 16, bold: true, charSpacing: 1.8, color: T.muted, fontFace: HEAD, breakLine: true } },
      { text: v, options: { fontSize: 21, bold: true, color: T.ink, fontFace: HEAD, breakLine: true, hyperlink: i ? { url } : undefined } },
      { text: sub, options: { fontSize: 16, color: T.body, fontFace: BODY, hyperlink: i ? undefined : { url } } }],
      { x, y: IY + 0.3, w: w - 0.3, h: 1.45, isTextBox: true, margin: 0, valign: "top", paraSpaceAfter: 4 });
  });
  s.addNotes("Hệ thống demo: https://scientist.beyond8.io.vn/. Tài khoản demo cho từng role ghi trong tờ phát tay. Cảm ơn Hội đồng rồi mời đặt câu hỏi.");
}

(async () => {
  await pres.writeFile({ fileName: OUT });
  console.log("written", OUT);
})();
