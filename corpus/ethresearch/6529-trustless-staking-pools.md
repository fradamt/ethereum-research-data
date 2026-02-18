---
source: ethresearch
topic_id: 6529
title: Trustless Staking Pools
author: liochon
date: "2019-11-29"
category: Sharding
tags: []
url: https://ethresear.ch/t/trustless-staking-pools/6529
views: 2707
likes: 3
posts_count: 7
---

# Trustless Staking Pools

Today a validator must remain connected and secured against hacking: a hacker could disconnect a node from the network or lead the validator to sign invalid blocks, making it slashable. Remaining connected can be problematic for some countries. [Iran recently cut its Internet connection for 5 days](https://netblocks.org/reports/internet-restored-in-iran-after-protest-shutdown-dAmqddA9). It’s generally accepted that China [could cut its Internet network](https://www.zdnet.com/article/oracle-chinas-internet-is-designed-more-like-an-intranet/) from the rest of the world as well. Russia [is also aiming at this](https://www.businessinsider.fr/us/russia-sovereign-internet-law-cut-web-access-censorship-2019-11). A possibility for these users is to join a staking pool. The staking pool will take of the connectivity and security. However, it is not a trustless solution: the staker has to trust the staking pool. While it is possible to ensure that the staking pool cannot unlock the funds, the staking pool can still lose all the funds because of the slashing & leaking mechanisms: the staking pool can have bugs or can be hacked. Moreover the staking pool must remain up and cannot cut its services for 2 weeks like an [exchange can](https://upbit.com/service_center/notice?id=1085) when something goes wrong. We can also imagine a staking pool threatening its users to be voluntary slashed if they don’t pay a fee.

In other words, it would be great if a user could stake its funds without having to trust the staking pool, regardless of what happens. The staking pool would take the risks (i.e. slashing/leaking/hacking) for the user against a cut on the rewards.

This can be implemented with a protocol change which adds 3 mechanisms:

1. The staker’s funds are locked, but the staking pool does not have access to these funds. Only the staker can unlock these funds (with a long delay as today).
2. The funds slashed/leaked are not the funds locked but funds owned by the staking pools.
3. There is ratio between locked funds and slashable funds. That corresponds to a leverage effect. 1% seems economically reasonable. If there are more locked funds than leveraged slashable funds only the first locked funds are used for slashing.

To illustrate, we can imagine a scenario like this one:

|  | Locked funds | Slashable funds |
| --- | --- | --- |
| Initial start: 1000 users | 32000 (32 *1000) | 320 (32*1000 *0.01) |
| Event: 1 validator in the pool is slashed with many others from other pools, hence get slashed by 32 ETH. | 32000 | 288 (320-32) |
| Now the mining pool has only 900 validator slots (288 / .32) |  |  |
| Event: the staking pool transfers 112 ethers to the slashable funds wallet. | 32000 | 400 |
| Now the mining pool has 1000 validator slots again. |  |  |
| Event: The mining pool stops participating for 1 day. | 32000 | 398 (400-0.002 * 1000) |
| Event: The mining pool is hacked and use its validating power to create slashable conditions. | 32000 | 0 (max (0, 398-1000*32) |

There are two impacts:

- The number of validators can vary a lot because of the leverage.
- The cost of acting badly is divided by 100 for a mining pool. Has it really an impact? That’s doubtful.

We can compare this to today’s mining pools: one can buy a set of GPUs and participate in a mining pool:

|  | GPU Mining | This staking |
| --- | --- | --- |
| Investment | A set of GPUs | 32 ETH |
| Infrastructure | Network / Site | No infra |
| Daily cost | Electricity | 0 |
| Financial risk if the pool misbehaves | Electricity + Amortization of the GPUs | 0 |
| Daily to leave the pool (for example if the pool misbehaves) | No delay | Months |

Of course, anything that helps staking pools could be suspected of pushing for centralization. But with this mechanism anyone can create a staking pool, as the participants are not taking any risk by joining a staking pool without an established reputation.

## Replies

**jgm** (2019-11-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/liochon/48/1028_2.png) liochon:

> There is ratio between locked funds and slashable funds. That corresponds to a leverage effect. 1% seems economically reasonable. If there are more locked funds than leveraged slashable funds only the first locked funds are used for slashing.

Surely this would cause everyone to create their own pool even if they were a single staker, as it reduces their exposure if they are slashed to 1% of what it would be otherwise.  Which would in turn reduce the effectiveness of the anti-slashing measures by 99%.

---

**Daraz1** (2019-12-01):

What is the GPUs set to be?

---

**liochon** (2019-12-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/daraz1/48/4260_2.png) Daraz1:

> What is the GPUs set to be?

It’s a comparison with a Ethereum 1 miner who use GPUs to contribute to a mining pool.

---

**liochon** (2019-12-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/jgm/48/25_2.png) jgm:

> Surely this would cause everyone to create their own pool even if they were a single staker, as it reduces their exposure if they are slashed to 1% of what it would be otherwise.

Of course. But they will still be removed from the validator set. There can be a difference between the amount staked and the amount at risk. Actually, IIRC it’s already the case: if you stop participating you will leak until you get to 16 ETH. You don’t have to slash the whole stake.

---

**Daraz1** (2019-12-02):

Hashrate doesn’t matter? Is there a minimum requirement?

---

**liochon** (2019-12-02):

I’m not sure I understand the question. In Ethereum 1 the hash rate impacts the rewards (but I don’t consider the rewards in this post). In Ethereum 2, as it’s a full proof-of-stake system there is no hash rate.

