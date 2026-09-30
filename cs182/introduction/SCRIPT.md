# CS182 · Introduction — narration

Generated from the episode subtitles (.srt).


## 01-what-is-dl

- `00:06` Here is the definition this course is built on. Deep learning uses simulated analog circuits to process information.
- `00:13` The parameters of those circuits, their settings, are chosen by an optimization algorithm that is driven by data.
- `00:20` The goal: the learned circuit has captured the relevant pattern in its training data, so it can solve problems on new data.
- `00:28` Start with the smallest circuit, Rosenblatt's adaptive neuron. Each input passes a knob, a weight, that scales it.
- `00:36` Add the scaled inputs and a bias. With these settings, the input 2 and 1 gives 0.8 times 2, minus 0.5 times 1, plus 0.2.
- `00:48` A threshold turns the sum into an answer: 1.3 is positive, so the circuit says plus one.
- `00:55` Turn the knobs and the same circuit says minus one instead. The parameters are the program.
- `01:02` Deep means that information flows through several such elements, one after another, before it reaches the output.
- `01:09` Each element still just multiplies, adds, and takes a max: the earlier unit's pattern, repeated in sequence.
- `01:18` Who sets the knobs? Data does. Twenty labeled points and a line from a random start.
- `01:24` The line is where the sum is zero. Points on its wrong side are circled in red: ten mistakes.
- `01:30` The perceptron update: take a mistake, add its label times its input to the weights, and its label to the bias.
- `01:37` The line swings toward that point, and the mistakes drop from ten to four.
- `01:42` Repeat. Now two mistakes. A step can also make things worse, and here the count jumps to six, but the updates keep correcting.
- `01:50` After four updates, no point is misclassified. The knob settings came from the data, not from a person.
- `01:58` But the goal was never these twenty points. Draw a hundred fresh points from the same source, and the circuit gets most of them right.
- `02:06` The few mistakes sit near the boundary: the learned line is close to the true rule, not identical to it.
- `02:13` Now let the labels follow a different pattern. The same circuit is right about half the time: it captured one pattern, not every pattern.
- `02:21` That is why the definition says a relevant pattern: learning is only as good as the match to new data.

## 02-alchemy

- `00:06` The idea is old. In 1950, Turing describes learning as a path to machine intelligence.
- `00:12` In 1957 Rosenblatt proposes the perceptron. In the same years, L M S appears in adaptive signal processing.
- `00:21` In 1969, Minsky and Papert publish a book on the fundamental limitations of neural networks.
- `00:27` In 1986, backpropagation becomes a practical way to train deep networks, and in 1989 LeNet reads handwriting.
- `00:35` Then attention shifted to probabilistic methods and convex optimization, mostly on shallow models.
- `00:42` Around 2006 deep networks regain attention; in 2012 Krizhevsky's AlexNet beats all methods on ImageNet.
- `00:50` From the perceptron to AlexNet is 55 years. The idea of a learned circuit is old; the breakthrough is recent.
- `01:00` What limit was 1969 about? Take four points labeled exclusive or: plus one when exactly one input is on.
- `01:08` One element draws one line. Try every line: some get three points right, none gets all four.
- `01:16` Stack two ramps on x1 plus x2, the second bending at 1, and read out first minus twice the second.
- `01:24` Compute the four rows: y comes out 0, 0, 1, 1. That is exclusive or, exactly, with no line in sight.
- `01:33` One element cannot, a stack can. Making stacks trainable is what backpropagation did in 1986.
- `01:42` Is deep learning engineering, or alchemy? The lecture puts that question next to a famous xkcd comic.
- `01:49` The comic's machine learning system: pour the data into a big pile of linear algebra, collect the answers on the other side.
- `01:56` What if the answers are wrong? Just stir the pile until they start looking right. That is the alchemist's method.
- `02:04` The learning rate decides whether training works. Try a bowl, starting from w equals 1.
- `02:10` Try four learning rates. 0.1 and 0.4 settle to zero, 0.5 bounces forever, and 0.6 blows up.
- `02:19` No magic: each step multiplies w by one minus four eta. It shrinks only while eta stays below two over four, which is 0.5.
- `02:30` That is engineering: a knob with a reason, which predicts where it works and where it fails.
- `02:37` Three earlier courses feed this one, and they line up with the definition.
- `02:42` Machine learning brings the patterns, optimization the circuits and knobs, probability the new data.
- `02:49` So the course is about designing, visualizing and understanding deep networks, and knowing why they work.
- `02:57` A companion reading: Terence Tao's essay, Mathematics in the Age of AI.
- `03:02` It sets aside what AI tools can do and asks what the goals and values of a field are. We can ask the same of deep learning.
