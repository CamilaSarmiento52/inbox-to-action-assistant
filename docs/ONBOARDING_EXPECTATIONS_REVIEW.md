# Onboarding expectations review

Reviewed by Codex (OpenAI), 2026-10-09.

## Result and scope

Reviewed all 25 records in `data/emails/onboarding.jsonl`, `docs/sops/onboarding-sop.md`, `data/customers.csv`, `data/customer_contacts.csv`, and the nine prospect quotation cases in `quotation.jsonl`. Also checked the quotation SOP, empty starting `prospects.csv`, delivery zones, catalogue/discount/delivery tables, evaluation and communication rules, and the two related order-to-onboarding handoffs. The mixed quotation file contains no prospect cases.

**All 25 onboarding routes are supported. Corrections are needed in cross-category state, contact-row expectations and some retrieval references.** The seed CSVs pass integrity checks. All nine prospect quotations pass independent price/discount/totals checks, but E-QUO-019 conflicts with the newly introduced onboarding timeline, and E-QUO-034 loses the supplied invalid postcode.

## Actionable findings

### 1. [P1] E-QUO-019 still treats Mira as a prospect after her account is created

E-QUO-018 at 12:50 adds Mira as a prospect. E-ONB-011 at 13:30 creates Hollins Biotech as C-1025, adds Mira as K-2043 with orders/invoices authorisation, and converts the prospect. E-QUO-019 arrives at 15:10 but expects `customer_id: null`, `account_status: unknown_sender`, `payment_terms: null`, `prospect: update`, and describes her as still unknown.

Under chronological shared state, E-QUO-019 should use C-1025, `active`, and `prepay`; its prospect must stay converted. Its prices and £92.94 total are unchanged. Update the quotation expectation and generator, or move the repeat quotation before the onboarding email if the intended trap is still an unknown prospect updating `last_seen`. Keep a separate later quotation to test conversion if the repeat is moved. The original quotation review predates this new account-creation case; its approval of E-QUO-019 as a prospect update is superseded for the combined timeline.

Define/replay one chronological customer/contact/prospect state across the relevant categories. Loading every quotation before onboarding merely to establish prospects would incorrectly process E-QUO-019 before its actual receipt time.

### 2. [P2] Onboarding generator replays IDs, but not created customer/contact state

`tools/generate_onboarding_emails.py` checks duplicate keys against the initial `CUST` (line 38) and account changes against initial `CONT` (line 73). The final chronological pass assigns IDs but does not add created records to these lookup tables. Two independent requests with the same new VAT number are therefore both marked `created`; a later change from a newly created contact is marked `unknown_sender`.

Isolated calls reproduced both behaviours. Current E-ONB-019 is explicitly linked to E-ONB-001, so it does not test identifier-based duplicate detection against a prior insertion. Replay actual customer/contact creation before evaluating later requests, alongside prospect conversions. Add a different sender/request using a VAT or registration number inserted earlier, plus a change from a newly created contact. This is a fixture-generator limitation; the application runtime was not exercised.

### 3. [P2] New contact expectations omit the CSV's `role` field

All 12 contact rows expected from the 11 created accounts omit `role`, although `customer_contacts.csv` includes that column. `authorised_for` expresses permissions and is separate from the job/department role. Several emails supply a role: Hannah is Lab Manager, D. Okafor is Science Technician, Grace is Lab Manager and Clare is Lab Technician.

Define how the new workflow records `role`: preserve the stated job/department role and use an empty string when absent, or explicitly document another policy. Include the column in expected contact rows so completeness/correctness checks cover the full CSV schema. Do not invent roles for senders who give none. The proposed customer rows otherwise include every customer CSV column.

### 4. [P2] E-QUO-034 discards the postcode it is supposed to reject

Sam supplies `ZZ9 4QT`, but the generator calls `quote()` without passing it, so `postcode_used` and `postcode_source` are both null. This makes the structured expectation resemble a missing-postcode case rather than the intended unmatched-postcode trap.

Pass `ZZ9 4QT` into the unfinished quotation: preserve it as `postcode_used`, set `postcode_source: email`, keep `zone: null`, and withhold delivery/VAT/total. The clarification route and £13.80 goods price are correct.

### 5. [P2] Some onboarding retrieval labels omit the section deciding the outcome

The default passages are only SOP §2 and §3. Add §4 for E-ONB-006, 007, 008 and 022 (duplicate/similar-name decisions), and §5 for E-ONB-014, 015 and 021 (not-served, unmatched postcode and destination-zone handling). These fields are retrieval ground truth, so they should identify the specific consulted sections as well as the general procedure. The expected routes remain supported.

## Onboarding outcomes checked

