# Glossary (Introduction unit; shared terms follow the function-approximation glossary)

| Preferred term | Meaning / note | Avoid |
|---|---|---|
| deep learning | simulated analog circuits whose parameters are set by data-driven optimization (the lecture's definition) | "AI" as a synonym |
| circuit | the parameterized computation: multiply, add, max/threshold | "model" only where the definition is quoted; "model" is fine from Ep 2 on |
| element | one unit of a circuit (one perceptron / one hidden unit) | "neuron" (except "Rosenblatt's adaptive neuron", the historical name) |
| parameters, knobs, weights, bias | knobs = weights and bias, said once as the picture of the parameters | "params" |
| deep | information flows through several elements in sequence before the output | |
| optimization algorithm | sets the parameters from data (perceptron update here, gradient descent later) | "trainer" |
| training data / new data | data used to set the parameters / data the circuit has not seen; "fresh points" only in the toy experiment | "unseen data" |
| pattern | the relevant regularity in the data that should carry to new data | |
| perceptron update | w <- w + y x, b <- b + y on a misclassified point | |
| learning rate (eta) | step size of gradient descent | "step length" |
| exclusive or | XOR example, spoken "exclusive or" | |
| engineering vs alchemy | the lecture's framing: knobs with reasons vs stirring the pile | |
