---
source: ethresearch
topic_id: 2566
title: Making the RANDAO less influenceable using a random 1 bit clock
author: rcconyngham
date: "2018-07-15"
category: Sharding
tags: [random-number-generator]
url: https://ethresear.ch/t/making-the-randao-less-influenceable-using-a-random-1-bit-clock/2566
views: 5068
likes: 2
posts_count: 22
---

# Making the RANDAO less influenceable using a random 1 bit clock

**TL;DR:** A thought experiment on how to make a RANDAO that is less influenceable by single validator by lowering last-contributor influence on the result by adding a “clock” that entropy contributors can’t predict.

The construction presented here lowers the influence of contributors and therefore lowers the incentive to look at the rewards in all shards. However, the current construction has very poor liveness, and I haven’t looked at 51%-attack scenarios.

The main problem with the RANDAO is that there is a “last influencer” of the entropy, who can make a decision to reveal or not reveal. Assume now that we only generate entropy every epoch of K blocks, XORing all the reveals. Then the revealer of the K'th block gets this unfair advantage, whereas all the other revealers have no information how they might influence the entropy (assuming no collusion). This can be fixed if we assume that there is an external random clock that could end an epoch at any point in time: You would not be able to know whether your block is the last one or not, thus making the point moot (or at least reducing the value of skipping a block to influence entropy by 1/K with K being the average length of an epoch).

Here’s an idea how to generate such an arbitrary “epoch end signal” without the generator of the block knowing whether the epoch will end with his block or not: After each block was generated, each validator XORs the last reveal with their own next reveal*. If it is smaller than a cutoff value p_C (that can be chosen arbitrarily to get any desired average epoch length K), then their reveal is a vote to end the epoch. If a certain number, of validators M vote to end the epoch, they can generate a block together (in practice one of them that has all the votes can generate that block) that ends the epoch immediately and makes the XOR of the last epoch reveals the entropy for the next epoch.

Analysis of this scheme: In this scheme, there are two ways to influence the entropy. When revealing a block of which I don’t like the entropy outcome (if the epoch were to end after it), I can decide not to reveal it. However, there was only a 1/K chance of that block becoming the last block anyway, so the expected influence on entropy is 1/K bits.

