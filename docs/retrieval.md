
---

# `docs/retrieval.md`

```markdown
# BillLens Retrieval System

## Overview

Retrieval is responsible for finding evidence relevant to a user's question.

BillLens uses a hybrid retrieval strategy.

```text
Question
   |
   +----> BM25
   |
   +----> Semantic Search
   |
   +----> Hybrid Ranking
             |
             v
          Reranker
             |
             v
        Top Evidence