| Cases | Result |
| --- | --- |
| 001–003 | Complete applications create separate active/prepay accounts. VAT spaces are removed; registration-only Fernside is accepted. Quayside retains its distinct invoice postcode and uses its delivery postcode for the zone. |
| 004, 005, 020 | Missing details clarify with no partial account. The sender's contact metadata is available; asking for customer type is not required. |
| 006, 007, 022 | Existing VAT or registration number stops creation and escalates to Sales without account-existence disclosure. Duplicate keys resolve to C-1008, C-1003 and C-1012 respectively. E-ONB-022's different VAT does not override its matching registration number. |
| 008 | Distinct Brackenridge VAT/registration numbers support a separate C-1022 account, flagged `similar_name` against C-1007 and notified to Sales. |
| 009 | Account starts on prepay; the 30-day request is flagged/notified to Finance and never granted automatically. |
| 010 | Rhys and the invoices-only accounts contact are added. Bethan is not added without her email; asking for it does not block creation of the complete account and other contacts under SOP §3. |
| 011, 013 | Mira and Piotr convert their existing prospects after account creation. E-QUO-018/020 precede their respective onboarding emails. |
| 012 | Westmoor's details follow E-ORD-027 at 14:20. Creation at 14:30 does not confirm the order held by Sales. |
| 014–017 | Isle of Man escalates without creation; unknown postcode and malformed VAT clarify; injected credit/terms instructions escalate to Sales without creation or granting terms. |
| 018 | Forwarded details are extracted; Clare remains the sender contact. The forwarded Finance address is not automatically given invoice permission without a stated authorisation role. |
| 019 | Resend links to E-ONB-001 and creates no second account. |
| 021 | NI712345 fits the stated format; Belfast is served in Zone 3. |
| 023–025 | All account changes escalate to Sales without automatic writes. Priya and Isla are seeded contacts of the respective accounts; the Kestrel-domain lookalike sender is unknown and receives no account disclosure. |

Created account IDs are C-1019–C-1029, contacts K-2036–K-2047, assigned correctly in receipt order rather than file order. All proposed accounts are active, prepay, with zero outstanding balance and the received date. E-ONB-010 creates two contacts; the other creations add one each. Extra contact roles remain restricted as stated.

## Customer CSV checks

18 seeded customers and 35 seeded contacts. Customer IDs, contact IDs and contact emails are unique. Every contact references an existing customer; permission tokens are orders/invoices after trimming whitespace. Nonempty VAT and registration keys are unique. Every customer's postcode maps to its recorded zone: 12 in Zone 1, 3 in Zone 2, 3 in Zone 3. The new IDs do not collide with the seed records. Existing 30-day/prepay terms, on-hold status and contact permissions were treated as recorded facts, not overwritten by new-account defaults.

## Prospect quotation checks

Reviewed E-QUO-005, 018, 019, 020, 033, 034, 037, 039 and 046. Complete quotations quote normally; missing/unmatched destinations clarify; Guernsey escalates as not served; the injected discount escalates with only the table discount applied. E-QUO-046's unknown address at an existing company does not inherit that company's address or account terms. All required Sales notifications are present.

Every line price, tier discount, line discount rounding, goods sum, available delivery charge, VAT and final total was independently checked against the source tables. E-QUO-033 correctly stops at £74 goods; E-QUO-034 at £13.80; E-QUO-046 at £84. Prospect creation does not create an account. The two conversion references point to genuinely earlier quotations. Piotr's E-ORD-035 at 16:20 still precedes E-ONB-013 at 16:40, so its no-account expectation is temporally consistent.

## Coverage and limits

25 onboarding emails: 18 tuning, 7 held out; 11 creation drafts, 5 clarifications, 8 escalations and 1 duplicate email. All N-01–N-14 traps occur. Useful additional cases are a duplicate of an earlier account insertion, a change from a newly created contact, a quote after conversion, a missing delivery postcode, and a record-creation failure that must not produce a success reply. Specify atomic handling of customer/contact creation and prospect conversion if the runtime is expected to guarantee no partial records on a write failure.

This is a documentation, fixture and seed-data review. Isolated read-only helper execution and independent consistency/arithmetic checks were used; no application pipeline, actual account creation, message sending or CSV mutation was performed. Only this review document and the emails README review status were changed.

## Creator response (2026-10-09)

The emails were created by Claude (Anthropic) and reviewed by Codex (OpenAI), so the review meets the different-family requirement in EVALUATION.md. All fixture changes were made in the generators and regenerated.

