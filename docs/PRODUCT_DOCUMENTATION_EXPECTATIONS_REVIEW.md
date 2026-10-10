# Product-documentation expected-answer review

Reviewed 2026-10-08 by Codex (OpenAI). Scope: all 40 emails in `product_documentation.jsonl` and the documentation parts of all seven emails in `mixed_documentation.jsonl`. Sources: the current local catalogue, product-document index, document-type synonyms, product-documentation SOP, communication policy, test traps and email schema. This reviews the fictional project's rules, not external laboratory requirements.

**Result:** no incorrect document selection or escalation owner found. Most expectations are supported as written. One exact-attachment requirement is stricter than the SOP, one route needs clearer justification, and three cases omit specific reply requirements. The expected-answer files have not been changed.

## Findings and proposed corrections

### 1. E-DOC-010: attaching the sample certificate is optional under the policy

The customer wants their own AB-220 Certified certificate, identified by serial number. Escalation to Technical / quality review is correct, and the sample is the only shareable certificate in the index. However, `send_documents` requires that sample to be attached exactly.

[Product-documentation SOP §5](sops/product-documentation-sop.md) says “We can send only the sample”; [trap P-04](TEST_TRAPS.md) explicitly says “May send the sample”. Neither requires attaching it. A draft that identifies the unit-specific request as unresolved and escalates without an irrelevant sample is also policy-compliant.

Proposed grading: accept either no attachment or `NLS-DOC-AB220-CERT-SAMPLE-R1`. If attached, require an explicit sample label and say it is not the certificate for serial 22C-04417. In either case require the quality-team handoff and no claim that the requested certificate has been supplied. Alternatively, change the SOP to require a sample if that is the intended product behavior; the existing fixture alone should not decide that policy.

### 2. E-DOC-028: clarify why the catalogue request asks a question

The customer names the VM-10. The synonym table and SOP §3 prescribe saying that no printed catalogue is issued and offering the product's documents. That content and the suggested document set are correct; this is not a missing-document escalation.

The fixture routes to `ask_for_clarification`, but its required reply contains only the statement and offer, not a question. SOP §10 does not explicitly assign a route to this catalogue-offer situation. A complete offer could reasonably be a `draft_for_approval`.

Proposed resolution: if keeping `ask_for_clarification`, require “Which would you like: the manual, the Basic specification sheet, or the technical note?” and record that catalogue offers requiring a document choice use this route. Otherwise use `draft_for_approval` for a complete offer. Do not force a version question before offering the shared manual/technical note; label the specification sheet as Basic-only.

### 3. E-DOC-031: add the instruction that the superseded revision should no longer be used

Sending R3 instead of the requested 2025/R2 manual is correct. The expected reply names R2 and says R3 replaces it, but omits the explicit “should no longer be used” requirement in SOP §7. Add that point, as already done for E-DOC-030. No route or attachment change.

### 4. E-DOC-038: explicitly label the certificate as typical-lot

The specimen-container datasheet and certificate are correct. The certificate title in the index is “Specimen containers 60 ml certificate of analysis (typical lot)”; the file states that its results are not a guarantee for any particular lot.

The empty `reply_must_state` is sufficient only if SOP §9's exact-title requirement is independently enforced. Add “The certificate of analysis is for a typical lot, not a certificate for the customer's own lot” to make the qualifier testable, consistently with E-DOC-024 and E-DOC-034. No escalation is required because the email does not request a particular lot.

### 5. E-DOC-039: include how Standard and Plus differ

Clarifying the version before sending a specification sheet is correct. SOP §4 also requires one line on how the options differ. The fixture currently requires only “Ask Standard or Plus”.

Add a short catalogue-grounded distinction: Standard has fixed speed settings; Plus has variable speed, a digital display and a second rotor. No price or technical suitability advice is needed. No route change.

## General grading and documentation notes

