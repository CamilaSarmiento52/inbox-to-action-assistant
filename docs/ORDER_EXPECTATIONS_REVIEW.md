# Order status, placement and records review

Reviewed by Codex (OpenAI), 2026-10-09. Scope: all 40 records in `order_status.jsonl`, the one record in `mixed_order.jsonl`, order-status-and-placement SOP v0.1, all three order CSVs, generators and shared policies/evaluation criteria.

Status: review complete; findings below remain proposed. No fixtures, generators, CSVs or SOPs changed. Creator-family provenance for this set was not established from the inspected files; confirm it to record compliance with the different-family review requirement.

## Findings requiring reconciliation

| Priority | Location | Finding and suggested correction |
| --- | --- | --- |
| Medium | Communication policy §3 versus order SOP §§3, 12; E-ORD-015 | Shared policy says a missing order number always escalates, whereas the category SOP, EVALUATION and fixture ask for clarification. Add an explicit shared-policy exception for missing/not-found numbers in status requests. Keep mismatch/unauthorised cases escalated. E-ORD-015's route is supported by the category SOP and evaluation criteria, but the policy conflict must be removed. |
| Medium | E-ORD-028; order SOP §6 steps 3 and 5 | Attachment-only PO correctly records the subject's PO number and invents no order lines. However, `missing_fields: [order_lines]` activates the unconditional instruction to ask the customer for every missing field, while step 5 and this fixture say the reviewer reads the attached PO. Distinguish pending attachment extraction from information absent from the customer's submission; do not require the customer to resend lines already supplied in the PO. No attachment contents were available to this review. |
| Medium | Order SOP §6; `order_request` schema | SOP requires each extracted value to record its source (`email`, `account`, or missing). Only postcode has an explicit source field; customer, lines, PO, requested date and quote reference do not. Add field-level provenance or narrow the SOP requirement to a documented schema. `customer_words` provides line evidence but does not implement provenance for every field. |
| Medium | E-ORD-040, `order_status.jsonl` line 40 | Complaint part uses `issues[].product_name`, whereas complaint fixtures/schema use `product_reported`; it also omits `record_lines_for_reviewer` and `customer_stated_age`. Align with the current complaint schema/generator to avoid exact-field grading failures. Customer only says “tips” and an unopened case, while the expected reported product is fixed to 200 µl from the order. Under complaint SOP §2's rule that reported product/version/pack is never filled from records, keep the customer phrase separate from the record SKU, or explicitly permit verified-record resolution and label provenance. Return route, one case, two-day age and 30-day window are supported. |
| Low | `data/emails/README.md`, file table | Says 40 order-category emails “plus” E-ORD-040. The file has 40 records total: 39 order-category records and one complaint boundary record. Correct the description; 11 held-out records is accurate. |
| Low | `tools/generate_orders.py` docstring | Says every order is dispatched on its order date, but new in-progress orders have later dispatch dates or no shipment. Restrict the statement to default delivered-history rows, and say explicit state rows supply their own dates. CSV chronology itself passed. |

Make fixture changes in `tools/generate_order_emails.py` and regenerate rather than editing JSONL directly.

## SOP and grading clarifications

- EVALUATION's status verification wording says matched sender plus order number suffices. The SOP additionally requires `authorised_for` to include `orders`, correctly exercising C-02. State that requirement in EVALUATION to avoid grading an invoices-only disclosure as valid.
- SOP §6 treats PO number as a missing field, but fixtures sometimes ask “if they use one.” Define whether PO is required or optional. Requested delivery date and quote reference are already optional; they should not trigger generic missing-field requests.
- For a new-account order, ask only for onboarding information still missing. E-ORD-027 already supplies organisation name and a full delivery address/postcode, while `reply_must_state` asks for organisation name again. Preserve those supplied fields and ask to confirm only if genuinely unclear; collect missing registration/VAT and invoice details. `account_details` as one aggregate field does not test each onboarding field's extraction.
- Make wording conditional: “will be confirmed in writing by our team” in every placement fixture can sound like guaranteed acceptance, especially for not-served, superseded or on-hold requests. Prefer “our team will review it and confirm whether we can accept it,” while preserving the no-confirmation rule.
- E-ORD-031 retains obsolete £249.00 as catalogue reference data in the reviewer draft and excludes it from the goods total. Add an explicit prohibition on presenting it as an orderable/current price in the customer reply. Likewise, superseded SKUs must never receive an automatic discount even if future data adds a matching rule.
- `record_for_reviewer.shipments[].expected_delivery` retains the original, expired date for E-ORD-010's delay with no revised date, even though the required reply correctly prohibits a date. Separate original/historical expectation from a reportable current date, or make the reportability gate explicit. Otherwise a generic serializer could repeat 2026-10-07 as current expectation.
- Change requests preserve only `request: change` and the order number. Add extracted change type/details for grading: CMP-style preservation is needed for ORD-036 cancellation, ORD-037 new postcode PH1 2NX and ORD-038 two extra glove boxes. The email remains available, but current exact-field expectations cannot detect those details being lost.
- Include order SOP §11 explicitly in EVALUATION's shared reply rubric examples. Shared rules supply dispatch dates, missing-field questions and prepay/on-hold wording not repeated in every fixture.
- Define how to classify a cancellation whose order is unavailable or unverified; determining delivered-versus-open state must not bypass verification or reveal another customer's order status.

