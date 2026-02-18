---
source: magicians
topic_id: 8674
title: Idea Improve client diversity by imposing penalties for using majority client(s)
author: ronaldjmaas
date: "2022-03-21"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/idea-improve-client-diversity-by-imposing-penalties-for-using-majority-client-s/8674
views: 509
likes: 1
posts_count: 3
---

# Idea Improve client diversity by imposing penalties for using majority client(s)

Although multiple clients are available for both the execution layer and consensus layer, there is a large disperity between in market share of the various clients. E.g. 85% of nodes use Geth for the execution layer and 67% of nodes use Prysm for consensus layer. For a healthy and robust Ethereum network we need each client to be below 33% market share in order to mitigate the risk of accepting invalid blocks caused by an implementation bug in a client.

Superphiz from the Ethstaker community has expressed these concerns on his Youtube channel better than I can explain in a post.

My proposal is to have a relatively small penalty (e.g. 5-10%) in the rewards to help nudge node administrators to switch from using a majority client to a minority client. Only when market share of all clients are below the threshold of 33% then the penalty mechanism will be deactivated as long as the respective market share across the various clients remain balanced.

So for this mechanism to work a number of changes need to be realized:

- Each client advertizes both the execution layer and consensus layer client types (such as Geth+Lighthouse, Besu+Teku, etc.) on the p2p network on a daily basis.
- Each consensus layer client keeps track of which client types are used per validator. Note validators may have deposited more than 32 ETH and this should be taken in account.
- Consensus layer client must impose a penalty for each validator that uses a majority client. If a validator uses a majority client for both the execution layer and the consensus layer, then the penalty imposed will double. A simple mechanism to impose a penalty is delaying the inclusion of a  percentage of attestations by 1 block in the epoch.

Hope to receive some feedback from the community on this proposal. Like to have your thoughts if it is meaningful to add such a mechanism to the Ethereum protocol, or if there are better / easier means of addressing client diversity.

Full disclosure: I run a validator node using the Geth+Lighthouse combo. So unless I change my execution layer client, I will get penalized if this is implemented.

## Replies

**timbeiko** (2022-03-21):

There is no way to prove which client is run by whom. At best, we have some simple heuristics (e.g. didn’t change the `graffiti` value, correlations around staking deposits, etc.) but this unfortunately isn’t explicit enough to base protocol rules on. That said, there are already anti-correlation penalties in the protocol, so if a majority client has an issue which leads to slashing, the penalties will be higher if that client represents a larger % of the network. This spreadsheet gives an example: [PUBLIC - Client diversity Ethereum Eth2 financial modelling - Google Sheets](https://docs.google.com/spreadsheets/d/12R8wkuv62hZyajrhhlkNrskkwH2-zjYZjXKkHJuxGQc/edit)

---

**ronaldjmaas** (2022-03-22):

Agree there is currently no reliable way to determine client type. In order to do that it will require a change in the current p2p chatter. Either by amending an existing message type or by defining a new message type specific for that purpose.

The anti-correlation penalties will work fine when no client is able to achieve the treshold of 67% of required attestations on its own. So in case a validator using the majority client proposes an incorrect block and then that block is accepted as valid by the other validators using the same majority client, then this block will be added to the chain once 67% of the validator nodes attest it is correct. Even worse if proposers using other clients will get slashed by producing correct blocks that are rejected by the majority client.

If this scenario is extremely unlikely but still possible then I think we should find a way to address it. My original post suggest one mechanism I think that can achieve that. But there are maybe better / easier / less intrusive ways to accomplish the same.

