# MVP scope

Status: high-level scope defined; acceptance criteria set in [EVALUATION.md](EVALUATION.md); quotation (v0.2), product-documentation (v0.2), technical-question (v0.2) and complaints-and-returns (v0.2) order-status-and-placement (v0.2) and invoices-and-payments (v0.2), onboarding (v0.1) and other-unclear (v0.1) SOPs drafted, one per category; product-documentation and technical-question test emails generated and reviewed; quotation test emails generated and reviewed; complaint test emails and order records generated and reviewed; order-status test emails generated and reviewed; invoice records and test emails generated and reviewed; onboarding test emails generated and reviewed; Other test emails generated and reviewed; 35 mixed-category emails (`data/emails/mixed.jsonl` reviewed, including E-MIX-DT-007); classification guide written (`CLASSIFICATION_GUIDE.md`). Updated 2026-10-10.

This file records the agreed high-level handling across the eight categories. It defines the broad MVP described in the planning discussion, with classification and quotations as the first implementation increment. It is not itself a company SOP; the detailed procedures live in `sops/`. Remaining behavior decisions and documentation tasks are identified below; explicitly marked suggestions are not agreed implementation choices.

## Relationship to the proof of concept

The [classification PoC](PROOF_OF_CONCEPT.md) evaluates all eight categories, including mixed-request emails, using deterministic exact-match grading against human-reviewed labels. Jev and a general LLM with a structured-output prompt are compared on the same set. The success targets (90% exact match overall, 85% on mixed emails) are set in [EVALUATION.md](EVALUATION.md).

The MVP builds on classification to handle the requests described below using company records and SOPs. Classification covers all eight categories from the start; handling capabilities can be implemented incrementally, beginning with quotations.

## Intended value

- Reduce human handling time.
- Provide faster, useful customer responses, particularly for sales enquiries.
- Reduce mistakes and missed requests.
- Reduce the reviewer's cognitive load.
- Improve the customer experience.

Quantified targets for correctness and processing time are in [EVALUATION.md](EVALUATION.md); a baseline for human handling time is still to be measured. Both human handling time and customer response time matter; speed alone is insufficient.

## Cross-category direction

- **Intake** (decided 2026-10-10): the solution reads email from a Gmail mailbox. The JSONL test emails are used to build and tune it; the final test loads them into a dedicated Gmail test mailbox and runs the whole solution end to end ([END_TO_END_TESTING.md](END_TO_END_TESTING.md)).
- Classification does not automatically mean routing to a department.
- Routine responses may be sent directly when the relevant SOP permits them. The earlier proposal that every external reply requires approval has been superseded by category- and action-specific handling. For the Northfield project all categories run in review mode: a person approves every external reply (see `company/communication-and-escalation-policy.md`); auto-send stays off until a category is released by an explicit decision.
- Company documentation and records must support replies and proposed actions.
- Human handoff depends on the request and applicable procedure; complaints initially require human review of the proposed resolution.
- For cases requiring human review, provide a starting draft and clearly identify unresolved points. Do not present a partial answer as complete.
- Keep the review summary brief: what was received, what was checked or done, what is proposed, and what needs attention. Distinguish completed actions from proposed ones.
- Preserve all requests in mixed emails. For quotation plus complaint, handle each part through its relevant process and bring the results together for the same email/ticket. Wait until both parts are ready, including any required human review, and send one combined reply rather than sending the quotation first.
- The category-specific human-review triggers below are agreed. Confidence-based thresholds and general fallbacks for unhandled failures remain undecided. Confidence alone does not establish completeness or correctness.

## Agreed category handling

