# CS61C · State and Timing — narration script (draft 1, 2026-10-11)

> **How to use this file.** Everything here is plain text.
> - **Body** = the plain lines under each `###` heading. That text is what the voice says and what the
>   `.srt` shows, one sentence at a time. A line break inside a beat is a paragraph: a longer pause.
> - **Notes** = any line starting with `>`. Never rendered. Each scene's notes say what the picture
>   shows and what the viewer knows and asks at that point.
> - Numbers are written as words because the voice reads them; the figures are on the screen.
> - **This is the script the episodes were written from.** The `say()` calls in `epNN_*.py` carry the
>   same words (one beat here = one `say()`); a change of wording is made in both places. The script as
>   rendered, with timings, is `SCRIPT.en.md`, generated from the subtitles.
> - Sources are in `PLAN.md` (coverage table): which page and section of the notes each scene covers,
>   and what was added or left out on purpose.

> **The story in one paragraph.** We try to add up a list with an adder and a feedback wire, and the
> sum runs away. What is missing is something that holds a value still and something that says when
> to let go: the register and the clock (episode 1). A register is a row of flip-flops, and "at the
> edge" turns out to be a window: setup, hold, clock-to-q (2). Those three numbers decide how short a
> clock period can be, and, separately, how fast a route is allowed to be (3). A register in a loop
> can remember more than a sum: three ones in a row, as a state machine, built down to gates (4). And
> a register can be added only to make the clock faster: pipelining, and the general model (5).

---

# Episode 1 · The Sum That Ran Away

> Worked example: the list 3, 1, 4, 2 (total 10); adder delay 2 ns; one number every 8 ns.
> Without a register the output reads 3, 6, 9, 12 by the time the second number arrives.
> With a register clocked every 8 ns it reads 3, 4, 8, 10.

## 01 · hook — a job for an adder

> Picture: one adder block, centre. Two input buses, one output bus. Then the list 3, 1, 4, 2 queued
> on the left, the feedback wire drawn last.
> The viewer knows: gates and adders from the previous chapter (combinational logic).

### hook 01
Here is an adder. Put two numbers on its inputs, and their sum comes out on the other side.
It has no memory at all, so its output depends only on what the inputs are right now.

### hook 02
Let's give it a job that sounds easy. A list of numbers arrives one at a time, three, then one, then four, then two, and we want their total.
The total is ten, but the adder only ever sees two numbers at once.

### hook 03
So one input has to be the next number from the list, and the other has to be the total so far.
And the total so far is exactly what the adder produces. The natural thing to do is to run a wire from the output straight back to the second input.

### hook 04
On paper this looks finished. To find out whether it works, we have to watch what the wires do over time, and for that we need a way to draw time.

## 02 · waveform — how to draw a wire over time

> Picture: the circuit shrinks to a corner. One wire, a probe, a voltage axis and a time axis; the trace
> draws itself left to right. Then four traces stacked (3 = 0011, then 6 = 0110) collapse into one bus band.
> Asks next: fine, what does the adder look like in this picture?

### waveform 01
Take a single wire and touch a probe to it. All the probe can measure is a voltage, so we plot that voltage against time.
A picture like this is called a waveform.

### waveform 02
Most of the time the voltage sits at one of two levels. By convention the low level means a zero and the high level means a one.
So this wire said zero, then one, then zero again.

### waveform 03
Look closely and the levels are not perfect. A high is sometimes a little short of the top, and a low floats a little above the bottom.
That is fine, because every gate reads anything near the top as a one and then drives its own output all the way to the top. The small errors are wiped out at each gate instead of piling up, and that is what makes a circuit digital.

### waveform 04
A number needs several wires, one for each bit. Here are four of them carrying the number three, and then the number six.
Drawing every wire gets crowded, so we draw the whole group, called a bus, as one band with its value written inside. Where the band pinches, the value is changing.

## 03 · delay — the adder is not instant

> Picture: three bus bands stacked (input A, input B, output). A changes 0 → 3; the output band pinches
> 2 ns later. A double arrow marks the gap; camera moves in on the gap.

### delay 01
Now watch the adder in this picture. Both inputs are zero, so the output is zero.
Change the top input to three. The output does become three, but not at the same moment.

