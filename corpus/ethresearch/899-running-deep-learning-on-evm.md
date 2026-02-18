---
source: ethresearch
topic_id: 899
title: Running Deep Learning on EVM
author: kladkogex
date: "2018-01-25"
category: EVM
tags: []
url: https://ethresear.ch/t/running-deep-learning-on-evm/899
views: 16312
likes: 29
posts_count: 32
---

# Running Deep Learning on EVM

At my company we are starting an experimental project to extend EVM with basic deep learning capabilities.

This is not to train a neural network, but to use a pre-trained neural network  inside a smart contract.  Computation-wise using a pre-trained neural network is actually not  so much more expensive than doing, say, RSA.

I understand that this may be a bit too heavy for the official Ethereum blockchain, so in our case we will run the EVM on a separate permissioned cluster with BFT-like consensus.

The current plan is that:

1. A pre-trained network is saved on the blockchain. We can use some of existing
neural network serialization standards such as the ones used in Keras framework
2. The EVM will need to pull the neural network from the blockchain.
3. In the simplest case there we add a single predict instruction similar to predict from Keras framework.  This instruction will take a fully qualified name of the neural network and an input data array, run the neural network and produce output data.

As an example input data could be an English-language string, and output will be a German translation of this string.

One problem that we will need to solve in the process is introducing deterministic floating point numbers such as  IEEE 754-2008 into the EVM in some way.

If there are other people interested to run AI on EVM, we would be willing to cooperate on this to establish a standard that everyone uses …

## Replies

**vbuterin** (2018-01-25):

Can I ask what the goal of this is? Running deep learning inside the EVM is probably not the solution.

---

**chriseth** (2018-01-25):

You might want to take a look at this approach: https://github.com/ethereum/research/issues/3

Basically the idea is to use a rational activation function and encoding the trained neural network inside a zkSNARK circuit. You can build it so that the weights are part of the private input and then basically have a smart contract confirm the result of a neural network applied to a certain input while not revealing the actual network weights.

An application of this would be verifying results to a competition that are ranked using a neural network. The reason why you might not want the weights to be public is that it is usually easy to fool a neural network once you know the weights.

The only problem with this approach is that the person generating the proof has to know the internal weights.

---

**kladkogex** (2018-01-25):

Well - I think many people have expressed different ideas about running a neural network as a trusted application so that all parties agree to the outcome.

As a toy example, you can consider an example of a smart contract that is an decentralized Uber which pays to drivers based on their behavior. The smart contract needs to differentiate bad drivers from good drivers by running a neural network on  driver historical behavior. Good drivers are get paid and bad drivers do not get paid.

What you do, you feed driver’s trajectory into a neural network, and then the driver gets either paid in-full or penalized  based on her behavior …

Another example is when a smart contract buys apples from a supplier and it needs to find out whether an apple is a good apple or a bad apple based  on chemical analysis data. Essentially you feed into the neural network 100 data points of chemical analysis and the network tells you whether the apple is good or bad.

In general, I think to answer your question, anytime a smart contract runs on data, there is no need to use neural networks. On the other hand  if a smart contract runs on Big Data, then, arguably, you need a neural network to extract important info from the data, as the data itself is too complex.

In the examples above the neural network does not need to be confidential or encrypted in anyway, it could be a pre-trained network which is trusted by all participants.

I am not saying EVM is a perfect place to run neural networks, on the other hand making it some kind of an simple extension to EVM/Solifity would draw many developers. Another possibility is to run a totally different thing and then feed the results into Ethereum somehow …

---

**rax** (2018-01-25):

In your driving example, wouldn’t we have to re-train the network as drivers realize how to maximize their profit without neccesarily driving in a way that would be “best” for a passenger? I mean that the trained network will have a very low probability in being perfect from a passengers point of view. Then I guess either training would have to be done on the blockchain somehow, or users should regularly be allowed to vote for a new trained network or training scheme to be used.

This could also apply to the apple sale scenario I guess, but on a much larger time scale. (Like the apple salesman tampering with the genes through generations to maximize the profit he would get form the network on the blockchain but minimizing his costs in production.)

Even if the network weights and/or other parameters are hidden as suggested by chriseth, I think patterns would become evident over time and would be subject to abuse to maximize profits.

Just some thoughts ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**kladkogex** (2018-01-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/rax/48/239_2.png) rax:

> In your driving example, wouldn’t we have to re-train the network as drivers realize how to maximize their profit without neccesarily driving in a way that would be “best” for a passenger? I mean that the trained network will have a very low probability in being perfect from a passengers point of view. Then I guess either training would have to be done on the blockchain somehow, or users should regularly be allowed to vote for a new trained network or training scheme to be used.

