---
source: magicians
topic_id: 2434
title: Remediations for EIP-1283 reentrancy bug
author: benjamincburns
date: "2019-01-16"
category: EIPs
tags: [security, hardfork, eip-1283]
url: https://ethereum-magicians.org/t/remediations-for-eip-1283-reentrancy-bug/2434
views: 11525
likes: 84
posts_count: 106
---

# Remediations for EIP-1283 reentrancy bug

Starting a thread here to discuss potential mitigations for the [reentrancy attack introduced by EIP-1283](https://medium.com/chainsecurity/constantinople-enables-new-reentrancy-attack-ace4088297d9).

Getting the obvious one out of the way up front: we could pull EIP-1283 from Constantinople. The obvious merit to this idea is that it’s quite simple to implement.

## Replies

**Arachnid** (2019-01-16):

Proposals I’ve seen so far:

1. Add a condition to SSTORE that causes it to revert if less than 2300 gas remains.

Straightforward.
2. Makes the violated invariant (‘the gas stipend is not enough to change state’) explicit.
3. Can be applied without the need to enable it only on a hardfork, since all past transactions meet this requirement (on mainnnet, at least).
4. Add a new call context that permits LOG opcodes but not changes to state.

Adds another call type beyond existing regular/staticcall
5. Makes the violated invariant into a fixed rule
6. Raise the cost of SSTORE to dirty slots to >=2300 gas

Straightforward
7. Makes net gas metering much less useful.
8. Reduce the gas stipend

Straightforward
9. Makes the stipend almost useless.
10. Increase the cost of writes to dirty slots back to 5000 gas, but add 4800 gas to the refund counter

Preserves net gas costs while preventing reentrancy.
11. Still doesn’t make the invariant explicit.
12. Requires callers to supply more gas, just to have it refunded.
13. Add contract metadata specifying per-contract EVM version, and only apply SSTORE changes to contracts deployed with the new version.

Ensures existing contract behaviour doesn’t change.
14. Adds more implementation complexity.
15. General mechanism that can be reused for other EVM changes.

---

**ajsutton** (2019-01-16):

For any potential solution we’ll need to remember that EIP-1283 has already rolled out on a number of test networks.  As such, we’ll need a way to not break them - most likely by having clients support Constantinople-with-EIP-1283 and Constantinople-as-deployed-on-Mainnet.  Test nets may potentially want to have an additional fork to move from EIP-1238 to whatever winds up being deployed on Mainnet.

I suspect from an implementation perspective just dropping EIP-1283 from Constantinople is simplest - clients could then treat it as a separate hard fork which on test nets happened at the same time and never happened on MainNet. How clean that solution is will vary from client to client though. This assumes that the “fixed” EIP-1283 or whatever replaces it would then be part of a later fork which is then applied to all nets.

---

**ajsutton** (2019-01-16):

The problematic EIP is EIP-1283 not 1238 btw. https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1283.md Might be worth updating the title.

---

**benjamincburns** (2019-01-16):

Ack, thanks for pointing that out! Should be fixed now.

---

**sorpaas** (2019-01-16):

I tried Option I in [Parity Ethereum](https://github.com/paritytech/parity-ethereum/pull/10191). Looks really simple to me because it applies universally to genesis (if not considering testnets). Some jsontests need to be regenerated, but we need to regenerate them anyway even if we decide to pull.

---

**MicahZoltu** (2019-01-16):

Proposal: Take some time to do some deep chain analysis to find out if there are any susceptible contracts that are actually in use, if not move forward with EIP as-is and update documentation to no longer advise users to rely on the stipend.

When critquing this proposal, pleases be clear whether your concern is with our ability to accurately find any such contract or that even if we don’t find such a contract we should still not move forward with this path.

---

**jochem-brouwer** (2019-01-16):

1. This looks fine
2. This should be a new opcode
3. This is not in line with the idea of gas usage (gas usage is proportional to computation time) which is, if I recall correctly, the entire idea why 1283 was proposed
4. This is only on the solidity side? Solidity explicitly forwards 2300 gas on transfers and calls. I don’t see how this can be changed
5. I don’t like this one because now you have to forward much more gas than which is actually used.

I like 1) the most. This is simple and mitigates this attack.

In general, we should discuss what hard forks can change and what not. Since via solidity most developers think that if send or transfer is used re-entrancy attacks are mitigated, we cannot change this in a hard fork later because it is almost certain that there will be vulnerable contracts to this attack (because most contracts are written in solidity and we have a lot of those contracts so the chance of hitting at least a vulnerable one is really high). However, if we think about other forks in the past (such as changing gas usage of `extcodesize`) this might look straightforward but it could change the behavior of contracts which depend `gasleft()` and explicitly assume that this opcode uses a certain amount of gas. The question is now: what if all contracts except one handle this EIP fine, but the single contract is now broken? Can we now fork or not? This is not ethical but it is worth discussing.

Another, much more general idea is to include an opcode which writes a number to some special storage where this certain contract can opt-in for EIPs. Let’s say a contract is vulnerable for the reentrancy attack. Only the owner of the contract can call this function. The owner simply decides not to opt-in for this EIP while other contracts can. Now the contract is not vulnerable.

---

**Flash** (2019-01-16):

Does the 2300 gas stipend have a purpose beyond preventing reentrancy?

Afaik, these calls were never supposed to change state. Making this explicit by introducing a new call context keeps expected behaviour consistent without shackling SSTORE. Couldn’t the gas stipend then be removed to allow for more logging?

---

**jochem-brouwer** (2019-01-16):

[@Flash](/u/flash) I think that the 2300 gas stipend was indeed introduced to prevent against reentrancy per [this stack exchange post](https://ethereum.stackexchange.com/questions/19341/address-send-vs-address-transfer-best-practice-usage) and [this discussion](https://github.com/ethereum/solidity/issues/610).

Introducing a new call context where everything is allowed except SSTORE might be interesting but it is starting to get very bloated with all the different call types (call, delegatecall, callcode, staticcall, this new one). Technically sending value is also a special kind of SSTORE since it alters the balance of an address. Logging (events) instead are not the same since these can never be SLOADed (or equivalent for the balance: BALANCE opcode).

What do you mean by “removing gas stipend”?

---

**tkstanczak** (2019-01-16):

1. Is good as a solution that does not require changes to the existing contracts after the release and allows for EIP-1283 to be delivered and remain important. It works nicely because it just blocks something that would not be allowed on Byzantium anyway (so no correctly built contract would expect this not to fail).
2. It may cause things that were expected not to fail in the valid contracts to fail after the change is introduced and we would have to specify which operations are allowed explicitly - LOG, PUSH?, DUP?, CALLCODE?, etc. - very likely that we would end up blocking SSTORE only in the end.

3,4,5 - all seriously decrease net gas metering impact

---

**Flash** (2019-01-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jochem-brouwer/48/14659_2.png) jochem-brouwer:

> What do you mean by “removing gas stipend”?

I mean removing the then redundant 2300 gas cap on send and transfer in the case that we went with 2.

I wouldn’t call that bloated, it’s a useful call type. But I’ll happily leave that decision to others.

---

**jochem-brouwer** (2019-01-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/flash/48/1356_2.png) Flash:

> mean removing the then redundant 2300 gas cap on send and transfer in the case that we went with 2.

This would be a change in solidity? We can’t change contracts which are on the chain already, so we cannot simply change that any contract which forwards 2300 gas now suddenly forwards less.

In solidity, I think the reasonable change would be to assume that `CALL` always costs at least 700 gas and then hence only forward 700 gas. This can only lead to problems if the fallback function is so deep in the contract (too much solidity functions are around) such that the 700 gas is already used before it reaches the fallback function. Of course this can be optimized via a check that if `CALLDATALENGTH==0` it immediately jumps to the fallback but this adds a slight amount of overhead gas before you get into any function block.

---

**Arachnid** (2019-01-16):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> Proposal: Take some time to do some deep chain analysis to find out if there are any susceptible contracts that are actually in use, if not move forward with EIP as-is and update documentation to no longer advise users to rely on the stipend.
>
>
> When critquing this proposal, pleases be clear whether your concern is with our ability to accurately find any such contract or that even if we don’t find such a contract we should still not move forward with this path

I think this is a bad idea both because we can’t guarantee we’ll identify all vulnerable contracts, and because we shouldn’t violate this invariant retrospectively.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jochem-brouwer/48/14659_2.png) jochem-brouwer:

> Introducing a new call context where everything is allowed except SSTORE might be interesting but it is starting to get very bloated with all the different call types (call, delegatecall, callcode, staticcall, this new one).

FWIW - delegatecall is a different call type, but results in a regular call context (it executes as normal). Likewise for callcode. We wouldn’t need a new opcode for this, either.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jochem-brouwer/48/14659_2.png) jochem-brouwer:

> This is only on the solidity side? Solidity explicitly forwards 2300 gas on transfers and calls. I don’t see how this can be changed

I wasn’t aware Solidity does this. The call stipend is an EVM feature; Solidity could equally set the gas to 0  with the same effect.

---

**AlexeyAkhunov** (2019-01-16):

In my opinion, the EIP-1283 does not need to be remediated, but rather removed all together. I do understand its intent (making inter-frame communications cheaper), and I proposed an alternative which is cheaper, slightly more powerful, and without the semantic changes to the existing opcodes:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/alexeyakhunov/48/17_2.png)
    [EIP-1153: Transient storage opcodes](https://ethereum-magicians.org/t/eip-transient-storage-opcodes/553) [Core EIPs](/c/eips/core-eips/35)



> I have written this EIP after having reviewed EIP-1087 (EIP-1087: Net gas metering for SSTORE operations) and its discussion (EIP-1087: Net storage gas metering for the EVM - #35 by Arachnid).
> I propose an alternative design (which Nick said he also considered at some point), which in my opinion can bring bigger benefits than EIP-1087, at lower cost (by this I mean new opcodes with very simple semantics and gas accounting rules, and keeping the existing gas accounting rules for SSTORE intact)…

Looking at the history EIP-1283, we see that it has been EIP-1087, formulated in a way which was harder to implement in Parity than in Geth. Then, it was reformulated into EIP-1283, to make it more abstract and less implementation-dependent. However, the semantic complexity was still there, and that caused a consensus issue on Ropsten, which delayed Constantinople once. And now it delays Constantinople once again, due to unintended consequences. Both of these incident can be traced to two things this EIP is doing that were not done before:

1. Reducing refund counter (prior to that, refund counter was only increased). That was basis of the Ropsten bug
2. Reducing the gas cost on an action. In all other hard forks, the gas cost of operations were only increased.

There is another potential impact of this EIP, which has not been appreciated yet. It will make harder for State Rent group to figure out alternatives to the State Rent, because the edge cases introduced by this EIP will make analysis harder.

My suggestion is to simply exclude this EIP from Constantinople. If the inter-frame communication is still in demand, it can be introduced by a more specialised change, rather than piggy-backing on the existing resource (contract storage). But honestly, I think this particular cost reduction is not a very important feature, and app developers can definitely live without it, while we are concentrating our efforts on Ethereum 1x and scalability improvements instead.

---

**jochem-brouwer** (2019-01-16):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> Proposal: Take some time to do some deep chain analysis to find out if there are any susceptible contracts that are actually in use, if not move forward with EIP as-is and update documentation to no longer advise users to rely on the stipend.
>
>
> When critquing this proposal, pleases be clear whether your concern is with our ability to accurately find any such contract or that even if we don’t find such a contract we should still not move forward with this path.

I agree with [@Arachnid](/u/arachnid). Besides doing a deep chain analysis which will take very long to “look” correct it will be extremely hard to prove that there are a low amount of contracts susceptible. Keep in mind that simply looking for “drain” attacks are just part of the scope. It is also possible to do funky things to the contract by writing to some storage slots which messes up the logic of the contract. I think this not doable, but I have no experience with static analysis so that might just be my inexperience.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arachnid/48/18_2.png) Arachnid:

> I wasn’t aware Solidity does this. The call stipend is an EVM feature; Solidity could equally set the gas to 0 with the same effect.

No this does not work, because the idea behind `transfer` and `send` is that you are also allowed to send Ether to contracts which have a payable fallback. These hence execute (given a solidity-compiled contract) the code to select a function: if none is found, it checks if there is a (payable) fallback. (Hence forwarding 0 gas will immediately result in an out of gas error).

Besides all this I agree with [@AlexeyAkhunov](/u/alexeyakhunov) to remove it altogether. I think in most cases writing to the same storage slot in a contract twice should be removed at compile time. At least in transactions which only happen during a single call this can be removed at compile-time. There might be some cases that this is harder if there are calls to other contracts (which call back into the current contract), but I think with some tricks this might also be possible. Hence the only case where this EIP is applicable is where a contract calls another one, which calls back into the current one. In all other cases more than single-writes to the same storage slot can be removed at compile time.

---

**MicahZoltu** (2019-01-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arachnid/48/18_2.png) Arachnid:

> we shouldn’t violate this invariant retrospectively

**IF** we can gain the necessary confidence that this bug isn’t exploitable against any active contracts in the wild, why is maintaining this invariant necessary?  Not only was the invariant only implied, not explicitly stated, but if no one is depending on it what do we gain by maintaining it?

---

**AlexeyAkhunov** (2019-01-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jochem-brouwer/48/14659_2.png) jochem-brouwer:

> I think in most cases writing to the same storage slot in a contract twice should be removed at compile time. At least in transactions which only happen during a single call this can be removed at compile-time. There might be some cases that this is harder if there are calls to other contracts (which call back into the current contract), but I think with some tricks this might also be possible. Hence the only case where this EIP is applicable is where a contract calls another one, which calls back into the current one. In all other cases more than single-writes to the same storage slot can be removed at compile time.

Unfortunately, it cannot be removed at compile time, IMO. In order to do that, there would need to be an alternative resource in EVM that allows retaining information between the call frames. Currently, only storage is retained between the frames, since fresh memory is given to each frame, and the stacks are segregated too.

---

**jochem-brouwer** (2019-01-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/alexeyakhunov/48/17_2.png) AlexeyAkhunov:

> Unfortunately, it cannot be removed at compile time, IMO. In order to do that, there would need to be an alternative resource in EVM that allows retaining information between the call frames. Currently, only storage is retained between the frames, since fresh memory is given to each frame, and the stacks are segregated too.

Yes, this is why I noted that you cannot remove it if there is a call to another contract which calls back into the current one. But you are right, it is more specific: it there are multiple call frames on the current contract then it is not possible to remove at compile time. However, I think there might be some kind of trick via the returnvalue of a call frame.

---

**MicahZoltu** (2019-01-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/alexeyakhunov/48/17_2.png) AlexeyAkhunov:

> Reducing the gas cost on an action. In all other hard forks, the gas cost of operations were only increased.

I’m generally against asserting that we will never decrease gas costs.  In order for gas accounting to function appropriately we need the power/authority to be able to tune them up/down as hardware/software changes with time.  While I can appreciate that having this ability makes things harder, I believe it is necessary for keeping Ethereum competitive.

IIUC, it sounds like you are sort of arguing that Ethereum 1.x is in maintenance mode and we basically shouldn’t be doing any active development on it that isn’t necessary for Ethereum 2.0?  Any changes to the EVM should be proposed targeting Ethereum 2.0 instead?

---

**AlexeyAkhunov** (2019-01-16):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> I’m generally against asserting that we will never decrease gas costs. In order for gas accounting to function appropriately we need the power/authority to be able to tune them up/down as hardware/software changes with time. While I can appreciate that having this ability makes things harder, I believe it is necessary for keeping Ethereum competitive.

I am not saying we should not decrease costs of operations. I am pointing out that there was complexity in EIP which was not on the plain sight. And it should have been given more weight when discussing the alternatives.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> IIUC, it sounds like you are sort of arguing that Ethereum 1.x is in maintenance mode and we basically shouldn’t be doing any active development on it that isn’t necessary for Ethereum 2.0? Any changes to the EVM should be proposed targeting Ethereum 2.0 instead?

Yes. It has already been proposed by Vitalik at DevCon3, October 2017, in his “Modest Proposal for 2.0”. He suggested to keep Ethereum 1.0 “safe and conservative”. Of course, Ethereum 1x initiative kind of goes opposite to that, but only because we believe that there are SOME changes necessary to keep Ethereum 1.0 alive.


*(85 more replies not shown)*
