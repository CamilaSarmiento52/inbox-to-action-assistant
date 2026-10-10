# Classification expectations review

Reviewed by Codex (OpenAI) on 2026-10-10 against `CLASSIFICATION_GUIDE.md`, version 1.0.

## Result

All 340 emails across all 15 JSONL files were read, including their subjects and bodies. **338 label sets are supported; 2 require clarification of the equipment complaint boundary.** The review concerns labels, not a fresh validation of routes, document selection, extraction or calculations. Fixtures, generators and the guide were left unchanged.

The complete per-email ledger is [CLASSIFICATION_LABEL_AUDIT.md](CLASSIFICATION_LABEL_AUDIT.md). All 340 IDs are unique. All labels use the eight exact allowed names; no set is empty or repeats a label; Other is never combined. Each non-duplicate email's part labels match its parent labels, and every duplicate email retains its original label set. There are 35 multi-label emails.

## Finding

### P2 — Clarify when an equipment complaint also needs a technical label

Affected: `mixed_technical.jsonl`, lines 1–2, E-MIX-TC-001 and E-MIX-TC-002.

- **E-MIX-TC-001:** the AB-220 “won't switch on at all”; the request is “Please could you send a replacement?”
- **E-MIX-TC-002:** the MC-12 stops after rebalancing/restarting; “I think the unit is faulty – can you arrange a repair or a replacement?”

Both expect `Technical suitability question` plus `Return / quality complaint`. The complaint label is supported. Neither asks how to use the unit, what to check or what else to try. Under §4.7, which explicitly excludes “a fault, damage or remedy request”, and G-1's action-based rule, the technical label is not independently supported. B-5 says equipment gets the complaint label “as well”, but does not say whether this presupposes an actual technical question or whether every equipment remedy request gets both labels.

The distinction matters for consistency: E-CMP-024 also describes malfunction, explicitly calls the VM-10 faulty and asks for replacement, but correctly expects complaint only under §4.7. E-CMP-012 and E-CMP-016 similarly ask for equipment remedies and expect complaint only. Safety mixed cases that ask “what should we do?” do have a technical question, and their labels are supported.

**Recommended resolution:** state in B-5 that adding complaint presupposes an independently identifiable technical question. To preserve these two mixed tests, add a real troubleshooting question to each email, such as asking what checks can be made before repair/replacement. Alternatively, retain their current text and remove the technical label and technical part, updating the generator and mixed coverage counts. This is a review recommendation; no source edits were made.

Until resolved, §6's unconditional “No label in the 340 test emails changes” is not fully demonstrated.

## Coverage observations

No email directly tests B-3's newly decided stock/availability/lead-time-only classification or B-8's invoice withholding/dispute because goods are defective. Existing price quotes do not isolate B-3, and E-MIX-IC-001's invoice-copy request beside a complaint does not test B-8's causal dispute. This confirms the guide's coverage note. Add those tests separately; no existing labels need changing for these rules.

Other boundaries are supported: price versus supply instruction; catalogue versus price list; document delivery versus interpretation; missing versus damaged items; delivered cancellations; account versus per-order addresses; prospect quotations; forwarded requests; resends; understood foreign languages; assistant injection and unrelated content. File names are not treated as categories: E-CMP-026 is quotation, E-ORD-040 complaint, and five cases in `other.jsonl` belong to identifiable business categories.

## Creator response (2026-10-10)

**P2 accepted; fixed with the recommended resolution.** The labels stay and each email now contains the question they assumed:

- **E-MIX-TC-001:** "Is there anything we should check first? If not, please could you send a replacement?" The technical part's expectations (the documented adaptor and socket check, cited; not urgent) now answer an actual question.
- **E-MIX-TC-002:** "Is there anything else we can try? If not, … can you arrange a repair or a replacement?" The technical part still escalates, because the documented steps are already tried.
- **Guide v1.1, B-5:** a fault report or remedy request with no question about the product is complaint only. When the email also asks a technical question, it gets the technical label, and the complaint label is added as well under (a) or (b). Technical SOP §8 and trap T-16 say the same. This is consistent with E-CMP-012, E-CMP-016 and E-CMP-024, which stay complaint only.
- All five emails with both labels (CT-001, DT-005, DT-006, TC-001, TC-002) now contain a question.

