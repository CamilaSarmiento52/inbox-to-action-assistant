# Quotation expectations and SOP review

Reviewed by Codex (OpenAI), 2026-10-08. Scope: all 40 records in `quotation.jsonl`, both records in `mixed_quotation.jsonl`, quotation SOP v0.2, generator, pricing/customer tables, evaluation criteria and shared policies.

Status: review complete; corrections below are proposed. Fixtures, generator and policy decisions have not been changed. Creator model provenance was not independently established for this set, so this report alone does not confirm the different-family review requirement.

## Findings requiring correction

| Priority | Location | Finding and suggested correction |
| --- | --- | --- |
| High | `mixed_quotation.jsonl`, line 2, E-MIX-QT-001 | “Whats the price of the MC-12 Plus” supplies no quantity. The fixture assumes one unit and a final £538.80 total, with `draft_for_approval`. SOP §2 requires quantity and EVALUATION prohibits final totals for incomplete requests. Show the £449.00 unit price, ask how many, set quotation and overall routes to `ask_for_clarification`, and remove delivery/VAT/final total pending quantity. Technical answer and its attachment remain supported. Make the correction in the generator. |
| Medium | `quotation.jsonl`, line 26, E-QUO-026 | Neither quantity nor version is given. Clarification route and per-unit version options are appropriate, but the required reply asks only which version. Add an explicit quantity question, matching SOP §§2, 11. One-unit option prices should be labelled as unit prices rather than extracted requested quantities. |
| Medium | Communication policy §3 versus quotation SOP §§3, 6, 11 | Shared policy says a requested product that cannot be found always escalates. E-QUO-025 (superseded MC-10), 031 (Large gloves), and 032 (25 ml pipettes) instead clarify with replacements/alternatives under the quotation SOP. Record an explicit quotation exception in shared policy, or change the applicable fixture routes. Do not leave both instructions unconditional. |
| Medium | `data/README.md`, discounts section; quotation SOP §5 | The data README says any case not matching a discount rule goes to a person. The table has no rule for consumables below 10 units or a single equipment unit, yet many fixtures correctly draft those routine quotes with zero discount. Document those as explicit no-discount cases; reserve escalation for uncertain applicability and `refer_to_sales`. |
| Medium | Quotation SOP §10, items 2 and 6 | Reply requirements unconditionally call for delivery/VAT/total and an outstanding amount. These conflict with §§7, 11 for incomplete requests and §8 for missing/zero on-hold balances. Make totals conditional on a complete, resolved request with served destination, and balances conditional on a recorded positive amount. |
| Medium | `mixed_quotation.jsonl`, line 1, E-MIX-QC-001 | Complaint says goods were received Monday, but does not say when cracked caps were noticed. Returns policy §5 requires that detail. Add “asks when the damage was noticed” to the complaint reply requirements. The complaint escalation and quotation arithmetic are supported. Monday receipt alone does not establish the issue's discovery date or eligibility for a remedy. |

## Clarifications and coverage gaps

- Define penny rounding in SOP §3: a concrete rule consistent with the generator is Decimal arithmetic, each line discount rounded half up to two decimal places, sum rounded net lines, add delivery, then round VAT half up to two decimal places. Existing numbers are consistent with this; the policy does not currently specify it.
- Define route precedence within a quotation containing both an escalation trigger and missing information. Evaluation defines precedence across parts; SOP §11's rows can overlap within one part. A proposed rule is escalation with all missing details listed in the starting draft.
- Explicitly say that an alternative offer asks the customer to confirm acceptance before any final quote. E-QUO-031/032 use clarification routes but their required reply points do not explicitly demand that question.
- Add a missing-quantity-only case. E-MIX-QT-001 can provide this after correction. Add an actual order/PO counterpart to the price-only boundary cases in the classification set when order fixtures are created.
- Add executable fixtures for C-06 (on-hold balance missing or zero), known customer with no delivery postcode, unknown sender at an existing customer's organisation, multiple equipment SKUs with one unit each, and a basket mixing resolved and unresolved lines.
- Add exact free-delivery-threshold cases, all PH district boundaries (16/17/50/51), and case-unit discount quantities. Current fixtures test representative zones and a discount-induced threshold crossing, but not all boundaries.
- E-QUO-019 is held out but its expected prospect update depends on tuning case E-QUO-018 being processed first. Supply an explicit initial prospect state for isolated held-out runs, or preserve chronological setup without using the setup email for scoring. File order is not chronological; the documented `received_at` order matters.
- The SOP is marked current but effective 2026-10-09, and its decision annotations are dated tomorrow relative to this review. Fixtures deliberately target the current snapshot and are themselves dated 2026-10-09, so this is not an arithmetic failure. Clarify whether it is a planned policy or correct the metadata if unintended.
- The shared reply rubric in EVALUATION names documentation and technical SOPs as examples; explicitly include quotation SOP §10 so greetings, validity, account address and payment terms do not rely on selective case-level requirements.