### delay 02
The change has to work its way through the transistors inside. The time from an input changing to the output settling is called the propagation delay.
Let's say that for this adder it is two nanoseconds.

## 04 · runaway — test the feedback wire

> Picture: the circuit with the feedback wire, top; under it two bands on a time axis marked in ns:
> X (3 until 8, then 1) and S (0, 3, 6, 9, 12, 13, 14, 15). Each new S value appears on its sentence,
> and a pulse runs round the loop in the circuit each time.
> The viewer expects it to work. This is the failure the whole series answers.

### runaway 01
With that we can test our circuit. The total starts at zero, and at time zero the first number, three, arrives.
The numbers come one every eight nanoseconds, so the three stays on the input until then.

### runaway 02
Two nanoseconds later the adder has worked out zero plus three, and the output says three. That is the correct total so far.

### runaway 03
But the output is wired back to the input, so now the adder sees three plus three, and two nanoseconds later it says six.
Then six plus three makes nine, and nine plus three makes twelve.

### runaway 04
Only now, at eight nanoseconds, does the second number show up. The total should still be three, ready to become four.
Instead the wire says twelve, and it carries on to thirteen, fourteen, fifteen.

### runaway 05
Nothing is broken here, because the adder did exactly what an adder does.
The trouble is that each new sum went back into the input the moment it was ready, and nothing in the circuit ever said wait.

## 05 · hold_it — what would fix it

> Picture: the feedback wire is cut; an empty box drops into the gap. It gets a third input from below
> (LOAD), then the labels D and Q, then its name.
> Derived from the failure: first the need, then the box, then the name.

### hold_it 01
So let's say what we need. Somewhere on that feedback wire there should be a box that holds on to the old total and keeps showing it to the adder.
The new sum can wait at the door, but it does not get in until we say so.

### hold_it 02
Give the box one extra input for that, and call it load. When load gives the signal, the box takes in whatever is at its input, and from then on shows that at its output.
At all other times its input can do anything, and its output stays put.

### hold_it 03
A circuit like this, one that remembers, is called a register. Its input is labelled D and its output Q.

### hold_it 04
Who gives the load signal, and when? We want exactly one load for each number, so it should come at the same rhythm as the numbers themselves.
In our example that is once every eight nanoseconds.

## 06 · clock — the signal that says when

> Picture: a square wave draws itself under the circuit. One rising edge and one falling edge get
> named; a brace marks one period, 8 ns. Then the wave's wire connects to LOAD, which is relabelled CLK
> (the small triangle on the box).

### clock 01
A computer has a signal with precisely that job. It is called the clock, and it does nothing but go high and low, high and low, at a steady rate.
It is made on the motherboard and wired to every part of the chip.

### clock 02
The moment it goes from low to high is called a rising edge, and the moment it comes back down is a falling edge.
The time from one rising edge to the next is one clock period. Ours is eight nanoseconds. In a real processor it is closer to one nanosecond, which is a billion ticks every second.

### clock 03
Now connect the clock to the load input. This register takes in a new value at every rising edge, and only then.

## 07 · works — run the list again

> Picture: circuit on top (adder, register in the loop, clock), waveforms below: reset, CLK, X, register
> output, adder output. One period per sentence; the value in the register box changes at each edge.
> Values: register 0, 3, 4, 8, 10; adder output 3, 4, 8, 10.

### works 01
Let's run the list again. First the register has to start at zero, and registers have an input for that, called reset.
If reset is one at a rising edge, the register clears to zero, whatever is waiting at D.

### works 02
The register shows zero and the first number is three, so the adder settles on three.
And this time the three just waits at the register's input, because no edge has come yet.

### works 03
Here is the edge. The register takes the three, the list moves on to one, and the adder settles on four.
At the next edge the register takes the four, the list gives four, and the adder says eight. One more edge, and eight plus two is ten.

### works 04
At the following edge the ten is stored. Four numbers, four ticks, and the total is ten.
The circuit now takes one step per clock period, and the register is what holds each step back until the next tick.

## 08 · close

> Picture: the finished circuit alone, large. Then camera moves onto the register box and its clock pin.

### close 01
So a circuit that feeds its own output back needs something that holds a value still, and something that says when to let go. Those are the register and the clock.
A circuit built this way, where every change follows a clock edge, is called a synchronous digital system.

