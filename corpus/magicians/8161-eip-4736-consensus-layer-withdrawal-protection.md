---
source: magicians
topic_id: 8161
title: "EIP-4736: Consensus Layer Withdrawal Protection"
author: benjaminchodroff
date: "2022-01-31"
category: EIPs
tags: [consensus-layer, clwp]
url: https://ethereum-magicians.org/t/eip-4736-consensus-layer-withdrawal-protection/8161
views: 4652
likes: 10
posts_count: 13
---

# EIP-4736: Consensus Layer Withdrawal Protection

There is a growing community of users that are either concerned or know their Ethereum consensus layer (CL) mnemonic and private keys have been compromised through scams or accidental negligence by the validator owner. If the user has not yet set an execution layer (EL) withdrawal address for their validator, as it was not originally possible, then there will be a race to win the “change withdrawal address” operation if multiple parties posses the CL mnemonic and key. Validator owners who do not know they have been compromised will be quite angry and confused to find out their address has already been permanently changed by an attacker with no warning or recourse. However, if we were to start collecting the proposed change withdrawal addresses early and recommend beacon node clients to implement protective features, we can help avoid this situation for the community.

It is only possible to create conditions which favor (not a guarantee) the rightful owner of the CL mnemonic will win the race without changing core consensus. The most verifiable signal that [@mcdee](/u/mcdee) [points out](https://ethresear.ch/t/preparing-withdrawals-for-compromised-validator-or-withdrawal-keys-fao-zilm/10453/9) is that the rightful owner was both in control of the CL mnemonic and EL deposit address. Using proof of the EL deposit address as part of core consensus for the change withdrawal address operation will not be feasible for a number of reasons, but there are other ways it could be optionally considered in the beacon node in a way that does not change consensus:

1. If beacon nodes supported and load an optional “Change Withdrawal Address Acceptance File” containing a list of verifiable withdrawal credential and EL deposit address, it would be possible to have the beacon nodes take this data into consideration (see #3)
2. If beacon nodes support and load an optional “Change Withdrawal Address Broadcast File” containing verifiable lines of change withdrawal address messages, beacon nodes could help automatically broadcast out verified change withdrawal address messages at the right block height when supported, to help spread these message as fast as possible. Additionally, this list can perpetually be used to filter rebroadcasting P2P requests mismatching any requests found in the file.
3. If beacon nodes were to allow an optional “change withdrawal address rebroadcast delay” parameter, they could delay rebroadcasting messages via P2P that do not match the original deposit address. This would not prevent an attacker from eventually winning, but would give favor to any user who requests their original deposit address or an optional line matching the broadcast file loaded by the client.

All of these ideas would not change core Ethereum consensus, but could provide significant protection to the entire Ethereum community by ensuring Change Withdrawal Address operations favor the requested address of the EL deposit address holder. Even if no data files are provided, clients enabling the “change withdrawal address rebroadcast delay” by default would give other clients who are “certain” they are correct an opportunity to gain consensus likely faster than any attacker could achieve. While attackers could use these features to load their contradictory/malicious content, they would be at no advantage unless they can convince a large amounts of nodes to agree.

No user can be certain that their CL mnemonic and key have not been compromised. It is recommended that anyone who wishes could participate in a social campaign on github to collect verifiable “CLWP Claims”, and client software operators implement these optional measures (and ideally enable them) to help the entire community. Multiple large beacon node operators have expressed interest in enabling such protections as a way to help the entire community. These measures can assist the change withdrawal address is as safe and orderly as possible for all legitimate users. I greatly appreciate any ideas or feedback.

## Replies

**Tobes** (2022-02-04):

Dear Ben, JGM, and Pietje Puk, Yorik and all other’s who have contributed to this outstanding proposal.

Having studied carefully your Github proposal and discussed this with yourselves, core devs & major staking providers as well as the countless post’s I have seen on Crypto Twitter and Reddit, it is crystal clear this proposal should be implemented to compound extra security to CL keys, in my opinion every Ethereum Staker running a validator node should use this, at a minimum vote for this proposal to protect their fellow Stakers and the integrity of the network. It is our duty to do so, it is our responsibility as node validators.

This is by far the most comprehensive and well thought out EIP for CL key security that has been discussed thus far, and may be the best chance we have to thwart bad actors who have been meticulously preying on targets all over the world with some highly sophisticated phishing and hacking attacks.

The true level of risk to consensus layer keys at this point is unknown, however we do know that many did not use air gapped computer devices to create their keys and so that in itself is a good enough reason to vote for this EIP.

Not only could this protect a node validator who knows for certain they have had a key breach, we sadly know the number of compromised keys could be in the thousands, this proposal may even help Stakehound who had a very unfortunate issue with validator keys for approximately 1193 nodes, not to mention the countless posts on Reddit and Twitter as previously mentioned. Additionally and maybe most importantly we should not underestimate an even bigger risk which is for those poor souls who are completely unaware that their keys have been breached. Without this EIP there is no way for a node validator to know for sure!

I implore the community to do the right thing and vote for this proposal, we have everything to gain from this EIP. Lets do this. WAGMI. Please let’s do our best to protect one another and not allow hackers to undermine the Ethereum protocol, it’s investors and the Ethereum reputation.

I will do everything I can to help your team and this proposal.

Godspeed!

Tobes - Vibration Servers

---

**matt** (2022-03-19):

It seems like this proposal really hinges on the idea that attackers can’t easily get access to the block production of a slot. If they do, they can completely bypass this protection layer. I’m curious to know your thoughts on this.

---

**benjaminchodroff** (2022-03-19):

Consensus Layer Withdrawal Protection EIP-4736 has been submitted

Yes, this proposal would not change any consensus itself. If an attacker does get selected as the block production, they can win – and this proposal changes nothing. We are willing to take this chance as, to the best of everyone’s knowledge, the block production selection process is random and we are simply trying to create the most favorable conditions for all legitimate validators.

---

**matt** (2022-03-21):

I do see the value in this proposal at the moment that withdrawals are enabled. There will likely be a race between honest actors who want to rotate their keys, because they suspect they’ve been compromised, and attackers who have compromised certain them. After this initial period, I expect that future compromises will not be noticed in the period of time between the compromise and the attacker gaining access to a block production slot. This is the period of time that this proposal is protecting users against. So if validators aren’t noticing that they are compromised in that time, this proposal will not provide any protection.

---

**NeMo540** (2022-05-17):

This proposal would be an excellent additional layer of security to protect one’s assets currently locked into the staking contract.  It’s a simple addition to allow proof of validator ownership by referring to one’s deposit based on the Execution Layer, almost like an on-chain 2FA.

You can most definitely be certain that there are quite a lot of stakers whose keys and mnemonics have been compromised silently in the background.  I know two people in fact who suspect their validator information has been compromised.  The problem is that no one will know until the day withdrawals (or changing of withdrawal addresses) are implemented.  I can’t imagine how so many will feel to find out all of their validators have been blind-sided, switched, or withdrawn to some hacker’s account.  It wouldn’t seem like this massive attack that has been brewing for years will be a good thing for the Ethereum network as a whole given their outstanding track record thus far (minus the DAO hack of course).

For those who are taking the time running validators and supporting the Ethereum network through their stake, it feels like this would be a fair solution that would allow those who were unable to add a withdrawal address initially to help protect their assets, or at least have a shot at recovering compromised funds.  For everyone’s stake, it would make a lot of sense to implement this so that everyone participating can add an extra layer of security to their validators, whether they think they have been compromised or not.

Thank you to all who have put this proposal together.  Excellent work!  I hope to see this implemented.

---

**benjaminchodroff** (2022-07-20):

We have launched a website clwp[dot]xyz which documents the Consensus Layer Withdrawal Protection mechanism outlined in EIP-4736. While still under research, we intend to use Kleros as an optional way for any validator owner to be able to request setting their Withdrawal Address in the safest and fastest way possible, once supported. This helps provide optional security and may even prevent a compromised consensus layer seed phrase from resulting in the attacker being able to withdrawal the funds once validator withdrawals are supported.

Here is a proposed outline of how Kleros curated lists on both ETH mainnet and gnosis chains will be used to collect the change withdrawal address operations (still under development):

[![CLWP-5-2-3-2-Simple.drawio](https://ethereum-magicians.org/uploads/default/optimized/2X/6/659d18df49abc2396e49ffd4bf25362c38b90abc_2_302x500.png)CLWP-5-2-3-2-Simple.drawio502×831 95.3 KB](https://ethereum-magicians.org/uploads/default/659d18df49abc2396e49ffd4bf25362c38b90abc)

---

**benjaminchodroff** (2023-01-03):

I am writing a presentation on Consensus Layer Withdrawal Protection (CLWP) - an optional way for Ethereum validators to broadcast their set withdrawal address as early as possible to a social community of nodes. I’d greatly appreciate any feedback. [CLWP Overview - Google Slides](https://docs.google.com/presentation/d/1qV0NP2-5UZI51Ja7Vf_ANOR9AqIPvNpfuTzxbJVCn90/edit?usp=sharing)

---

**benjaminchodroff** (2023-01-12):

I have recorded a demo that documents what is EIP-4736 CLWP, and how to create a community submission on Github:

  [![image](https://i.ytimg.com/vi/EWkGyorgpAg/hqdefault.jpg)](https://www.youtube.com/watch?v=EWkGyorgpAg)

We have had 35 mainnet validator submissions since the new year, and growing daily. We welcome submissions from anyone and encourage every staker to set their withdrawal address as early as possible. We don’t mind if people do it with CLWP or just set it on their own node alone (instructions coming soon!), but please ***just get it done for your own protection***. Once Capella launches, there is no valid reason to run a validator without a withdrawal address set.

CLWP validator submissions for goerli and mainnet may be sent here:



      [github.com](https://github.com/benjaminchodroff/ConsensusLayerWithdrawalProtection/)




  ![image](https://opengraph.githubassets.com/6af1265ff1f9af7bf3e035d58d84b694/benjaminchodroff/ConsensusLayerWithdrawalProtection)



###



Contribute to benjaminchodroff/ConsensusLayerWithdrawalProtection development by creating an account on GitHub.

---

**souptacular** (2023-01-13):

I have some potentially valuable info on the history of these types of EIPs. I also have some thoughts on EIP-4736 specifically.

Many people would site EIP-999, the EIP that set out to recover stuck funds from the 2nd Parity multi-sig wallet failure, as an example of why there should not be recovery or various social fund recovery mechanisms for lost or stolen tokens. There is actually an older, more complicated, example of this idea.

[EIP-867: Standardized Ethereum Recovery Proposals](https://eips.ethereum.org/EIPS/eip-867) (February 2018) set out to develop a standardized format for different fund recovery requests. The EIP notes in the Simple Summary Section: " This EIP does not advocate for or against the acceptance of any particular recovery proposals, nor would its acceptance alone result in any state changes to the blockchain." There was discussion for this EIP on [GitHub](https://github.com/ethereum/EIPs/issues/866) and [EthMagicians](https://ethereum-magicians.org/t/eip-867-standardized-ethereum-recovery-proposals-erps/139/22). It basically didn’t go anywhere because it some people said that they didn’t want to set a recovery standard without the mechanisms in place, and proper buy in, to execute the recovery proposals submitted. An idea that was tossed around was having a counsel of trusted community members decide which ERPs should be honored. There was even discussion of who should be on the council and many people who were qualified were not interested due to the time sink and risk it would likely involve.

EIP-4736 has a noble goal, just like EIP-867. It sucks to have funds lost or stolen, especially when it involves validators because that generally means you lost a considerable sum of money, 32 ETH. There needs to be more empathy in the ecosystem around this in the form of brainstorming ways to prevent mistakes from happening. This does not mean that a recovery mechanism built into the Ethereum protocol or layers around the protocol are the answer. EIP-867 did have one category of ERP that was interesting to many. It said that if the lost coins could be computationally proved to be lost and belong to the user that would be applicable.

In December 2015, there was a bug in ethereumjs-utils (now web3.js I believe) where when an address was being generated, the wrong address could be derived from a private key. See [this forum post](https://wayback.archive-it.org/16516/20210622115240/https://forum.ethereum.org/discussion/3988/bug-in-ethereumjs-util) and [this Reddit post](https://www.reddit.com/r/ethereum/comments/47nkoi/psa_check_your_ethaddressorg_wallets_and_any/). This is something that could have been (and still could be) accomplished by proving you had the misderived key. Now that time has passed, it would be harder to get this type of recovery accomplished, but it still provides an example of where recovery is somewhat warranted in my opinion.

Ethereum strives to be both immutable and as unbiased as possible at the protocol layer when it comes to dapps and token allocations. If the worst dictator in the world has millions of ETH (and it is not affecting the health of the protocol) they should not be taken away from them because 95% of the world hates them or thinks they are evil. The exception to this is The DAO recovery, but time has shown this was a one time event that did not set a precedent. It was (arguably) necessary for a blockchain that was so young to make that choice for the good of the ecosystem, but now Ethereum is mature enough to steadfastly reject interventions at the protocol layer like that.

That is not to say 4736 is that entirely. It says that a lot of what it describes would need to be decided on by CL clients to implement. The issue is that for the specification to not get convoluted and introduce more complexity (which increases the chance of vulnerabilities) this EIP would need wide buy in from the community and core devs. I do not see that buy in currently and don’t anticipate it happening.

My top specific issues with the EIP are this:

1. It is unclear how many people would be affected by stolen or lost validator keys/staked ETH. I have seen people supporting EIP-4736 saying it is numerous people, but have never seen released estimates by anyone. If there is no way to even get rough estimates it comes into question if this EIP is worth the dev time, debate that will distract the community, and complicating the Ethereum spec.
2. The proposal seems to have a lot of things users have to to recover their funds. Are there UI mockups of what a webpage for recovery steps or clickable links to recover funds would look like?
3. Kleros court is not a good choice for arbitration of protocol layer issues. There are many reasons for this, and most of them do not have to do with how good/bad/effective Kleros court is in general (although I have heard bad things that are unresolved about favoritism and lack of transparency). The issues are:

a. If your EIP is implemented, a bad actor could effectively, and cheaply DDoS both Kleros court and the withdrawal protection system. The mock ups say Kleros court will make a decision in 7 days, but I doubt they will be able to handle tens of thousands of requests. If you do not believe it will be, at minimum, tens of thousands of requests, then the issue of lost/stolen funds in general for stakers is a very very small fraction of the total stakers.

b. Kleros has a token related to their system which would potentially put protocol developers and orgs in trouble by effectively integrating an org with a token who still has legal entities (isn’t fully decentralized). The regulatory challenges would be vast.

I am a big proponent of the belief that on-chain governance (like Polkadot) is ineffective and results in oligarchies. I am not sure the same would happen with Kleros, but there would be ample incentives to act maliciously as a Kleros juror or others involved in the system.

**Ethereum’s protocol and software that builds directly on top of and influences the protocol need to remain as neutral as possible to allow the most freedom of dapps and security/trust by the community.** EIP-4736 has good intentions, but is unfortunately not something I can see happening.

---

**benjaminchodroff** (2023-01-13):

Thanks for the feedback [@souptacular](/u/souptacular). Really appreciate the kind words. The good news it that until the Capella hard fork, no funds have been stolen since the operation is not yet allowed on chain. We have outlined suggestions that could further help - but they are purely optional to client teams. Regardless if they implement them, we believe CLWP will help the community.

We currently have 35 mainnet validator submissions received, and look forward to handling many more. Our biggest goal is to see every validator set their withdrawal address - we don’t mind if they do it themselves or use CLWP, we just want to see every validator set a withdrawal address for their own security as early as possible.

For CLWP, no additional time is required by the Ethereum devs to implement this EIP as it does not change consensus. Instead, it relies upon the community of willing participants to rebroadcast these valid signatures on their own nodes. We also have low latency bots and large custodial node operators who are helping.

1. We have been contacted by companies via https://clwp.xyz that have concerns on “hundreds” of validators due to bankruptcy cases facing recent large crypto-asset exchanges/businesses. While I would say the risk of these validators actually being compromised is low, nobody can have certainty until it is too late. No ethereum specification change is required to encourage setting the withdrawal address early.
2. Please see the above post on our github and youtube video. The ethereum withdrawal address specification changed yesterday so we have halted the CLWP github process but intend to launch an update once ethdo and staking-deposit-cli are updated accordingly. Stay tuned.
3. Kleros is purely optional. Use of a centralized github is equally acceptable, or anyone may make their own list - including hackers. Kleros is the best solution we could find that embraces decentralization but I fully agree with the concerns. There is no perfect solution that I could find.

Let the race begin ![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=12) We greatly appreciate all the help and consideration Ethereum Magicians, Ethereum R&D, ethstaker, flashbots, ETH Cat Herders, offchain, Kleros, Allnodes, and may volunteers have made. Regardless of the outcome, we hope CLWP helps everyone learn a little how to improve their security and set their withdrawal address early.

---

**poojaranjan** (2023-02-07):

[PEEPanEIP-4736: Consensus Layer Withdrawal Protection](https://youtu.be/C8rxSljl2PM) with [@benjaminchodroff](/u/benjaminchodroff)

  [![image](https://ethereum-magicians.org/uploads/default/original/2X/0/0bc7501ac4fc4cd380ad2b632d54f00615588374.jpeg)](https://www.youtube.com/watch?v=C8rxSljl2PM)

---

**benjaminchodroff** (2023-02-16):

Thank you, Pooja, we cannot thank you enough for what you do for the Ethereum community with ETH Cat Herders and PEEPanEIP.

As of this morning, we have received 566 mainnet validators using CLWP in our GitHub repository:



      [github.com](https://github.com/benjaminchodroff/ConsensusLayerWithdrawalProtection)




  ![image](https://opengraph.githubassets.com/bf56c5a8fa4cf8ff393620dec231cabb/benjaminchodroff/ConsensusLayerWithdrawalProtection)



###



Contribute to benjaminchodroff/ConsensusLayerWithdrawalProtection development by creating an account on GitHub.










Thankfully, no submissions have been contested. We do have [CLWP on Kleros](https://curate.kleros.io/tcr/1/0x479083b5343aB89bb39608e3176D750c8A6957B5) standing ready and able to help arbitrate any duplicate submissions using evidence such as signed messages from deposit address or fee recipient address.

We are still planning to accept early CLWP submissions until 2023/02/28, and we encourage anyone who has not stored their seed phrase offline and securely the entire time to use CLWP to set their withdrawal address.

