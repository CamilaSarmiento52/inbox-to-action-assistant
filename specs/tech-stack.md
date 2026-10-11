# Tech stack

Status: agreed with the user, 2026-10-11. Items marked *pending* are decided in the phase named.

## 1. Choices
| Concern | Choice | Why |
| --- | --- | --- |
| Language | Python 3.13 | The fixture generators are Python; `Decimal` for money |
| Classifier | **Jev** (TypeSafe AI), compared with the **OpenAI Decisions API on GPT-6 Luna** | Decision models: a fixed set of answers with calibrated probabilities, fast and cheap. The PoC compares them on the same grader (`docs/PROOF_OF_CONCEPT.md`) |
| Specialist agents | **LangGraph**, one graph per category, with **OpenAI** models | Each category's steps are an explicit, inspectable graph. The OpenAI model is chosen in phase 3 by testing |
| Structured outputs | **Pydantic** | Every classifier result, extraction, case part and grader verdict is a validated model |
| Database | **PostgreSQL** with **pgvector**, run locally in Docker Compose | One database for business records, cases, the audit log, evaluation runs and the vector indexes |
| Embeddings | **OpenAI** embedding models | Model chosen in phase 3, when the catalogue index is built |
| Keyword and fuzzy search | PostgreSQL full-text search and `pg_trgm`; RapidFuzz in code where needed | The exact and fuzzy steps of product resolution, and the keyword half of hybrid retrieval |
| PDF text | pdfplumber | Supplier invoices and documents that have a text layer |
| Scanned documents | **Gemini** (vision) | Only for image-only scans (RN-77344, KSC-5203 today). Unreadable values must be flagged, not guessed |
| Reply grading | **Claude** (Anthropic), as an LLM judge against the shared rubric | A different model family from the agents, so replies are not graded by the family that wrote them |
| Email intake | Gmail API (`google-api-python-client`, OAuth) | `docs/END_TO_END_TESTING.md`; no permission to send |
| Review screen | *Pending (phase 4)*: Streamlit suggested | Depends on where replies are reviewed (END_TO_END_TESTING.md §6) |
| Tooling | uv (environment and lock file), ruff, pytest, GitHub Actions | CI runs the tests that call no model; model evaluations are run by hand because they cost money |

## 2. Architecture
One pipeline, two ways in (`docs/END_TO_END_TESTING.md` §2):

1. **Intake.** The JSONL adapter or the Gmail adapter produces one normalised message: sender, recipients, date, subject, plain-text body, attachments, thread and message IDs. The Gmail adapter strips `X-Test-Email-Id` first.
2. **Duplicate check** in code. A resend is linked to its first case and stops here.
3. **Classification.** Jev or the Decisions API answers **eight yes/no questions, one per category**, each with a probability. A label applies above its threshold; thresholds are tuned on the `tune` split only. Other applies only when no category does. Low-confidence results are flagged for review.
4. **Routing in code.** One case per email, one part per label. There is no orchestrator agent: the classifier decides the categories, and code starts one specialist graph per part.
5. **Specialist graphs (LangGraph).** Each follows its SOP: model nodes extract and draft; code nodes look up records, price, verify and check required fields. Each graph has only its own category's tools. Documents and technical questions loop over retrieval; most others are fixed sequences.
6. **Rules gate** in code: required fields, verification, route ranking, the review-mode switch. The code wins over the model on any disagreement.
7. **Merge.** When every part is ready, one combined reply with deduplicated attachments; the email's route is the most restrictive part's.
8. **Review.** A person approves, edits or rejects. Nothing is sent in review mode.
9. **Audit log.** Every step is recorded (input, output, retrieved passages, tool calls, model and prompt versions, cost, latency, human edits) and graded by the evaluation runner.

**State lives in PostgreSQL.** Cases, parts, their statuses and review decisions are database rows. A review may take days, so it is never held as a paused graph. LangGraph state covers one specialist run; any LangGraph checkpointing is for recovering a run, not the record of a case.

**LangChain use is limited** to what LangGraph needs to call models and tools (`langchain-core`, `langchain-openai`). Retrieval, document loading and prompts are our own code, so every prompt and tool call is visible to the grader.

## 3. Data model
| Group | Tables |
| --- | --- |
| Business records (loaded from `data/`) | catalogue, discounts, delivery zones and charges, customers, contacts, prospects, orders, order lines, shipments, invoices, invoice lines, suppliers, supplier invoice register and lines, product-document index |
| Knowledge (from `docs/` and `data/documents/`) | document chunks with embeddings and metadata (document, section, product, version, effective date, current or superseded); catalogue entries with embeddings |
| Cases | messages, cases, case parts, drafts, review decisions |
| Audit and evaluation | step log, runs (with model and prompt versions), per-email results, metrics |

Every run starts from the seeded state and replays emails in `received_at` order, because the emails share one time-ordered state (`data/emails/README.md`).

## 4. Retrieval
- **Two indexes** (`docs/KNOWLEDGE_SOURCES.md`): documents (passages the model reads and cites) and the catalogue (rows that code prices). Prices are never read from an index.
- **Chunks are document sections**, because the golden set labels the passages to retrieve at section level.
- **Filters in SQL before the model sees anything**: product, version (`applies_to_skus`), `status = current`, `customer_shareable = yes`.
- **Hybrid search**: keyword and vector results combined.
- **Baseline**: each category also runs with its own documents placed directly in the prompt, to show which categories need retrieval (EVALUATION.md).
- *Pending (phase 5)*: chunk size within sections, how many passages to retrieve, keyword/vector weighting, whether to re-rank.

## 5. Evaluation
- **Exact grading in code**: labels (exact set match), routes, flags, extracted fields, prices and totals, attachments, duplicate links.
- **Retrieval metrics** against the labelled passages: recall@5, citation correctness, correct version.
- **Reply quality**: Claude judges each reply against `reply_must_state` and the shared rubric. Judged failures are read by the user.
- **Splits**: `tune` for development; `held_out` decides. Every run is stored with its model and prompt versions so regressions show.
- **Classifier comparison**: Jev against the Decisions API on accuracy, latency, cost per email and consistency over three runs.

## 6. Constraints
- **Secrets** (OpenAI, TypeSafe, Anthropic, Google keys; Gmail OAuth files) live in `.env` or local files listed in `.gitignore`, never in the repository.
- **No sending.** Review mode is on for every category; the Gmail scopes exclude sending.
- **Arithmetic and rules are code**, never the model.
- **Everything runs locally**: Docker Compose for PostgreSQL; no cloud deployment in the MVP.
- **Cost and latency** are recorded per step and reported per run.
- **Access risk**: the Decisions API is new and its availability may be limited; the classifier interface is provider-neutral so either model can be used alone.
