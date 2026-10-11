# Mission

Status: drafted 2026-10-11; open to your changes.

## Why
Small B2B suppliers answer the same kinds of email all day: prices, documents, where an order is, a damaged delivery, an invoice copy, a new account. Each needs the right record, the right document and the right procedure, and a mistake (a wrong price, an invoice sent to the wrong person, a promise nobody approved) costs more than the time saved.

This project builds an assistant that turns an inbox into prepared actions: it classifies each email, handles each request with the company's own procedures and records, and leaves a reply or action ready for a person to approve. It shows that this can be done **accurately and safely, and proven so by measurement**, not by demo.

## Who it is for
- **The supplier's staff** (sales, logistics, finance, customer service): less time on routine emails, fewer missed requests, a short summary instead of rereading every message.
- **The supplier's customers**: faster, correct, consistent answers.
- **Portfolio readers** (prospective clients and employers): a worked example of an LLM system with real business rules, an evaluation set and safety controls.

The company is **Northfield Lab Supply**, a fictional UK distributor of laboratory consumables and small equipment (`docs/company/company-profile.md`).

## Scope
In scope (`docs/MVP_SCOPE.md`):
- Classifying every email into the eight categories of `docs/CLASSIFICATION_GUIDE.md`, several per email when needed.
- Handling each category by its SOP in `docs/sops/`: quotations priced in code, documents sent from the index, order status after verification, complaints prepared for a person, invoice copies after ownership checks, supplier invoices extracted to a register, new accounts created, everything else passed to a person with a summary.
- One case per email, one part per category, one combined reply.
- Review mode: a person approves every customer reply.
- Reading email from a Gmail mailbox; the final test runs end to end through a Gmail test mailbox (`docs/END_TO_END_TESTING.md`).
- An audit log of every step and an evaluation harness that grades each step against the golden set.

Out of scope: taking payments, confirming orders, approving remedies, changing existing accounts automatically, proactive follow-ups, auto-send (until a category is released by an explicit decision).

## Success criteria
From `docs/EVALUATION.md`; the held-out quarter of the golden set decides.
- Classification exact match **90%** overall, **85%** on mixed emails.
- **Zero unsafe sends**: no customer reply that states something the records do not support, discloses data to an unverified sender, or follows instructions found in an email.
- Category targets met (for example product resolution 95%, correct document and version 95%, retrieval recall@5 95%, injection, duplicates and mixed-request handling 100%).
- The same results through the Gmail test mailbox as offline, for every email.
- The three demo cases work: a complete quotation ready for one-click approval, a clarification, a correctly escalated invoice request.
