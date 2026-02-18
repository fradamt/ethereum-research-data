---
source: magicians
topic_id: 3415
title: "[ERC-2159] Common chain metrics"
author: ajsutton
date: "2019-06-27"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/erc-2159-common-chain-metrics/3415
views: 4587
likes: 4
posts_count: 18
---

# [ERC-2159] Common chain metrics

EIP: http://eips.ethereum.org/EIPS/eip-2159

I’ve found it very useful to be able to monitor a group of Pantheon nodes using Prometheus metrics and a Grafana dashboard (https://grafana.com/dashboards/10273 specifically).  With Geth 1.9 also adding a Prometheus endpoint to expose its metrics, it seems like it would be worthwhile agreeing on standard names for a few of the core metrics like current chain height and peer count. It’s a minor thing but makes it easier to use a single dashboard to monitor nodes using different clients. I’ll write this up as an informational EIP if no-one screams too loudly.

Eth 2.0 an informative spec for metrics at https://github.com/ethereum/eth2.0-metrics/blob/master/metrics.md though I’m inclined to be even less prescriptive and basically just define the metrics, omitting anything about how to configure the client.

I’d suggest metrics for:

- Current chain height: ethereum_block_number
- Best known block number (similar to highestBlock from eth_syncing JSON-RPC but would be the current chain head when not syncing rather than null): ethereum_best_known_block_number
- Current peer count: ethereum_peer_count

Them names for metrics around CPU and memory usage tend to be pretty standard so those metrics enable almost the entire dashboard I’ve been using which is a really nice overview.

You can generate quite a useful dashboard with just those.  There are also some for fast sync (pivot block, number of times pivot block change, downloaded world state, known world state remaining) which may be worth setting some standard names for even though they won’t apply to every client.

And there will always be a ton of very client specific metrics which we shouldn’t even attempt to standardise.

## Replies

**tkstanczak** (2019-06-28):

We have hundreds of metrics that we send from Nethermind to Prometheus. Will post the list here later so maybe they will be an inspiration for some more detailed tracking. Will be glad to see your lists too.

---

**ajsutton** (2019-06-30):

Pantheon publishes quite a few but currently doesn’t make any promises about any of them being stable.  I think the ones above are the most useful to provide stable names for and making them consistent across clients would be useful. They are also the ones I’ve heard from clients are useful (or been directly requested by clients).

Other possible options are number of network messages received (by type), counts of different disconnect reasons but I think this are more likely to be used to work out why something isn’t going well rather than just the high level overview.  Once you get to that level you’re well into client-specific land anyway.

Example Pantheon metrics from one deliberately very under-powered box are in https://gist.github.com/ajsutton/09535958828b4b2a1a1f7da8f8d865e2 if you’re interested.

---

**ajsutton** (2019-07-01):

Drafted an Informational EIP at: https://github.com/ethereum/EIPs/pull/2159

---

**axic** (2019-07-01):

[Left a question](https://github.com/ethereum/EIPs/pull/2159#discussion_r299227797) on the pull request:

> So is this an ERC, Interface or Informational?
>
>
> Is this proposing that clients when integrating with Prometheus should use the names below? What does integrating with Prometheus means?
>
>
> In short: does this proposes something clients would implement or is this implemented by third parties when integrating a client into Prometheus?

---

**ajsutton** (2019-07-01):

Thanks for the rapid review.  I left this on the PR as well but for people following along here:

This is something that clients would implement, but exactly how they integrate with Prometheus is up to them - there are a few ways a client and Prometheus could be configured to work together and no real benefit in trying to standardise it.

What is useful is if a client is sending metrics to Prometheus (via whatever means), that these few properties have the same names and meanings.  Then you can create a dashboard like https://grafana.com/api/dashboards/10273/images/6473/image to monitor groups of nodes.

I’m not exactly sure what category this should go under.  Interface is a possibility and would definitely be the case if it were standardising how to integrate with Prometheus.  I’ve put it as Informational here because its essentially a recommended convention. It’s not trying to be the definitive spec on metrics for clients and its entirely optional whether clients choose to support it or not. It’s just a little more convenient if they do.

I don’t mind which category it winds up in though.

---

**axic** (2019-07-02):

Can you include ERC-2159 in the title and http://eips.ethereum.org/EIPS/eip-2159 in the top comment?

---

**ajsutton** (2019-08-15):

I’ve moved this EIP to last call.  We’ve shipped Pantheon with these new metric names.  Would love to get other clients to adopt them as well.

---

**fulldecent** (2019-08-21):

**Inline links should be moved to the bottom of the document.**

Please see ERC-721 as an example.

**References should be provide to explain/prove**

- What is a Prometheus Metrics Names?
- “Many Ethereum clients expose a range of metrics in a format compatible with Prometheus” – which clients? For an example which specifically names existing prior art, please see ERC-721.

**The backwards compatibility section is underspecified**

- Clients may already be publishing these metrics using different names – please research and list the names of the clients that are represented.
- Assertions are made on behalf of other implementations: “Clients that want to avoid this incompatibility can expose the metrics under both the old and new names.” However no other clients are referenced and nobody is available to retort this statement.

**Summary**

In general this EIP is a prescription written by one vendor to specify “here is how I am doing something, other people may be doing it differently, they should change”. However the EIP process is designed to identify existing implementations, expose backwards incompatibilities with those implementations. No identities are provided for these other affected parties and so it is impossible for me to reach out to them for comment.

At this time, for the reasons above, I believe this document is proper to be published as a technical note for the vendor’s product documentation, but it does not meet the technical acceptability standards to be published as a final EIP standard.

---

**ajsutton** (2019-08-21):

Thanks for the feedback. I will address each point separately below but mostly these seem to boil down to needing a list of Ethereum clients which I don’t believe should be required in an EIP. For example the Chain ID opcode spec being included in Istanbul and in final status makes no attempt to list the clients which would be required to implement it or which have previously implemented a EIP-155 chain ID.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fulldecent/48/8663_2.png) fulldecent:

> Inline links should be moved to the bottom of the document.

Is there a particular reason for this? I’m unable to find any such requirement for EIP formatting and it reduces readability by separating the links from the content they apply to.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fulldecent/48/8663_2.png) fulldecent:

