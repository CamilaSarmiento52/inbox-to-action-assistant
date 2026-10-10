# Complaint expectations, SOP and order records review

Reviewed by Codex (OpenAI), 2026-10-08. Scope: all 26 records in `complaint.jsonl`, both records in `mixed_complaint.jsonl`, complaints-and-returns SOP v0.1, `orders.csv`, `order_lines.csv`, `shipments.csv`, both generators and supporting policies/customer/catalogue records.

Status: review complete; corrections proposed below. No fixtures, generators or policies were changed. Creator family for this complaint set has not been confirmed in the inspected documentation, so different-family review compliance remains subject to that provenance.

## Findings requiring correction

| Priority | Location | Finding and suggested correction |
| --- | --- | --- |
| High | E-MIX-CT-001, `mixed_complaint.jsonl` line 2 | Customer says VM-10, no version or order number. The expected issue assigns `NLS-VM10-BAS` from an account order, although SOP §4 requires the number from the email and the generator's own note acknowledges it is missing. Keep the model/version unresolved, add `product_version` to missing information, and ask for it or resolve it once the order is verified. Safety handling remains urgent and must not wait for these details. |
| High | E-MIX-CT-001 | “Barely a week old” does not supply an exact delivery date of 2026-10-02. `stated_delivery` invents that date, yielding exactly 7 days and a definite `within` window. Record an approximate age only in the summary; ask when delivered, keep exact days/window unknown until supported. Do not find the order by account to fill the gap. |
| Medium | E-CMP-002, 014, 023 | `missing_info` omits `when_noticed`. CMP-002 gives no discovery time; CMP-014's “after a day in the fridge” describes the failure condition, not when it was first noticed; CMP-023 gives no discovery time. Add the missing field and the required question under SOP §2. Delivery dates in records do not establish discovery dates. |
| Medium | E-CMP-012, `complaint.jsonl` line 12 | Unverified sender gives no version or serial number. Fixture assigns Standard from another customer's order, omits those unresolved fields and does not establish when damage was noticed. Keep reported AB-220 separate from record-derived Standard; request version/serial where available and discovery time. The order's information can be shown to the reviewer with provenance, but cannot become customer-reported issue facts or appear in the reply. Mismatch flag and no-disclosure requirements are correct. |
| Medium | E-CMP-020, `complaint.jsonl` line 20 | No order, pack size or quantity is supplied, yet issue SKU is fixed to the box SKU `NLS-PT200-B`. Tips also have a case SKU. Leave SKU unresolved and request pack size or use a subsequently verified order; preserve the product-level defect description. |
| Medium | E-CMP-022 and E-MIX-CT-001 | `customer_asks` is null and `customer_request` marked missing even though the customer asks “Do we need to send it back?” or “What should we do?” SOP §2 asks what the customer is requesting, not necessarily a chosen commercial remedy. Preserve those explicit process/help requests. If a preferred remedy is additionally needed, represent that separately rather than discarding the stated request. The same distinction should be made explicit for “Please advise” (CMP-003) and “Please could you look into it?” (CMP-013), which currently also encode null requests. |
| Medium | SOP §7 versus E-CMP-025 | Transit-damage remedies list replacement or refund when asked, but CMP-025 proposes a credit note. The shared returns policy permits credit notes, so the proposal is reasonable; extend SOP §7 to cover customer-requested credit notes for transit damage/wrong items, or align the expectation with the existing SOP. No credit may be promised. |

Make fixture corrections in `tools/generate_complaint_emails.py` and regenerate; direct JSONL edits would be overwritten. Route changes are not required for these complaint findings: all affected complaint parts still escalate.

## SOP and schema clarifications