| Category | Current direction | Status |
| --- | --- | --- |
| Quotation request | Answer the requested quotation using product prices, applicable discounts, delivery rules, and the quotation SOP. | First response capability selected; SOP drafted: `sops/quotation-sop.md`. |
| Product documentation request | Identify the product/version and send the matching document directly; clarify ambiguity; flag missing documents and hand off to a human. | SOP drafted: `sops/product-documentation-sop.md`. |
| Order status / delivery issue / order placement | Report shipment status directly; apologize for recorded delays and provide the recorded delivery date. Prepare drafts for human review for delays without a delivery date, missing items, or partial deliveries. When a customer places an order, extract the order details and send them to a human for review (decided 2026-10-07). | SOP drafted: `sops/order-status-and-placement-sop.md`. Order placement belongs to this category (decided 2026-10-07); label confirmed in `CLASSIFICATION_GUIDE.md`. |
| Return / quality complaint | Gather information, prepare a draft and concise summary, and hand the case to a human to decide the resolution. | SOP drafted: `sops/complaints-and-returns-sop.md`. |
| Invoice / payment question | Extract incoming supplier invoices into a database. Separately, retrieve and send existing customer invoices after ownership and requester-authorization checks; clarify ambiguity or hand off failed verification. | SOP drafted: `sops/invoices-and-payments-sop.md` (both workflows and payment questions); payment processing is outside scope. |
| Customer account / onboarding | Collect the required details and automatically create the new customer record. | SOP drafted: `sops/onboarding-sop.md`. |
| Technical suitability question | Answer from applicable documentation, cite the source, and send the relevant technical note or guide. Hand unclear cases, missing information, or unavailable documentation to a human for review. | SOP drafted: `sops/technical-question-sop.md`. Label name kept and defined broadly in `CLASSIFICATION_GUIDE.md` §4.7 (decided 2026-10-10). |
| Other / unclear / unrelated | Includes spam and unsolicited promotions. Send to a human with a brief summary and reason for the classification. | SOP drafted: `sops/other-unclear-sop.md`; no separate spam label. |

Category boundaries settled so far: placing an order belongs to Order status (decided 2026-10-07), not Quotation; supplying a document, including a technical note asked for by name, is a Product documentation request, while explaining or advising is a Technical question (product-documentation SOP §1). Historical complaints versus current requests were settled on 2026-10-08: any report of a problem with supplied goods is a complaint, with or without a remedy request; a settled past problem mentioned as background is not (complaints SOP §1). Several requests may share one category, and an email gets one label per category, not per request.

**Classification guide: written last** (decided 2026-10-08; written 2026-10-10 as `CLASSIFICATION_GUIDE.md`, which confirms every rule below and adds B-3 availability and B-8 invoice disputes). The guide is written after the SOPs and documentation for all eight categories exist, because the boundaries depend on how each category is handled. Until then, label rules assumed by an SOP or a test email are provisional: record them in the SOP that assumes them, and the guide confirms or changes them. Assumed so far: a document request plus a question gets both the documentation and technical labels; the complaint label is added when the customer calls the unit faulty or asks for a remedy, or when the unit itself shows a safety signal, but not for documented steps that did not work or a user-caused spill (technical-question SOP §8, decided 2026-10-08); "price list" is a quotation request and "catalogue" a documentation request (product-documentation SOP §2).

## First selected capability: quotation responses

### Agreed behavior

Classify the email and answer the requested quotation correctly, following the company's documented pricing rules and quotation SOP. Routine quotations should not require sales-team approval solely because they are sales enquiries.

The assistant needs to identify and apply:

- The requested product and, where relevant, version.
- What each version includes and its price.
- Requested quantity and the corresponding unit price and total.
- Applicable quantity discounts.
- Delivery charges by zone or region.
- Applicable free-delivery conditions.

### Boundary handling agreed on 2026-10-05

