# ARIA Project - Decision Log

**Version: 0.1 (Initial Plan)**
**Date: 2024-05-21**

| Decision ID | Decision                                                                              | Rationale                                                                                                                   |
| :---------- | :------------------------------------------------------------------------------------ | :-------------------------------------------------------------------------------------------------------------------------- |
| D-01        | **Use Python as the core language.**                                                  | Standard for AI/ML development with the most extensive libraries and community support.                                   |
| D-02        | **Adopt LangChain as the primary orchestration framework.**                           | Prevents reinventing the wheel for agent logic, memory management, and tool integration. Accelerates development.         |
| D-03        | **Start with OpenAI API, then move to a local LLM.**                                  | Prioritizes getting the core logic right with a powerful model first, before tackling the hardware/software challenge of local hosting. |
| D-04        | **Implement a dual-memory system: ChromaDB (Vector) and SQLite (Structured).**        | Directly addresses the user's need for both associative "memory" and factual data storage. This is a robust and scalable pattern. |
| D-05        | **Adopt a phased development plan starting with a CLI.**                              | Reduces initial complexity, allowing focus on the "brain" of ARIA. A UI can be built on a solid foundation later.       |
| D-06        | **Define "Priority Scale" and "Intensity Scale" as core concepts.**                     | Formalizes the user's key ideas for task management and proactive notifications, making them implementable features.  