## Checks and supported outcomes

- Parsed all 42 JSONL records. Single-category counts match the README: 24 drafts, 10 clarifications, 5 escalations, 1 duplicate; 29 tuning and 11 held out. Mixed records currently have one escalation and one draft, both tuning.
- Independently recomputed every stored quotation line price, gross total, discount rule/percentage/amount, net goods total, delivery charge, VAT and final total from CSV sources using Decimal arithmetic. All passed. This validates arithmetic for the encoded inputs; it does not validate quantities inferred from the email, as E-MIX-QT-001 demonstrates.
- Verified quotation account IDs, statuses and payment terms against sender contact records, account-postcode fallback, postcode-zone lookups, and final/nonfinal total fields. All passed.
- Verified label sets equal part labels and overall routes follow the most restrictive part route, with the duplicate exception. All passed structurally; the semantic route correction above remains necessary.
- Verified unknown-sender prospect add/update expectations in received-time order. E-QUO-019 correctly updates the prospect introduced by E-QUO-018. E-QUO-040 links to the earlier E-QUO-001 rather than generating a second reply.
- Confirmed every Q-01–Q-09 and D-01–D-11 trap is represented, plus C-05, C-07, C-08 and C-09. C-06 remains acknowledged but unimplemented.
- Confirmed E-QUO-007's discounted goods total £239.15 attracts Zone 2 delivery £12.95 despite the undiscounted £250.40 basket; E-QUO-011 correctly uses email postcode PH33, Zone 3, instead of the account postcode.
- Confirmed E-QUO-013/014 preserve requested packs and offer cheaper cases as suggestions; E-QUO-016 uses the recorded £1,842.60 balance; E-QUO-036/038 preserve list/table pricing while escalating discretionary discounts; E-QUO-039 ignores the injected 50% discount and flags/escalates.
- Confirmed MC-12 Plus PCR-strip compatibility is supported by `NLS-DOC-MC12-TECH-R1`, “Compatible tubes”: Plus-only 8-place rotor for 0.2 ml strips. Mixed cases preserve both requested parts and require a combined reply.

All remaining single-category expectations are supported by the quotation SOP and records, subject to the shared-policy conflicts above. These are source/fixture checks; no classifier, quotation agent, retrieval system or email-sending runtime was exercised. No fixture regeneration was performed.

## Creator response (2026-10-08)

The emails were created by Claude (Anthropic) and reviewed by Codex (OpenAI), so the review meets the different-family requirement in EVALUATION.md. All fixture changes were made in `tools/generate_quotation_emails.py` and regenerated.

**Applied**
- E-MIX-QT-001: no quantity, so the quotation part asks how many; unit price shown, no total; overall route ask for clarification.
- E-QUO-026: asks version and quantity; prices labelled as unit prices.
- E-QUO-031, 032: the reply asks whether the customer wants a quote for the alternative. Quotation SOP §6 says so.
- E-MIX-QC-001: the complaint part asks when the damage was noticed.
- Communication policy §3: exception for labelled alternatives offered under quotation SOP §3 and §6; escalation only when none exists. This records the alternative-product decision of 2026-10-05.
- Data README: quantities below every discount rule simply get no discount; a person decides only on `refer_to_sales` or uncertainty.
- Quotation SOP: §3 rounding rule (matches the generator); §10 totals only for complete, served requests and the balance only when positive; §11 escalation wins within one part, with missing details listed.
- SOP metadata: effective date and decision dates corrected to 2026-10-08 (they were wrongly set a day ahead).
- EVALUATION.md: the shared reply rubric includes quotation SOP §10.
- Held-out dependency: E-QUO-019 moved to tuning and E-QUO-015 to held out; the README states that held-out runs replay all emails in `received_at` order.

