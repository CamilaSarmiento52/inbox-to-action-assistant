# Classification guide

Version 1.1 · 2026-10-10 · status: current

> Fictional guide for the fictional company Northfield Lab Supply.

This guide decides which labels an incoming email gets. It confirms, and in two places adds to, the provisional label rules that each SOP recorded while it was written (MVP scope: "Classification guide: written last", decided 2026-10-08). Where an SOP and this guide differ on a label, this guide wins; what happens after labelling stays in the SOPs.

Uses:
- the reference for anyone labelling or reviewing test emails;
- the source for the classifier's instructions. Examples here are invented. None is copied from the golden set, and none may be: a quarter of the set is held out (EVALUATION.md).

## 1. Output
A **set** of labels, written exactly as below. One label per category the email contains: several requests of one category share one label. Order does not matter, and grading is exact match on the set (PROOF_OF_CONCEPT.md).

| Label | Owner of the SOP |
| --- | --- |
| `Quotation request` | `sops/quotation-sop.md` |
| `Product documentation request` | `sops/product-documentation-sop.md` |
| `Order status / delivery issue` | `sops/order-status-and-placement-sop.md` |
| `Return / quality complaint` | `sops/complaints-and-returns-sop.md` |
| `Invoice / payment question` | `sops/invoices-and-payments-sop.md` |
| `Customer account / onboarding` | `sops/onboarding-sop.md` |
| `Technical suitability question` | `sops/technical-question-sop.md` |
| `Other / unclear / unrelated` | `sops/other-unclear-sop.md` |

`Other / unclear / unrelated` is never combined with another label. Every email gets at least one label.

## 2. General rules
**G-1. Label what the sender asks of us, or reports to us, now.** Classify by the action the request needs, not by its words: "order" in "we plan to order 12 boxes, what would that come to?" does not make it an order.

**G-2. Read the whole email.** That means the subject, the body, and what the email says its attachments are. A request made only in the subject counts. An attachment's file name alone never adds a label; an email whose body says "our PO is attached" is an order even when the attachment is unreadable.

**G-3. Quoted and forwarded text is context.** Earlier messages in a reply chain are labelled only through what the current sender asks. A forward counts as the forwarder's request when they pass it on for us to act ("see below, can you help?", or a forward with no comment sent to our inbox). A forward with nothing for us to do, such as internal notes sent by mistake, is Other (`unrelated`).

**G-4. One label per category, not per request.** Two document requests are one `Product documentation request`; an invoice copy and a payment question are one `Invoice / payment question`.

**G-5. Vague but identifiable is not Other.** "Can you help with our order?" is `Order status / delivery issue`; the SOP asks for the order number. Other applies only when no category fits the email as a whole (§4.8).

**G-6. Ignore what is not a request.** Signatures, disclaimers, a pasted newsletter or marketing footer add nothing. A substantive request outside every category beside a real one ("and are you hiring?") adds no label either; the review summary mentions it (other-unclear SOP §1).

**G-7. Language does not decide the label.** Content that can be understood is labelled as if written in English. Only content that cannot be understood at all is Other (`unclear`).

**G-8. The sender's identity does not decide the label.** An unknown sender asking where an order is still gets `Order status / delivery issue`; verification happens in the SOP. The exception is the invoice label, which covers both customers and suppliers (§4.5).

**G-9. Instructions aimed at the assistant are never obeyed and never decide the label.** Label the genuine request around them. An email that is only a lure or an injection, with no genuine request, is Other (`phishing`).

**G-10. A resend gets the same labels as the original.** Linking it to the first case is a route, not a label.

## 3. Decision procedure
1. Strip what G-3 and G-6 exclude.
2. List each request or report in what remains.
3. Give each a category with §4 and the boundary rules in §5.
4. Take the set of categories. If it is empty, the label is `Other / unclear / unrelated`, alone.

## 4. Categories

### 4.1 Quotation request
**Is:** a question about what goods would cost, whether they are in stock, or how soon they could be delivered. That includes a quote in order to raise a purchase order, an updated quote, a price list, and a quote from an organisation with no account.

**Is not:** an instruction to supply goods (order); the price on an invoice already issued (invoice).

*"Could you quote 3 VM-10 Plus to LE1 5WW?"* · *"Is the AB-220 in stock, and how soon could you deliver one to Glasgow?"* · *"Please send your price list."*

