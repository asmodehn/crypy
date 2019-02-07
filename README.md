# crypy

## Design
We adopt here the stream/dataflow point of view, between "agents", to be more easily parallelisable and resilient, yet humanly manageable.

Each of these can be viewed as an "actor", spinning at a specified frequency, communicating with others over streams with a specific API/protocol/language.

This can be done in sync (entity component system) or async style (trio), but beware of traps when trying to mix the two styles.
Interfaces should probably be streams of events ( see [Scott Wlaschin talk](https://www.youtube.com/watch?v=AG3KuqDbmhM) and [Whitesnake](https://github.com/asmodehn/functional-python/) for references)

One important thing is that each of these must have a terminal/telnet interface, so that a human can dynamically configure its behavior, via a specific set of commands / programming language.
This needs to be a different interface than the streaming one for dataflow. We will call it the controlflow.

Another dimension is the logic relationships: the code required is interchangeable, managed via plugins/extensions. same for technical indicators, strategies, etc.
Their relationships are not related with the dataflow or the controlflow. If we consider the relationship between agents, it is alike "same logic" "same set of dependencies", or "different dependencies".
It can be consider alike a "deployment strategy", or a logicflow.

The timeframes between the controlflow, the dataflow, and the logicflow are quite different.
dataflow is high frequency data moving around.
controlflow is human speed : seeing what is happening on the system at a speed acceptable for humans, in a way that human can adjust it
logicflow is very low frequency of change, akin to a doing a deployment of a software with different constraints/configuration/machine
Note : all this is about relationships between actors, not about the code "inside" an actor.

## Concepts

- Broker : The cutoff point for communication with the "outside world"/the exchange. One place to kill in case of emergency. High Availability via redundancy eventually (similar to a webserver process pool).
It retrieves data from an Exchange E (ex: kraken) at a configurable frequency(sync), and store it locally to be able to provide it quickly to others.
For each owned asset reporter by the exchange, it will create and manage a "Holder".
It also accept or refuse order requests from Holders (for whatever criteria specified) and transmit them to the exchange.

- Holder : One per "owned asset/currency". It stays connected to the exchange (async), in order to find the best strategy for the asset.
If required it creates one trader per tradable pair related to his asset. It validates or refuse strategies from traders based on criteria configured by the human controller.
Note : traders have direct access to broker for communication, but they need a "validation stamp"/crypto-sign from holder.
Once a holder accepts a strategy, it specifies the amount the trader can use for this strategy, and if the trader opens a position, it commit suicide, killing all its traders, as it doesnt need to manage anything any longer.


- Trader : An agent that evaluates a strategy on a pair and simulate it, in order to calculate return ratio, and other indicators of potentialities of success.
Retrieve data form a broker, and propose strategies to the holder, who can accept or refuse it. the holder also gives the amount of asset available for this strategy.
The trader can then decide if the position is worth going into or not. If not it kills itself, and the holder creates a new one. memory of attempted trades comes from the holder who modfies the trader template.
After a successful strategy is accepted by the holder, the trader enters a position (communicating via broker) and monitors it (async).


Note : holders and traders are created from templates, that a human controller can modify, to be used on next broker iteration.
System needs to learn from failed strategies, failed positions, etc.
- On one pair, a trader, via its template, will evolve to select best strategies for this pair
- If a strategy doesnt work for multiple pairs, the holder will record that in its template, and upon next lifetime, will avoid it...
- If some assets usually give bad return, the broker will record that in its template/configuration, and upon next lifetime, will tend to divert the asset.




## MVP : 