- SOP §3 requires a reporting-window result **for each issue**, but the complaint schema/generator stores a single aggregate `window`. Add issue-level window results, keeping an aggregate only if useful. A case with damage outside 2 days and a quality defect within 14 days should preserve both results. Existing multi-issue CMP-021 has two 2-day issues, so it does not expose this gap.
- SOP §6 intentionally treats 48 hours as 2 calendar days. This is reproducible with date-only shipment records but differs from elapsed 48-hour precision in the shared policy. Explicitly record the calendar-day convention in the shared policy, or store delivery timestamps and calculate hours. Do not label the current calculation as an exact elapsed-hours test.
- Define missing delivery-date handling. Cases with no order and no usable customer delivery statement currently ask for order number, but omit a delivery-date question. Decide whether order-number follow-up alone suffices until lookup succeeds; otherwise add `delivery_date` consistently. E-MIX-CT-001 cannot use an invented date either way.
- Distinguish evidence requested **where available** from mandatory evidence. CMP-016/019/025 explicitly request photographs; several other damage fixtures do not. A recorded lot/serial can satisfy that identifier under §2, but does not supply photographs. Specify when photographs are useful and ask conditionally without treating unavailable photographs as a blocking failure.
- Limit “when noticed” to actual problems; convenience returns have no defect discovery date. Confirm unused/original-packaging condition where a convenience return email does not establish it. Sealed packs in CMP-007/008 support a provisional proposal, with eligibility confirmed by the reviewer.
- SOP §8 says returnable goods must be unused, then describes inspection returns of units used with biological material. Distinguish convenience-return eligibility from faulty-unit inspection and the decontamination requirement, so a used faulty unit is not automatically rejected by the convenience rule.
- Ensure SOP §14's no-disclosure check covers **all** record-derived contents, including product/version/quantities and prices. Its examples focus on order numbers, identifiers, dates and addresses, whereas §4 and §13 prohibit any order details. Compare reply statements with customer-provided evidence, not just isolated values that may coincidentally overlap records.
- Include complaints SOP §10 explicitly in EVALUATION's shared reply rubric examples. Case-specific `reply_must_state` does not consistently list every required missing-information question, so the SOP rubric remains essential.

## Order files

The three requested files are `data/orders.csv`, `data/order_lines.csv` and `data/shipments.csv`. All current rows passed integrity and arithmetic checks:

- 22 unique order IDs, 24 unique `(order_id, line_no)` keys, and 22 unique shipment IDs.
- Every order references an existing customer and contact; the placing contact belongs to that customer. Delivery postcodes match the configured account postcodes.
- Every line references an existing order and SKU, has positive quantity, the correct catalogue price and applicable discount, and a correct net total under penny rounding.
- Equipment lines carry serial numbers and consumable lines carry lot numbers, with the other identifier field empty.
- Every shipment references an existing order and valid line numbers; the current full shipments cover every order line. Order date ≤ dispatch date ≤ delivery date, with consistent delivered/shipped statuses.

These files describe what was ordered and recorded as shipped. A customer's wrong-item or missing-item report is not a CSV inconsistency: SO-10425 records Plus while CMP-003 reports Standard received; SO-10434 records four pipette packs shipped while the mixed email reports two received.

Future limitations, not failures of the current delivered-order fixture set:

- `generate_complaint_emails.py` indexes shipments by order ID, silently keeping the last shipment if an order has several. Select the shipment for the affected line/lot and represent delivery separately by issue before adding split deliveries.
- Shipment `line_nos` cannot encode how many units were shipped from one line, and a line has one lot/serial field. Quantity-split deliveries, multiple lots or multiple equipment serials need a richer representation.
- `generate_orders.py` computes a rounded net amount directly; the quotation SOP rounds the discount first. The current 24 lines agree under both methods, but they can differ at half-penny boundaries. Use one shared calculation convention before introducing prices/discounts that expose this difference.
- Every shipment generator row uses the order date as dispatch date. The AB-220 Certified made-to-order order SO-10380 is also dispatched that day and delivered seven days later in Zone 1. This is not prohibited by the approximate dispatch policy, but the fixture does not demonstrate the stated lead-time calculation. Keep dates intentionally historical rather than presenting them as generated delivery predictions.
- All orders are delivered. Delayed, partial and in-transit cases are explicitly deferred in the data README; these files do not yet validate order-status handling across those states.

## Supported outcomes and coverage

All complaint parts escalate to the documented owner: Logistics for transit damage/wrong items; Technical / quality review for quality defects, equipment faults and convenience returns. Unknown or mismatched senders can report complaints, but receive no account/order disclosures. Missing information does not downgrade the escalation route. Equipment faults have no proposed remedy or warranty judgement; safety is urgent; return authorisation precedes returns; remedies remain proposals.

- CMP-001/004 correctly preserve affected quantities and explicit replacement requests; CMP-006 correctly handles a non-safety fault without inventing a technical question.
- CMP-007/008 preserve convenience-return quantities and the opened-sterile split; CMP-009 flags the made-to-order restriction in the summary without refusing in the reply.
- CMP-010/011/017/022/025 have correct record-derived outside-window flags and do not refuse late reports.
- CMP-005 requests the absent order rather than selecting an account order; CMP-013 correctly flags SO-99999 as not found; CMP-020 flags an unknown sender.
- CMP-017 flags/ignores the injected refund approval. Its on-hold account does not trigger a quotation payment reminder in complaint handling.
- CMP-018 follows CMP-001 from the same sender and links to it without a second reply. CMP-019 correctly reads the forwarded request under the outer sender's account.
- CMP-021 preserves damage and wrong items in one complaint part. CMP-024 correctly verifies another contact of the same customer, not only the original purchaser.
- CMP-026 is correctly quotation-only: the settled historical complaint is background. Its £92.50 goods + £12.95 delivery + £21.09 VAT = £126.54 is correct.
- MIX-CO-001 preserves the damage complaint and missing-item delivery part; both go to Logistics, with one combined reply. MIX-CT-001 correctly combines complaint and technical safety parts with stop-using/disconnect advice first, subject to the extraction corrections above.