- **Missing or vague information:** ask for clarification. Provide any price or other information that can already be established reliably, making clear what remains unresolved.
- **Discounts:** consult the discount rules stored in the database to determine whether a discount applies. If applicability is uncertain, redirect to a human.
- **Alternative products:** when the requested product is not in the catalogue, look for the closest catalogue item and offer it explicitly as a suggestion. Do not silently substitute it for the requested item. The criteria for an acceptable alternative, and what to do when none is suitable, will belong in the documentation. Absence from the catalogue does not establish stock availability.
- **Quotation plus complaint:** identify both categories. The quotation process handles the quotation portion and the complaint process handles the complaint portion. Combine the results, preserving both parts. Wait until both parts are ready and any required human review is complete before sending one combined reply. Adopted in the SOPs and `architecture.mmd`: one label per category, one case part per label, one specialist agent per category.

Implementation pattern (reflected in the SOPs): keep one parent ticket with linked request parts and individual statuses, then assemble a coherent response and review summary. This would avoid losing context when the work is split and support the agreed rule to wait for both parts.

### Documentation created

| Need | Where |
| --- | --- |
| Product and price catalogue, with versions and units of sale | `data/catalogue.csv` |
| Discount rules | `data/discounts.csv` |
| Delivery charges, zones and free-delivery thresholds | `data/delivery_charges.csv`, `data/delivery_zones.csv`, `company/delivery-policy.md` |
| Commercial terms (VAT, validity, calculation order) | `company/terms-of-sale.md` |
| Quotation procedure | `sops/quotation-sop.md` |
| Company profile, mission and values | `company/company-profile.md` |

### Quotation decisions resolved in the SOP

- **Acceptable alternative:** same category, same function, nearest size or version, offered as a labelled suggestion. If nothing is related, say we do not carry it and escalate to Sales (SOP §6).
- **Thresholds:** line total, then discount, then delivery, then VAT; free delivery judged on the discounted goods total ex VAT (SOP §3, §7; terms of sale 3.3).
- **Commercial details:** prices ex VAT, VAT at 20% shown separately, quote valid 30 days (SOP §10).
- **Human help:** uncertain discount, D4 equipment quantities, special prices, no alternative, not-served destinations, `on_hold` accounts (SOP §11).
- **Showing every version** when the version is not stated, and **arithmetic in code**, are now SOP rules (SOP §1, §3).

Still open: how additional requests in the same email are handled while their category is not yet implemented (see "Behavior decisions still open").

### Evaluation

Targets and grading are in [EVALUATION.md](EVALUATION.md) (quotation: price and route both correct, 95% of complete requests; 100% of incomplete or ambiguous requests clarified, never a final total). The planted cases are in [TEST_TRAPS.md](TEST_TRAPS.md).

## Product documentation requests

### Agreed behavior

- Identify the requested product and version.
- Find the matching manual, specification sheet, or other requested product document in the company's records.
- Send the matching document directly with a brief explanation of what it contains.
- Ask for clarification when the product or version is ambiguous.
- If the requested document is missing, flag the missing document and hand the request to a human. Do not treat the request as fulfilled.
- Apply the shared human-review requirement: provide a concise summary and a starting draft with the unresolved point clearly marked.

This category covers supplying documents. Advice about technical suitability and troubleshooting will be defined under the technical-question category.

### Documentation created

- Product-document index: `data/product_documents.csv` (32 documents, linked to SKUs), with `data/document_type_synonyms.csv` for customer wording.
- The documents themselves: `data/documents/` (Markdown source and PDF).
- Procedure: `sops/product-documentation-sop.md`. Documents are attached as PDF; missing documents go to Customer service, or to Technical / quality review for validation documents, unit calibration certificates and lot-specific certificates of analysis (SOP §5). In a mixed email the document part waits for the other parts and goes out in one merged reply (SOP §8), following the same wait-for-all-parts rule agreed for quotation plus complaint.

## Order status / delivery issues

### Agreed behavior

