---
source: magicians
topic_id: 2440
title: Immutables, invariants, and upgradability
author: lrettig
date: "2019-01-16"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/immutables-invariants-and-upgradability/2440
views: 7188
likes: 81
posts_count: 62
---

# Immutables, invariants, and upgradability

One of the critical meta-questions raised by [Remediations for EIP-1283 reentrancy bug](https://ethereum-magicians.org/t/remediations-for-eip-1283-reentrancy-bug/2434/18) and the [delay of the Constantinople upgrade](https://ethereum-magicians.org/t/core-devs-discussion-about-a-vulnerability-in-constantinople-delay-of-the-upgrade/2427) is: Precisely what on Ethereum is immutable and what behavior should be considered invariant?

Since irregular state transitions are outside the scope of this conversation, for sake of argument let’s all agree that code and data (storage) are immutable.

However, we’re left with the challenge that EVM semantics can and do change during a hard fork, the most germane example here being a change in gas cost. In other words, as a smart contract developer, **even though I know my *code* will not change, I do not have a guarantee that its *behavior* will not change.**

As [@AlexeyAkhunov](/u/alexeyakhunov) [points out](https://ethereum-magicians.org/t/remediations-for-eip-1283-reentrancy-bug/2434/16):

> In all other hard forks, the gas cost of operations were only increased

and it appears that many developers may have been relying on this to be invariant, as well as on the fact that `send` and `transfer` couldn’t result in reentrancy, which as [@MicahZoltu](/u/micahzoltu) points out [here](https://ethereum-magicians.org/t/remediations-for-eip-1283-reentrancy-bug/2434/18), was only “implied” and never explicit:

> Not only was the invariant only implied, not explicitly stated, but if no one is depending on it what do we gain by maintaining it?

I assert that:

- in general (with the possible exception of an emergency fix to EVM behavior where the risk of not fixing it is greater than the risk of changing the behavior of deployed code) there is a tacit social contract with developers whereby not only code but behavior should be immutable. This has not always been true historically, but many people nevertheless believe it to be true, hence the tacit social contract and the problem of “implied” invariants.
- intended behavior of deployed code is extraordinarily hard to establish – e.g., did a developer write something a certain way intentionally, or did they make a mistake? Therefore, we should not be in the business of trying to figure out or maintain intended behavior of deployed code. For this reason I disagree with use of the word “break” as in “breaking changes” or “breaking someone’s code” since, without establishing intent, we cannot know whether behavior has been “broken” or not.

If you agree with both of these points, then I think it follows that:

- all upgrades should be backwards-compatible, which is to say, they should not change the behavior of on-chain code.

I see two potential ways of achieving this:

1. Introducing an “EVM version” flag to deployed code (like a solidity pragma) so that a developer knows that their code will always target a particular version of EVM. This adds the requirement that all clients implement all historical EVM semantics and can fire up a VM for any EVM version. In practice all major clients today do implement all historical EVM semantics, but future clients may not. Another challenge with this approach is that contracts can call other contracts, which may in turn call contracts that target a newer EVM, so it does not solve the underlying problem. This could be addressed using a form of snapshotting or “static linking” of contracts, but that introduces complexity and problems with upgradability. A final challenge here is that it makes analysis and auditing much harder.
2. Another, simpler approach is to never change the behavior of an existing opcode (again, except in case of emergency). All changes to existing opcodes are introduced as new opcodes–in the case of EIP-1283, instead of changing SSTORE, a new SSTORE2 (or SSTORE_CHEAPER) could be introduced. This has the upside of simplicity and the downside of making the EVM more complicated.

There are two big, outstanding questions, however:

1. If we move forward with state rent or a similar solution, can it be done without changing the behavior of deployed code?
2. Should Ethereum 1.x be in “maintenance mode” with no further EVM changes, and should all such changes instead target Eth 2 and perhaps be done in Ewasm?

Thanks.

[Thanks to Liam Horne, Dan Robinson, Joshua Goldbard, and James Prestwich for sharing thoughts and discussing this issue. This was inspired by the conversation we had on this topic.]

## Replies

**Ethernian** (2019-01-16):

would merge here from other topic…

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png)

> The root cause of the ERC-1283 re-entrancy bug is an assumption about stability of gas costs and in particular that the gas cost of any storage change is more than a transfer call offers to the target contract.
>
>
> Gas costs of OPCODE come from sampling on “usual” hardware. Whatever “usual” hardware can be, it changes in years. Correspondent gas costs should be tuned time to time to prevent DDOS attacks or too low block limits. For example, if Non-Volatile Memory becomes significantly faster, the gas cost ratio SSTORE/MSTORE may change accordingly (lowing the SSTORE costs). Simply rising limits for gas per block will not work because it will create a DDOS attack vector by excessive usage of still-slow OPCODEs.
>
>
> I thing we should make it clear, that OPCODE gas costs are NOT constant in long term.
> Avoidable assumptions about gas costs in the future is a bad practice and should be discouraged.

---

**Ethernian** (2019-01-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png) lrettig:

> Another, simpler approach is to never change the behavior of an existing opcode (again, except in case of emergency).

Do you mean gas cost of an opcode is its behavior?  As I mentioned above, gas cost tuning may be necessary in the future because of hardware evolution. It is just not constant in long term.

---

**lrettig** (2019-01-16):

> gas cost tuning may be necessary in the future because of hardware evolution. It is just not constant in long term

This is a good point. Yes, I am considering gas cost tuning to be a behavior change as well–again, ample evidence in this present SSTORE issue. We always have the option of increasing the block gas limit rather than lowering the gas cost, of course, although that’s much less surgical.

---

**jpitts** (2019-01-16):

Definitely appreciate the first principles approach here!

A lot can be learned from recent computing history. The evolution of the x86 architecture sheds a lot of light, particularly as it fit into the IBM PC platform (allegorical to all of the other factors of the Ethereum protocol which affect how smart contracts run in the EVM).

Serious resources were put into backwards compatibility, and this is because Intel, MS, developers, and other stakeholders wanted to maintain stability of applications for its current user base. I recall that [@gcolvin](/u/gcolvin) mentioned this at the Council of Prague.

There have been generations of new features added to x86, as well as advances made to the PC platform at which it was the center. How did the designers ensure that backwards compatibility given all of those evolving parts?

As an example of the dedication to backwards compatibility as so much has moved forward in the PC platform, only now is the PC BIOS being removed!


      ![image](https://cdn.arstechnica.net/wp-content/uploads/2016/10/cropped-ars-logo-512_480-60x60.png)

      [Ars Technica – 22 Nov 17](https://arstechnica.com/gadgets/2017/11/intel-to-kill-off-the-last-vestiges-of-the-ancient-pc-bios-by-2020/)



    ![image](https://cdn.arstechnica.net/wp-content/uploads/2017/11/Ibm_pc_5150-1152x648.jpg)

###



The ability to boot DOS and other legacy relics is going to disappear.

---

**Ethernian** (2019-01-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png) lrettig:

> We always have the option of increasing the block gas limit rather than lowering the gas cost,

Do you think there will be no need to tune single opcode’s cost in the future even if the hardware will change significant?

---

**Arachnid** (2019-01-16):

In general I’m strongly in agreement. A large part of the point of using a blockchain like Ethereum is certainty about your code’s execution, and it’s crucial we retain that if we want Ethereum to be useful.

I think that we’re benefiting from a lot of hindsight bias here, though. Before this behaviour was discovered, nobody considered reducing the gas cost of SSTORE a potentially breaking change; reducing a cost is less likely to cause problems with contract execution than increasing it. I don’t think it’s reasonable to require a new opcode for every change, when the only difference between the two is that the new one is that it’s more gas-efficient. I also don’t  think it’s practical - if we do this we will run out of opcodes very quickly.

Versioning seems like a more practical approach, but will likely require consensus-level changes in order to function. On the other hand, it will also open the door to EWASM, which would require some kind of versioning anyway.

---

**Ethernian** (2019-01-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arachnid/48/18_2.png) Arachnid:

> Versioning seems like a more practical approach, but will likely require consensus-level changes in order to function.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png) lrettig:

> Introducing an “EVM version” flag to deployed code (like a solidity pragma ) so that a developer knows that their code will always target a particular version of EVM

I think the “EVM version” should not be embedded into deployed code, but be a function of block number of the particular chain.

Nevertheless I can’t understand how it could help in the ERC-1283 case.

Consider an a victim contract (V) was deployed at the age of EVM_v1 with the assumption about re-entrance safety of the `transfer`method.

Then we deploy an EVM_v2 and the attacker deploys his contract (A), sticking to  EVM_v2.

The victim code get executed in EVM_v1, the attacker code - EVM_v2 (with cheap SSTORE). I see no change to current buggy behavior.

---

**Arachnid** (2019-01-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png) Ethernian:

> I think the “EVM version” should not be embedded into deployed code, but be a function of block number of the particular chain.

Why?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png) Ethernian:

> Nevertheless I can’t understand how it could help in the ERC-1283 case.
> Consider an a victim contract (V) was deployed at the age of EVM_v1 with the assumption about re-entrance safety of the transfer method.
> Then we deploy an EVM_v2 and the attacker deploys his contract (A), sticking to EVM_v2.
>
>
> The victim code get executed in EVM_v1, the attacker code - EVM_v2 (with cheap SSTORE). I see no change to current buggy behavior.

That’s a good point.

---

**Ethernian** (2019-01-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arachnid/48/18_2.png) Arachnid:

> I think the “EVM version” should not be embedded into deployed code, but be a function of block number of the particular chain.

Why?

because it does not belongs to ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=12)

I can deploy the same code to different chains with different EVM versions inside.

---

**Ethernian** (2019-01-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arachnid/48/18_2.png) Arachnid:

> The victim code get executed in EVM_v1, the attacker code - EVM_v2 (with cheap SSTORE). I see no change to current buggy behavior.

That’s a good point.

hmm… may be I am wrong… It is too late…

May be the applicable rule set (EVM_v1 or EVM_2) should depends on which storage is accessed (which exactly means “the code gets executed”).

hmm… If we assume that the (V) Victim should store anything in own storage, then it is ok: he has EVM_v1 and “expensive” SSTORE. The reentrance attack using `transfer` call will fail.

But what if it depends on some critical state stored in some EVM_v2 contract, that an attacker could manipulate cheep? Then the attack will succeed.

Then we need indeed a possibility to define a target EVM for a contract we deploying. Oh… it gets complicated ![:frowning:](https://ethereum-magicians.org/images/emoji/twitter/frowning.png?v=12)

---

**fubuloubu** (2019-01-17):

Two really random thoughts:

1. The gas limit on transfer was a poor precedent to set as it created a bad development practice that can be easily violated in an otherwise innocent change like this. We should avoid doing subtle little hacks like this in future because they are hard to reason about.
2. It would instead be more beneficial if transfer literally would not allow a call back directly, by somehow shutting down execution or at least disallowing a re-entrancy more directly. That’s how most developers think of it in practice IMO.

---

**rajeevgopalakrishna** (2019-01-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jpitts/48/15152_2.png) jpitts:

> There have been generations of new features added to x86, as well as advances made to the PC platform at which it was the center. How did the designers ensure that backwards compatibility given all of those evolving parts?

Having worked at Intel for a few years, I observed that backward-compatibility was always a top-priority, very challenging and time-consuming to get right. As [@lrettig](/u/lrettig) points out, it is an explicit/implicit social contract with your developers/users, and in this case, fundamental to the immutability

(of behaviour) guarantee. This aspect may have been critical to the wide-spread adoption of x86 architecture because one can always buy the next generation processor with full confidence that the software they use/wrote (from n years ago) will continue to function as before.

---

**rajeevgopalakrishna** (2019-01-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fubuloubu/48/2484_2.png) fubuloubu:

> It would instead be more beneficial if transfer literally would not allow a call back directly, by somehow shutting down execution or at least disallowing a re-entrancy more directly. That’s how most developers think of it in practice IMO.

This is similar to what was suggested in [EIP-1283 Incident Report](https://github.com/trailofbits/publications/blob/master/reviews/EIP-1283.pdf) that we should consider introducing a contract-level reentrancy-/recursion-free `CALL` opcode. This could allow value transfers and state modifications (unlike `STATICCALL`) but prevent a contract-level indirect recursion.

---

**Arachnid** (2019-01-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rajeevgopalakrishna/48/1463_2.png) rajeevgopalakrishna:

> This is similar to what was suggested in EIP-1283 Incident Report that we should consider introducing a contract-level reentrancy-/recursion-free CALL opcode. This could allow value transfers and state modifications (unlike STATICCALL ) but prevent a contract-level indirect recursion.

I still think this is a bad idea. Preventing function-level recursion could be a useful thing to do, but preventing contract level recursion is far too blunt a tool. There are lots of cases where calling one’s caller is a useful thing to do, and next to no workaround for those cases if it’s prohibited.

---

**rajeevgopalakrishna** (2019-01-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arachnid/48/18_2.png) Arachnid:

> There are lots of cases where calling one’s caller is a useful thing to do, and next to no workaround for those cases if it’s prohibited.

I see. Given that `STATICCALL` should already reduce the reentrancy attack surface, introducing a variant of it that allows value transfers (for `transfer/send`) and only `LOG` opcodes in fallback functions seems too specific, wouldn’t it? This is essentially the second proposal listed [here](https://ethereum-magicians.org/t/remediations-for-eip-1283-reentrancy-bug/2434/2) I suppose.

---

**rajeevgopalakrishna** (2019-01-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png) Ethernian:

> The victim code get executed in EVM_v1, the attacker code - EVM_v2 (with cheap SSTORE). I see no change to current buggy behavior.

In the example contract [illustrated](https://medium.com/chainsecurity/constantinople-enables-new-reentrancy-attack-ace4088297d9) by ChainSecurity, the dirty/cheaper SSTORE is executed by the victim’s contract (in `updateSplit`) when called by the attacker contract’s fallback function. So, even though the attacker contract is in EVM_v2 context, when it makes a call to the victim contract, the context should change to EVM_v1 (assuming victim contract was deployed with EVM_v1 i.e. without EIP-1283) and the legacy SSTORE will fail with OOG. The attacker shouldn’t be able to force the victim contract to execute in the newer post-EIP-1283 EVM_v2 context. What am I missing?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arachnid/48/18_2.png) Arachnid:

> Versioning seems like a more practical approach, but will likely require consensus-level changes in order to function. On the other hand, it will also open the door to EWASM, which would require some kind of versioning anyway.

What do we mean by “consensus-level changes in order to function”?

If anyone is planning to work on this EVM versioning proposal, I will be interested in contributing. ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**Ethernian** (2019-01-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rajeevgopalakrishna/48/1463_2.png) rajeevgopalakrishna:

> So, even though the attacker contract is in EVM_v2 context, when it makes a call to the victim contract, the context should change to EVM_v1 //…// and the legacy SSTORE will fail with OOG. //…// What am I missing?

Yes, you are right. Although for pure re-entrance only.

In general the Victim can depend on other contract’s storage and if it is in EVM_v2 scope, we have a problem.

We will need a possibility to enforce the target EVM version on deployment.

But if there many Victims in different EVMs depending on shared storage, accessible by Attacker, it will be a version conflict…

---

**rajeevgopalakrishna** (2019-01-17):

Versioning, in general, will be tricky to design and enforce I suspect. But if we would like to update existing developer-exposed interfaces/semantics without sacrificing backwards-compatibility, then the options are to (1) offer new interfaces for updated semantics (i.e. via new opcodes) or (2) update semantics of existing interfaces (i.e. new opcode behaviour) but provide a versioning system to allow developers to bind their code to specific semantics.

---

**Ethernian** (2019-01-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rajeevgopalakrishna/48/1463_2.png) rajeevgopalakrishna:

> This is similar to what was suggested in EIP-1283 Incident Report that we should consider introducing a contract-level reentrancy-/recursion-free CALL opcode.

disagree.

Devs should create an re-entrance lock at the particular “entrance”, not at particular “exit” (call). At the “entrance” we know the function we would like to guard. Behind the “exit” it depends on callee and unknown to deployment time of caller’s contract.

We should publicly promote an explicit re-entrance lock usage. Assumption about reentrant behavior of other constructs, that were not developed as a re-entrancy lock, should be strongly discouraged.

Devs must use a lock on a function if there is something to guard and there is a call to other contract inside.

[@fubuloubu](/u/fubuloubu), would you agree on the statement above?

---

**fubuloubu** (2019-01-17):

For Vyper, we’ve discussed adding function-level recursion locks that would attempt and prevent mutal recursion between a set of contracts, but it would involve a lot of overhead and be too complex as to open a lot of attack surface in practice I think.

I really like the proposal of adding a callback-safe `transfer` opcode because it allows the developer an additional option to explicitly reduce their attack surface so they can protect themselves if a particular protocol would have safety issues that need to be protected. Re-entrancy is probably one of the most complex bugs possible with smart contracts, and I think giving protocol-level tools to protect against unintended behaviors is important to provide as it will actually mitigate the problem instead of band-aiding it as the 2300 gas stipend does.

This “callback-safe” version of `transfer` could allow `STATICCALL`s back but no mutating function calls. This might also be more broadly useful as an a method of calling, something like `FINALCALL` that does not allow mutating calls to itself after the call is forwarded e.g. “I don’t care what you do with this, but don’t come crawling back to me with it because I won’t be listening”.

I do agree with [@Arachnid](/u/arachnid) that this starts to break the “composable” behavior that developers tend to tout of Ethereum smart contracts, but it’s a trade of interoperability for safety that I think would be very helpful to developers.

I’ll caveat all of the above with “I am not a VM expert, and this all could be very difficult to design”.


*(41 more replies not shown)*
