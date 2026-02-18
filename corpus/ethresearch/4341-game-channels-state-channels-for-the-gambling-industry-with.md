---
source: ethresearch
topic_id: 4341
title: "Game Channels: state channels for the gambling industry with built-in PRNG"
author: davy42
date: "2018-11-22"
category: Layer 2 > State channels
tags: []
url: https://ethresear.ch/t/game-channels-state-channels-for-the-gambling-industry-with-built-in-prng/4341
views: 5126
likes: 3
posts_count: 17
---

# Game Channels: state channels for the gambling industry with built-in PRNG

After very extensive and detailed research in conjunction with BlockProof Tech LLC, so [DAO.Casino](https://dao.casino/) has some exciting news for the Ethereum industry. In what it is terming **Gambling 3.0**, DAO.Casino has found a way to increase interaction speed between DApps’ players, without losing any gas costs or security. The study has successfully shown that the generating of a new block approximately every 15 seconds and every transaction taking an average of six minutes can be reduced. This is because Game Channels will run on top of existing blockchains.

**What was carried out**

Ethererum already offers plenty of opportunities. What DAO.Casino was looking to achieve was to build on that to create what they term as Gambling 3.0, where they are looking to evolve and develop the possibilities within blockchain.

State Channels solve the problem of scalability while increasing the blockchain's speed and efficiency. That’s why they were used as a foundation to build around the needs of the gambling market. Each aspect of the research relied on the aspect of trust and finality within these channels, with other factors such as Provably fair random number generation support and instant verification of randomly generated numbers.

The research, with BlockProof Tech LLC, tested for a two-party game, so the scenario of a casino versus a player. It also tried scenarios for any game that requires the PRNG tool to function, and for payment to be easily obtained and simple to trace back.

There was a detailed coverage of protocols that allow two parties to open a game channel, play a game, close the channel and get rewards, without any risk of counterparty fraud. The dispute resolution mechanism was also looked at, as was the value of a Third Person Observer who can make any necessary Smart Contracts updates.

As a blockchain specialist with an increasing set of followers, DAO.Casino was aware how vital trust and security is, as well as betting flexibility and speed of interaction. That’s why the research tested a player against a casino, the possibility of a random number generation and the likely probability of a winner after each round. Various studies took place concentrating on different parts of the channel. Griefing and Signidice were also carried out.

[![07](https://ethresear.ch/uploads/default/optimized/2X/d/dfcb5a9f72c3f521fee4306d4ed4d943ec8ec9ba_2_683x500.jpeg)071104×808 77.5 KB](https://ethresear.ch/uploads/default/dfcb5a9f72c3f521fee4306d4ed4d943ec8ec9ba)

**What the research showed**

That’s how Game Channels were created, with an enabled Signidice PRNG that uses unique digital signatures. Not only that, there is also a dispute resolution mechanism. The potential use of Game Channels technology is not only for casino games. In very interesting news for the iGaming industry, online gaming may also be able to use it.

Having carried numerous tests, BlockProof Tech LLC who carried out the research, has proven that Game Channels can be run on top of existing blockchains. As a result, the interaction speed between DApps players can be faster than the current Ethereum time of every 15 seconds without losing on the security or flexibility factors. It also significantly reduces any possibility of cheating.

**The research set-up**

Alexander Davydov from the Research Department at DAO.Casino worked alongside Alisa Chernyaeva and Ilya Shirobokov of BlockProof Tech LLC research team.

*“This paper describes* *"Game* *Channels", a novel approach that applies blockchain technology* *to the gambling industry. It is well known that blockchain technology has issues with scalability* , *as well as transaction times. The longer a blockchain becomes, the more problematic these* *issues can become. In the worst case a distinctly user-unfriendly experience results. Many approaches have been tried to mitigate these issues; one of the most promising approaches is that of state channels. This paper describes a modified form of state channels that they refer to as Game Channels. The primary application is to gambling with two participants (dealer/player and player/player).”*

*“The paper describes the algorithms used from a transaction-based approach, in which each game action is associated with an exchange of data, which may be thought of as a message. Great care is taken in rigorous defining these data exchanges, which of course are based on strong cryptographic primitives. The paper also presents a dispute resolution mechanism that can be used to mitigate certain common forms of cheating. The exposition is thorough and lucid. All currently known algorithms that are thought to be unbreakable have undergone years of cryptanalysis, simulation and red-teaming, so more work needs to be done, but my initial impression is that this approach shows significant promise.”*

Mark Reynolds, a Research Scientist from Boston University and a graduated MIT Ph.D. in Computer Science.

**What exactly is Gambling 3.0**

Some industry companies talk about 1.0, and staying away from the digital world, while others refer to 2.0, which means they’re into iGaming but they’re not keen on any further developments. DAO.Casino is looking further ahead. It is introducing an exciting new term for the gambling world. Gambling 3.0 is all about innovation and a desire to use technology to create a greater experience for anyone using DAO.Casino.

The Gambling 3.0 industry is fully regulated by technology. It’s all part of the process of building a decentralized protocol for gambling on Ethereum blockchain that ensures the automation of transactions and facilitates interactions between all the industry participants. Creating new and better opportunities for casino operators, game developers, affiliates and players. That includes the possibility of game developers and casino operators creating games and becoming a casino operator. Therefore, not only is it simpler to get involved, but also easier to earn revenue.

**Conclusion**

The fact Game Channels can be run on top of existing blockchains brings exciting opportunities. It means the interaction speed between DApps players can be faster than the current Ethereum time of every 15 seconds, without losing on the security or flexibility factors. It also means that the potential use of Game Channels technology is not only for casino games. Some types of online gaming may also be able to use it.

**Link to the paper:** [GameChannels.pdf](https://dao.casino/rnd/gamechannels.pdf)

## Replies

**tawarien** (2018-11-22):

Enabling PRNG’s in a StateChannel is very useful.

What I don’t get is how the following Szenario is prevented:

It is unavoidable that one of the two parties has all of the necessary information to calc the Random number before the other one.

What prevents that party to check if this number is beneficial for it or not and if not beneficial just stops participating?

If nothing stops this then it is only usable for games where the party that can compute the random number first does independent of the random number looses more by not revealing then by revealing (independent of the random number) and the other party wins more if the random number is not revealed then when it is revealed.

---

**davy42** (2018-11-22):

If the participant stops playing, another participant can open a dispute. Read more about the dispute resolution process in the paper.

---

**tawarien** (2018-11-22):

Thanks: I missed the Protocol 5 - which explains it:

> Protocol 5 Expiration closer
>
>
> Either party calls the closeByTime(channelId) function. The function
> checks whether or not a dispute was initiated during its execution.
> If yes, the closeByDispute(channelId) function is executed; it interprets
> the channel state in favor of Player, giving them the highest possible
> reward provided in the game logic.
> The channel is closed and removed (see items 6 and 7 for the 3 protocol).

If I interpret this correctly: The Dealer is always the participant that gets to know the Random number first. If the Random number is to his disadvantage and he withholds it, then the player starts a dispute and after it times out the state is interpreted as if the player would have won the highest possible amount (Basically assuming the random number would have been in favor of the player)

---

**davy42** (2018-11-22):

Yes, that’s right. In case, when we know the estimated amount, the player will win the estimated amount (for example in a dice game). If we don’t know the estimated amount, the player will win the highest possible amount.

---

**hkalodner** (2018-11-22):

I’m reading the paper now, but could you summarize the advantages you have over a Fate Channel like commit-reveal scheme

> It allows a reduction in communication complexity in comparison with the commit􏰃-reveal RNG scheme.

That scheme to my understanding requires 3 messages per round:

Setup:

Players A and B onion hash privately generated random seeds N times and commit to the outer hash

Round:

- Player A sends player P their unwrapped hash Ra (32 bytes)
- Player B sends player A their unwrapped hash Rb and a signature over (Ra, Rb) (32 bytes + 65 bytes)
- Player A sends player B their signature over (Ra, Rb) (65 bytes)

This doesn’t seem to add much overhead on top of simple state channels though I could definitely be missing something.

---

**davy42** (2018-11-22):

Yes, you are right. In the article, we meant the “classical” commit-reveal scheme, in which there are more rounds of communication.

If we are talking about the fate channels, we recognize that at the moment the scheme we have developed has no fundamental advantages over them, as well as disadvantages. But we look at it from the point of view of future changes and developments. Unique signatures have the clear algebraic structure such we can move to the more complicated challenges. One of them is the task of developing n-party protocols of random generation (e.g. dfinity’s BLS-based scheme). Opportunities for the development of schemes based on hash functions look more limited.

---

**tomclose** (2018-11-25):

I could have missed something, but it seems like the signidice protocol has the disadvantage that, after the first round, one party (Alice in the paper) can increasingly influence the PRNG that is generated:

- The protocol starts by Alice sending a seed to Bob.
- Bob then generates a pseudo-random number by performing a series of operations on that seed (hashing, signing, hashing the signature etc.).
- Crucially the use of the signature means that Alice can check the operations but can’t predict the outcome of the operations beforehand.
- However, once Alice has done this once with a given seed, she then knows the number that Bob will generate from that seed. If she is free to replay the seed, she can cause Bob to generate that number at any time she chooses.

Is there anything in the protocol that prevents Alice from sending the same seed multiple times?

---

**MaverickChow** (2018-11-25):

1. PRNG is a fancy way of saying it is not random at all. By right, you should aim for CSPRNG.
2. Gambling can be so competitive today, that house edge can go lower than 1%, that you have much higher ROI running a F&B business vs a blockchain-based casino because the barriers to entry is lowered tremendously with blockchain. On the other hand, traditional casinos thrive because there is still plenty of statistically-impaired customers around.

---

**davy42** (2018-11-25):

Alice’s seed and the game-related data are “mixing” with the help of the hash function. Game related data are unique for the each round. This data are predictable, but cannot be changed. Thus Alice needs to find a collision in the chosen hash function if she wants to produce the same message to signing.

---

**davy42** (2018-11-25):

1. We use very similar algorithm to the one of classic CSPRNG design approaches. The classic approach is as follows: you take some block-cipher and run it in counter mode. We use unique signatures to instead block cipher.
2.We are researching technologies for gambling 3.0 and this technology is one of the possible ones.

---

**tomclose** (2018-11-26):

Ok - that makes sense. It might be worth updating section 2.3 to reflect this and make it clear that the random seed is dependent on the current state of the game and is not a value that Alice has freedom to choose.

---

**davy42** (2018-12-13):

Yes, sure, we will update a paper.

---

**lazygorilla** (2018-12-17):

I like that you have included a dispute resolution process there

---

**Hither1** (2019-01-20):

I wonder if the gambling game is disposed to blockchain, why it still needs an operator.

And will this be legalising gambling? will it work for countries with different gaming laws?

can the features of Game Channel be installed to other state channels that may have multiple functions? Thanks a lot.

---

**davy42** (2019-01-23):

Hello!

- In this case, the operator maintains a platform with games. The operator can also be a bankroller and attract users.
- Discussing the decentralized applications from the point of law is difficult. The Legal authorities usually require certification. It is considered to be legal when certification is successful.
- If we talk about the current situation, game channels are not compatible with other solutions on the go. Realizations of the game channels and other solutions are still being developed and improved. They might be compatible in the future.

---

**davy42** (2020-02-27):

[github.com](https://github.com/DaoCasino/Game-Channels-Paper)




  ![image](https://ethresear.ch/uploads/default/optimized/3X/d/7/d7d84585f5fb79a052225f9a2fe92926c1d46aad_2_690x344.png)



###



Contribute to DaoCasino/Game-Channels-Paper development by creating an account on GitHub.

