# PLAN: CS61C · State and Timing (L18)

Source: https://notes.cs61c.org/content/sds-state/ and its five sub-pages (register, timing, FSM,
pipelining, summary), fetched 2026-10-11; text in `notes.txt`  ·  Languages: en  ·
Voice: edge-tts `en-US-AndrewNeural` at −4%, pauses 0.75 / 1.6 / 1.8 s (the Newton–Schulz choice)  ·
Subtitles on frame: no, `.srt` beside each video  ·  Typeface: LaTeX for all text
Audience: a CS61C student who has seen gates, truth tables and an adder (L16–L17), and no state.

Status (2026-10-11): all five episodes are written (`ep01`–`ep05`), from the script in `narration.md`.
The user asked for English only and for the review to be done here, so the script was not sent for
a wording pass first; every scene was rendered as a voiced 480p clip and its frames inspected.

## Episodes

| # | Title | The question it answers | Notes covered | Words · length |
|---|---|---|---|---|
| 1 | The Sum That Ran Away | Why can't an adder with a feedback wire add up a list, and what is missing? | Signals/Waveforms/Clock §2–4; Register §1–2; Timing §2.1–2.3 | 1130 · ~8 min |
| 2 | Inside the Register | What is in a register, and what does "at the rising edge" mean for a real device? | Register §3; Summary (register example, exercises) | 920 · ~6.5 min |
| 3 | How Fast Can the Clock Tick? | How short can the clock period be, and can a circuit be too fast? | Timing §1, §2.4, §3, §4; Summary (two relationships) | 1010 · ~7 min |
| 4 | Three Ones in a Row | What can a register in a loop remember besides a sum, and how do you build it? | FSM (all); Summary (two-state machine) | 1010 · ~7 min |
| 5 | A Register to Go Faster | How can adding a register make a circuit faster, and what does it cost? | Pipelining (all); Signals/Waveforms/Clock §5 | 660 · ~5 min |

About 34 minutes in all at 135–145 words per minute.

## Why this order and not the notes' order

The notes go clock → register → flip-flop timing → accumulator → FSM → pipelining: every tool is
defined before the problem that needs it. The videos turn the first half round. The accumulator's
failure comes first (notes: Timing §2.1, the "strawman"), and the register and the clock are what the
viewer asks for after watching the sum run away. Each later definition is reached the same way:

| The notes state | The video gets there by |
|---|---|
| "The clock signal is the heartbeat of the system" | who should press LOAD, and when? Once per number, at the numbers' own rhythm |
| a register "captures the value … under the control of LOAD" | the feedback wire needs a box that holds the old total until told |
| setup and hold: "the d input must be stable … before … and after" | let d change in the middle of the clock's rise and ask which value was sampled |
| critical path = clk-to-q + CL + setup | shorten the period 10 → 8 → 7 → 6 ns until the register stores a wrong sum |
| hold violation, "add delay" | follow one edge through two registers; show that stretching the period changes nothing |
| the three states S0, S1, S2 | gates alone fail (same input, different output); ask what must be known for the next bit |
| "we need a register … and a combinational logic circuit" | the truth table's left side decides its right side: logic; only the state is remembered |
| pipeline register | the period is long only because one signal must pass both blocks between two edges |
| general model of an SDS (page 1, §5) | last scene: the three circuits of the series redrawn in one shape |

## Scene plans

Every number below is computed and asserted in the episode's code. The picture and the viewer's
state for each scene are in the `>` notes of `narration.md`; this is the short form.

### Episode 1: The Sum That Ran Away
- **Worked example.** List 3, 1, 4, 2 (total 10); adder delay 2 ns; one number per 8 ns. Feedback wire
  alone: output 3, 6, 9, 12 at 2, 4, 6, 8 ns, then 13, 14, 15. With a register on an 8 ns clock: 3, 4, 8, 10.
- **Aha.** Nothing is broken; nothing ever said "wait".