- Look up the relevant order and shipment records and report delivery status to the customer.
- For delays, the assistant may reply directly, acknowledge and apologize for the delay, and give the delivery date supported by the records.
- If a delay is recorded but no revised delivery date is available, prepare a draft and send the case for human review. Do not invent a date or automatically send the draft.
- For missing items, prepare a reply draft and send it for human review.
- For partial deliveries, prepare a reply draft and send it for human review.
- For human-reviewed cases, include the brief summary and supporting records described in the shared review requirements.

Replies must preserve the source's certainty: an estimated delivery date remains an estimate, not a guaranteed delivery promise. Reporting a status does not authorize changing shipment records.

### Order placement (decided 2026-10-07)

The same category and agent also handle customers placing an order.

- Extract the order details: customer and sender, products and versions, quantities, delivery address or postcode, requested date, customer purchase-order number, and any quote reference.
- Check the sender against the customer records. Note the account's payment terms and status.
- Prepare a structured order draft and a brief summary, and send both to a human for review. The assistant does not confirm the order, take payment or create shipments.
- Missing or ambiguous details are listed for the human and may be requested from the customer.
- Order placement is an order *request*, not a confirmed order.

### Decisions made 2026-10-09

- Order placement is reviewed by Sales; status, delivery issues and changes by Logistics.
- Missing order details are listed for Sales and asked for in the acknowledgement reply.
- An order from someone without an account is drafted for Sales, flagged, and the reply asks for the onboarding details.
- Changes and cancellations of orders not yet delivered belong to this category, verified like status requests and always decided by a person. "Cancel" for delivered goods is a return.

### Documentation created

- Procedure: `sops/order-status-and-placement-sop.md`.
- Records: `data/orders.csv`, `order_lines.csv`, `shipments.csv`, including in-transit, delayed, partial and not-yet-dispatched orders.

## Returns / quality complaints

### Agreed initial behavior

- Gather the information needed to understand the complaint, using the customer's message, relevant records, and the SOP's information requirements. Ask for missing details where necessary.
- Prepare a reply draft based on the company documentation and available facts.
- Send the case to a human with a brief summary of the issue, information collected, unresolved points, and any SOP-supported proposed action.
- The human decides and approves the resolution. The assistant does not independently authorize refunds, replacements, or other remedies in this initial scope.
- Keep any proposed remedy distinct from an approved or completed action.

Missing items and partial deliveries retain their existing human-review requirement. For quotation-plus-complaint emails, wait until both parts and the required human review are ready before sending the combined reply.

### Decisions made 2026-10-08

- Wrong items and goods damaged in transit are complaints, decided by Logistics; quality defects, faults and returns by Technical / quality review. Missing items and partial deliveries stay with order status.
- Any report of a problem with supplied goods gets the complaint label, with or without a remedy request.
- A sender who does not match the order is still heard; the reply discloses nothing from the order and the case is flagged.
- Reports outside the policy window are handled as normal and flagged for the person deciding; the assistant never refuses.

### Documentation created

- Procedure: `sops/complaints-and-returns-sop.md` (every complaint part escalates; missing information is asked for in the starting draft).
- Order, order-line and shipment records: `data/orders.csv`, `order_lines.csv`, `shipments.csv`.

Autonomous complaint resolution may be considered later and is not part of the agreed initial handling.

## Incoming supplier invoices

### Agreed scope

Extract information from invoices received for purchases made by the fictional company and store the extracted information in a database. This is the complete initial supplier-invoice workflow requested by the user.

Do not add a mandatory human-review stage or pending-approval workflow. Fields (header and line items), flags and duplicate handling are in `sops/invoices-and-payments-sop.md` §5; the register is `data/supplier_invoice_register.csv`. Decided 2026-10-09: credit notes are extracted; an unknown supplier's invoice is extracted and flagged; statements and payment reminders are not extracted and go to Finance as ordinary escalated emails (not a notification workflow).

### Outside this workflow

- Business validation, purchase-order matching, or goods-receipt matching.
- Invoice approval, accounting posting, or payment processing.
- A finance dashboard or notification/reporting workflow. Earlier notification ideas are not part of the latest extraction-and-storage-only scope.