Counts: `complaint.jsonl` has 24 escalations, one duplicate, one quotation draft; 19 tuning and 7 held-out records. Both mixed records escalate and are tuning. R-01 through R-15 all appear. Add boundary fixtures for exactly/just outside 14 and 30 days, a convenience return past 30 days, mixed Logistics/Technical ownership, different issue windows, an unknown sender with a real order number, and conflicting customer-versus-record delivery dates.

No classifier, agent, retrieval system, attachment-image inspection or email-sending runtime was exercised. The checks validate source consistency and expected fixture values, not end-to-end implementation performance.

## Creator response (2026-10-08)

The emails were created by Claude (Anthropic) and reviewed by Codex (OpenAI), so the review meets the different-family requirement in EVALUATION.md. All fixture changes were made in the generators and regenerated.

**Fixtures**
- E-MIX-CT-001: VM-10 version unresolved (`sku` null; version and serial asked for); "barely a week old" kept as `customer_stated_age`, window unknown; the stated request "what to do" kept. The safety instruction is still first.
- E-CMP-012: AB-220 version unresolved and asked for, with serial, discovery time and photographs; the record's lines are in `record_lines_for_reviewer`, not in the customer's issue.
- E-CMP-020: pack size unresolved and asked for.
- E-CMP-002, 014, 023: `when_noticed` added and asked.
- E-CMP-003, 013, 022: the stated request kept ("advice", "look into it", "whether to send it back"); a preferred remedy asked for only where relevant (003, 013).
- Photographs asked for in transit-damage cases without attachments (E-CMP-010, 012, 021, 031, E-MIX-CO-001).
- Issue-level windows: each issue now carries `window_days` and `window`; the overall `window` is `outside` if any issue is.

**SOP v0.2 and policy**
- §2: what counts as the customer's request; `when_noticed` for problems only; unused-condition check for convenience returns; evidence asked where useful, never blocking; product, version, pack and quantity never filled in from the record.
- §6: a window per issue; calendar days, also stated in returns policy §1; the record wins over a conflicting customer date (flagged `delivery_date_conflict`); approximate ages never become dates; no order and no date means unknown, and asking for the order number is enough.
- §7: credit note added for transit damage and wrong items when asked (E-CMP-025).
- §8: convenience-return eligibility separated from inspection returns of used faulty units.
- §14: the no-disclosure check covers everything taken from the record, compared with the customer's own email.
- EVALUATION.md: the shared reply rubric includes complaints SOP §10.

**Order files**
- `generate_orders.py` now rounds the discount first, the same convention as the quotation SOP; all existing lines are unchanged. Its docstring and the data README record that dates are fixed history and that split deliveries need a richer shape. Six orders added for the boundary cases (28 in total).

**Boundary cases added (E-CMP-027 to 033)**
Exactly 14 and 15 days (quality), exactly 30 and 31 days (convenience return), one email with two owners and two windows, an unknown sender quoting a real order, and a customer date that conflicts with the record. New traps R-16 to R-18. Not yet reviewed.

## Follow-up review: seven added emails (2026-10-09)

Reviewed E-CMP-027 through E-CMP-033 against SOP v0.2, the regenerated order tables and the creator response. All seven have supported classification, escalation owners and window calculations. Two fixture corrections remain proposed; no numeric window or route corrections are needed.

