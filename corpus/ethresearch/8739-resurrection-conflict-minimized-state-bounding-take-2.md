---
source: ethresearch
topic_id: 8739
title: Resurrection-conflict-minimized state bounding, take 2
author: vbuterin
date: "2021-02-22"
category: Execution Layer Research
tags: []
url: https://ethresear.ch/t/resurrection-conflict-minimized-state-bounding-take-2/8739
views: 8700
likes: 13
posts_count: 18
---

# Resurrection-conflict-minimized state bounding, take 2

See also v1: [Alternative bounded-state-friendly address scheme](https://ethresear.ch/t/alternative-bounded-state-friendly-address-scheme/8602)

This document describes a scheme for how accounts and storage slots can be stored in a way that allows them to be pruned over time (see [this doc on state expiry schemes](https://hackmd.io/@HWeNw8hNRimMm2m2GH56Cw/state_size_management)) and minimizes issues around resurrection conflicts. The mechanism is epoch-based and so can be viewed as a form of “regenesis”.

- Let an epoch be a period of roughly 1 year in length.
- We introduce an extended address scheme: an address can be viewed as a tuple (e, s) where e is an epoch and s is a subcoordinate (a 20-byte value that contains the same information that addresses contain today). An account with address (e, s) can only be touched when the chain is in epoch \ge e
- The state consists of an ever-growing list of state trees, S_1, S_2, S_3…, where each S_i is the state corresponding to the current epoch. During epoch e:

Only tree S_e can be modified
- Old trees (all trees S_d where d  e) are empty (because there was not yet any legal way to modify them)

An account (e, s) can be accessed in any epoch f \ge e, and is always stored in the tree at position hash(e, s)

Account editing rules are as follows:

- If an account (e, s) is modified during epoch e, this can be done directly with a modification to tree S_e
- If an account (e, s) is modified during epoch f > e, and this account is already part of tree S_f, then this can be done directly with a modification to tree S_f
- If an account (e, s) is first created during epoch f > e and was never before touched, then the sender of the transaction creating this account must provide a witness showing the account’s absence in all trees S_{e}, S_{e+1} ... S_{f-1}
- If an account (e, s) is modified during epoch f > e, and this account is not yet part of tree S_f, and the account was most recently part of tree S_{e'} with e \le e'

## Example

#### Epoch 7

- Alice publishes a smart contract in epoch 7. Alice generates an address (7, 0x14b647f2) and sends a transaction to initialize that contract. The contract is saved in the state tree S_7 at position hash(7, 0x14b647f2). This is unchanged from status-quo Ethereum.
- Later in epoch 7, Alice interacts with her contract. The record at position  hash(7, 0x14b647f2) is modified. This is still unchanged from status-quo Ethereum.

#### Epoch 8

- Time passes and it is now epoch 8. To interact with her contract again, Alice’s transaction in the block would need to provide the witness from S_7 (which can no longer be modified) to prove to the chain the most recent state of that block from the last epoch. Fortunately, as a convenience for Alice, block producers are expected to store S_7, so Alice simply sends her transaction as is, and the block producer will add the witness. The record of Alice’s contract is now saved in the state tree S_8 at position hash(7, 0x14b647f2). Alice’s experience is unchanged from status-quo Ethereum, but block producers do have the new requirement that they need to generate the witness. S_8 stores the updated state of Alice’s contract, S_7 forever stores the state that it had at the end of epoch 7.
- Alice interacts with her contract again in epoch 8. Because the position hash(7, 0x14b647f2) in S_8 already contains a state object, there is no need for even the block producer to provide a witness.

#### Epoch 13

- Alice’s plane crashes on an island, and Alice has no contact with the world for five years. Fortunately, Alice is eventually discovered, and she makes it back to civilization.
- As soon as she gets home, she immediately wants to get back to playing with the most important thing in the world for her: her smart contract. It is now epoch 13. To recover her smart contract, she needs to find someone who has a witness to show the value at position hash(7, 0x14b647f2) in S_8, and show that that position is empty in S_9, S_{10} and S_{11} (the block producer can add the witness for S_{12}).
- Bob, overjoyed at Alice’s return, sends her a nyancat NFT as a welcome-back present. However, he foolishly assigns the nyancat’s ownership to another address that Alice generated and gave him all the way back in epoch 5 (the address is (5, 0x2718bfa3)).
- Alice never actually used that address. So she finds some third party (eg. etherscan) who has the witnesses proving that (5, 0x2718bfa3) was not in S_5, S_6 or any other tree up to S_{11}. She sends a transaction containing those witnesses, verifying the state of her account (her account might be stateful because it’s a social recovery wallet in which case simply proving the code from the address and adding an epoch-aware anti-replay scheme is not sufficient), and transfers her nyancat NFT to a different account.

#### Epoch 16

- Alice hibernates for a few years, and wakes up. It is now epoch 16. To use her smart contract or her nyancat-holding account (as well as the nyancat itself), she must provide witnesses from S_{13} and S_{14}.

## Nice properties

- Full protection against resurrection conflicts
- No situation is unrecoverable; even when Alice was on an island or hibernating, she was always later able to recover her account by asking a third party for witnesses

Note: if we want to support recovery from multi-hundred-year absences [eg. Alice is cryogenically frozen and then revived with advanced technology in the 2300s], then we may need ZK-SNARKs to make the set of all witnesses for the intervening epochs verifiable within the gas limit, but we don’t need to actually think about adding support for this for at least a hundred years

Does not require any fancy properties from trees; trees can simply be key-value stores

### Adding storage slots

The simplest way to add storage slots to this construction is to move toward a one-layer state scheme, so storage slots are treated equivalently to independent accounts. The SSTORE and SLOAD opcodes *would* need to be modified to add an epoch parameter (so each account would de-facto have a separate storage tree for each epoch), and for maximum efficiency contracts would need to be rewritten to take advantage of this. But even if they do not, contracts would not break; rather, existing SSTORE/SLOAD operations would be mapped to epoch 0, so reading/writing to new storage slots would simply start to become more and more expensive due to witness costs, and performance would degrade gracefully.

## Replies

**imkharn** (2021-03-03):

So for users this means they have to spend 21000 gas per year to keep their account active and if they fail to do so they have to pay for a witness proof.

Do you have a ballpark of the gas used by a witness proof?

If miners are required to store the current epoch and the previous epoch, and all contracts and accounts used at least once per year are in both the current and previous epoch, wont that make the amount miners have to store 2x the total active ethereum state?  If so, then if the active ethereum data * 2 is greater than the inactive ethereum data, then this change would end up increasing the amount of data miners have to store.

---

**MicahZoltu** (2021-03-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/imkharn/48/5564_2.png) imkharn:

> So for users this means they have to spend 21000 gas per year to keep their account active and if they fail to do so they have to pay for a witness proof.

Yes.

![](https://ethresear.ch/user_avatar/ethresear.ch/imkharn/48/5564_2.png) imkharn:

> If miners are required to store the current epoch and the previous epoch, and all contracts and accounts used at least once per year are in both the current and previous epoch, wont that make the amount miners have to store 2x the total active ethereum state? If so, then if the active ethereum data * 2 is greater than the inactive ethereum data, then this change would end up increasing the amount of data miners have to store.

In theory, miners can prune state that is already migrated to the current epoch from the previous.  Should they choose to do so, there would be no data duplication.  While the state root for the previous epoch cannot change, they may need to generate a proof for state that is the sibling of a pruned node.  Luckily, they only need the hash of the pruned branch to generate such a proof, not the data itself.

That being said, pruning state is actually a hard problem given current client database design so an alternative database design (maybe only for the previous epoch branch) may be necessary to enable better pruning.

It would be very valuable to get an idea of how much state is active vs inactive though, so we can identify whether this is something we should think harder about or ignore.

---

**vbuterin** (2021-03-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/imkharn/48/5564_2.png) imkharn:

> Do you have a ballpark of the gas used by a witness proof?

Around 20k gas per item? Though if we switch to Verkle I could see it changing to something like 40k + 1k gas per item.

> and all contracts and accounts used at least once per year are in both the current and previous epoch, wont that make the amount miners have to store 2x the total active ethereum state?

I think miners should be able to forget any previous epoch state that has been carried over into the current epoch.

---

**imkharn** (2021-03-04):

Thanks for the replies.

Now that you mention it, there is even more that can be ignored,  in addition to any state that is identical in previous and current epoch (carried over) , it could also include deleting previous epoch data about any account active in the current epoch  because the only reason for keeping the previous epoch is to allow accounts to always avoid reinstatement cost when under 1 year, and if an account is active in the current epoch the reason for storing its data about the previous epoch disappears.

A potential issue is that a miner might be overly aggressive with pruning or not store previous epoch because perhaps the cost of storing the previous epoch immediately / after a couple months will not be worth it and they would rather effectively censor any witness transaction. While storage cost to the miner is pretty cheap, so is ignoring a witness transaction for the next highest paying non-witness transaction. Just ignoring witness transactions and picking something else from the transaction pool will be tiny loss, and witness transactions will be pretty rare I imagine. Might need a way to incentivize the previous epoch to be stored and that incentive mechanism would need to be mindful of not punishing missing data that is pointless to store.

---

**MicahZoltu** (2021-03-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/imkharn/48/5564_2.png) imkharn:

> While storage cost to the miner is pretty cheap, so is ignoring a witness transaction for the next highest paying non-witness transaction. Just ignoring witness transactions and picking something else from the transaction pool will be tiny loss, and witness transactions will be pretty rare I imagine. Might need a way to incentivize the previous epoch to be stored and that incentive mechanism would need to be mindful of not punishing missing data that is pointless to store.

I *suspect* this will work itself out in the end as miners can simply demand a higher inclusion fee for resurrections.  For example, they may put stale state on a slower drive and then they would need a higher fee to incentivize them to go to that drive to get the data.

---

**vbuterin** (2021-03-04):

> I suspect this will work itself out in the end as miners can simply demand a higher inclusion fee for resurrections.

I actually had an even simpler solution in mind: witnesses for resurrections cost gas.

---

**shamatar** (2021-03-06):

Hm, would it require that a smart contract that has something like mapping address -> uint256 would have to store a current mapping value in the user’s account storage at some storage subtree or slot linked to this contract’s address?

---

**vbuterin** (2021-03-06):

I think you can get away with something simpler: the contract has a child contract for each address space, and stores data relevant to accounts in address space `e` in the storage of the child contract in address space `e`. We could also just add a `SSTORE_TO_ADDRESS_SPACE` and `SLOAD_FROM_ADDRESS_SPACE` opcode that allows contracts to access the storage of themselves in different address spaces.

---

**shamatar** (2021-03-06):

That would be quite generic, but I had a simpler case in mind for a start. Some notation: an example ERC20 contract named ERC20, user addresses A, B, C, … etc

- option 1 (as described by the first post): user A has some balance in ERC20 contract in epoch 0, then time passes to epoch n >= 2, and may be some transfers has happened to A along the history, so A has to create proofs and post them for epochs 0…n-1 for storage slots related to A in the space of ERC20. This is perfectly fine, but I would want to try to investigate an option like “user (= user’s address) is responsible to his data”
- option 2: we somehow change the programming paradigms and compiler + create a new opcode that allows ERC20 to write data in A’s subtree to some index. This way we still can not avoid a case of “spilling” when e.g. after epoch 0 someone does a transfer to A that invalidates a subtree of the contract ERC20 and requires A to post linear number of proofs instead of potentially something shorter like “here is a state of ERC20 in my account at epoch 0 with some root, and proofs from the same root in all next epochs”

May be there are even better options, not sure yet, but the second one potentially allows user to have a one isolated place for his data in all well formed contracts that may be valuable by itself

---

**vbuterin** (2021-03-06):

One thing that’s worth noting is that the user only needs to provide proofs the *first* time. The second time the user accesses their ERC20 balance in epoch N, the storage slot would already be stored in the epoch N state tree (respite being part of the epoch 0 *address space*), and so you would not need a witness the second time.

---

**shamatar** (2021-03-06):

Sure, that is clear and implied. Proof size is linear over the number of elapsed epochs, provided only once at the first access at this epoch (if proof is ever required)

---

**Zergity** (2021-03-18):

Is this possible to let each EE responsible for state rent/pruning/resurrection? We can have the protocol incentive to each EE, and let EE design how they incentive the user transaction.

- Eth1 EE can still have the storage expansion cost and contraction gas refund.
- Libra EE can have their state rent.
- Polkadot EE can have their Existential Deposit.

---

**zsfelfoldi** (2021-03-24):

I like this storage model a lot but I’m not sure it’s a realistic approach in the short/medium term to deal with different epochs within a contract’s storage space. I mean it’s not totally undoable but it would be a full redesign of the storage paradigm (probably also our contract programming languages) which sounds to me like a long term solution that’s probably not going to make it into the current EVM. Making EVM sustainable for the short/medium term is non-negotiable though. Luckily we can get away with our current storage model if we use the epoch where each contract was created as the “default epoch” in which the storage of the given contract will operate forever. This is okay because every contract remains usable and if it is indeed actively used for a multi-epoch timespan (so that degrading performance becomes an issue) then new versions of the same contract can be deployed in each new epoch and the contract design should only care about allowing users to migrate frequently used data to the new version.

---

**vbuterin** (2021-03-26):

Hmm, not sure what you mean by this. There’s two distinct ideas:

1. Individual storage slots of a contract are migrated to newer epoch state trees separately
2. There’s the possible extension of allowing a contract to have storage in different address spaces

I don’t think (1) would change how the EVM or any programming languages work. It would still look like how things work today, except that your transaction will sometimes have to come with renewal witnesses for specific storage slots.

For (2), I agree that it would be a big change to how contracts work. There’s already the simpler alternative that if contracts want to have storage slot spaces in which they can add new content freely without witnesses, they can just create child contracts in newer address spaces.

There are also other alternatives we haven’t explored yet; for example, a contract can have a counter of what its total storage slot count is, and a counter of the number of storage slots poked in the current epoch, and if the two are equal then we know that the contract has been fully migrated forward, and we can just move the entire contract into the latest address space. Though that would add some implementation complexity…

---

**zsfelfoldi** (2021-03-27):

I was talking about whether a single contract should be able to handle multiple address spaces. And my opinion at the moment is that the answer is no (at least in the short/medium term). What I was suggesting is that contracts should usually be able to migrate their user data to newer versions of the same contract anyway, so we could just as well say that each contract has an address space in the epoch where it was originally created and even that should be acceptable. You’re right though, there might be even better options, like auto-migrate the entire contract storage address space to a newer epoch when all individual items have been updated and present in more recent state trees. If it’s not a lot of complexity then that’s even better. Still, my point is that (at least in the first version) we should go with some version of (1), one contract should have one address space based in a single epoch.

---

**vbuterin** (2021-03-27):

Got it. Sounds good to me; I have no problem with a contract being bound to a single address space.

---

**adietrichs** (2021-06-09):

Really interesting proposal! My first-pass thoughts:

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> If an account (e,s) is first created during epoch f>e and was never before touched, then the sender of the transaction creating this account must provide a witness showing the account’s absence in all trees S_e,S_{e+1}...S_{f−1}

I think the most pratical way to do this would be via access lists. So any transaction would have an ([EIP-2930](https://eips.ethereum.org/EIPS/eip-2930)-style, but adapted to the new address scheme) list of state locations that would be part of the signed tx data. The witness itself (meaning the state at the specified locations, and inclusion / exclusion proofs) would not be signed over. Transactions could include witness data during propagation, but would only be included into blocks in their raw form. The block itself would then include one aggregated witness created by the block producer, so that:

- If a transaction tries to access old state (meaning from a previous epoch and not in the latest tree) that is provided by the witness, the state access always succeeds (even if the location was not in the tx’s access list) and tx execution continues.
- If a transaction tries to access old state not provided by the witness and not present in the access list, transaction execution fails (and the whole tx is reverted, not only the current level), but the tx sender is still charged.
- If a transaction tries to access old state not provided by the witness, but present in the access list, the block is considered invalid.

In addition (less confident on these):

- Access lists are fully charged (for state refresh cost, except for those locations that are already part of the latest tree, where only calldata price is charged) at the beginning of a tx. At the end of the tx, all locations not touched during execution are refunded (up to calldata cost).
- A block with unused witness parts is considered invalid, even if these locations were included in access lists of the block’s txs.
- There could be a new tx type for explicitly refreshing locations (i.e. moving them into the latest tree), without any execution attached. For those the block witness would be required to include all such locations.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Block producer nodes are expected to store S_{e-1} to assist with producing witnesses (so users only need to produce witnesses for epochs more than 2 in the past).

I think this would likely have to be enshrined into protocol, meaning that the rules listed above would be modified with:

- If a transaction tries to access old state not provided by the witness and not present in the access list, but where the witness includes an exclusion proof against S_{e-1}, transaction execution fails (and the whole tx is reverted, not only the current level), but the tx sender is still charged.
- If a transaction tries to access old state not provided by the witness and not present in the access list, and if the witness does not include an exclusion proof against S_{e-1}, the block is considered invalid.

Without this modification, users would have to add all accessed S_{e-1} locations to a tx’s access list, which for many applications would require full execution of the transaction, which would in turn require the user to hold the relevant S_{e-1} state and make this “block producers keep S_{e-1}” rule mostly useless. Note also that for any such transactions there are new UX challenges regardless, as without the necessary state users cannot easily assess the tx’s likely outcome (including its gas consumption).

![](https://ethresear.ch/user_avatar/ethresear.ch/imkharn/48/5564_2.png) imkharn:

> So for users this means they have to spend 21000 gas per year to keep their account active and if they fail to do so they have to pay for a witness proof.

It seems to me that users would have to pay the refresh cost even for access to state from the S_{e-1} tree. In addition, if the transaction is sent via the “vanilla” transaction pool, it would likely have to come with a witness for the sender account regardless, to allow propagating nodes to assess its validity.

Transaction pool propagation rules would likely also require transactions to come with full witnesses attached for their access lists (with the discussed S_{e-1} exceptions), although state providers that voluntarily store more than the latest two state trees could offer ways to send txs without those witnesses directly.

**edit:**

I just realized that in the updated version of this proposal [here](https://hackmd.io/@vbuterin/state_expiry_paths) all nodes are required to also hold S_{e-1}. That makes a lot of sense to me and simplifies these S_{e-1} special case rules I described above. Accessing state from S_{e-1} would presumably still have to be more expensive to account for moving the state to S_e.

