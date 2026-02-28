# Agentic Researcher

A locally-running multi-node research agent powered by Mistral via Ollama. Give it any topic and it searches, judges, rewrites, and generates a full structured research report — entirely on your own machine.

---

## How It Works

```
User Query → Tool Selector → Search (Wikipedia / DuckDuckGo) → Router
                                        ↓ bad results
                                  Query Rewriter → Retry
                                        ↓ still failing
                                  Fallback to other tool
                                        ↓
                             Extractor → Reporter → Final Report
```

---

## Nodes

| Node | File | What it does |
|---|---|---|
| Tool Selector | `nodes/tool_selector.py` | LLM decides whether to use Wikipedia or DuckDuckGo |
| Search | `nodes/search.py` | Fetches Wikipedia page using LLM-based candidate matching |
| DuckDuckGo | `nodes/duckduckgo.py` | Searches the web for recent or practical topics |
| Router | `nodes/router.py` | Judges if search results are good enough to proceed |
| Query Rewriter | `nodes/query_rewriter.py` | LLM rewrites a failed query to get better results |
| Extractor | `nodes/extractor.py` | Extracts key points from search results |
| Reporter | `nodes/reporter.py` | Writes a full structured research report |

---

## Requirements

- Python 3.9+
- [Ollama](https://ollama.com/) running locally with Mistral pulled
- Internet connection for Wikipedia and DuckDuckGo search

---

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/tanushbuilds/agentic-researcher.git
cd agentic-researcher
```

**2. Install dependencies**
```bash
pip install ollama wikipedia-api wikipedia ddgs
```

**3. Pull Mistral**
```bash
ollama pull mistral
```

**4. Run**
```bash
python main.py
```

---

## Example

```
Enter your research topic: How to master Claude AI

Tool selected: DuckDuckGo
DuckDuckGo results good! Moving on...

=== FINAL REPORT (source: duckduckgo) ===
...
```

---

## Built With

- [Ollama](https://ollama.com/) — Local LLM inference
- [Mistral](https://mistral.ai/) — Language model
- [Wikipedia-API](https://pypi.org/project/Wikipedia-API/) — Wikipedia page fetching
- [wikipedia](https://pypi.org/project/wikipedia/) — Wikipedia candidate search
- [ddgs](https://pypi.org/project/ddgs/) — DuckDuckGo web search

---

## Roadmap

- [ ] Memory across sessions
- [ ] LangGraph implementation
- [ ] Multi-source search synthesis
- [ ] Web UI

---

<sub>Built by [@tanushbuilds](https://github.com/tanushbuilds) · 14 year old developer</sub>
