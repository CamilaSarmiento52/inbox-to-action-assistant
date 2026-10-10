# Data

All data is fictional (Northfield Lab Supply). Prices are invented for the project.

The master list of deliberately planted traps and gaps, with the expected behaviour for each, is [`docs/TEST_TRAPS.md`](../docs/TEST_TRAPS.md). The sections below describe the data; the test cases they mention are listed there with stable IDs.

## catalogue.csv

One row per product and version (one SKU per row). The source of truth for prices; the catalogue vector index is built from the text columns and never supplies prices.

| Column | Meaning |
| --- | --- |
| `sku` | Unique ID, `NLS-<product>-<variant>` |
| `product_name` | Name shared by all versions of a product |
| `version` | Pack size, size or model version that distinguishes SKUs of one product |
| `category` | `Consumables` or `Equipment` |
| `description` | Plain-language description, used for search |
| `inclusions` | What the unit includes, separated by `;` |
| `unit_of_sale` | `each`, `box`, `bag`, `pack` or `case` |
| `units_per_pack` | Items in one unit of sale |
| `price_gbp_ex_vat` | Price per unit of sale in GBP, excluding VAT, decimal with no symbol |
| `stocked` | `yes` or `no` (`no` = made to order, lead time per delivery policy) |
| `status` | `current` or `superseded` |
| `effective_from` | Date the row took effect |
| `replaced_by_sku` | For superseded rows, the SKU that replaces it |
| `aliases` | Informal names customers use for the SKU, separated by `;`. Used to resolve names before fuzzy and semantic matching; typos are handled by fuzzy matching, not listed here. Version words ("standard", "plus", "dual") are only meaningful once the product is resolved |

## Contents (17 rows, 11 products)

- 8 consumable SKUs across 6 products. Pipette tips and microcentrifuge tubes come in two pack sizes. Gloves are medium only, so other sizes are deliberately not offered.
- 8 equipment SKUs across 4 products, each in two versions with different inclusions and prices.
- 1 superseded SKU (MC-10 Basic), replaced by the MC-12 Standard.

## Intended test uses

- Version ambiguity: the equipment products and the pipette tip and microtube pack sizes.
- Informal names and typos: similar names such as `Microcentrifuge Tubes 1.5 ml` and `Conical Centrifuge Tubes 50 ml`.
- Superseded trap: a request for the MC-10 must not be quoted at the old price as if current.
- Made-to-order: `NLS-AB220-CRT` is not stocked.
- Not in catalogue, on purpose: gloves in sizes other than medium, and any product not listed.

## document_type_synonyms.csv

Maps the words customers use for a document to the document types in `product_documents.csv`.

| Column | Meaning |
| --- | --- |
| `phrase` | Lowercase word or phrase as customers write it |
| `maps_to` | One document type; several joined with a vertical bar where the product decides (equipment gets `spec_sheet`, consumables get `datasheet`); `all` for "every current, shareable document"; `none` for documents we do not produce; `reroute` for phrases that are not a product-document request (the note says where they go) |
| `note` | How to handle it |

Phrases that map to several types, such as "certificate" or "technical documentation", need the product to decide or a clarification. Phrases that map to `none` (IQ/OQ, CE certificate, brochure) are treated as missing documents. Phrases that map to `reroute` (`catalogue`, `price list`) are not missing documents: they follow the note, for example a price list goes to the quotation SOP.

## discounts.csv

Quantity discounts by category. Quantities count units of sale of the same SKU on one line; mixed baskets do not combine.

| Column | Meaning |
| --- | --- |
| `rule_id` | D1 to D4 |
| `category` | Matches `catalogue.csv` category |
| `min_units`, `max_units` | Quantity range; blank max means no upper limit |
| `discount_percent` | Percentage off the line total; blank when not automatic |
| `action` | `apply_discount` or `refer_to_sales` |

Rules: one discount per line; no stacking; superseded SKUs are never discounted. A quantity below every rule's minimum (consumables under 10, a single equipment unit) simply gets no discount. A person decides only when a rule says `refer_to_sales` or applicability is uncertain. Order of calculation: line total, discount, delivery, VAT; the free-delivery threshold uses the discounted goods total ex VAT.

## delivery_charges.csv

One row per zone: charge, free-delivery threshold (both ex VAT) and lead time in working days. Zone `NS` is not served.

## delivery_zones.csv

Maps postcode area (and optional district range) to a zone. Blank `district_from`/`district_to` means the whole area. Simplification: areas are matched by postcode area and district number only; the Isle of Wight, Isles of Scilly and a few cross-border districts are not treated separately. Unmatched postcodes are asked to be confirmed.

## customers.csv

