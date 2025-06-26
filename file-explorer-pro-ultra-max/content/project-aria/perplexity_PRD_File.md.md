<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" class="logo" width="120"/>

# PRD_File.md

## 1. Vision

Create **ARIA** (A Random Intelligent Assistant)—a privacy-first, lifelong AI companion that proactively improves a user’s productivity, well-being and growth. Unlike general chatbots, ARIA forms a persistent model of one individual, learns continuously from real-world signals and orchestrates specialized agents to act on the user’s behalf.

## 2. Objectives \& Key Results (OKRs)

| Objective | Key Results (12-month) |
| :-- | :-- |
| Deliver an on-device MVP | -  Text chat latency < 2 s round-trip[^1] -  Users rate answer relevance > 85% in weekly survey -  Local RAM footprint ≤ 6 GB on Raspberry Pi 5[^2] |
| Build trusted, context-aware memory | -  Retrieve correct past fact in blind test 8/10 times using vector recall[^3] |
| Demonstrate proactive health \& mood support | -  Detect at-risk emotional state with recall > 75% vs. manual labels using EmoNet[^4] |
| Automate daily tasks | -  Close-loop success for “schedule meeting” \& “pay bill” flows ≥ 90% |

## 3. Personas

1. **Solo developer (“Maker”)** – wants local, hackable AI.
2. **Busy professional (“Optimizer”)** – seeks scheduling \& task automation.
3. **Health-focused user (“Tracker”)** – values mood and bio-signal insights.

## 4. Core Features (V = version in roadmap)

| Feature | Description |
| :-- | :-- |
| Conversational Reasoning (V1) | Chat interface powered by GPT-4o or local Gemma fallback for low latency reasoning[^1][^2]. |
| Persistent Memory (V1) | Hybrid store: **Vector DB (Weaviate/Chroma)** for embeddings[^3][^5] + lightweight Postgres for structured facts; periodic summarisation to control context length[^6]. |
| Priority-Scale Task Manager (V1) | Queue tasks by numeric urgency; Redis Streams with multiple priority queues implements the **Priority Queue pattern**[^7]. |
| Multi-Agent Orchestration (V2) | Use AutoGen \& LangGraph to spawn specialized agents (Search, Planner, Executor) that collaborate[^8][^9]. |
| Emotion \& Health Monitor (V2) | Audio/vision models (LAION EmoNet, FER-2013 fine-tune) and wearables via HealthKit / Google Fit APIs to flag anomalies[^4][^10]. |
| Proactive Coaching \& Nudges (V3) | Reinforcement loop sends suggestions only when priority score crosses threshold; defers low-impact tips to “Daily Digest.” |
| Voice I/O (V3) | Whisper.cpp or Vosk for ASR; Coqui TTS or ElevenLabs for responses; local fallback for privacy[^2]. |
| Cross-Device Sync (V3) | End-to-end encrypted sync via LibSQL replication; optional cloud bucket for attachments. |
| Plugin/Tool API (V4) | Secure plugin sandbox so community can add smart-home, finance or metaverse hooks. |
| Ethics \& Safety Controls (V1+) | On-device policy checks, user-reviewable memory, “forget” command, explicit consent for each data source[^11]. |

## 5. Architecture Snapshot

1. **Client layer:**
    - CLI (Node.js + Ink) → earliest MVP
    - React Native app (Phase 3)
2. **Gateway:** FastAPI (async) exposes `/chat`, `/tasks`, `/sensor`.
3. **Inference services:**
    - Remote GPT-4o via Azure OpenAI with rate limiter[^1]
    - Ollama runtime hosting Gemma-2B, DeepSeek-R1 for offline[^2][^12].
4. **Agent Orchestrator:** LangGraph running inside worker pods.
5. **Memory stores:**
    - Weaviate docker with HNSW index for embeddings[^3]
    - PostgreSQL for structured entities
6. **Task queues:** Redis Streams (three priority streams).
7. **Data ingestion:**
    - Webhooks (Gmail, Calendar, Notion)
    - Wearable bridge (BLE → MQTT)
8. **Security:**
    - Age-encrypted vault for secrets
    - Device-bound E2EE keys