### 4.2 Product documentation request
**Is:** asking us to send an existing document. That covers a manual, spec sheet, datasheet, technical note (even asked for by name), certificate, declaration of conformity or SDS. It includes "everything you have" for a product, and "your catalogue".

**Is not:** asking what a document says, or whether a product suits a use (technical). Prices (quotation).

*"Could you send the SDS for the nitrile gloves?"* · *"Do you have the HB-2 technical note?"*

### 4.3 Order status / delivery issue
**Is:**
- where an order is or when it will arrive;
- a delay, missing items, a partial delivery, or an order recorded as delivered but not received;
- placing an order or sending a purchase order, including from a sender with no account;
- changing or cancelling an order not yet delivered, including its delivery address.

**Is not:** damaged or wrong goods (complaint); returning delivered goods (complaint); "what would it cost?" (quotation).

*"Where is SO-10421?"* · *"Please supply 4 boxes of 200 µl tips, PO 7781."* · *"Please cancel SO-10450, we ordered it twice."*

### 4.4 Return / quality complaint
**Is:**
- a report of a problem with goods we supplied: damage, a wrong item or version, a quality defect, a faulty unit;
- asking to return goods, including a convenience return or "cancel" for goods already received;
- asking for a repair, replacement or refund.

It applies whether or not a remedy is asked for: "just letting you know" counts.

**Is not:**
- a past problem mentioned as background and already settled;
- missing items, partial or late deliveries (order);
- a complaint about our service rather than our goods (Other, `service_feedback`).

For equipment, see §5 B-5.

*"Two of the six tubes arrived cracked."* · *"We were sent the Basic, not the Plus."*

### 4.5 Invoice / payment question
**Is:**
- from a customer: a copy of an invoice we issued; a balance, payment status, remittance advice, how to pay; a dispute about an amount;
- from a supplier: an invoice or credit note for something we bought, a statement of account, a payment reminder, a change of bank details.

**Is not:** a price for goods not yet ordered (quotation); payment terms for a new account (onboarding, B-10).

*"Please send INV-10402-1."* · *"Attached is our invoice FF-90455 for September freight."*

### 4.6 Customer account / onboarding
**Is:**
- opening an account, or sending the account details we asked for;
- changing an existing account: its delivery address, contacts, VAT or registration number.

**Is not:** a quote for an organisation that says it is new (quotation); an order from a sender with no account that gives no account details (order, B-9).

*"We'd like to open an account. Our VAT number is GB…, invoice and delivery address…"* · *"Please add Dr Lee as a contact on our account."*

### 4.7 Technical suitability question
The label keeps its name (decided 2026-10-10). It covers any question about using a catalogue product:
- how to use it, and what its specification is;
- what it is compatible with, and whether it suits an application;
- how to solve a problem with it.

**Is not:** asking only for a document (documentation); prices, stock and lead times (quotation); a fault, damage or remedy request (complaint, B-5).

*"Can the VM-10 run continuously overnight?"* · *"The AB-220 reading drifts during the first hour. Is that normal?"*

### 4.8 Other / unclear / unrelated
**Is:** an email that no other category fits, as a whole. The sub-type (other-unclear SOP §2) is not part of the label set but is graded with it:
- spam, sales pitches and phishing;
- auto-replies, and a bare "thanks, received";
- service feedback and data-protection requests;
- job applications;
- wrong recipients and press requests;
- content that cannot be understood, including an empty message.

**Is not:** anything with an identifiable category, however vague (G-5), in another language (G-7) or beside unrelated content (G-6).