## Supported fixture outcomes

| Emails | Result |
| --- | --- |
| ORD-001–009 | Supported verified status drafts: in-transit estimated/confirmed dates, made-to-order awaiting dispatch, revised delay, recorded delivery, two orders reported separately. ORD-005 correctly retains a confirmed future date; estimates elsewhere remain estimates. |
| ORD-010–014 | Supported Logistics escalation for no revised delay date, partial shipment, delivered/not received, missing items and conflicting expected dates. No replacement or delivery promise. |
| ORD-015–019 | Supported category-SOP routes: missing/not-found numbers clarify; wrong legal entity, invoices-only contact and unknown sender escalate with no disclosure. Shared-policy reconciliation for ORD-015 is noted above. |
| ORD-020–021 | Injection ignored/flagged with escalation and no record mutation; resend links to ORD-001 with no duplicate reply. |
| ORD-022–027 | Supported Sales drafts: complete order with D1, unclear version, disputed price/unverifiable quote reference, on-hold Finance approval/reminder, prepay, new account with supplied delivery postcode. Provenance/onboarding refinements above remain applicable. |
| ORD-028–035 | Supported Sales routes for attached PO, requested date, not-served destination, obsolete product, supply-versus-price boundaries, invoices-only purchaser with D4, and prospect accepting an offer. Subject is a valid source for ORD-028's PO number; it is not inferred from filename. |
| ORD-036–039 | Supported Logistics changes/cancellation routes, with verification before disclosure and nothing recorded as changed. Extracted change details need schema coverage. |
| ORD-040 | Delivered unopened goods correctly route as convenience return to Technical / quality review; schema/report provenance correction noted above. |
| MIX-OQ-001 | Separate order and quotation parts, combined after review at overall escalation. Ten microtube bags: £98.00 less D1 £4.90 = £93.10 catalogue goods. Independent HB-2 Dual quote: £329.00, free Zone 1 delivery, VAT £65.80, total £394.80. No basket merging or order confirmation. |

## Three order files: verification and limitations

Checked `data/orders.csv`, `data/order_lines.csv`, `data/shipments.csv` independently of generator calculations.

- 44 unique orders, 51 unique `(order_id, line_no)` keys and 40 unique shipments. All foreign keys resolve; placing contacts belong to the recorded customer.
- Status distribution: 31 delivered, 6 in transit, 4 awaiting dispatch, 2 delayed and 1 partially shipped.
- Every current line has positive quantity, correct catalogue price, table discount and net amount under discount-first Decimal half-up rounding.
- Parsed shipment `lines` entries as `line_no:quantity`; all references exist, quantities are positive, and per-line shipment sums equal `quantity_shipped` without exceeding quantities ordered. `pending`/`partially_shipped`/`shipped` line statuses agree with those sums.
- Dispatch never precedes order date; delivered shipment dates never precede dispatch. Awaiting-dispatch orders have no shipment. SO-10445 has six pipette packs delivered and one VM-10 pending, correctly matching the status fixture.
- Revised date selection and estimated/confirmed labels in fixture reviewer records match the CSVs. SO-10443 uses revised 2026-10-13; SO-10444 has no revised date; SO-10447's future date is confirmed.

Existing delivered-order histories remain available to complaint fixtures. `generate_complaint_emails.py` now obtains delivery through a helper, so the original single-shipment dictionary issue was addressed for current fixtures, but its helper still assumes one delivered shipment. Multiple delivery dates for affected lines need issue-specific shipment selection.

The shipment shape now supports line quantities, but no fixture actually tests one line split between multiple shipments or multiple shipment dates. `record()` omits shipment IDs, line/quantity mappings and product contents from its reviewer snapshot, so its shipment dates cannot be tied to affected lines using that snapshot alone. Preserve these relationships before adding such cases. One lot/serial field per order line also still limits multiple-lot or multiple-unit equipment traceability.

## Checks, coverage and limits