18 customer accounts: 12 in Zone 1, 3 in Zone 2, 3 in Zone 3. Organisation names, addresses, VAT and registration numbers are invented. Each customer has at least one of `vat_number` and `company_reg_number`; these are the duplicate keys for onboarding. `payment_terms` is `30 days` or `prepay`. `zone` is derived from `postcode` using `delivery_zones.csv`. `status` is `active` or `on_hold` (Finance has paused the account). `outstanding_balance_gbp` is the amount owed; for `on_hold` accounts it is quoted in the payment reminder, and `on_hold_reason` says why. It will be replaced by a sum over the invoices table once that exists.

## customer_contacts.csv

35 contacts, 1-3 per customer. `email` (lowercase, `.example` domains) is the match key for verification. `authorised_for` lists what the contact may receive: `orders`, `invoices`, or both separated by `;`. Order status needs `orders`; an invoice copy needs `invoices`.

### Planted cases

- Contact authorised for orders only: e.g. Tom Hargreaves (C-1001), who gets order status but not invoice copies.
- Contact authorised for invoices only: e.g. Helen Whitcombe (C-1001).
- Unknown sender at a known company: any address not in the contacts table.
- Same name, two accounts: Brackenridge Diagnostics Ltd (C-1007) and Brackenridge Diagnostics (Scotland) Ltd (C-1013) are separate legal entities with different VAT numbers.
- `on_hold` customer: Kestrel Environmental Testing Ltd (C-1010), balance £1,842.60 for overdue invoices. A quote request must receive the quote plus a payment reminder with that amount.
- Prepay customers: C-1004, C-1011, C-1015.
- Registration-number-only duplicate key: C-1003, C-1004, C-1011, C-1012.
- Duplicate onboarding: test emails from "new" customers quoting an existing VAT or registration number (E-ONB-006, 007, 022).
- New records: onboarding emails create customers from `C-1019` and contacts from `K-2036` onwards, in the order received; they are expected outputs, not rows in these files.

## prospects.csv

Senders who are not customers and have asked for a quote. Created by the quotation workflow, empty at the start. A prospect is not a customer account.

| Column | Meaning |
| --- | --- |
| `prospect_id` | Unique ID, e.g. `P-0001` |
| `email` | Sender address, lowercase; duplicate key (an existing email updates `last_seen` instead of adding a row) |
| `name`, `organisation` | As stated in the email; blank if not stated |
| `first_request_summary` | The request in brief |
| `first_seen`, `last_seen` | Dates |
| `status` | `new` or `contacted` or `converted` (becomes a customer through onboarding) |
| `email_id` | ID of the first email |

## product_documents.csv

Index of the 32 product documents, each linked to the SKUs it covers. The documents themselves are fictional, written from templates so their facts match `catalogue.csv`, and kept in two formats: Markdown (source) and PDF (what is sent to customers) under `data/documents/`. The files are generated from templates by `tools/generate_documents.py` (content in `tools/doc_content.py`); rerun it after changing the index or the content, and it refreshes the `pages` column.

| Column | Meaning |
| --- | --- |
| `doc_id` | Unique, `NLS-DOC-<product>-<type>[-<version>]-R<revision>` |
| `title`, `doc_type` | `manual`, `spec_sheet`, `technical_note`, `datasheet`, `certificate_of_analysis`, `declaration_of_conformity`, `safety_data_sheet`, `calibration_certificate` |
| `product_name` | Matches `catalogue.csv` |
| `applies_to_skus` | SKUs the document covers, separated by `;` |
| `revision`, `effective_date` | Revision of the document |
| `status`, `superseded_by` | `current` or `superseded`, and the replacing `doc_id` |
| `file_path_md`, `file_path_pdf` | Paths relative to `data/` |
| `pages` | Page count of the PDF, filled when generated |
| `summary` | One line used in the reply to say what the document contains |
| `customer_shareable` | `yes` or `no`; superseded revisions are `no` |

**Rules the index supports**
- A manual covers every version of a product, so it can be sent without asking which version.
- Spec sheets differ by version, so a spec-sheet request that does not say which version needs a clarification.
- A datasheet that covers several pack sizes is one document, so it is sent without asking which pack size.
- Superseded documents are never sent as current.

**Deliberate gaps (missing-document tests)**
- VM-10 Variable speed has no spec sheet (`NLS-VM10-VAR`); only the Basic has one.
- No safety data sheet for the specimen containers.
- No validation (IQ/OQ) protocol exists for any equipment.
- The AB-220 Certified has only a sample calibration certificate; each unit's certificate is issued with the unit.
- Certificates of analysis are typical-lot only; there is no certificate for a customer's own lot.