### close 02
We were generous to the register, though. In our picture it took its new value in no time at all, exactly at the edge.
But a register is made of transistors, just like the adder. So what is inside it, and what does at the edge really mean?

> End card recap:
> - A waveform plots a wire's voltage over time; low is zero, high is one, and a bus is drawn as one band.
> - Every circuit has a propagation delay between its inputs changing and its output settling.
> - An adder wired back to itself keeps adding: nothing tells it to wait.
> - A register holds a value and takes a new one only at the rising edge of the clock.

---

# Episode 2 · Inside the Register

> Worked examples: a four-edge waveform where q follows d only at rising edges; then the notes' own
> example (setup 2.5 ps, hold 1.5 ps, clock-to-q 1.5 ps, period 13 ps).

## 01 · recap

> Picture: last episode's circuit, small; the camera goes to the register box, which becomes the stage.

### recap 01
Last time a register saved our running sum. It took in a new value at each rising edge of the clock and held it still for the rest of the period.
Today we open the box.

## 02 · inside — a register is n flip-flops

> Picture: the register box widens and becomes transparent: four small boxes side by side, one wire in
> and one wire out each, one clock line running under all four. Bus labels D and Q outside, d and q on
> one small box. Then three of the four fade and the remaining one moves to the centre.

### inside 01
Our register stored a whole number, so it has several wires going in and several coming out.
Inside there is no clever machinery. There is one small circuit for each bit, side by side, and all of them listen to the same clock.

### inside 02
Each of these small circuits is a register for a single bit. It is called a flip-flop, because all it ever does is flip to one or flop back to zero, and it takes about ten transistors to build.
By convention the input of a register is capital D and its output is capital Q. For a single flip-flop we use the small letters.

### inside 03
So to understand a register of any width, we only have to understand one flip-flop. Let's put a probe on its three wires and watch.

## 03 · sample — q follows d only at rising edges

> Picture: flip-flop symbol top left; three traces: CLK (four rising edges), d (changes between edges
> as well), q (drawn edge by edge, after the viewer has had a second to predict). A thin vertical line
> at each rising edge, a dot on d where it is sampled.
> Notes §3.2 leaves this "as an exercise": here it is done.

### sample 01
Here is the clock, and here is an input that changes whenever it likes. Before the output appears, try to predict it.
All you need to know is that the flip-flop only looks at its input at each rising edge.

### sample 02
At the first edge the input is high, so the output goes high. During this period the input drops and comes back up, and the output takes no notice at all.
At the second edge the input is low, so the output goes low.

### sample 03
At the third edge the input is low again. The flip-flop does take that value in, but it is the value the output already has, so nothing visible happens.
At the fourth the input is high, and the output goes high again.

### sample 04
So the rule is short. At every rising edge q becomes whatever d is at that moment, and between edges q does not move.
This kind is called a positive edge triggered D flip-flop. There is also a kind that acts on the falling edge, but we will only use this one.

## 04 · edge — what "at that moment" hides

> Picture: camera zooms onto one rising edge until the clock's rise is visibly a slope. d is drawn
> changing in the middle of it; q's trace splits into a grey "unknown" band. Then d is moved earlier:
> setup arrow. Then the later change is moved out to the right: hold arrow. Window shaded between two
> dashed lines. Last, q's change appears to the right of the edge: clock-to-q arrow.
> Each quantity comes from asking what could go wrong, not from a list of three definitions.

### edge 01
That rule has a soft spot, and it is the phrase at that moment. Let's zoom in on one rising edge, far enough to see that the clock itself takes a little while to rise.

### edge 02
Suppose the input changes right here, in the middle of the rise. Is the value at the edge a zero or a one?
The transistors inside are partway through taking the old value in, and now they are handed a different one. What the output ends up as is anyone's guess.

### edge 03
So the flip-flop comes with a condition. Its input has to be steady already a short time before the edge, so that the value has time to get in.
That time is called the setup time.

### edge 04
And the input has to stay steady for a short time after the edge, until the flip-flop has safely let go of it. That time is called the hold time.
Together they make a window around every rising edge. Inside the window the input must not change. Outside it, the input can do whatever it wants.

### edge 05
There is one more delay, on the output side. Even when the input behaves, the new value does not show up at the output on the edge itself.
It appears a little later, and that delay is called the clock to q delay.

