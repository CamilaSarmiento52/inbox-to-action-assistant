"""Build the 30-email anchor set (EVALUATION.md: a set across categories that the user reads once).

Picks are fixed below with the reason for each. Only `tune` emails are allowed: the held-out quarter is never read
while prompts are tuned. Writes data/anchor_set.jsonl (copies of the emails, unchanged; kept outside data/emails/ so a loader reading every
*.jsonl there does not count them twice) and docs/ANCHOR_SET.md (a reading
sheet). Run from the project root after the other generators:  python3 tools/build_anchor_set.py
"""
import collections, glob, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMAILS = os.path.join(ROOT, "data", "emails")

# (email ID, what it checks). Grouped by expected label set; the guide rule in brackets.
PICKS = [
    # Quotation request
    ("E-QUO-007", "Full priced quote: three lines, one discount per line, free delivery lost after the discount"),
    ("E-QUO-028", "\"1,000 pipette tips\" when a box holds 960: price both options and ask"),
    ("E-QUO-048", "Stock and lead time only, no price asked: still a quotation [B-3]"),
    ("E-CMP-026", "Arrives among complaints but only asks a price: quotation [G-1]"),
    # Order status / delivery issue
    ("E-ORD-033", "Tells us to supply gloves and asks the price: an order, not a quote [B-1]"),
    ("E-ORD-036", "Cancels an order not yet delivered: order, not a return [B-6]"),
    ("E-OTH-023", "Order status written in German: classified by content, reply in English [G-7]"),
    # Return / quality complaint
    ("E-CMP-016", "Cracked VM-10 casing, remedy asked, no question: complaint only [B-5]"),
    ("E-ORD-040", "\"Cancel\" an order already delivered: a return [B-6]"),
    # Product documentation request
    ("E-DOC-028", "\"Catalogue\" for the vortex mixer: documentation, not a price list [B-2]"),
    ("E-OTH-029", "Manual request plus a work-experience question: no Other label [G-6]"),
    # Technical suitability question
    ("E-TEC-012", "Error persists after the documented steps: technical only, escalated [B-5]"),
    ("E-TEC-021", "Typo-ridden question about running the vortex all day: answered from the duty cycle"),
    ("E-TEC-023", "Liquid spilled inside the HB-2: stop-using reply, but user-caused, so no complaint [B-5]"),
    # Invoice / payment question
    ("E-INV-019", "Delivery charge disputed on an invoice: a billing point, invoice only [B-8 contrast]"),
    ("E-INV-028", "Scanned supplier invoice: stored with no reply [B-13]"),
    ("E-INV-030", "Supplier asks us to pay new bank details: escalated as possible fraud [B-13]"),
    # Customer account / onboarding
    ("E-ONB-009", "New account asking for 30-day terms: onboarding, flagged to Finance [B-10]"),
    ("E-ONB-018", "Account details in a forwarded chain: the forwarder's request counts [G-3]"),
    ("E-ONB-023", "New delivery address for the account: onboarding, not order [B-11]"),
    # Other / unclear / unrelated
    ("E-OTH-010", "Complaint about the courier's manner: service, not goods [B-7]"),
    ("E-OTH-018", "Only instructions aimed at the assistant: phishing [G-9]"),
    # Mixed
    ("E-MIX-CO-001", "Damaged and missing items in one delivery: complaint + order [B-6]"),
    ("E-MIX-TC-001", "Asks what to check, then asks for a replacement: technical + complaint [B-5]"),
    ("E-MIX-CI-001", "Payment withheld over torn gloves: invoice + complaint [B-8]"),
    ("E-MIX-NO-001", "Opens an account and places an order: onboarding + order, account applied first [B-9]"),
    ("E-MIX-DT-007", "Asks for the VM-10 note and a question it answers: documentation + technical, attached once [B-4]"),
    ("E-MIX-QO-001", "Quote and order status, with an injected instruction: no invoice label [G-9]"),
    ("E-MIX-IQ-003", "Resend of a mixed email: same two labels, linked to the first case [G-10]"),
    ("E-MIX-CIO-001", "Three categories: equipment fault, invoice copy, new order"),
]

ROUTE_WORDS = {"draft_for_approval": "draft for approval", "ask_for_clarification": "ask for clarification", "escalate": "escalate",
               "store_extraction": "store, no reply", "link_to_existing_case": "link to existing case"}


def load():
    out = {}
    for f in sorted(glob.glob(os.path.join(EMAILS, "*.jsonl"))):
        for line in open(f, encoding="utf-8"):
            e = json.loads(line); out[e["email_id"]] = (os.path.basename(f), e)
    return out


