I’m mapping the project from the repo summary first, then I’ll trace the main user flows from the client into the server so I can answer where the core logic lives and what processes text behind the scenes.I’m loading the relevant project-analysis skills now so the architecture walkthrough stays grounded in the repo’s frontend and backend patterns.

Read skill [frontend-patterns](file:///c%3A/Users/Adarshere/.claude/skills/frontend-patterns/SKILL.md?vscodeLinkType%3Dskill#1-1), lines 1 to 240

Read skill [backend-patterns](file:///c%3A/Users/Adarshere/.claude/skills/backend-patterns/SKILL.md?vscodeLinkType%3Dskill#1-1), lines 1 to 240

Read skill [python-patterns](file:///c%3A/Users/Adarshere/.claude/skills/python-patterns/SKILL.md?vscodeLinkType%3Dskill#1-1), lines 1 to 240

I have the general frontend/backend guidance loaded. Next I’m reading the repo’s own entry points and route files so I can explain the real request flow instead of giving a generic architecture summary.

Read [](file:///d%3A/Github_Desktop/Bhashini/Glossaries/Glossary_App/src/repomix-output.xml#1-1), lines 1 to 260

Read [](file:///d%3A/Github_Desktop/Bhashini/Glossaries/Glossary_App/src/client/docs/high_level_architecture.md)

Read [](file:///d%3A/Github_Desktop/Bhashini/Glossaries/Glossary_App/src/server/docs/high_level_architecture.md)

Read memory

I’ve confirmed the app is a Next.js client talking to a FastAPI server, but I still need the concrete call chain. I’m reading the main pages, API client, server router, and processing modules now to trace exactly what happens to uploaded text.

Read [](file:///d%3A/Github_Desktop/Bhashini/Glossaries/Glossary_App/src/client/src/lib/api.ts#1-1), lines 1 to 320

Read [](file:///d%3A/Github_Desktop/Bhashini/Glossaries/Glossary_App/src/client/src/app/page.tsx#1-1), lines 1 to 260

Read [](file:///d%3A/Github_Desktop/Bhashini/Glossaries/Glossary_App/src/client/src/app/upload/page.tsx)

Read [](file:///d%3A/Github_Desktop/Bhashini/Glossaries/Glossary_App/src/client/src/app/batches/page.tsx)

Read [](file:///d%3A/Github_Desktop/Bhashini/Glossaries/Glossary_App/src/client/src/app/batches/%5Bid%5D/page.tsx#1-1), lines 1 to 360

Read [](file:///d%3A/Github_Desktop/Bhashini/Glossaries/Glossary_App/src/client/src/app/export/page.tsx)

Read [](file:///d%3A/Github_Desktop/Bhashini/Glossaries/Glossary_App/src/server/app/main.py)

Read [](file:///d%3A/Github_Desktop/Bhashini/Glossaries/Glossary_App/src/server/api/routes/batches.py#1-1), lines 1 to 420

The client pages confirm the user flow. I’m now tracing the internal stores and server modules, because that is where the real behavior sits: request dispatch, state polling, extraction, translation, glossary generation, Mongo persistence, and export.

Read [](file:///d%3A/Github_Desktop/Bhashini/Glossaries/Glossary_App/src/client/src/store/batchStore.ts)

Read [](file:///d%3A/Github_Desktop/Bhashini/Glossaries/Glossary_App/src/client/src/store/glossaryStore.ts#1-1), lines 1 to 400

Read [](file:///d%3A/Github_Desktop/Bhashini/Glossaries/Glossary_App/src/client/src/store/settingsStore.ts)

Read [](file:///d%3A/Github_Desktop/Bhashini/Glossaries/Glossary_App/src/server/modules/batch_processor.py#1-1), lines 1 to 420

Read [](file:///d%3A/Github_Desktop/Bhashini/Glossaries/Glossary_App/src/server/modules/extractor.py)

Read [](file:///d%3A/Github_Desktop/Bhashini/Glossaries/Glossary_App/src/server/modules/translator.py)

Read [](file:///d%3A/Github_Desktop/Bhashini/Glossaries/Glossary_App/src/server/modules/glossary_engine.py#1-1), lines 1 to 420

Read [](file:///d%3A/Github_Desktop/Bhashini/Glossaries/Glossary_App/src/server/modules/mongo_connector.py#1-1), lines 1 to 420

I’ve got the main path from upload to glossary generation. I’m filling the remaining gaps now: auxiliary routes, preprocessing/postprocessing, chunking, export, and the exact client API surface so I can tell you which pieces are real APIs versus internal services.

Searched for regex `@router\.(get|post|patch|delete)\(` (`**/src/server/api/routes/**`), 23 results

Read [](file:///d%3A/Github_Desktop/Bhashini/Glossaries/Glossary_App/src/server/api/routes/metrics.py)

Read [](file:///d%3A/Github_Desktop/Bhashini/Glossaries/Glossary_App/src/server/api/routes/postprocessors.py#1-1), lines 1 to 340

Read [](file:///d%3A/Github_Desktop/Bhashini/Glossaries/Glossary_App/src/server/api/routes/health.py)

Read [](file:///d%3A/Github_Desktop/Bhashini/Glossaries/Glossary_App/src/server/modules/preprocessor.py#1-1), lines 1 to 420

Read [](file:///d%3A/Github_Desktop/Bhashini/Glossaries/Glossary_App/src/server/modules/postprocessor.py#1-1), lines 1 to 420

Read [](file:///d%3A/Github_Desktop/Bhashini/Glossaries/Glossary_App/src/server/utils/chunker.py)

Read [](file:///d%3A/Github_Desktop/Bhashini/Glossaries/Glossary_App/src/server/utils/export.py)

I now have the backend processing modules. I’m pulling the remaining route definitions and the client’s exported API functions so I can give you a clean map of “screen -> store -> API route -> backend service/module.”

Read [](file:///d%3A/Github_Desktop/Bhashini/Glossaries/Glossary_App/src/server/api/routes/batches.py#420-420), lines 420 to 666

Searched for text `export async function ` (`**/src/client/src/lib/api.ts`), 24 results

Read [](file:///d%3A/Github_Desktop/Bhashini/Glossaries/Glossary_App/src/client/src/store/postProcessorStore.ts)

Read [](file:///d%3A/Github_Desktop/Bhashini/Glossaries/Glossary_App/src/client/src/store/metricsStore.ts)

Read [](file:///d%3A/Github_Desktop/Bhashini/Glossaries/Glossary_App/src/server/config.py)

Read [](file:///d%3A/Github_Desktop/Bhashini/Glossaries/Glossary_App/src/client/src/lib/constants.ts)

I have enough to explain the system. I’m grabbing precise locations for the core entry points now so the walkthrough points you to the right files to read first instead of making you hunt through the repo.

Searched for regex `def create_app|include_router|startup_event|uvicorn.run` (`**/src/server/app/main.py`), 7 results

Searched for regex `export async function createBatch|export async function startBatch|export async function getGlossary|export async function exportGlossary|export async function getSystemMetrics|export async function applyRules` (`**/src/client/src/lib/api.ts`), 6 results

Searched for regex `createBatch: async|fetchBatches: async|startBatch: async|fetchGlossary: async|fetchPartialGlossary: async|applyRulesToGlossary: async|checkApiHealth: async` (`**/src/client/src/store/**`), 7 results

Searched for regex `async def create_new_batch|async def list_batches|async def start_batch_processing|async def get_glossary|async def export_glossary|async def get_combined_glossary|async def export_all_glossaries|async def update_term|async def search_terms` (`**/src/server/api/routes/batches.py`), 9 results

Searched for regex `def create_batch|def process_single_batch|def get_batch_info|def get_all_batch_info|def get_batch_glossary|def cancel_batch` (`**/src/server/modules/batch_processor.py`), 6 results

Searched for regex `def extract_text|def extract_from_pdf|def extract_from_docx|def extract_from_txt|def extract_from_json` (`**/src/server/modules/extractor.py`), 5 results

Searched for regex `def translate_text|def translate_chunk|def translate_with_retry` (`**/src/server/modules/translator.py`), 3 results

Searched for regex `def create_prompt|def generate_glossary_chunk|def generate_glossary|def call_gemma_api|def poll_nvcf_result` (`**/src/server/modules/glossary_engine.py`), 5 results

Searched for regex `class TextQualityAnalyzer|def detect_language|class BilingualSeparator|class TextSanitizer` (`**/src/server/modules/preprocessor.py`), 4 results

Searched for regex `class JSONRepair|def repair_and_parse|class GlossaryValidator|def deduplicate_entries` (`**/src/server/modules/postprocessor.py`), 4 results

Searched for regex `def init_batch_in_mongo|def update_batch_status_mongo|def push_chunk_entries|def save_batch_to_mongo|def get_batch_from_mongo|def get_batch_glossary_from_mongo|def update_term_in_mongo|def search_batch_terms` (`**/src/server/modules/mongo_connector.py`), 8 results

Searched for regex `@router.get\("/metrics|@router.post\("/postprocessor/apply|@router.get\("/health` (`**/src/server/api/routes/**`), 3 results

One last gap is the live-state layer. I’m reading the Redis helper so I can distinguish transient runtime state from persisted Mongo data and explain why the UI can show partial progress while a batch is still running.

Searched for regex `def set_batch_status|def set_batch_data|def get_batch_data|def set_batch_error|def set_chunk_status|def get_chunk_summary|def is_batch_active|def load_from_redis` (`**/src/server/utils/redis_client.py`), 8 results

Read [](file:///d%3A/Github_Desktop/Bhashini/Glossaries/Glossary_App/src/server/utils/redis_client.py#1-1), lines 1 to 360

I found two architecture details that matter a lot: the docs are a bit stale, and the runtime is more in-process than the high-level docs suggest. I’m reading the LLM provider abstraction now so I can accurately explain the optional post-processing path too.

Searched for regex `def generate_with_llm|provider|gemma|openai` (`**/src/server/utils/llm_provider.py`), 69 results

Searched for regex `useBatchStore|useGlossaryStore|usePostProcessorStore|useMetricsStore` (`**/src/client/src/components/**`), 10 results

Read [](file:///d%3A/Github_Desktop/Bhashini/Glossaries/Glossary_App/src/server/utils/llm_provider.py)

The call chain is complete now. I’m checking the combined-glossary UI once so I can tell you where the post-processing rules fit in from the user’s point of view, not just on the server side.

Read [](file:///d%3A/Github_Desktop/Bhashini/Glossaries/Glossary_App/src/client/src/components/feature/export/TotalGlossariesSection.tsx#1-1), lines 1 to 260

Read [](file:///d%3A/Github_Desktop/Bhashini/Glossaries/Glossary_App/src/client/src/components/feature/postprocessor/PostProcessorSection.tsx)

**Big Picture**

This project is a 2-tier app, not a monolith with many hidden layers.

The frontend is a Next.js App Router app that renders pages and manages client state with Zustand stores, then calls the Python backend directly through fetch wrappers in api.ts. The backend is a FastAPI app created in main.py, with routers for batches, metrics, health, and post-processors mounted in main.py.

There is no separate Next.js API layer in this repo. The browser talks straight to FastAPI using the base URL defined in constants.ts.

One important correction to the docs: the actual frontend state layer is mostly Zustand, not React Context. The real state entry points are batchStore.ts, glossaryStore.ts, settingsStore.ts, metricsStore.ts, and postProcessorStore.ts.

Also, the runtime is more in-process than the docs imply. Batch execution is started with FastAPI BackgroundTasks in batches.py, and live batch state is primarily kept in memory with optional Redis sync in redis_client.py. MongoDB is the durable store for batch/glossary data in mongo_connector.py.

**What Happens When The User Uses It**

From the user side, the main screens are:
page.tsx
page.tsx
page.tsx
page.tsx

The end-to-end flow is:

1. User uploads a source file and optionally a reference file on page.tsx.
2. That page calls the batch store in batchStore.ts.
3. The store calls the client API function createBatch in api.ts.
4. The browser sends POST /api/v1/batches to FastAPI, handled by batches.py.
5. FastAPI calls create_batch in batch_processor.py.
6. That function stores metadata and raw file bytes in runtime state, marks the batch pending, and initializes a Mongo document via mongo_connector.py.

At that point the batch exists, but processing has not started yet.

When the user clicks Start:

1. The client calls startBatch from api.ts.
2. FastAPI handles POST /api/v1/batches/{id}/start in batches.py.
3. FastAPI schedules process_single_batch from batch_processor.py.

That processing pipeline is the real heart of the app:

1. Extract text from uploaded files using extractor.py.
2. Decide how to get Hindi reference text:
   Path A: user supplied a Hindi reference file.
   Path B: source file is bilingual, so Hindi is split out with preprocessor.py.
   Path C: source is mostly English, so Bhashini translation becomes the fallback Hindi reference.
3. Translate English chunks to Hindi via Bhashini in translator.py.
4. Run glossary extraction against Original + Reference + Bhashini output using the Gemma prompt pipeline in glossary_engine.py.
5. Repair malformed LLM JSON with postprocessor.py.
6. Persist chunk-level and final results into Mongo with mongo_connector.py and mongo_connector.py.
7. Update live progress/status through the in-memory/Redis helper in redis_client.py.

The status progression is:
pending -> extracting -> translating -> auditing -> done or error

While this is running, the UI polls:
- the batch list/detail using batch store calls from batchStore.ts
- the glossary endpoint, including partial glossary during processing, from glossaryStore.ts

That is why the batch detail page can show partial terms before the job finishes. The detail page explicitly fetches partial glossary while processing in page.tsx.

**Which APIs Are Called**

From frontend to backend, the important real HTTP calls are:

- POST /api/v1/batches -> create batch in batches.py
- GET /api/v1/batches -> list batches in batches.py
- GET /api/v1/batches/{id} -> batch detail in batches.py
- POST /api/v1/batches/{id}/start -> start processing in batches.py
- GET /api/v1/batches/{id}/glossary -> final or partial glossary in batches.py
- PATCH /api/v1/batches/{id}/terms/{term_id} -> term edits in batches.py
- GET /api/v1/batches/{id}/terms -> server-side search/filter in batches.py
- GET /api/v1/batches/{id}/export -> per-batch export in batches.py
- GET /api/v1/batches/glossaries/combined -> combined glossary in batches.py
- GET /api/v1/batches/glossaries/export-all -> combined export in batches.py
- GET /api/v1/metrics -> system metrics in metrics.py
- GET /health -> health check in health.py
- POST /api/v1/postprocessor/apply -> apply LLM post-processing rules in postprocessors.py

From backend to external services, the important non-local calls are:

- Bhashini translation API from translator.py
- NVIDIA NVCF Gemma endpoint from glossary_engine.py
- Optional rule-based post-processing also goes through Gemma via llm_provider.py

So yes, there are two kinds of “API” in play:
- internal HTTP APIs between browser and FastAPI
- external service APIs from FastAPI to Bhashini and Gemma

**Which Files “Handle The Text”**

If your question is “where is the actual text work happening?”, these are the key files:

- Text extraction from PDF/DOCX/TXT/JSON: extractor.py
- Language detection and bilingual split: preprocessor.py and preprocessor.py
- Text chunking: chunker.py and chunker.py
- Bhashini translation: translator.py
- Gemma prompt and glossary generation: glossary_engine.py and glossary_engine.py
- LLM JSON cleanup and dedup logic: postprocessor.py and postprocessor.py
- Mongo persistence and term update/search: mongo_connector.py and mongo_connector.py

If you want to improve extraction quality, start with extractor.py.

If you want to improve translation behavior, start with translator.py.

If you want to change what terms get extracted, the most important file is glossary_engine.py.

If you want to improve noisy OCR/bilingual input handling, focus on preprocessor.py.

If you want to change how results are cleaned up after the LLM responds, use postprocessor.py.

**Where You Should Work**

If you are trying to change UI/UX:
- Start in page.tsx, page.tsx, page.tsx, and feature components under feature

If you are trying to change the frontend-backend contract:
- Start in api.ts and batches.py

If you are trying to change processing flow:
- Start in batch_processor.py

If you are trying to change persistence or term review/search:
- Start in mongo_connector.py

If you are trying to change progress handling or live status:
- Start in redis_client.py

If you are trying to change combined glossary export or post-processing:
- UI: TotalGlossariesSection.tsx and PostProcessorSection.tsx
- Server: postprocessors.py and llm_provider.py

Do not work in repomix-output.xml. That file is only a packed snapshot of the repo for analysis, not the source of truth.

**Important Observations**

A few things matter when you reason about this codebase:

- The “worker” is not a separate queue system like Celery. Processing is started as an in-process FastAPI background task in batches.py.
- Live state is memory-first, Redis-second, as implemented in redis_client.py. So Redis is helpful, but not the primary runtime source.
- MongoDB is the long-term source of truth for saved batches and glossary terms, and batch info overlays live Redis/in-memory status on top of Mongo in batch_processor.py.
- The combined glossary endpoints currently do not truly deduplicate, even though the UI text suggests unique terms. The dedup logic is commented out in batches.py and batches.py.

If you want, I can next give you one of these:
1. a screen-to-API map
2. a backend sequence diagram for one batch
3. a “read these 10 files first” onboarding order
