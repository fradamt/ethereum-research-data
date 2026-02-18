---
source: magicians
topic_id: 14195
title: "EIP-7002: Execution layer triggerable exits"
author: djrtwo
date: "2023-05-09"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-7002-execution-layer-triggerable-exits/14195
views: 8199
likes: 26
posts_count: 27
---

# EIP-7002: Execution layer triggerable exits

Discussion topic for EIP-7002

https://github.com/ethereum/EIPs/pull/7002

## Replies

**petertdavies** (2023-05-10):

I have two big opinions on the EIP.

Firstly, I think rather that specifically having an “Exit Validator” precompile, we should instead have a “Send Message to Consensus Layer” precompile. It’s entirely possible that we will want the EL to send different kinds of message and it would be annoying to have to add a precompile every time we want to add a new message type. We should also allow messages to carry Ether so we can do things like having new ways to initialise a validator. This gives us a broad scope to make EL-to-CL interaction changes without updating the EL at all.

Secondly, I’m really confused why this is a precompile, rather that just a smart contract with some special handling rules (if it emits a log put it in the header). The entire logic of the precompile is the sort of accounting computation that is the bread and butter of smart contracts and it seems pointlessly wasteful to make every EL client include a bunch of special case code for it when it could be implemented in Solidity once.

---

**djrtwo** (2023-05-10):

I’m hesitant to implement a general messaging bus here. It’s not clear to me that we will have a proliferation of messages beyond deposits and exits, and designing generically to try to predict such cases – and handle them appropriately on CL – is a large undertaking with unclear value proposition.

With this message type, validators can now be fully controlled – they can enter and exit the mechanism. And they can have arbitrary logic for performing both as well as governing/updating ownership via smart contracts.

As for the second, I am extremely hesitant to utilize a system-level contract like the deposit contract. This was a good choice at the time, but going this path carries quite a bit of social baggage. For example, we’ve discussed potentially modifying the deposit contract logic in proposals and gotten *very* strong pushback that you can’t modify smart contract code as it is an irregular state change akin to the DAO. I see this strongly as a false equivalence but it is certainly a real thing to contend with.

Also, a smart contract here would still need special update logic to manage the message queue at the end of the block as currently specified. Just emitting a log was considered and rejected in our design process because you have no bound to messages going into CL other than the gas limit. Utilizing the in-state queue with the post-TX updates allows for managing the load from EL to CL (and on the size of block body due to the messages)

---

**Wander** (2023-11-30):

I wanted to make a record of a conversation we had at DevConnect 2023 about the potential for an additional “priority queue” for EL-induced exits (thanks to [@SnapCrackle2383](/u/snapcrackle2383) for bringing together all the tech leads from various staking protocols).

This all started because [@OisinKyne](/u/oisinkyne) had a great idea to give 7002-based exits priority over the current exit queue. This is useful for LST protocols which would benefit from better liquidity guarantees and will need to use this mechanism for safety anyway. Processing only up to some portion (half?) of the maximum exits per block from this “priority queue” would prevent anyone from using this to grief users in the “free queue”.

