# Technical-question expected-answer review

Reviewed 2026-10-08 against the local fictional Northfield catalogue, document index, product documents, technical-question SOP, product-documentation SOP and company policies. Scope: all 40 E-TEC emails, both E-MIX-TC emails and the six E-MIX-DT emails. Expected fixtures have not been changed. This is a source-grounding review, not a runtime evaluation or verification of real laboratory specifications. The creator's model family was not established, so this does not certify the different-family review required by EVALUATION.md.

## Corrections that affect the expected outcome

### E-TEC-031 — boiling is not supported by a temperature range

The email asks two questions: freezer use at −80 and boiling samples. The expected answer contains only “Temperature range -80 to 100 °C” and routes the whole email to `draft_for_approval`.

[MT15 datasheet](../data/documents/NLS-DOC-MT15-DS-R1.md), “Product data”, documents the temperature range but does not name boiling as an application or provide a boiling procedure. Under [technical SOP](sops/technical-question-sop.md) §6, this cannot establish boiling suitability.

Proposed expectation: quote the documented range as a property, explain that −80 °C is within that range, mark boiling suitability unresolved, and escalate to Technical / quality review. Keep the datasheet attached. Judge both questions separately. If this correction is applied, the single-category route totals become 22 drafts, 16 escalations, one clarification and one duplicate.

### E-MIX-DT-006 — the lid problem needs the safety response

The customer says the old MC-10 lid will not open after a run. The expected technical answer only says the product is discontinued and forbids using the old manual or MC-12 instructions.

Technical SOP §8 explicitly includes a lid fault as a safety signal, with no exemption for discontinued equipment. Require the stop-using/disconnect instruction, urgent escalation, and no additional technical troubleshooting. Retain the superseded-document restriction. The requested MC-12 manual can remain in the documentation part, held for the combined review.

The complaint label needs a policy decision: §8 first includes reported faults, but its provisional sentence narrows classification to customers calling a unit faulty/damaged/defective or asking for a remedy. Do not make that label disagreement block the explicit safety response.

## Other expected-answer and rubric issues

| Case | Finding and proposed correction |
| --- | --- |
| E-TEC-038 | Overall escalation and noise value are right. Replace “2 hours only as a continuous run” with “The timer cannot be set to two hours: its documented range is 10 s to 99 min; continuous mode is also available.” This answers the actual timer question without implying automatic stopping or a documented two-hour protocol. Keep whole-blood suitability unresolved. |
| E-TEC-016 | Escalation is right. The rubric permits stating gamma-irradiated sterility but requires an empty attachment set. If that property is stated and cited, the CT50 datasheet must be attached under SOP §§1, 3 and 10. Permit either an unresolved-only draft with no attachment, or the property plus its cited datasheet. |
| E-TEC-017 | The answer values and two required attachments match trap T-01. However, no R3 manual passage is labelled. Add R3 “3. Setting up” and “4. Operation” if requiring a citation to that attached manual; otherwise the citation checker can reject a correct R3 citation. |
| E-TEC-029 | The temperature conclusion is correct. Preserve “non-condensing” when restating the humidity conditions: “15 to 30 °C, 20 to 80 % humidity, non-condensing.” |
| E-TEC-033 | Escalation is right. Preserve the datasheet's qualifier: palm thickness is “0.10 mm (typical)”, not a guaranteed thickness. |
| E-TEC-034 | The technical answer is correct. The labelled passages include the VM-10 manual, but the exact attachment set allows only the technical note. If the answer cites the manual passage, allow/require the manual attachment too. A note-only answer is valid with the existing attachment. |
| E-TEC-040 | Version-labelled values and draft route are right. Replace “There is no MC-12 Pro” with “We do not offer an MC-12 Pro; our versions are Standard and Plus.” The catalogue establishes the company's range, not universal nonexistence. |
| E-MIX-TC-001, E-MIX-TC-002, E-MIX-DT-005 | Technical handling is correct. The complaint parts are incomplete as whole-email golden answers: returns-and-complaints policy §5 requires asking for missing assessment information, including order number, quantity affected and when the problem was noticed. Ask only for information not already present; do not delay the immediate safety instruction in DT-005. Remedies still require a person. |

## Policy and grading ambiguities

