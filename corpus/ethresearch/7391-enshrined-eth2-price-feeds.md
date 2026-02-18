---
source: ethresearch
topic_id: 7391
title: Enshrined Eth2 price feeds
author: JustinDrake
date: "2020-05-11"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/enshrined-eth2-price-feeds/7391
views: 17537
likes: 59
posts_count: 26
---

# Enshrined Eth2 price feeds

**TLDR**—We suggest adding to the beacon chain a simple price feed service tracking a small set of key assets. The service allows building fully decentralised oracles that produce a price for every tracked asset at every epoch boundary, i.e. with a granularity of 6.4 minutes.

*Thanks to [@albert](/u/albert), [@benjaminion](/u/benjaminion), [@dankrad](/u/dankrad), [@danrobinson](/u/danrobinson), [@DCinvestor](/u/dcinvestor), [@djrtwo](/u/djrtwo), Eric Conner, Evan Van Ness, [@karl](/u/karl), [@khovratovich](/u/khovratovich), Mehdi Zerouali, [@mkoeppelmann](/u/mkoeppelmann), [@paulhauner](/u/paulhauner), [@protolambda](/u/protolambda), [@Robert](/u/robert), [@ryanseanadams](/u/ryanseanadams), [@sassal](/u/sassal), @scott_lew_is, [@vbuterin](/u/vbuterin) for feedback and discussions ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)*

**Construction**

