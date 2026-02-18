---
source: ethresearch
topic_id: 3587
title: Request for participation in Futarchy experiments
author: mkoeppelmann
date: "2018-09-28"
category: Economics
tags: [futarchy]
url: https://ethresear.ch/t/request-for-participation-in-futarchy-experiments/3587
views: 8184
likes: 18
posts_count: 18
---

# Request for participation in Futarchy experiments

Hey - quite a while ago [@vbuterin](/u/vbuterin) suggested a bunch of crypto economic experiments [here](https://www.reddit.com/r/ethereum/comments/453sid/empirical_cryptoeconomics/)

We (Gnosis) are since a long time interested in providing the tools for projects to use

[Futarchy](https://blog.ethereum.org/2014/08/21/introduction-futarchy/) for decision making. Thus we have been naturally interested in those experiments around market manipulation.

Long story short - we are now ready to start those experiments and are looking for people to participate. While in principal those experiments are open and anyone can participate we nevertheless want to have an active core group to make sure it makes sense to start them.

On a high level there will be a special actor that will get some incentives to MANIPULATE MARKET PRICES. And ideally we will be able to prove that this actor is not able to do this even if incentives are high.

An canonical example that is often given for Futarchy is the decision to fire the CEO (or pick a different CEO). So the setup is that you have two conditional markets of some success metric of the company (e.g. future revenue/ earning per share) under the condition that CEO A or CEO B is selected. The company would hire according to the forecast of the market. We want to simulate a decision where the market has CLEAR KNOWLEDGE that CEO A is better - but CEO B has of course an incentive to be hired nevertheless.

To simulate the future revenue of the company we will instead predict the difficulty (for CEO B) and the difficulty +x for the CEO A. We do not know what the correct forecasts are but we know that the difference should be +x. Now CEO B will get some payout IF the difference is smaller than X.


      [docs.google.com](https://docs.google.com/presentation/d/1omvPYWndBZ0dat2j51-wQnaSvy6ClfhzUhRWCu9lrrY/edit#slide=id.g2737733097_0_170)


    https://docs.google.com/presentation/d/1omvPYWndBZ0dat2j51-wQnaSvy6ClfhzUhRWCu9lrrY/edit#slide=id.g2737733097_0_170

###

Futarchy experiments Supported by the Ethereum Foundation








(Experiment Setup by [@josojo](/u/josojo))

At this stage we would like to see who is interested in participating in those experiments. Someone will need to provide the payout for successful market manipulation. So we are now looking for people that are confident that this is NOT POSSIBLE and that are willing to contribute for this incentive pool. If the mechanism works (market can not be manipulated) this money will be given back and we would add a premium to insentience participation in the experiment.

Let us know what you think!

## Replies

**satroan** (2018-09-29):

Where do you go to take part?

---

**ralexstokes** (2018-09-29):

Yeah I would like to follow the experiment!

---

**ankit98** (2018-09-29):

Where do we apply to take part in this experiment?

---

**JeffEmmett** (2018-10-01):

Would love to join in the fun!

---

**nmontone** (2018-10-05):

I’d love to participate

---

**Daniels** (2018-10-05):

Hi [@mkoeppelmann](/u/mkoeppelmann) [@josojo](/u/josojo), really love the experiment and of course love to participate!

I have some skepticism regarding the scale this experiment takes places in: if we are only a few dozen or hundred people then can we really simulate the outcome of a market representing the collective behaviour of millions of agents ?

In particular one actor is not supposed to be able to manipulate prices on their own but if we are only say 15 people it would be easy for a large wallet to create a standoff situation. Not sure we can as a small group of researchers call the bluff of EF’s or Gnosis’ wallet with our life savings… while in a market you would need true collective belief in an outcome (or certainty of manipulation) to move the price towards one decision or another.

How would you suggest us being reassured our balls won’t be squeezed? (metaphorically speaking)

---

**josojo** (2018-10-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/daniels/48/2386_2.png) Daniels:

> How would you suggest us being reassured our balls won’t be squeezed? (metaphorically speaking)

If you plan to your trades well, you should definitively not loose any money.

Either you would making money by predicting correctly that the markets can not be manipulated, or  markets are getting successfully manipulated and you would profit from the market itself. In the second case, the manipulator would have to buy outcome-tokens of the prediction markets at unreasonable high prices and thereby giving you the chance to make money from the prediction market.

Also, a big manipulator would probably not manage to be able to manipulate the the real difficulty of ethereum. Hence, there is no chance on manipulating the oracle input of the experiment.

![](https://ethresear.ch/user_avatar/ethresear.ch/ankit98/48/2336_2.png) ankit98:

> Where do we apply to take part in this experiment?

Currently, we are evaluating the community interest. If the interest is confirmed, we would publish further information on our various public channels.

---

**eburgwedel** (2018-10-07):

I‘d be interested as well.

---

**Obsidjan** (2018-10-23):

Very interested in this. Awaiting further info.

---

**wighawag** (2018-10-30):

Hey [@mkoeppelmann](/u/mkoeppelmann)

We briefly met at web3 summit, I was mentioning the potential use of my game https://tugofwar.io for a futarchy experiment.

It currently run on the testnet but I have been planning to deploy it on the mainnet at some point. It could be a cool opportunity ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

The game is pretty simple and could be a fun example to test futarchy since there is no obvious strategy to win.

To summarize, the game set 2 players against each other.

- They each start with the same number of unit and at each turn they decide how many units they spend.
- The first player submit the hash of its move,
- the second player can simply submit its move,
- the first player then reveal (and submit is next hash at the same time).
- A player win a round when it send more unit than the other on that round. When a player win 3 rounds more than the other, it win the game.
- If one player run out of unit, the other player simply send one unit each turn to win as many round. (this is automatically computed by the smart contract.
- If both player run out of unit, the one with more round won, win the game.
- On a draw, both players get back their deposit.
- Else the winner get the sum of the deposits.

You can see a demo of a game here : https://www.youtube.com/watch?v=_2FYlDFIHVk

And I published a blog post a while ago about it : https://medium.com/@etherplay/our-first-unstoppable-game-tug-of-war-bb69c63a8734

Since the game relies on the secret of only one of the player, the player ( a human or group of human) that play against the futarchy would play first so the futarchy can publicly decide on its next move.

What do you think?

---

**kwikiel** (2019-02-20):

What was the outcome of those futarchy experiments?

---

**mkoeppelmann** (2019-08-16):

I have to apologize for making the initial post and then not following up. We decided to go a slightly different route. Futarchy is basically a concept you could use IF people trade conditional markets. But until today conditional markets basically do not exist in practice. So we want to lay the foundation first by getting real world experience with conditional markets.

You can see a (main-net) demo here: https://twitter.com/koeppelmann/status/1137000297757323270

If you are interested in trying/ trading those markets or you have suggestions around what markets to create please sign up here:

[http://sight.pm](http://sight.pm/)

https://gnosis.us13.list-manage.com/subscribe?u=1a123436baa68728b8cfa3402&id=61f94000b9

If you are more interested in the underlying tech, check out this:

https://github.com/gnosis/conditional-tokens-contracts

---

**Graeme-Code** (2019-08-19):

Hi [@kwikiel](/u/kwikiel), Graeme Barnes here, product manager of Sight, a prediction market we are building from the conditional token standard. If you would like to take part, please go to sight.pm  and tap get early access.

---

**Graeme-Code** (2019-08-19):

Hi [@eburgwedel](/u/eburgwedel). My name is Graeme Barnes, I’m the product manager of Sight, a prediction market  been built off the conditional token standard, if you are keen to take part would you mind signing up via  sight.pm?

---

**Graeme-Code** (2019-08-19):

Hi [@JeffEmmett](/u/jeffemmett), My name is Graeme Barnes, I’m the product manager of Sight, a prediction market built off the conditional token standard. If you are interested in taking part, trying out some beta markets, please use sight.pm and tap on “get early access”.

---

**Meibols** (2019-09-22):

Hi Graeme, my name is David Abad, Blockchain investigator and Civil Engineer. I live in La Linea and have some works in Gibraltar. I’m trying to investigate how Futarchy could be applied to Real Estate Market Prices. Are you working in this kind of investigations with Gnosis-Sight?? Thanks mate!

---

**mrsolgsm** (2021-11-17):

Hi David Abad (Meibols). I have a proposal for you. Can you write me an email at [mr.xtraf@gmail.com](mailto:mr.xtraf@gmail.com) ?