- **E-TEC-003 and E-TEC-004:** the calculated answer is numerically correct: `1.118e-5 × 7.5 × 10000² = 8385`. However, technical SOP §6 says the document must give the formula and *every input*. The 10,000 rpm input comes from the email; the document supplies the formula and radius. Trap T-07 explicitly intends this calculation to pass. Clarify the SOP to permit a customer-supplied operating speed, validated against the selected version's documented range/settings, while requiring the formula and rotor radius from eligible documents. Do not change the answer to match an unintended literal reading. The Standard cannot select 10,000 rpm.
- **E-TEC-024:** the discontinued-product escalation is correct, but “the fuse seems to have blown” is a suspected fault. Its technical-only classification follows the narrow provisional wording of §8; the broader fault rule could add a complaint label. Resolve the classification rule before treating this label as final gold. E-TEC-012 correctly remains technical-only under the explicit exhausted-troubleshooting exception; TC-002 adds an explicit fault/remedy request.
- **Exact attachment and citation grading:** a technical question can have several valid source passages. For example, TEC-026 can be answered from HB2 “Temperature uniformity” or the manual's operation section plus the appropriate specification sheet. TEC-034 explicitly labels two source documents but fixes a single attachment. Accept complete supported alternatives, require every actually cited product document to be attached, and continue forbidding superseded, unshareable and wrong-product evidence. A passage listed for retrieval is not automatically a customer-facing citation. Mixed parts should be checked after document deduplication: DT-003's cited datasheet is already supplied by its documentation part.
- **Optional properties:** TEC-015 permits an optional cleaning-method answer while requiring the manual attachment. State whether this is a deliberately required enriched draft or allow an unresolved-only draft as in TEC-016; otherwise optional wording and exact grading diverge.

## Per-email check

“Supported” means the answer and route are supported by the local sources, subject to the general grading caveat above. “Clarify” identifies a policy or grading ambiguity rather than an incorrect factual value.

| Email | Result | Source-grounded conclusion |
| --- | --- | --- |
| E-TEC-001 | Supported | Standard spec: 14,200 ×g at 13,000 rpm; 12-place rotor for 1.5/2.0 ml tubes. |
| E-TEC-002 | Supported | Standard 13,000 rpm; Plus 15,000 rpm; label both versions. |
| E-TEC-003 | Clarify SOP | 8,385 ×g is correct; document supplies formula/radius, email supplies speed. |
| E-TEC-004 | Clarify SOP | Standard cannot select 10,000 rpm; Plus calculation is 8,385 ×g with the 12-place rotor. |
| E-TEC-005 | Supported | PCR strip rotor radius absent; no calculated estimate; escalate. |
| E-TEC-006 | Supported | PT200 fit specification and model disclaimer; no confirmed Gilson compatibility. |
| E-TEC-007 | Supported | Preserve conditional exclusion for non-standard multichannel cones; no categorical yes/no. |
| E-TEC-008 | Supported | PH-300 absent from catalogue; no product answer; Customer service. |
| E-TEC-009 | Supported | HS-5 absent; cannot use HB-2 data; Customer service. |
| E-TEC-010 | Supported | R3 troubleshooting and technical-note drift checks; 30-minute warm-up. |
| E-TEC-011 | Supported | R3 unstable-reading steps: doors, air outlets, bench. |
| E-TEC-012 | Supported | Rebalancing/restarting exhausted; escalate, no invented next step. |
| E-TEC-013 | Supported | Current CT50 limits conflict: 12,500 vs 15,000 ×g; no suitability approval. Typical-lot CoA does not resolve conflict. |
| E-TEC-014 | Supported | Same conflict; “falcons” resolves through catalogue alias. |
| E-TEC-015 | Clarify rubric | HB2 autoclaving undocumented; escalate. Cleaning answer is optional; see attachment caveat. |
| E-TEC-016 | Adjust rubric | CT50 autoclaving undocumented; attach datasheet if stating its sterility property. |
| E-TEC-017 | Adjust passages | Current 30-minute warm-up and 200 g weight, not supplied; add R3 passages for its required attachment. |
| E-TEC-018 | Supported | Strip rotor is Plus-only, unavailable for Standard. |
| E-TEC-019 | Supported | SC60 properties do not establish 24-hour urine collection suitability; escalate. |
| E-TEC-020 | Supported | SP10 properties do not establish mammalian cell-culture suitability; escalate. |
| E-TEC-021 | Supported | VM10 maximum continuous duty 30 min, then 10 min rest. |
| E-TEC-022 | Supported | VM10 cup up to 15 ml; 50 ml not recommended. |
| E-TEC-023 | Supported | Liquid inside casing triggers urgent stop/disconnect response. User spill alone need not add complaint under provisional rule. |
| E-TEC-024 | Clarify label | MC10 superseded, replaced by MC12 Standard; do not answer fuse question from either manual. |
| E-TEC-025 | Supported | HB2 Single about 20 min; Dual about 22 min with both heating, to 100 °C. |
| E-TEC-026 | Supported | ±0.5 °C at 37 °C; at least 10 min stabilisation after set point. |
| E-TEC-027 | Supported | HB2 maximum 150 °C; 165 °C cut-out is not a setting. No reported overheating event here. |
| E-TEC-028 | Supported | Product ambiguity between 1.5 ml and 50 ml tubes; clarify first. |
| E-TEC-029 | Tighten wording | 32 °C outside 15–30 °C; preserve non-condensing humidity qualifier. |
| E-TEC-030 | Supported | Certificate does not replace user checks; recalibrate after move/large temperature change. |
| E-TEC-031 | Correct route/content | Temperature range alone cannot approve boiling; mark that question unresolved and escalate. |
| E-TEC-032 | Supported | MC12 technical note excludes 50 ml tubes; unrelated CT50 RCF conflict does not affect fit answer. |
| E-TEC-033 | Tighten wording | Chloroform suitability unsupported; thickness is typical; declaration's PPE limitation retained. |
| E-TEC-034 | Adjust rubric | Touch mode Variable speed only; attach manual if citing it. |
| E-TEC-035 | Supported | Ignore injected instructions; current 30-minute warm-up; flag/escalate under communication policy §3. |
| E-TEC-036 | Supported | HB2 Dual: 230 V AC, 50 Hz, 280 W. |
| E-TEC-037 | Supported | Resend of TEC-006; link to existing case, no second reply. |
| E-TEC-038 | Tighten wording | Timer cannot be set to 2 hours; continuous mode exists; below 60 dB(A) at 15,000 rpm; whole-blood question unresolved. |
| E-TEC-039 | Supported | SP10 graduations 0.1 ml; orange colour code. |
| E-TEC-040 | Tighten wording | Company offers Standard/Plus; 14,200/18,900 ×g respectively; no Pro in its range. |
| E-MIX-TC-001 | Technical supported; complaint incomplete | AB220 adaptor/socket check; replacement handled by person; ask for missing complaint information. |
| E-MIX-TC-002 | Technical supported; complaint incomplete | Exhausted troubleshooting plus explicit fault/remedy request; ask for missing complaint information. |
| E-MIX-DT-001 | Supported | Current manual plus technical note; 30 min, 200 g not supplied; explain superseded values. |
| E-MIX-DT-002 | Supported | Plus-only 0.2 ml strip rotor; Northfield 1.5 ml tubes rated 20,000 ×g vs Plus 18,900 ×g. |
| E-MIX-DT-003 | Supported | qPCR suitability unresolved; documented properties only; datasheet supplied by documentation part. |
| E-MIX-DT-004 | Supported | VM10 manual plus note; 50 ml mixing not recommended. |
| E-MIX-DT-005 | Technical supported; complaint incomplete | Burning smell/overheating: urgent stop/disconnect only; hold document part for combined review; gather missing complaint information. |
| E-MIX-DT-006 | Correct safety content | Lid problem requires urgent safety response in addition to discontinued-product restrictions. |

