# CS182 · Introduction: series plan

Source: Lecture 0 slides (`notes/00_introduction.pdf`, 22 pages): intros, logistics, "What is Deep Learning?", "Studying Deep Learning...", "Engineering or Alchemy?", history timeline, Tao essay pointer.
The slides carry little substance beyond the definition and the timeline, so both episodes add worked toy examples (marked as own additions below). Colors as in dl.py (data white, model blue, loss red, new data purple, lr yellow).

| Ep | Title | Question | Worked example (computed in Python, asserted) | Aha | Notes items |
|---|---|---|---|---|---|
| 1 | What Is Deep Learning? | What exactly is being defined? | Rosenblatt-style element: z = 0.8*2 - 0.5*1 + 0.2 = 1.3 then -0.9 with other knobs; perceptron update on 20 points: mistakes 10, 4, 2, 6, 0; 92/100 on fresh points, 53/100 when the pattern differs | The parameters are the program; a learned circuit captures one pattern, and only works where it applies | definition slide, "deep", relevant pattern / new data |
| 2 | Engineering or Alchemy? | Where does this come from, and what is the course for? | timeline with computed gaps (55 and 17 years); XOR: best line gets 3 of 4, two ramps + readout gets 4 of 4; gradient descent on 2w^2: eta 0.1/0.4/0.5/0.6 give factors 0.6/-0.6/-1/-1.4, stable iff eta < 0.5 | The pile-stirring knob has a reason (2/L) | timeline, "Engineering or Alchemy?", xkcd, prerequisites, course title, Tao reading |

Own additions (not on the slides): the perceptron experiment, the fresh-data accuracy numbers, the XOR demonstration (the slide only says "fundamental limitations"), the learning-rate stability example, and the mapping of the three prerequisite courses onto the definition.