Parsed all 41 emails and checked each request against its expectations. Independently checked every status verification result, reportability flag, order-status/dispatch field, selected expected date and its certainty, delivered dates and pending quantities against CSV records; every priced placement line and available goods total; label sets and most-restrictive overall route. All stored-value checks passed. The mixed quote arithmetic was also verified.

Single-file totals: 9 drafts, 2 clarifications, 28 escalations, 1 duplicate; 29 tuning and 11 held out. All O-01–O-24 trap IDs occur. The single mixed email escalates and is tuning.

Coverage additions still useful: late missing-item report and its required flag; exactly/just beyond the calendar-day limit; missing quantity and missing postcode in placement; made-to-order placement; unmatched postcode; mixed verified/unverified orders in one email; order placement plus status under one label; unauthorised change; unknown sender with nonexistent order number; quantity-split shipments and per-shipment revised/confirmed dates. Current `status_route()` checks whether **any** delayed shipment has a revised date, which would miss another delayed shipment without one; use per-shipment readiness before testing multiple shipments.

No classifier, agent, attachment parser or email-sending runtime was exercised. This review checks source/fixture consistency, not measured end-to-end implementation performance.

## Creator response (2026-10-09)

The emails were created by Claude (Anthropic) and reviewed by Codex (OpenAI), so the review meets the different-family requirement in EVALUATION.md. All fixture changes were made in the generators and regenerated.

**Findings**
- Communication policy §3: a missing or unrecognised order number is asked for, not escalated; mismatched and unauthorised senders still escalate.
- E-ORD-028: the attached PO's lines are in `pending_attachment_review`, not `missing_fields`; the reply does not ask the customer to resend them. SOP §6 says details in an attachment are not missing.
- Provenance: SOP §6 narrowed to what the schema holds: customer words per line, postcode source, and PO, requested date and quote reference from the email only.
- E-ORD-040: one correction to the review: the complaint schema already uses `product_name` (renamed in the complaint follow-up). The part is now built with the complaint generator's own function, so it carries `record_lines_for_reviewer`, `customer_stated_age` and `customer_quantity_estimate`; the product stays as the customer described it ("tips, one unopened case") and the SKU is reviewer-only.
- README counts corrected; `generate_orders.py` docstring now limits the dispatch-on-order-date statement to default delivered rows.

**Clarifications**
- EVALUATION.md: verification includes `authorised_for` containing `orders`; the shared reply rubric includes order SOP §11.
- PO number defined as optional (asked for "if you use one"); requested date and quote reference never asked for.
- New-account orders ask only for onboarding details not given; `account_details` replaced by explicit fields (E-ORD-027, E-ORD-035).
- Acknowledgement wording: "our team will review it and confirm in writing whether we can accept it".
- Superseded SKUs never discounted (enforced in the generator) and their old price never quoted (E-ORD-031).
- Reviewer records separate `original_estimated_delivery` from `current_expected_delivery`, which is null for a delay without a revised date; shipments now carry their ID and lines.
- Change requests carry `change` (type and details): E-ORD-036 to 039.
- SOP §7: a cancellation that fails verification is handled as an order change; the open-or-delivered state is looked at only after verification.
- Delay readiness is judged per shipment.
- The complaint generator was made importable without changing its output (checked byte for byte).

**Added cases (E-ORD-041 to 046, traps O-25 to O-29)**
Late missing-item report; one verified and one unverified order in one email; unknown sender with a non-existent order number; made-to-order placement; placement with a missing quantity and an unrecognised postcode; order plus status in one part. Not yet reviewed.

**Not done**
- Quantity-split shipments and per-shipment revised dates are not yet tested; the complaint helper still assumes one delivered shipment per order.
- Exact calendar-day boundary cases for missing items, and an unauthorised change request, are not added.

## Follow-up review: six added emails (2026-10-09)

Reviewed E-ORD-041 through E-ORD-046 against SOP v0.2, the updated generators, contact/customer/catalogue/discount/delivery tables, and the creator response. All six have supported classification, routes, verification and stored numeric/date values. One retrieval-label correction remains proposed; no route, pricing or date corrections are needed.