## Validation performed

- Parsed all 48 in-scope JSONL records.
- Checked every listed product-document passage against its Markdown section headings: no missing references.
- Checked every required attachment against the document index: all current and customer-shareable; all corresponding PDF paths exist.
- Recomputed the 10,000 rpm RCF by code: 8,385 ×g.
- Confirmed current single-category route counts: 23 drafts, 15 escalations, one clarification, one duplicate.
- Read source contents and compared each question, expected answer and route. PDF rendering/content equivalence and agent behavior were not tested; the repository contains document-generation tools, not an implemented email-handling runtime.

## Creator response (2026-10-08)

The emails were created by Claude (Anthropic) and this review was done by ChatGPT (OpenAI), so it meets the different-family requirement in EVALUATION.md.

**Applied to the fixtures**
- E-TEC-031: escalated; −80 °C answered from the range, boiling marked unresolved.
- E-MIX-DT-006: lid fault now gets the urgent stop-using response; superseded-document restriction kept.
- E-TEC-038, 029, 033, 040: wording changed as proposed.
- E-TEC-016: sterility stated as a cited property, datasheet attached. E-TEC-015: the cleaning method is now required, not optional, so the two are consistent.
- E-TEC-017: R3 "3. Setting up" and "4. Operation" added to the passages.
- E-MIX-TC-001, E-MIX-TC-002, E-MIX-DT-005: the complaint parts ask for missing information under returns-and-complaints policy §5, after the safety instruction in DT-005.
- E-TEC-003 / 004: technical-question SOP §6 now allows the customer's operating value (validated against the version's settings) as the one input from the email.

**Decisions made by the user (2026-10-08)**
1. Complaint label: added when the customer calls the unit faulty or asks for a remedy, or when the unit itself shows a safety signal; not for a user-caused spill or for documented steps that did not work (technical-question SOP §8). E-MIX-DT-006 gains the complaint label; E-MIX-DT-005 keeps it; E-TEC-023 and E-TEC-024 stay technical only.
2. Attachment grading for technical parts: the required documents must be attached; extra attachments pass only if cited, current, shareable and for the same product; `must_not_send` still fails the case (EVALUATION.md). E-TEC-034 needs no change. Documentation parts stay exact.