9. **Deployment:** Docker Compose for dev; K3s or RasPi swarm for home-lab; GPU-optional[^2][^13].

*[see diagram in /docs/architecture.png]*

## 6. Tech-Stack Decision Highlights

| Layer | Choice | Rationale |
| :-- | :-- | :-- |
| Agent framework | LangChain + LangGraph | Mature, modular, graph-based control flow[^9]. |
| Multi-agent runtime | Microsoft AutoGen | Structured role chat \& tool use; integrates with LangGraph[^8]. |
| LLMs | GPT-4o (cloud) / Gemma-2B-It (local) | Best reasoning vs. GPU-lite fallback[^1][^2]. |
| Embedding model | E5-Mistral (4096 ctx) | Open-source, high recall in RAG pipelines. |
| Vector DB | Weaviate (Rust WAL) or Chroma | Self-hosted, GPU-accelerated ANN search[^3]. |
| Scheduling | Redis Streams | Supports strict priority semantics \& consumer groups[^7]. |
| Emotion model | LAION EmoNet release 2025-06[^4] | Open-source, multi-modal EQ benchmark leader. |
| Speech | OpenAI Whisper.cpp or Vosk | On-device, no network traffic. |
| Mobile | React Native + Expo | Single codebase across Android/iOS. |

## 7. Data Flow (Happy Path)

1. User types “Remind me to drink water”.
2. FastAPI forwards to Orchestrator.
3. Planner-Agent tags `task`, extracts `drink water`, urgency=4.
4. Task enqueued in medium-priority stream; confirmation reply.
5. When queue consumer hits due time, Notification-Agent fires mobile push.

## 8. Privacy \& Compliance

- Default “local-first”; cloud calls routed only when user opts-in[^2][^14].
- Face / voice samples processed on device; embeddings stored encrypted.
- GDPR-style data export \& purge commands.


## 9. MVP Scope (Version 1, 4 months)

1. Local FastAPI service with CLI.
2. GPT-4o API w/ fallback.
3. Vector memory + summarisation.
4. Priority queue \& simple reminder agent.
5. Basic settings UI.

## 10. Success Metrics

- < 2 s median response latency (local).
- > 85% user satisfaction in pilot survey.
- Zero P0 privacy incidents.
- Memory recall BLEU > 0.6 (blind eval).


## 11. Risks \& Mitigations

| Risk | Mitigation |
| :-- | :-- |
| LLM cost spike | Local fallback; token budgeting. |
| Wearable API changes | Abstract adapters \& open-source community patches. |
| Privacy breach via plugins | Sandbox, code-signing, permission prompts. |

# TODO_File.md