- **Common reply requirements:** SOP §9 requires the exact document title, index summary and revision, plus greeting/closing and clear unresolved items. Several cases intentionally have empty `reply_must_state` lists. Treat the case-specific lists as additions to a shared SOP rubric; otherwise incomplete replies can pass. Conversely, DOC-001 and DOC-012 require explanatory statements about shared coverage that are true and useful but not explicitly mandatory in the SOP. Decide whether they are strict editorial requirements or optional context; the key behavior is attaching the shared document without an unnecessary version/pack question.
- **Missing-document wording:** DOC-007, DOC-008 and DOC-025 say a document “does not exist”. Prefer “We do not have a specification sheet for the VM-10 Variable speed”, “We do not have an SDS for these specimen containers”, and “We do not have a certificate for the HB-2”. The index establishes what Northfield holds. For CE certificates, brochures and IQ/OQ, the stronger “we do not issue/produce” wording is explicitly supported by the synonym table.
- **Lot-certificate wording conflict:** the synonym-table notes say “offer” a typical-lot certificate for a lot-specific request; SOP §5 and P-11 say “send”. DOC-016 follows the SOP correctly. Align the synonym notes to “send, clearly labelled as typical, and escalate” to avoid a future exact-attachment disagreement. This is distinct from the optional unit-certificate sample in DOC-010.
- **“Everything” and version specificity:** DOC-014 correctly sends both HB-2 specification sheets under the explicit “everything” exception in SOP §4. The later prose saying a version-specific document is “never sent while the version is unknown” is too absolute. Add “unless the customer requests all documents, in which case label each version”. Do not change DOC-014 to clarification.
- **Mixed requests:** grade documentation attachments on their case part and the final attachments as the deduplicated union of all parts. A technical citation can legitimately add an attachment beyond the documentation part's exact set. Hold the combined reply for the most restrictive route. The current DT-006 fixture already contains the urgent lid-fault response added after the technical review; that earlier finding is resolved in the current data.
- **README bookkeeping:** `mixed_documentation.jsonl` now contains six document + technical emails, **two** also with complaint parts (DT-005 and DT-006), plus one document + quotation email. The README still says one also has a complaint. Its product-documentation review status should link to this review and indicate that the findings above are pending reconciliation, rather than marking every expectation approved.
- **Time semantics:** some test emails precede the SOP's 2026-10-08 effective date. This review treats the fixtures as tests of the current policy snapshot. If historical policy-at-receipt behavior is intended, dates/policy versions need alignment.

## Case-by-case results

Document IDs below omit the common `NLS-DOC-` prefix for readability. “Supported” assesses the case-specific selection, route and content, subject to the shared grading notes above. The mixed rows assess the documentation part and its overall holding route, not a new full review of every technical or quotation requirement.

