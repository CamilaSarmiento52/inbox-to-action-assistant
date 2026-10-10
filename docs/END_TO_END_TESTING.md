# End-to-end testing with Gmail

Status: decided 2026-10-10 in discussion with the user. Implementation details marked *open* are decided when the intake is built.

The JSON test emails are for building and tuning: they are fast, cheap and exactly repeatable. The finished solution is tested the way it will run: connected to a Gmail mailbox, reading the messages there, classifying them, preparing replies and leaving them for review. The emails are the same 344 golden-set emails, loaded into the mailbox.

## 1. Test stages
| Stage | Input | Emails | Purpose | When |
| --- | --- | --- | --- | --- |
| 1. Tuning | JSONL files | `tune` split | Build and adjust the classifier, the agents and the prompts; read failures | Every change |
| 2. Offline scoring | JSONL files | `held_out` split, scored | Check the targets in EVALUATION.md on emails never used for tuning | Before each release candidate |
| 3. Gmail connection | Gmail test mailbox | A small smoke set (section 4) | Prove that reading, attachments, labels and drafts work | When the intake is built, and after any change to it |
| 4. End to end | Gmail test mailbox | All 344, loaded in `received_at` order | Test the whole solution: mailbox in, labels and drafts out, audit log, grading | Final acceptance |

All 344 are loaded in stage 4, not only the held-out quarter, because the emails share one time-ordered state: accounts created by onboarding emails are used by later quotes and orders, and resends need their originals (data/emails/README.md). Results are reported separately for `tune` and `held_out`; **acceptance is judged on the held-out results**, against the same targets as offline scoring.

**Parity check.** Each stage-4 result is compared with the stage-2 or stage-1 result for the same email. A difference in labels or route that the offline run did not show is a bug in the intake (encoding, attachments, threading), not in the classifier, and is fixed before acceptance.

## 2. One pipeline, two ways in
The pipeline reads one normalised message: sender, recipients, date, subject, plain-text body, attachments (file name, type, bytes), thread and message IDs. Two adapters produce it:
- **JSONL adapter**: reads `data/emails/*.jsonl`; attachments are read from the files they name (`data/supplier_documents/`).
- **Gmail adapter**: reads the mailbox through the Gmail API; decodes MIME, prefers the plain-text part, converts HTML to text when there is none, and downloads attachments.

Everything after the adapter (duplicate check, classifier, agents, rules, review, audit log) is the same code for both.

## 3. The test mailbox
- **One dedicated Gmail account** for testing, never a personal or business mailbox. The user creates the account and the Google Cloud OAuth credentials; credentials stay outside the repository.
- **Loading** (`tools/load_gmail.py`, to build): for each golden-set email in `received_at` order, build an RFC 822 message with its From, To, Date, Subject, body and attachments, and put it in the inbox with the Gmail API's insert or import call. Nothing is sent: the fictional senders (`*.example`) cannot send mail, and the date header is kept so the timeline is preserved. Resends and "RE:" emails carry `In-Reply-To` and `References` to their originals where the fixture is a reply, so Gmail threads them as a real mailbox would.
- **Matching to expected answers**: each loaded message carries `X-Test-Email-Id: <email_id>`. The grader uses it to find the expected answer. **The Gmail adapter removes it before anything else sees the message**; a test fails if the header reaches the classifier or an agent.
- **Reset**: the loader can empty the test mailbox and reload it, so stage 4 always starts from the same state.

## 4. Connection tests (stage 3)
Run on a handful of emails chosen to cover the mechanics, not the categories:

| Check | Pass when |
| --- | --- |
| Authentication | The adapter connects with the granted scopes only |
| Reading | A newly loaded message is picked up once, with sender, date and subject intact |
| Encoding | Accents and symbols survive (the German emails, "µl", "°C", "£") |
| HTML-only body | Converted to readable text |
| Attachments | A supplier PDF and a raster scan arrive as the same bytes as the source files |
| Test header | `X-Test-Email-Id` is absent from the normalised message |
| Threading | A resend is linked to its original case (G-10) |
| Labels | The predicted categories appear as Gmail labels on the message |
| Drafts | The reply appears as a Gmail draft in the same thread, with its attachments |
| No sending | No message leaves the mailbox |
| Idempotency | Running the pipeline twice creates no second case, label set or draft |

## 5. What the system may do in the mailbox
- **Read** messages, **apply labels** (one per category, plus processing state), **create drafts**. Review mode: a person approves every reply (communication policy §2), so a draft is the end of the line in testing.
- **Never send, delete or archive.** The OAuth scopes requested exclude sending (`gmail.send`) and full access; the exact scope set is *open* (likely `gmail.modify` with `gmail.compose` for drafts, and `gmail.insert` for the loader only).
- Labels written by the system are prefixed (`NLS/…`), so they never mix with labels a person adds.

## 6. Pending (decided 2026-10-10: leave open until the intake is built)
Nothing is designed around any of these yet; each is decided when implementation reaches it.
- **Noticing new mail**: checking on a timer, or Gmail push notifications.
- **Where replies are reviewed**: in Gmail drafts only, or in a separate review screen that also writes the Gmail draft.
- **Outlook**: whether a Microsoft Graph adapter is added. The two-adapter design allows it.