A `price_data: PriceData` field is added to [BeaconBlockBody](https://github.com/ethereum/eth2.0-specs/blob/6474218fb162424a9c362de7d114e68a24059877/specs/phase0/beacon-chain.md#beaconblockbody) where

```python
PRICES_PER_ASSET = 8

# Type aliases
Price = uint64
AssetPrices = Vector[Price, PRICES_PER_ASSET]

class PriceData(Container):
    # Currencies in the IMF SDR basket
    usd: AssetPrices  # 0.01 USD price denomination
    eur: AssetPrices  # 0.01 EUR price denomination
    cny: AssetPrices  # 0.01 CNY price denomination
    jpy: AssetPrices  # 1.00 JPY price denomination
    gbp: AssetPrices  # 0.01 GBP price denomination
```

From the point of view of Eth2 consensus the `price_data` object is treated similarly to the `graffiti` string. That is, `price_data` can be arbitrary data whose value is ignored by the beacon chain state transition function and fork choice rule.

Honest beacon block proposers must populate best-effort prices for every tracked asset in `PriceData`. The prices must:

- baseline—represent 1 ETH of the tracked asset
- snapshots—be snapshotted at the latest PRICES_PER_ASSET epoch boundaries (ordered increasing by age in the AssetPrices vector)
- denomination—be denominated in the smallest ISO 4217 currency unit (e.g. if 1 ETH is 213.09 USD set to Price(21309))
- rounding—be rounded with half down rounding (e.g. if 1 ETH is 22,732.66 JPY set to Price(22733))
- overflow—be set to Price(2**64 - 1) in case of uint64 overflow
- underflow—be set to Price(0) in case of negative prices

**Example—honest-majority ETH-USD oracle**

One can build an honest-majority ETH-USD oracle with a price at every epoch boundary. Consider a smart contract that takes the median of all prices corresponding to a given epoch boundary (up to `SLOTS_PER_EPOCH * PRICES_PER_ASSET = 256` price points).

If more than half the corresponding beacon blocks are produced by honest validators the median price is secure, i.e. not manipulatable by dishonest validators.

**Basic features**

Below are basic features of the price feed service:

- consensus minimalism—By treating price_data the same as graffiti both the beacon chain state transition function and fork choice rule are minimally impacted.
- subsidised delivery—Every beacon block contains a dedicated PriceData object, bypassing application-layer block space constraints and gas markets.
- raw prices—The price feed is a low-level service that exposes raw price points. Those can be mixed and matched with other price sources to create hybrid oracles with custom logic.
- bandwidth efficiency—Each tracked asset serialises to type_byte_length(uint64) * PRICES_PER_ASSET = 64 bytes for an overhead of 320 bytes per BeaconBlock. The bandwidth overhead for block propagation is marginal, especially with network-level compression.
- public good—The service is an unopinionated public good which can be used by Eth1, Eth2, as well as other blockchains. It can also be used offchain, e.g. by fully decentralised wallets to estimate fiat-denominated gas costs.
- initial deployment—The price feed service is optional Eth2 infrastructure which can be deployed when ready. Eth1’s DeFi ecosystem could benefit from an deployment, e.g. in phase 1.

**Feed governance**

Maintenance of the set of tracked assets is a governance issue for which we suggest the following social norms:

- minimum viability—The set of tracked assets should be kept to a minimum viable, i.e. only include assets important to Ethereum’s long-term health and success. The five initial assets USD, EUR, CNY, JPY, GBP reflect three key principles:

credible neutrality—they are the currencies from the IMF’s special drawing rights (SDR) basket
- high liquidity—they are the fiat currencies most traded with ETH
- broad utility—they are major fiat currencies natural for DeFi (e.g. for decentralised stablecoins to peg against)

**rough consensus**—New assets (such as gold, oil, Bitcoin) could be added to the tracked set through hard forks driven by rough consensus.
**backward compatibility**—Once added assets must not be removed from the tracked set to maintain backward compatibility.

**Operator behaviour**

We discuss the expected behaviour of various types of validator operators:

1. honest operators—By definition honest operators run validators that follow the consensus rules and report correct price data.
2. lazy operators—The laziest behaviour for a lazy operator (e.g. a busy amateur staker) is to run the default validator client settings. As such lazy operators should run validators that report correct price data. (Computational laziness is not a concern since the computational overhead—in bandwidth, CPU time, RAM, disk—is marginal.)
3. rational operators—Rational operators seek to maximise revenue and will consider price data manipulation to maximise Validator Extractable Value (VEV). However, since PriceData objects are both public and cryptographically signed, dishonest validators are identifiable by the social layer. Potential punishments include:

social shaming—Public staking-as-a-service operators (e.g. Coinbase, Binance) that run validators reporting incorrect price data would get socially flagged (e.g. on Twitter, Reddit) and risk losing reputation as well as business from disgruntled customers.
4. social slashing—If a price manipulation attack is attempted, and especially if the attack succeeds or almost succeeds, the community can coordinate a hard fork to slash the balance of dishonest validators. The balance of dishonest validators can be fully slashed (more so than enshrined slashing which by default partially slashes balances).
5. social orphaning—If dishonest price reporting is observed the community could socially orphan block proposals and attestations from dishonest validators to deprive them from rewards and inflict inactivity penalties.

**Validator client guidelines**

Validator clients must be able to query external sources to derive prices at epoch boundaries. Below are client implementation guidelines:

- diversity—several diverse price sources must be queried for robustness, including onchain sources (e.g. Uniswap V2, MakerDAO, Chainlink—see oracles.club) and offchain sources (e.g. Coinbase, CoinMarketCap)
- security—attack vectors arising from querying untrusted APIs must be carefully addressed
- sanitisation—outlier sources must be handled adequately (e.g. with sanity checks and weighted medians)
- customisability—client operators should have the option to easily change the default price derivation logic and customise their price sources
- decorrelation—implementations should strive to maximise decorrelation in the price derivation logic (e.g. across implementations, releases, slots)
- standardisation—over time price derivation best practices must be formalised and standardised

**Guidelines for dApps**

- historical accumulator—Every PriceData object can be authenticated against the historical_roots in the BeaconState. For gas efficiency the SHA256 Merkle witnesses can be efficiently compressed to a SNARK (with optimisations such as plookup).
- risk analysis—The data feeds are provided “as is”. dApps must carefully evaluate price manipulation risk from dishonest validators and make informed security assumptions (e.g. validator honesty assumptions).
- hybrid oracles—dApps should consider combining the enshrined feed service with other price sources available to them. The feed service is a piece of infrastructure designed to increase choice and robustness for the Ethereum ecosystem.

## Replies

**adlerjohn** (2020-05-11):

https://twitter.com/danrobinson/status/1253348955355852800

---

**djrtwo** (2020-05-11):

Although an exciting prospect, I lean a bit against on first read due to the following:

1. Additional component that eth2 clients have to secure and an attack vector on core protocol
2. Clients will provide a default implementation that will be widely known. This might result in a more brittle/attackable oracle than centralized solutions today (e.g. maker)
3. on-chain oracles are getting better and better (e.g. see uniswap v2) so this might not be necessary

(1) is the most concerning imo. You open up a whole host of new layer 1 attacks and a new bounty on hacking validators.

note for (2) you’ve put in an external dependency on running your validator “honestly” this means the protocol takes on counterparty risk in the form of wherever the default client feeds are pulling from (e.g. coinbase, coinmarketcap, etc)

---

**vbuterin** (2020-05-11):

I’m definitely quite opposed!

**First of all this is a fundamental change to the technical properties of what a blockchain is trying to do**. Right now, we have the property that the correctness of a blockchain’s progress can be verified fully programmatically. Validity is a deterministic function, and availability (ie. non-censorship) can be verified by online nodes, and [there are even techniques](https://ethresear.ch/t/timeliness-detectors-and-51-attack-recovery-in-blockchains/6925) for online nodes with low latency to reach consensus on whether or not a blockchain is censoring transactions. This proposal, on the other hand, aims to introduce a property of the chain that cannot be programmatically verified under any assumption even in principle. There’s even possible future worlds where there’s no obvious consensus on what correct value to put in (eg. one of the above countries has a civil war and both sides claim to be maintaining the “real” USD/CNY/JPY).

**Second, it relies on honest majority, but so much of what we are trying to do with eth2 is fundamentally about moving away from the honest majority assumption** and trying to create “second lines of defense” in case honest majority fails. For instance:

- Proof of custody, trying to change the security assumption on aggregation from “must be honest” to also covering not-evil-but-lazy actors.
- Data availability proofs and fraud proofs, allowing for 51% attack chains that push invalid or unavailable blocks to be rejected
- The fact that users can run full nodes and not just light nodes generally
- The censorship detection technique linked above
- The inactivity leak mechanism and its use for recovering from >1/3 offline attacks

Making a critical functionality that depends on honest majority goes in the opposite direction of all of these advancements.

Third, **it compromises protocol neutrality and opens a slippery slope toward further compromises of neutrality**. This proposal (1) elevates “defi” as a privileged application class, and (ii) elevates a particular set of assets / price indices. Demand for more assets will inevitably appear, and eventually demand for oracles for things other than prices. It also opens base-layer governance to political risk; base-layer governance will have to judge (i) which currencies are “sufficiently important”, (ii) which application classes are sufficiently important, (iii) how to adjudicate emergencies…

Fourth, **it closes the door to innovation in oracle designs**, eg. one natural alternative to this design is that the price at time T should only be agreed upon at time T + 1 day, to give room for on-chain attacks, situations where exchanges stop working for an extended duration, and situations where ordinarily functional APIs give unexpectedly wrong answers… there’s a lot of ways to design an oracle, and it doesn’t seem right for L1 to dominate the ecosystem with one approach.

Fifth, **it increases the risk of staking validator centralization**, as clients will require more automatic updates to maintain their oracles, increasing the risk that validators will just blindly follow instructions from client developers (or that people will give up outright and switch to pools).

Sixth, **it doesn’t actually offer much more security compared to application-layer token-based oracles (eg. Augur and the like)**. The MKR market cap is ~2 million ETH, so application-layer tokens can clearly get significant market caps. We expect initial staking ETH to also… be in the ~2 million range (maybe ~10 million longer term). So it’s definitely not the case that base-layer oracles are in a fundamentally much higher security class than application-layer oracles that become sufficiently popular; seems more like a single order of magnitude difference at best.

**I actually think that we should be moving in the opposite direction, explicitly limiting and circumscribing the function of the base layer, so as to deliberately leave space for the application-layer ecosystem to come up with these other tools**. Augur has been functioning well as an oracle, and other designs (UMA, MKR, Chainlink…) exist.

**The Ethereum ecosystem benefits from having a strong application-layer token ecosystem, as opposed to a L1/ETH monopoly on all important functions**. This is because the Ethereum ecosystem has a large need for public goods, and there is a limited supply of ETH ready to provide those public goods (the ~590k ETH in the EF plus some whales), and it is politically difficult (for good reasons) to modify the Ethereum protocol to print more ETH for these purposes. However, application-layer tokens *can* provide these public goods; eg. Gnosis has done a lot in smart contract wallets and now maintaining openethereum already, etc etc. Application-layer tokens can even directly bake in quadratic funding to fund public goods. So we should be deliberately seeking and engineering for symbiosis with such application-layer tokens, not seeing them as just an experimentation ground where the base layer sucks up anything truly important that they develop.

---

**ameensol** (2020-05-11):

I think V left out the point of *scope creep*. Every minute spent thinking / talking about this proposal is a minute that could have been spent getting PoS / Sharding shipped faster. As someone building a stablecoin protocol I am reasonably confident centralized oracles like Coinbase, oracle platforms like Chainlink (which allow medianizing), and DEXs with moving averages will fill this gap.

This is how we’re thinking about it for Reflexer / MetaCoin:



    ![](https://ethresear.ch/user_avatar/ethresear.ch/sionescu/48/4752_2.png)
    [MetaCoin Governance Minimized Oracle](https://ethresear.ch/t/metacoin-governance-minimized-oracle/7293) [Applications](/c/applications/18)



> Although this scheme is meant to be used primarily in  MetaCoin  (pegged-coin system) and  Reflexer  (reflex-bond system), it can be applied to any DeFi protocol.
> General Mechanism
> In order to have a resilient price feed and at the same time minimize governance’s power over oracles, I propose the following on-chain oracle network medianizer:
>
>
> A contract keeps track of whitelisted oracle networks it can call in order to request collateral prices for the pegged-coin/reflex-bond system. The cont…

---

**vbuterin** (2020-05-11):

> Every minute spent thinking / talking about this proposal is a minute that could have been spent getting PoS / Sharding shipped faster.

FWIW I don’t actually think Justin and myself retiring tomorrow would slow down eth2 deployment by much at this point. My recent comments weren’t just self-congratulatory marketing; it truly is a matter of coordination, implementation, testing and deployment in the hands of the devs and it has been that way for all of this year. Research should be focused on the lower half of [the roadmap](https://twitter.com/VitalikButerin/status/1240365047421054976) and being on-call for iteration; this post is a totally fine direction to come up with a proposal in.

---

**phil** (2020-05-11):

Agree that deciding parameters / assets / etc is a governance nightmare that invites pretty much every kind of imaginable capture.  IMO it’s bad enough that this will be happening on the application layer, potentially opening up incentives to bribe/corrupt L1. In the consensus protocol the drama will find a more effective path to derail the system.  I’d posit that Hudson’s hair is grey enough as it is.

---

**danrobinson** (2020-05-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/djrtwo/48/12_2.png) djrtwo:

> on-chain oracles are getting better and better (e.g. see uniswap v2) so this might not be necessary

Uniswap v2 will only give you a price feed for ERC-20s; it won’t help with feeds for these currencies.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Right now, we have the property that the correctness of a blockchain’s progress can be verified fully programmatically.

I would say this is most analogous to timestamps, which can’t be verified programmatically and depend on subjective facts about when messages were propagated to the network. Similar (despite the mitigations you mention) with censorship, PoS forks, data availability attacks…

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The Ethereum ecosystem benefits from having a strong application-layer token ecosystem, as opposed to a L1/ETH monopoly on all important functions .

The benefit of having this in the base layer is developer confidence that their contracts can rely on it existing forever. Oracles are one of the few intractable sticking points that force a project to include some upgradeability or governance.

On the flip side, I do admit that the social commitment for validators to operate this oracle forever is quite daunting and maybe a dealbreaker.

---

**vbuterin** (2020-05-11):

> I would say this is most analogous to timestamps, which can’t be verified programmatically and depend on subjective facts about when messages were propagated to the network. Similar (despite the mitigations you mention) with censorship, PoS forks, data availability attacks…

True though clients *do* verify timestamps in one direction (they reject future timestamps) and the “timestamps must monotonically increase” rule effectively means that assuming even one honest timekeeper the timestamp staying close to the real time reduces to the censorship prevention problem.

---

**DennisPeterson** (2020-05-11):

Social shaming works equally well for any price feed implemented on a smart contract. In fact, it could work *better* since a contract could require some kind of real-world verified identity, which we probably don’t want to require of validators.

Social slashing could also be done on a smart contract. Just fork the chain and make a state change, like in 2016. It does seem like a terrible idea to do all that just to keep a contract’s price feed correct, but I’m not sure I could come up with a reason why it’s any better just because the “contract” is embedded in the L1 protocol. Seems like you could do just as well with a well-known contract, where price reporters post bonds and the contract can apply a stake vote to slash them.

Even social orphaning could work. There could be a social norm to ignore validators that report dishonest prices to some well-known contract. But this would be contrary to the social norm of anti-censorship, without much benefit since a relatively small bond could expose reporters to an equal penalty.

These last two aren’t likely to motivate impressive accuracy, since validators only have to be accurate enough to avoid getting nuked by the community.

Ultimately, all these measures seem fairly crude compared to what’s already being done in the application layer. And since it’s entirely possible that some application will come up with a better price feed (by better accuracy or by pricing many more assets in one convenient place), developers couldn’t actually have confidence that the social measures enforcing the built-in feed wouldn’t ultimately be abandoned.

---

**AFDudley** (2020-05-11):

This idea is a nightmare, nuke it from orbit. A better idea is a means of moving contract code into the native client, via WASM or something. That’s a general solution that would provide an upgrade path to this sort of functionality if some collective of client devs are convinced price feeds should be first class.

I strongly agree we should have a way of making new functionality first class, but a one-off solution for oracles will cause huge problems in short order.

---

**ameensol** (2020-05-11):

“Justin and myself”

> Thanks to @albert, @benjaminion, @dankrad, @danrobinson, @DCinvestor, @djrtwo, Eric Conner, Evan Van Ness, @karl, @khovratovich, Mehdi Zerouali, @mkoeppelmann, paulhauner, protolambda, Robert, ryanseanadams, sassal, scott_lew_is, vbuterin for feedback and discussions

I suppose it’s fine to research in whatever direction but this is also just the worst idea and the last thing I want from Ethereum (L1), and so it’s the last thing I want soaking up brainspace of protocol devs. Justin could build this as a dapp or a set of ERC standards. I am firmly opposed to the ETH staker set being hijacked to compete with Chainlink.

---

**kaiynne** (2020-05-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/danrobinson/48/755_2.png) danrobinson:

> The benefit of having this in the base layer is developer confidence that their contracts can rely on it existing forever. Oracles are one of the few intractable sticking points that force a project to include some upgradeability or governance.

While I agree there is some benefit to the idea of having some certainty of access to the specific set of data available at the time a contract is deployed, this benefit will inevitably erode over time as new data is required by users or the originally deployed contract will become less useful as new prices are added yo L1 that the contract does not know about. So I really don’t see how even if we ignore all of the other arguments against this, that the proposal reduces the need for ongoing governance in any meaningful sense. Even more importantly I feel like the premise that oracles are the main requirement for governance is inaccurate, there are many other things that require governance, and this is likely to only increase as the complexity of contract suites increase. Putting effort into safer upgrade patterns feels like it would be far more useful than trying to solve this by embedding oracles in L1.

---

**JustinDrake** (2020-05-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Right now, we have the property that the correctness of a blockchain’s progress can be verified fully programmatically.

Is that true?

1. As pointed out by Dan Robinson, the timestamp in Eth1 is not fully verifiable programmatically. Time is something external, inherently subjective, manipulable on the margin, but generally blockchains have done a pretty good job maintaining it. Why can’t a similar success story be replicated for price?
2. The per-block Eth1Data in Eth2 is also not fully verifiable. A malicious proposer could put data in their Eth1Data which is not fully verifiable programmatically. In fact, you can think of the Eth1Data voting gadget (see process_eth1_data) as essentially an Eth1 oracle. The enshrined Eth1 oracle is not too far from the enshrined price oracles in the proposal.

More philosophically, why should this L1 purity test trump delivering utility for the L2 ecosystem?

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> it relies on honest majority

I don’t think this is true. More specifically, while honest majority is *sufficient* I don’t see it as *necessary*. The example in the proposal was just that—an example. Consider the following scenario: 1/3 of the validators are honest (say, enthusiast stakers and the EF), 1/3 of the validators are rational (say, Coinbase and Binance), and 1/3 of the validators are actively malicious (say, they always put garbage price data).

As I argued above, the public staking-as-a-service providers are incentivised to put correct price data because otherwise they risk 1) losing reputation, 2) losing customers, 3) legal action. In the above scenario I expect 2/3 of the validators to populate correct price data despite no validator honest majority.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> (1) elevates “defi” as a privileged application class

1. One of the main motivations for fully decentralised oracles is fully decentralised stablecoins. Are you arguing that the importance of stablecoins is limited to DeFi? I’d argue that stablecoins are basic public goods that are broadly fundamental to the Ethereum ecosystem.
2. Finance applications are “eating” Ethereum. The majority of use cases and innovation today is finance-driven. In other words, finance applications are already “socially elevated” and “socially privileged”. The price oracle proposal embraces that reality.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> elevates a particular set of assets / price indices

One could argue this the other way round, i.e. that Ethereum would be *more* neutral by enshrining key assets. Indeed, Ethereum does not live in a vacuum and enshrined key assets would reflect realities external to L1. Take for example the USD. It is the world reserve currency. It also dominates Ethereum’s activity today:

1. The top gas burned, by far, is for Tether USD.
2. DAI is denominated in USD and Maker has a dominance of 52% in terms of Total Value Locked.

L1 Ethereum not appropriately “elevating” USD could be argued as an unnatural bias which goes against the realities of the L2 ecosystem.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> it closes the door to innovation in oracle designs

Why? Ethereum is fundamentally permissionless. (Metaphorically speaking, where is the “door”?) Are you worried enshrined oracles would crush all competition? If so, consider that the data feed is limited in several ways:

1. The set of enshrined assets is a tiny “minimum viable” fraction of assets. There’s no way this can compete with oracles like Augur or Chainlink that can support thousands of assets.
2. The granularity is fixed to 6.4 minutes. I don’t see slot-level granularity as possible for the beacon chain, for various reasons including bandwidth overhead.
3. The design is one of many other possible designs. Why would this particular design be the end be all of oracles? There are clearly many tradeoffs to be explored in the design space.
4. The enshrined price feeds are just one of many sources can that be plugged into a hybrid oracle design. I see hybrids (as opposed to a L1/ETH monopoly) as the natural way forward for price oracles.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> it doesn’t actually offer much more security […] a single order of magnitude difference at best

Are you arguing that an order of magnitude more security is not a massive improvement? I’d argue that if we can produce an order of magnitude security improvement that should seriously explored ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Augur has been functioning well as an oracle

As much as we all love Augur, as far as I can tell there’s been no significant adoption or stress-testing of Augur in the context of a price oracle for stablecoins. Are you arguing that MKR should use Augur and call it a day? I expect the MKR team has considered Augur, yet decided that an oracle run by 14 opaque trusted entities is superior to Augur for their use case.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The Ethereum ecosystem benefits from having a strong application-layer token ecosystem

We agree on that ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) If the foundations are shaky then the application-layer token ecosystem is weak from a security standpoint. Consider for example an attack on the MKR oracles today. That would have rippling effects to the various tokens and services that use and build upon DAI.

Now consider a future (say in 10 years) where there’s a multi-trillion DeFi ecosystem which is attacked at its foundations. The rippling effect could go beyond L2 and affect ETH and the integrity of Ethereum’s L1. Again, Ethereum L1 does not live in a vacuum. If the realities of L2 impose systemic risk to L1 (in a similar way that the realities of The DAO imposed systemic risk to L1) that is arguably the L1’s problem also.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> the Ethereum ecosystem has a large need for public goods

We also agree on that ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) Having said that, I don’t see public goods funding and enshrined price oracles as mutually exclusive. DeFi has a trust issue at its foundations with the lack of robust fully decentralised oracles. That is limiting scalability and growth for DeFi.

My gut feel is that Ethereum is missing out on significant potential. Tether dominates the stablecoin scene despite the potential for Ethereum to produce a stablecoin 10x better than Tether. I believe a successful decentralised stablecoin would foster a significantly more vibrant Ethereum ecosystem, itself leading to more public goods funding.

---

**alonmuroch** (2020-05-12):

Why is that piece of information more valuable than others and requires protocol level consideration?

Also, will we start having listing procedures on the beacon-chain? Like exchanges do?

---

**edmundedgar** (2020-05-13):

I don’t particularly like this idea for the reasons everyone else has stated but if you *were* going to put a reference external-world information in the core protocol of Ethereum (or more realistically some other system you might build), a better way to do it might just be to point at a generalized claim like “this list of contracts are honest judges”.

If you’ve got a basic trust root like that, you can then use that to support price feeds (“hey honest contract whitelisted by the protocol, tell me what price feeds are good”) and all kinds of other information, without needing the protocol to have an opinion about what use-cases are important.

You can then use an escalation game to make the decisions handled by the list of honest judges very small (potentially zero, just working as a game-theoretical backstop) to reduce the set of decisions that need to be made at protocol level to questions like “did somebody break Kleros?”

---

**vbuterin** (2020-05-13):

> As pointed out by Dan Robinson, the timestamp in Eth1 is not fully verifiable programmatically.

1. It’s verifiable in one direction (clients reject blocks with timestamps that are too high)
2. As long as there is at least one honest miner getting included, the timestamp keeps getting pushed close to the limit

These two facts together basically mean that timestamp integrity is guaranteed up to censorship resistance.

> The per-block Eth1Data in Eth2 is also not fully verifiable

Yes but I am fine with eth1data only because it is a temporary measure that exists during a particular phase of protocol transition that is heavily managed anyway. I would never support something like eth1data as a permanent feature.

> More philosophically, why should this L1 purity test trump delivering utility for the L2 ecosystem?

Because lots of platforms are going for utility and purity is one of the few things that ethereum-like blockchains have going for them?

> ```
>  I don’t think this is true. More specifically, while honest majority is sufficient I don’t see it as necessary.
> ```

By “honest” I mean “motivated by extra-protocol factors”; so being off-chain reputationally motivated is a subset of honesty. And we have decided that this is insufficient in the proof of custody case…

> In other words, finance applications are already “socially elevated” and “socially privileged”. The price oracle proposal embraces that reality.

Embraces, or entrenches? I worry it’s more the latter.

> L1 Ethereum not appropriately “elevating” USD could be argued as an unnatural bias which goes against the realities of the L2 ecosystem.

That would be true if L1 ethereum elevates other application classes! But so far it doesn’t.

> Are you worried enshrined oracles would crush all competition? If so, consider that the data feed is limited in several ways:

I’m worried that we’ll see one of two things happen:

1. Enshrined oracles would suck up enough of the usage to heavily demotivate competition, and so they would “crush” it.
2. Enshrined oracles would see some usage, but there will also be room for off-chain usage, and at that point we’ll be in an awkward situation where L1 mechanisms and L2 mechanisms are competing with each other. (It’s awkward because we are burdened with both the risks of maintaining the L1 thing and the risks associated with the L2s breaking)

> Are you arguing that an order of magnitude more security is not a massive improvement?

I did say “at best”; most likely it’s even less.

> As much as we all love Augur, as far as I can tell there’s been no significant adoption or stress-testing of Augur in the context of a price oracle for stablecoins. Are you arguing that MKR should use Augur and call it a day? I expect the MKR team has considered Augur, yet decided that an oracle run by 14 opaque trusted entities is superior to Augur for their use case.

MKR not using augur directly makes sense; crypto projects having external dependencies to other crypto projects has its own risks that are best avoided. That said, there’s other stablecoins that are actively considering Augur-like oracles; UMA is one of them.

> Also, will we start having listing procedures on the beacon-chain? Like exchanges do?

This is one of the things that worries me ![:smiley:](https://ethresear.ch/images/emoji/facebook_messenger/smiley.png?v=12)

> a better way to do it might just be to point at a generalized claim like “this list of contracts are honest judges”.

My main worry with general-purpose oracles is that we still haven’t seen a really good explanation of what happens in edge cases, and if there is a specific path to take in an edge case how to deal with the meta-edge case of determining whether or not a case that leans on one side to count as “edgy” enough. Enshrining those at L1 could lead to the chain forking over controversial meatspace questions.

---

**Recmo** (2020-05-14):

A design broadly similar to this has been discussed as part of a 0x decentralized L2 chain. The L2 validators would do essentially what is described here. We mostly rejected the design for reasons not mentioned here yet:

Here’s how I look at security: For any non-tautological guarantee the system provides, there is a cost of attack. i.e. cryptography is impossibly high, consensus logic is bounded by staking pool / mining reward / etc. The security margin is the difference with the economic opportunity exploitable with the attack.

The attack cost of this oracle design is very hard to analyse, because it depends on whatever the clients choose as their source of truth. It’s reasonable to assume a majority will run the default setup or similar (there are not a lot of options on how to implement this), which in the best case uses a mix of maybe up to five exchange price feeds. Now the attack cost is the minimum over the attack surface. In this case the attack surface is very large, from consensus to the source oracles themselves. One of the cheaper elements likely being an outright DOS attack on all the default sources. This can still be good enough for some use-cases, but putting it in L1 gives the illusion that the guarantee is stronger than it really is.

Compare this with an AMM based oracle like UniswapV2 integrated over sufficient time. Now the ‘attack’ cost is a function of liquidity depth over time, very costly to manipulate and somewhat quantifiable. (And I put it in ‘quotes’ because during this time, you can actually exchange at the oracle price, so in a sense the manipulated price is real). Only works for onchain assets, but it shows that alternative solutions exists and it’s probably best for L1 not to be opinionated.

We may revisit this design in for our L2 validators, but I think that is where such solutions belong, in application specific contracts/L2’s and not in L1.

> this is most analogous to timestamps

Here the lower bound (monotonicity) is guaranteed by consensus rules, and the upper bound by local time oracles in each validator. It’s hard to but a value on the attack-cost of the latter, but at least it doesn’t depend on a handful of central servers. (Let’s hope not, I haven’t looked into NTP too deeply)

---

**JustinDrake** (2020-05-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/djrtwo/48/12_2.png) djrtwo:

> Additional component that eth2 clients have to secure and an attack vector on core protocol […] is the most concerning imo

Right, it’s an additional component to secure. Having said that I don’t see the additional work as insurmountable. Security is (or at least should be) part of the DNA of any Eth2 client team. Eth2 clients are by design pieces of security-critical software. Calling untrusted Web2 web APIs shouldn’t be a deal breaker—that’s standard stuff.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> purity is one of the few things that ethereum-like blockchains have going for them

If we consider Ethereum’s purity from a holistic standpoint (i.e. L1 and L2 combined) then enshrined oracles feel like a net purity win. The reason is that enshrined oracles would unlock an ecosystem of “pure” dApps (à la Uniswap and Gnosis) at L2.

Right now there’s significant friction to building pure dApps. For DeFi, that’s in large part because Ethereum is not “purely aware” of its own price. I feel we risk the purity of DeFi if everyone is building on an “impure” Maker. Enshrined oracles tradeoff a limited amount of L1 impurity for a potentially much larger amount of purity at L2.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Embraces, or entrenches? I worry it’s more the latter.

This is a tough political/philosophical/social question ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) To me it’s embracing but maybe I’m thinking too narrowly or too short term ![:man_shrugging:](https://ethresear.ch/images/emoji/facebook_messenger/man_shrugging.png?v=12)

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> crypto projects having external dependencies to other crypto projects has its own risks that are best avoided

Exactly! ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) And I see this as a strong argument for enshrined price oracles. The reason is that there are network effects for stablecoins—it’s been winner-take-most for DAI so far. Any project that wants to build on the dominant stablecoin now has to accept a not-fully-decentralised external dependency. The users of a dozen or so DeFi projects (I am no DeFi expert but things like Compound, Synthetix, Set Protocol, Dharma that may use DAI) have to pay the risks of external dependencies when all they wanted was access to a public good stablecoin.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> I did say “at best”; most likely it’s even less.

I’d say it’s “at least” an order of magnitude ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) A $2B MKR is not necessarily 10x less secure than a $20B Eth2. Part of the reason is coin distribution. The decentralised and robustness of ETH hodler base is hard to match for a token.

