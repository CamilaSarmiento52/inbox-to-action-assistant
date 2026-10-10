"""Generate the fictional order, order-line and shipment records (data/orders.csv, order_lines.csv, shipments.csv).

Orders are designed by hand below; prices and discounts are computed from catalogue.csv and discounts.csv.
Dates are fixed history, not delivery predictions. Delivered-history rows use the default state: dispatched on the order
date, delivered in one shipment. Rows with an explicit state supply their own dispatch, delivery and status values.
An order delivered in full has one shipment (the default). Orders still in progress list their shipments explicitly:
each shipment names the lines and quantities it carries (`lines` = "line:qty;line:qty"). A line has one lot or serial.
Run from the project root:  python3 tools/generate_orders.py
"""
import csv, os
from decimal import Decimal as D, ROUND_HALF_UP

DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
rd = lambda f: list(csv.DictReader(open(os.path.join(DATA, f), encoding="utf-8")))
CAT = {r["sku"]: r for r in rd("catalogue.csv")}
DISC = rd("discounts.csv")
CUST = {r["customer_id"]: r for r in rd("customers.csv")}
CONT = {r["name"]: r for r in rd("customer_contacts.csv")}

# order_id, contact name, order date, delivered date (None if not delivered in full), customer PO, [(sku, qty, lot or serial)], optional state
ORDERS = [
    # Kestrel's two overdue invoices come from these (customers.csv outstanding balance £1,842.60)
    ("SO-10310", "Stephen Maddox", "2026-07-13", "2026-07-15", "KET-0388", [("NLS-HB2-DBL", 1, "HB2D-26-0201"), ("NLS-SP10-P", 2, "SP-26-0610")]),
    ("SO-10322", "Stephen Maddox", "2026-08-03", "2026-08-05", "KET-0396", [("NLS-AB220-STD", 1, "AB2S-26-0377"), ("NLS-PT200-B", 20, "PT-26-0705")]),
    ("SO-10350", "Fraser Linklater", "2026-09-07", "2026-09-10", "OMA-0912", [("NLS-MT15-B", 6, "MT-26-0731")]),
    ("SO-10360", "Gwen Probert", "2026-09-14", "2026-09-15", "", [("NLS-SC60-P", 8, "SC-26-0802")]),
    ("SO-10370", "Euan MacRae", "2026-09-22", "2026-09-25", "DFA-221", [("NLS-CT50-P", 6, "CT-26-0815")]),
    ("SO-10380", "Lucy Penhale", "2026-09-17", "2026-09-24", "BD-7781", [("NLS-AB220-CRT", 1, "AB2C-26-0117")]),
    ("SO-10385", "Hugh Lanyon", "2026-09-17", "2026-09-21", "TMSC-0455", [("NLS-HB2-DBL", 1, "HB2D-26-0342")]),
    ("SO-10390", "Isla Drummond", "2026-09-21", "2026-09-22", "CU-ILS-3310", [("NLS-GL-NM", 12, "GL-26-0905")]),
    ("SO-10395", "Morag Sinclair", "2026-09-23", "2026-09-25", "TTC-118", [("NLS-SP10-P", 6, "SP-26-0820")]),
    ("SO-10398", "Sarah Fenwick", "2026-09-28", "2026-09-29", "", [("NLS-GL-NM", 20, "GL-26-0911")]),
    ("SO-10402", "Adebayo Adeyemi", "2026-09-25", "2026-09-28", "CVP-20931", [("NLS-PT200-B", 10, "PT-26-0822")]),
    ("SO-10408", "Ben Aldous", "2026-10-01", "2026-10-02", "MBA-077", [("NLS-MT15-B", 10, "MT-26-0901")]),
    ("SO-10411", "Ciaran Doherty", "2026-09-28", "2026-10-01", "LEAS-3302", [("NLS-AB220-STD", 1, "AB2S-26-0458")]),
    ("SO-10415", "Anita Verma", "2026-10-05", "2026-10-06", "TRI-55120", [("NLS-SC60-P", 5, "SC-26-0910")]),
    ("SO-10419", "Janet Oldroyd", "2026-09-30", "2026-10-01", "", [("NLS-VM10-BAS", 1, "VM1B-26-0731")]),
    ("SO-10420", "Claire Tilling", "2026-10-05", "2026-10-07", "", [("NLS-VM10-BAS", 1, "VM1B-26-0802")]),
    ("SO-10425", "Marcus Bellamy", "2026-10-06", "2026-10-08", "EU-CHEM-4410", [("NLS-MC12-PLS", 1, "MC12P-26-0388")]),
    ("SO-10426", "Euan MacRae", "2026-09-29", "2026-10-02", "DFA-229", [("NLS-VM10-VAR", 1, "VM1V-26-0219")]),
    ("SO-10428", "Callum Reid", "2026-10-06", "2026-10-08", "TRI-55187", [("NLS-HB2-SNG", 1, "HB2S-26-0577")]),
    ("SO-10430", "Priya Raman", "2026-10-06", "2026-10-08", "NU-BIO-9921", [("NLS-CT50-P", 4, "CT-26-0920"), ("NLS-SP10-P", 2, "SP-26-0905")]),
    ("SO-10431", "Hugh Lanyon", "2026-10-06", "2026-10-08", "TMSC-0471", [("NLS-SC60-P", 10, "SC-26-0915")]),
    ("SO-10432", "Tom Hargreaves", "2026-10-06", "2026-10-08", "NU-BIO-9925", [("NLS-PT200-B", 2, "PT-26-0910")]),
    ("SO-10433", "Katie Dunmore", "2026-10-07", "2026-10-08", "RML-4402", [("NLS-MT15-B", 5, "MT-26-0915")]),
    ("SO-10372", "Gareth Pugh", "2026-09-04", "2026-09-08", "", [("NLS-SC60-P", 4, "SC-26-0725")]),
    ("SO-10375", "Imran Qureshi", "2026-09-07", "2026-09-09", "RML-4310", [("NLS-GL-NM", 10, "GL-26-0820")]),
    ("SO-10386", "Isla Drummond", "2026-09-25", "2026-09-29", "CU-ILS-3318", [("NLS-HB2-SNG", 1, "HB2S-26-0561"), ("NLS-MT15-B", 4, "MT-26-0905")]),
    ("SO-10388", "Ruth Ellison", "2026-09-22", "2026-09-24", "EU-CHEM-4391", [("NLS-CT50-P", 8, "CT-26-0808")]),
    ("SO-10391", "Alasdair Menzies", "2026-09-23", "2026-09-25", "BDS-1182", [("NLS-SP10-P", 5, "SP-26-0815")]),
    ("SO-10417", "Lucy Penhale", "2026-10-02", "2026-10-05", "BD-7790", [("NLS-CT50-P", 6, "CT-26-0912")]),
    ("SO-10434", "Imran Qureshi", "2026-10-06", "2026-10-08", "RML-4398", [("NLS-GL-NM", 3, "GL-26-0918"), ("NLS-SP10-P", 4, "SP-26-0905")]),
    # ---- orders in progress, for order status (state as of 2026-10-09)
    ("SO-10440", "Katie Dunmore", "2026-10-07", None, "RML-4410", [("NLS-PT200-B", 4, "PT-26-0915")],
     dict(status="in_transit", shipments=[dict(lines=[(1, 4)], dispatched_on="2026-10-08", status="in_transit", estimated_delivery="2026-10-12", delivery_date_status="estimated")])),
    ("SO-10441", "Euan MacRae", "2026-10-06", None, "DFA-236", [("NLS-CT50-P", 10, "CT-26-0920")],
     dict(status="in_transit", shipments=[dict(lines=[(1, 10)], dispatched_on="2026-10-07", status="in_transit", estimated_delivery="2026-10-13", delivery_date_status="estimated")])),
    ("SO-10442", "Lucy Penhale", "2026-10-07", None, "BD-7795", [("NLS-AB220-CRT", 1, "")],
     dict(status="awaiting_dispatch", estimated_dispatch="2026-10-12", shipments=[])),
    ("SO-10443", "Ben Aldous", "2026-10-05", None, "MBA-081", [("NLS-MC12-STD", 1, "MC12S-26-1204"), ("NLS-SC60-P", 2, "SC-26-0915")],
     dict(status="delayed", shipments=[dict(lines=[(1, 1), (2, 2)], dispatched_on="2026-10-06", status="delayed", estimated_delivery="2026-10-07", delivery_date_status="estimated",
                                            revised_delivery="2026-10-13", delay_reason="Carrier delay at the regional depot")])),
    ("SO-10444", "Marcus Bellamy", "2026-10-05", None, "EU-CHEM-4415", [("NLS-HB2-DBL", 1, "HB2D-26-0350")],
     dict(status="delayed", shipments=[dict(lines=[(1, 1)], dispatched_on="2026-10-06", status="delayed", estimated_delivery="2026-10-07", delivery_date_status="estimated",
                                            delay_reason="Parcel held at the carrier's depot; no new date yet")])),
    ("SO-10445", "Isla Drummond", "2026-10-05", None, "CU-ILS-3324", [("NLS-SP10-P", 6, "SP-26-0905"), ("NLS-VM10-VAR", 1, "")],
     dict(status="partially_shipped", shipments=[dict(lines=[(1, 6)], dispatched_on="2026-10-06", status="delivered", estimated_delivery="2026-10-07", delivery_date_status="confirmed", delivered_on="2026-10-07")])),
    ("SO-10446", "Priya Raman", "2026-10-02", "2026-10-06", "NU-BIO-9930", [("NLS-MT15-C", 1, "MT-26-0901")]),
    ("SO-10447", "Fiona Gallagher", "2026-10-08", None, "CVP-20977", [("NLS-SC60-P", 6, "SC-26-0915"), ("NLS-GL-NM", 10, "GL-26-0918")],
     dict(status="in_transit", shipments=[dict(lines=[(1, 6), (2, 10)], dispatched_on="2026-10-09", status="in_transit", estimated_delivery="2026-10-12", delivery_date_status="confirmed")])),
    ("SO-10448", "Anita Verma", "2026-10-06", "2026-10-07", "TRI-55190", [("NLS-PT200-C", 1, "PT-26-0910")]),
    ("SO-10449", "Sarah Fenwick", "2026-10-09", None, "", [("NLS-GL-NM", 10, "GL-26-0918")],
     dict(status="awaiting_dispatch", estimated_dispatch="2026-10-09", shipments=[])),
    ("SO-10450", "Tom Hargreaves", "2026-10-07", None, "NU-BIO-9934", [("NLS-CT50-P", 5, "CT-26-0920")],
     dict(status="in_transit", shipments=[dict(lines=[(1, 5)], dispatched_on="2026-10-08", status="in_transit", estimated_delivery="2026-10-12", delivery_date_status="estimated")])),
    ("SO-10451", "Alasdair Menzies", "2026-10-07", None, "BDS-1190", [("NLS-PT200-B", 6, "PT-26-0915")],
     dict(status="in_transit", shipments=[dict(lines=[(1, 6)], dispatched_on="2026-10-08", status="in_transit", estimated_delivery="2026-10-12", delivery_date_status="estimated")])),
    ("SO-10452", "Hugh Lanyon", "2026-10-08", None, "TMSC-0480", [("NLS-VM10-VAR", 1, "")],
     dict(status="awaiting_dispatch", estimated_dispatch="2026-10-12", shipments=[])),
    ("SO-10453", "Morag Sinclair", "2026-10-07", None, "TTC-124", [("NLS-MT15-B", 8, "MT-26-0915")],
     dict(status="in_transit", shipments=[dict(lines=[(1, 8)], dispatched_on="2026-10-08", status="in_transit", estimated_delivery="2026-10-12", delivery_date_status="estimated")])),
    ("SO-10455", "Hugh Lanyon", "2026-10-06", "2026-10-08", "TMSC-0478", [("NLS-GL-NM", 6, "GL-26-0918"), ("NLS-SC60-P", 4, "SC-26-0915")]),
    # delivered in two shipments, so it has two invoices
    ("SO-10405", "Priya Raman", "2026-09-28", None, "NU-BIO-9915", [("NLS-PT200-B", 10, "PT-26-0822"), ("NLS-VM10-BAS", 1, "VM1B-26-0745")],
     dict(status="delivered", shipments=[dict(lines=[(1, 10)], dispatched_on="2026-09-28", status="delivered", estimated_delivery="2026-09-29", delivery_date_status="confirmed", delivered_on="2026-09-29"),
                                          dict(lines=[(2, 1)], dispatched_on="2026-09-30", status="delivered", estimated_delivery="2026-10-01", delivery_date_status="confirmed", delivered_on="2026-10-01")])),
    ("SO-10456", "Fraser Linklater", "2026-09-30", "2026-10-02", "OMA-0931", [("NLS-MT15-B", 4, "MT-26-0905"), ("NLS-CT50-P", 2, "CT-26-0920")]),
    ("SO-10454", "Ciaran Doherty", "2026-10-08", None, "LEAS-3311", [("NLS-HB2-SNG", 1, "")],
     dict(status="awaiting_dispatch", estimated_dispatch="2026-10-12", shipments=[])),
]