`mixed_technical.jsonl` has no generator: like the documentation and technical sets, it was written by hand, so the two bodies and notes were edited in the file. No label, route or part changed. Guide §6 now records the two text changes.

**Coverage observation:** agreed. B-3 (availability only) and B-8 (invoice withheld because of the goods) still need test emails; they will be added as a separate step.

**Coverage added (2026-10-10, not yet reviewed):**
- **B-3:** E-QUO-048 asks whether "the HB-2" is in stock (both versions stocked, so no version question; account address used). E-QUO-049 asks for the AB-220 Certified lead time to Inverness from an unknown sender (made to order, Zone 3, prospect recorded). Both are `Quotation request` only, with an `availability` block and no price.
- **B-8:** E-MIX-CI-001 withholds INV-10398-1 over torn gloves. E-MIX-CI-002 withholds INV-10426-1 over a VM-10 fault and asks no technical question, so it also exercises the B-5 clarification. Both are `Invoice / payment question` + `Return / quality complaint`.
- Traps Q-10 and M-13. The existing 340 emails are byte-identical after regeneration.

## Follow-up review — four new emails (2026-10-10)

Reviewed against guide v1.1, the updated quotation/invoice/technical SOPs, delivery policy, catalogue, delivery tables, customer/contact records, order lines, shipments, invoice records and the relevant generator definitions. **All four label sets and expected outcomes are supported; no new actionable findings.**

| Email | Labels | Expected handling verified |
| --- | --- | --- |
| E-QUO-048 | Quotation request | B-3: stock and hypothetical delivery only. Both HB-2 versions are stocked; Ruth belongs to active C-1002, NR4 7TJ, Zone 1. The before-1pm working-day dispatch condition and next-working-day delivery are estimates. No price, quantity or version clarification needed for this availability-only request. |
| E-QUO-049 | Quotation request | B-3: AB-220 Certified is not stocked; about 3 working days to dispatch, then 3–5 working days to Zone 3 (IV2). Unknown sender: prospect added and Sales notified, with no assumed account terms. No price requested. |
| E-MIX-CI-001 | Invoice / payment question + Return / quality complaint | B-8: payment withheld over six defective glove boxes. Finance handles the dispute; Technical / quality review handles replacement. Sender matches C-1003; SO-10398 contains 20 boxes, delivered 2026-09-29: 10 calendar days to the email date, within 14 days. Lot requested; no remedy promised. No invoice copy was requested. |
| E-MIX-CI-002 | Invoice / payment question + Return / quality complaint | B-8 and clarified B-5: fault plus repair/replacement and withheld payment, without a technical question. Sender matches C-1016; SO-10426 contains one VM-10 Variable speed, delivered 2026-10-02: 7 calendar days, within 14 days. Verified record supplies serial VM1V-26-0219, so no redundant request. No safety signal, technical label or invoice-copy attachment. |

For E-QUO-048, the email arrives after the cutoff; its conditional before-1pm rule is supported, but must not be turned into a promise of dispatch that evening. The policy does not define an after-cutoff date, so the expected refusal to promise a delivery date remains appropriate.

The two mixed cases correctly escalate both parts to their respective owners and propose one reply with no attachments. Invoice references and complaints point to the same customer's orders. Finance decides the payment point; a person decides the remedy.

**Previous P2 resolved:** guide B-5 now explicitly requires a technical question for the additional technical label. E-MIX-TC-001 now asks what to check first; E-MIX-TC-002 asks what else to try. Their existing two-label sets are now supported. The B-3 and B-8 coverage gaps are closed by the four new emails, with one tuning and one held-out example per rule.

Current inventory: **344 unique emails, 37 multi-label emails; all 344 label sets supported** using the original full audit plus this follow-up. Label uniqueness, nonempty sets, Other exclusivity and parent/part agreement were rechecked across all 344. This is fixture and source review, not a runtime evaluation of the assistant. Test emails, SOPs and generators were not modified by this review.

## Creator response to the follow-up (2026-10-10)

Agreed; no findings to fix. On the after-cutoff note for E-QUO-048, the expectation is now explicit: the reply must not say an order placed now would go today, because the email arrived after 1pm. No other email changed. All 344 label sets are supported, and the classification guide is final at v1.1.
