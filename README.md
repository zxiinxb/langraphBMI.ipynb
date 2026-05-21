# 🦜🔗 LangGraph Practice Lab

A clean, minimal repository documenting my hands-on journey learning and practicing the core fundamentals of **LangGraph** to build stateful, resilient AI workflows.

---

## ⚙️ Key Pillars of LangGraph & Implementation

LangGraph is built to move past linear pipelines into robust, controllable graph architectures. Here is how these core capabilities are implemented using the framework's native Python classes and functions:

### 1. Core Mechanics
* **State**: Structured using standard Python dictionaries, `Pydantic` models, or `TypedDict`. State fields are updated using specific reducer annotations like `Annotated[list, add_messages]`.
* **Nodes & Edges**: Nodes are standard Python functions added to the graph using `.add_node("node_name", function)`. Control flow connections are defined using `.add_edge("from_node", "to_node")`.
* **Conditional Routing**: Implemented using `.add_conditional_edges()`. This takes a routing function that analyzes the current state and returns a string pointing to the next node destination.

### 2. Advanced Control Flow
* **Persistence (Memory)**: Enabled by compiling the graph with a checkpointer mechanism, such as `MemorySaver()` (for in-memory tracking) or `PostgresSaver()`. Threads are managed via the `thread_id` key in the run configuration dictionary.
* **Human-in-the-Loop**: Configured by adding the `interrupt_before` or `interrupt_after` parameter directly inside the `.compile()` function. The graph automatically pauses execution, awaiting an external update via `.update_state()`.
* **Fault Tolerance**: Handled by passing standard python exception handling strategies or configuring explicit node retries directly within the workflow components.
* **Observability**: Automatically initiated by setting the system environment variables for LangSmith (`LANGCHAIN_TRACING_V2="true"`), allowing deep, visual node-by-node debugging without modifying the Python source code.
* **Event-Driven Execution**: Handled at runtime using the `.stream()` or `.astream_events()` async methods on the compiled graph instance to yield granular chunk payloads as the graph processes steps.

---

## 📂 Project Structure

```text
.
├── basic_graphs/          # Getting started with graph building
│   ├── simple_chain.py    # Standard sequential flow using StateGraph
│   └── cyclic_agent.py    # Basic agent using loops and conditional routing
├── requirements.txt       # Core framework dependencies
└── README.md              # Repository documentation