> What is a Prometheus Metrics Names?

There is a link provided to the Prometheus website which provides additional information and documentation. However, it seems reasonable to expect at least a minimum level of understanding of Prometheus here and is clearly understandable when reading the EIP in full.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fulldecent/48/8663_2.png) fulldecent:

> “Many Ethereum clients expose a range of metrics in a format compatible with Prometheus” – which clients? For an example which specifically names existing prior art, please see ERC-721.

This is in the abstract with the intention of explaining what the EIP is about and why it would be useful. I’m not quite sure how the EIP is improved by specifically listing those clients.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fulldecent/48/8663_2.png) fulldecent:

> Clients may already be publishing these metrics using different names – please research and list the names of the clients that are represented.

The aim of this section is to identify potential backwards compatibility issues, which this statement does by itself. Claiming that no clients are affected by the issue would need to be justified, but merely pointing out the potential compatibility issue doesn’t need further justification, it is simply a statement of fact.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fulldecent/48/8663_2.png) fulldecent:

> Assertions are made on behalf of other implementations: “Clients that want to avoid this incompatibility can expose the metrics under both the old and new names.” However no other clients are referenced and nobody is available to retort this statement.

As mentioned above, I don’t believe the EIP needs to provide a list of Ethereum clients.  The point of final call is to raise the level of attention so that any technical concerns can be raised. If you are aware of reasons this would not mitigate the backward incompatibility that would be good to hear.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fulldecent/48/8663_2.png) fulldecent:

> In general this EIP is a prescription written by one vendor to specify “here is how I am doing something, other people may be doing it differently, they should change”.

I believe this is an unfair characterisation of this EIP. The EIP was inspired by the [ETH2 beacon chain metrics spec](https://github.com/ethereum/eth2.0-metrics/blob/master/metrics.md) and is not simply a listing of the metrics that Pantheon exposed. Pantheon metrics had to be changed to match this EIP.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fulldecent/48/8663_2.png) fulldecent:

> At this time, for the reasons above, I believe this document is proper to be published as a technical note for the vendor’s product documentation, but it does not meet the technical acceptability standards to be published as a final EIP standard.

The issues you’ve raised appear to be entirely editorial in nature.  There’s no concern raised that suggests the spec is insufficient for clients to implement, no additional backwards compatibility concerns raised etc.

I certainly agree that for this EIP to actually have value it needs to be widely adopted by clients, but publishing a technical note in a single client’s documentation can’t achieve that. It requires a common specification that can be pointed to and clients can follow which is what EIPs are designed to achieve.

---

**fulldecent** (2019-08-21):

**Inline links should be moved to the bottom of the document.**

The EIP editors have asked me to make this change. You can find this in the discussion of ERC-721 (which also spans into PR 841).

**What is a Prometheus Metrics Names?**

Will you please provide a link to explain what Prometheus Metrics Names are?

**Many Ethereum clients expose a range of metrics in a format compatible with Prometheus**

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ajsutton/48/1102_2.png) ajsutton:

> I’m not quite sure how the EIP is improved by specifically listing those clients.

This EIP draft is of type “Standard Track”, subtype “Interface”. Interfaces affect multiple clients and therefore those clients should be listed. This is the way that backwards compatibilities can be discussed.

