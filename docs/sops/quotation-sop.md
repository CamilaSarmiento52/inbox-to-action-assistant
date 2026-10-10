# SOP: quotation requests

Version 0.2 (draft) · effective 2026-10-08 · status: current

> Fictional procedure for the fictional company Northfield Lab Supply.

## 1. Purpose and scope
Answer a customer's request for a price, using the catalogue, discount rules, delivery tables and terms of sale. A person approves every reply before it is sent. This SOP covers the quotation part of an email only. Other requests in the same email are handled by their own SOPs and merged (section 9).

An email that asks what something will cost is a quotation request even when it says "order" ("we plan to order 12 boxes, what will that come to?") or asks for a quote in order to raise a purchase order. An email that tells us to supply goods, or sends a purchase order, is an order (order SOP). Confirmed in the classification guide (B-1).

A question only about stock, availability or lead time is also a quotation request (classification guide B-3, decided 2026-10-10). It is answered from `stocked` in `catalogue.csv` and the zone lead time in `delivery_charges.csv` (delivery policy §2), stated as estimates; no price is given unless one is asked for, and no stock level or date is promised. The version is not asked for when the answer is the same for every version. An unknown sender is recorded as a prospect, as for any quotation (section 8).

Prices, discounts and delivery charges are read only from `catalogue.csv`, `discounts.csv`, `delivery_charges.csv` and `delivery_zones.csv`. All arithmetic is done by code, never by the model.

## 2. Required information
A full quote needs all four:
1. Product.
2. Version, pack size or model, where the product has more than one.
3. Quantity.
4. Delivery postcode. For a known customer whose email gives none, the delivery postcode on their account is used, and the reply names the address used so the customer can correct it. A postcode in the email always wins (decided 2026-10-08).

The sender's identity is not required. Check it against the customer records for payment terms and account status. The account is decided by the contact record that matches the sender's email address, not by the organisation name in the email.

## 3. Procedure
1. **Identify the lines.** Extract each requested product and quantity, quoting the words used in the email.
2. **Resolve each product** to a catalogue SKU: exact match, then fuzzy, then semantic. The model only chooses among the candidates shown.
   - High confidence: use it, and show the resolved catalogue name in the reply.
   - Medium confidence: ask "did you mean X?" and show its price.
   - No match: go to section 6.
3. **Check status.** A `superseded` SKU is never quoted as current. Offer the `replaced_by_sku` as a labelled suggestion, with its price. A SKU with `stocked = no` is made to order; say so, and that it is dispatched within about 3 working days, plus the zone's delivery lead time (delivery policy 2.3). Both are estimates.
4. **Resolve version.** If a product has several versions and the email does not say which, show every version with its price and inclusions, and ask which one.
5. **Convert quantity to units of sale** (section 4).
6. **Apply discounts** from `discounts.csv` (section 5).
7. **Add delivery** from the postcode (section 7).
8. **Calculate** in this order: line totals, discount, delivery, VAT at 20%. Rounding: each line's discount amount is rounded half up to the penny; the goods total is the sum of the discounted lines; delivery is added; VAT is calculated on goods plus delivery and rounded half up to the penny.
9. **Write the reply** (section 10) and send it for approval.

## 4. Quantity and unit of sale
If the quantity is not stated in the unit of sale, say what the unit contains and price the nearest options.

Example: a request for 1,000 pipette tips. Our box holds 960 tips. Reply that a box holds 960 and show 1 box (960 tips) and 2 boxes (1,920 tips) with prices. Recommend the smaller quantity that covers the request, here 2 boxes, and ask which the customer wants. The quote is not final until the customer chooses.

If a case is cheaper per item than the same quantity in boxes, mention it as a suggestion. It never replaces what was asked for.

## 5. Discounts
Quantities count units of sale of the same SKU on one line.

| Situation | Action |
| --- | --- |
| Quantity falls in a rule with `apply_discount` | Apply it, show the percentage and the amount |
| Equipment, 2 or more units of one SKU (D4) | No discount; send to Sales |
| Applicability uncertain, or the customer asks for a special price | Send to Sales |

One discount per line; no stacking; superseded SKUs are never discounted.