| Scene | Picture | Must get across | Notes |
|---|---|---|---|
| `hook` | adder, list, feedback wire | the job and the natural design | Timing §2, fig. 1–2 |
| `waveform` | probe → trace; four wires → bus band | waveform, 0/1 levels, restoration, bus | Signals §3, §3.1 |
| `delay` | three bands, gap of 2 ns, zoom | propagation delay | Signals §4 |
| `runaway` | X and S bands, loop pulse | 3, 6, 9, 12: out of control, and why | Timing §2.1 |
| `hold_it` | box in the feedback wire, LOAD, D/Q | what a register does, from the need | Register §1–2 |
| `clock` | square wave, edges, period, CLK → LOAD | clock, rising/falling edge, period, 1 GHz | Signals §2; Register §2 fig. 2 |
| `works` | reset, CLK, X, Q, S waveforms | reset; 3, 4, 8, 10; one step per period | Timing §2.2–2.3 |
| `close` | circuit; camera to the register | "synchronous"; the next question | Signals §3 (third observation) |

### Episode 2: Inside the Register
- **Worked examples.** Four rising edges with d sampled high, low, low, high. The notes' example:
  setup 2.5 ps, hold 1.5 ps, clock-to-q 1.5 ps, period 13 ps.
- **Aha.** "At the edge" is a window, and what goes wrong inside it.

| Scene | Picture | Must get across | Notes |
|---|---|---|---|
| `recap` | episode 1 circuit → register box | | |
| `inside` | box → n flip-flops on one clock | n-bit register = n FFs; D/Q, d/q; ~10 transistors | Register §3, fig. 3 |
| `sample` | CLK, d, q traces; predict, then draw | positive edge-triggered D FF; no visible change when d = q | Register §3.1–3.2, fig. 4–5 |
| `edge` | zoom on one edge; setup, hold, clk-to-q arrows | each quantity from what could go wrong | Register §3.3, fig. 6 |
| `numbers` | windows on the notes' example | read a timing diagram with real values; grey = unknown | Summary fig. 2; Register footnote 3 |
| `check` | the two true/false statements | | Summary, exercises 1–2 |
| `close` | | the next question | |

### Episode 3: How Fast Can the Clock Tick?
- **Worked examples.** Accumulator with clock-to-q 1, adder 5, setup 1 ns: sum ready at 6, minimum
  period 7 ns ≈ 143 MHz. Late input (X at 3 ns): garbage from 6 to 8 ns, harmless. Quick check from the
  notes: 1 + 3 + 1 = 5 ns → 200 MHz. Hold: hold 2, clock-to-q 1, wire 0 → violation; 1 ns of delay fixes it.
- **Aha.** Slowing the clock cannot fix a hold violation.

| Scene | Picture | Must get across | Notes |
|---|---|---|---|
| `recap` | accumulator with the window at D | | Timing §1 |
| `cycle` | ruler 0–10 ns, markers at 1, 6, 9 | one period in numbers, slack | Timing §2.3, fig. 4 |
| `late` | X at 3 ns, hatched band 6–8 | arrival mismatch is normal and ignored | Timing §2.4, fig. 5 |
| `squeeze` | period slides 10 → 8 → 7 → 6 | minimum period, the formula, f = 1/T | Timing §3, fig. 6 |
| `critical` | notes' four-gate circuit, routes lit | critical path; why not four gates | Timing §3 quick check, fig. 7–8 |
| `hold` | two registers, one edge, a racing pulse | hold rule; delay is the fix; why rare | Timing §4; Summary; Register fn. 3 |
| `close` | | the next question | |

### Episode 4: Three Ones in a Row
- **Worked example.** The notes' stream 0101101110111101111110 → output pulses at bits 9, 13, 18, 21.
- **Aha.** The table needs no memory; only the state does.

| Scene | Picture | Must get across | Notes |
|---|---|---|---|
| `hook` | input band, output pulses | the specification, on the stream | FSM §3, §3.1, fig. 2 |
| `memory` | two boxed moments; three tallies | gates alone fail; what must be remembered | (added motive) |
| `states` | circles, one arrow per sentence | states, arcs input/output, self-loop, definition | FSM §2, §3.2, fig. 1, 3 |
| `run` | token hopping on the diagram | the diagram does the job | FSM §3.1 |
| `table` | codes; one row per arrow | PS, INPUT → NS, OUTPUT; 11 unused | FSM §3.3, table 1 |
| `circuit` | CL block + state register, loop | check, transition, output each cycle | FSM §3.4, fig. 4–6 |
| `gates` | rows → AND gates | OUTPUT = PS1·¬PS0·IN; NS1, NS0 | FSM fig. 7 (+ added NS gates) |
| `other` | two-state machine; cache controller | any FSM = register + logic | Summary fig. 1; FSM §1 |
| `close` | | the next question | |