| Phase | Task ID | Task Description | Status | Priority | Depends On |
| :-- | :-- | :-- | :-- | :-- | :-- |
| 0 Planning | 0-1 | Set up mono-repo (pnpm + Poetry) | Done | High | — |
| 0 Planning | 0-2 | Define coding guidelines \& CI (GitHub Actions) | In Progress | High | 0-1 |
| 1 MVP | 1-1 | Dockerize FastAPI skeleton | Not Started | High | 0-2 |
| 1 MVP | 1-2 | Integrate GPT-4o \& Gemma switcher | Not Started | High | 1-1 |
| 1 MVP | 1-3 | Implement vector DB memory (Weaviate) | Not Started | High | 1-1 |
| 1 MVP | 1-4 | Implement sliding-window → summary memory routine | Not Started | Medium | 1-3 |
| 1 MVP | 1-5 | Priority queue (Redis Streams) | Not Started | High | 1-1 |
| 1 MVP | 1-6 | CLI chat + reminders | Not Started | High | 1-2,1-5 |
| 1 MVP | 1-7 | Unit + load tests | Not Started | High | 1-6 |
| 1 MVP | 1-8 | E2EE local secret vault | Not Started | Medium | 1-1 |
| 2 Context+Agents | 2-1 | Adopt LangGraph for orchestrator | Not Started | High | 1-7 |
| 2 Context+Agents | 2-2 | AutoGen multi-agent sample (Search \& Planner) | Not Started | High | 2-1 |
| 2 Context+Agents | 2-3 | Implement task-executor agent | Not Started | High | 2-2 |
| 2 Context+Agents | 2-4 | Unit tests for agent loop | Not Started | High | 2-3 |
| 2 Context+Agents | 2-5 | Docker Compose update with worker pool | Not Started | Medium | 2-3 |
| 2 Context+Agents | 2-6 | Telemetry dashboard (Prometheus + Grafana) | Not Started | Low | 2-5 |
| 3 Health/Mobile | 3-1 | Integrate EmoNet model (voice) | Not Started | High | 1-7 |
| 3 Health/Mobile | 3-2 | BLE wearable bridge (Heart Rate) | Not Started | High | 3-1 |
| 3 Health/Mobile | 3-3 | React Native chat UI | Not Started | High | 1-6 |
| 3 Health/Mobile | 3-4 | Push-notification service | Not Started | Medium | 3-3 |
| 3 Health/Mobile | 3-5 | Voice ASR (Whisper.cpp) | Not Started | Medium | 3-3 |
| 4 Proactive \& Plugins | 4-1 | Daily Digest scheduler | Not Started | Medium | 2-3 |
| 4 Proactive \& Plugins | 4-2 | Plugin sandbox API \& docs | Not Started | High | 2-3 |
| 4 Proactive \& Plugins | 4-3 | Early adopter plugin—Google Calendar | Not Started | Medium | 4-2 |
| 5 Hardening | 5-1 | Threat-model \& pen-test audit | Not Started | High | 3-4,4-3 |
| 5 Hardening | 5-2 | Release candidate 1.0 packaging | Not Started | High | 5-1 |

Legend—Status: Done / In Progress / Not Started. Priority: High (critical path) / Medium / Low.

# log_file.md

| Change \# | Decision / Change Made | Reason | Date |
| :-- | :-- | :-- | :-- |
| 1 | Adopt **LangGraph + AutoGen** instead of custom agent code | Leverage 2025 mature agent frameworks, faster path to multi-agent capabilities[^1][^8][^9] | 26-Jun-25 |
| 2 | Use **Weaviate** (or Chroma) for memory instead of plain SQLite | Vector DBs optimise semantic recall and RAG pipelines[^3] | 26-Jun-25 |
| 3 | Chosen **Gemma-2B / DeepSeek-R1** as local fallback LLM | Runs on Raspberry Pi 5 with 8 GB RAM, satisfies privacy requirement[^2][^12] | 26-Jun-25 |
| 4 | Emotion detection via **LAION EmoNet** (open-source) | Best-in-class EQ benchmark; avoids paid APIs[^4] | 26-Jun-25 |
| 5 | Task prioritisation implemented with **Redis Streams** (multi-queue)** | Aligns with Azure Priority Queue pattern, supports consumer groups[^7] | 26-Jun-25 |
| 6 | Voice I/O stack switched to Whisper.cpp + Coqui TTS | Wholly on-device, no vendor lock-in | 26-Jun-25 |
| 7 | Deployment baseline = Docker Compose; optional K3s | Simplifies local + home-lab installations | 26-Jun-25 |

All deviations from the original high-level idea have been logged for future traceability.

<div style="text-align: center">⁂</div>

[^1]: https://www.fluid.ai/blog/top-5-ai-agent-frameworks-for-2025

[^2]: https://blog.whiteprompt.com/building-a-private-ai-assistant-with-local-llms-a-practical-guide-1725647901d3

[^3]: https://www.datacamp.com/blog/the-top-5-vector-databases

[^4]: https://techcrunch.com/2025/06/24/new-data-highlights-the-race-to-build-more-empathetic-language-models/

[^5]: https://www.gocodeo.com/post/what-is-a-vector-database-and-why-its-essential-for-ai-in-2025

[^6]: https://mlpills.substack.com/p/issue-60-memory-in-conversational?r=n1n50

[^7]: https://learn.microsoft.com/en-us/azure/architecture/patterns/priority-queue

[^8]: https://metadesignsolutions.com/langchain-agents-vs-autogen-agents-choosing-the-right-ai-agent-framework-in-2025/

