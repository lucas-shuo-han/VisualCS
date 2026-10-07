# TRIAL LOG ep02

- Gate 1 (facts): file ran, exit 0.
- Scene runs: scene 1 PASS first try; scenes 2+3 together: first run FAIL render (disk full on C:, other workers), second run FAIL render (empty svg ParseError, transient), third run PASS; scenes 4+5 together PASS first try.
- Full episode: first run FAIL report (expected), then --no-render.
- Scenes 2+3 and 4+5 were checked in pairs, not one by one (render time with other workers).