| Email | Result | Evidence |
| --- | --- | --- |
| E-ORD-041 | Supported | SO-10456 is the sender's order, delivered 2026-10-02. Four bags were recorded shipped; customer reports two missing. Receipt on 2026-10-09 is seven calendar days later, correctly flagged `outside_reporting_window`. Logistics escalation, no refusal or remedy promise. |
| E-ORD-042 | Supported | Katie is verified for Riverside's SO-10440, whose delivery is estimated 2026-10-12. SO-10447 belongs to Calder; nothing about it is disclosed. One category part escalates to Logistics while retaining the permitted answer for SO-10440. |
| E-ORD-043 | Supported under documented check order | SO-10998 does not exist, so verification stops at `order_not_found` before testing the unknown sender. Clarification asks to check the supplied number, with no order facts or ownership disclosed. No account is created. |
| E-ORD-044 | Supported | One AB-220 Certified at £795.00, no discount, active C-1007, account postcode BS8 1LN/Zone 1. Made-to-order flag and Sales escalation are correct. About three working days is an estimated dispatch duration, not a confirmed date or an accepted order. |
| E-ORD-045 | Supported | Glove quantity is absent; the reliable pipette line is 2 × £42.00 = £84.00. Overall goods total remains null. Email postcode BX1 1LT has no delivery-zone row and must not be replaced by the account postcode. Ask for glove quantity and address confirmation; Sales reviews the incomplete draft. |
| E-ORD-046 | Supported outcome; add placement retrieval labels | Shona is an orders-authorised contact of C-1016, so SO-10441's estimated 2026-10-13 date is reportable. New order is 3 × £14.40 = £43.20, no discount, PO DFA-240, account postcode IV3 8LX/Zone 3. Both requests share one label/part; Sales escalation is correct under §10. However, `passages` lists only SOP §§3, 4. Add §6 for the order draft/acknowledgement and §10 for the same-label merge/owner rule. These are material sources for this case's retrieval grading, not optional background. |

Make the E-ORD-046 passage correction in `tools/generate_order_emails.py` and regenerate. This follow-up changed neither generator nor fixtures.

### Creator-response verification

Confirmed the shared-policy exception for missing/not-found order numbers; pending attachment review instead of missing lines in ORD-028; narrowed provenance requirements; optional PO wording; explicit missing onboarding fields; conditional acceptance acknowledgement; superseded-price prohibition and discount guard; separate original/current shipment dates and shipment relationships; extracted change details; verification before delivered/open cancellation routing; per-shipment delay readiness; and the matching evaluation rubric/verification updates.

Correction to this review's original schema finding: the creator is right that the complaint schema had already been renamed to `product_name`. The earlier suggestion to use `product_reported` was outdated. ORD-040 now uses the complaint builder, has reviewer-only record lines and the common age/quantity-estimate fields, and preserves “tips, one unopened case” without treating the record SKU as customer-reported. The original provenance/common-field concerns are addressed; no rename back to `product_reported` is needed.

The creator identifies Claude (Anthropic) as creator, so on that recorded provenance the Codex (OpenAI) review meets the different-family requirement. This resolves the original report's provenance caveat. Importable complaint generation was inspected; the creator's historical byte-for-byte comparison was not independently rerun in this follow-up.

### Checks and remaining limits

- Independently checked all six new verification outcomes/reportability flags, reviewer shipment IDs/line mappings/current dates/certainty/delivery dates, account IDs/status/payment terms, postcode sources/zones, priced lines and goods totals against source records. All passed.
- Confirmed the late-report flag from the actual email date and recorded delivery, and the distinction between the absent glove quantity and the complete pipette line.
- Current single-file counts: 46 records; 9 drafts, 3 clarifications, 33 escalations and 1 duplicate; 33 tuning and 13 held out. Current tables contain 45 orders, 53 lines and 41 shipments. This follow-up checked records used by the new emails; it did not repeat the full-table audit from the initial review.
- Remaining coverage gaps recorded by the creator are accurate: quantity-split shipments/per-shipment revised dates, exact missing-item calendar-day boundaries and an unauthorised change request are still untested.
- Before adding multiple delivered shipments, replace the late-missing-item calculation's latest-delivery-date selection with the affected shipment/line date. Otherwise a later unrelated shipment could make an older shortage appear timely. Existing single-shipment ORD-041 is correct.
- Define ownership when a same-label placement-plus-status email includes a status problem requiring Logistics review. ORD-046's routine status answer needs no such escalation, so Sales ownership is supported; a future failed-verification/delivery-issue counterpart should preserve Logistics involvement as well.

No runtime classifier/agent, attachment parser or email-sending system was exercised. These are fixture/source checks, not end-to-end performance results.


## Creator response to the follow-up (2026-10-09)

- E-ORD-046: passages now include SOP §6 and §10, changed in the generator and regenerated.
- SOP §10: when an order and a status request share a part and the status request needs a person, Logistics is told as well and both decide before the reply is sent.
- The late-missing-item calculation carries a comment: before orders with several delivered shipments are added, use the affected line's shipment, not the latest one.

Still not tested: quantity-split shipments and per-shipment revised dates, the exact 2-day boundary for missing items, an unauthorised change request.
