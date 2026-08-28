
---

# `docs/data-sources.md`

```markdown
# BillLens Data Sources

BillLens is designed around authoritative and traceable parliamentary and legislative sources.

## UK Parliament

The UK Parliament is the primary source for parliamentary information.

Potential data includes:

- MPs
- Members
- Debates
- Parliamentary questions
- Bills
- Votes
- Committees
- Parliamentary proceedings

BillLens should prefer first-party parliamentary data whenever available.

## Lex

Lex provides an API-oriented interface for UK legal information and is used by BillLens as a legislation research source.

Repository:

https://github.com/i-dot-ai/lex

BillLens uses Lex to help retrieve legal and legislative information relevant to user questions.

## Hansard

Hansard contains records of parliamentary debates and proceedings.

BillLens can use Hansard-related data to identify:

- What MPs said
- When subjects were discussed
- Who raised particular issues
- Parliamentary debate history

## Source Priority

BillLens should generally prioritize sources in this order:

```text
1. Primary parliamentary source
2. Primary legislation source
3. Official parliamentary publication
4. Trusted structured dataset
5. Secondary source