Customer requests for copies of invoices issued by the company follow the separate workflow below.

## Customer invoice-copy requests

### Agreed behavior

- Find the existing invoice for the requested order.
- Verify that the invoice belongs to the customer and that the requester is authorized to receive it.
- Send the invoice directly when those checks pass and the requested invoice is unambiguously identified.
- Ask for clarification if the request is ambiguous.
- Hand the case to a human if ownership or requester authorization cannot be verified; do not send the invoice automatically in that case.

### Decisions made 2026-10-09

- An order number identifies the invoice when that order has exactly one; otherwise the invoice number is asked for.
- Payment questions (balance, remittance advice, payment method, disputes) always go to Finance; the reply discloses no balance or payment status.

### Documentation created

- Procedure: `sops/invoices-and-payments-sop.md` §3 and §4.
- Records: `data/invoices.csv`, `invoice_lines.csv` and the PDFs in `data/invoices/`.

This workflow resends existing invoices. Creating or modifying invoices and processing payments are not included.

## Customer account / onboarding

### Agreed behavior

For a new customer who has decided to buy, collect the required customer-record details and create the customer record automatically, without a routine human-approval step.

### Decisions made 2026-10-09

- New accounts start on prepay; a request for 30-day terms is flagged to Finance, never granted automatically.
- The sender becomes a contact authorised for orders and invoices; other people are added only with an email address and a stated role.
- Changes to existing accounts belong to this category, are verified like order status, and always go to Sales; nothing is changed automatically.
- When a "new" customer's VAT or registration number already exists, no record is created and the reply does not confirm that an account exists. A similar name with different numbers is a separate entity: created and flagged.

### Documentation created

- Procedure: `sops/onboarding-sop.md` (required fields, format checks, duplicates, postcode, record creation, failure handling).

Creating a customer record is separate from confirming an order or processing payment; those capabilities are not added by this onboarding decision.

## Technical questions

### Agreed behavior

- Answer directly from applicable company/product documentation when it clearly supports the answer.
- Cite where the answer came from and send the relevant technical note or guide with the response.
- If the answer or documentation is unclear, required information is missing, or the relevant documentation cannot be found, send the case to a human for review rather than sending an unsupported technical answer.
- For human review, retain the shared requirement to prepare a starting draft and a brief summary of the question, available evidence, and unresolved points.

Supplying a requested document alone belongs to product-documentation requests. Explaining an answer or providing documented technical guidance belongs here. Application-suitability claims must be supported by applicable documentation rather than inferred beyond it.

### Documentation needed

- Technical notes, guides, and product documentation linked to the applicable product and version.
- A technical-response SOP defining source applicability, citations, document delivery, and human handoff: drafted as `sops/technical-question-sop.md` (citations name the document, `doc_id`, revision and section; cited documents are attached as PDF).

The original category label is "Technical suitability question"; it is kept and defined to cover the agreed technical-question handling (`CLASSIFICATION_GUIDE.md` §4.7, decided 2026-10-10).

## Other / unclear / unrelated

### Agreed behavior

- Keep the existing Other category, including spam and unsolicited promotions. Do not add a separate spam label; the classification scope remains eight categories.
- Briefly summarize what the email is about and explain why it was classified as Other, using evidence from the message.
- Send all emails in this category to a human for review and handling.

The latest user decision supersedes the earlier suggestion to separate spam. No automatic deletion, rejection, or customer reply is included in this handling rule. The brief summary and classification reason are the specified handoff for this category; a customer-facing draft is not required by this rule.

### Decisions made 2026-10-09

- Emails in another language are classified by content and handled by their category's SOP, with the reply in English; Other only if not understood.
- Other emails carry a sub-type for triage (spam, sales_pitch, phishing, auto_reply, acknowledgement, service_feedback, data_request, job_application, unrelated, unclear); still one label, still to a person.
- Complaints about service rather than goods are Other (`service_feedback`); late or missing deliveries stay order status.
- Unrelated content beside a real request adds no Other label.