## 6. Products that are not in the catalogue
1. Look for an alternative in the same category with the same function and the nearest size or version.
2. If one exists, offer it explicitly as a suggestion, labelled as an alternative, with its price, and ask whether the customer would like a quote for it (route: ask for clarification). Never substitute it silently.
3. If nothing is related, say that we do not carry the product, and send the case to Sales.
4. Absence from the catalogue says nothing about stock elsewhere.

## 7. Delivery
- **Postcode given:** match it to a zone with `delivery_zones.csv`. The charge, free-delivery threshold and lead time come from `delivery_charges.csv`. Free delivery is judged on the discounted goods total, ex VAT.
- **Postcode missing** (unknown sender, or a known customer with no delivery address on the account): give the goods price, ask for the delivery postcode, and say that the delivery charge and the total will be added once it is received. Show what the quote is so far, not a total.
- **Postcode not matched:** ask the customer to confirm the address.
- **Not served** (Channel Islands, Isle of Man): say that we cannot deliver there and send the case to Sales.

## 8. Customers and senders
| Sender | Handling |
| --- | --- |
| Known customer, active | Quote as normal; use their payment terms in the reply |
| Known customer, `on_hold` | Quote as normal, with a payment reminder in the reply (see below), and flag to Sales. `on_hold` means Finance has paused the account, for example for overdue invoices; a quote is not a commitment, but new orders need Finance and Sales approval |
| Unknown sender | Quote as normal. No account terms are assumed. Record the sender as a prospect and notify Sales (see below) |

**Payment reminder.** For an `on_hold` customer, the reply includes a polite reminder that the account has an outstanding balance, stating the amount from `outstanding_balance_gbp` and pointing them to Finance. The amount comes only from the customer record, never from the email or the model. If the amount is missing or zero while the account is `on_hold`, no amount is stated and the case goes to Sales and Finance. The reminder never threatens, and a person approves it with the rest of the reply.

**Prospect record.** For an unknown sender, add a row to `prospects.csv`: name, email, organisation if stated, the request in brief, the date and the email ID. If the email is already recorded as a prospect, update `last_seen` instead of adding a new row. A prospect is not a customer account; creating an account follows the onboarding SOP. Sales is told that a possible new customer has asked for a quote.

## 9. Mixed requests
Every email has an email ID. The classifier gives it the set of categories it contains, one label per category; several requests of the same category share one label. Each label becomes one case part, handled by that category's agent under the same email ID.

- The quotation agent handles only the quotation part, including every quotation line in the email.
- When every part is ready and any required review is done, the parts are merged into one reply. The quotation is not sent on its own first.
- The review summary lists each part, what was done and what is proposed.

## 10. Reply content
1. Greeting and thanks.
2. The quote: for each line, the catalogue name and version, unit of sale, quantity, unit price, discount and line total. Then, only when the request is complete and the destination is served, delivery, VAT and the total, all in pounds, with prices ex VAT stated. Otherwise the prices established so far, without a total (sections 7, 11). The delivery address used, when it comes from the account.
3. Anything unresolved, clearly marked: what we need from the customer and what happens once we have it.
4. Suggested alternatives or case pricing, labelled as suggestions.
5. Validity: 30 days from the date of the quote.
6. For an `on_hold` customer, the payment reminder, with the outstanding amount only when the record holds a positive amount (section 8).
7. Closing and team sign-off.

Estimates stay estimates, and nothing is stated that the records do not support.

## 11. Routes
| Outcome | Route |
| --- | --- |
| All four required items present, nothing unresolved | Draft for approval |
| Anything missing or ambiguous | Ask for clarification, with the reliable parts quoted |
| No alternative, discount uncertain, D4 equipment, not served, special price | Escalate to Sales with a summary and a starting draft |
| `on_hold` customer with a complete request | Draft for approval, including the payment reminder, flagged to Sales |

If one quotation part meets both an escalation trigger and a clarification trigger, it escalates, and the starting draft lists the missing details as well.

## 12. Never
- Quote a guessed product or version.
- Read a price from anywhere other than the catalogue table.
- Do arithmetic in the model.
- Promise a discount, a delivery date or stock that the tables do not support.
- Treat the quote as an order.