def main():
    allm = load()
    ids = [i for i, _ in PICKS]
    assert len(ids) == 30 and len(set(ids)) == 30, "need 30 distinct picks"
    for i in ids:
        assert i in allm, i
        assert allm[i][1]["split"] == "tune", f"{i} is held out"

    with open(os.path.join(ROOT, "data", "anchor_set.jsonl"), "w", encoding="utf-8") as h:
        for i in ids: h.write(json.dumps(allm[i][1], ensure_ascii=False) + "\n")

    labels = collections.Counter(l for i in ids for l in allm[i][1]["expected"]["labels"])
    routes = collections.Counter(allm[i][1]["expected"]["route"] for i in ids)
    multi = sum(len(allm[i][1]["expected"]["labels"]) > 1 for i in ids)

    md = ["# Anchor set", "",
          "Thirty test emails for you to read once (EVALUATION.md). Built by `tools/build_anchor_set.py`; the same emails, unchanged, are in `data/anchor_set.jsonl` (outside `data/emails/`, so they are not counted twice).", "",
          "**How to read it.** For each email, read the subject and body first, decide what labels and outcome you would expect, then compare with the expected answer. Tick **Agree**, or write what you would change in **Note**. A disagreement is a reason to fix the generator, SOP or classification guide, never the JSONL.", "",
          "**How the 30 were chosen.**",
          "- Only emails in the tuning split, so the held-out quarter stays unread while prompts are tuned.",
          "- Every category appears, each with at least one boundary case from `CLASSIFICATION_GUIDE.md`; the reason column names the rule.",
          f"- {multi} mixed-category emails, including one with three categories.",
          "- Every route, and the hard personas: formal, rushed, typo-ridden, urgent, another language, a forwarded chain, a prompt injection and a resend.", "",
          "| Label | Emails |", "| --- | --- |"]
    md += [f"| {k} | {v} |" for k, v in sorted(labels.items())]
    md += ["", "| Route | Emails |", "| --- | --- |"]
    md += [f"| {ROUTE_WORDS[k]} | {v} |" for k, v in sorted(routes.items(), key=lambda kv: -kv[1])]
    md += ["", "## Checklist", "", "| # | Email | Expected labels | Route | What it checks | Agree | Note |", "| --- | --- | --- | --- | --- | --- | --- |"]
    for n, (i, why) in enumerate(PICKS, 1):
        f, e = allm[i]; x = e["expected"]
        md.append(f"| {n} | [{i}](#{i.lower()}) | {'; '.join(x['labels'])} | {ROUTE_WORDS[x['route']]} | {why} | ☐ | |")
    md += ["", "## The emails", ""]
    for n, (i, why) in enumerate(PICKS, 1):
        f, e = allm[i]; x = e["expected"]
        md += [f"### {i}", "", f"{n}. From **{e['from_name']}** &lt;{e['from_email']}&gt; · {e['received_at']} · `{f}`", "",
               f"**Subject:** {e['subject'] or '(empty)'}", ""]
        body = e["body"].strip() or "(empty)"
        md += ["> " + l if l else ">" for l in body.split("\n")]
        if e.get("attachments"): md += ["", "**Attachments:** " + ", ".join(a if isinstance(a, str) else a.get("filename", str(a)) for a in e["attachments"])]
        md += ["", "<details><summary>Expected answer</summary>", "",
               f"- **Labels:** {'; '.join(x['labels'])}", f"- **Route:** {ROUTE_WORDS[x['route']]}"]
        if x.get("flags"): md.append(f"- **Flags:** {', '.join(x['flags'])}")
        if x.get("duplicate_of"): md.append(f"- **Duplicate of:** {x['duplicate_of']}")
        for p in x["parts"]:
            owner = f", owner {p['owner']}" if p.get("owner") else ""
            md.append(f"- **{p['label']}** ({ROUTE_WORDS[p['route']]}{owner})")
            for m in p.get("reply_must_state", []): md.append(f"  - {m}")
            if p.get("send_documents"): md.append(f"  - Attach: {', '.join(p['send_documents'])}")
        if e.get("notes"): md.append(f"- **Why:** {e['notes']}")
        md += [f"- **Checks:** {why}", "", "</details>", ""]
    with open(os.path.join(ROOT, "docs", "ANCHOR_SET.md"), "w", encoding="utf-8") as h:
        h.write("\n".join(md))
    print(len(ids), dict(routes), multi)


if __name__ == "__main__":
    main()