### edge 06
Three numbers, then, describe a flip-flop. Setup and hold are demands it makes on its input, and clock to q is how long it makes its output wait.

## 05 · numbers — the notes' example

> Picture: clock (two rising edges, period 13 ps), input (several pulses), output. Windows drawn at
> each edge, 2.5 ps before to 1.5 ps after. Output grey until 1.5 ps after the first edge.
> From the notes' summary page, figure 2. The last beat settles the notes' two statements about hold
> and clock-to-q (footnote: "no particular relation"; summary: "clk-to-q ≥ hold").

### numbers 01
Let's put numbers on them. Take a flip-flop with a setup time of two and a half picoseconds, a hold time of one and a half, and a clock to q delay of one and a half.
The clock period is thirteen picoseconds.

### numbers 02
Draw the window at each edge. It opens two and a half picoseconds before and closes one and a half after.
This input changes many times, but every change falls outside a window, so each edge samples a clean value.

### numbers 03
Now the output. Before the first edge we have no idea what the flip-flop holds, so we shade it as unknown.
One and a half picoseconds after that edge, the output shows the value the input had, which was a one. After the next edge it shows a zero.

### numbers 04
Here the hold time and the clock to q delay happen to be equal. Nothing forces that, because one describes the input and the other describes the output.
In practice, though, flip-flops are built so that the hold time is the smaller of the two, or at most equal.

## 06 · check — the notes' two questions

> Picture: the zoomed edge diagram again; the statement appears as one line, the relevant arrow lights up.

### check 01
Here are two statements to test yourself on. The first says that the clock to q delay is the time from the rising edge to the hold time.
That is false. Clock to q runs from the rising edge to the moment the output shows the new value, and the hold time is about the input.

### check 02
The second says that a flip-flop only updates its output at a rising edge, even if its input changes in between.
That one is true, and it is the whole point of the device.

## 07 · close

### close 01
So a register is a row of flip-flops. Each one samples its input in a small window around the rising edge and answers a moment later.
Now put it back in our circuit, where the adder's result has to arrive before that window opens. How short can we make the clock period before the sum stops being right?

> End card recap:
> - An n-bit register is n flip-flops on one clock.
> - A positive edge-triggered D flip-flop copies d to q at each rising edge and ignores d otherwise.
> - Setup time: how long before the edge d must be steady. Hold time: how long after.
> - Clock-to-q delay: how long after the edge q shows the new value.

---

# Episode 3 · How Fast Can the Clock Tick?

> Worked examples: the accumulator with clock-to-q 1 ns, adder 5 ns, setup 1 ns (minimum period 7 ns);
> the notes' quick check (four AND gates, critical path 5 ns, 200 MHz); a hold violation with hold 2 ns.

## 01 · recap

> Picture: the accumulator circuit, with the flip-flop's window drawn small at the register's D pin.

### recap 01
We have an adder with a register on its feedback wire, and we know that a register needs its input steady in a window around each rising edge.
Today we put the two together and ask how fast this circuit can be clocked.

## 02 · cycle — one period with real numbers

> Picture: circuit on top with each delay written on its part. Below, a time ruler 0 to 10 ns and three
> bands: register output, adder output, and CLK with the window shaded from 9 to 10 (and on past the edge).
> Markers appear at 1, 6, 9 as they are said; a brace shows the 3 ns of slack.

### cycle 01
Give everything a number. The register has a clock to q delay of one nanosecond and a setup time of one nanosecond.
The adder takes five nanoseconds, and the clock period is ten.

### cycle 02
Follow one period, starting at a rising edge. One nanosecond later the register's output shows the stored total.
Suppose the next number from the list shows up at that moment too. The adder now has both inputs, and five nanoseconds later, at six, the new sum is ready.

### cycle 03
The next edge comes at ten, and the register needs its input steady one nanosecond before that, so from nine on.
The sum has been waiting since six, which leaves three nanoseconds to spare.

## 03 · late — inputs that arrive at different times

> Picture: same ruler; the X band now changes at 3 instead of 1. The adder output band gets a hatched
> stretch from 6 to 8, then the right value. The window at 9 stays clear of the hatching.
> Notes §2.3–2.4, figure 5 (hatched regions): X0 + X0 is the wrong sum right after X0 was stored.