Secondly, when voting to end an epoch, I can decide not to vote for an entropy outcome I don’t like. This time, I can only influence the vote if there were exactly M voters to begin with (or rather of M-1 of the other possible voters decided to reveal), in all other cases my missing vote will not have any influence on entropy (assuming no collusion, analogous to [[RNG exploitability analysis assuming pure RANDAO-based main chain](https://ethresear.ch/t/rng-exploitability-analysis-assuming-pure-randao-based-main-chain/1825)]).

The probability of getting exactly M votes can be computed using the binomial distribution:

 \displaystyle p_{=M} = \binom{N}{M} p_C^{M} (1-p_C)^{N-M}

where N is the total number of validators.

The probability of getting more than M votes can be approximated using the normal approximation to the binomial distribution:

 \displaystyle p_{\geq M} = 1 - \Phi \left( \frac{M-p_C N}{\sqrt{N p_C (1-p_C)}} \right)

(\Phi is the distribution function of the standard normal distribution). Now assuming that I am a rational validator and I see an entropy outcome that is unfavourable to me. Assuming that I have a positive vote and that the overall vote outcome would be positive, then I can only influence the vote if there are exactly M votes available and not more, i.e.

 \displaystyle p_\text{Voter influence} = \frac{p_{=M}}{p_{\geq M}} .

We can clearly make this smaller than 1, which give each voting validator an expected influence of less than 1 bit on the outcome of the vote.

For tuning the constants, we first need to choose a suitable p_C by balancing between the following two factors:

1. We want p_C large, because then the variance of the binomial distribution N p_C (1-p_C) is large giving less of a chance to influence
2. However, we will need to choose M \text{very}\approx p_C N (more accurate formula below), so with p_C too large the number of votes to be aggregated would become unmanageable.

For a given p_C, and a desired p_{\geq M} = 1/K can be achieved by setting

 \displaystyle M = p_C N + \sqrt{N p_C (1-p_C)} \Phi^{-1} (1-p_C)

Intuitively it makes sense to set p_\text{Voter influence} \approx p_{\geq M} to give block generators and epoch end voters a similar amount of influence on the entropy outcome. As an example, with N=100000 validators, we can use p_C=0.00325 and C = 348 to get  p_\text{Voter influence} \approx p_{\geq M} \approx 0.1. Then the expected influence of single validators on the entropy is reduced to approximately one bit.

* Maybe you want a separate hash onion for this in order not to interfere with the normal block generation and reveal secrets early.

Current problems with this scheme:

1. Liveness: The above assumes all validators are online all of the time. If validators are randomly offline, and this is evenly distributed, this can be incorporated by simply scaling p_C. However, of course this is not how reality works. Here it turns out to be a real weakness to use the binomial distribution as a base for voting. It would be nice if we could find a way to compute the votes were the votes are highly correlated (a kind of “landslide mechanism”). This would both reduce the influence of the single voter and could improve the liveness of the mechanism. But how to construct such a mechanism without it being predictable in any way by the contributor of the block?
2. Collusion: I haven’t made a 51% analysis as in [RANDAO beacon exploitability analysis, round 2] yet.

## Replies

**vbuterin** (2018-07-16):

> After each block was generated, each validator XORs the last reveal with their own next reveal*. If it is smaller than a cutoff value p_C (that can be chosen arbitrarily to get any desired average epoch length K), then their reveal is a vote to end the epoch. If a certain number, of validators M vote to end the epoch…

The way this sounds, if M-1 validators already revealed a value less than p_C, then the Mth validator knows perfectly well that their vote will be the last vote before they publish it, and so they can exert 1 bit of influence by not publishing. Or am I missing something here?

---

**rcconyngham** (2018-07-16):

But he does not know whether there will be exactly M – there may be more.

---

**vbuterin** (2018-07-16):

Ah, I thought the algorithm was that there’s a specific cutoff M and once the total number of end votes reaches M the epoch stops? If that’s not know it works, then when does the epoch end become known?

---

**rcconyngham** (2018-07-16):

Hmm, I think you might be assuming that the votes are accumulated over the epoch? My suggestion is that they would be for every block. So after every block, there is an independent vote on whether the epoch should stop after this block.

So of course any validator would have the choice not to reveal their “vote”, whether or not there are M-1 other votes. However, the probability that this will influence the vote, assuming that the vote should have been positive, is only p_\text{Voter influence}, because there can be many other votes out there that might push it over M. This probability can be pushed arbitrarily close to 0, but that might be impractical for other reasons.

---

**vbuterin** (2018-07-16):

So to be clear, is the protocol as follows?

- Everyone votes simultaneously after block N
- All of these votes can be included in blocks N+1…N+k (we need k>1 because otherwise the proposer of N+1 controls everything)
- Choose the lowest Q such that \sum_{i=1}^Q vote[i] \le \frac{2^{256}}{k} = M (for some M < N), and then take \sum_{i=1}^M vote[i] as the result

If this is the case, I think the problem is that everyone (or at least everyone with vote[i] \le \frac{2^{256}}{k}) benefits from waiting as long as possible to see everyone else’s values and try to learn if they are the final voter, and then deciding whether or not to publish? In equilibrium the deciding power would fall on the proposer of block N+k.

---

**rcconyngham** (2018-07-17):

I don’t quite understand bullet point 3. In your construction, I would reformulate it as follows: If at block N+k a total number of votes \geq M have been accumulated, then block N is the end of the epoch. I think in this construction, it is indeed best to wait for block N+k to cast the vote, if I don’t like the entropy of block N (rational but not honest nodes). Indeed I would look at all the blocks N+1 to N+k-1 to check if I like any of their entropies better than N and can instead vote for that one (which may or may not be unlikely depending on p_C and N).

Now, my suggestion was instead as follows: Instead of having only RANDAO blocks, we have two types of blocks. One is the normal RANDAO block, the other one has \geq M votes and can be produced by any of the voters if they have seen the other at least M-1 votes. After every RANDAO block, a node which has an epoch end vote immediately distributes this through the P2P network. This block type would need a higher weight in the blockchain than the normal RANDAO block to ensure it is included in the chain. If several voters produce the block, there would have to be some mechanism to prioritise, e.g. take the smallest hash to have the highest weight or so.

---

**vbuterin** (2018-07-17):

Does “the other kind of block” require a sufficiently low hash preimage to be revealed to take the vote count from M-1 to M? If so, that’s still a grinding opportunity.

---

**rcconyngham** (2018-07-17):

Yes, it does. The grinding opportunity is absolutely there, however there can be others who will be able to reveal the vote count if it is >M. So the influence that the average validator has when they have an epoch end vote is less than 1 bit.

The current construction is quite impractical due to the binomial distribution of votes. More desirable would be some distribution with a high correlation between the single votes, but without RANDAO (“normal block”) producers being able to predict the vote outcome. I haven’t found such a scheme yet, it is probably impossible if votes are completely independent of each other (because a block producer could just simulate their own pool of hash onions), but it might be possible if hash preimages would have to be combined in some way to produce a valid epoch end vote?

---

**vbuterin** (2018-07-17):

> however there can be others who will be able to reveal the vote count if it is >M

I still don’t see this. Is the idea that the N blocks are published in parallel, so if there are more than exactly M of them, then any subset of those M could theoretically be chosen? But if that’s true, then there are multiple possible epoch-end blocks, and then there would have to be a proposer that chooses which epoch-end block to build on…

---

**rcconyngham** (2018-07-17):

Yes, each of the epoch end voters who has seen \geq M - 1 of the other votes would be able to generate one block, so there would need to be a rule to choose between those blocks (e.g. giving the highest weight to those with lower hashes; even letting the next block producer choose freely would not be much of a problem except that it lets them redistribute awards among voters, but it would not influence the entropy). However, all of these blocks would lead to the same entropy in the entropy pool, as the epoch end signal is only used to decide that the entropy collection stops at this block.

---

**vbuterin** (2018-07-17):

So then what are the epoch end voters actually deciding? Which M-1 other votes they saw if there’s actually more than M-1 of them?

I feel like there’s still a “last chooser” problem here that’s being shifted to another place, and the last chooser still has 1 bit of influence.

---

**vbuterin** (2018-07-17):

I’ll suggest a different protocol. Let me know if this is close to what you were trying to get at.

Step 1: validators V_1 … V_N submit values x_1 … x_N. The protocol stores all of them.

Step 2: each validator V_i submits bits b_{(i,0)} … b_{(i,k)} where k = log(N). Take B_j = floor((\sum_{1 \le i \le N} b_{(i, j)}) \div \frac{N}{2}) (that is, B_j = 1 if the majority of b_{(i,j)} bits is 1, otherwise it is 0).

Step 3: Combine the bits into an index M = \sum_j B_j * 2^j  and return \sum_{i=1}^M V_i as the result.

Every validator V_i has a chance of \frac{1}{N} that M=i and so they will be able to have influence on the result. The probability that any given \sum_i b_{(i,j)} will be exactly at the cutoff, and so one validator will be able to influence it, is on the order of \frac{1}{\sqrt{N}}, so the possibility one validator will be able to influence the result by influencing bits is roughly \frac{log(N)}{\sqrt{N}}. But this comes at the cost that a validator with \approx \frac{1}{\sqrt{N}} of all validator slots will have a guarantee of being able to influence the result, though at higher cost.

---

**rcconyngham** (2018-07-18):

> So then what are the epoch end voters actually deciding? Which M-1 other votes they saw if there’s actually more than M-1 of them?

They are deciding, if there are \geq M of them, to end the epoch at this block and use the current entropy for the next epoch.

The “votes” are predetermined by their hash preimages, But of course, they could decide not to reveal the votes. So you could say, the hash preimage gives them the ability to vote for an epoch end, and if \geq M of them are revealed, the epoch ends. The block producer (or probably rather, the next block producer) decides which of the epoch end vote blocks to include in the block chain (but they can be incentivised to choose a certain one).

By giving high rewards to voters for successful votes, and also maybe adding incentives to reveal unsuccessful votes in the next block, it could be possible to get people to reveal their votes early as well, or they might miss out.

> I’ll suggest a different protocol. Let me know if this is close to what you were trying to get at.

I think your construction would achieve something similar. I assume that the bits b_{(i,j)} will be determined in a way that does not make it possible for validators to pick them freely, so the only choice they really have is to withhold them in some way. [I hope the word “vote” I chose to describe my construction above was not too confusing, as I don’t mean for them to be free votes but rather predetermined by the protocol as much as possible – the only freedom you have would be to withhold them, but the intended honest behaviour is always to reveal them as early as possible]

However, I don’t understand how you would collect the bits on step 2? Is this another sequence of blocks on the blockchain? In the latter case, I think the grinding opportunity is more dominant for later revealers than in my construction, because of the predetermined number of votes.

---

**rcconyngham** (2018-07-18):

I’ll try to go in a bit more detail how my construction works, hopefully this makes it a bit clearer as I guess I kept that very brief in my first post (I also added the possible incentives I sketched earlier which would incentivise validators to publish votes early):

RANDAO reveal: Each validator has committed to a hash onion H^{1024}(x) that predetermines their reveals as in the standard RANDAO construction

Epoch end reveal: In addition, each validator commits to a second hash onion H^{2^{30}}(y) that determines one single reveal for each block height, also verifiable by anyone after it has been revealed.

There are two type of blocks:

1. RANDAO block: are produced based on current entropy, that was determined at the last EPOCH END block, with block reward R. In addition, it can contain m<M epoch end votes. Each epoch end vote gets a reward S and the block producer will get an additional reward mT for including them.
2. EPOCH END block: Contains m\geq M epoch end votes. Leads to the entropy of the immediately preceding RANDAO block to be adopted as the current entropy pool for beacon chain block producers as well as shards, with a reward of U for each epoch end vote and an additional reward mV for the block producer. Counts as P RANDAO blocks for chain length computations (P is larger than 1 but not super large), such that a chain with more epoch end votes usually wins (proper notarising TBD).

After every RANDAO block, each validator XORs the reveal with their current epoch end reveal for this block height. If it is less than p_C, this produces a valid epoch end vote. Epoch end votes should be distributed through the P2P network (the rewards S and U incentivise doing this quickly in order to be either included in a valid epoch end vote and/or in the next RANDAO block if epoch end voting is unsuccessful). Finally, any voter who has seen a total of \geq M epoch end votes (including their own) can produce an EPOCH END block.

The entropy after the EPOCH END block is equal to the XOR of all the RANDAO reveals from the previous EPOCH END block to the current one. So if there are at least M epoch end votes available, there are also many different EPOCH END blocks that can be produced, but all of them end the epoch at the same height and therefore lead to the same entropy. The next RANDAO block producer would be the same for all of them, and she can in fact choose freely among the EPOCH END blocks the one which will be included in the block chain. We can incentivise her to choose the one with the lowest epoch end vote as the block producer if we want to make it more random and less arbitrary who gets the reward.

---

**vbuterin** (2018-07-18):

Aah, I see. The construction is similar, except in your case what’s happening is that after each individual x_i is revealed everyone releases a bit that votes on whether or not that block is the last one.

BTW I agree that allowing validators to choose their bits independently is bad, and we want to just give them a binary choice of “reveal preimage” vs “don’t reveal preimage”.

It does seem like there’s a class of algorithms here that’s worth studying. I wonder if the sqrt(N) barrier is breakable.

---

**vbuterin** (2018-07-19):

Update: yes it is, with a catch.

See Iddo Bentov’s paper on low influence functions:

https://arxiv.org/pdf/1406.5694.pdf

And the paper on TRIBES:



      [cs.cmu.edu](https://www.cs.cmu.edu/~odonnell/boolean-analysis/lecture14.pdf)



    https://www.cs.cmu.edu/~odonnell/boolean-analysis/lecture14.pdf

###



64.36 KB










And my implementations to give concrete numbers for influence:


      ![](https://ethresear.ch/uploads/default/original/2X/b/bad3e5f9ad67c1ddf145107ce7032ac1d7b22563.svg)

      [github.com](https://github.com/ethereum/research/tree/master/randao_analysis/low_influence)





###



Contribute to ethereum/research development by creating an account on GitHub.










The theoretical minimum is O(log(n) / n). However, the catch is this: the “influence” that these functions minimize is the influence that *any specific validator* has on the result; they do not capture the model where an attacker has a large fraction (eg. 1/5) and we are trying to maximize the *expected cost of attack*. In these cases, LIFs may actively make things worse: for example, in TRIBES, any 1 can be flipped to a 0 with a single validator not showing up.

---

**rcconyngham** (2018-07-19):

Very interesting! I think the construction I suggested actually does much worse in terms of collusions, but I haven’t analysed it yet.

TRIBES still seems very interesting and I will try to have a look if it can be used instead of the voting mechanism above. I think it might be able to yield a much more promising construction. But I also fear that the problem that larger groups actually get to increase their influence persists, which would make this scheme unworkable.

---

**rcconyngham** (2018-07-20):

Quick question about this, from my perspective there are three aspects in this model and I just wonder which ones of them would be worth pushing most –

- Getting some sort of information from several nodes at the same time, in what I called the EPOCH END block; So there is not necessarily a last influencer of entropy, but in how far this is true would still need to be analysed. I think this is only possible because only positive bits are collected in my approach. Is it actually worth following this or is it just a crazy idea and blocks created by single validators are the way to go?
- I originally thought of this construction because I did not like the idea of vdfs that much. I’ve become a bit more comfortable with them now though, and Justin brought me the idea that maybe a combination of low influence and vdfs might also be feasible and improve the overall construction
- The big problem is of course how to protect against collusion. That problem will have to be solved in order for the whole construction to be useful. However, how do you feel about single validator influence? I guess it is also worth pushing this down as it would make honest behaviour more stable?

---

**vbuterin** (2018-07-21):

I’m personally somewhat iffy about VDFs as well ![:smile:](https://ethresear.ch/images/emoji/facebook_messenger/smile.png?v=9)![:smile:](https://ethresear.ch/images/emoji/facebook_messenger/smile.png?v=9)

The dependency on a delicate balance between commodity ASICs and attackers doesn’t really sit well with the “be the scalable blockchain that can survive WW3” desideratum.

Though the nice thing about all of these approaches is, I’m pretty sure we can stack most of them together and get the benefits of all together. I know that’s true for plain RANDAO + VDF (+ my GHOST-related work in making the algo more robust to bad randomness in the first place); I imagine it could be true for low-influence functions as well.

---

**rcconyngham** (2018-07-25):

**TL;DR:** Improvement of the above scheme using a variant of the TRIBES low-influence function. Leads to better results on the single validator influence, but the trade off with coalitions can clearly be seen.

One problem with my voting scheme above is the binomial distribution of the number of votes, making it very impractical. I thought the TRIBES function might be a better paradigm, and I think I at least got a practical result in terms of reducing single vote.

**TRIBES**: The TRIBES function for n voters divided into tribes of w consists of dividing the voters into n/w tribes of w voters each. Each tribe computes the AND of all the votes in the tribe, then the votes of all tribes are ORed. The resulting bit is the result of the TRIBES function.

In the case of the block end scheme above, the what we care about is whether a voter who has a positive vote can change the result from 1 to 0 by not submitting their vote. Not submitting a negative vote has no influence. TRIBES actually performs quite poorly in this, as is intuitively clear when you consider that a typical positive vote only has one tribe voting positively and then any of its voter can turn it into a negative one by not submitting their vote.

So instead, I consider the function ITRIBES: In this function each tribe of w members computes the OR of its votes, and then the AND of the votes from all tribes is computed. (This is in fact \neg TRIBES(\neg X).)

**New voting construction:** Using this, we consider this new voting scheme based on ITRIBES with parameters p_C, n, w

Each RANDAO block uniquely determines n voters as well as a split of these voters into n/w tribes of size w. All the n voters then publish their votes if positive (predetermined by the second hash onion above) and any voter who sees a positive vote coalition according to the ITRIBES function can publish an EPOCH END block.

The probability of a positive vote is then

 \displaystyle p_\text{EPOCH END} = (1 - (1 - p_C)^w)^\frac{n}{w}

(assuming all nodes are honest and online)

**Single voter influence:** If a single voter has a positive vote, and the overall vote is positive, then the probability that holding back his vote will make the vote fail is

 \displaystyle p_\text{Influence} = (1 - p) ^ {w - 1}

which is the probability that all other voters in the same tribe have a negative vote.

[The traditional single voter influence on the vote is:  \text{Inf}_1 = (1 - p) ^ {w - 1} (1 - (1 - p_C)^w)^{\frac{n}{w} -1}, but I think p_\text{Influence} is the more important measure]

**Coalition influence:** Now, we can also compute the probability that a coalition of f validators can prevent a positive vote from happening by holding back their votes. Let’s consider tribe one only. Then, assuming that the vote of this tribe is positive, we can compute the probability that the coalition controls all the positive votes as

\displaystyle \theta = \frac{(1 - (1 - f)p)^w - (1 - p)^w}{1 - (1 - p)^w}

Then, if the overall vote is positive, the probability that the coalition controls at least one tribes positive vote is the probability that the total vote is controlled by the coalition:

\displaystyle p_\text{Coalition influence} = 1 - (1 - \theta)^\frac{n}{w}

**Choosing the parameters:** For a given p_\text{EPOCH END} and a number of voters n, we can choose the parameters p_C and w in many different ways. Of particular interest are two sets of parameters:

1. We can optimize for minimal single voter influence p_\text{Influence}. This leads to values for p_C close to 1/2. I call these the “Influence optimised” values.
2. We can optimize for coalition influence. In this case, we want fewer tribes and therefore a smaller p_C, to reduce the chance of the coalition controlling any single tribe. In the extreme this leads to w=n and p_C = p_\text{EPOCH END} / n, which is trivial, but minimises the chance of coalition influence (the probability of controlling a single voter is simply equal to f.

**Results:** Below are some results for p_\text{EPOCH END} = 0.1. I allowed w to be fractional to be able to perform optimisation on p_C while fixing p_\text{EPOCH END}. The “Average” optimisation simply halves the p_C from the Influence optimisation. p_\text{Coal} is the coalition influence for a coalition of size 0.05 of all validators, and “Coalition” refers to the coalition size required in order to get a 50% influence on the outcome of positive votes.

So far this confirms the suspicion that the trade off for reducing the influence of single validators is a (probably unacceptable) increase in the power of larger coalitions.

```
Optimization	n	w	p_C	p_EPOCH	Inf1	p_Inf	p_Coal	Coalition
Influence	20	2.58	0.409	0.100	0.059	0.435	0.221	0.129
Average		20	4.19	0.205	0.100	0.078	0.481	0.153	0.187
Influence	60	3.28	0.479	0.100	0.026	0.227	0.325	0.084
Average		60	5.86	0.239	0.100	0.033	0.265	0.221	0.128
Influence	100	3.63	0.501	0.100	0.017	0.161	0.376	0.071
Average		100	6.73	0.250	0.100	0.022	0.192	0.257	0.109
Influence	140	3.88	0.513	0.100	0.014	0.127	0.409	0.064
Average		140	7.34	0.256	0.100	0.017	0.153	0.281	0.099
Influence	180	4.06	0.520	0.100	0.011	0.106	0.434	0.060
Average		180	7.81	0.260	0.100	0.014	0.129	0.299	0.092
Influence	220	4.21	0.526	0.100	0.010	0.091	0.454	0.057
Average		220	8.19	0.263	0.100	0.012	0.111	0.314	0.087
Influence	260	4.34	0.530	0.100	0.008	0.080	0.470	0.054
Average		260	8.52	0.265	0.100	0.011	0.099	0.327	0.083
Influence	300	4.45	0.533	0.100	0.007	0.072	0.484	0.052
Average		300	8.80	0.267	0.100	0.010	0.089	0.337	0.080
Influence	340	4.55	0.536	0.100	0.007	0.065	0.496	0.051
Average		340	9.05	0.268	0.100	0.009	0.081	0.347	0.078
Influence	380	4.64	0.539	0.100	0.006	0.060	0.506	0.049
Average		380	9.27	0.269	0.100	0.008	0.075	0.355	0.076
Influence	420	4.72	0.541	0.100	0.006	0.056	0.516	0.048
Average		420	9.47	0.270	0.100	0.007	0.069	0.363	0.074
Influence	460	4.79	0.542	0.100	0.005	0.052	0.524	0.047
Average		460	9.65	0.271	0.100	0.007	0.065	0.370	0.072
```


*(1 more replies not shown)*