### Episode 5: A Register to Go Faster
- **Worked example.** Adder 5 ns, shifter 3 ns, clock-to-q 1, setup 1. One stage: 10 ns. Two stages: 7 and
  5 ns → period 7 ns (≈143 MHz), latency 14 ns. Data (3,1) → 4 → 8; (2,5) → 7 → 14; (6,2) → 8 → 16.
- **Aha.** Throughput goes up while each item takes longer.

| Scene | Picture | Must get across | Notes |
|---|---|---|---|
| `recap` | | use the rule backwards | Timing §1 |
| `one_stage` | reg, adder, shifter, reg; delay bar | one result per 10 ns, 10 ns each | Pipelining §2, fig. 1 |
| `idea` | third register drops in; bar splits | period = slower half | Pipelining §3, fig. 2 |
| `flow` | grid: edges × registers | a new input every edge | Pipelining §3 ("Can this circuit…") |
| `trade` | before/after: throughput, latency | both terms; why latency grew; when to pipeline | Pipelining §4 |
| `model` | three circuits → one shape | CL blocks between registers, clock only to registers, feedback optional | Signals §5, fig. 5 |

## Coverage

| Notes item | Episode · scene | or omitted, because |
|---|---|---|
| **Signals, Waveforms, and the Clock** | | |
| Chip photo; pins, package, PCB; power supply, Vdd/GND, 110 V AC, ~10 W | | omitted: background from the previous chapter, nothing later depends on it |
| Clock: generated on the motherboard, distributed on chip, "heartbeat" | 1 · clock | |
| ~1 GHz; square wave; period measured rising edge to rising edge | 1 · clock | |
| Why "rising" and "falling" edge | 1 · clock | |
| Waveform of a wire; low = 0, high = 1 | 1 · waveform | |
| Levels not at the extremes; restoration | 1 · waveform | |
| Changes follow clock edges (synchronous) | 1 · close | |
| Signal wires, bus, lower/upper-case labels, bus waveform (fig. 4) | 1 · waveform | case convention shown on screen, not spoken |
| Propagation delay; always less than the clock period | 1 · delay; 3 · squeeze | |
| General model of an SDS (fig. 5) and its four bullet points | 5 · model | |
| **The Register** | | |
| CL has no memory; memory circuit; LOAD; holds until loaded | 1 · hook, hold_it | |
| CLK used as LOAD (fig. 2) | 1 · clock | |
| n-bit register = n flip-flops; name; D/Q, d/q | 2 · inside | |
| Edge-triggered D FF; ~10 transistors; positive vs negative edge | 2 · inside, sample | |
| Verifying the behaviour on a waveform; no change when d = q (fig. 4) | 2 · sample | |
| Simulator screenshot (fig. 5) | | omitted: same content as fig. 4 |
| Setup time, hold time, window, clk-to-q (fig. 6, A/B/C) | 2 · edge | |
| Footnote: hold vs clk-to-q, no relation, in practice hold is less | 2 · numbers | |
| **Timing a Synchronous System** | | |
| Two uses of registers (control flow; raise clock frequency) | 3 · recap; 5 · recap | |
| Accumulator: block diagram, strawman, "out of control" | 1 · hook, runaway | |
| Register in the feedback path; reset; synchronous reset has priority | 1 · hold_it, works | |
| Waveforms of the working accumulator (fig. 4) | 1 · works; 3 · cycle | |
| Different arrival times, X0 + X0, hatched instability (fig. 5) | 3 · late | |
| Minimum period limited by logic delay; wrong value if too short | 3 · squeeze | |
| Critical path definition; f = 1/T; clk-to-q + CL + setup (fig. 6) | 3 · squeeze, critical | |
| Quick check: four AND gates, 200 MHz (fig. 7–8) | 3 · critical | answer options not listed on screen |
| Hold time violations; best-case delay; add delay | 3 · hold | |
| **Finite State Machines** | | |
| What FSMs are for; cache controller | 4 · other | |
| Inputs, outputs, states, arcs with input/output labels (fig. 1) | 4 · states | |
| Self-loop | 4 · states | |
| Three ones: specification and waveform (fig. 2) | 4 · hook, run | |
| S0, S1, S2 and all six transitions (fig. 3) | 4 · states | |
| Truth table, codes 00/01/10, PS and NS (table 1) | 4 · table | |
| Each cycle: check inputs, transition, output | 4 · circuit | |
| State register + CL block in a loop (fig. 4–6) | 4 · circuit | |
| What is inside the CL block; OUTPUT gate (fig. 7) | 4 · gates | |
| **Pipelining for Performance** (out of scope for the midterm) | | |
| Non-pipelined add/shift, registers at both ends, one-cycle delay (fig. 1) | 5 · one_stage | |
| Period too short → wrong value captured | 3 · squeeze | covered there |
| Pipeline register; new input each cycle (fig. 2) | 5 · idea, flow | |
| Critical path and latency of both designs | 5 · one_stage, idea, trade | see "notes differences" |
| Throughput against latency; when pipelining is good | 5 · trade | |
| **Summary** | | |
| Two-state FSM (fig. 1) | 4 · other | |
| Setup/hold definitions; register example 2.5 / 1.5 / 1.5 ps, 13 ps; grey = garbage (fig. 2) | 2 · numbers | |
| Period small enough / large enough | 3 · close | |
| τ critical path = clk-to-q + CL + setup | 3 · squeeze | |
| clk-to-q + smallest CL delay ≥ hold | 3 · hold | |
| Exercises 1 and 2 (true/false) | 2 · check | |
| Textbook readings, handout links | | omitted: references |

