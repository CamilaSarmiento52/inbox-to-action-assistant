# Roadmap

Status: drafted 2026-10-11; open to your changes. ✅ done · 🟡 in progress · ⬜ not started.

Each phase runs on its own branch with its own folder `specs/phases/phase-N-<name>/` (`plan.md`, `implement.md`, `validation.md`, `testing.md`) and follows plan → implement → validate before the next starts. Phases build one capability end to end and are measured against `docs/EVALUATION.md` on the JSONL test emails; the Gmail mailbox comes in once the pipeline is complete.

| # | Phase | Delivers | Done when | Status |
| --- | --- | --- | --- | --- |
| 0 | Documentation and golden set | SOPs, policies, classification guide, fictional records and documents, 344 reviewed test emails, anchor set, test plan | All reviewed; anchor set read by the user | 🟡 anchor set reading pending |
| 1 | Foundations | Project skeleton (uv, ruff, pytest, CI); PostgreSQL in Docker loaded from `data/`; the normalised message and the JSONL adapter; case and part tables; audit log; evaluation runner with stored runs | A run over the golden set records every email and grades a stub classifier | ⬜ |
| 2 | Classification | Jev and the OpenAI Decisions API (GPT-6 Luna), each as eight yes/no questions with thresholds tuned on `tune`; per-label precision and recall; latency, cost and consistency over three runs | 90% overall and 85% mixed on held-out | ⬜ |
| 3 | Quotations | First LangGraph specialist and OpenAI model choice; catalogue index and embedding model; product resolution (exact → fuzzy → semantic); pricing in code; prospects; reply drafting; Claude judge for the shared reply rubric | Quotation targets met; demo quotation ready for approval | ⬜ |
| 4 | Review and combined replies | Review screen (approve, edit, reject); parts merged into one reply with deduplicated attachments; route ranking | Mixed-request rules at 100% on the cases built so far | ⬜ |
| 5 | Documents and technical questions | Document index (section chunks, hybrid search, version filters); retrieval tuning; citations and attachments; no-RAG baseline | Documentation and retrieval targets met, including correct version 100% | ⬜ |
| 6 | Orders and complaints | Verification in code, status from records, order drafts, complaint preparation, safety handling | Verification and complaint targets met; zero disclosure to unverified senders | ⬜ |
| 7 | Invoices and onboarding | Invoice copies with ownership checks; supplier invoice extraction into the register (pdfplumber for text, Gemini for scans); account creation | Invoice, extraction and onboarding targets met; demo escalation works | ⬜ |
| 8 | Other, duplicates and injection | Other with sub-types; resend detection; injection flagging across all categories | Duplicates and injection at 100%; all eight categories in one run | ⬜ |
| 9 | Gmail intake | Gmail adapter, loader for the test mailbox, labels and drafts, connection tests; pending intake decisions taken | Every connection test in `END_TO_END_TESTING.md` §4 passes | ⬜ |
| 10 | End-to-end acceptance | All 344 through the test mailbox; parity with offline; results dashboard; demo | Held-out targets met through Gmail; parity on every email | ⬜ |

Order notes:
- Quotations come first after classification: the first capability chosen (MVP scope).
- Retrieval starts in phase 3 with the catalogue index, which product resolution needs; phase 5 adds the document index.
- The review screen comes before the remaining categories because every category depends on it; the decision on where replies are reviewed (END_TO_END_TESTING.md §6) is taken in phase 4.
- Each phase reruns the earlier phases' evaluations, so a regression is visible.