| Email | Result | Evidence |
| --- | --- | --- |
| E-CMP-027 | Supported | SO-10391 delivered 2026-09-25: exactly 14 calendar days at receipt, within the quality window. Customer reports five pipette packs, discovery this morning and asks for replacement. Verified C-1013 contact; Technical / quality review; replacement proposed only. |
| E-CMP-028 | Correct window/route; preserve uncertain quantity | SO-10388 delivered 2026-09-24: 15 days, outside the 14-day quality window. Technical / quality review and outside-window flag are correct. However, “probably two packs' worth” is an estimate, while `quantity_affected: 2` represents an exact quantity and `missing_info` is empty. Preserve the estimate with explicit uncertainty, or leave the exact quantity unresolved with an estimated-quantity field/note; ask the customer to confirm how many packs are affected. Do not silently convert an estimate to a confirmed replacement quantity. |
| E-CMP-029 | Supported | SO-10375 delivered 2026-09-09: exactly 30 days, within the convenience-return window. Ten unopened glove boxes reported; return authorisation is a proposal for a person, not permission to send goods back. Technical / quality review is correct. |
| E-CMP-030 | Supported | SO-10372 delivered 2026-09-08: 31 days, outside the convenience-return window. Four unopened packs reported; no action proposed under the window rule, with a person deciding. No customer-facing refusal. Gareth belongs to the order customer; invoices-only authorisation does not restrict complaints. |
| E-CMP-031 | Supported | SO-10386 delivered 2026-09-29: 10 days. Split bag transit damage is outside 2 days; heater fault is within 14 days. Technical / quality review owns the part, Logistics is also notified. Replacement proposed for the bag only; none for the heater. Customer supplies a singular heater and bag; no technical question or safety signal requires another label. |
| E-CMP-032 | Supported | SO-10433 exists, but sender is absent from contacts. `sender_matches_order: false` and `unknown_sender` flag are correct under the updated generator. Product and quantity remain unresolved, record lines are reviewer-only, and the reply asks for expected/received products, quantity, discovery time and order-number confirmation under the shared rubric. Logistics; replacement/collection proposed only. Same-order similarity to CMP-002 is correctly left for human linking rather than treated as an established duplicate. |
| E-CMP-033 | Correct window/route; add discovery-time question | SO-10417 records delivery 2026-10-05, versus customer's “yesterday” (2026-10-08). Record-based 4 days, `delivery_date_conflict`, outside-window flag and Logistics owner are correct under SOP §6. Customer says a pack “is crushed” but does not say when they discovered it. Add `when_noticed` to `missing_info` and require the question in the reply. A stated arrival date is not a discovery date. Preserve both delivery dates in the summary and avoid contradicting the customer in the reply. |

Make these two corrections in `tools/generate_complaint_emails.py` and regenerate. No fixture or generator was changed by this follow-up review.

### Creator-response verification

Confirmed the previous critical fixes: MIX-CT-001 now has unresolved SKU/version, no invented delivery date, unknown days/window, an approximate age recorded separately and the customer's help request retained; CMP-012 separates reviewer record lines from the unresolved reported version; CMP-020 leaves pack SKU unresolved. Discovery-time questions were added to CMP-002/014/023, and explicit requests are retained in CMP-003/013/022.

Confirmed issue-level windows, mixed-owner notification, the credit-note remedy rule, calendar-day wording in the shared policy, return/inspection distinctions, approximate-age and conflicting-date handling, expanded no-disclosure checks, and complaint SOP inclusion in EVALUATION's shared rubric. Order generation now rounds the discount before subtracting it and documents fixed historical dates and split-delivery limitations.

The creator response identifies Claude (Anthropic) as creator. On that recorded provenance, the Codex (OpenAI) review meets the project's different-family requirement; this resolves the original report's provenance caveat.

One extraction clarification remains useful: `product_reported` is generated from canonical catalogue names and versions when an SKU is supplied, rather than preserving the customer's actual words. Treat it as a resolved display name or add a separate source phrase. The SOP's requirement to quote the customer's words should not be graded against a canonical string the customer never used. Unopened original boxes/packs support provisional convenience-return proposals; reviewer confirmation of unused/original-packaging eligibility remains part of the shared rubric when not explicit.

### Checks performed

- Independently checked all seven new sender/order matches, reviewer-only record lines, delivery-day differences, each issue's window length/result, overall outside-window flags, owners/secondary notification and escalation routes. All stored values passed, apart from the semantic quantity/discovery-time findings above.
- Rechecked the expanded tables: 28 orders, 31 lines and 28 shipments. Unique keys, contact/customer relationships, catalogue prices, discounts, rounded net line totals, valid shipment line references and order/dispatch/delivery chronology all passed.
- Current single-file counts: 33 emails, comprising 31 escalations, one duplicate and one quotation draft; 24 tuning and 9 held out. The two mixed records remain separate and escalate.
- New cases cover the 14/15-day and 30/31-day boundaries, separate windows/owners in one complaint, an unknown sender with a real order, and a customer/record date conflict.

These are fixture and source checks. No agent/classifier runtime or image attachment inspection was performed. The remaining initial-review limitations about multiple shipments per order and quantity-split shipment records remain applicable.


## Creator response to the follow-up (2026-10-09)

- E-CMP-028: `quantity_affected` is null and asked for; the estimate is kept as `customer_quantity_estimate`.
- E-CMP-033: `when_noticed` added and asked.
- `product_reported` renamed `product_name` and documented as a resolved display name (or the customer's description when unresolved), not the customer's exact words.

All in the generator, regenerated. Still outstanding: multiple shipments per order and quantity-split shipments, before order status data is added.