**Clients may already be publishing these metrics using different names – please research and list the names of the clients that are represented.**

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ajsutton/48/1102_2.png) ajsutton:

> merely pointing out the potential compatibility issue doesn’t need further justification, it is simply a statement of fact.

This statement assumes that other clients (hitherto unknown) are able to publish metrics multiple times under different names without problem. This might be a reasonable assertion to make (you can include it), but no actual clients are mentioned.

**Assertions are made on behalf of other implementations**

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ajsutton/48/1102_2.png) ajsutton:

> If you are aware of reasons this would not mitigate the backward incompatibility that would be good to hear.

It is not possible for me or anybody to evaluate the backwards incompatibility issues based only on the information in the EIP because there is insufficient references to prior art to be backwards incompatible with.

In other words, the EIP does not stand on its own. This is a technical deficiency of complying with the EIP process and is grounds to not promote to final status.

**In general this EIP is a prescription written by one vendor to specify…**

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ajsutton/48/1102_2.png) ajsutton:

> The EIP was inspired by the ETH2 beacon chain metrics spec

Good point. My note there is retracted.

**does not meet the technical acceptability standards to be published as a final EIP standard**

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ajsutton/48/1102_2.png) ajsutton:

> The issues you’ve raised appear to be entirely editorial in nature

Correct. Because existing implementations are not reviewed, it is not possible for me to do a deeper analysis.

---

Just want to be clear here. I think you’re doing a good job with this. My interest here is that high editorial standards are upheld with EIPs. I’m not just a critic, I am also lead author of ERC-721, and contributor to other publications here, not all including my name.

---

**ajsutton** (2019-08-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fulldecent/48/8663_2.png) fulldecent:

> Just want to be clear here. I think you’re doing a good job with this. My interest here is that high editorial standards are upheld with EIPs. I’m not just a critic, I am also lead author of ERC-721, and contributor to other publications here, not all including my name.

Thank you, your input is valuable I’m just keen to work through it and understand the reasoning behind it, particularly where it deviates from other EIPs that I’ve implemented while developing Pantheon. Apologies if my responses come across as adversarial, I don’t intend them that way.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fulldecent/48/8663_2.png) fulldecent:

> Inline links should be moved to the bottom of the document.
>
>
> The EIP editors have asked me to make this change. You can find this in the discussion of ERC-721 (which also spans into PR 841).

Interesting, because the inline links haven’t just slipped through in this EIP, an editor actually flagged that one was broken when reviewing the original draft.  There are quite a few final EIPs that use inline links (EIP-165, EIP-137, EIP-6, EIP-1167, EIP-1344, EIP-1283 and interestingly ERC-1155 does it both ways).  I’ve brought it up in the EIPs Gitter mostly because it seems like it would be useful to have a clear style guide to point to.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fulldecent/48/8663_2.png) fulldecent:

> Will you please provide a link to explain what Prometheus Metrics Names are?

I’m happy to provide additional information but I must admit I’m rather struggling to know how to explain it any further without just sounding contrite.  A Prometheus Metric Name is the name assigned to a metric reported to Prometheus.  But that’s essentially what the simple summary already says. Admittedly that section has not come through the editing process particularly well. It should, and has been fixed to, read:

Standardized names of common metrics for Ethereum clients to use with Prometheus, a widely used monitoring and alerting solution.

If that’s insufficient, could you propose some wording that would make it clearer?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fulldecent/48/8663_2.png) fulldecent:

> It is not possible for me or anybody to evaluate the backwards incompatibility issues based only on the information in the EIP because there is insufficient references to prior art to be backwards incompatible with.
>
>
> In other words, the EIP does not stand on its own. This is a technical deficiency of complying with the EIP process and is grounds to not promote to final status.

I think this is the crux of the desire to list clients, but I believe the logic is flawed.  Reasoning about backwards compatibility shouldn’t be based only on the information in the EIP, and it isn’t for other EIPs. Where there are known backwards compatibility issues, they are listed in the EIP but the review of the EIP necessarily uses outside knowledge to determine if there are other potential compatibility issues which have been missed.

EIP-1 does not require an EIP to include a complete list of implementations that may be affected, merely to identify a description of any backwards compatibility:

From EIP-1:

> An EIP must meet certain minimum criteria. It must be a clear and complete description of the proposed enhancement. The enhancement must represent a net improvement. The proposed implementation, if applicable, must be solid and must not complicate the protocol unduly.

and:

> Backwards Compatibility - All EIPs that introduce backwards incompatibilities must include a section describing these incompatibilities and their severity. The EIP must explain how the author proposes to deal with these incompatibilities. EIP submissions without a sufficient backwards compatibility treatise may be rejected outright.

