# Knowledge sources

Decided 2026-10-06. Where each kind of company knowledge lives and which categories consult it. To feed `specs/tech-stack.md` once the specs are created (the `specs/` folder does not exist yet).

## Vector store: two indexes

### Index 1 — documents (passages the LLM reads and cites)

| Content | Examples | Used by |
| --- | --- | --- |
| Company core | profile, terms of sale, delivery and returns policy, data-protection notice | all categories |
| SOPs | one per category, one or two pages each | the category it belongs to |
| Product documentation | manuals, specification sheets and technical notes (equipment and two consumables); datasheets, certificates of analysis, a declaration of conformity and a safety data sheet (consumables); a sample calibration certificate (32 files for 11 products; see `data/product_documents.csv`) | product documentation, technical questions |
| Planted traps | outdated checklist, superseded policy, contradictory note | evaluation only |

Chunk metadata: document, section, product and version where relevant, effective date, current/superseded flag.

### Index 2 — catalogue (rows the code prices)

One entry per product and version: SKU, name, description, inclusions, unit of sale. Searched exact → fuzzy → semantic for product resolution. The price is never read from the index; it is read from the catalogue table after the row is resolved.

## Database tables (lookup tools, never retrieval)

Catalogue with prices and versions, discount rules, delivery charges by zone, customers and authorised contacts, orders and shipments, invoices, product-document index.

## Configuration and code (enforced, never retrieved)

Required fields per category, duplicate keys, auto-send preconditions, verification rules for order status and invoice copies.

## SOPs live in two places on purpose

The SOP text is in the document index so the LLM can follow the procedure and cite it. Its hard rules (what must be present before sending, what triggers escalation) are also implemented as code checks. The code wins on any disagreement, and such a disagreement is a test case.

## Which categories call the document index

- Always: technical questions, product documentation.
- For SOP and policies (and the subject of the no-RAG baseline): quotations, complaints, order status, invoice copies, onboarding.
- Never: supplier invoice extraction, Other.

## Approximate document count

35–50 documents: 5–6 company core, 8 SOPs, 32 product documents (template-generated, one with a planted contradiction), 3 traps.
