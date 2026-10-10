# Proof of concept: email classification

## Objective

Evaluate how accurately the model distinguishes between the eight email categories, including emails containing multiple requests that belong to different categories.

Jev by TypeSafe AI is the initial model selected for evaluation. It is compared with a general LLM using a structured-output prompt, on the same set and with the same grader ([EVALUATION.md](EVALUATION.md)). This PoC evaluates classification capability; it does not implement the full email-assistant workflow.

## Categories

The starting categories come from the project preparation plan:

1. Quotation request
2. Product documentation request
3. Order status / delivery issue
4. Return / quality complaint
5. Invoice / payment question
6. Customer account / onboarding
7. Technical suitability question
8. Other / unclear / unrelated

All eight categories are included from the start. An email receives one label per category it contains: several requests of the same category share one label, so the expected output is a set of categories, not one label per request.

Spam, including unsolicited promotions, remains within `Other / unclear / unrelated`. There is no separate spam label. Human handling of these messages is documented in [MVP scope](MVP_SCOPE.md).

Category boundaries decided so far:

- **Placing an order** belongs to `Order status / delivery issue`, not `Quotation request` (decided 2026-10-07; see [MVP scope](MVP_SCOPE.md)).
- **Supplying a document**, including a technical note asked for by name, is a `Product documentation request`. Explaining a document, advising on suitability or troubleshooting is a `Technical suitability question` (product-documentation SOP §1).

All label rules are now in [CLASSIFICATION_GUIDE.md](CLASSIFICATION_GUIDE.md) (2026-10-10): historical complaints are settled there, and the technical label keeps its name with a broad definition.

## In scope

- Classifying emails against all eight categories.
- Recognizing every applicable category in mixed-request emails.
- Preparing a golden set of test emails with human-reviewed expected labels.
- Comparing predicted labels with expected labels using deterministic grading.
- Reporting overall performance, performance by category, and performance on mixed-category emails.
- Recording Jev's available confidence or probability outputs to explore whether they help identify classification errors.

## Inputs and outputs

**Input:** a test email. Its human-reviewed expected labels are held separately for evaluation and are not provided to the classifier.

**Output:** the model's predicted set of category labels, with available confidence or probability outputs recorded separately.

## Evaluation

### Exact-match grading

A test email passes when the predicted label set exactly matches the expected label set. Label order does not matter.

- Missing any required label fails the example.
- Adding any incorrect label fails the example.
- Correctly identifying only one category in an email requiring several categories fails the example.

For example, if the expected labels are `Quotation request` and `Order status / delivery issue`, predicting both and no others passes. Predicting only one, or adding `Invoice / payment question`, fails.

Classification grading does not use an LLM judge or compare the wording of generated replies.

### Results to report

- **Overall exact-match rate:** the proportion of test emails receiving the complete correct label set.
- **Performance by category:** correctly identified labels, missed labels, and incorrectly added labels.
- **Mixed-category performance:** exact-match results for emails with multiple expected categories, reported separately from single-category emails.

An example-level failure does not automatically mean the entire PoC fails. The success targets are **90% exact match overall and 85% on mixed-category emails** ([EVALUATION.md](EVALUATION.md)).

### Confidence analysis

Confidence and probability outputs are supplementary signals, not substitutes for comparing predictions with the golden set. A high confidence value does not establish that all requests were identified correctly.

No confidence threshold has been agreed. Whether these signals reliably identify errors must be assessed using reviewed examples.

## Out of scope

- Knowledge-base retrieval and RAG.
- Applying company policies or SOPs to decide actions.
- Extracting business fields such as quantities and order references as a separately evaluated capability.
- Drafting customer replies or evaluating their meaning with an LLM judge.
- Creating tasks, executing actions, or sending emails.
- Building the human-review interface or implementing the fallback workflow.

For the later system, the discussed requirement remains that uncertain cases should still provide an SOP-based draft as a starting point, with unresolved issues clearly identified for human review. That behavior is not part of this classification PoC.

## Decisions still open

- Remaining category definitions (complaints versus remedy requests; technical label wording) and rules for other ambiguous or overlapping cases.
- How the confidence or probability outputs will be assessed; no operational threshold is set yet.

Decided in [EVALUATION.md](EVALUATION.md): golden-set size and coverage (40 emails for confusable categories, 25 for the others, 30–40 mixed, about a quarter held out) and the success targets above.

## Reference

[Laboratory supplier email assistant preparation plan](https://docs.google.com/document/d/1khjViLz2tOWmjmnUnEmNTTek-ZFsZuDVU68RDbc9FnE/edit)