### late 01
In a real machine the two inputs rarely arrive together. Say the stored total shows up at one nanosecond as before, but the next number from the list only at three.

### late 02
For those two nanoseconds the adder sees the new total next to the old number. Right after the first number was stored, that means it starts adding three plus three, which nobody asked for.

### late 03
That wrong sum does travel through the adder, so for a while the output is garbage.
Then at three the right number arrives, and five nanoseconds later, at eight, the output settles on the right sum.

### late 04
Eight is still before nine. The register only looks during its small window around the edge, so it never sees the garbage.
This happens in every circuit. Signals wobble in the middle of a period, and all that matters is that they are quiet when the edge comes.

## 04 · squeeze — shorten the period until it breaks

> Picture: back to both inputs at 1 ns, sum ready at 6. The right-hand edge of the ruler slides left:
> period 10 → 8 → 7 → 6, the window sliding with it. At 6 the window overlaps the still-changing band
> and turns red; the register box shows a wrong value. Then the three segments 1 + 5 + 1 are laid end
> to end and become the formula.

### squeeze 01
So how short can the period be? Go back to both inputs arriving at one nanosecond, with the sum ready at six.
Try a period of eight. The window now opens at seven, and the sum is there in time.

### squeeze 02
Try seven. The window opens at six, exactly when the sum settles, and that just works.
Now try six. The window opens at five, the adder is still working, and the register stores whatever happens to be on the wire. The total is wrong, and so is every total after it.

### squeeze 03
So seven nanoseconds is the shortest period, and we can read off where it comes from.
One nanosecond for the register to show its value, five for the adder, and one for the setup time of the register that catches the result.

### squeeze 04
In general the period has to be at least the clock to q delay, plus the delay of the logic, plus the setup time.
The hold time is not in this sum, because it concerns what happens just after an edge, not how long the logic takes.

### squeeze 05
A clock is usually described by its frequency, which is one divided by the period.
A period of seven nanoseconds is one seventh of a gigahertz, or about a hundred and forty three megahertz.

## 05 · critical — many routes, one clock (the notes' quick check)

> Picture: the notes' circuit redrawn: four AND gates and one register whose output feeds back.
> Routes light up one at a time with their gate count; the three-gate route stays lit as the critical path.
> Then 1 + 3 + 1 = 5 ns and 200 MHz. Camera follows the lit route.
> Common wrong answers this heads off: counting all four gates (6 ns), adding the hold time (6 or 7 ns).

### critical 01
Real circuits have many routes from one register to the next. Here is one from the course notes, with four AND gates that each take one nanosecond.
The register has a clock to q delay and a setup time of one nanosecond each, and the four inputs on the left come from other registers of the same kind.

### critical 02
Every route has to finish within one period, so the slowest route sets the pace. Let's time them.
From this input the signal passes two gates before it reaches the register, and from these two it also passes two.

### critical 03
But start from this input, or from the register's own output coming back around, and the signal passes this gate, then this one, then this one. That makes three.
No route goes through all four, because the lower gate sits beside that chain and not in it.

### critical 04
The slowest route is called the critical path. Here it costs one nanosecond for clock to q, three for the gates and one for setup, which is five in all.
So the clock can run at one fifth of a gigahertz, and that is two hundred megahertz.

## 06 · hold — a route can also be too fast

> Picture: two registers in a row on one clock, a short wire between them. One rising edge on the
> ruler; the second register's hold window shaded from 0 to 2 ns. A pulse leaves the first register at
> 1 ns and lands inside the window (red). Then a delay element is inserted in the wire and the pulse
> lands at 2 ns. The clock period brace is stretched to show that nothing changes.
> Motive the notes skip: why slowing the clock does not help.

### hold 01
The setup time gave us a rule that the logic must not be too slow. The hold time gives a second rule, and it points the other way.
Take two registers on the same clock with almost nothing between them.

### hold 02
At a rising edge the second register samples its input, and it needs that input to stay put until its hold time is over.
But the same edge makes the first register change its output, one clock to q delay later. That change sets off down the wire toward the second register.

### hold 03
If it gets there before the hold time is over, the second register's input moves inside the window.
Say the hold time is two nanoseconds, clock to q is one, and the wire takes no time. The new value arrives at one, which is too early.