**Traps**
- `NLS-DOC-MC10-MAN-R1` is for a superseded product.
- `NLS-DOC-AB220-MAN-R2` is a superseded revision of a current manual.
- `NLS-DOC-CT50-TECH-R1` states 15,000 ×g where the current datasheet and certificate of analysis state 12,500 ×g. Both are current; the contradiction is deliberate (`TEST_TRAPS.md`, T-14).

## emails/

Golden-set test emails with expected labels, routes and documents. See [`emails/README.md`](emails/README.md).

## orders.csv, order_lines.csv, shipments.csv

Generated by `tools/generate_orders.py` (orders designed by hand there; prices and discounts computed from the catalogue and discount tables). 45 orders for 18 customers, dated September to October 2026: 31 delivered, used by the complaint emails, and 14 in progress as of 2026-10-09 (in transit, awaiting dispatch, delayed, partially shipped), used by the order-status emails.

| File | Columns |
| --- | --- |
| `orders.csv` | `order_id` (`SO-nnnnn`), `customer_id`, `placed_by_contact_id`, `order_date`, `customer_po`, `delivery_postcode`, `status` (`awaiting_dispatch`, `in_transit`, `delayed`, `partially_shipped`, `delivered`), `estimated_dispatch` (orders not yet dispatched) |
| `order_lines.csv` | `order_id`, `line_no`, `sku`, `quantity` (units of sale), `unit_price_gbp_ex_vat`, `discount_percent`, `net_total_gbp_ex_vat`, `lot_number` (consumables), `serial_number` (equipment), `quantity_shipped`, `line_status` (`shipped`, `partially_shipped`, `pending`) |
| `shipments.csv` | `shipment_id`, `order_id`, `lines` (`line:quantity;…`, the lines and quantities this shipment carries), `dispatched_on`, `status` (`in_transit`, `delayed`, `delivered`), `estimated_delivery`, `delivery_date_status` (`estimated` or `confirmed`, for the current expected date: the revised one if present), `revised_delivery`, `delay_reason`, `delivered_on` |

The records show what was ordered and shipped, not what the customer received: a wrong item or a missing pack is the customer's report against the record (e.g. SO-10425 records an MC-12 Plus; the complaint says a Standard arrived). An order may have several shipments, each carrying stated quantities of stated lines. A line still has one lot or serial number; per-unit lots or serials would need another table.

## invoices.csv, invoice_lines.csv, invoices/

Generated by `tools/generate_invoices.py` from the orders. One invoice per dispatched shipment, numbered `INV-<order digits>-<n>` (so SO-10405, shipped twice, has INV-10405-1 and INV-10405-2), with the order's delivery charge on its first invoice, priced for the order's recorded delivery postcode. The generator refuses a shipment that carries part of a line, until a discount allocation rule exists. Status as of 2026-10-09: `paid`, `unpaid` (not yet due) or `overdue`. Prepay invoices are paid. Kestrel's two summer invoices (SO-10310, SO-10322) are the only overdue ones and add up to its `outstanding_balance_gbp` of £1,842.60; the generator checks that every customer's balance equals its overdue total. PDFs and Markdown copies are in `data/invoices/`.

| File | Columns |
| --- | --- |
| `invoices.csv` | `invoice_id`, `order_id`, `shipment_id`, `customer_id`, `invoice_date`, `due_date`, `goods_net_gbp`, `delivery_gbp`, `vat_gbp`, `total_gbp`, `status`, `paid_on`, `file_path_md`, `file_path_pdf` |
| `invoice_lines.csv` | `invoice_id`, `order_id`, `line_no`, `sku`, `quantity`, `unit_price_gbp_ex_vat`, `discount_percent`, `net_total_gbp_ex_vat` |

## suppliers.csv, supplier_invoice_register.csv, supplier_documents/

Generated by `tools/generate_supplier_invoices.py`. Five suppliers. The register holds the four supplier invoices stored before the test emails (R-0001 to R-0004, with their lines in `supplier_invoice_register_lines.csv`); resends of R-0001 and R-0004 (the latter without a VAT number, matched by name) are the duplicate tests. `supplier_documents/` holds the incoming invoices, a credit note, a statement and a payment reminder (Markdown and PDF). Planted: an illegible due date (RN-77344), totals that do not add up (KSC-5188), an unknown supplier (Marlow Lab Services), a Polaris name with a different VAT number (PL-24601), a bank-details change (FF-90455) and an instruction to automated systems (PL-24590). RN-77344 and KSC-5203 are image-only scans (rendered as images with a slight tilt, noise and JPEG artefacts, no text layer); their blotted values (a due date, a line quantity) are the planted illegible fields. Their Markdown files keep the source text with `(illegible)` in those places.

Shipment and invoice IDs are derived from the order number, so adding orders never renumbers them.