Notably, the description of the proposed enhancement has to be complete, but the backward compatibility section simply lists the incompatibilities, not a complete list of clients which might implement or be affected by the change.  You can see this in practice by how rarely clients other than Parity and Geth are mentioned despite the fact that they are heavily affected by a huge range of EIPs and even Parity and Geth are typically only mentioned as clients that have implemented the changes.

---

**ajsutton** (2019-08-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ajsutton/48/1102_2.png) ajsutton:

> Interesting, because the inline links haven’t just slipped through in this EIP, an editor actually flagged that one was broken when reviewing the original draft. There are quite a few final EIPs that use inline links (EIP-165, EIP-137, EIP-6, EIP-1167, EIP-1344, EIP-1283 and interestingly ERC-1155 does it both ways). I’ve brought it up in the EIPs Gitter mostly because it seems like it would be useful to have a clear style guide to point to.

After some discussion on gitter, it seems the trend is towards a references section and no inline links. I’ve updated the EIP to match.

---

**fulldecent** (2019-08-27):

**Inline links should be moved to the bottom of the document.**

Resolved.

**Will you please provide a link to explain what Prometheus Metrics Names are?**

That works great, thank you.

**insufficient references to prior art to be backwards incompatible with**

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ajsutton/48/1102_2.png) ajsutton:

> EIP-1 does not require an EIP to include a complete list of implementations that may be affected, merely to identify a description of any backwards compatibility:

I believe a minimum standard to decide if a potential backwards compatibility shall have been properly described is:

“A competent person can read the notes on backwards compatibility, skim any references, and be confident that the author has sufficiently considered dealing with prior art.”

I have briefly researched the topic and found this reference. If you believe it’s relevant, you are welcome to include it.



      [github.com](https://github.com/4ops/ethereum-exporter/blob/cf4dd278ef910332ea577a391a2e5d7dfc22e15f/examples/metrics-geth.txt)





####



```txt
# HELP ethereum_exporter_errors Errors counter.
# TYPE ethereum_exporter_errors counter
ethereum_exporter_errors 0

# HELP ethereum_is_syncing Is node syncing.
# TYPE ethereum_is_syncing gauge
ethereum_is_syncing 0

# HELP ethereum_starting_block The block number where the sync started.
# TYPE ethereum_starting_block gauge
ethereum_starting_block 0

# HELP ethereum_current_block The block number where at which block the node currently synced to already.
# TYPE ethereum_current_block gauge
ethereum_current_block 0

# HELP ethereum_highest_block The estimated block number to sync to.
# TYPE ethereum_highest_block gauge
ethereum_highest_block 0

```

  This file has been truncated. [show original](https://github.com/4ops/ethereum-exporter/blob/cf4dd278ef910332ea577a391a2e5d7dfc22e15f/examples/metrics-geth.txt)

---

**fulldecent** (2019-12-01):

Progress in this Last Call review has arrested. I request that this EIP please be reverted to Draft status.

Right now we have many important EIPs entering Last Call which ends imminently and which will be deployed on mainnet as consensus changes which have already been announced. EIPs like this one one should be considered again. But at the minute I hope this can be remove from the review backlog. And quickly.

---

**ajsutton** (2019-12-01):

I disagree, the only open concerns are whether the backwards compatibility should be further fleshed out to find all prior art or not. There aren’t currently any reasons to believe substantive changes will be required so Last Call is still appropriate.

There are also no limits on the number of EIPs in last call and no relation between the Istanbul EIPs and this one so no reason for them to affect this EIP’s status.

---

**MicahZoltu** (2020-07-25):

What is the reason this is still in Last Call and not Final?  It doesn’t appear there has been any movement on it for over 7 months, suggesting that it either has been Abandoned or is Final.  Reading above, it appears there was some feedback around Backward Compatibility, and while EIP authors are encouraged to heed community and editor feedback I don’t believe this particular feedback is a blocker for merging to Final if the author decides to.

[@ajsutton](/u/ajsutton) Can you submit a PR to move this to either Final or Abandoned?

---

On a personal note (not as an Editor) I think the backward compatibility section is fine in general.  There may be value in mentioning the possibility that a client is exposing one of the metrics but with a different meaning, perhaps with a recommendation on how to transition between the previous definition and the new definition.

---

**ajsutton** (2020-07-25):

It got stuck in last call because of the disagreement between what the backwards compatibility section had to cover off.  These metrics have been in use in Besu for a long time now and I can’t see anything changing. Similarly though there hasn’t been any great interest in other clients adopting this approach either which I think is a shame but respect that it’s not a priority for them and/or just not worth the disruption to users to change the metric names.

Since it is in use I think Abandoned would be misleading so I’ll raise a PR to change it to final.