### hold 04
So the second rule is that clock to q plus the fastest route through the logic must be at least the hold time.
Notice that the clock period is not in it. Both events follow the same edge, so slowing the clock down does not help at all.

### hold 05
What helps is to put some delay on the route. With one nanosecond of delay here, the new value arrives at two, just as the window closes.
In practice this problem is rare, because flip-flops are usually built with a hold time no longer than their clock to q delay. Then even a bare wire is slow enough.

## 07 · close

### close 01
So the clock period has a floor, set by the slowest route between two registers. And every route has a floor of its own, set by the hold time.
With timing under control we can ask what a register in a loop is good for besides adding. Our circuit remembered a running total. What else could a circuit choose to remember?

> End card recap:
> - Signals may wobble in the middle of a period; they must be steady in the window around the edge.
> - Minimum clock period = clock-to-q + longest logic delay + setup time: the critical path.
> - Maximum frequency = 1 / minimum period.
> - Hold rule: clock-to-q + shortest logic delay ≥ hold time; the clock period cannot fix it.

---

# Episode 4 · Three Ones in a Row

> Worked example: the notes' own input stream 0 1 0 1 1 0 1 1 1 0 1 1 1 1 0 1 1 1 1 1 1 0,
> which gives four output pulses (checked in code against the table and the gates).

## 01 · hook — the job

> Picture: one input band scrolling in from the right, one bit per clock period, and an empty output
> band under it. The pulses appear on the output as the runs of ones complete.

### hook 01
Here is a wire that brings one bit in each clock period. We want a circuit that watches it and raises its output for one period whenever it has just seen three ones in a row.
After that it starts counting again from nothing.

### hook 02
Let's see what that means on a stream. A single one, and then two ones, give us nothing.
Then come three ones, and on the third the output goes high.

### hook 03
With four ones in a row we still get a single pulse, on the third, and the fourth is a fresh start.
Six in a row give two pulses.

## 02 · memory — why gates alone cannot do it

> Picture: two periods of the stream are boxed, one where the input is 1 and the output must be 0, one
> where the input is 1 and the output must be 1. Camera on the two boxes side by side. Then three small
> tallies appear: "none", "one", "two".

### memory 01
Can logic gates alone do this? Look at these two moments. In both the input is a one, but at the first the output must be zero and at the second it must be one.
Gates without memory give the same output for the same input, so the answer is no.

### memory 02
The circuit has to remember something about the past, but not the whole history. Ask what it must know in order to deal with the next bit.
All it needs is how many ones in a row it has just seen, and that is none, one or two. On the third it fires and goes back to none.

## 03 · states — build the diagram one arrow at a time

> Picture: three circles appear with their meaning under them. Arrows are drawn one per sentence, each
> labelled input/output; the arrow that outputs 1 is the only coloured one. Afterwards the meanings fade
> and the definition's words (inputs, outputs, states, arrows) point at parts of the picture.

### states 01
Give those three situations names. S zero means no ones yet, S one means one so far, and S two means two so far.
We draw each as a circle and call it a state. At any moment the machine is in exactly one of them.

### states 02
Now go through them and ask what each bit does. In S zero a one arrives, which makes one in a row, so we move to S one and the output stays zero.
We draw that as an arrow, labelled with the input, a slash, and the output. If a zero arrives instead we stay where we are, and that is an arrow from the state back to itself, called a self loop.

### states 03
In S one, another one takes us to S two, still with output zero. A zero breaks the run, so we go back to S zero.

### states 04
In S two, a one is the third in a row. This is the arrow that carries an output of one, and it leads back to S zero to start over.
A zero from S two also leads back to S zero, with output zero.

### states 05
That makes six arrows, two out of every state, so the machine always knows what to do.
A picture like this is called a finite state machine. It has inputs, outputs, a fixed set of states, and arrows that say where each input leads and what to output on the way.

## 04 · run — the stream through the diagram

> Picture: the stream band above the diagram; a dot sits on the current state and hops along one arrow
> per bit, the output band filling in below. Speeds up after the first pulse, silent to the end of the stream.

### run 01
Let's run the stream through it. A zero, and we stay. A one takes us to S one, and the next zero sends us back.
Then one and one bring us to S two, but a zero sends us home again.

### run 02
Now one, one, and one more. On that last arrow the output is one, and we are back in S zero, ready for the next run.

## 05 · table — states become bits