My tweak of this suggestion is a fee market for determining placement in the priority queue. That is, if I attach more gas to my EL exit, I can get priority ordering over someone who paid less. Practically speaking, this could help fight stETH dominance in LSTfi protocols such as Liquity v2 and [Gravita](https://www.gravitaprotocol.com/). Currently, they have to give preferential treatment (higher LTVs, lower fees, etc) to LSTs with higher liquidity, but with this idea, they could support low-liquidity LSTs in the same way as high-liquidity LSTs, just with the potential for higher fees on redemption during obscure network conditions. Speaking of those conditions, simply skipping the returning of excess gas would effectively burn ETH when market instability leads to bidding wars on this priority queue.

I will be the first to admit that this is all a bit complicated, and the ideas above would certainly benefit from more modeling and consideration, especially for what could happen during correlated slashing or inactivity leaking. I do think any actual changes to 7002 would be relatively small, however, and the ecosystem benefits would be large. Staking concentration is on everyone’s mind at the moment, and I’d love to find a way to empower smaller LSTs with 7002-style exits.

---

**eawosika** (2024-01-09):

Hi all. I wrote a deep dive on EIP-7002 to help others, especially stakers and staking pool operators, understand the rationale behind introducing execution-layer exits for Beacon Chain validators: [EIP-7002: Unpacking Improvements to Staking UX Post-Merge](https://research.2077.xyz/eip-7002-unpacking-improvements-to-staking-ux-post-merge). All feedback and comments are welcome. cc: [@djrtwo](/u/djrtwo) [@petertdavies](/u/petertdavies) [@Wander](/u/wander)

---

**OisinKyne** (2024-01-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wander/48/11010_2.png) Wander:

> This all started because @OisinKyne had a great idea to give 7002-based exits priority over the current exit queue. This is useful for LST protocols which would benefit from better liquidity guarantees and will need to use this mechanism for safety anyway.

Hi all, I’d like to weigh in here and expand a bit more on my point. I haven’t had the bandwidth to formalise this into something actionable, but if I don’t say something soon, I won’t have the opportunity to, so here’s something quick.

The crux of the matter in my eyes is that a simple FIFO exit queue will some day lead to bank-run like behaviour of the validator set around contentious forks, if everybody is piling out, it’s rational to panic first and exit early rather than to leave it too late. We can and should do better here, and the adjustment is, in my eyes relatively minor.

I think this can be fixed with a control-loop mechanism, this EIP *already has an escalating basefee* like EIP1559, to prevent too many exits, **my belief is that these exits should simply be processed first, ahead of the ‘free queue’**. This means you can always have your money back immediately(-ish), if you are willing to pay the base fee, this gives you reason to relax and not exit ‘just in case’.

The upsides of this design would be significant in the context of LSTs. Currently we suffer from a situation where only the largest are materially liquid, and whales won’t allocate to an LSP that they would make up too large of a percentage of. LSPs also have to subsidise an LP pool to convince users these assets are liquid. If they could be redeemed near instantly, the risk of being stuck would be greatly reduced. These protocols could also keep their peg more predictably. Similarly, lending protocols are less likely to see liquidations due to ‘queue mismanagement’, where an LST is under target for longer than the liquidation window, because they didn’t foresee a ‘profitable trading strategy’ where someone drains the LP for their token, forcing withdrawals, but achieving cascading liquidations faster than the withdrawals can clear the exit queue.

On the implementation side of things, I have had a chance to speak with [@djrtwo](/u/djrtwo), [@mikeneuder](/u/mikeneuder) and others, and I acknowledge there is complexity around how to handle huge demand for a priority queue (e.g. if it’s > the amount of processable exits, what do, third queue? fail the tx?) among other things like the statefulness of this feature, but I do think its worth allocating some time towards this. If we don’t; we get a feature that costs lots of gas for users, and provides minimal benefits that is only for worst case scenarios. If we do; we fundamentally change the need for LSPs in the market, we make direct staking more palatable to users that are telling and showing us that liquidity is a must, we make competition amongst the long tail of LSPs easier, and we make the game theory of panics more stable, hopefully.

I know everyone (myself included) really really wants this feature soon, but I strongly believe that if we go with a simple FIFO queue, with an added tax for withdrawal key initiated exits, we will be in a worse place than if we do something more forward looking and pre-emptive.

Feedback welcome. ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**rakita** (2024-04-06):

If EOF gets included, it would be good to make the system contract in EOF format.

---

**logach** (2024-04-23):

Hey-hey!.

This is a highly anticipated update and thanks for the great work!

Since the spec is still being updated (added support for partial withdrawals), I would like to suggest to consider adding an event on EL like `WithdrawalRequest(pubkey, amount)`, what do you think?

To make both deposits and withdrawals look more symmetrical (There is a `DepositEvent` for deposits).

---

**matt** (2024-04-23):

What is the motivation for having an event? The withdrawal requests will be accessible via the block in the RPC.

The deposit contract has a deposit event because it was the only reasonable way to share the data from the PoW to the PoS chain without modifying PoW clients.

---

**etan-status** (2024-04-29):

> (e.g. care that might need to be taken in future upgrades if, for example, the shape of the merkle tree of BEACON_ROOT changes, then the contract and proof structure might need to be updated).

If something based on `BEACON_ROOT` is chosen, [EIP-7688](https://github.com/ethereum/EIPs/pull/8439/files) may help with forward compatibility. That at least helps as long as the portions of the state being used in this EIP don’t fundamentally change. Note that decentralized staking pools such as Rocket Pool share the same issues. It would be great to find a solution that we are comfortable using ourselves, if we deem it acceptable for application developers.

---

**etan-status** (2024-04-29):

> Note, validator_index also disambiguates validators.

For reference, the CL uses `validator_index` in [Withdrawal data structure](https://github.com/ethereum/consensus-specs/blob/dev/specs/capella/beacon-chain.md#withdrawal).

There may be interactions with other ideas for reusing validator indices, and also across different branches / deposit orders. The current EIP design seems fine in that regard, but still mentioning it for completeness.

---

**pk910** (2024-06-25):

Hi everyone,

I’d like to reopen the discussion about adding an event to this EIP. I hope it’s not too late for consideration.

Including an event in the EIP-7002 and EIP-7251 contracts would greatly enhance the traceability of execution layer-triggered operations on the beacon chain. Without such an event, explorers and other tools cannot easily determine the origin of these operations (e.g., txhash or sender) without tracing all transaction executions in each block. Even if it’s not strictly required from a technical perspective, adding a simple event upon successful contract calls would make it much easier to track the operations back to the original transactions.

Additionally, having an event for these critical operations would be consistent with practices in the deposit contract and upcoming EIP-7708.

---

**for3** (2024-08-13):

hi, i saw a lot of talk about eip-7251 recently.

i am wondering if there can be a period (weeks or months) where the withdrawal credentials and validator credentials combined can change the withdrawal address.

i am saying this because i can see when searching that many people have had their withdrawal address compromised.

i think we are talking hundres of millions in USD.

i am aware it is not too much in the big picture, and also it is late and probably not easy, but as a network it will be nice we handle this situation instead of as it is now that these people will loose their money with high likelihood by front runners.

let me know what you think.

---

**matt** (2024-08-13):

This would be outside the scope of this proposal, but in general I don’t see a change like that happening for the consensus layer.

---

**for3** (2024-08-13):

ok thanks for the reply,

i just wondered if it could be related to the 0x02 talk

i.e. if there is a change in that aspect, then i wondered if for some time people with compromised withdrawal credentials could be allowed to change it by requiring both the withdrawal credentials and the validator credentials

---

**for3** (2024-08-14):

it would be a temporary change / window for those who lost withdraw creds, which seems to be quite a few,

like weeks or months

but i think you got that

it could be a “small” fork before spectra or similar

---

**etan-status** (2024-09-18):

Should there a be a sequential index on these (across all blocks), to help distinguish between multiple copies of the same exit data? Deposit requests and withdrawals have a unique index as well.

---

**etan-status** (2024-09-19):

If the idea is for `MAX_WITHDRAWAL_REQUESTS_PER_PAYLOAD` to increase in the future, the Merkleization limit should be put to a theoretic limit (similar to how it is done for blobs and for `MAX_DEPOSIT_REQUESTS_PER_PAYLOAD`). Otherwise, increasing the limit later breaks `hash_tree_root`.

---

**wadealexc** (2024-11-14):

Hey all, digging through this EIP now as we prep our restaking contracts for the Pectra fork.

2 questions:

1. The “Utilizing CALL to return excess payment” section in the EIP mentions returning excess fee to the sender and concludes that the CALL opcode will be used to do this. However, neither the pseudocode for add_withdrawal_request, nor the included EVM bytecode have a CALL anywhere. Is this still a part of the EIP, or was it cancelled?
2. How much ETH can I withdraw from a validator before it’s exited?

I assume any withdrawals that bring the validator under 32 ETH will result in a full withdrawal, but how is this handled?
3. If I have a validator with 32 ETH and I trigger a withdrawal request for 1 ETH, does the full 32 ETH get withdrawn, or does the withdrawal simply fail to be processed?
4. If I request a withdrawal for a validator that has no balance, or from an address that is not the validator’s withdrawal address, will the call to the predeploy succeed, but no withdrawal will be processed?

2 gripes:

1. The current fee is not queryable via the predeploy. I can query and calculate it from get_excess_withdrawal_requests, but my only references are a pseudocode python method and a bunch of EVM bytecode. If there’s not a getter in the predeploy, I wish there was at least a reference implementation in Solidity!
2. The calling conventions for these predeploys is such a deviation from typical EVM calling conventions, where we’d use a 4-byte function selector to signify which method to call instead of relying on CALLDATASIZE. I’m not quite sure what the rationale is for this - maybe wanting to avoid standardizing 4 byte function selectors? Either way, it feels like the decision to use CALLDATASIZE to disambiguate methods leads to a really limited selection for what methods can be included in the predeploy - and as a result, the predeploys are clumsy and awkward to use.

---

**lucassaldanha** (2024-12-10):

> The current fee is not queryable via the redeploy

I think the information on the EIP-7002 page is out of date. The latest version of the contract will return the fee instead of the excess requests. Here is the commit that introduced that change ([withdrawals: change contract to return fee instead of excess in read op · lightclient/sys-asm@fa35d11 · GitHub](https://github.com/lightclient/sys-asm/commit/fa35d11835a3822d86360f6557ac5fb468491132)).

> The calling conventions for these predeploys is such a deviation from typical EVM calling conventions

When implementing the contracts, the rationale is to keep its execution cost as low as possible. And given the “simple” nature of the logic (the user has only two options, query the fee or add a request), the need for selectors is less relevant. Even though we do not have a solidity reference implementation, we have a geas implementation that is pretty much a 1-1 to solidity bytecode. You can check it here: [sys-asm/src/withdrawals/main.eas at main · lightclient/sys-asm · GitHub](https://github.com/lightclient/sys-asm/blob/main/src/withdrawals/main.eas)

Some references on usage:

- sys-asm/test/Withdrawal.t.sol at main · lightclient/sys-asm · GitHub
- pectra-utils/requests_contract/Requests.sol at master · lucassaldanha/pectra-utils · GitHub

---

**wadealexc** (2024-12-11):

Thanks for the pointer - looks like all but question 2 are answered! (“How much ETH can I withdraw from a validator before it’s exited?”)


*(6 more replies not shown)*