Agree - actually Uber drivers are getting really bad - have you noticed that if they want you  to cancel sometimes they keep on moving their car slightly  to fool the algorithm ?) I think if they just do not move the car for 5 min after they accept they are automatically penalized.

This example shows though, that simple algorithms are easy to fool, a machine learning algorithm is harder to fool.  Actually the best way to find how to fool a neural network is to run another neural network called [adversarial network](https://en.wikipedia.org/wiki/Generative_adversarial_network).

Re-training on a decentralized network would require GPUs - could also be done though …

---

**mewwts** (2018-01-26):

I personally think this makes sense. The weights of the network can then be updated through a smart contract call itself.

However, even though the weights might be completely in the open, the fact that you as the owner of the contract is the only one allowed to *train* the network and upload the weights, means that the people interacting with this contract will need to trust your good intentions.

In the case of the decentralized Uber - the driver and the passenger will need to trust you as a company to train a balanced model. It’s hard for both those groups to say if that algorithm is fair or not.

Another point is that neural nets can have millions of parameters. Updating such a network often would be very costly.

I do think doing this just for the purpose of doing it has merit though.

---

**kladkogex** (2018-01-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/mewwts/48/637_2.png) mewwts:

> However, even though the weights might be completely in the open, the fact that you as the owner of the contract is the only one allowed to train the network and upload the weights, means that the people interacting with this contract will need to trust your good intentions.

Good point!)

Do you think it could be fixed by a procedure like that:  the neural network can be updated by a vote of a governing body of people, that drivers and passengers trust?  How to form this body then ? Should there be some kind of a token for that?

Imho governance is a huge question -  I was born in a country (USSR) which tried a communistic experiment  - it failed profoundly !   In the USSR taxi drivers were taking advantage of passengers in all possible ways, in addition to that they were stealing gas all the time ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

A simplistic approach, where you pass all the power to the drivers will probably fail, you need to take into account both the drivers and the passengers somehow, the question is, is there a sustainable governance model to do it?

---

**kladkogex** (2018-01-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/mewwts/48/637_2.png) mewwts:

> Another point is that neural nets can have millions of parameters. Updating such a network often would be very costly.

Good point !   Usually if one retrains deep neural nets, all parameters change.  One can though introduce “gas-optimized”  re-training, where only some weights change for each retraining epoch,  so you pay less to update weights …

---

**mewwts** (2018-01-26):