> Picture: diagram on the left; each circle gets a two-bit code. On the right the table grows one row
> per arrow, the arrow lighting up as its row appears. Columns: PS, INPUT, NS, OUTPUT.
> Added to the notes: one sentence on the unused pattern 11.

### table 01
To build this, the states have to become bits. Three states fit in two bits, so let S zero be zero zero, S one be zero one, and S two be one zero.
Then every arrow becomes a row of a table. On the left go the present state and the input, and on the right the next state and the output.

### table 02
Take the arrow from S one on a one. Its row reads present state zero one, input one, next state one zero, output zero.
Six arrows give six rows. The pattern one one never appears, because no arrow leads to it.

## 06 · circuit — a register and a block of logic

> Picture: the table shrinks into a box labelled CL. A two-bit register appears beside it. Wires are
> drawn as said: register output → CL (present state), input bit → CL, CL → output, CL → register input
> (next state), clock → register. Last, the accumulator from episode 1 appears small beside it, same shape.

### circuit 01
Look at what this table is. Its left side decides its right side with no memory involved, so it is a job for plain logic gates.
The only thing that has to be remembered is the present state, which is two bits, and we know what remembers bits.

### circuit 02
So the circuit is a register for two bits and a block of logic. The register's output is the present state.
The logic takes that and the input bit and produces the output and the next state. And the next state goes around to the register's input, where it waits for the clock.

### circuit 03
At each rising edge the next state becomes the present state, and the logic starts on the following bit.
This is the same loop as our running sum, with the adder swapped for a table.

## 07 · gates — what is inside the block

> Picture: camera onto the table; the single row with OUTPUT = 1 lights up and turns into an AND gate with
> PS1, NOT PS0, INPUT. Then the two rows with a 1 in NS become two more AND gates.
> The notes draw only the OUTPUT gate (figure 7); the two next-state gates are added here and asserted
> against the table in code.

### gates 01
What is inside the logic block? We can read it off the table. The output is one in a single row, where the present state is one zero and the input is one.
So the output is the high state bit, and not the low state bit, and the input.

### gates 02
The next state works the same way. Its high bit is one only in the row with state zero one and input one, and its low bit only in the row with state zero zero and input one.
That is three AND gates and a few inverters, and the machine is complete.

## 08 · other — the recipe works for any diagram

> Picture: the notes' two-state machine (summary page): 0 keeps the state and outputs 0, 1 switches the
> state and outputs 1. Then a plain three-box sketch of a cache controller's states, no detail.

### other 01
The same recipe works for any diagram. Here is a smaller one with two states. On a zero it stays where it is and outputs zero, and on a one it switches to the other state and outputs one.
One flip-flop holds the state, and a little logic does the rest.

### other 02
Real processors are full of machines like this. The controller of a cache, for instance, steps through states as it serves a request, first checking, then fetching from memory, then storing.
Any step by step procedure with a fixed number of situations can be built from a register and logic.

## 09 · close

### close 01
So a register in a loop can remember anything we can number, and the logic decides how that memory changes.
There is one more use for a register, and it has nothing to do with remembering. Sometimes we add one just to make the clock faster.

> End card recap:
> - Logic without memory cannot tell two moments apart when the input is the same.
> - A finite state machine: states, and arrows labelled input/output.
> - Number the states, and the arrows become a truth table: present state, input → next state, output.
> - Any state machine is a register for the state plus combinational logic for the table.

---

# Episode 5 · A Register to Go Faster

> The notes mark this page as out of scope for the midterm; it returns with the five-stage datapath.
> Worked example: adder 5 ns, shifter 3 ns, clock-to-q 1 ns, setup 1 ns. One stage: period 10 ns.
> Two stages: 7 ns and 5 ns, period 7 ns, latency 14 ns. Data: 3 + 1 = 4, shifted left once = 8.

## 01 · recap

### recap 01
The clock period has to cover the slowest route from one register to the next.
Today we use that rule backwards. If a route is too slow, we change the route.

## 02 · one_stage — add, then shift

> Picture: register, adder, shifter, register in a row, delays written on each part. A pair (3, 1)
> flows through: 4, then 8. Under it the four delay segments laid end to end: 1 + 5 + 3 + 1 = 10.

