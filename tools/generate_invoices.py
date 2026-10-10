"""Generate the fictional customer invoices: data/invoices.csv, data/invoice_lines.csv and data/invoices/<id>.md/.pdf.

One invoice per dispatched shipment, dated the dispatch day; the order's delivery charge goes on its first invoice and
is judged on the whole order's goods total (terms of sale §3.3). Status as of 2026-10-09: prepay invoices are paid;
Kestrel's two summer invoices are overdue and add up to its outstanding balance in customers.csv; other invoices past
their due date are paid and the rest unpaid. Run from the project root after tools/generate_orders.py:
    python3 tools/generate_invoices.py
"""
import csv, os, re, datetime as dt
from decimal import Decimal as D, ROUND_HALF_UP
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from xml.sax.saxutils import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
rd = lambda f: list(csv.DictReader(open(os.path.join(DATA, f), encoding="utf-8")))
ORD = {r["order_id"]: r for r in rd("orders.csv")}
LINES = rd("order_lines.csv"); SHIPS = rd("shipments.csv")
CUST = {r["customer_id"]: r for r in rd("customers.csv")}
CAT = {r["sku"]: r for r in rd("catalogue.csv")}
DELIV = {r["zone"]: r for r in rd("delivery_charges.csv")}
ZONES = rd("delivery_zones.csv")


def zone_of(pc):
    """Zone of the order's recorded destination (outward code only), as in the quotation generator."""
    m = re.fullmatch(r"([A-Z]{1,2})(\d+)[A-Z]?", pc.replace(" ", "").upper()[:-3])
    area, dist = m.group(1), int(m.group(2))
    return next(z["zone"] for z in ZONES if z["postcode_area"] == area and (not z["district_from"] or int(z["district_from"]) <= dist <= int(z["district_to"])))
TODAY = dt.date(2026, 10, 9)
OVERDUE = {"SO-10310", "SO-10322"}
q2 = lambda x: x.quantize(D("0.01"), rounding=ROUND_HALF_UP)
DISCLAIMER = "Fictional invoice for Northfield Lab Supply, a fictional company created for a portfolio project. Not a real invoice."

invoices, inv_lines = [], []
dispatched = sorted((s for s in SHIPS if s["status"] in ("in_transit", "delayed", "delivered")), key=lambda s: (s["dispatched_on"], s["shipment_id"]))
seen_orders, count = set(), {}
for sh in dispatched:
    oid = sh["order_id"]; o = ORD[oid]; cust = CUST[o["customer_id"]]
    olines = {l["line_no"]: l for l in LINES if l["order_id"] == oid}
    carried = []
    for x in sh["lines"].split(";"):
        ln, qty = x.split(":"); l = olines[ln]
        if int(qty) != int(l["quantity"]):  # a split line: invoice only what this shipment carries
            raise NotImplementedError(f"{oid} line {ln}: split-line invoicing needs an allocation rule for the discount first")
        carried.append(l)
    goods = sum(D(l["net_total_gbp_ex_vat"]) for l in carried)
    delivery = D(0)
    if oid not in seen_orders:  # first invoice of the order carries the delivery charge
        order_goods = sum(D(l["net_total_gbp_ex_vat"]) for l in olines.values())
        z = DELIV[zone_of(o["delivery_postcode"])]  # the order's destination, not the account's zone
        delivery = D(0) if order_goods >= D(z["free_delivery_from_gbp_ex_vat"]) else D(z["charge_gbp_ex_vat"])
        seen_orders.add(oid)
    vat = q2((goods + delivery) * D("0.20"))
    inv_date = dt.date.fromisoformat(sh["dispatched_on"])
    prepay = cust["payment_terms"] == "prepay"
    due = inv_date if prepay else inv_date + dt.timedelta(days=30)
    if prepay: status, paid_on = "paid", inv_date.isoformat()
    elif oid in OVERDUE: status, paid_on = "overdue", ""
    elif due < TODAY: status, paid_on = "paid", (due - dt.timedelta(days=3)).isoformat()
    else: status, paid_on = "unpaid", ""
    count[oid] = count.get(oid, 0) + 1
    iid = f"INV-{oid[3:]}-{count[oid]}"  # derived from the order, so adding orders never renumbers invoices
    invoices.append({"invoice_id": iid, "order_id": oid, "shipment_id": sh["shipment_id"], "customer_id": cust["customer_id"],
                     "invoice_date": inv_date.isoformat(), "due_date": due.isoformat(), "goods_net_gbp": f"{goods:.2f}",
                     "delivery_gbp": f"{delivery:.2f}", "vat_gbp": f"{vat:.2f}", "total_gbp": f"{goods + delivery + vat:.2f}",
                     "status": status, "paid_on": paid_on, "file_path_md": f"invoices/{iid}.md", "file_path_pdf": f"invoices/{iid}.pdf"})
    for l in carried:
        inv_lines.append({"invoice_id": iid, "order_id": oid, "line_no": l["line_no"], "sku": l["sku"], "quantity": l["quantity"],
                          "unit_price_gbp_ex_vat": l["unit_price_gbp_ex_vat"], "discount_percent": l["discount_percent"],
                          "net_total_gbp_ex_vat": l["net_total_gbp_ex_vat"]})