**Added by user decision: six edge cases (E-QUO-041 to 046)**
Exact free-delivery threshold (new trap D-12); PH16 as the Zone 2 boundary counterpart of PH33; discount tier counted in cases; two equipment items of different SKUs (no D4); a basket with one resolved and one unresolved line (new field `pending_options`); an unknown sender at a customer's domain (C-03, C-04). The set is now 46 emails. These six have not yet been reviewed.

**Not done**
- C-06 still needs a test fixture with an on-hold account and no balance.
- An order/PO counterpart to the price-only boundary cases belongs to the order-placement emails, still to be written.

## Follow-up review: six added emails (2026-10-08)

Reviewed E-QUO-041 through E-QUO-046 against the updated quotation SOP, catalogue, discount and delivery tables, customer/contact records, generator and fixture schema. All six have supported routes and correct stored arithmetic. One reply requirement needs a wording correction; no route or numeric corrections are needed.

| Email | Result | Evidence |
| --- | --- | --- |
| E-QUO-041 | Supported | 4 × £18.50 + 3 × £42.00 = £200.00, exactly the Zone 1 free-delivery threshold. Email postcode LS1 overrides account BT7. VAT £40.00; total £240.00. No discount applies to either line. |
| E-QUO-042 | Supported; narrow postcode wording | PH16 matches Zone 2; 10 glove boxes receive D1: £69.00 − £3.45 = £65.55. Delivery £12.95, VAT £15.70, total £94.20. C-1015 is prepay. However, “unlike PH17 and above” overstates the table: Zone 3 covers PH17–PH50 only. Replace with “unlike PH17–PH50, which are Zone 3”; PH51 is unmatched under these tables. Make the correction in the generator and regenerate the fixtures. |
| E-QUO-043 | Supported | 10 cases are 10 units of sale, not 50 discount-counted boxes. £1,050.00 less D1 £52.50 = £997.50; free Zone 1 delivery; VAT £199.50; total £1,197.00. |
| E-QUO-044 | Supported | One MC-12 Standard and one VM-10 Basic are different SKUs with one unit each, so D4 does not apply. Goods £368.00, free Zone 1 delivery, VAT £73.60, total £441.60. |
| E-QUO-045 | Supported | “An MC-12” supplies a singular quantity but no version. Quote the resolved tubes line at £72.00; keep Standard £289.00 and Plus £449.00 as separate pending options, not basket lines. Clarify version and withhold delivery/VAT/final total. C-1010 is on hold: recorded £1,842.60 reminder and Sales notification are correct. Version inclusions and the Finance reference are covered by the shared SOP rubric. |
| E-QUO-046 | Supported | Sender address is absent from contacts despite matching an existing customer domain. Neither Brackenridge account/address/terms may be inferred. Two pipette packs cost £84.00; ask for postcode and withhold total. Add a prospect and notify Sales. This tests the quotation-specific unknown-sender rule; it does not replace order/invoice verification tests for C-03 or an account-selection test for C-04. |

### Verification of the creator response

Confirmed the previously requested quantity questions, alternative-acceptance questions, complaint discovery-time question, shared-policy exception, no-discount documentation, rounding rule, conditional reply totals/balances, within-part route precedence, corrected SOP dates and quotation reply rubric are present. E-MIX-QT-001 now clarifies quantity without a final total. The split swap and chronological replay instructions are also present.

The creator response identifies Claude (Anthropic) as the creator. On that recorded provenance, this Codex (OpenAI) follow-up meets the documented different-family review requirement; this supersedes the original provenance caveat for this review record.

Independently recalculated all six new emails' line prices, discount rules/percentages/amounts, net goods, delivery, VAT and totals using Decimal half-up rounding. Checked customer IDs/status/payment terms, pending option prices, on-hold balance/Sales notification, and label/route consistency. Postcode zone boundaries were checked against the CSV rows. No runtime agent or classifier was exercised. The generator and JSONL files remain unchanged by this follow-up review. E-QUO-042's wording correction remains proposed; C-06 and the order/PO counterpart remain outstanding as recorded above.


## Creator response to the follow-up (2026-10-08)

E-QUO-042: the reply requirement now reads "unlike PH17 to PH50, which are Zone 3", changed in the generator and regenerated. No other changes. Still outstanding: the C-06 fixture and the order/PO counterpart.
