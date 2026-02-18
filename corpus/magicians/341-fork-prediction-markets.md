---
source: magicians
topic_id: 341
title: Fork prediction markets
author: jannikluhn
date: "2018-05-11"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/fork-prediction-markets/341
views: 903
likes: 3
posts_count: 3
---

# Fork prediction markets

Hey everyone!

It was supposed to be a surprise, but since the idea is [out there](https://medium.com/eip0-summit/eip0-summit-statement-of-intent-to-support-ethereum-governance-initiatives-e54ff782933) already, I figured I could ask for early feedback. I’m working on prediction markets for forks as a signal for the governance process.

A major part of blockchain governance is deciding when and which protocol changes to implement. If such decisions are made without consensus, the blockchain forks. In general, forks should be avoided because they split the community and break existing network effects. Thus, we should strive to create consensus before implementing changes. However this is quite difficult as determining if there is consensus or not is pretty hard in the decentralized and open setting of blockchain communities.

One example is the DAO fork: Many [citation needed] thought that Ethereum Classic would die quickly, but this did not happen. If the community would have known that (or had a somewhat reliable prediction that this would happen) they might have decided differently: Either to not fork or to engage in more discussions to find a better compromise.

Prediction markets are an intriguing tool to gather information from the crowd and make it easily accessible to everyone. Here’s a quick summary of how they work within the Gnosis framework: First, the market is setup by defining an event with its possible outcomes, and recording this in a smart contract. Next, anyone can create tokens for each outcome by depositing a collateral. Those tokens are traded and prices emerge. When the event is over, an oracle resolves the market providing the real-world outcome. At this point, ”right” outcome tokens can be exchanged for the collateral, whereas “wrong” outcome tokens get nothing. This entitlement for collateral makes rational markets find prices that correspond to the probabilities for each potential outcome.

How would a fork prediction market look like? Quite simple: The event should clearly state the proposed protocol changes and the implementation deadline. In many cases, this could just be the corresponding EIP document. There will be three possible outcomes: The protocol change is accepted, it is dismissed, or a contentious fork appears.

I’m eager to try out this approach, even though (or because?) it’s an experiment that I’m not entirely convinced will work out. One issue is that if the community uses the market as a signal in the governance process (which is the whole point), a feedback loop is created: The market gives some prediction which that the governance process then takes into account, making the market in turn update their prediction, and so on.

Another problem is finding adequate definitions of “fork” and “non-fork”. In principle, a single node is enough to create a fork. Such a fork would be irrelevant though and predicting it of little value. Furthermore, it would make the prediction market gameable: One could effortlessly create a fork with the sole intention to change the outcome of the market. Token price and transaction volume are other criteria that are straightforward to measure, but are also prone to manipulation. A good compromise is requiring a certain proof of work to accumulate in some defined timespan (say, 1 month). Faking this is possible, but would come with a high and well-defined cost.

Next issue: What is the oracle? For now I’ll offer to be the oracle, in the future I think it should be a committee of trusted community members. The issue with both approaches is though, that centralized oracles can deliberately decide on the wrong outcome, resulting in a huge, risk-free profit for them if they bought the corresponding tokens first.

Final problem: Regulations. It is unclear to me what the legal implications of running a prediction market oracle or a market maker are. Mainly for this reason, I’m going to launch this on a testnet first (probably Rinkeby). Unfortunately, this means that there is no financial incentive to buy and sell rationally. To still make the result meaningful, participating in the market will require a special token, which I’ll distribute to interested and trusted community members (for free, of course).

I’m working on this project in my free time on weekends, but I hope to publish this project in a couple of weeks. For now, I’d appreciate any feedback! And if you’d like to participate, please send me your address to receive some tokens at launch!

## Replies

**MicahZoltu** (2018-05-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jannikluhn/48/2990_2.png) jannikluhn:

> One issue is that if the community uses the market as a signal in the governance process (which is the whole point), a feedback loop is created: The market gives some prediction which that the governance process then takes into account, making the market in turn update their prediction, and so on.

IMO this is the biggest problem.  If this is used as a signal, then it turns into a Keynesian Beauty Contest, which doesn’t provide meaningful value.  If it isn’t used as a signal, then it isn’t part of the governance process and instead is just a “fun way to bet on the future”.

Also, once Augur launches you could just use that, plus it solves your oracle problem for you.

---

**jannikluhn** (2018-05-13):

Interesting! You’re saying that if people use it as a signal, it becomes meaningless. Continuing that argument: If it’s meaningless people will stop considering it. If they stop considering it, it will become meaningful again, people will use it again, and so on.

So both significance of the prediction and weight of the signal oscillate and the relevant question becomes: Around which point does it oscillate and at which frequency and amplitude? Which is probably quite hard to answer in advance.

Having said that, even if the market would not be used as a signal at all I think it can have value as it gives users more information when preparing for the potential fork:

- exchanges need to prepare for listing the token of the forked chain
- (minority) client developers need to decide on implementing the rules of the fork or not
- traders could take the fork probability into account when determining the value of the token
- dapp developers need to decide in advance on which fork they want to live (and discuss this with their respective communities)

(Each of those may in turn influence the governance process, but then we are back at the oscillation argument above.)

