---
source: magicians
topic_id: 3018
title: Is ASIC-resistance good for Ethereum?
author: elliot_olds
date: "2019-03-27"
category: Uncategorized
tags: [progpow]
url: https://ethereum-magicians.org/t/is-asic-resistance-good-for-ethereum/3018
views: 2620
likes: 9
posts_count: 4
---

# Is ASIC-resistance good for Ethereum?

There has been some discussion in [this thread](https://ethereum-magicians.org/t/governance-concerns-after-listening-to-all-progpow-discussions-on-core-dev-calls) and in the ProgPow-review gitter channel about whether ASIC-resistance is a goal that Ethereum should be striving for.

I thought it might be good to have a more permanent record of these discussions, in a thread that was exclusively devoted to them.

The main arguments in favor of ASICs are:

**(1) GPU mined coins are cheaper to attack with rented hashpower**

It’s easier to rent a large amount of GPU power than it is to rent a large amount of ASIC power, because the market for rentable GPUs encompasses non-cryptocurrency uses (for instance, machine learning). Amazon and other cloud providers have lots of GPUs for rent which people routinely use for non-mining things. So if you want to do a hashpower rental attack, you’ll be able to rent a higher % of the total hashpower needed if you’re attacking a GPU-mined coin.

Why does this matter? Because as [described here](https://www.youtube.com/watch?v=N6eDuEEb0Oc&feature=youtu.be&t=458) by Joseph Bonneau, rental attacks are much cheaper than attacks in which you buy or build out the mining capacity used for the attack. The difference is huge – about three orders of magnitude (millions of USD vs. billions). This video is extremely important to understand to get the context of these arguments.

The main objections to this are that the Ethereum GPU mining network is so large that it’s impossible to rent enough GPUs to get 51% of the total hashrate.

It’s unclear how much GPU hash power could really be rented, because a lot of claims that this wouldn’t work are based on Amazon being unwilling to rent a large portion of its capacity to a random attacker, or based on other cloud providers being unwilling to rent their GPUs to miners because miners are too hard on their equipment.

To the extent that barriers to renting GPU hashpower are social, it’s unclear whether just offering to pay 2x the market rate, or playing a long game where the attacker first builds a positive relationship with the rental service can bypass these issues.

The thing that it’s important to stress here is that a build/buy attack is so much more expensive than a rental attack that an attacker wanting to rent GPUs can throw around a lot of money (hundreds of millions of USD) to get the rental to work out and still create the attack for much cheaper than if they bought/built the capacity. As a general rule if you’re willing to spend many millions of dollars you can usually get special favors and pretty good customer service.

To the extent that there just aren’t enough GPUs available to make a purely rental based 51% attack possible even if everyone involves was perfectly willing to cooperate, this should reduce our concern about these attacks.

However it shouldn’t eliminate these concerns because any amount of hashpower that can be rented serves to reduce the overall cost of the attack. If an attacker can only rent 1/3 of the necessary hashpower for an attack and needs to buy out mining farms to get the other 2/3, they’ve still reduced their attack cost by almost 1/3 by renting.

**(2) The risks from ASICs are small**

People really don’t like big ASIC manufacturers and ASIC farms, but if we look at the economics and game theory of mining it’s not clear that ASICs post much of a threat.

The main idea is that if a big ASIC manufacturer did want to attack/censor the network, their cost would be in the billions of dollars because Ethereum would likely switch PoW algorithms, making the ASIC manufacturer’s hardware worthless. It’s essentially equivalent to the ASIC manufacturer doing a “build attack” on the network, with the same huge costs.

Worries about ASIC manufacturers usually depend on the idea that once they took over the network and started doing bad things, that they would continue to control the network for a significant period of time.

This doesn’t seem plausible, because I think there would be almost unanimous community agreement to fork away from the attacker ASAP when the alternative is to live under censorship and double spending attacks / long rollbacks indefinitely. Changing PoW is a hassle but far better than accepting that Ethereum will be a censored network from now on.

Concerns about this situation often assume that the ASIC miners would have some power to stop the community from changing to a different PoW algorithm, and could somehow use their haspower to make this switch difficult, but I’m not aware of any actual mechanism by which they could exert any such power. Their ASICs won’t help them at all when the network switches to a new PoW.

If these ASIC manufacturers had been mining honestly for a while before their attack, then it’s true that they would probably have a lot of money. So if they were spiteful they could buy up or rent a bunch of general purpose hardware after the PoW change and attack the network. It seems unlikely that a company big enough to have so much economic power would engage in an act that would bring such bad PR while causing them to lose so much additional money. This would have huge costs to such a company and no apparent benefits.

Another risk from big ASIC manufacturers is that they might place a bet on Ethereum failing or its price falling significantly, and then attack the network in order to profit from their bet. This is possible, but the same opportunity is available to anyone with a lot of money: they could buy some mining farms and make the same bet. To the extent that GPU mined coins are cheaper to do rental attacks on, GPU mined coins are actually more vulnerable to this sort of thing. This would only be an argument against ASICs if we thought that ASIC miners were more likely than any other rich entity to try this.

**(3) Ethereum should try to be more resistant to state-sponsored attacks, all else being equal**

An argument that I often see is that hash rental attacks won’t be profitable, so we shouldn’t worry about them. I believe that there is a real risk from states trying to disrupt Ethereum. These entities would not be aiming for a profit. The difference between an attacker with a destructive goal needing to spend a few billion dollars vs. tens of millions to disrupt Ethereum, or even 2 billion vs. 3 billion seems like something we should care about.

**(4) We don’t know if our current security level is adequate, so if there are no significant tradeoffs we should prefer higher security levels**

I’ve heard arguments that since Ethereum has been GPU mined for a while and that we haven’t seen it attacked yet, the status quo is just fine. I see a few problems with this:

(a.) When you’re dealing with probabilistic risks, just because you haven’t seen something bad happen yet doesn’t mean that the risk level is acceptable. If the probability of nuclear war has been 1% every year for each of the last 20 years, we should still want to reduce this probability even though in hindsight everything looks OK.

(b.) Ethereum will presumably grow in prominence in the future (we hope). Powerful entities will see it as more of a threat than they have in the past. This will plausibly make these organizations more interested in attacking it than they have been until now.

(c.) Security depends on price. So even if there is a threshold above which Ethereum is “secure enough”, that threshold varies as price varies. Being far above the threshold protects Ethereum in a market downturn. Whether Ethereum is safe as long as its price stays above $70 vs. safe as long as its price stays above $20 is an important difference.

**Anti-ASIC arguments**

The main arguments I’ve seen against ASICs seem to focus on rejecting argument (2) above. The claim is that ASIC manufacturers and farms really will be willing and able to significantly harm Ethereum. I’ve described above why I don’t think we should worry much about this, but am curious to hear more arguments for why we should be wary of ASICs. I’m especially interested to hear of cases where big ASIC manufacturers / farms engaged in censorship or other attacks against the network.

There’s also a community-based argument: mining is how a lot of people get into crypto, so having a GPU-mined coin will make the coin more popular and increase its network effect. This could be a good argument. I’m not sure how strong this effect is but am curious to explore it. This argument gets better if people new to Ethereum can profitably mine with GPUs that they already own. If seems worse but possibly still good if miners almost always have to buy a new high end GPU if they want to get into mining (assuming these high end GPUs are cheaper than ASIC hardware would be).

**Request for more data / arguments**

I’ve presented the rough outline of the pro-ASIC argument and discussed some common counterarguments. I’m very interested to hear additional arguments either for or against the goal of ASIC-resistance, and am especially interested in any concrete data relevant to this topic.

**Previous discussion**

A few interesting comments from the gitter discussion from members of IfDefElse (the group that created ProgPow and has been advocating for its inclusion in Ethereum):

From [@ifdefelse](/u/ifdefelse):

> I don’t know how many GPUs there are in datacenters, but back-of-the-envelope calculations says the total number is probably less than the eth hashrate. Datacenters use almost exclusively Nvidia Tesla products. Nvidia’s sold around $3 billion to the datacenter market in the last 2 years (this includes government supercomputers). If we ballpark these expensive datacenter GPUs at $1000 each that’s just 3 million GPUs total, across all datacenters in the world.
> https://s22.q4cdn.com/364334381/files/doc_financials/quarterly_reports/2019/Q1-FY19-Rev_by_Mkt_Qtrly_Trend.pdf

Ifdefelse later estimated “The ETH hashrate [is] around 5 million GPUs”

[@ohgodagirl](/u/ohgodagirl) provided her perspective:

> I cannot comment on AWS’ GPU amount. Apologies.
> You want to be considering FPGAs with Ethash, too.
> 51% attacking Ethereum is significantly hard with GPUs.
> I know intimately what each farm has and where GPUs land.
> There are less than two farms that have over 800,000 cards.
> Most “large” farms range in the 40,000-100,000 range and I can tell you people over exaggerate with how much hardware they have consistently.
> A 100,000 GPU farm requires workers. And workers blab all sorts of secrets.
> You guys didn’t factor in Azure or Oracle
> Or Google Compute Cloud
> Or even the private clouds.
> But guess what? None of those will ever touch crypto. There are legal risks, operational risks, and if just plain doesn’t make financial sense.

## Replies

**greerso** (2019-03-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/elliot_olds/48/2094_2.png) elliot_olds:

> (1) GPU mined coins are cheaper to attack with rented hashpower

Ethereum, currently still a GPU mineable coin, is more expensive to attack than every top 50 ASIC **combined**.  Further, the cost of a *theoretical 1hr attack on Ethereum is currently $83,110.  The cost of a 1hr attack attack on Bitcoin is $318,602.  Bitcoin is < 4x more expensive to attack than Ethereum, meanwhile 1BTC is 30x the dollar value 1ETH.

*theoretical because this much hash isn’t available to rent.



      [crypto51.app](https://www.crypto51.app/)





###










https://messari.io/c/screener/


      ![](https://ethereum-magicians.org/uploads/default/original/2X/1/111e6007bae3e0b2dd8cf08bc35995f58d53fda5.png)

      [Crypto Mining Blog – 15 Jan 19](https://2miners.com/blog/51-attack-explained/)



    ![](https://2miners.com/blog/wp-content/uploads/2019/01/51-percent-attack-mining-1200x628-cropped.jpg)

###



Today we will discuss the 51% attack, which is particularly relevant in light of the issues Ethereum Classic is experiencing. Many cryptocurrency “experts” believe that if a user has more than a half of the network hash rate, he can do whatever he...



    Est. reading time: 5 minutes











![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/elliot_olds/48/2094_2.png) elliot_olds:

> (2) The risks from ASICs are small

This argument really made me think the first time I heard it, it sounds undeniable until you consider, with the possible exception of ETC, that every 51% attack we have seen to date has come from Nicehash.  The hash on Nicehash is made up of, indiscriminately, ASIC’s, FPGA’s, GPU’s and possibly other.  The equipment operators are ignorant to the attacks that their hardware is participating in.

ETC have stated publicly that they believe the attack on their network did come from ASIC’s and not from rented ones either.  It did not kill the chain, in fact, ETC price went up immediately after the attack.  See Jan 5th to Jan 7th https://messari.io/asset/ethereum

If that was an ASIC attack and if it was successful, those ASIC’s could have been used on any one of many other ethash chains including Ethereum.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/elliot_olds/48/2094_2.png) elliot_olds:

> (3) Ethereum should try to be more resistant to state-sponsored attacks, all else being equal

In order for any ASIC to be worth the production cost, it needs to be able to monopolize the network hash (paraphrased from David Vorick of Obelisk ‘monopoly’ is a word used often).  If a small group of ASIC’s do monopolize ethash, push out the GPU miners are concentrated in an unfriendly country, this kind of attack becomes far far less costly.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/elliot_olds/48/2094_2.png) elliot_olds:

> (4) We don’t know if our current security level is adequate, so if there are no significant tradeoffs we should prefer higher security levels

When the price of ETH was $800, the hash was lower than it is today.  Ethereum will never see the network any less expensive than it is today because as Eth goes up in values, GPU miners choose to mine Ethereum pushing up network difficulty.

Again, If a small group of ASIC’s do monopolize ethash, push out the GPU miners you may have a high or higher network hash rate, but you do not have security unless the hash is sufficiently distributed.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/elliot_olds/48/2094_2.png) elliot_olds:

> Anti-ASIC arguments

Improving ethash with ProgPoW does not make fixed function ASIC’s impossible, it just significantly restricts the potential efficiency to be had over GPU’s.  Either a fixed function ASIC with <20% (with similar build costs such as similar memory type) can be built and will further help distribute network hash because GPU’s *and* ASIC’s mining on the same network is ideal **OR** The fixed function ASIC is not financially viable because it would be unable to monopolize the network hash.  Nobody wants a monopoly on the security of Ethereum.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/elliot_olds/48/2094_2.png) elliot_olds:

> A few interesting comments from the gitter discussion from members of IfDefElse (the group that created ProgPow and has been advocating for its inclusion in Ethereum):

I feel that I should put those comments in context:  The question was raised about renting GPU’s for attack from AWS.  It was pointed out that there are not enough rentable GPU’s in datacenters including AWS, GCS, Azure, Oracle and private and even if there were the amount of GPU’s required would not be rentable and even if they were, those services go to great efforts not to allow illegal/malicious activity on their networks.

### Other arguments

---

The 2 manufacturer of GPU’s argument not mentioned here is worth a mention in case it comes up later in the thread.  GPU is the name of the chip, miners do not buy GPU’s they buy AIB’s ‘Add In Boards’ made by Nvidia, AMD and soon Intel AIB Partners.  These cards are widely available worldwide from retailers, you do not need permission from Nvidia or AMD to purchase one.

---

From the Ethereum White Paper:

> The Bitcoin mining algorithm works by having miners compute SHA256 on slightly modified versions of the block header millions of times over and over again, until eventually one node comes up with a version whose hash is less than the target (currently around 2192). However, this mining algorithm is vulnerable to two forms of centralization. First, the mining ecosystem has come to be dominated by ASICs (application-specific integrated circuits), computer chips designed for, and therefore thousands of times more efficient at, the specific task of Bitcoin mining. This means that Bitcoin mining is no longer a highly decentralized and egalitarian pursuit, requiring millions of dollars of capital to effectively participate in. Second, most Bitcoin miners do not actually perform block validation locally; instead, they rely on a centralized mining pool to provide the block headers. This problem is arguably worse: as of the time of this writing, the top three mining pools indirectly control roughly 50% of processing power in the Bitcoin network, although this is mitigated by the fact that miners can switch to other mining pools if a pool or coalition attempts a 51% attack.

From the Ethereum Yellow Paper:

> One plague of the Bitcoin world is ASICs. These are specialised pieces of compute hardware that exist only to do a single task (Smith [1997]). In Bitcoin’s case the task is the SHA256 hash function (Courtois et al. [2014]). While ASICs exist for a proof-of-work function, both goals are placed in jeopardy. Because of this, a proof-of-work function that is ASIC-resistant (i.e. difficult or economically inefficient to implement in specialised compute hardware) has been identified as the proverbial silver bullet.

Despite Ethereum’s clear anti-ASIC stance and effort to thwart them, ASIC manufacturers went ahead and developed the hardware anyway.  Now their arguments consist of, “you’re choosing chip manufacturers and excluding us” or “No point trying to resist us, we’ll monopolize your hash no matter what you try” akin to mobsters selling protection to store owners.  See Linzhi’s public commentary.

---

ProgPoW does not benefit from undervolting, so many of the tricks large farms use to gain advantage over home miners will no longer be useful, hash rate will be better represented across different cost hardware.

---

I, and others have been told by Linzhi that we will not pass ‘customer qualification’.  Mining Ethereum should not require permission from a manufacturer.

https://twitter.com/OhGodAGirl/status/1109932988404359169

---

Monero’s hash rate recently dropped by 80% when they forked from suspected FPGA’s and ASIC’s.  No FPGA bitstream or ASIC miner was ever made publicly available for Monero.


      ![](https://cointelegraph.com/_duck/img/favicons/favicon-16x16.png)

      [Cointelegraph](https://cointelegraph.com/news/decentralization-first-privacy-coin-monero-cuts-out-asic-miners-to-stay-independent)



    ![](https://images.cointelegraph.com/cdn-cgi/image/f=auto,onerror=redirect,w=1200/https://s3.cointelegraph.com/storage/uploads/view/6d522f36df1bf37a6f54f84349e048fa.jpg)

###



On March 9, Monero was successfully upgraded via a hard fork.










---

ASIC manufacturers compete directly with their customers.

https://medium.com/@CobraBitcoin/the-sad-story-of-sha-256-and-why-we-need-a-new-pow-algorithm-6ffe9d919cfb

---

At 50:40 on this podcast Zooko Wilcox states that “there were probabaly 10 times as many zcash miners before the ASIC’s kicked in”

https://www.whatbitcoindid.com/podcast/privacy-and-zcash-with-zooko-wilcox

---

### Other sources

https://medium.com/@OhGodAGirl/the-problem-with-proof-of-work-da9f0512dad9

https://medium.com/@ifdefelse

  [![image](https://ethereum-magicians.org/uploads/default/original/2X/c/c3b6bf59e8ef9bdba77fb9026d0e91645ad49247.jpeg)](https://www.youtube.com/watch?v=pe1pDGDy6iE)

https://medium.com/@andrea.lanfranchi/what-gpu-miners-may-not-know-about-progpow-a9bb42a0d5a7

https://medium.com/@andrea.lanfranchi/ethereum-governance-me-and-progpow-729ed1d9445f

https://medium.com/@lookfirst/13-questions-about-ethereums-movement-to-progpow-e17e0a6d88b8

https://medium.com/@fubuloubu/skeptical-about-progpow-i-am-too-5211c88faf35



      [swende.se](https://swende.se/blog/Progpow.html)





###



Martin Holst Swende, programming and appsec










https://medium.com/@infantry1337/comprehensive-progpow-benchmark-715126798476?sk=8acbe3fb45ef704a20dc09c87a5890a8



      [github.com/monero-project/meta](https://github.com/monero-project/meta/issues/316#issuecomment-473872335)












####



        opened 07:58AM - 12 Mar 19 UTC



          closed 03:26PM - 05 Jun 20 UTC



        [![](https://avatars.githubusercontent.com/u/18739807?v=4)
          dEBRUYNE-1](https://github.com/dEBRUYNE-1)










This ticket is meant as supplement to #315 as well as a place where ideas can be[…]() discussed in more detail and outside of the scheduled meeting(s). As far as I can see, we basically have these options:

1. Maintain the current tweaking schedule. I think we can all agree this strategy has not worked and is potentially dangerous and should thus be abandoned.

2. Expedite the current tweaking schedule (e.g. fork every 3-4 months). This would, in my opinion, be unsustainable and thus not feasible. Some services already deem our current 6 month schedule as aggressive. Expediting the schedule may even put us at risk of these services delisting us. We also have to keep in mind a future where the Monero ecosystem grows. The more the ecosystem grows, the more difficult forks will become to coordinate and execute.

3. Switch to an ASIC friendly algorithm in the next scheduled protocol upgrade. Some people are worried the ASIC (manufacturer) ecosystem has not sufficiently matured yet. Presumably, it will mature further once time passes. Whether waiting is worth the incurred trade-offs is the question though.

4. Perform one more tweak and switch to an ASIC friendly algorithm thereafter. This would allow the current miners to achieve some ROI, which can presumably subsequently be used to invest in ASICs.

5. Perform `x` more tweaks and switch to an ASIC friendly algorithm thereafter. This seems like an unwise strategy if we deem the tweaks as a failed strategy.

6. Implement RandomX in October or April (in case it is not ready yet, though it would presumably mean one more tweak). Do not precommit to anything thereafter. I think this strategy would be susceptible to a lot of future controversy to the extent that there will be a contentious debate about the future of the PoW algorithm *if* specialized devices show up for RandomX.

7. Implement RandomX in October or April (in case it is not ready yet, though it would presumably mean one more tweak). Precommit to an ASIC friendly algorithm after 1.5-2 years. This would enable ASIC manufacturers to already start designing devices. Furthermore, it would give us time to try to find a company that could publish an open-source design. Additionally, this removes future friction and allows us to focus on the protocol.

8. Explore a GPU centric algorithm.

9. Explore dual PoW: e.g. RandomX for CPUs, CryptonightR (with tweaks favoring GPUs) for GPUs. As far as I know Zcash investigated harmony mining and deemed it relatively unsafe insofar as that it would significant raise the attack surface and not add that much additional security.

10. [Game Theoretical approach to ASIC resistance (proposed by MoneroCrusher).](https://github.com/monero-project/meta/issues/316#issuecomment-472677985)

11. **Implement RandomX in October. Precommit to switching to an ASIC friendly algorithm (such as SHA3) in case of failure of RandomX. No further tweaks.** // Currently preferred path, as can be seen from [here](https://repo.getmonero.org/monero-project/monero-site/blob/b87354501b6343f9146f331805ddadc45696f728/_posts/2019-03-24-logs-for-the-dev-meeting-held-on-2019-03-24.md).

I'd personally be in favor of option 3, 4, or 7. I have some reservations about RandomX though, which are as follows:

- Fairly new and untested. It thus has not succeeded the test of time.
- Has to be audited, which is going to be costly (and will have to be funded by the community). By contrast, a well-known ASIC friendly algorithm would not require such an audit.
- ~~Increases verification time for nodes, especially for lower end devices. This is predominantly caused by 4GB memory requirement. That is, any device with less than 4GB RAM available will take a large verification performance hit. This, in my opinion, is paradoxical to our ethos where we want everyone to have access to Monero. It would, for instance, making running a node on a Raspberry Pi rather difficult if not completely unfeasible. Lowering the memory requirement significantly would resolve this issue as far as I can see. However, it would also make cryptojacking more attractive.~~ This has been addressed in the new version. Verification time is now approximately similar to earlier versions of CryptoNight.
- ASIC resistance is basically a function of market cap. If Monero grows a lot, someone will inevitably create a specialized device for it that slowly drives out other miners. This would be significantly less of an issue, however, if we'd precommit to a switch to an ASIC friendly algorithm after say, 1.5-2 years. [Hyc responded to this with:](https://www.reddit.com/r/Monero/comments/azinzk/transcript_of_discussion_between_an_asic_designer/eia2nyi/)

>This is only true up to a limit. Everyone has access to the same transistor technology. Unbundling components that CPUs contain that the ASIC doesn't need can only yield so much power savings. Our pessimistic estimate is that ASICs can be 2x more power efficient than CPUs; best case is only 1.2x. These numbers are based on physics, not market cap.

- These numbers are theoretical and I am not entirely convinced they will hold up in practice / the real world as well.
- May be met with a lot of opposition for the mining community, potentially causing a split. Same can be said for switching to ASICs I guess. Although, having one more tweak to allow current miners to achieve some ROI would somewhat mitigate this.

To reiterate, the concept of ASIC resistance, in my opinion, better than ASICs. However, if we cannot viable attain it, the subject should be revisited. Some community members also seem to be venturing into an "at all costs" strategy to preserve ASIC resistance, which is potentially dangerous and may be a net negative for Monero.












### Polls

https://twitter.com/etherchain_org/status/1084349056883802112

https://twitter.com/ethcatherders/status/1093202321310404616

http://progpowcarbonvote.com

https://www.etherchain.org/charts/progpow

https://twitter.com/IslandHunting/status/1109248245031731201

https://twitter.com/themazuma/status/1109230231452352515

https://twitter.com/ethcoredevs/status/1109477560176513024

---

**fubuloubu** (2019-03-29):

Dang, this is comprehensive!

Mega ProgPoW resource post!

---

**elliot_olds** (2019-03-30):

A few brief comments on [@greerso](/u/greerso)’s post:

When I say that GPU mined coins are cheaper to attack with rented hashpower, I’m talking about **all else being equal**. In other words, if ETH is GPU mined then it will be cheaper to attack than if it’s ASIC mined, holding everything else constant (market cap, etc).

Comparing Ethereum today (GPU mined) to a lower market cap ASIC and saying Ethereum is more expensive to attack doesn’t get at the core issue of whether we should allow Ethereum to transition to ASIC mining.

> If a small group of ASIC’s do monopolize ethash, push out the GPU miners are concentrated in an unfriendly country, this kind of attack becomes far far less costly.

It becomes far less costly for the government of that single state, true. But it remains very costly for governments of all other states.

One might object “but then we’re totally at the mercy of the one state that the ASICs are in the jurisdiction of!” This ignores the ease of switching from ASICs → GPUs in response to an attack.

It’s true that Ethereum wouldn’t be harder to attack if ASIC mined vs. GPU mined for that specific country, but it’d be harder to attack for all others and if it were attacked by the one specific country then it could evade its attack relatively easily.

> When the price of ETH was $800, the hash was lower than it is today.

Hashrates improve with technology – all that matters is the $ cost of securing or attacking the network. The amount spent to secure the network will in the long run be what is paid out by the network to miners, and will be independent of the hash function used.

A while back Phil Daian wrote a post arguing for why ASICs should not be avoided. People seem to find it pretty convincing (moreso than my posts), so here it is:

https://pdaian.com/blog/anti-asic-forks-considered-harmful/

Phil makes one interesting argument that I don’t make above: that PoW-changing hard forks open up a governance attack vector. Interesting to think about given all the drama of ProgPow so far.

