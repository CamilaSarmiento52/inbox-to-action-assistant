"""Generate the fictional product documents (Markdown and PDF) from data/product_documents.csv.

Run from the project root:  python3 tools/generate_documents.py
Updates the `pages` column of the index with the page count of each PDF.
"""
import csv, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from doc_content import *
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, ListFlowable, ListItem
from xml.sax.saxutils import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
DISCLAIMER = "Fictional document for Northfield Lab Supply, a fictional company created for a portfolio project. Not for real use."

# ------------------------------------------------------------------ builders
def manual_blocks(p, extra=None):
    b = [("h2", "1. Introduction"), ("p", p["intro"])]
    if p.get("versions"):
        b += [("p", "Differences between the versions:"), ("table", p["versions"][0], p["versions"][1])]
    b += [("h2", "2. Safety"), ("ul", p["safety"]), ("h2", "3. Setting up"), ("ol", p["setup"]), ("h2", "4. Operation"), ("ol", p["operation"]),
          ("h2", "5. Cleaning and maintenance"), ("ul", p["maintenance"]), ("h2", "6. Troubleshooting"),
          ("table", ["Problem", "Likely cause", "What to do"], p["trouble"]),
          ("h2", "7. Warranty and contact"), ("p", f"Warranty: {p['warranty']}"), ("p", WARRANTY_NOTE), ("p", f"Contact: {CONTACT}")]
    return b

AB_MANUAL = lambda v: dict(
    name=AB220["name"], intro=AB220["intro"], versions=AB220["versions"],
    safety=["Use only the mains adaptor supplied. Do not use the balance with a damaged adaptor or cable.",
            f"Operate only within {v['temp']} and 20 to 80 % humidity, non-condensing.",
            "Do not exceed the 220 g capacity; overloading can damage the sensor.", "Keep liquids away from the pan and the casing.", "Disconnect the adaptor before cleaning."],
    setup=["Remove the packaging and check the contents against the packing list.", "Place the balance on a firm, level bench away from draughts and vibration.",
           "Level the balance using the feet until the level indicator is centred.", "Fit the pan and the draft shield, then connect the adaptor (UK plug).",
           f"Leave the balance powered for {v['warm']} minutes before use."],
    operation=["Close the draft shield doors and press Zero.", "Place the sample or container on the centre of the pan, then close the doors.",
               "Wait for the stability indicator and read the value.", f"To calibrate: after warm-up, hold the calibration key and place the {v['cal_weight']} test weight (not supplied) when prompted.",
               "Remove the sample and press Zero before the next weighing."],
    maintenance=["Wipe the pan and shield with a lint-free cloth and a mild detergent; dry before use.", "Clean spills immediately. Do not use solvents on the casing.",
                 "Recalibrate after moving the balance or after a large temperature change."],
    trouble=[["Unstable reading", "Draughts or vibration", "Close the doors, move away from air outlets and check the bench"],
             ["Reading drifts", "Warm-up too short, or temperature difference with the sample", f"Allow {v['warm']} minutes warm-up; let the sample reach room temperature"],
             ["Overload shown", "Weight above 220 g", "Remove the load"], ["Does not switch on", "Adaptor not connected", "Check the adaptor and socket"]],
    warranty="Standard: 1 year. Certified: 2 years.")
HB_MANUAL = dict(name=HB2["name"], intro=HB2["intro"], versions=HB2["versions"],
    safety=["The blocks reach 150 °C. Do not touch a hot block; use the block handle or wait until it is cool.", "Do not heat flammable liquids.",
            "Use only the blocks supplied with the unit, and do not use damaged blocks.", "Place on a heat-resistant surface with clear space around the unit.", "Switch off and unplug before changing blocks."],
    setup=["Check the contents against the packing list.", "Place the heater on a level, heat-resistant surface.", "Fit the block(s) into the unit; no tools are needed.", "Connect the mains cable (230 V AC, 50 Hz)."],
    operation=["Switch on and set the temperature (Dual block: set each block separately).", "Wait until the display shows the set temperature and allow about 10 minutes to stabilise.",
               "Place the tubes in the block wells so they touch the bottom.", "Set the timer if required and start the run.", "Switch off and let the block cool before removing or cleaning."],
    maintenance=["Wipe the unit with a damp cloth when cool.", "Clean the block wells with a swab and 70 % ethanol.", "Do not immerse the unit in liquid."],
    trouble=[["Display shows an error", "Over-temperature cut-out", "Switch off, let the unit cool and restart"], ["Temperature not reached", "Block not seated", "Reseat the block"],
             ["Does not switch on", "Mains cable not connected", "Check the cable and socket"]],
    warranty="Single block: 1 year. Dual block: 2 years.")
