# History: measured runs

Not needed to do the work; read it to weigh the cost of a pipeline run.

## CS70 notes 10 and 11

Measured on CS70 note 10 (five episodes): a cheap model working alone from `STRICT.md`
passes every mechanical gate and still makes a mediocre video, because the gates see
overlaps and empty frames, not a weak explanation. One episode cost the cheap builder
about 18 M input tokens over 165 tool calls; a mid model about 0.2 M. The split above
follows from that.

Run once end to end, on CS70 note 11 (ten episodes, about 45 minutes of video):

| Role | Model | Per episode | Whole unit |
|---|---|---|---|
| Author | Opus | 5 to 8 minutes for a board | about 1.2 M tokens, boards and two revision passes |
| Builder, first build | DeepSeek in the Claude Code harness | 14 to 70 minutes, 6 to 14 M input tokens (proof episodes are the slow ones) | about 90 M input tokens, 5.7 hours of agent time |
| Reviewer | Sonnet | 1 to 2 minutes, about 0.1 M tokens | 1 M |
| Builder, fix round | DeepSeek | 10 to 21 minutes, 1.5 to 9 M input tokens | about 59 M input tokens, 3 hours |
| Verifier | Haiku | under a minute, about 0.1 M tokens | 1 M |

Every first build passed the gate and matched its board word for word; every episode
still needed one fix round. What the reviewer found was mostly one family, now rules in
the author's and builder's briefs: the thing a beat is about drawn as the smallest text
on the frame, dashed lines too faint to see, a highlight fading with its cell, a scene
change before the last sentence had ended. The builder's questions to the author were
worth reading (a picture contradicting its caption, a count on screen that did not
prove what the voice claimed). The verifier's verdicts matched the coordinator's own
look on the frames checked; it cannot judge sizes, so write review rows in terms of
what is visible ("larger than the cell names"), not in points.

What that run does not show. Nobody listened to the voice, and the 1080p files were
not inspected, so it has not met the test that reshaped every earlier series: the
user watching and listening. Fix rounds took about 40% of the builder's tokens, most
of them avoidable with the pilot above. The coordinator's own tokens were not
measured, and they were what ran into the usage limit. The first builds needed no
narration rewrite, which no earlier series managed; whether the narration is good is
still the user's call.
