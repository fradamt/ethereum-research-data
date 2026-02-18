---
source: ethresearch
topic_id: 9555
title: Simple Withdrawal Credentials Rotation
author: gakonst
date: "2021-05-19"
category: The Merge
tags: []
url: https://ethresear.ch/t/simple-withdrawal-credentials-rotation/9555
views: 6739
likes: 11
posts_count: 10
---

# Simple Withdrawal Credentials Rotation

**Summary**

Eth2 validators may lose access to their withdrawal credentials, and as a result lose access to their 32 ETH deposit and inflation rewards. There is also no way to upgrade to new withdrawal credential types. We propose a protocol that allows rotating a validator’s withdrawal credentials.

**Context & Motivation**

In order to stake, a user sends 32 ETH to the Eth2 Deposit Contract, along with:

1. A BLS public key, used by their validator for producing blocks
2. A withdrawal credential (as specified here)

If a validator’s state is [Unslashed and Exitable](https://notes.ethereum.org/@hww/lifecycle#46-Step-6-Withdrawable), 27 hours later, they can withdraw their 32 ETH principal and any rewards earned to the withdrawal credentials’ address. Withdrawal credentials cannot be changed. If a validator loses access to their BLS withdrawal credentials, they are unable to reclaim their funds.

There’s a few potential pain points when managing BLS keys, which may result in loss of funds:

- Hardware wallets are not supported by the Deposit CLI, meaning that most validators’ credentials so far are on a mnemonic. Secure storage of mnemonics is hard.
- Individuals have reported losing access to their mnemonic, without having backed up their withdrawal credentials (anecdotal).
- Key management best practices suggest periodically rotating keys, which is not possible today.

The benefits from this feature are twofold:

- Security: Tooling around BLS is not mature yet, and key management is one of the most important problems to get right.
- Future Proofing: It’d make introducing new withdrawal credential types easier, since it’d provide an upgrade path for old credentials to migrate to the newer format (e.g. 0x02 keys for triggering from an eth1 contract)

**Protocol Description**

1. A transaction is submitted specifying new BLS withdrawal credentials for a validator’s public key, signed by the validator’s private key
2. A timer of T seconds starts.
3. One of following may happen:
4. If the owner of the withdrawal creds is not the person that initiated this transfer, they can veto it
5. If nobody responds after T seconds, the withdrawal credentials are updated.

**Implementation**

1. A simple way to implement this would be by introducing a new WithdrawalCredentialsRotation contract on Eth1, which would implement the protocol and emit an event which validators listen for. Once such an event is observed, the Beacon Node updates its validator object’s state to the event’s newly specified withdrawal credentials. If the pubkey specified does not match a validator, then the Beacon Node ignores that event.
2. Introduce a new OP_CHANGE_WITHDRAWAL_CREDENTIALS on the BeaconChain which would allow a validator to update their own credentials and a OP_CANCEL_WITHDRAWAL_CREDENTIALS_CHANGE which would allow the BLS withdrawal creds to cancel the update.

The T parameter can be set very high, e.g. on the order of 6 or 12 months.

**Risks & Tradeoffs**

Introducing any additional code in the consensus logic is an overhead that should be minimized. The above 2 solutions should be simple to implement, but if the community is supportive, we should investigate the consensus complexity which will be introduced and weigh it against the benefits.

A grieving vector is introduced whereby if a validator’s hot signing key is stolen, it can be used to force the withdrawal credentials to act before T is over. Ideally, if T is long enough, this should never be an issue.

**Deployment**

This update can be included in the BeaconChain hardfork after The Merge, when withdrawals will be enabled.

## Replies

**jgm** (2021-05-19):

It seems to me that ETH1 is the wrong place to be doing this due to interaction required between ETH1 and ETH2 to implement.  [Withdrawal credential rotation from BLS to Eth1](https://ethresear.ch/t/withdrawal-credential-rotation-from-bls-to-eth1/8722) is an alternative proposal that runs purely on ETH2, and allows withdrawal credentials to be set to an ETH1 address.  If that address is a smart contract it allows ultimate flexibility for control of withdrawn funds.

Are there any benefits, in your view, to the above proposal Vs the one I linked?

---

**ryanberckmans** (2021-05-19):

The usefulness of this proposal makes sense to me.

Yet, I’d be strongly opposed to any mechanism that may circumvent the property rights of withdrawal credential holders.

The proposal that Jim linked mentions “if authenticated by the current withdrawal credential holder”, which seems to be a categorically different type of proposal that maintains withdrawal property rights.

---

**gakonst** (2021-05-19):

Thanks for the thoughts [@ryanberckmans](/u/ryanberckmans) [@jgm](/u/jgm). Comments inline below:

![](https://ethresear.ch/user_avatar/ethresear.ch/jgm/48/25_2.png) jgm:

> Are there any benefits, in your view, to the above proposal Vs the one I linked?

The benefit is that this proposal would also allow a validator that’s lost access to their withdrawal creds to recover them. I view this as complementary to Vasiliy’s proposal.

![](https://ethresear.ch/user_avatar/ethresear.ch/ryanberckmans/48/1499_2.png) ryanberckmans:

> Yet, I’d be strongly opposed to any mechanism that may circumvent the property rights of withdrawal credential holders.

Agreed. As I wrote on [twitter](https://twitter.com/gakonst/status/1395090078087659524), it may be worth allowing validators to override the default T with a T’ of their choice (instead of locking them in a T which they may believe to be too short).

---

**jgm** (2021-05-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/gakonst/48/1101_2.png) gakonst:

> The benefit is that this proposal would also allow a validator that’s lost access to their withdrawal creds to recover them.

There are many situations today where the holders of the validator key and withdrawal key are different entities.  What you call a benefit is also a mechanism to dispossess legitimate but unwary users of their funds.

The only entity that should be able to change withdrawal credentials is the holder of the key represented by the withdrawal credentials.  Time locks are not an acceptable substitute for the guarantees provided by sole possession of the relevant key.

---

**ryanberckmans** (2021-05-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/gakonst/48/1101_2.png) gakonst:

> Agreed. As I wrote on twitter, it may be worth allowing validators to override the default T with a T’ of their choice (instead of locking them in a T which they may believe to be too short).

That’s a good idea to vary T per validator.

However, I’m still not in favor of this proposal. It seems to create a sort of slippery slope where the property rights of withdrawal credential holders would go from being absolute to a grey spectrum of guess-and-check and various failure modes or footguns.

---

**NicolasMassart** (2021-05-21):

I’m not in favour of this proposal either.

The risk for stacker who are running validators on a cloud service and only hold the withdrawal keys is not acceptable.

Losing keys is hard and I hope it will not affect too many people. But this is the life of crypto owners. It’s the same as loosing a bill…

A delay system doesn’t mitigate the risk when you don’t have any access to the validator node. The best to me would be to have more tools to handle BLS keys from a seed and be able to secure them as Eth1 keys.

---

**vshvsh** (2021-05-22):

I’m tentatively in favor of something like that proposal - as something temporary, not a long term mechanism.

Tooling around Beacon Chain key handling was, indeed, pretty bare-bones at launch. Still is, to an extent. Anecdotically, some people did lose their withdrawal credentials, and some other would want to rotate it to a safer key management tool. To acknowledge that, let people rectify the consequences of that and, in a year or so, when the tooling is mature, to close that window, would be prudent IMO.

---

**lsankar4033** (2021-05-27):

I think it’s pretty clear that disenfranchising either key (withdrawal cred or validator key) is not a great idea, so perhaps this scheme isn’t worth exploring as a way to handle withdrawal cred loss.

However, a modification of this proposal where signatures from *both* the withdrawal credential key and validator key are required for rotation would allow us to update withdrawal creds for other reasons (i.e. the existence of new, more fully featured prefixes).

I strongly feel that the option to ‘upgrade’ withdrawal creds should exist and a new canonical ‘WithdrawalCredentialsRotation’ contract seems like a clean way to do it.

---

**yoavw** (2021-07-19):

As many have noted, there are issues with the current proposal.  And it also creates an incentive to kill validators along with their owners. ![:crazy_face:](https://ethresear.ch/images/emoji/facebook_messenger/crazy_face.png?v=9)  Kill the owner, wait T seconds, withdraw 32 ETH.  Some people kill for less.

Recent events demonstrated that some countries take action against miners.  If you’re [under arrest](https://www.thenationalnews.com/business/energy/2021/07/19/malaysia-steamrolls-1069-bitcoin-mining-machines-after-owners-stole-energy) and your validator can’t veto on your behalf because it is [under a steamroller](https://youtu.be/c_tcg9kOfkg), then anyone can grab your stake before you are released.

We could come up with all sorts of schemes to mitigate this.  Social recovery, guardian nodes, etc.  But my suggestion is that instead of a one-size-fits-all solution, we allow delegating it to a contract.

Allow validators to specify a contract address instead of a withdrawal key.  The contract may be a simple ownable proxy that checks a signature while still allowing key rotation through changeOwner(), or it could be a multisig, or even a contract wallet supporting social recovery.

The deposit contract remains unopinionated about recovery methods.  After the merge, the stake can be withdrawn via the validator’s contract according to its logic.

