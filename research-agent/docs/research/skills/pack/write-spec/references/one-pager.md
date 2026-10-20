# One-pager shapes (impact.com)

## Defaults

| Audience | Shape | Where |
|---|---|---|
| UX initiative (roadmap) | **UX short form** (below) | Confluence space `ux`, often under [UX Roadmap](https://impact.atlassian.net/wiki/spaces/ux/pages/6436978692/UX+Roadmap) |
| Cross-functional PM shaping | **Product Shaping** template | Copy structure from [Product Shaping One Pager Template](https://impact.atlassian.net/wiki/spaces/ITECH/pages/5044568069/Product+Shaping+One+Pager+Template); apply label `product-one-pager` |

Canonical product template purpose: problem, goals, approach, success metrics — align business, UX, Eng, Marketing. Skip solution-heavy “Approach” until the Designer is happy and has chatted with a PM unless the user asks for a full PRD.

## UX short form (preferred for write-spec)

Mirror existing UX one-pagers (e.g. Holistic Brand Experience Rethink):

1. **Problem / opportunity** — pains only; rank by severity; VoC when Verified
2. **Audience** — Brand / Partner / Shared + persona names when known
3. **Jobs-to-be-done** — bullets
4. **Success criteria** — measurable + Designer sign-off, then PM chat
5. **Scope** — In / Out
6. **Design deliverables** — e.g. mocks, prototype (placeholder OK)
7. **Research context** — links to Empathize sources / report
8. **Beliefs this rests on** — claim ids, confidence and n, copied from the
   Frame. This is the back-link `frame-maintenance` uses to rank a claim by
   exposure; without it a retired claim leaves live specs standing on nothing.

## Product Shaping sections (when expanding)

Metadata table: Target release, Epic, Document status, Owner, Designer, Tech lead, Tech writers, QA, PMM, Stakeholders, Eng/QA one-pager links.

Body: Problem/Opportunity → Goal → Competitive Intel (optional) → Approach → Critical Requirements & Release Plan (In/Out/Success) → Access Controls → Risks & Mitigations → Success Measurement + Exit Criteria by Phase.

## Anti-sycophancy checks before publish

- Is Goal actually a feature name? Rewrite to customer/business outcome.
- Is evidence single-source or low-N? Downgrade confidence in the doc.
- Missing marketplace side called out?