1. **E-QUO-019 and the shared timeline.** E-QUO-019 tests a prospect writing again, so it now arrives at 13:10, after E-QUO-018 (12:50) and before E-ONB-011 creates Mira's account (13:30); its expectations are otherwise unchanged. A new quote, E-QUO-047 at 17:10, tests the converted state: customer C-1025, active, prepay, the account's postcode, no prospect change. The quotation generator now reads the accounts the onboarding emails create and uses one only if it was created before the quote arrived. The emails README defines one time-ordered customer, contact and prospect state across files, and the generation order.
2. **Created state replayed.** The onboarding generator now handles emails in `received_at` order, adding each created customer and contact before the next email; IDs are assigned at creation. Outcomes of the 25 reviewed emails are unchanged (compared). New cases: E-ONB-027, a second sender with the VAT number E-ONB-001 created, is a duplicate of C-1019; E-ONB-028, a change from Tom Ellery, is verified against C-1023, created by E-ONB-009.
3. **Contact `role`.** Every expected contact row has `role`: the stated job or department (Lab Manager, Science Technician, Lab Technician, Accounts) or empty. SOP §3 says so, and never guessed.
4. **E-QUO-034.** `postcode_used` ZZ9 4QT, `postcode_source` email, zone null, no total.
5. **Retrieval labels.** §4 added to E-ONB-006, 007, 008 and 022; §5 to E-ONB-014, 015 and 021.

Also: E-ONB-026 (an address with no postcode, asked for); SOP §3 states that the customer row, contacts and prospect conversion are written together or not at all. Trap N-15 added. Not added: a record-creation failure case, which needs the runtime to simulate a failed write.


## Follow-up review — E-ONB-026 to 028, E-QUO-047 and creator response (2026-10-09)

**Result: all four new emails pass. All five previous findings are resolved for the current fixtures. No new actionable fixture findings.**

| Email | Review result |
| --- | --- |
| E-ONB-026 | The application supplies the organisation, valid VAT number, sender and invoice/delivery address, but no postcode. `missing_fields: ["postcode"]`, clarification and no account/prospect write are correct. No zone or account ID is invented. |
| E-ONB-027 | Harlow's VAT GB431772908 matches C-1019, created by E-ONB-001 at 09:00. This different sender arrives at 15:30. Escalate to Sales with `duplicate_account`, `duplicate_of: C-1019` and no new record or contact. The reply must not confirm account existence to the unverified sender. |
| E-ONB-028 | Tom became Pennine's contact through E-ONB-009 at 11:40. His 16:00 request is therefore verified against C-1023. Escalate the address addition to Sales without changing the account or promising the addition is complete. |
| E-QUO-047 | Mira's 17:10 quote correctly uses C-1025, active/prepay, created by E-ONB-011 at 13:30. No postcode is supplied, so use the account's LS6 2AB and name its recorded delivery address in the reply. No prospect insertion/update is expected. Ten conical-tube packs at £14.40 = £144; D1 5% discount £7.20 leaves £136.80. Below the Zone 1 free-delivery threshold, add £9.95; £146.75 × 20% = £29.35 VAT; total £176.10. Draft for approval. |

### Previous findings verified

1. **Timeline:** E-QUO-019 now arrives at 13:10, between E-QUO-018 at 12:50 and account creation at 13:30. Its unknown-prospect update is supported again. E-QUO-047 tests the later converted state. The quotation helper's time gate gives an unknown sender before creation and the new account afterwards when the receipt time is supplied. The README now specifies chronological state across categories and generation order.
2. **Created account/contact replay:** onboarding expectations are evaluated in receipt order, and created customers and contacts are added to the lookup state immediately. Isolated execution reproduced the prior-creation duplicate check and the newly created contact's verification. Missing-postcode clarification did not consume an account/contact ID.
3. **Contact roles:** every one of the 12 expected new contacts now includes the complete seeded contact CSV column set. The stated Lab Manager, Science Technician, Lab Technician and Accounts roles are preserved; other roles are empty. SOP §3 explicitly distinguishes the job/department role from authorisation.
4. **Unmatched postcode:** E-QUO-034 preserves ZZ9 4QT with source `email`, null zone and no total. Its clarification and £13.80 goods price remain correct.
5. **Retrieval references:** the previously listed duplicate/similar-name cases now include SOP §4; destination cases include §5. The new emails also cite the sections deciding their outcomes.

The SOP now explicitly requires customer/contact creation and prospect conversion to commit together or not at all, and later requests to see earlier creations. This resolves the documented atomicity requirement. Actual rollback on a failed write remains untested; the creator correctly identifies that a runtime failure simulation has not been added. That is a validation limit, not a failure of these four emails.

### Checks and limits

Read the four complete emails, the creator response, updated SOP, relevant generator functions and README. Verified the receipt-time dependencies, side-effect expectations, complete contact columns and all requested retrieval-label corrections. Executed isolated onboarding and quotation helpers without regenerating data, and checked E-QUO-047's calculation against the catalogue, D1 discount and delivery tables. No application pipeline, transaction rollback, actual account creation or external reply was exercised.

Counts confirmed: onboarding 28 emails (20 tuning, 8 held out), with 11 creation drafts, 6 clarifications, 10 escalations and 1 linked duplicate. Quotations 47 emails (34 tuning, 13 held out), with 29 drafts, 12 clarifications, 5 escalations and 1 linked duplicate. The README's old quotation count of 28 drafts was updated to 29. Only review documentation and README were edited; fixtures, generators, SOPs and CSVs remain unchanged by this review.