## Notes differences (to report with the videos)

1. **Latency of the pipelined circuit.** The notes give it as the sum of the two stage delays
   (clk-to-q + add + setup + clk-to-q + shift + setup; 12 ns with this plan's numbers). With one clock
   at the slower stage's period the item takes two periods, 2 × 7 = 14 ns. The two agree only when the
   stages are balanced. The video says 14 and shows where the extra 4 ns go.
2. **Hold time and clock-to-q.** The register page's footnote says there is "no particular relation"
   but in practice hold < clk-to-q; the summary says "hold time is generally included in clk-to-q
   delay" and clk-to-q ≥ hold. The video says: no necessary relation, in practice hold ≤ clk-to-q.
3. **Unit slip in the quick-check answer.** "The minimum clock period is 5 ns = 10-9 seconds per
   cycle" should read 5 × 10⁻⁹ s; the result, 200 MHz, is right.
4. **Next-state gates.** The notes draw only the OUTPUT gate. NS1 = ¬PS1·PS0·IN and NS0 = ¬PS1·¬PS0·IN
   are added from the table (checked in code over the whole stream).
5. **Unused state 11.** The notes' table has six rows and does not mention the fourth bit pattern; one
   sentence is added.

## Glossary and colours

One name per thing in the narration; one colour per concept on screen.

| Concept | Term used | Said aloud as | Colour |
|---|---|---|---|
| CLK | the clock; rising edge, falling edge, clock period | "the clock" | yellow |
| combinational logic (adder, shifter, CL block, gates) | logic; the adder | | blue |
| register / flip-flop | register (n bits), flip-flop (one bit) | | teal |
| data in the list | the next number; X on screen | | white |
| stored value / total | the total so far; S on screen | | green |
| setup + hold window | the window | | orange, shaded |
| clk-to-q | clock to q delay | "clock to q" | purple |
| wrong or unknown value | garbage; unknown | | grey hatching; red when it is captured |
| critical path | the slowest route; then "critical path" | | red route |
| state | S0, S1, S2 | "S zero" … | teal circles; the output-1 arrow in yellow |

## Decisions and open points

- English only, the Newton–Schulz voice and pace, `.srt` beside the video. Made without asking because
  the last three units were built that way; say so if this one should be Chinese or bilingual like
  `cs61c/riscv` (the script would be translated before any code is written).
- Five episodes of 5 to 8 minutes rather than one per notes page: the split follows the viewer's
  questions, and each episode ends on the next one's question.
- Written with one model end to end (`SKILL.md`), not the author/builder pipeline: zooms, LaTeX text
  and an auditioned voice are what `PIPELINE.md` lists as untested in that arrangement.
- English only, confirmed by the user on 2026-10-11, who also asked that the review be done here.
- The quick check's critical path: the notes highlight the route from the register's own output; the
  second input from the top passes the same three gates, so the video names both.