I guess techniques such as [quantization](https://www.tensorflow.org/performance/quantization) would become very important in this scenario.

---

**kladkogex** (2018-01-26):

Interesting - never used it before. My understanding of the idea is that you cant train in low precision, but once trained, you can quantize to low precision and it will still work …

---

**mewwts** (2018-01-27):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Do you think it could be fixed by a procedure like that:  the neural network can be updated by a vote of a governing body of people, that drivers and passengers trust?  How to form this body then ? Should there be some kind of a token for that?

I mean this is only an issue in usecases like the dUber case, and to be honest the more I think about this, the further I go down the rabbithole, and the less it has to do about the specific issue of doing a forward pass in a neural net.

However, in the case, it’s the drivers and the passengers that *create* the training data. If you could somehow verify that the network is trained on a set of transactions..

---

**veqtor** (2018-01-30):

Why not solve it in a simpler way:

To work on a job, you will need to stake some amount of ether

When creating a job, you send a swarm hash for the set of data to be predicted upon.

Along with this hash, the sender also submits a salted verfication set

A number of nodes then perform the prediction and salt their result hash, which is merkle tree encoded (it needs to be a quantized result to avoid differences in floating point implementations)

When enough nodes have submitted their hash, they reveal their hash.

When the hashes have been revealed, the submitter reveals the salt for the verification, this decodes the verification which then loops through the different answers, verifying if they’ve correctly computed the verification answers. Any node that tried to cheat is robbed off their staked eth. The rest split the reward for the computation.

---

**PhABC** (2018-01-30):

In my opinion, DL might be an overkill for a Uber driver evaluation model on the EVM, especially since the EVM does not support vector operations at the moment (see [EIP-616](https://github.com/ethereum/EIPs/issues/616) for an interesting proposal).

To me, it seems like an off-chain solutions like Truebit could be a better way of tackling this problem.

---

**denett** (2018-01-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/veqtor/48/660_2.png) veqtor:

> The rest split the reward for the computation.

If you create multiple nodes and submit the same answer multiple times, you will get a bigger piece of the pie.

A more sophisticated version of your proposal by [@kladkogex](/u/kladkogex) was discussed in [this thread](https://ethresear.ch/t/proof-of-sequential-work/866) and seems to encourage centralization.

---

**kladkogex** (2018-01-31):

![](https://ethresear.ch/user_avatar/ethresear.ch/phabc/48/35_2.png) PhABC:

> To me, it seems like an off-chain solutions like Truebit could be a better way of tackling this problem.

The problem is that there is currently not a single person in the world that can mathematically prove TrueBit security.

Most good BFT and Blockchain protocols have reasonable mathematical models  proofs that prove security either deterministically or at least probabilistically at least under some assumptions (such as 2/3 of nodes, deposits, PoW, you name it …)

---

**cburgdorf** (2018-02-03):

I wonder if it would be feasible to take something like keras.js and port it to a solidity library.

https://github.com/transcranial/keras-js

Just for clarity. Keras is a Deep Learning framework that uses TensorFlow behind the scenes. It’s basically an abstraction on top of TF to make working with TF more pleasant and higher level.

Now what keras.js enables is, you can take a trained model and run the predictions in the browser. I wonder if the same approach could work for Ethereum. So you take a trained Keras model which essentially is just a huge bag of numbers and then run a couple of matrix multiplications and geometric functions over them to get the prediction. This is basically what keras.js essentially does.

I think there’s nothing really that would want prevent one to apply the same approach in solidity, right? Just the fact that the more complex the model is the more gas would it take to run the predictions.

---

**kladkogex** (2018-02-03):

Chris - thank you, I was aware of Keras but not aware of Keras.js. Keras is definitely the leading library now for abstracting out deep learning implementation details.

The question is how whats the MVP implementation to add a Keras.js like prediction opcode to Ethereum Virtual Machine, because Solidity ultimately gets compiled into EVM.

Here is a link to Ethereum Yellow paper that describes the current EVM implementation

[Ethereum Yellowpaper](https://github.com/ethereum/yellowpaper)

---

**cburgdorf** (2018-02-03):

> Keras is definitely the leading library now for abstracting out deep learning implementation details

I agree. We’re working on a Machine Learning platform that lets people start playing with Keras and other ML libs from right within the browser (even though we also have a CLI around the corner). Experiments run on our cloud infrastructure though.

For instance, here’s a link to some easy Reinforcement Learning experiment that I did:

https://machinelabs.ai/editor/SyPFkpjEG/1516292262547-ByJnOH0V

Back to the topic:

Well, I think if it doesn’t exist yet then probably an opcode for matrix multiplications would be useful. But even without that it should be possible to just come up with an MVP state solidity library that does the basic math on top of todays EVM.

After all, you can do matrix multiplications by hand:



      [mathsisfun.com](https://www.mathsisfun.com/algebra/matrix-multiplying.html)





###



Math explained in easy language, plus puzzles, games, quizzes, worksheets and a forum. For K-12 kids, teachers and parents.










So the way I understand it, one could build a keras-solidity library today even though it may be inefficient unless further opcodes are added to improve the speed of some underlying mathematical operations.

---

**d10r** (2018-02-16):

The idea to integrate support for neural networks into Ethereum recently started to rotate in my head too, glad to have found this thread - [@kladkogex](/u/kladkogex) please keep us updated!

I guess Vitalik’s scepticism comes from the assumption that the intention is to run *deep learning* on-chain. But the point is to use models trained off-chain and only do *inference* on-chain (which is much cheaper).

My line of thought was not to integrate it into the EVM, but to add it as a kind of additional runtime, similarly to how Parity allows WASM contracts alongside EVM contracts (see [doc](https://paritytech.github.io/wiki/WebAssembly-(WASM)) - at least that’s how I understood it).

Similarly, an Ethereum client could be extended with a runtime for neural networks (I guess Tensorflow/Keras would be best suited). That way it should be possible to run these computations more efficiently (e.g. even using GPU support).

It may be a bit of a challenge to guarantee deterministic results, thus quantization may be a good idea not only for performance.

The EVM would only need a mechanism for making a call to the neural network runtime and handle its result.

This is however just an intuition driven guess about what a reasonable architecture may look like as I don’t yet have much expertise in ML.

Besides hitting buzzword/bullshit bingo, I’m quite sure such a construction would open up a huge new playing ground. Putting an AI in charge of distributing economic rewards (this could be tokens created out of thin air) sounds like a pretty powerful possibility to me…

---

**kladkogex** (2018-04-20):

Does any one here know how to run Tensorflow in a reproducible fashion on different NVIDIA cards?

We are adding Tensorflow as a set of pre-compiled smart contracts.  For the software version of Tensorflow we can get it to be reproducible by fixing seeds of the pseudo-random generator and then compiling using -sse2 flag of gcc …


*(11 more replies not shown)*
