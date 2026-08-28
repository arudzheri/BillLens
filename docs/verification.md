
---

# `docs/verification.md`

This is particularly important for BillLens because it explains **why the system is trustworthy**.

```markdown
# BillLens Verification

## Purpose

The verification layer attempts to prevent BillLens from presenting unsupported claims as facts.

This is one of the core design principles of the project.

## The Problem

A language model may generate a plausible statement even when the retrieved evidence does not support it.

For example:

```text
Evidence:

"A housing bill was introduced."

Bad AI answer:

"Parliament passed the housing bill into law."