VM_MANUAL = dict(name=VM10["name"], intro=VM10["intro"], versions=VM10["versions"],
    safety=["Place the mixer on a level, non-slip surface.", "Hold tubes firmly and do not overfill them.", "Do not mix flammable or hazardous liquids unless you have assessed the risk.", "Unplug before cleaning."],
    setup=["Check the contents against the packing list.", "Place the mixer on a level surface and fit the cup head.", "Connect the mains cable (230 V AC, 50 Hz)."],
    operation=["Basic: switch on for continuous mixing at 2,800 rpm. Variable speed: set the speed with the dial (200 to 3,000 rpm).",
               "Press the tube lightly into the cup head. In touch mode (Variable speed only) the mixer runs while the tube presses the head.",
               "Mix for the time needed, then lift the tube away. Switch off when finished.", "Do not run for more than 30 minutes continuously; rest for 10 minutes."],
    maintenance=["Wipe the head and casing with a damp cloth and mild detergent.", "Do not immerse in liquid."],
    trouble=[["Does not start", "Mains cable not connected", "Check the cable and socket"], ["Tube does not mix well", "Speed too low or tube overfilled", "Increase the speed or reduce the volume"]],
    warranty="Basic: 1 year. Variable speed: 2 years.")

def spec_blocks(title, rows, version):
    return [("h2", f"Specification: {version}"), ("table", ["Item", "Value"], rows)]

def tech_blocks(sections):
    b = []
    for h, items in sections:
        b.append(("h2", h))
        for it in items:
            b.append(("p", it) if isinstance(it, str) else (it[0], it[1]))
    return b

def datasheet_blocks(c, extra=None):
    b = [("h2", "Product data"), ("table", ["Item", "Value"], c["rows"])]
    if extra: b += extra
    b += [("p", f"Contact: {CONTACT}")]
    return b

def coa_blocks(c):
    return [("h2", "Typical lot results"), ("p", "These are typical results for a representative lot, supplied for information. They are not a guarantee for any particular lot."),
            ("table", ["Test", "Result"], c["coa"])]

def ab_cert():
    return [("h2", "SAMPLE - not valid for any unit"), ("p", "This is a sample of the certificate supplied with the AB-220 Certified. Each unit's own certificate is issued with that unit and carries its serial number."),
            ("table", ["Item", "Value"], [["Certificate number", "SAMPLE-0000"], ["Instrument", "Analytical Balance AB-220 Certified"], ["Serial number", "SAMPLE"],
                                          ["Date of calibration", "SAMPLE"], ["Conditions", "21 °C, 45 % humidity"]]),
            ("h2", "Results"), ("table", ["Test weight (g)", "Reading (g)", "Error (mg)", "Uncertainty (mg)"],
                                [["10.0000", "10.0001", "+0.1", "0.2"], ["50.0000", "49.9999", "-0.1", "0.2"], ["100.0000", "100.0001", "+0.1", "0.2"], ["200.0000", "200.0000", "0.0", "0.3"]]),
            ("p", "Readings are traceable to national standards through the test weights used. The certificate does not replace calibration checks by the user.")]

GL_DOC = [("h2", "Declaration"), ("p", "Northfield Lab Supply declares that the nitrile examination gloves, powder-free, size medium (SKU NLS-GL-NM), conform to the standards listed below."),
          ("table", ["Standard", "Subject"], [["EN 455-1", "Freedom from holes"], ["EN 455-2", "Physical properties"], ["EN 455-3", "Biological evaluation"], ["EN ISO 374-1", "Protection against chemicals and micro-organisms: terminology and performance requirements"]]),
          ("p", "The gloves are for laboratory use and are not personal protective equipment for hazardous chemicals unless the datasheet states so."), ("p", f"Issued by Northfield Lab Supply, {CONTACT}.")]