### one_stage 01
Here is a piece of a processor. Two numbers come out of a register, an adder adds them, a shifter shifts the sum, and the result goes into a second register.
For example three plus one is four, and shifted left by one bit that becomes eight.

### one_stage 02
For the timing, say the adder takes five nanoseconds and the shifter three, and each register has a clock to q delay of one and a setup time of one.
The only route goes through everything, so the period is one plus five plus three plus one, which is ten nanoseconds.

### one_stage 03
At every edge a new pair goes in on the left, and the previous result is caught on the right.
So we get one result every ten nanoseconds, and each result takes ten nanoseconds from going in to being caught.

## 03 · idea — cut the route in two

> Picture: the segment bar 1 + 5 + 3 + 1 stays. A gap opens between adder and shifter and a third
> register drops in. The bar splits into 1 + 5 + 1 = 7 and 1 + 3 + 1 = 5; the 7 is kept as the period.

### idea 01
Suppose that is not fast enough. We can't make the adder or the shifter any quicker.
But notice why the period is long. It is long only because one signal must get through both of them between two edges.

### idea 02
So let's stop asking for that. Put a third register between the adder and the shifter.
Now the sum is caught in the middle at one edge, and the shifter works on it during the next period.

### idea 03
Each period only has to cover one of the two halves. The first half is one plus five plus one, seven nanoseconds, and the second is one plus three plus one, five.
One clock drives all the registers, so the period has to suit the slower half. That gives seven nanoseconds instead of ten.

## 04 · flow — a new input at every edge

> Picture: the three registers and two blocks in a row; under them a grid, one row per clock edge, one
> column per register, filling in: (3,1) | – | – ; (2,5) | 4 | – ; (6,2) | 7 | 8 ; … Values move one
> column right at each edge.

### flow 01
Watch the data move. At the first edge the pair three and one goes in.
At the second edge its sum, four, is caught in the middle. And at that same edge a new pair goes in on the left, because the adder is free again.

### flow 02
At the third edge the first result, eight, is caught on the right. The second sum moves to the middle, and a third pair goes in.
From then on a finished result comes out at every edge, and two computations are always under way at once, one in each half.

## 05 · trade — throughput against latency

> Picture: two rows to compare, before and after. First row: results per time (one per 10 ns, one per
> 7 ns). Second row: time for one item (10 ns, then two periods = 14 ns). The 14 is broken into its
> parts so the 4 extra nanoseconds are visible: 2 for the added register, 2 of waiting in the fast half.
> The notes give the latency as the sum of the two halves (12 ns here); with one clock at 7 ns it is 14.

### trade 01
Now compare the two designs. Before, we got one result every ten nanoseconds, and now we get one every seven.
The number of results per second is called the throughput, and it has gone up by more than forty percent.

### trade 02
But follow one single pair. It needs two periods to get through, and two times seven is fourteen nanoseconds, where before it needed ten.
The time one item takes from start to finish is called the latency, and it got worse.

### trade 03
It got worse for two reasons. The item now passes an extra register and pays that register's clock to q and setup time.
And the faster half sits idle for two nanoseconds in every period, because the clock is set by the slower half.

### trade 04
This move is called pipelining. It is the right trade when you care about results per second, as a processor running a long stream of instructions does.
It is the wrong one when you only care how soon a single answer comes back.

## 06 · model — one shape for all three circuits

> Picture: the three circuits of the series side by side, small: accumulator, three-ones machine,
> pipeline. They morph into the same drawing: logic blocks (one colour) separated by registers
> (another), the clock line touching only the registers. Feedback arrows shown on the first two.
> Notes page 1 §5 (general model), placed last so it summarises what was watched.

### model 01
Step back and look at the three circuits of this series, the running sum, the machine that counts ones, and this pipeline.
They are all built the same way. There are blocks of logic with no memory, separated by registers, and a clock that connects to the registers and to nothing else.

### model 02
Sometimes a register's output loops back, as in the first two, and sometimes the data only moves forward. Registers can sit back to back, and so can logic blocks.
That is the whole model of a synchronous digital system, and a processor is a large one of these.

> End card recap:
> - A register between two blocks lets each block have its own clock period.
> - The period is set by the slowest stage.
> - Pipelining raises throughput (results per second) and makes latency (time for one item) worse.
> - A synchronous digital system: logic blocks separated by registers, one clock that drives only the registers.