[^9]: https://blogs.infoservices.com/artificial-intelligence/langchain-multi-agent-ai-framework-2025/

[^10]: https://www.softude.com/blog/ai-and-wearable-technology-why-they-are-perfect-pair-in-the-healthcare

[^11]: https://www.geeky-gadgets.com/setup-and-run-ai-models-locally-and-securely/

[^12]: https://dify.ai/blog/dify-deepseek-deploy-a-private-ai-assistant

[^13]: https://ai.icai.org/usecases_details.php?id=71

[^14]: https://www.reddit.com/r/selfhosted/comments/1lirihv/im_building_a_100_private_local_ai_assistant_but/

[^15]: Problem_Statement_2.md

[^16]: https://tech-stack.com/blog/ai-app-ideas-13-for-2025/

[^17]: https://www.netguru.com/blog/ai-agent-tech-stack

[^18]: https://www.biz4group.com/blog/how-to-create-a-personal-ai-assistant

[^19]: https://dev.to/copilotkit/the-tech-stack-for-building-ai-apps-in-2025-12l9

[^20]: https://texta.ai/blog/ai-technology/ai-personal-assistants-in-2025-revolutionizing-the-way-you-manage-your-life

[^21]: https://www.iarj.in/index.php/ijrase/article/view/406

[^22]: https://dev.to/ryder_andrew/the-future-of-digital-companionship-ai-conversationalists-in-2025-1l7k

[^23]: https://www.kaufbei.tv/magazin/en/news-and-reviews/ai-assistants-what-s-new-in-2025/

[^24]: https://www.edenai.co/post/best-emotion-detection-apis

[^25]: https://www.tavus.io/post/emotional-ai

[^26]: https://research.aimultiple.com/emotional-ai-examples/

[^27]: https://www.forasoft.com/blog/article/emotional-analysis-machine-learning

[^28]: https://www.linkedin.com/pulse/may-edition-2025-imagevision-ai-ddcec

[^29]: https://arxiv.org/pdf/2102.10985.pdf

[^30]: https://lakefs.io/blog/12-vector-databases-2023/

[^31]: https://www.shakudo.io/blog/top-9-vector-databases

[^32]: https://www.youtube.com/watch?v=g55GusplWao

[^33]: https://dataconomy.com/2024/09/25/ai-real-time-data-processing-an-overview/

[^34]: https://www.andela.com/blog-posts/collaborative-intelligence-in-multiagent-systems-with-python

[^35]: https://celerdata.com/glossary/best-vector-databases

[^36]: https://www.shakudo.io/blog/top-9-ai-agent-frameworks

[^37]: https://www.turing.com/resources/ai-agent-frameworks

[^38]: https://blog.gopenai.com/openais-new-assistants-api-v2-2e898a3cf77c?gi=4d688573b63a

[^39]: https://texta.ai/blog/ai-technology/the-ultimate-guide-to-building-an-ai-personal-assistant-in-python

[^40]: https://datahub.io/@donbr/langgraph-unleashed/agent-platform-ecosystem

[^41]: https://zapier.com/blog/best-ai-scheduling/

[^42]: https://devpost.com/software/jarvis-4o3yeq

[^43]: https://vertu.com/ai-tools/top-ai-companion-apps-2025/

[^44]: https://github.com/arawind-s/Contextual-Memory-for-AI-Systems

[^45]: https://media.bitpipe.com/io_32x/io_320797/item_2847135/h20028-digital-assistants-design-guide.pdf

[^46]: https://www.linkedin.com/learning/advanced-data-processing-batch-real-time-and-cloud-architectures-for-ai/characteristics-of-realtime-ai

[^47]: https://www.restack.io/p/multi-agent-systems-answer-simulating-with-python-cat-ai

[^48]: https://www.youtube.com/watch?v=LQ5xtsp7gYo

[^49]: https://www.restack.io/p/customizable-ai-user-interfaces-answer-documentation-best-practices-python-ai-cat-ai

[^50]: https://www.scirp.org/journal/paperinformation?paperid=132006

[^51]: https://peerj.com/articles/cs-2531.pdf