![](https://ethresear.ch/user_avatar/ethresear.ch/recmo/48/3666_2.png) Recmo:

> One of the cheaper elements likely being an outright DOS attack on all the default sources.

DOS attacks are an interesting point. Having said that, Ethereum is itself somewhat hard to DOS and I do advocate (see “diversity” under “Validator client guidelines”) for the default settings to query onchain sources with strong liveness in addition to the fully-centralised APIs.

![](https://ethresear.ch/user_avatar/ethresear.ch/recmo/48/3666_2.png) Recmo:

> Compare this with an AMM based oracle like UniswapV2 integrated over sufficient time.

As was noted by [@Robert](/u/robert) and [@danrobinson](/u/danrobinson) an AMM based oracle like UniswapV2 does not really solve the oracle problem for USD—UniswapV2 solves the oracle problem for ERC20s like DAI, USDC, USDT, etc.

---

**Robert** (2020-05-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> Exactly!  And I see this as a strong argument for enshrined price oracles.

Fully agree! The big advantage of an enshrined oracle is that it potentially offers stronger immutability guarantees than any dApp that is collecting external ETH:USD price data.

If an oracle deployed to address A is replaced by a new oracle version at address B and stops getting price updates, it will break all immutable dApps that are relying on its data.

---

**Recmo** (2020-05-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> Recmo:
>
>
> Compare this with an AMM based oracle like UniswapV2 integrated over sufficient time.

As was noted by [@Robert](/u/robert) and [@danrobinson](/u/danrobinson) an AMM based oracle like UniswapV2 does not really solve the oracle problem for USD—UniswapV2 solves the oracle problem for ERC20s like DAI, USDC, USDT, etc.

My point was not to bring up AMMs as a solution (they aren’t) but to suggest how broad the solution space could be without having a clear winner. IMHO, if there is a large solution space and there is no obvious good-enough-for-everyone solution, it’s best for a low level of the stack to stay agnostic and let higher levels (contracts/dapps/L2s) decide what is appropriate for their use case.

Since we seem to be concerned primarily with fiat price oracle and my example doesn’t work for that, I’ll offer an alternative to make my point (but please don’t attack the solution, it’s purpose is only to indicate the non-trivial extend of the solution space): Maintain a list of credible sources and have validators relay authenticated messages from them. This could be straight-up signed messages like in the case of Coinbase’s friendly new oracles, on-chain state for on-chain sources, or recorded authenticated HTTPS transmissions. The consensus rules would verify authenticity. Happy to discuss the pros and cons of this approach, but, again, that is not really the point. More alternatives have also been brought up by others above (trusted council like MKR, prediction markets).

I’m just wondering why the proposed solution in particular is being singled out for beacon-chain-consensus status when the solution space seems to me an active area of innovation with no clear winner. It’s also not entirely clear to me what we gain by promoting it to the consensus layer, though I see a lot of the drawbacks articulated by others above.


*(5 more replies not shown)*
