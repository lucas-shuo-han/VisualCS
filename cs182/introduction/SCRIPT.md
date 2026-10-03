# CS182 · Introduction — narration

Generated from the episode subtitles (.srt).


## 01-what-is-dl

- `00:06` So what is deep learning, really, underneath all the excitement?
- `00:09` The definition this course runs on is simulated analog circuits, which just means circuits with knobs on them.
- `00:16` And nobody turns those knobs by hand.
- `00:18` An optimization algorithm sets them, and it's driven by training data.
- `00:22` The whole point is that the circuit captures a pattern in its training data.
- `00:27` So when new data arrives, the same circuit still gives a useful answer.
- `00:32` Let's start small, with Rosenblatt's adaptive neuron.
- `00:36` Each input passes through a knob, called a weight, that scales it.
- `00:40` Then we add everything up, along with a bias.
- `00:43` Feed in two and one, and we get one point six, minus zero point five, plus zero point two,
- `00:49` which comes to one point three.
- `00:52` Then a threshold turns that number into an answer.
- `00:55` It's positive, so the circuit says plus one.
- `00:57` Now flip the sign of both weights.
- `00:59` With the same wires and the same input, the circuit says minus one instead, so the knobs really are the program.
- `01:08` So where does the word deep come in?
- `01:10` It comes from chaining elements together,
- `01:13` so that the signal passes through several of them in a row before it reaches the output.
- `01:18` Each element is still just multiply, add, and take a max, which is the same pattern as before, repeated in sequence.
- `01:27` If nobody sets the knobs by hand, then the data has to do it.
- `01:30` Here are twenty labeled points, and a line drawn from a random starting guess.
- `01:35` The line is where the weighted sum hits zero, and every point on the wrong side gets a red ring.
- `01:40` Right now that's ten mistakes.
- `01:43` The fix is almost too simple.
- `01:45` We grab one mistake, add its label times its input to the weights, and add its label to the bias.
- `01:51` The line swings toward that point, and the mistakes drop from ten to four.
- `01:56` Do it again and we're down to two.
- `01:58` But the next update jumps back up to six, so a single step can make things worse.
- `02:03` Keep going anyway, and after four updates there are zero mistakes.
- `02:07` Nobody chose those knob settings, the data did.
- `02:12` But we never really cared about those twenty points.
- `02:15` So let's draw a hundred fresh points from the same source, and the circuit gets ninety-two of them right.
- `02:20` The misses all hug the boundary, because the learned line is close to the real rule, just not exactly on it.
- `02:28` Now change the rule behind the labels.
- `02:30` The same circuit gets only fifty-three right, which is a coin flip, because it learned one pattern and not this one.
- `02:37` That's why the definition says relevant pattern.
- `02:39` Learning only pays off if the new data follows the same rule.

## 02-alchemy

- `00:06` Is deep learning really as new as it feels?
- `00:08` Back in nineteen fifty, Turing was already picturing machines that learn their way to intelligence.
- `00:14` In nineteen fifty-seven, Rosenblatt built the perceptron,
- `00:17` and around the same time the least mean squares rule showed up in adaptive signal processing.
- `00:23` Then in nineteen sixty-nine, Minsky and Papert wrote a whole book about what these networks can't do.
- `00:29` In nineteen eighty-six, backpropagation made deep networks trainable,
- `00:33` and by nineteen eighty-nine a network called LeNet was reading handwriting.
- `00:37` After that the field drifted toward probabilistic and convex methods, with mostly shallow models.
- `00:43` Around two thousand six, deep networks started creeping back.
- `00:47` And in twenty twelve, Krizhevsky's AlexNet beat every other method on ImageNet.
- `00:52` From the perceptron to AlexNet is fifty-five years.
- `00:55` So learned circuits are an old idea, and what's new is that they finally work this well.
- `01:02` So what was the complaint back in nineteen sixty-nine?
- `01:06` Take four points labeled by exclusive or, which is plus one when exactly one input is on.
- `01:11` One element can only draw one line.
- `01:13` Try any line you like, and you can get three of the points right, but never all four.
- `01:20` But stack two elements and the problem goes away.
- `01:23` Put two ramps on the sum of the inputs, where the second one only switches on once the sum passes one.
- `01:30` Then take the first ramp minus twice the second.
- `01:33` Run the four rows through, and out comes zero, zero, one, one, which is exactly exclusive or.
- `01:39` So one element can't do it, but a stack can.
- `01:42` And making stacks trainable is exactly what backpropagation did in nineteen eighty-six.
- `01:49` Now for an awkward question, which is whether deep learning is engineering or alchemy.
- `01:55` There's a famous xkcd comic about exactly this.
- `01:58` Its machine learning system is a big pile of linear algebra,
- `02:01` where you pour data in on one side and collect answers on the other.
- `02:06` And if the answers come out wrong, you just stir the pile until they start looking right.
- `02:10` That's what alchemy looks like.
- `02:15` So what would engineering look like instead of stirring?
- `02:18` Take a single knob, the learning rate, and run gradient descent on a simple bowl, starting from w equals one.
- `02:24` Here are four settings of that knob.
- `02:27` At zero point one and at zero point four, w settles down to zero.
- `02:31` At zero point five it bounces back and forth forever, and at zero point six it blows up.
- `02:37` The reason is that each step multiplies w by one minus four eta,
- `02:41` and that factor only shrinks w while eta stays under one half.
- `02:45` That's engineering, not stirring.
- `02:47` It's a knob with a reason behind it, so you know where it works and where it breaks.
- `02:54` This course sits on top of three earlier ones, and they line up with the three parts of the definition.
- `03:00` Machine learning brings the patterns, optimization brings the circuits and their knobs,
- `03:05` and probability tells us about new data.
- `03:08` So that's the plan for the course.
- `03:10` We'll design deep networks, look inside them, and understand why they work.
- `03:17` There's one last thing to read alongside this, which is Terence Tao's essay, Mathematics in the Age of AI.
- `03:23` He sets aside what the tools can do, and asks what a field is actually for.
- `03:27` That's a question worth asking of deep learning too.
