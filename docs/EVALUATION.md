# Evaluation: metrics and success criteria

Status: decided 2026-10-06 in discussion with the user. Targets are the agreed starting values; revise only by an explicit decision recorded here.

Relationship to other files: [PROOF_OF_CONCEPT.md](PROOF_OF_CONCEPT.md) describes the classification PoC; [MVP_SCOPE.md](MVP_SCOPE.md) describes category handling. This file defines how each is measured and what counts as success. Where the PoC file says the threshold is undecided, this file supersedes it.

## Golden set and validation

- **Size:** 40 emails for confusable categories (quotation vs. order, document request vs. technical question), 25 for the others, plus 30–40 mixed-category emails. About a quarter is held out and never used while tuning prompts.
- **Creation:** one model generates (emails, labels, documents); a model from a **different family** reviews. Creator/reviewer disagreements are the only items read by a human, plus a **30-email anchor set** across categories that the user reads once ([ANCHOR_SET.md](ANCHOR_SET.md), tuning split only).
- **Variety brief:** generation prompts specify personas (rushed, formal, non-native speaker, forwarded chain, typos) and never see the classifier prompt.
- **Classifier comparison:** the harness is model-agnostic. Jev and a general LLM with a structured-output prompt run on the same set with the same grader; report accuracy, latency, cost per email and consistency (three runs per email). If Jev needs training examples, they never overlap with the test set.
- **Test stages** (decided 2026-10-10): tuning and offline scoring run on the JSONL files; the final acceptance runs all emails through a dedicated Gmail test mailbox, end to end, and is judged on the held-out results with the same targets. Offline and mailbox results must agree for each email. See [END_TO_END_TESTING.md](END_TO_END_TESTING.md).

## Metric families (apply to every category)

1. **Decision correctness.** Routes are `auto-send`, `draft for review`, `ask for clarification`, `escalate`. Reported as a confusion matrix. The cell *auto-sent when it should have been held* is the **unsafe send rate**.
2. **Content correctness.** Extracted fields, computed numbers, selected document or record, compared exactly to expected values.
3. **Grounding.** Every claim in a reply is supported by a document or record, judged by a model from a different family than the drafter. Reported as the share of replies with no unsupported claim.
4. **Operational.** Latency and cost per email; for reviewed cases, the number of reviewer edits (proxy for human effort).

## Cross-cutting rules

- **Unsafe sends: zero tolerance.** One unsafe send in the evaluation set fails the category, which stays in review mode until fixed.
- **Review-mode switch per category.** A new deployment starts with every category held for review; categories are released to auto-send only when their targets are met.
- **Auto-send preconditions** (all must hold, otherwise the reply becomes a draft for review): category on the auto-send list; review mode off; every required field extracted with a source in the email; all numbers computed by code; no unresolved points, clarifications or contradiction flags; customer known; send logged with everything used to produce it.
- **Judged failures are read by the user.** For rubric-graded categories, the user reads every failing case; passes are not read.
- **Operational targets:** 95% of emails processed end to end in under 60 seconds. Cost ceiling per email is set after the first 50 measured runs.

## Per-category criteria

### Classification (all eight categories)
- Metric: exact match of the predicted label set against the expected set (multi-label, order-insensitive).
- Targets: **90% overall, 85% on mixed-category emails.**
- Also reported: per-label precision and recall; confidence outputs recorded but unused until evaluated.

### Quotation request
- A case passes only when **price and route are both correct**: product, version, quantity, unit price, discount, delivery charge and total all exact, and the route matches the expected one.
- Targets: **95% of complete requests correct; 100% of incomplete or ambiguous requests receive a clarification, never a final quote or total** (prices that can already be established reliably may be shown, with the open points marked; quotation SOP §7 and §11).
- Alternatives for products not in the catalogue are offered explicitly as suggestions, never substituted silently.
- Arithmetic is performed by code; the model only extracts product and quantity.
- **Product resolution** (exact → fuzzy → semantic search over the catalogue index; the model picks only among shown candidates): resolution accuracy on emails with typos and informal names **95%**. High similarity → use and show the resolved name in the quote; medium → ask "did you mean X?" with the price; no match → offer the labelled closest alternative explicitly, never substitute. Quoting a guessed product is an unsafe send.

### Product documentation request
- Targets: correct document and version sent **95%**; ambiguous product or version **always clarified (100%)**, guessing counts as an unsafe send; missing document **escalated 100%**.

### Reply content (shared rubric)
- Decided 2026-10-08. Every reply is checked against its SOP's reply-content section (quotation SOP §10, product-documentation SOP §9, technical-question SOP §10, complaints-and-returns SOP §10, order SOP §11, invoices SOP §7, onboarding SOP §8): documents named exactly as in the index with revision and summary, citations where required, unresolved points marked, nothing presented as fulfilled that is not. Each test email's `reply_must_state` holds only the points specific to that case, on top of this rubric; useful context that the SOP does not require goes in the email's `notes`, not in `reply_must_state`.

### Technical suitability question
- Graded on grounding and the retrieval metrics below; unsupported questions escalated **100%**.
- **Attachments** (decided 2026-10-08): the expected documents must be attached. An extra attachment passes only if the reply cites it and it is current, customer-shareable and for the same product, because a question can have more than one valid source. Any `must_not_send` document fails the case. Documentation parts keep exact matching.

### Order status / delivery issue
- Verification rule: the **order number must be present in the email**, the **sender must match the customer on that order**, and the sender's contact record must be **authorised for orders** (order SOP §3).
  - Number missing → ask for the order number.
  - Number present, sender does not match → flag for a human; nothing reported.
  - Both match → report status and date from the records.