GL_SDS = [("h2", "1. Identification"), ("p", "Product: nitrile examination gloves, powder-free (SKU NLS-GL-NM). Supplier: Northfield Lab Supply."),
          ("h2", "2. Hazards"), ("p", "The product is an article and is not classified as hazardous. Some people may react to nitrile; stop use if irritation occurs."),
          ("h2", "3. Composition"), ("p", "Nitrile rubber. Contains no natural rubber latex and no powder."),
          ("h2", "4. First aid"), ("p", "Skin irritation: remove the gloves, wash the skin and seek medical advice if it persists."),
          ("h2", "5. Handling and storage"), ("p", "Store cool and dry, away from direct sunlight and ozone sources."),
          ("h2", "6. Disposal"), ("p", "Dispose of as general waste, or as clinical waste if contaminated, following local rules.")]

# ------------------------------------------------------------------ doc table
def blocks_for(doc):
    d = doc["doc_id"]; t = d.split("-")
    key = d.replace("NLS-DOC-", "")
    if key == "MC12-MAN-R1": return manual_blocks(MC12)
    if key == "MC12-SPEC-STD-R1": return spec_blocks("", MC12_SPEC["Standard"], "Standard")
    if key == "MC12-SPEC-PLS-R1": return spec_blocks("", MC12_SPEC["Plus"], "Plus")
    if key == "MC12-TECH-R1": return tech_blocks(MC12_TECH)
    if key == "MC10-MAN-R1": return manual_blocks(MC10)
    if key == "AB220-MAN-R3": return manual_blocks(AB_MANUAL(AB220_R3))
    if key == "AB220-MAN-R2": return manual_blocks(AB_MANUAL(AB220_R2))
    if key == "AB220-SPEC-STD-R1": return spec_blocks("", AB220_SPEC["Standard"], "Standard")
    if key == "AB220-SPEC-CRT-R1": return spec_blocks("", AB220_SPEC["Certified"], "Certified")
    if key == "AB220-TECH-R1": return tech_blocks(AB220_TECH)
    if key == "AB220-CERT-SAMPLE-R1": return ab_cert()
    if key == "HB2-MAN-R1": return manual_blocks(HB_MANUAL)
    if key == "HB2-SPEC-SNG-R1": return spec_blocks("", HB2_SPEC["Single block"], "Single block")
    if key == "HB2-SPEC-DBL-R1": return spec_blocks("", HB2_SPEC["Dual block"], "Dual block")
    if key == "HB2-TECH-R1": return tech_blocks(HB2_TECH)
    if key == "VM10-MAN-R1": return manual_blocks(VM_MANUAL)
    if key == "VM10-SPEC-BAS-R1": return spec_blocks("", VM10_SPEC["Basic"], "Basic")
    if key == "VM10-TECH-R1": return tech_blocks(VM10_TECH)
    if key == "PT200-TECH-R1": return tech_blocks(PT_TECH)
    if key == "CT50-TECH-R1": return tech_blocks(CT_TECH)
    if key == "GL-DOC-R1": return GL_DOC
    if key == "GL-SDS-R1": return GL_SDS
    prod = t[2]  # e.g. PT200
    if key.endswith("-DS-R1"): return datasheet_blocks(CONS[prod])
    if key.endswith("-COA-R1"): return coa_blocks(CONS[prod])
    raise KeyError(key)

