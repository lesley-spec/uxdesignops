# Re-running the measure

The point is comparability. Everything here protects it.

---

## Re-run, do not rebuild

Open the original insight and run it. Do not write a new query that looks like
it: a rebuilt funnel quietly differs in a step definition, a filter or a
window, and the difference is invisible and roughly the size of the finding you
are trying to report.

If the original is gone, say so, and treat today's figure as a new baseline
rather than an after.

## Hold these constant

- The same insight, by `short_id`
- The same window **length** — a 30-day before against a 7-day after is not a
  comparison
- The same cohort definition
- The same test-account filter
- The same event definitions — **check these did not change in the release**

That last one catches a whole class of false findings. A renamed or re-fired
event looks exactly like a behaviour change.

## Windows

| Usage pattern | Wait at least |
|---|---|
| Daily | 2 weeks |
| Weekly | 4–6 weeks |
| Monthly or seasonal | A full cycle, and say which |

Check too early and you measure novelty. Novelty always moves, and it always
comes back down.

Avoid windows containing a holiday, a billing boundary or a known outage on one
side only.

## Exposure before effect

Always two questions, never one:

1. **Did they encounter it?** Impressions, surface views, entry points
2. **Did it help?** Completion, time, repeat use, the downstream measure

A feature nobody saw has not failed — it has not shipped, in the only sense that
matters. Reporting that as a value failure sends a team to rebuild something that
was never found, which is the most expensive mistake this check can prevent.

```
exposure    did the surface get seen, by how many, vs before
effect      conditional on exposure, did the outcome move
```

## Segments

Run the breakdown the original study segmented on. An average across personas
hides the case where it worked for one and broke for another — which is the
normal outcome, not the exception.

If the study had no segment, say the check has none either, rather than
inventing one afterwards that happens to show movement.

## What you cannot claim

- **Causation**, without a control. Say "consistent with" and name what else moved
- **Success**, from usage alone. Usage is not benefit
- **Failure**, from a flat line without checking exposure
- **Anything**, from a window shorter than the usage cycle

The check is worth running precisely because it can come back negative. A method
that cannot embarrass you is not measuring anything.
