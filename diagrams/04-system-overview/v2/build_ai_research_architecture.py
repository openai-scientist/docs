"""AI Research Architecture v2 (Report 7 IV, Figure IV-2), aligned with the LOGOS_Platform spec.

usage: python3 build_ai_research_architecture.py   (writes AI-Research-Architecture.html next to this file)

Same visual style as ../build_system_architecture_v3.py (its Figure and page helpers are reused).
Changes against v1 (System-Architecture-v3-ai-tier), from docs/LOGOS_Platform/02-kien-truc/01-tong-quan-kien-truc.md:
- the Platform does not run science: it sends commands with an ID through the Core Gateway and
  receives versioned events from the Scientific Core (no direct consult/advice into the AI PI)
- release of derived assets is the Platform airlock (M04 -> M07, ReleaseReview), not a box in the Local Node
- the Core calls AI providers with a short-lived credential lease issued by the Platform (M09)
- the Local Node keeps its own architecture (Q9); only compute requests and aggregates cross the boundary
No free-floating notes on the canvas.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import build_system_architecture_v3 as v3  # noqa: E402

Figure, page, LINK = v3.Figure, v3.page, v3.LINK
v3.ICONS.update({"Platform API": ("si-fastapi", "#009688"), "Release Airlock": ("tb-shield-lock", v3.INK)})
OUT = Path(__file__).resolve().parent / 'AI-Research-Architecture.html'


def ai_research():
    f = Figure()
    f.zone(24, 72, 192, 528, "LOGOS Platform", "app")
    f.zone(280, 72, 720, 360, "Scientific Core · on the VPS", "ai")
    f.zone(296, 220, 688, 196, "Shared AI Engine runtime · one container per engine", "ai", dashed=True)
    f.zone(280, 480, 512, 120, "Data holder · Local Node", "ext", dashed=True)
    f.zone(1032, 180, 208, 252, "AI services", "ext", dashed=True)

    EX, EW, EG, EY, EH = 312, 116, 20, 268, 100
    stages = [("Dataset", "DatasetSnapshot"), ("Hypothesis", "HypothesisSet"),
              ("Experiment\nDesign", "AnalysisPlan"), ("Execution", "EvidenceBundle"), ("Paper", "PaperPack")]

    # arrows: Platform <-> Core only through the Core Gateway
    f.arrow([(200, 300), (296, 300)])                                   # commands
    f.arrow([(296, 340), (200, 340)], dashed=True)                      # events
    f.arrow([(120, 352), (120, 448)])                                   # api -> release airlock
    f.arrow([(632, 184), (632, 220)], dashed=True)                      # ai pi -> engines (advice)
    for i in range(4):
        x = EX + i * (EW + EG) + EW
        f.arrow([(x, EY + EH / 2), (x + EG, EY + EH / 2)])
    f.arrow([(968, 152), (1200, 152), (1200, 220)], color=LINK)         # ai pi -> llm
    f.arrow([(984, 290), (1040, 290)], color=LINK)                      # engines -> llm
    f.arrow([(984, 380), (1040, 380)], color=LINK)                      # engines -> literature
    f.arrow([(460, 416), (460, 516)], dashed=True)                      # engines -> local node
    f.arrow([(680, 516), (680, 416)])                                   # local node -> engines

    # nodes
    f.node(40, 288, 160, 64, "Platform API", "Core Gateway", "focal")
    f.node(40, 448, 160, 96, "Release Airlock", "ReleaseReview")
    f.node(312, 120, 656, 64, "AI PI Service", "oversight · advises at stage end, failure and close", "focal")
    for i, (n, art) in enumerate(stages):
        f.node(EX + i * (EW + EG), EY, EW, EH, n, art)
    f.node(296, 516, 480, 48, "Local Node", "runs authorized jobs next to the data")
    f.node(1040, 220, 192, 88, "LLM providers", "OpenAI·Gemini·OpenRouter", "ext")
    f.node(1040, 336, 192, 88, "Literature APIs", "OpenAlex · arXiv · …", "ext")

    # labels
    f.label(248, 300, "Commands")
    f.label(248, 340, "Events")
    f.label(120, 404, "Release", "right")
    f.label(632, 202, "Advice", "right")
    f.label(1084, 152, "Prompts · lease")
    f.label(452, 456, "Compute requests", "left")
    f.label(688, 456, "Aggregates", "right")

    legend = [("focal", "focal component"), ("ext", "outside the VPS"),
              ("solid", "call"), ("link", "HTTPS to a provider"), ("dashed", "async")]
    desc = ("The Platform sends commands through the Core Gateway and receives versioned events; inside the "
            "Scientific Core the AI PI advises five stage engines, which call LLM providers with a short-lived "
            "credential lease and literature APIs, and send authorized compute requests to the Local Node, "
            "which returns only aggregates. Derived assets leave through the Platform release airlock.")
    return page("ai-research-v2", "Architecture · LOGOS · Figure IV-2", "AI research architecture",
                f.svg("ai-research-v2", "LOGOS AI research architecture", desc, legend))


if __name__ == "__main__":
    OUT.write_text(ai_research())
    print("written", OUT)