# ------------------------------------------------------------------ renderers
def md_text(doc, blocks):
    L = [f"# {doc['title']}", "", f"> {DISCLAIMER}", ""]
    if doc["status"] == "superseded":
        L += [f"> **SUPERSEDED.** Replaced by {doc['superseded_by']}. Not to be used as current.", ""]
    L += ["| | |", "| --- | --- |", f"| Document ID | {doc['doc_id']} |", f"| Product | {doc['product_name']} |",
          f"| Applies to | {doc['applies_to_skus'].replace(';', ', ')} |", f"| Revision | {doc['revision']} |",
          f"| Effective date | {doc['effective_date']} |", f"| Status | {doc['status']} |", ""]
    for b in blocks:
        k = b[0]
        if k == "h2": L += [f"## {b[1]}", ""]
        elif k == "p": L += [b[1], ""]
        elif k == "ul": L += [f"- {x}" for x in b[1]] + [""]
        elif k == "ol": L += [f"{i}. {x}" for i, x in enumerate(b[1], 1)] + [""]
        elif k == "table":
            L += ["| " + " | ".join(b[1]) + " |", "| " + " | ".join("---" for _ in b[1]) + " |"] + ["| " + " | ".join(r) + " |" for r in b[2]] + [""]
    return "\n".join(L).rstrip() + "\n"

def pdf_file(doc, blocks, path):
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["BodyText"], fontSize=9.5, leading=13)
    cell = ParagraphStyle("c", parent=body, fontSize=8.5, leading=11)
    h1 = ParagraphStyle("h1", parent=ss["Title"], fontSize=17, leading=21, alignment=0)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontSize=12, spaceBefore=10, spaceAfter=4)
    note = ParagraphStyle("n", parent=body, fontSize=8, textColor=colors.HexColor("#555555"))
    banner = ParagraphStyle("bn", parent=body, textColor=colors.HexColor("#8a1c1c"), fontName="Helvetica-Bold")
    P = lambda s, st=body: Paragraph(escape(s), st)
    def table(rows, header):
        data = [[P(c, ParagraphStyle("th", parent=cell, fontName="Helvetica-Bold")) for c in header]] + [[P(c, cell) for c in r] for r in rows]
        n = len(header); w = (A4[0] - 4 * cm)
        widths = [w * 0.34, w * 0.66] if n == 2 else [w / n] * n
        t = Table(data, colWidths=widths, repeatRows=1)
        t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8eef7")), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
        return t
    story = [P(doc["title"], h1), P(DISCLAIMER, note), Spacer(1, 6)]
    if doc["status"] == "superseded":
        story += [P(f"SUPERSEDED. Replaced by {doc['superseded_by']}. Not to be used as current.", banner), Spacer(1, 6)]
    story += [table([["Document ID", doc["doc_id"]], ["Product", doc["product_name"]], ["Applies to", doc["applies_to_skus"].replace(";", ", ")],
                     ["Revision", doc["revision"]], ["Effective date", doc["effective_date"]], ["Status", doc["status"]]], ["Item", "Value"])]
    for b in blocks:
        k = b[0]
        if k == "h2": story.append(P(b[1], h2))
        elif k == "p": story += [P(b[1]), Spacer(1, 4)]
        elif k in ("ul", "ol"):
            story.append(ListFlowable([ListItem(P(x), leftIndent=14) for x in b[1]], bulletType="bullet" if k == "ul" else "1", leftIndent=14))
        elif k == "table": story += [table(b[2], b[1]), Spacer(1, 6)]
    foot = lambda c, d: (c.saveState(), c.setFont("Helvetica", 7.5), c.drawString(2 * cm, 1.2 * cm, f"{doc['doc_id']}  |  Fictional document - Northfield Lab Supply"), c.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"Page {d.page}"), c.restoreState())
    t = SimpleDocTemplate(path, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=2 * cm, bottomMargin=2 * cm, title=doc["title"], author="Northfield Lab Supply (fictional)")
    t.build(story, onFirstPage=foot, onLaterPages=foot)
    return t.page

def main():
    idx = os.path.join(DATA, "product_documents.csv")
    rows = list(csv.DictReader(open(idx, newline="", encoding="utf-8")))
    os.makedirs(os.path.join(DATA, "documents"), exist_ok=True)
    for r in rows:
        bl = blocks_for(r)
        md = md_text(r, bl)
        md.encode("cp1252")  # PDF base fonts: fail loudly on unsupported characters
        open(os.path.join(DATA, r["file_path_md"]), "w", encoding="utf-8").write(md)
        r["pages"] = str(pdf_file(r, bl, os.path.join(DATA, r["file_path_pdf"])))
    with open(idx, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print(len(rows), "documents generated")

if __name__ == "__main__":
    main()