# the balance in customers.csv must equal the sum of overdue invoices
for cid, c in CUST.items():
    owed = sum(D(i["total_gbp"]) for i in invoices if i["customer_id"] == cid and i["status"] == "overdue")
    assert owed == D(c["outstanding_balance_gbp"]), (cid, owed, c["outstanding_balance_gbp"])


def render(inv):
    cust = CUST[inv["customer_id"]]; o = ORD[inv["order_id"]]
    rows = [l for l in inv_lines if l["invoice_id"] == inv["invoice_id"]]
    head = [["Invoice number", inv["invoice_id"]], ["Invoice date", inv["invoice_date"]], ["Due date", inv["due_date"]],
            ["Customer", f"{cust['company_name']} ({cust['customer_id']})"], ["Invoice address", cust["invoice_address"]],
            ["Order", inv["order_id"]], ["Your reference", o["customer_po"] or "-"], ["Payment terms", cust["payment_terms"]]]
    body = [[CAT[l["sku"]]["product_name"] + ", " + CAT[l["sku"]]["version"], l["quantity"], l["unit_price_gbp_ex_vat"], l["discount_percent"] + "%", l["net_total_gbp_ex_vat"]] for l in rows]
    totals = [["Goods (ex VAT)", inv["goods_net_gbp"]], ["Delivery (ex VAT)", inv["delivery_gbp"]], ["VAT 20%", inv["vat_gbp"]], ["Total (GBP)", inv["total_gbp"]]]
    md = [f"# Invoice {inv['invoice_id']}", "", f"> {DISCLAIMER}", "", "Northfield Lab Supply (fictional)", "", "| | |", "| --- | --- |"] + [f"| {a} | {b} |" for a, b in head]
    md += ["", "| Product | Quantity | Unit price (GBP ex VAT) | Discount | Net (GBP) |", "| --- | --- | --- | --- | --- |"] + ["| " + " | ".join(map(str, r)) + " |" for r in body]
    md += ["", "| | |", "| --- | --- |"] + [f"| {a} | {b} |" for a, b in totals]
    open(os.path.join(DATA, inv["file_path_md"]), "w", encoding="utf-8").write("\n".join(md) + "\n")
    ss = getSampleStyleSheet(); P = lambda t, st=ss["BodyText"]: Paragraph(escape(str(t)), st)
    def tbl(data, widths):
        t = Table([[P(c) for c in r] for r in data], colWidths=widths)
        t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
        return t
    w = A4[0] - 4 * cm
    story = [P(f"Invoice {inv['invoice_id']}", ss["Title"]), P(DISCLAIMER, ParagraphStyle("n", fontSize=8, textColor=colors.grey)), Spacer(1, 6),
             tbl(head, [w * .35, w * .65]), Spacer(1, 8),
             tbl([["Product", "Qty", "Unit price", "Discount", "Net"]] + body, [w * .44, w * .1, w * .16, w * .14, w * .16]), Spacer(1, 8),
             tbl(totals, [w * .6, w * .4])]
    SimpleDocTemplate(os.path.join(DATA, inv["file_path_pdf"]), pagesize=A4, title=f"Invoice {inv['invoice_id']}",
                      leftMargin=2 * cm, rightMargin=2 * cm, topMargin=2 * cm, bottomMargin=2 * cm).build(story)


os.makedirs(os.path.join(DATA, "invoices"), exist_ok=True)
for inv in invoices: render(inv)
for name, rows in (("invoices.csv", invoices), ("invoice_lines.csv", inv_lines)):
    with open(os.path.join(DATA, name), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print(len(invoices), "invoices,", len(inv_lines), "lines;", sum(i["status"] == "overdue" for i in invoices), "overdue")
