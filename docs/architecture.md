# BillLens Architecture

## Overview

BillLens is an AI-powered parliamentary research assistant that helps citizens understand what the UK Parliament has discussed, proposed, voted on, and enacted.

Instead of requiring users to search hundreds of parliamentary documents manually, BillLens combines parliamentary data, legislation data, retrieval systems, and AI reasoning to produce evidence-backed answers.

## High-Level Architecture

```text
                    ┌──────────────────┐
                    │      User        │
                    │                  │
                    │ "What happened   │
                    │  with housing?"  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   BillLens API   │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │     Planner      │
                    │                  │
                    │ Understands the  │
                    │ question and     │
                    │ creates a plan   │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │    Researcher    │
                    └────────┬─────────┘
                             │
             ┌───────────────┼────────────────┐
             │               │                │
             ▼               ▼                ▼
       ┌───────────┐   ┌───────────┐   ┌───────────┐
       │ Parliament│   │    Lex    │   │  Hansard  │
       │    API    │   │   API     │   │   Data    │
       └─────┬─────┘   └─────┬─────┘   └─────┬─────┘
             │               │                │
             └───────────────┼────────────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │    Retrieval     │
                    │                  │
                    │ BM25             │
                    │ Semantic Search  │
                    │ Hybrid Search    │
                    │ Reranking        │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │     Verifier     │
                    │                  │
                    │ Checks claims    │
                    │ against evidence │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Answer Generator │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Evidence-backed  │
                    │ BillLens Answer  │
                    └──────────────────┘