| Email | Result | Expected behavior checked against sources |
| --- | --- | --- |
| E-DOC-001 | Supported | MC12-MAN-R1 covers Standard and Plus; no version question. SOP §4. |
| E-DOC-002 | Supported | Current AB220-MAN-R3; never R2. SOP §§4, 7. |
| E-DOC-003 | Supported | “Instructions” maps to manual; HB2-MAN-R1 current and shared. Unknown sender is allowed. SOP §§2–4. |
| E-DOC-004 | Supported | MC12-SPEC-PLS-R1 only. Mentioning a validation folder is not requesting IQ/OQ. SOP §4. |
| E-DOC-005 | Supported | Ask Standard/Certified and distinguish them; attach neither spec until clarified. Catalogue and SOP §4. |
| E-DOC-006 | Supported | Ask Single/Dual, with a distinction. Purchase interest without a price request does not require a quotation part. SOP §4. |
| E-DOC-007 | Supported; wording | Variable-speed spec missing; Customer service; offer shared VM10 manual/note, never substitute Basic sheet. SOP §5. |
| E-DOC-008 | Supported; wording | No SC60 SDS in index; Customer service; list datasheet and typical-lot CoA. SOP §5. |
| E-DOC-009 | Supported | IQ/OQ not produced; Technical / quality review; list MC12 Plus manual/spec/note. SOP §5. |
| E-DOC-010 | Adjust attachment rubric | Unit-specific certificate unresolved; Technical / quality review; sample permitted, not mandatory. SOP §5 and P-04. |
| E-DOC-011 | Supported | MC10 manual superseded/unshareable; Customer service; offer MC12 manual only as replacement-product suggestion. SOP §7. |
| E-DOC-012 | Supported | PT200-DS-R1 covers box and case; no pack clarification. SOP §4. |
| E-DOC-013 | Supported | “tubs 1,5ml”, bag of 500 resolves to MT15; MT15-DS-R1. SOP §§3, 4. |
| E-DOC-014 | Supported | All four HB2 documents: manual, Single and Dual specs, technical note; label versions. SOP §4 “everything” exception. |
| E-DOC-015 | Supported | All four Certified-applicable AB220 documents: R3 manual, Certified spec, note, sample certificate. Exclude Standard spec and R2. SOP §§4, 5. |
| E-DOC-016 | Supported | PT200 typical-lot CoA clearly not lot 25L0912; escalate lot-specific request to Technical / quality review. SOP §5. |
| E-DOC-017 | Supported | pH meter not in catalogue; no documentation or reasonable functional alternative; Customer service. SOP §6. |
| E-DOC-018 | Supported | CE certificate not issued; Customer service; list all HB2 documents as suggestions, no invented certificate. SOP §5. |
| E-DOC-019 | Supported | Brochure not produced; Customer service; offer VM10 manual, Basic spec and note, each correctly named. SOP §5. |
| E-DOC-020 | Supported | “Centrifuge tubes” ambiguous between MT15 and CT50; ask which, attach neither. SOP §3. |
| E-DOC-021 | Supported | Quick-start synonym maps to MC12 manual; explain no separate guide and setup steps in manual. Synonym table and SOP §3. |
| E-DOC-022 | Supported | Application-note synonym maps to VM10 technical note; accurately name what is supplied. SOP §3. |
| E-DOC-023 | Supported | Explicit sample request: AB220 sample certificate, labelled sample; no unit-specific escalation. SOP §§3.1, 5. |
| E-DOC-024 | Supported | SP10 has one certificate type: typical-lot CoA; name it; no unnecessary clarification. SOP §3.1. |
| E-DOC-025 | Supported; wording | HB2 has no certificate type; Customer service; list Single-applicable manual/spec/note. SOP §§3.1, 5. |
| E-DOC-026 | Supported | “Technical documentation” selects MC12 Standard spec plus shared technical note, not all manuals. SOP §3.1. |
| E-DOC-027 | Supported | Ambiguous “doc” does not establish declaration of conformity; ask among gloves datasheet/DoC/SDS. SOP §3.1. |
| E-DOC-028 | Clarify route | No printed catalogue; offer VM10 documents. Clarification route needs an explicit document-choice question/policy rule. SOP §3 and catalogue synonym. |
| E-DOC-029 | Supported | Large not offered; offer Medium datasheet labelled Medium, do not attach as fulfillment for Large; draft. SOP §6.1. |
| E-DOC-030 | Supported | Requested R2 replaced with R3; explicitly say R2 should no longer be used. SOP §7. |
| E-DOC-031 | Add reply requirement | 2025 revision is R2; send R3; add “R2 should no longer be used”. SOP §7. |
| E-DOC-032 | Supported | MSDS maps to safety_data_sheet; GL-SDS-R1. SOP §3. |
| E-DOC-033 | Supported | Explicit declaration request; GL-DOC-R1. SOP §4. |
| E-DOC-034 | Supported | CT50 typical-lot CoA, labelled typical; no lot-specific request and no technical RCF answer requested. SOP §§4, 9. |
| E-DOC-035 | Supported | MC12 manual only in starting draft; ignore/flag injection, escalate to Customer service; never attach MC10/R2. Communication policy §§3, 4. |
| E-DOC-036 | Supported | Forwarded request is for HB2 technical note itself, not an answer about uniformity; HB2-TECH-R1. SOP §§1, 3. |
| E-DOC-037 | Supported | Same sender chasing DOC-001; link to existing case, no duplicate reply. EVALUATION duplicate rule. |
| E-DOC-038 | Add reply requirement | SC60 datasheet plus typical-lot CoA; one documentation label; explicitly preserve typical-lot qualifier. SOP §§4, 8, 9. |
| E-DOC-039 | Add reply requirement | Equipment “datasheet” maps to spec sheet; ask Standard/Plus and add one line of differences. SOP §§3, 4. |
| E-DOC-040 | Supported | Only Basic spec exists but version unknown: clarify Basic/Variable, do not send Basic spec prematurely. SOP §4. |
| E-MIX-DT-001 | Supported | Documentation part supplies AB220-MAN-R3; technical note comes from technical part; combined draft. |
| E-MIX-DT-002 | Supported | Documentation part supplies MC12 Plus spec; technical part adds note; combined draft. |
| E-MIX-DT-003 | Supported | PT200 datasheet selected; whole case escalates for unresolved qPCR suitability; no separate document reply. |
| E-MIX-DT-004 | Supported | VM10 manual selected; technical part adds compatibility note; combined draft. |
| E-MIX-DT-005 | Supported | Requested HB2 note remains in documentation part; combined case held for urgent safety/complaint review. |
| E-MIX-DT-006 | Supported | Requested MC12 manual for new units is valid; never use it as MC10 troubleshooting advice; case held for urgent lid-fault review. |
| E-MIX-DQ-001 | Supported documentation part | CT50 datasheet selected; price-list part routes to quotation; overall clarification for missing quote information. |