def discount_pct(sku, qty):
    for r in DISC:
        if r["category"] == CAT[sku]["category"] and qty >= int(r["min_units"]) and (not r["max_units"] or qty <= int(r["max_units"])):
            return D(r["discount_percent"]) if r["action"] == "apply_discount" else D(0)
    return D(0)


orders, lines, ships = [], [], []
for oid, contact, od, dd, po, items, *state in ORDERS:
    st = state[0] if state else dict(status="delivered", shipments=[dict(lines=[(n, q) for n, (_, q, _) in enumerate(items, 1)], dispatched_on=od,
                                                                            status="delivered", estimated_delivery=dd, delivery_date_status="confirmed", delivered_on=dd)])
    c = CONT[contact]; cust = CUST[c["customer_id"]]
    orders.append({"order_id": oid, "customer_id": cust["customer_id"], "placed_by_contact_id": c["contact_id"], "order_date": od,
                   "customer_po": po, "delivery_postcode": cust["postcode"], "status": st["status"], "estimated_dispatch": st.get("estimated_dispatch", "")})
    shipped = {}
    for sh in st["shipments"]:
        for n, q in sh["lines"]: shipped[n] = shipped.get(n, 0) + q
    for n, (sku, qty, ident) in enumerate(items, 1):
        price = D(CAT[sku]["price_gbp_ex_vat"]); pct = discount_pct(sku, qty)
        disc = (price * qty * pct / 100).quantize(D("0.01"), rounding=ROUND_HALF_UP)  # same convention as quotation SOP §3
        net = price * qty - disc
        equip = CAT[sku]["category"] == "Equipment"
        q = shipped.get(n, 0)
        lines.append({"order_id": oid, "line_no": n, "sku": sku, "quantity": qty, "unit_price_gbp_ex_vat": f"{price:.2f}",
                      "discount_percent": f"{pct:.0f}", "net_total_gbp_ex_vat": f"{net:.2f}",
                      "lot_number": "" if equip else ident, "serial_number": ident if equip else "",
                      "quantity_shipped": q, "line_status": "shipped" if q == qty else ("partially_shipped" if q else "pending")})
    for k, sh in enumerate(st["shipments"], 1):  # IDs derive from the order, so adding orders never renumbers them
        ships.append({"shipment_id": f"SH-{oid[3:]}-{k}", "order_id": oid, "lines": ";".join(f"{n}:{q}" for n, q in sh["lines"]),
                      "dispatched_on": sh["dispatched_on"], "status": sh["status"], "estimated_delivery": sh["estimated_delivery"],
                      "delivery_date_status": sh["delivery_date_status"], "revised_delivery": sh.get("revised_delivery", ""),
                      "delay_reason": sh.get("delay_reason", ""), "delivered_on": sh.get("delivered_on", "")})

for name, rows in (("orders.csv", orders), ("order_lines.csv", lines), ("shipments.csv", ships)):
    with open(os.path.join(DATA, name), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print(len(orders), "orders,", len(lines), "lines,", len(ships), "shipments")