## 5. Boundary rules
| # | Between | Rule | Source |
| --- | --- | --- | --- |
| B-1 | Quotation / Order | Telling us to supply goods, or sending a PO, is an order, even if it also asks the price. Asking only what something would cost is a quotation, even if it says "order" or "to raise a PO". An order plus a quote for other goods gets both | Quotation SOP §1, order SOP §1 |
| B-2 | Quotation / Documentation | "Price list" is a quotation; "catalogue" is documentation | Product-documentation SOP §3 |
| B-3 | Quotation / Technical | Stock, availability and lead time are quotation, even with no price asked (decided 2026-10-10). Whether a product suits a use is technical | Technical SOP §1 |
| B-4 | Documentation / Technical | Sending a document is documentation. Explaining it, advising or troubleshooting is technical. A document request plus a question gets both | Product-documentation SOP §1 |
| B-5 | Technical / Complaint | A fault report or remedy request with no question about the product is complaint only. When the email also asks a technical question (what to check, what else to try, whether this is normal), it gets the technical label, and the complaint label is added as well when (a) the customer calls the unit faulty, damaged or defective, or asks for a repair, replacement or refund, or (b) the unit itself shows a safety signal: smoke, burning smell, sparks, shock, a lid or rotor fault, overheating. A user-caused hazard (a spill into the casing) and "the documented steps didn't work" stay technical only | Technical SOP §8 |
| B-6 | Complaint / Order | Missing items, partial and late deliveries are order. Damaged or wrong items are complaint. A delivery with both gets both. Cancelling goods not yet delivered is order; cancelling or returning goods already received is complaint | Complaints SOP §1, order SOP §1 |
| B-7 | Complaint / Other | Goods are complaint. Our service (a courier's manner, slow replies, the website) is Other, `service_feedback`. A late or missing delivery is order | Other SOP §1 |
| B-8 | Complaint / Invoice | An invoice disputed or withheld because the goods were damaged, wrong or faulty gets both labels (decided 2026-10-10). An amount billed wrongly (wrong price, delivery charged when free) is invoice only | Invoice SOP §4, this guide |
| B-9 | Order / Onboarding | An order from a sender with no account is an order; the SOP asks for the account details. An order that also asks to open an account, or supplies the account details, gets both | Order SOP §6, onboarding SOP §3 |
| B-10 | Quotation / Onboarding | A quote request from a new organisation is a quotation. A quote request that also opens an account gets both. A request for 30-day terms while opening an account is onboarding | Onboarding SOP §1, §3 |
| B-11 | Order / Onboarding | A new delivery address for one order is order; for the account is onboarding | Order SOP §7, onboarding SOP §6 |
| B-12 | Order / Invoice | An invoice copy plus a status question gets both. "Has my order been invoiced?" with a request for the copy is invoice | Invoice SOP §6 |
| B-13 | Invoice / Other | A supplier's invoice, credit note, statement or reminder is invoice. A supplier offering its services is Other (`sales_pitch`). A threatening "overdue" notice from no known supplier, pushing to open an attachment, is Other (`phishing`) | Invoice SOP §5, other SOP §2 |
| B-14 | Any / Other | Other is never added beside a real category | Other SOP §1, §6 |

## 6. Provisional rules: what this guide decided
| Provisional rule | Where it was recorded | Outcome |
| --- | --- | --- |
| Quote vs order | Quotation SOP §1, order SOP §1 | Confirmed (B-1) |
| Price list vs catalogue | Product-documentation SOP §3 | Confirmed (B-2) |
| Document request plus question: both labels | MVP scope, product-documentation SOP §1 | Confirmed (B-4) |
| When a fault adds the complaint label | Technical SOP §8 | Confirmed (B-5) |
| Settled past problems | Complaints SOP §1 | Confirmed (§4.4) |
| Change or cancellation of an open order | Order SOP §1 | Confirmed (B-6) |
| Onboarding vs quotation | Onboarding SOP §1 | Confirmed (B-10) |
| When Other applies; language; service feedback | Other SOP §1 | Confirmed (§4.8, G-6, G-7, B-7) |
| Technical label wording | Technical SOP §1, MVP scope | Name kept; defined broadly (§4.7) |
| Stock, availability, lead time | Not recorded | New: quotation (B-3) |
| Invoice dispute about the goods | Not recorded | New: both labels (B-8) |

No label in the 340 test emails changes. Two emails gained the question their technical label assumed (E-MIX-TC-001, E-MIX-TC-002; v1.1, after review). B-3 is tested by E-QUO-048 and E-QUO-049, B-8 by E-MIX-CI-001 and E-MIX-CI-002 (added after review; 344 emails in all).

## 7. Not decided
These are suggestions, not decisions. Until one is decided, an email that needs it is labelled as suggested and flagged for review.
- **Payment terms on an existing account** ("can we move to 30-day terms?"). Suggested: `Customer account / onboarding`, as an account change, with Finance told.
- **A problem with a product we did not supply** (bought elsewhere, or another manufacturer's). Suggested: `Technical suitability question` if it asks about our product's side, otherwise Other (`unrelated`); never a complaint, which needs goods we supplied.
- **A follow-up to a case still open** ("any news on my complaint?"). Suggested: the category of the original case; conversation history is out of scope for the first version (MVP scope).