## Checks performed

- Parsed all 47 JSONL records and reviewed each customer request against its expected documentation outcome.
- Verified all attached and suggested document IDs against the index: each exists, is current and customer-shareable, and has both Markdown and PDF files on disk.
- Verified forbidden IDs exist and do not overlap required attachments.
- Verified all documentation-part SOP/policy section references exist.
- Verified part labels and overall route aggregation, including the duplicate exception.
- Confirmed DOC-037 follows DOC-001 on the same date from the same email address.
- Confirmed all P-01 through P-24 trap IDs occur in the documentation and mixed set.
- Single-category totals: 21 drafts, 7 clarifications, 11 escalations, 1 duplicate; 29 tuning and 11 held-out emails.

These are fixture/source checks. No agent runtime was exercised, and PDF content/rendering equivalence was not tested. Review findings remain proposed until reconciled with the fixtures and policies.

## Creator response (2026-10-08)

The emails were created by Claude (Anthropic) and reviewed by Codex (OpenAI), so the review meets the different-family requirement in EVALUATION.md.

**Applied**
- E-DOC-031: "R2 should no longer be used" added. E-DOC-038: typical-lot qualifier added. E-DOC-039: one line on how Standard and Plus differ added.
- E-DOC-007, 008, 025: "we do not have" instead of "does not exist".
- `document_type_synonyms.csv`: lot-specific certificate notes say "send, labelled as typical, and escalate", matching SOP §5.
- Product-documentation SOP §4: a version-specific document may be sent without knowing the version when the customer asks for every document, labelled by version (as in E-DOC-014).
- Emails README: two mixed emails have a complaint part; the review is linked; fixtures test the current policy snapshot.
- EVALUATION.md: mixed-request attachments are the deduplicated union of all parts, at the most restrictive route.

**Decided by the user**
1. E-DOC-010: the labelled sample certificate is always attached when a customer asks for their own unit's certificate, and the request is escalated (SOP §5, P-04). Fixture unchanged.
2. E-DOC-028: a catalogue request asks which of the product's documents the customer wants, naming each; route ask for clarification (SOP §3, §10; synonyms note). Fixture's required reply now includes the question.
3. Reply grading: a shared rubric from each SOP's reply-content section applies to every reply; `reply_must_state` holds only case-specific points (EVALUATION.md). The context lines in E-DOC-001 and E-DOC-012 moved to `notes`.
