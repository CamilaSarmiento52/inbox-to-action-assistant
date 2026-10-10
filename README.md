# Inbox-to-action assistant

An email assistant for a small B2B supplier: it reads incoming customer and supplier emails, classifies each request, handles it with the company's own procedures and records, and prepares a reply or action for a person to approve.

The company is **Northfield Lab Supply**, a fictional UK distributor of laboratory consumables and small equipment. Every customer, price, policy and document here is invented for this portfolio project.

## Status

Documentation and evaluation data are complete. Implementation has not started; the plan is in [`specs/`](specs/) once agreed.

| Done | Where |
| --- | --- |
| Scope, handling rules per category, success targets | [`docs/MVP_SCOPE.md`](docs/MVP_SCOPE.md), [`docs/EVALUATION.md`](docs/EVALUATION.md) |
| Classification guide: 8 labels, boundary rules | [`docs/CLASSIFICATION_GUIDE.md`](docs/CLASSIFICATION_GUIDE.md) |
| One SOP per category, company policies | [`docs/sops/`](docs/sops/), [`docs/company/`](docs/company/) |
| Fictional records: catalogue, customers, orders, invoices, supplier documents, product documents | [`data/`](data/) |
| 344 golden-set test emails with expected labels, routes, extractions and reply requirements, each reviewed by a second model family | [`data/emails/`](data/emails/) |
| Planted traps and the behaviour each must trigger | [`docs/TEST_TRAPS.md`](docs/TEST_TRAPS.md) |
| End-to-end test plan with a Gmail test mailbox | [`docs/END_TO_END_TESTING.md`](docs/END_TO_END_TESTING.md) |

## The eight categories

Quotation request · Product documentation request · Order status / delivery issue · Return / quality complaint · Invoice / payment question · Customer account / onboarding · Technical suitability question · Other / unclear / unrelated. An email can carry several; each becomes one part of one case, and the customer gets one combined reply.

## Principles

- **Records and documents, not memory.** Prices, statuses and answers come from the data and the documents, cited.
- **Arithmetic and rules in code.** Pricing, verification and required-field checks are code; the model extracts and drafts.
- **A person approves every reply** while the categories are evaluated (review mode).
- **Measured.** Every behaviour has a target in `EVALUATION.md` and test emails that exercise it; a quarter of the set is held out.

## Regenerating the fixtures

```bash
pip install -r tools/requirements.txt
```

Generation order and commands are in [`data/emails/README.md`](data/emails/README.md). Corrections are made in the generators in `tools/`, never in the JSONL files.
