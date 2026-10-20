# Warm segments in Pendo

Three recipes. All of them target **behaviour**, not self-description, and all of
them exclude people who have already seen the guide.

---

## 1 — Guide-interaction based

The default for research recruitment. Prior guide engagement is the cleanest
available proxy for "will read an in-product message".

```
Segment: Research panel candidates
├─ Viewed guide "<any recent release guide>" in last 90 days
├─ Has NOT seen "UXR research panel" before
├─ Account tier = Partner or Premium          (optional)
└─ Expect 50–200 warm prospects per launch
```

## 2 — Behavioural

For feature-specific recruitment, where you need people who have actually used
the thing you want to talk about.

```
Segment: Feature explorers
├─ Viewed the feature release guide in last 30 days
├─ Clicked through to the feature > 3 times
├─ Account created > 6 months ago            (experienced, not onboarding)
└─ Highly engaged, low churn
```

## 3 — Intent / support-based

For problem-aware participants who already have something to say. Treat the
resulting sample as skewed towards the frustrated — useful for diagnosis, bad
for measuring satisfaction.

```
Segment: Feedback-ready partners
├─ Opened a support ticket in last 60 days   (has a pain point)
├─ OR submitted a feature request            (has an idea)
├─ OR attended a webinar                     (signals intent)
└─ Problem-aware and motivated
```

---

## Rules that apply to all three

- **Exclude prior viewers.** Always. Re-showing is the fastest way to teach
  people that guides are noise.
- **Frequency cap** so one person is asked once per campaign.
- **Segment and page**, never site-wide.
- **Name who you excluded.** A warm segment is defined as much by who is missing
  from it, and that belongs in the write-up — a panel recruited from guide
  engagers over-represents people who like in-app content.
- **Size the segment before you launch.** If the warm segment is under ~50, you
  will not hit a panel target from it; widen the behaviour window rather than
  dropping to cold.

## Testing which segment is warmest

Run the same copy to two segments for two weeks and compare click rate. That is
a targeting test. Changing copy *and* segment at once tells you nothing — one
variable at a time, or you cannot attribute the lift.
