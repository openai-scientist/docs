"""Business-level Conceptual ERD for Report 7 (about 33 entities).

Reduces the full LOGOS model in ../v2 (91 entities) to the business concepts:
technical logs, projections, Core references and infrastructure tables are left out,
child records fold into their parent, and "Ref" suffixes are dropped. The reduced model
is then drawn by build_erd.py with the same style and router.

usage: python3 build_business_erd.py [--detail]   (run inside diagrams/03-conceptual-erd/v3)
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
V2 = HERE.parent / "v2"   # shared style, router and full model
sys.path.insert(0, str(V2))
import build_erd  # noqa: E402

KEEP = {
    # M01, M02 identity and project
    "Tenant": None, "User": None, "Membership": None, "Project": None, "Invitation": None,
    "Responsibility": None,
    # M03 research
    "ResearchCaseRef": "ResearchCase", "InquiryRef": "Inquiry", "ScientificObjectRef": "ScientificObject",
    "Discussion": None,
    # M04 data
    "DataSource": None, "DataVersionRef": "DataVersion", "DataUseGrant": None, "Connector": None,
    # M05 decision and review
    "DecisionTask": None, "ApprovalRequest": None, "ReviewAssignment": None, "ReviewComment": None,
    # M06 run
    "RunRequest": None, "RunAttempt": None,
    # M07 results
    "ScientificPackageRef": "ScientificPackage", "ReleaseManifest": None, "ShareGrant": None,
    "ManuscriptJob": "Manuscript",
    # M08, M09 configuration and AI
    "PolicyRule": None, "ConfigVersion": None, "ModelOffering": None, "CredentialRef": None,
    # M10 budget
    "BudgetAccount": None, "BudgetReservation": None,
    # M11, M12 operations
    "Notification": None, "AuditEvent": None,
}
# child records shown as part of their parent at the conceptual level
MERGE = {"DecisionOption": "DecisionTask", "DecisionResponse": "DecisionTask",
         "ApprovalVote": "ApprovalRequest", "RoleGrant": "Membership",
         # run admission, credential and pricing details fold into the business entity they describe
         "AdmissionReceipt": "RunRequest", "CredentialBinding": "CredentialRef", "CredentialVersion": "CredentialRef",
         "EffectiveConfigSnapshot": "ConfigVersion", "SettingDefinition": "ConfigVersion",
         "PolicyException": "PolicyRule", "Provider": "ModelOffering", "RateCard": "ModelOffering"}
# Incident is left out: the source model links it only to SupportAccessGrant, an operations record
# two blocks drawn top and bottom: people, projects and research work; then data, runs and results
PEOPLE_AND_WORK = {"Tenant", "User", "Membership", "Project", "Invitation", "Responsibility", "Notification",
                   "AuditEvent", "ResearchCase", "Inquiry", "ScientificObject", "Discussion", "DecisionTask",
                   "ReviewAssignment", "ReviewComment", "ApprovalRequest"}
OUT = HERE / "Entity-Relationship-Diagram-Business.drawio"
MODEL = HERE / "business_model.py"


# --detail: about 55 entities; brings back the records a reader needs to follow each business rule
DETAIL_KEEP = {"RoleGrant": None, "Delegation": None, "Handover": None,
               "DecisionOption": None, "DecisionResponse": None, "ApprovalVote": None, "ConflictDeclaration": None,
               "DataClassification": None, "ReleasePolicy": None, "ReleaseReview": None,
               "AdmissionReceipt": None, "ResearchAssetRef": "ResearchAsset", "ExportJob": None,
               "SettingDefinition": None, "PolicyException": None,
               "Provider": None, "CredentialBinding": None, "RateCard": None,
               "UsageEvent": None, "LedgerEntry": None, "Quota": None,
               "NotificationPreference": None, "Incident": None, "SupportAccessGrant": None,
               "LegalHold": None, "DeletionRequest": None,
               # second layer: sessions, receipts, file versions, run steps, routing and allocation rules
               "Session": None, "ServicePrincipal": None, "ProjectTemplate": None, "AuthorityReceipt": None,
               "DataFileVersion": None, "RunDataAccess": None, "RunPlanStep": None, "RunTimelineEntry": None,
               "FeatureFlag": None, "CredentialVersion": None, "RoutingPolicy": None, "BudgetException": None,
               "Allocation": None, "RetentionRule": None}
DETAIL_WORK = {"RoleGrant", "Delegation", "Handover", "DecisionOption", "DecisionResponse", "ApprovalVote",
               "ConflictDeclaration", "NotificationPreference", "Incident", "SupportAccessGrant", "LegalHold",
               "DeletionRequest"}


# detailed figure: small blocks packed into rows (order follows the module order of build_erd)
DETAIL_GROUPS = [
    {"Tenant", "User", "Membership", "RoleGrant", "Delegation", "ConflictDeclaration", "Notification",
     "NotificationPreference", "AuditEvent", "Incident", "SupportAccessGrant", "Session", "ServicePrincipal", "RetentionRule"},                                                      # identity
    {"Project", "Invitation", "Responsibility", "Handover", "LegalHold", "DeletionRequest", "Quota", "ProjectTemplate"},  # project
    {"DataSource", "DataVersion", "DataClassification", "DataUseGrant", "Connector", "DataFileVersion", "RunDataAccess"},              # data
    {"ResearchCase", "Inquiry", "ScientificObject", "Discussion", "DecisionTask", "DecisionOption", "DecisionResponse",
     "ApprovalRequest", "ApprovalVote", "ReviewAssignment", "ReviewComment", "AuthorityReceipt"},                     # research, review
    {"PolicyRule", "PolicyException", "ConfigVersion", "SettingDefinition", "Provider", "ModelOffering", "RateCard",
     "CredentialRef", "CredentialBinding", "FeatureFlag", "CredentialVersion", "RoutingPolicy"},                                                        # configuration, AI
    {"RunRequest", "AdmissionReceipt", "RunAttempt", "UsageEvent", "BudgetAccount", "BudgetReservation",
     "LedgerEntry", "RunPlanStep", "RunTimelineEntry", "BudgetException", "Allocation"},                                                                               # runs, budget
    {"ScientificPackage", "ReleaseManifest", "ShareGrant", "ResearchAsset", "ExportJob", "Manuscript",
     "ReleasePolicy", "ReleaseReview"},                                                            # results
]
CODES = ["M01", "M02", "M05", "M08", "M04", "M09", "M10", "M06"]
GROUPS = []
ROW_ARGS = ["--per-row", "1"]


def module(n):
    if not GROUPS:
        return "M01" if n in PEOPLE_AND_WORK else "M02"
    return next((CODES[i] for i, g in enumerate(GROUPS) if n in g), CODES[len(GROUPS)])


def reduce(model):
    name = lambda n: MERGE.get(n) and (KEEP[MERGE[n]] or MERGE[n]) or (KEEP[n] or n if n in KEEP else None)
    ent = [(name(e[0]), module(name(e[0]))) + tuple(e[2:])
           for e in model.ENT if e[0] in KEEP]
    rel, seen = [], set()
    for r in model.REL:
        a, b = name(r[0]), name(r[1])
        if a and b and a != b and frozenset((a, b)) not in seen:
            seen.add(frozenset((a, b)))
            rel.append((a, b) + tuple(r[2:]))
    return ent, rel


def main():
    if "--detail" in sys.argv:
        global OUT
        KEEP.update(DETAIL_KEEP); PEOPLE_AND_WORK.update(DETAIL_WORK)
        for k in DETAIL_KEEP: MERGE.pop(k, None)
        OUT = HERE / "Entity-Relationship-Diagram-Business-Detailed.drawio"
        GROUPS[:] = DETAIL_GROUPS; ROW_ARGS[:] = ["--max-width", "2000", "--nodesep", "0.75", "--ranksep", "0.8", "--gap", "60"]
        global MODEL; MODEL = HERE / "business_model_detailed.py"
    model = build_erd.load_model(build_erd.DEFAULT_MODEL.resolve())
    ent, rel = reduce(model)
    MODEL.write_text("# generated by build_business_erd.py; do not edit\n"
                     f"ENT = {ent!r}\nREL = {rel!r}\nCONTEXTS = {model.CONTEXTS!r}\n")
    print(f"{len(ent)} entities, {len(rel)} relations")
    subprocess.run([sys.executable, str(V2 / "build_erd.py"), str(MODEL), str(OUT), *ROW_ARGS], check=True)


if __name__ == "__main__":
    main()
