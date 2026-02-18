---
source: magicians
topic_id: 24885
title: Soliciting stakeholder feedback on Glamsterdam headliners
author: nixo
date: "2025-07-22"
category: EIPs
tags: [glamsterdam]
url: https://ethereum-magicians.org/t/soliciting-stakeholder-feedback-on-glamsterdam-headliners/24885
views: 2326
likes: 102
posts_count: 26
---

# Soliciting stakeholder feedback on Glamsterdam headliners

## Headliners were selected at

- Consensus layer: EIP7732 ePBS
- Execution layer: EIP7928 Block-level Access Lists
- Stakeholder-feedback-synthesized

Thank you everyone for your feedback.

---

The [Glamsterdam headliner](https://ethereum-magicians.org/t/eip-7773-glamsterdam-network-upgrade-meta-thread/21195) feature is being chosen over the next few All Core Dev calls. You have an opportunity to voice your opinion on which feature should be selected.

For an overview of these choices, visit [Forkcast](https://forkcast.org/upgrade/glamsterdam).

### What stakeholder category do you represent?

*e.g. wallet devs, DEXs, bridges*

### What do you view as the top priority theme in this fork & why?

*e.g. censorship resistance, scaling the L1, improving UX, etc.*

### Which EIP(s) do you favor as a headliner for Glamsterdam?

*note*: the process is aiming for one EIP each for the consensus and execution layers

### If known, what specific impacts would this have on your community?

*e.g. this EIP would enable our users to…*

### Does anything make this an urgent feature for you or your community?

*e.g. not urgent, but it would streamline…*

### The leading headliners among client teams are described in a . Do you have any concerns about any particular proposal?

*e.g. they’re all good eggs*

### Any additional comments?

---

## Replies

**quickchase** (2025-07-22):

### What stakeholder category do you represent?

*e.g. wallet devs, DEXs, bridges*

RPC Providers

### What do you view as the top priority theme in this fork & why?

*e.g. censorship resistance, scaling the L1, improving UX, etc.*

Scaling the L1 can bring additional traffic but may also increase infrastructure costs. Improving UX can onboard more users and attract new customers. Censorship resistance helps maintain Ethereum’s credible neutrality, making it attractive to institutions seeking to avoid counterparty risk.

### Which EIP(s) do you favor as a headliner for Glamsterdam?

*note*: the process is aiming for one EIP each for the consensus and execution layers

We have no official stance.

### If known, what specific impacts would this have on your community?

*e.g. this EIP would enable our users to…*

Provable RPC responses may provide some additional security and piece of mind to our customers knowing that the data they are receiving is unaltered. However, this EIP focuses mostly on logs and receipts where as most of our customer’s headaches comes from the outputs of poorly standardized methods like debug_traceBlockByX.

### Does anything make this an urgent feature for you or your community?

*e.g. not urgent, but it would streamline…*

No.

### The leading headliners among client teams are described in a series of blog posts listed here. Do you have any concerns about any particular proposal?

*e.g. they’re all good eggs*

No concerns.

### Any additional comments?

![:rocket:](https://ethereum-magicians.org/images/emoji/twitter/rocket.png?v=15)

---

---

**claravanstaden** (2025-07-23):

### What stakeholder category do you represent?

Bridges – specifically **Snowbridge**, a trustless, light-client-based bridge between Ethereum and Polkadot.

### What do you view as the top priority theme in this fork & why?

**Faster finality:** Trustless bridging is only viable if the user experience is competitive with centralized multisig bridges. When finality delays are excessive, users opt for less secure but faster alternatives. If we want to preserve decentralization in the bridging space, we must reduce Ethereum’s time to finality.

### Which EIP(s) do you favor as a headliner for Glamsterdam?

**EIP-7782:** Time to finality is the primary UX bottleneck for Snowbridge. Halving block times would halve the time it takes for a transaction to finalize on Ethereum, offering a major improvement to the bridging experience.

### If known, what specific impacts would this have on your community?

It would dramatically improve the speed and usability of trustless Ethereum → Polkadot transfers. Polkadot users are accustomed to ~1–2 minute delays. The current ~13–15 minute finality wait from Ethereum is a major friction point that deters usage and limits adoption.

### Does anything make this an urgent feature for you or your community?

Absolutely. We are losing users and integrations due to Ethereum’s slow finality. It also restricts the types of bridge applications that can be built, such as arbitrage, payments, or real-time interactions, where latency is a critical constraint.

### The leading headliners among client teams are described in a series of blog posts listed here. Do you have any concerns about any particular proposal?

No concerns at this time.

### Any additional comments?

We’re excited to see Ethereum continue evolving in ways that preserve decentralization without compromising usability. Reduced block latency would be a milestone for bridges and cross-chain apps. We’re eager to support and build on a faster, more responsive Ethereum.

[![glamsterdam-headliner-rankings](https://ethereum-magicians.org/uploads/default/original/2X/a/a04d58cd4721aa6d75f3ce54d3db8fcf33195e5f.png)glamsterdam-headliner-rankings540×270 35.3 KB](https://ethereum-magicians.org/uploads/default/a04d58cd4721aa6d75f3ce54d3db8fcf33195e5f)

---

**fiddy** (2025-07-23):

### What stakeholder category do you represent?

I am a contributor to the Lido DAO, which runs the Lido Protocol, a Decentralised Staking Middleware. The opinions are not a DAO-wide mandate, rather a reflection from several discussions both internally and externally. The mention of ‘we’ in this discussion is a reference to our collective consensus on topics relevant to Glamsterdam.

### What do you view as the top priority theme in this fork & why?

The top priority theme is L1 Scaling via Slot Pipelining. While other goals like lower latency and censorship resistance are critical, slot pipelining is the most strategic, foundational improvement. It focuses on mechanisms in block production, creating efficiency that enables higher throughput (more gas/blobs) and makes future improvements, including latency reduction, safer and more impactful.

### Which EIP(s) do you favor as a headliner for Glamsterdam?

- Execution Layer: We favor EIP-7928 (Block-level Access Lists). It’s a high-impact, low-risk proposal that directly enhances transaction execution efficiency and L1 scalability.
- Consensus Layer: Our position is nuanced. For slot pipelining, we have a slight preference for EIP-7886 (Delayed Execution) due to a smaller consensus-layer footprint. However, we recognize that EIP-7732 (ePBS) has greater community momentum and a more mature specification. We are committed to supporting whichever solution the community chooses, provided the risks to staking infrastructure are mitigated. Finally, our ideal choice would be a mix of ePBS and Delayed Execution, where DE uses the payload-block separation logic of ePBS with a PTC to validate payload timeliness.
- We also strongly advocate for EIP-7805 (FOCIL) to be included alongside any pipelining EIP to ensure Ethereum’s credible neutrality is hardened in parallel with its performance. The logic here is that FOCIL is compatible with slot pipelining approaches, as per research.

### If known, what specific impacts would this have on your community?

- Slot Pipelining (ePBS/DE): This would require significant development to adapt our infrastructure. For ePBS specifically, it means managing the operational complexity of a dual pipeline (in-protocol and MEV-Boost) and ensuring the security of delegated stake. The refinements we’ve collaborated on (like the 0x03 credential and feeRecipient) are crucial to making this viable and preventing negative impacts on our users and node operators. More on this topic here: Lido Contributor Recommendations for the Glamsterdam Upgrade - HackMD
- FOCIL: This would have a profoundly positive impact by providing our users with the assurance that they are staking on a credibly neutral platform with strong, in-protocol censorship resistance guarantees.

### Does anything make this an urgent feature for you or your community?

Yes. **Slot Pipelining** is strategically urgent because it unblocks future scaling and latency improvements. **FOCIL** is philosophically urgent; if we don’t enshrine core values like censorship resistance now, during a major architectural upgrade, we risk creating a precedent where they are perpetually sidelined for performance gains. This is a critical window of opportunity to do both.

### The leading headliners among client teams are described in a . Do you have any concerns about any particular proposal?

Yes, we have well-defined concerns about **EIP-7732 (ePBS)**, detailed here: [Lido Contributor Recommendations for the Glamsterdam Upgrade - HackMD](https://hackmd.io/@lido/BJM4Lco8gg#Slot-Pipelining-Part-I-%E2%80%94-The-Case-for-ePBS-EIP-7732)

Our primary concern is the **implementation risk** for large-scale staking infrastructure. Its complexity and direct modifications to the consensus layer mean that any late-stage changes to the specification would be extremely costly and time-consuming for us to adapt to, posing a risk to our operations. While our collaborations with client teams have been very productive in mitigating the initial security and design flaws, this risk of “in-flight” changes remains.

### Any additional comments?

Our position is fundamentally collaborative. While we have a preference for the lower-risk path of Delayed Execution + PTC (a combination of the best from ePBS and DE), our primary goal is to ensure that whichever pipelining solution is chosen is implemented in a way that is secure, stable, and operationally viable for the entire staking ecosystem. We believe the best outcome for Glamsterdam is one that combines a robust scaling solution with an unwavering commitment to Ethereum’s core value of credible neutrality via FOCIL.

---

**dataalways** (2025-07-23):

### What stakeholder category do you represent?

Flashbots

### What do you view as the top priority theme in this fork & why?

Scaling the L1 without introducing negative externalities.

### Which EIP(s) do you favor as a headliner for Glamsterdam?

BALs and ePBS, assuming that the Free Option Problem can be sufficiently mitigated.

### If known, what specific impacts would this have on your community?

Enabling trustless exchange between builders and proposers would be a strong change for the ecosystem; disintermediating relays would remove one of the main chokepoints in the MEV supply chain that contributes to geographic centralization and censorship.

### Does anything make this an urgent feature for you or your community?

MEV market structure is unstable due to years of indecision on disintermediating relays. The inclusion of rejection of ePBS will force that decision and move us to a different equilibrium.

### The leading headliners among client teams are described in a . Do you have any concerns about any particular proposal?

FOCIL’s lack of coverage of blobs makes it only a stepping stone to full CR. If it led to a decrease in the number of local builders, the CR of blob-carrying transactions would be greatly reduced because of the gap in coverage.

Shorter-slot times are very under researched and we’re not confident about their feasibility or the impact that they would have on the geographic decentralization of the validator set.

The current version of EIP-7732 introduces a Free Option Problem that we strongly suggest should be mitigated. Our conversations with searchers have made it clear that failing to mitigate it will lead to a substantial increase in empty blocks on the Network. Extended analysis is available here.


      ![](https://collective.flashbots.net/uploads/default/optimized/1X/7a99a7f355a2ab01e7eec8bb90f6cc59be63573a_2_32x32.png)

      [The Flashbots Collective – 23 Jul 25](https://collective.flashbots.net/t/the-free-option-problem-in-epbs/5115)



    ![image](https://collective.flashbots.net/uploads/default/original/2X/0/020e09e1c39c182751664fef47e8f3dc25c6e8bb.png)



###





          Research






            pbs
            auction







tl;dr: we argue that the “free option” problem is potentially substantial in the current specification of  EIP-7732: Enshrined Proposer-Builder Separation  joint work with @0xSybil and @BrunoMr  Special thanks to @dataalways for extensive...



    Reading time: 10 mins 🕑
      Likes: 35 ❤











### Any additional comments?

We provided an extended MEV-informed opionion on all the consensus layer headline proposals and would encourage everyone to read it.


      ![](https://collective.flashbots.net/uploads/default/optimized/1X/7a99a7f355a2ab01e7eec8bb90f6cc59be63573a_2_32x32.png)

      [The Flashbots Collective – 23 Jul 25](https://collective.flashbots.net/t/an-mev-perspective-on-glamsterdam/5116/1)



    ![image](https://collective.flashbots.net/uploads/default/original/1X/7a99a7f355a2ab01e7eec8bb90f6cc59be63573a.png)



###





          The Flashbots Ship






An MEV Perspective on Glamsterdam This post reflects the opinions of Data Always and Hasu and seeks to provide an MEV-informed perspective on the headlining proposals for Glamsterdam. Our aim is to highlight tradeoffs that are missing from the...



    Reading time: 3 mins 🕑
      Likes: 16 ❤

---

**ryanberckmans** (2025-07-24):

imo when compared to recent forks, the Glamsterdam fork design process seems to be more self-aware and holistic in terms of representing competing stakeholder interests and the overall longitudinal health and ambition of ethereum. I’m happy to see this - thanks to everyone involved.

One thread that caught my eye and seemed like a yellow flag was Hasu and DataAlways’s discussion of ePBS potentially causing many more empty blocks due to builders being paid by searchers to withhold block data.

---

**jdetychey** (2025-07-24):

### What stakeholder category do you represent?

*e.g. wallet devs, DEXs, bridges*

Solo staking (myself), Account Abstraction and EU-regulated Custody provider (Cometh)

### What do you view as the top priority theme in this fork & why?

*e.g. censorship resistance, scaling the L1, improving UX, etc.*

UX, L1 and L2 scaling without compromise on decentralization, censorship resistance and neutrality

### Which EIP(s) do you favor as a headliner for Glamsterdam?

*note*: the process is aiming for one EIP each for the consensus and execution layers

CL: EIP-7782 Reduce Block Lattency

EL: EIP-7692 EVM Object Format

**re EIP-7782**, it brings immediate UX improvements on DeFi, on block building market (more frequent and smaller auctions), faster L1 finality for bridges and L2 interop.

Solo stakers will have their reward volatility reduced. Bandwidth is often mentioned as a major issue for solo stakers, potentially having more frequent but less full blocks could be better. Being picked twice more often as a proposer is very appealing from a censorship resistance perspective.

**One concern on EIP-7782**, it has to come with emission adjustment so as to not end up with greater emission rate.

**re EIP-7692**, new execution formats like Risk-V is very attractive. New use cases and new account management method through smart account call for more flexibility at the execution level. Pre-compile additions on the L1 have proven to be a long process (for example, we’ve already been discussing [EIP-7212](https://ethereum-magicians.org/t/eip-7212-precompiled-for-secp256r1-curve-support/14789) for 2 years now).

### If known, what specific impacts would this have on your community?

*e.g. this EIP would enable our users to…*

---

### Does anything make this an urgent feature for you or your community?

*e.g. not urgent, but it would streamline…*

---

### The leading headliners among client teams are described in a . Do you have any concerns about any particular proposal?

*e.g. they’re all good eggs*

Good eggs

### Any additional comments?

---

---

**jvranek** (2025-07-24):

### What stakeholder category do you represent?

*e.g. wallet devs, DEXs, bridges*

Commit-Boost and Fabric

### What do you view as the top priority theme in this fork & why?

*e.g. censorship resistance, scaling the L1, improving UX, etc.*

We’re extremely excited to see ePBS and 6s slots pushing L1 scaling but our heart truly lies with FOCIL. Censorship resistance is one of the features that drew many of us to Ethereum in the first place. In fact a flavor of FOCIL was one of the first Commit-Boost module’s developed: [il-boost/src at main · eserilev/il-boost · GitHub](https://github.com/eserilev/il-boost/tree/main/src).

Doubling down on CR in Glamsterdam makes sense to us in spirit and in strategy. We’re witnessing a complete renaissance of Ethereum as institutions begin to adopt the technology. It’s never been more important to enshrine one of our most important values today, not after it’s too late.

### Which EIP(s) do you favor as a headliner for Glamsterdam?

*note*: the process is aiming for one EIP each for the consensus and execution layers

EIP-7805 FOCIL

### If known, what specific impacts would this have on your community?

*e.g. this EIP would enable our users to…*

This EIP would ensure censorship resistance remains a top priority regardless of how the builder market ends up developing in the future.

### Does anything make this an urgent feature for you or your community?

*e.g. not urgent, but it would streamline…*

Not urgent but we believe it’s now or never.

### The leading headliners among client teams are described in a series of blog posts listed here. Do you have any concerns about any particular proposal?

*e.g. they’re all good eggs*

They’re all great proposals, in fact we’ve written about how ePBS can remain compatible with the L1 preconf specs from Fabric here: [Notion](https://twisty-wednesday-4be.notion.site/ePBS-EIP-7732-Based-Preconfs-20f968886c71806488d4d08abfc404a2?source=copy_link)

---

**tim-clancy.eth** (2025-07-24):

### What stakeholder category do you represent?

Cypherpunks, Miladys, L2s.

### What do you view as the top priority theme in this fork & why?

Ethereum’s censorship resistance is the single most important thing to begin improving. FOCIL is the first step towards this and ought to have been prioritized for Fusaka if not Pectra. We need it in Glamsterdam.

### Which EIP(s) do you favor as a headliner for Glamsterdam?

I favor EIP-7805 FOCIL for the consensus layer with [EIP-7732 ePBS as a nice potential bonus](https://ethereum-magicians.org/t/epbs-focil-compatibility/24777).

I favor EIP-7928 BALs for the execution layer but am largely ambivalent provided we never implement EOF with its introspection-banning flaws.

### If known, what specific impacts would this have on your community?

FOCIL would enable our community to freely transact without censorship on Ethereum. It would also enable us to advocate much more reliably for Ethereum by pointing to a proven, implemented mechanism for educating people about the reduced peril of centralized builders. Most importantly, it is critical to have a mechanism like this as we move into the ZK endgame and scale to such a degree that we effectively abolish the ability for standard, local, full node builders to exist.

BALs are mostly important as a tool for, alongside transaction gas limits, guaranteeing some degree of parallelism in each block to constrain the worst case proving times of the ZK endgame.

### Does anything make this an urgent feature for you or your community?

[![2025-06-03-224442_753x305_scrot](https://ethereum-magicians.org/uploads/default/optimized/2X/2/225328516f352d8c8ba563e45477d9ee909b666c_2_690x279.png)2025-06-03-224442_753x305_scrot753×305 333 KB](https://ethereum-magicians.org/uploads/default/225328516f352d8c8ba563e45477d9ee909b666c)

I advocate with religious fervor for Ethereum to consume all software in existence and become the [hardest neutral blockspace in the lightcone of all intelligence](https://chii.nekoweb.org/files/milady_zine_01.pdf). Ethereum’s hardness is indisputable. Its neutrality is also second to none, but we all watched builder centralization actively test that during the Tornado Cash sanctions. We need to use the time we have now to ensure that can never happen again, if for no other reason than to honor Roman Storm’s potential martyrdom by ensuring his creation is eternally operable. Ethereum’s credible neutrality survived the coercive effects of a superpower but it was a closer run thing than it ever had any reason to be.

### The leading headliners among client teams are described in a . Do you have any concerns about any particular proposal?

I like that most client teams acknowledges the importance of FOCIL and are broadly supportive, but I am concerned about the clients who propose deferring FOCIL until 2026. It’s been too long.

I dislike that some clients are still supportive of EOF in its current state. As the [Besu team puts it](https://hackmd.io/@RoboCopsGoneMad/Ski-5cHLge), the “issues that led to deferring EOF in previous planning cycles have not materially shifted”. It is simply not suitable for the application layer in its current state.

### Any additional comments?

I love the core devs and this is my ranking.

[![glamsterdam-headliner-rankings](https://ethereum-magicians.org/uploads/default/original/2X/4/4d79f9cac9300ec78ef0fc8d7423884bacb58560.png)glamsterdam-headliner-rankings540×312 44.3 KB](https://ethereum-magicians.org/uploads/default/4d79f9cac9300ec78ef0fc8d7423884bacb58560)

---

**wminshew** (2025-07-25):

### What stakeholder category do you represent?

*e.g. wallet devs, DEXs, bridges*

Wallet dev / account abstraction

### What do you view as the top priority theme in this fork & why?

*e.g. censorship resistance, scaling the L1, improving UX, etc.*

Improving the UX. Ethereum, afaict, is reasonably censorship resistance atm and gas prices continue to stay low, but the overall UX is nowhere near good enough for the average human. (Biggest issues here that come to mind are slowness & the tension between AA & rollup scaling.)

### Which EIP(s) do you favor as a headliner for Glamsterdam?

*note*: the process is aiming for one EIP each for the consensus and execution layers

CL: EIP 7782 reduce block latency. Should make ~everything snappier, which has a lot of other downstream benefits (as elucidated in forkcast). Honorable mention goes here to FOCIL, which I think we should do shortly thereafter.

EL: EIP 7928 BAL. Feels like a big efficiency boost for a lot of load-bearing systems, if done right.

### If known, what specific impacts would this have on your community?

*e.g. this EIP would enable our users to…*

7782 should just make every single interaction with ethereum+ better.

BAL, as I understand it, would lower costs for AA, swapping, L2 settling & bridging, etc

### Does anything make this an urgent feature for you or your community?

*e.g. not urgent, but it would streamline…*

n/a

### The leading headliners among client teams are described in a . Do you have any concerns about any particular proposal?

*e.g. they’re all good eggs*

I’m pretty skeptical about EOF helping developers, personally. It seems very complicated and I just don’t really see the benefits as a smart contract / app developer atm (and even makes my life a lot harder in the short term).

### Any additional comments?

Appreciate all of you. Thank you for your time.

---

**bnjyyy** (2025-07-25):

### What stakeholder category do you represent?

Home staker & User

### What do you view as the top priority theme in this fork & why?

L1 & L2 scaling , CR

### Which EIP(s) do you favor as a headliner for Glamsterdam?

CL: ePBS (+ FOCIL if doable, otherwise next fork)

EL: BALs

### If known, what specific impacts would this have on your community?

ePBS would significantly reduce peak bandwidth for stakers. unlocks future L1 & L2 scaling, separates proposers & builders in protocol.

### Does anything make this an urgent feature for you or your community?

lays the foundation for massive scaling. app focus shifts to L1 again and keeps it usable for individual users.

pipelining seems to be essential for increasing the gas limit and blobs futher while keeping the chain stable. according to a comment on ACDC yesterday not adding pipelining to Glamsterdam would push zkVMs back ~1 year.

### The leading headliners among client teams are described in a . Do you have any concerns about any particular proposal?

6 second slots (EIP-7782):

many uncertainties and it’s not known if this proposal is even possible currently. still a lot of things to investigate and there seems to be a broad consensus among core devs to do pipelining first.

while I really like the UX improvements it brings I’d rather have it in the fork after Glamsterdam.

### Any additional comments?

CL Teams want ePBS, EL Teams want BALs. Different opinions from Community & Stakeholders but it seems like there is no opposition to any of the favourite headliners.

So I think ePBS and BALs should go into Glamsterdam.

(maybe FOCIL if it’s not too much effort alongside ePBS and doesn’t delay the fork)

---

[![glamsterdam-headliner-rankings](https://ethereum-magicians.org/uploads/default/original/2X/a/a98b9aa83c72e419f8a01066ba42b923fcf7006a.png)glamsterdam-headliner-rankings540×438 41.1 KB](https://ethereum-magicians.org/uploads/default/a98b9aa83c72e419f8a01066ba42b923fcf7006a)

Kind regards, keep up the good work ![:heart:](https://ethereum-magicians.org/images/emoji/twitter/heart.png?v=15) ![:rocket:](https://ethereum-magicians.org/images/emoji/twitter/rocket.png?v=15)

---

**and882** (2025-07-25):

### What stakeholder category do you represent?

Shutter Network

### What do you view as the top priority theme in this fork & why?

censorship resistance

The current PBS supply chain is based on centralization and trust assumptions, allowing censorship to occur at various stages, including at the relay, builder, and proposer levels. This concentration of power in the supply chain could undermine the very principles of fairness and decentralization Ethereum originally set out to achieve.

### Which EIP(s) do you favor as a headliner for Glamsterdam?

EIP-7805 (FOCIL) and EIP-7732 (ePBS)

### If known, what specific impacts would this have on your community?

These EIPs improve censorship resistance and reduce central points of trust, two goals that the Shutter Network aims to achieve as well with its decentralized approach towards encrypted mempools. In fact, the EIPs integrate well with encrypted mempools, allowing to further strengthen censorship resistance and prevent malicious MEV extraction. For instance, an encrypted mempool could help address the [free option problem](https://collective.flashbots.net/t/the-free-option-problem-in-epbs/5115) in EIP-7732 (ePBS), where builders can decide not to release the block payload if it is economically advantageous to do so. When transactions in the block are encrypted, however, builders cannot tell how much value a block holds, which significantly reduces the free option. EIP-7805 (FOCIL), on the other hand, provides a mechanism to guarantee transaction inclusion, a crucial requirement for an encrypted mempool. Essentially, encrypted transactions must eventually be decrypted, but only once their inclusion is guaranteed.

While there are some EIPs that relate directly to the encrypted mempool such as [EIP-7793 (Conditional Transactions)](https://ethereum-magicians.org/t/eip-7793-conditional-transactions/21513), we, along with others in the community, are actively working to prepare additional EIPs and align more closely with existing proposals to achieve good censorship resistance. We encourage and need continued support from the broader ecosystem to bring this vision to production.

### Does anything make this an urgent feature for you or your community?

Yes, these EIPs are urgent because they provide critical infrastructure for deploying encrypted mempools securely and at scale. Without ePBS and FOCIL encrypted mempool solutions must rely on complex workarounds or additional trust assumptions, which hinder adoption.

### The leading headliners among client teams are described in a series of blog posts listed here. Do you have any concerns about any particular proposal?

No.

---

**donnoh** (2025-07-25):

### What stakeholder category do you represent?

L2s

### What do you view as the top priority theme in this fork & why?

Censorship resistance and L1 scaling. Apart from the technical merits (which are discussed below), we have the opportunity to signal and prove that what makes Ethereum unique is the ability to both focus on scalability and decentralization at the same time, while most of other blockchains tend to just focus on the former.

### Which EIP(s) do you favor as a headliner for Glamsterdam?

- Consensus layer: FOCIL
- Execution layer: BALs

### If known, what specific impacts would this have on your community?

FOCIL would enable Ethereum to ossify its position as the best eventual censorship resistance (*eCR*) layer for L2s. Today, L2s make use of forced transactions mechanisms to inherit L1’s eCR guarantees and [bypass L2-driven censorship](https://x.com/donnoh_eth/status/1879210463952818472). Forced transactions mechanisms are not simple, as they very often require changes in the derivation logic (see [here](https://specs.optimism.io/protocol/derivation.html#deriving-the-transaction-list), [here](https://docs.arbitrum.io/how-arbitrum-works/transaction-lifecycle#bypassing-the-sequencer), [here](https://docs.scroll.io/en/developers/l1-and-l2-bridging/enforced-transactions/)) and sometimes in the state transition function (see [here](https://github.com/ethereum-optimism/op-geth/blob/3884f258949215fd1bc1f5fddd1b51dc126d4467/core/types/deposit_tx.go#L29), [here](https://github.com/OffchainLabs/go-ethereum/blob/master/core/types/arb_types.go#L81), [here](https://github.com/chainupcloud/scroll-geth/blob/develop/core/types/l1_message_tx.go#L10)), meaning that teams put real effort to build them, or need real effort by projects that don’t have one yet. For context, inheriting L1 eCR is currently considered a [requirement for Stage 1](https://forum.l2beat.com/t/stages-update-a-high-level-guiding-principle-for-stage-1/338) (with some nuance). Some L2s are currently considering building decentralized sequencer networks, primarily to improve real-time censorship resistance (*rtCR*) guarantees, but are also [rightfully asking themselves](https://x.com/jaosef/status/1948407489197682697) if those are enough to provide eCR and avoid the need to build forced transaction mechanisms from L1. **If L1 collapses both eCR and rtCR guarantees to the same set of centralized actors, then we risk not having good arguments in favor of using forced transaction mechanisms from L1. In this world, external sequencing networks might actually provide better guarantees in practice.** Decentralized sequencer networks can also be easily migrated to live on top of any other chain. Ethereum being the best eCR layer would solidify its position as the best L1 for L2s. It’s also important to acknowledge the limits of FOCIL in terms of missed support for blob-carrying transactions. While it’s possible to design forced transaction mechanisms that utilize both blobs and calldata to force message passing from L1 to L2, **all** projects live today with a forced transaction mechanism use calldata (>100 L2s).

BALs are a great way to enable parallel execution and higher throughput on Ethereum. Higher throughput allows for lower L1 transaction prices, which in turn allows projects to post transaction batches, proofs and state updates more often on L1. Today, [most chains](https://l2beat.com/scaling/liveness) touch L1 only once every hour or few hours to better amortized L1 costs over a larger set of L2 transactions. Infrequent batch posting to L1 increases finalization latency, which increases the amount of value at risk of being unilaterally reorged by the L2 sequencer, deposit times to CEXs, and the risk that intent solvers need to take when relaying funds, potentially increasing fees. Infrequent proof posting incentivizes the development of “proof aggregation” layers that might extract fees and add another dependency to already very complex systems. Infrequent state updates increase withdrawal times for all users and the ability to send messages across L2s, hurting interoperability. Increasing L1 throughput does a much better job at reducing L2 latency than reducing slot times from 12s to 6s as the current bottleneck is L1 costs.

### Does anything make this an urgent feature for you or your community?

FOCIL is a critically urgent feature as L2s need to know where L1 is going and plan ahead the development of eCR mechanisms such as forced transaction mechanisms or decentralized sequencer networks. We need to know what to recommend to teams, in particular whether it makes sense to keep inheritance of L1 eCR as a requirement for Stage 1 and 2, as it only makes sense if L1 is the best provider. Again, I invite everyone to ponder on what they would reply to [this question by the Aztec team](https://x.com/jaosef/status/1948407489197682697).

### The leading headliners among client teams are described in a . Do you have any concerns about any particular proposal?

Main concern lies on those proposals that have the potential to lower eCR guarantees, including ePBS and shorter block times, as they would aggravate the issues described above. Introducing them with or after FOCIL would allow to get all their benefits without the relevant downsides expressed here.

### Any additional comments?

The above represents the views of L2BEAT’s research team.

---

---

**Ariiellus** (2025-07-26):

### What stakeholder category do you represent?

*Home Staker, user, MEV enthusiast*

### What do you view as the top priority theme in this fork & why?

*L1 Scaling, CR, MEV*

### Which EIP(s) do you favor as a headliner for Glamsterdam?

*CL: ePBS*

*EL: BALs*

### If known, what specific impacts would this have on your community?

*BALs improve UX which will attract L2s/AltL1s users to Mainnet. ePBS creates more room for block/blob propagation.*

### Does anything make this an urgent feature for you or your community?

*BALs enable parallel execution, which reduces gas costs, directly impacting the user experience and attracting more users to DeFi on L1. ePBS promotes decentralization.*

*ePBS is a win for Home Stakers because the slot reestructure. Additionally, promotes decentralization and contributes MEV minimization in multiblock scenarios.*

I*n addition, I would like to see ePBS along FOCIL to increase CR.*

---

**huiwang925** (2025-07-27):

Above everything else, I would like to hightlight Mark Tyneway’s post here:


      ![](https://storage.googleapis.com/papyrus_images/694b314a3591e8ebaba73dee4801526d.jpg)

      [name pending](https://paragraph.com/@tynes/on-glamsterdam-and-privacy)



    ![](https://paragraph.com/api/og?title=On+Glamsterdam+and+Privacy&blogName=name+pending&blogImageUrl=https%3A%2F%2Fstorage.googleapis.com%2Fpapyrus_images%2F694b314a3591e8ebaba73dee4801526d.jpg&publishedDate=1753561193995)

###



We have an opportunity to cement Ethereum as the economic hub of the internet. This opportunity is not guaranteed or permanent, there are many other networks that would be happy to beat us in achieving that outcome. Institutional capital is coming...










### What stakeholder category do you represent?

A daily user really cares about Ethereum and ETH

### What do you view as the top priority theme in this fork & why?

Scaling the L1, improving UX.

### Which EIP(s) do you favor as a headliner for Glamsterdam?

CL: 6 second slots (EIP-7782)  preferred, or ePBS if there is no P0 bug like free option AND we will implement 6 second slots in the immediate H* fork.

EL: BALs

### If known, what specific impacts would this have on your community?

Cheaper and Faster transactions for all Ethereum users.

### Does anything make this an urgent feature for you or your community?

It’s urgent for Ethereum to strengthen and cement its position as the foundational settlement and issuance layer. Over the next few years, the strongest and most mature narratives for Ethereum and ETH are **stablecoins** (potentially ~$3T within four years) and **tokenization** (potentially hundreds of trillions scale). Yet Ethereum has been losing stablecoin market share to Tron in recent years—and if we don’t respond, we risk ceding tokenization to other alt-L1s as well. How do we fight back?  Make transactions cheaper (e.g. BAL or ePBS) and faster (e.g., 6‑second slots). While gas repricing and BALs reduce costs, from a return‑on‑investment and user‑experience perspective, **prioritizing latency improvements** should take precedence over additional gas‑limit increases that ePBS may enable.*

### The leading headliners among client teams are described in a . Do you have any concerns about any particular proposal?

Ethereum currently secures more than $500 billion in value and could surpass $1 trillion by year‑end. We should not ship any EIP that carries even a remote risk of a P0‑class bug. Security takes precedence over everything else—including making transactions faster or cheaper.

### Any additional comments?

People in the Ethereum developer community often talk about cool and advanced technologies. But if we truly want to build Ethereum as a product, we need to solve real user pain points. One of the most obvious and persistent issues is the anxiety and nervousness users feel when transferring ETH or USDC or USDT on Ethereum—by far the most common types of transactions, as shown on the ultrasound.money burn leaderboard. The uncertainty, pressure, and fear of losing funds grow exponentially with every passing second during a transaction.

---

---

**yorickdowne** (2025-07-27):

Seven people on ethstaker Discord weighed in. That’s too small a sample to be “the voice of the solo staker”. Still, a clear pattern can be seen: ePBS + BAL are the clear front runners.

Opinion on FOCIL is split: FOCIL now even if it leads to delays; FOCIL now as long as the complexity can be managed; FOCIL later because of concerns about complexity if doing ePBS + FOCIL in one fork.

Raw numbers:

ePBS: 7

BAL: 6

purETH: 1

FOCIL now, delays acceptable: 1

FOCIL now but complexity qualifier: 2

FOCIL later bcs of complexity: 2

FOCIL later implied (didn’t mention FOCIL): 2

---

**0x00101010** (2025-07-28):

### What stakeholder category do you represent?

L2s, The following feedback reflects the views of the Base team.

### What do you view as the top priority theme in this fork & why?

We believe scaling the L1 is the top priority for Glamsterdam because it’s the foundation for onboarding the world to Ethereum. A more scalable L1 lowers costs, increases capacity, and improves reliability for both direct users and L2s. This not only unlocks the full potential of rollups but also ensures Ethereum can serve as the global settlement layer for millions of applications and billions of users.

### Which EIP(s) do you favor as a headliner for Glamsterdam?

**![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXehfsgxiaqeho_at33jsSoOJHhCqNZ-kxxnw1a8AX4DVYl_qTTNRz1isO5gib0PN8Iy9LtAH7oWN--MTCCgQpFP-tq3M73AydxFSn99hohdW-Z1m9LWNz9SVccaSynPvsFogEqSYQ?key=xFGlSvTOXi2rfKXq2LnYaQ)**

Edit: We acknowledge that ePBS is the competitive slot restructuring EIP to Delayed Execution in Glamsterdam, and that’s why we list them in different tiers signaling our preference to EIP-7886 Delayed Execution. It can be read as

Option A (our preference): Delayed Execution

Option B: ePBS + BAL

### If known, what specific impacts would this have on your community?

- Delayed execution -

Scaling L1 and blobs: Delayed execution decouples execution from block building, allowing larger blocks and more blobs. It improves throughput and resource efficiency, enabling Ethereum to scale without overloading validators.
- Directly Applicable to L2s: L2s benefit even more from this decoupling. Removing execution from the critical path allows us to reduce buffer times (e.g. for flashblocks), enabling faster blocks and improved decentralization of infrastructure.
- Fast Preconfirmations: By deferring execution, transaction ordering can be committed quickly—unlocking low-latency UX and composability across both L1 and L2.

ePBS - Our community would benefit from the improvements ePBS would make to bandwidth bottlenecks at the CL. This EIP closely aligns with our goal to scale blobs on the L1 and should keep DA costs low for L2 users.

Block-level Access Lists - We see the parallelism this proposal enables as high impact on both the L1 and L2 execution performance. For us at the L2 level, this would massively improve the execution performance of non-sequencing nodes and enable pipelined disk access and execution.

### Does anything make this an urgent feature for you or your community?

Yes—delayed execution is urgent for realizing the full potential of PeerDAS. By reducing execution time constraints and giving more time to propagate blobs, it allows for higher blob throughput, which is a critical next step for scaling Ethereum’s data availability layer. It also significantly improves user experience with fast preconfirmations and enhances L2 scaling.

### The leading headliners among client teams are described in a [series of blog posts listed here]

- Reduce Block Latency to 6s

While we support faster slot times in the long term for better UX, we are concerned about the risks of shipping this in Glamsterdam. Specifically, the reduced time budget intensifies existing consensus overhead, which could negatively impact scaling in the short term. We agree with the view that slot restructuring should precede slot shortening.

### Any additional comments?

---

---

**duncancmt** (2025-07-28):

This prioritization has been revised after [@ethDreamer](/u/ethdreamer) was very kind to take several hours to explain the finer points of some of these EIPs to me.

[![glamsterdam-headliner-rankings](https://ethereum-magicians.org/uploads/default/original/2X/e/edde0fd4220ae9c573db849fb48d904a559a7ac8.png)glamsterdam-headliner-rankings540×480 68 KB](https://ethereum-magicians.org/uploads/default/edde0fd4220ae9c573db849fb48d904a559a7ac8)

S-tier: EIPs required for the topline goal of scalability without centralization

A-tier: it doesn’t seem like a good idea to not have this, but I can see a world where engineering tradeoff require pushing this to a future hardfork

B-tier: I like this. This would make my life easier or I would build on top of this, but it’s not required

D-tier: I have misgivings, but depending on the specific implementation I could be convinced.

### What stakeholder category do you represent?

I represent [0x](https://0x.org/) and [Matcha](https://matcha.xyz/), a DEX aggregator and RFQ platform. (i.e. on-chain token trading)

### What do you view as the top priority theme in this fork & why?

Scaling without centralization.

Ethereum’s draw is its “hardness”, which comes from credible neutrality, which comes from a broad set of participants coming together to reach consensus on the “rules of the game”. Broadening and cheapening access to this is an obvious good, but doing so without compromising on decentralization (and resisting existing centralizing forces) extends Ethereum’s advantages in areas that are hard to commoditize or attack.

### Which EIP(s) do you favor as a headliner for Glamsterdam?

FOCIL (7805) and either ePBS (7732) or delayed execution (7886) are the combination that I’m most excited about, but if you want to get your average blockspace consumer fired up about Glamsterdam, 6-second blocks (7782) should probably be the headliner. Ethereum’s future is healthier with the former, rather than the latter; it is a matter of marketability of the hardfork which I am admittedly a nonexpert at.

I have a slight preference for DE over ePBS because I consider it a simpler concept and prefer the free-DA problem over the free-option problem. The complex interplay between FOCIL and DE (with BAL) seems best solved to me by adopting eBPS’s payload separation. However, I am far from an expert here and my opinion is weakly-held. Either combination is highly desirable. If time pressure and maturity of implementation are a concern, then I fully support ePBS as a pragmatic alternative.

### If known, what specific impacts would this have on your community?

EOF (7692) without introspection would make my life hard. EVM64 (7937) is cool and I would probably use it. However, in our testing, the bottleneck tends to be state access rather than compute, so my interest in EVM64 is relatively low-priority.

### Does anything make this an urgent feature for you or your community?

Things work pretty great. Scaling the L1 is always a concern and would be aligned with our goals, but there is no missing feature that we cannot build delightful applications without.

### The leading headliners among client teams are described in a . Do you have any concerns about any particular proposal?

I still have concerns about the details of the implementation of EOF (7692), as I did for Fusaka. I still hold the opinion that EOF, if implemented, should try to avoid backwards-incompatible/breaking changes *at the level of capabilities for dApp developers*. That means that while I acknowledge that legacy EVM will continue to be maintained and that escape hatches will continue to exist, the capabilities, design patterns, and techniques available to EVM programmers should not be diminished if they choose to port their pipeline over to EOF. Notably that means that I still support things like “Option D” or other options that provide the EVM programmer a superset of that functionality. Attempting to ban gas/code introspection or limit the patterns of contract creation are a net negative to the ecosystem.

### Any additional comments?

I appreciate the process improvement. I am excited to try to get myself and other dApp developers more involved in the hardfork/EIP process.

---

**linoscope** (2025-07-29):

At Nethermind, we pride ourselves on having experts across all levels of the blockchain stack and beyond, with freedom to express their own views. In this article, we present the views of [Nethermind Research](https://www.nethermind.io/nethermind-research) on Glamsterdam. These views are not necessarily representative of [other teams within Nethermind](https://www.nethermind.io/about-us), e.g. Nethermind Client, Nethermind Infrastructure, Nethermind Security, etc.

### What stakeholder category do you represent?

Ethereum Protocol Research and Design.

### What do you view as the top priority theme in this fork & why?

Decentralization

### Which EIP(s) do you favor as a headliner for Glamsterdam?

CL: FOCIL

EL: Block-level Access Lists (BALs)

### If known, what specific impacts would this have on your community?

FOCIL: This is a clear signal that Ethereum is prioritizing censorship resistance. Although the censorship resistance of FOCIL is limited to eventual censorship resistance and vanilla transactions (non-blob transactions), FOCIL stands as an important first step towards censorship resistance. In addition, exciting research have been proposed to [improve FOCIL’s bandwidth consumptions](https://meetfocil.eth.limo/focil-but-with-transaction-hashes/) and extending censorship [resistance for blobs](https://notes.ethereum.org/7EGS7DVtTAKnqlh9LDEWxQ?both). Furthermore, once the validator set can reliably enforce eventual censorship resistance, the protocol can rely more on sophisticated block builders (or execution proposers under APS). A foundation of sophisticated block builders, in turn, clears a path to bolder scalability directions, such as ZK‑ifying L1 execution, where we must rely on sophisticated builders (or execution proposers) to keep full state, execute transactions, and potentially generate proofs.

BALs: BALs lay the groundwork for efficient parallel execution in the EVM. Although extra engineering is still needed to make full use of them, BALs are an essential first step. An exciting [follow‑up](https://ethresear.ch/t/proper-disk-i-o-gas-pricing-via-lru-cache/18146) is to charge less gas for “warm” slots that remain in cache and more for “cold” slots. This ties fees to actual disk work and largely mitigates the negative impact of state growth without complex schemes like state rent or expiry.

### Does anything make this an urgent feature for you or your community?

Both are necessary upgrades.

### The leading headliners among client teams are described in a . Do you have any concerns about any particular proposal?

Although we acknowledge that ePBS’s  decoupling of block validation and payload would be good for Ethereum throughput in isolation, ePBS introduces the [well-documented free-option problem](https://collective.flashbots.net/t/the-free-option-problem-in-epbs/5115). We believe the free option problem needs to be addressed before ePBS is included. Removing the need to commit to a transaction payload in order to receive attestations [may alleviate the problem](https://www.notion.so/c7acde3ff21b4a22a3d41ac4cf4c75d6?pvs=21), but the exact implementation of this needs further work. The referenced solution introduces slot auctions, which come with [well‑documented drawbacks](https://www.notion.so/c7acde3ff21b4a22a3d41ac4cf4c75d6?pvs=21). Furthermore, slot auctions give rational proposers a [strong incentive to bypass the in‑protocol auction](https://www.notion.so/c7acde3ff21b4a22a3d41ac4cf4c75d6?pvs=21) altogether, calling into question why the in-protocol auction mechanism is needed. It may be worth exploring pipelining-only designs that exclude auctions from scope—for example, by embracing the fact that a PBS auction will occur out-of-protocol at the PTC deadline.

Delayed execution removes execution from the critical path, similar to ePBS, yet keeps the protocol simpler, as it avoids PTC, trustless payments, fork-choice modification, etc. However, the current design only pipelines execution, leaving payload broadcasting in the critical path. There are discussions about adding a delayed payload broadcast on top of delayed execution. However, this idea is still in its early stages and requires review for potential issues, such as the free-option problem. Adopting delayed execution first and extending it later may be a viable [plan](https://ethresear.ch/t/slot-restructuring-design-considerations-and-trade-offs/22687#p-55168-minimize-complexity-maximize-future-compatibility-a-pragmatic-path-forward-11), but only if execution‑only pipelining alone proves valuable enough. We require more evidence that this is the case.

Shorter slot times improve UX and reduce the sizeable amounts of MEV that depend on slot time. All else equal, shorter block times also boost censorship resistance by accelerating proposer rotation and can shrink the window from mempool arrival to block inclusion in FOCIL. However, the risk of validator centralization, as [highlighted by Flashbots](https://collective.flashbots.net/t/an-mev-perspective-on-glamsterdam/5116), requires deeper study. Furthermore, we still need a thorough analysis of how shorter slot times interact with other proposals. Even if not scheduled for inclusion in Glamsterdam, we recommend initiating such analysis as soon as possible, given the likely benefits and potential impact of shorter slot times. We want to see shorter slot times incorporated as soon as this analysis is completed and no major issues arise.

### Any additional comments?

Nethermind Research are strong believers in introducing some form of attestor proposer separation (APS). The primary reasons are to preserve the decentralization of the validator set, and addressing the shortcomings that a decentralized validator set introduces with respect to proposer duties. Within the APS design space, there are several designs that would handle the identified risks of both ePBS and faster slot times.

---

**los_a** (2025-07-31):

### What stakeholder category do you represent?

*e.g. wallet devs, DEXs, bridges*

Indexer, Analytics

### What do you view as the top priority theme in this fork & why?

*e.g. censorship resistance, scaling the L1, improving UX, etc.*

Improving UX is essential to onboard a fresh set of users.

### Which EIP(s) do you favor as a headliner for Glamsterdam?

*note*: the process is aiming for one EIP each for the consensus and execution layers

No particular preference

### If known, what specific impacts would this have on your community?

*e.g. this EIP would enable our users to…*

Safe head will allow for more real time data as accounting for reorg can be relaxed

### Does anything make this an urgent feature for you or your community?

*e.g. not urgent, but it would streamline…*

No urgencies

### The leading headliners among client teams are described in a . Do you have any concerns about any particular proposal?

*e.g. they’re all good eggs*

All good

### Any additional comments?

no additional comments

---

---

**duncancmt** (2025-07-31):

[@ethDreamer](/u/ethdreamer) was kind enough to help me develop a more informed opinion on various EIPs, so 0x/Matcha’s response has been updated


*(5 more replies not shown)*