Procedure: `sops/other-unclear-sop.md`.

## Deferred sales capabilities

Earlier discussion included remembering quoted products and prices across replies, handling additions, and collecting purchase details before handing the request to a team. The user subsequently narrowed the first step to answering quotation requests.

- Conversation continuation is a desired broader behavior; its inclusion in the first quotation increment is unresolved.
- Proactive follow-ups are not needed for the current scope.
- Order confirmation and payment processing remain outside scope.
- Order placement is handled as in the "Order placement" section above: extract the details and hand them to a human for review. It must distinguish an order request from a confirmed order and report only verified payment information. Superseded for the Northfield project on 2026-10-07: earlier text deferring purchase handling.

## What remains before implementation

### Behavior decisions still open

- Handling of mixed-category combinations beyond quotation plus complaint, including unsupported parts during incremental implementation.
- How much conversation history the first version retains and uses when a customer replies. Proactive follow-ups remain excluded.
- Mailbox intake details, left pending until the intake is built (2026-10-10): how new mail is noticed, where replies are reviewed, and whether Outlook is supported ([END_TO_END_TESTING.md](END_TO_END_TESTING.md) §6).
- Category definitions: done in `CLASSIFICATION_GUIDE.md` (2026-10-10). Three edges remain undecided there (§7).
- Remaining exception rules listed in each workflow, such as no suitable catalogue alternative, an invoice that cannot be found, or duplicate customer records.

### Documentation and data

Done: company profile, mission, values and shared policies (`company/`); catalogue, prices, discounts, delivery rules and terms of sale; customer, contact and prospect records; product-document index and documents, including technical notes; quotation, product-documentation and technical-question SOPs; planted test cases (`TEST_TRAPS.md`).

Still to create:
- Test emails for all eight categories and 37 mixed emails exist in `data/emails/`, all reviewed, including the four added for classification guide B-3 and B-8; all 344 label sets are supported. The 30-email anchor set is selected (`ANCHOR_SET.md`) and waits for the user's reading.
- The policy-level trap documents planned in `KNOWLEDGE_SOURCES.md`.

These do not mean the agreed high-level handling must be defined again.

### Evaluation and delivery details to define

Set in [EVALUATION.md](EVALUATION.md): PoC exact-match targets, golden-set size and coverage, and per-category targets. Still to define:
- Confidence thresholds, if evaluation shows the outputs are useful.
- A baseline for human handling time and review effort.
- The golden-set emails themselves, with expected results, including mixed requests and human handoffs.
- A minimal human-review experience and the implementation choices needed to demonstrate the workflows.

## Next phase

Write the remaining SOPs and the order, shipment and invoice records, resolving the remaining behavior questions as each SOP is written. Then author the golden-set emails from `TEST_TRAPS.md` before testing the implementation.

Record scope-changing rules during category discussions, but defer detailed fictional prices and policy values until the documentation step. Revisit scope if writing an SOP reveals a material dependency.

## Continuation notes

The user wants guidance in making scope decisions, rather than the assistant choosing the entire MVP unprompted. Keep the discussion simple, proceed category by category, and distinguish confirmed choices from suggestions.

High-level scope is defined across all eight categories. Company documentation, the quotation and product-documentation SOPs, and the supporting product and customer data now exist; the remaining SOPs and records are listed above. Do not restart the category-by-category scope discussion unless the user requests a change. The Google Doc has not been edited during this work.

## Original reference

[Laboratory supplier email assistant preparation plan](https://docs.google.com/document/d/1khjViLz2tOWmjmnUnEmNTTek-ZFsZuDVU68RDbc9FnE/edit)

The original plan contains earlier proposals. Where this file records an explicit later user decision, use that decision for continued planning.