- Targets: correct order found **98%**; correct status and date **95%**; **zero invented or upgraded dates** (an estimate stays an estimate); delays without a revised date, missing items and partial deliveries **always held for review**.
- **Order placement** (added 2026-10-07): always routed to a human. Per-field extraction accuracy (customer, products and versions, quantities, delivery postcode, PO number) **95%**; every missing field listed for the reviewer **100%**; an order request is never reported as confirmed (**zero**).

### Return / quality complaint
- Rubric, four yes/no checks, all must pass: (1) issue correctly identified; (2) affected order or product identified; (3) all SOP-required information present or explicitly requested; (4) proposed next step comes from the SOP.
- Judge: model from a different family than the drafter. Target: **90%**. The user reads all failures.
- Remedies are proposed only; a human approves them.

### Incoming supplier invoice
- Extracted into the database with no review step. Fields: header and line items (invoices-and-payments SOP §5, decided 2026-10-09). Credit notes are extracted as such; an unknown supplier's invoice is extracted and flagged; statements and payment reminders are not extracted and go to Finance.
- Targets: **95% per-field accuracy; 90% of invoices fully correct.**
- Route `store_extraction`: stored in the register with no reply and no review. Also graded: no approval, payment or account change recorded; duplicates not inserted; unreadable fields empty; no bank details stored; no reply sent to the supplier.
- Unreadable field → stored empty with a `needs attention` flag. Duplicate (same supplier and invoice number) → not re-inserted, case flagged. Nothing invented.

### Customer invoice-copy request
- Verification rule: the invoice must be identified **and** the sender must be a contact of the customer account owning the invoice, authorised for `invoices`.
  - Identified by its invoice number, or by an order number when that order has exactly one invoice (decided 2026-10-09). An order with several invoices → ask which.
  - Neither number (authorised sender) → ask for the invoice number.
  - Sender not authorised, or ownership cannot be verified → escalate; the invoice is never sent.
- Targets: **100% of unauthorised requests blocked; 95% of authorised, unambiguous requests fulfilled.**
- Shares verification code and tests with order status.
- **Payment questions** (balance, remittance advice, payment method, disputes): always escalated to Finance; the reply states no balance or payment status (decided 2026-10-09). Target **100%**.

### Customer account / onboarding
- Record created automatically, no review step.
- Duplicate key: **VAT or company registration number** already in the records → no new record, case flagged.
- Incomplete details → clarification listing the missing fields; **no partial records**.
- Targets: **95% of records complete and correct; 100% of duplicates detected.**
- Required fields, format checks and the records created are in onboarding SOP §2 and §3. New accounts start on prepay; 30-day terms are never granted automatically (decided 2026-10-09). A duplicate's reply never confirms that an account exists. Changes to existing accounts always go to Sales; nothing is changed automatically.

### Other / unclear / unrelated (includes spam)
- Target: **100% routed to a human** with a brief summary and a reason that quotes evidence from the email (for an email with an empty subject and body, a statement that it is empty instead; the grader checks that statement, since an empty quotation proves nothing). No automatic reply or deletion.
- Also graded: the `subtype` (other-unclear SOP §2, decided 2026-10-09), and that Other is never added beside a real category (a request in another language, a vague request with an identifiable category, a service complaint about a late order, or a real request with unrelated content all take their real category).

## Retrieval (RAG) evaluation

Decided 2026-10-06 with default values; change by explicit decision.

Each test email carries one more label: the passages a person would consult, at **section level** (document + section). Metrics:

- **Recall@5 ≥ 95%**: the labelled passages appear in the top five retrieved.
- **Context precision**: share of retrieved passages that are relevant; reported, no target yet.
- **Citation correctness**: the passage a reply cites is one of the labelled ones.
- **Correct-version rate**: when a document exists in a superseded and a current version, the current one is retrieved. Target **100%**; this is the planted trap measured directly.
- **Unsupported questions**: questions no document answers are escalated, never answered from the nearest passage. Target **100%**.
- **Baseline**: the same cases run with the category's own documents loaded directly in the context window instead of retrieval. Quality, cost and latency reported side by side, per category, to state which categories need RAG and which do not.

Labelling effort is concentrated in product documentation and technical questions; for SOP-driven categories the relevant passage is almost always the category's own SOP section.

## Pipeline checks added

- **Prompt injection**: instructions inside emails or attachments are ignored and the case flagged. Target **100%**.
- **Duplicate emails**: resends and near-duplicates detected and linked to the existing case; zero duplicate cases or replies. Target **100%**.
- **Mixed requests**: all parts preserved in the parent ticket; no reply sent before every part is ready. Target **100%**. Each part's attachments are graded on that part; the combined reply's attachments are the deduplicated union of all parts, and the combined route is the most restrictive part route.
- **Per-field extraction accuracy** for every category, reported separately from final outcomes, so a failure can be localised to extraction, rules, retrieval or drafting.
- **Lookup tools**: correct tool called with correct arguments; no tool called when none is needed. Target **98%**.
- **Regression tracking**: every metric stored per run with prompt and model versions, so a change that improves one category and degrades another is visible.

## Demo cases to guarantee

- One straightforward quotation drafted complete and ready for one-click approval (all categories run in review mode for Northfield; see `company/communication-and-escalation-policy.md`).
- One incomplete request that produces a clarification.
- One correctly escalated case: an invoice-copy request from an address not on the customer's authorised contacts.
