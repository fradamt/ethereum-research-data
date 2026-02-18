---
source: magicians
topic_id: 21615
title: "EIP-7809: Native Tokens"
author: PaulRBerg
date: "2024-11-07"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-7809-native-tokens/21615
views: 570
likes: 29
posts_count: 16
---

# EIP-7809: Native Tokens

Discussion topic for EIP-7809 [Add EIP: Native Tokens by PaulRBerg · Pull Request #9026 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/9026)

#### Update Log

- 2024-11-07: initial draft
- 2024-11-08: EIP-7809 number assigned, dropped “Multiple” from name

#### External Reviews

None as of 2024-11-07.

#### Outstanding Issues

None as of 2024-011-07.

## Replies

**microbecode** (2024-11-08):

An interesting suggestion! I feel this definitely goes into a good direction, but I wonder how “feasible” it is to get this implemented? There is a lot of new functionality required (opcodes).

I don’t have any idea how difficult it is nowadays to get new opcodes. Do you?

---

**shemnon** (2024-11-08):

While there may be technical advantages to this approach, what does this proposal add that would otherwise be impossible with smart contract tokens as they exist in the EVM today?

i.e. what does EIP-7809 do that Cancun-era EVM cannot?  Apart from gas efficiency.

---

**wjmelements** (2024-11-09):

I’m not a fan of putting native tokens into the EVM.

One motivation you are missing is that standardizing token behavior prevents categories of undefined behavior rampant in ERC20, making tokens safer to use and more predictable.

> By embedding token balances into the VM state, the cumbersome process of approving tokens before transferring them is
> eliminated. Token transfers can be seamlessly included into smart contract calls, simplifying transaction flows and
> reducing the number of steps users must take. This streamlined process not only enhances the user experience but also
> reduces gas costs associated with multiple contract calls, making interactions more efficient and cost-effective.

Gas costs reflect cost to the system and are not valid motivation unless the cost to the system has itself been reduced.

Several token standards have implemented transferAndCall. One of them is ERC-677. Why don’t you use them? It should be pretty easy to make wrappers for ERC-20 tokens such that they gain the functionality you want.

> Storing token balances in the VM state unlocks the potential for sophisticated financial instruments to be implemented
> at the protocol level. This native integration facilitates features such as recurring payments and on-chain incentives
> without the need for complex smart contract interactions. For instance, platforms could natively provide yield to token
> holders or execute airdrops natively, similar to how rollups like Blast offer yield for ETH holders. Extending this
> capability to any token enhances utility and encourages users to engage more deeply with the network.

Current programmability is sufficient. I’m not convinced this enables anything that isn’t already possible.

---

**wjmelements** (2024-11-11):

The `CALLVALUES` opcode returning a variable number of stack items sounds difficult to use, even with the size on top. Usually variable-length returns are put into memory. In particular there doesn’t seem to be a way to check if there are any callvalues without polluting the stack. Consider the number of operations required just to check this:

```evm
CALLVALUES
JUMPI(clearstackarr, DUP1)
hasnone:
POP
// ...
clearstackarr:
POP(SWAP1)
JUMPI(clearstackarr, DUP1)
hasany:
POP
// ...
```

How would `CALLVALUE` be affected? Its behavior isn’t mentioned. I would hope that it still only refers to the one true native currency for backwards compatibility.

`NTCALLCODE` seems insufficiently defined. If its purpose is to correspond to `CALLCODE`, it should be removed from the spec. `CALLCODE` is deprecated in favor of `DELEGATECALL`.

---

**Dexaran** (2024-11-13):

[@PaulRBerg](https://github.com/PaulRBerg) what this opcode should do?

`NTCALL - 0xb4` `NTCALLCODE - 0xb5`

(I suppose they act similar to call and callcode but the behaviour/logic of the opcodes is not written in the proposal, just the args)

Also, why is the transferring method so overcomplicated?

- transferred_tokens_length: the number of transferred tokens
- The list of transferred_tokens_length (token_id, token_amount) pairs
- argsOffset: byte offset in the memory in bytes, the calldata of the sub context
- argsSize: byte size to copy (size of the calldata)
- retOffset: byte offset in the memory in bytes, where to store the return data of the sub context
- retSize: byte size to copy (size of the return data)

I guess the idea was to let tokens be transferred with just one transaction but this overcomplicates the logic of transferring significantly and I can envision a huge number of mistakes the implementers will be making with that.

I would be in favour of keeping the logic as clean and simple as possible. Only allow 1 token to be transferred at a time, so that you would only need `gas`, `address`, `token_id`, `quantity` and `data`. No offsets, no lists in args.

---

**Dexaran** (2024-11-13):

> One motivation you are missing is that standardizing token behavior prevents categories of undefined behavior rampant in ERC20, making tokens safer to use and more predictable.

ERC-20’s “undefined behavior” resulted in a situation where we have an insecure token standard with lack of error handling possibility.

- $16,000 were lost because of this issue in 2017.
- $2,000,000 were lost in 2018
- $60,000,000 were lost in 2023
- $90,000,000 on 1 Nov, 2024
- $115,000,000 today (one user lost $25M)

Source: [ERC-20 Losses Calculator](https://dexaran.github.io/erc20-losses)

In the light of how the situation is developing I can conclude that any token standard that does not cause users to keep losing millions of dollars for years would be better than ERC-20 and this alone could justify this proposal.

Side note on ERC-1155, ERC-677 (and 777), ERC-1363: any token standard that claims to be “backwards compatible” with ERC-20 is insecure as well.

The problem with ERC-20 is that it violates “error handling” and “failsafe defaults” principles of secure software development principles. [7 Principles of Secure Design in Software Development | Jit](https://www.jit.io/resources/app-security/secure-design-principles)

If a token standard implements `transferAndCall` but keeps the `transfer` function the same way it is implemented in ERC-20 without redefining its logic - it still violates the principle of failsafe defaults and will inevitably result in a loss of money.

---

**wjmelements** (2024-11-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dexaran/48/10810_2.png) Dexaran:

> If a token standard implements transferAndCall but keeps the transfer function the same way it is implemented in ERC-20 without redefining its logic - it still violates the principle of failsafe defaults and will inevitably result in a loss of money.

The native transfer mechanism inherited by the proposal can’t block transfer because accounts without code cannot reject transfers. One advantage of coded tokens over native tokens is that they can implement standards and mechanisms that people want to use rather than forcing a one-size-fits-all standard that can only be improved by hard fork.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dexaran/48/10810_2.png) Dexaran:

> ERC-20’s “undefined behavior” resulted in a situation where we have an insecure token standard with lack of error handling possibility.

The undefined behaviors that I was referring to are innate to the freedom of implementation rather than to ERC20. Some examples I’ve encountered:

- preventing sell (and other blacklist mechanisms)
- transfer taxes
- minimum balances
- preventing adjustment of allowance
- selfdestruct
- rebased balances (usually with numerator and denominator)

I don’t think this freedom is so bad but eliminating the possibility of malicious features is a plus that should be mentioned in the motivation.

---

**u59149403** (2024-11-18):

This EIP is totally awesome! Please, try hard to advertise it. Here is copy of part of my comment `https://gist.github.com/Dexaran/9bd90c1885b4818573368ad02b784125?permalink_comment_id=5288645#gistcomment-5288645` (and then I will tell what you need to add):

---

I think native tokens (EIP-7809) is way to go (yes, I changed my opinion on native tokens). Native tokens have many advantages over ERC-223 tokens, and thus native tokens actually have chance to become widespread. And native tokens solve problems, which ERC-223 intends to solve.

- First of all, if native tokens are implemented in EVM, then they will be considered “official” by everyone and everyone will support them
- Native tokens implemented directly in nodes, and thus they are very cheap in terms of gas
- As I said above, native tokens will be “official”, and thus they will be supported in Solidity. So, you will be able to write payable functions in Solidity, which accept tokens. Thus you will not have double ABI encoding problem of ERC-223, i. e. you will not need to encode arguments to bytes data. You will get clean type safe experience. (Unfortunately, as well as I understand, EIP-7809’s Solidity fork doesn’t implement payable. I think this is a mistake.)
- Node implementations can “see” native tokens, and thus nodes can implement optimizations, which are impossible with ERC-20 and ERC-223 tokens. For example, balance can be stored in owning account (in implementation), not in token contract. This will cause major efficiency gains, because ERC-20 tokens are responsible for huge share of Ethereum state (see figure 2 here: https://www.paradigm.xyz/2024/03/how-to-raise-the-gas-limit-1 )
- When you do ERC-223 transfer, you call untrusted transfer function, which then calls untrusted tokenReceived function. This is bad for security, and opens door for reentrancy attacks and other attacks. And you cannot be sure that transfer will actually execute tokenReceived. You cannot be sure that token contract will not take some fee. With native tokens transfer is implemented directly in nodes, transfer causes execution of receiving function, but it does not cause execution of untrusted code of token itself. Thus, security is improved. Moreover, if you transfer tokens to EOA, then no external code is executed at all!

---

Now let me tell you **what to add**.

First of all, we need feature parity with ERC-20. ERC-20 has transfer logs, and thus native tokens need something similar, too. So you should ensure that JSON-RPC allows one to read token transfer history.

Then: as I said above, `payable` Solidity functions are mandatory.

Then: it may be good idea to introduce native tokens in the same time as EOF ( `https://github.com/ipsilon/eof/blob/main/spec/eof.md` ). So we will have a chance to change opcodes in breaking way. We will have a chance to change semantic of `CALL` instead of adding `NTCALL`.

Then: currently “Motivation” section is not motivating at all. It is vague. I suggest removing it and rewriting from scratch. Focus on technical advantages. And there are a lot of them! I listed them above, feel free to copy. Additional motivations:

- Native tokens solve ERC-20 problems. First of all, awkward “approve + transferFrom” pattern. Second, native tokens solve problem of approval-related insecurity. Then, NTs solve problem of “stuck” ERC-20 tokens ( https://gist.github.com/Dexaran/9bd90c1885b4818573368ad02b784125 )
- Vitalik says here ( https://hackmd.io/@vbuterin/selfdestruct ): “SELFDESTRUCT is the only opcode which can change other accounts’ balances without their consent… This risks breaking smart contract wallets, breaks other potentially useful tricks, and generally is yet another edge case that contract developers and auditors need to think about”. So, Vitalik says that impossibility to send someone money without their consent is important property. And I agree with him. And, as well as I understand, native tokens provide this invariant! (Assuming SELFDESTRUCT will be deleted.)

Then: “Cross-Contract NT Transfers” - I fully disagree with your solution here. Instead, this EIP should be implemented such way, that existing contracts should reject transfers of any native tokens, except for ETH. I. e. rejection should be default. I. e. specially designed contracts only should accept other native tokens.

Then: as I already said on Github, ETH’s id should be `0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee`, not zero. Also, I just found that this is requirement by ERC-7528.

Then: total supply for ETH should be tracked the same way it is tracked for other native tokens. I don’t see any reasons for making ETH special. Yes, this will be possibly major technical task, and it is possible it will even require changes to consensus layer nodes. But still this task is solvable, and there is no any fundamental reasons not to solve it

---

**wjmelements** (2024-11-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/u59149403/48/13764_2.png) u59149403:

> Then, NTs solve problem of “stuck” ERC-20 tokens

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/u59149403/48/13764_2.png) u59149403:

> SELFDESTRUCT is the only opcode which can change other accounts’ balances without their consent

This isn’t true. A codeless account cannot give affirmative consent because it can’t say no. What he meant was that accounts with code can reject transfers but not selfdestruct (and `COINBASE` rewards such as gas fees and the block subsidy).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/u59149403/48/13764_2.png) u59149403:

> Then: as I already said on Github, ETH’s id should be 0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee, not zero. Also, I just found that this is requirement by ERC-7528.

There are compression advantages to using `0`, and those gas advantages should belong to the true native token, ETH. ERC-7528 is a request for comment, and some of its rationale is wrong:

> Ultimately, all of these addresses collide with potential precompile addresses and are less distinctive as identifiers for ETH.

`0` does not collide with a precompile and is the logical location for a future native token precompile.

---

**shemnon** (2024-11-19):

To double down on [@wjmelements](/u/wjmelements) concerns about CALLVALUES, runtime variable stack inputs and outputs make EOF stack validation impossible.  And stack validation is a key speed unlock for zk representation of a transaction.

If variable amounts of NTs are desired then an immediate argument could be use to express how many NT pairs to use, but that would need to be hard coded into the code, and not dynamic on the stack.  Note also that more than one operand returned from an opcode is also novel within the EVM, but not nearly as problematic as a dynamic stack return based on stack values.  So a statically scaled number of input and output operands may be tolerable, a value that is dynamic based on stack values is no bueno.

So based on the opcode definitions alone I would move to reject this from being adopted in mainline EVMs, independent of any other suitability issues.

---

**wjmelements** (2024-11-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> Note also that more than one operand returned from an opcode is also novel within the EVM

In the [yellowpaper](https://ethereum.github.io/yellowpaper/paper.pdf) the SWAP`N` opcodes are defined as having `N` input and output operands. I find it easier to think of them as [having no operands](https://github.com/wjmelements/evm/blob/748ae9c3d4eea170e3edcd45ad074940e5291f33/include/ops.h#L151) but thinking of them as operands simplifies stack validation. Otherwise you’re right.

---

**shemnon** (2024-11-20):

Oh yea, SWAPN.   The exception that proves the rule.

My headspace was that swaps don’t create new data, just shuffle it, so it didn’t “count.”  But the novelty in these opcodes is that each new operand is new data, not just shuffled data.

---

**codebyMoh** (2024-11-21):

Are we really considering the extra opcodes to be added more. Native token can be a good thing for a longer term, but does it come with complexity of states management in contracts?

---

**sullof** (2024-11-22):

I worked for the Tron Foundation in 2018/19. One of the differences between the EVM and the EVM Tron variation that I liked more was native tokens (i.e., TRT10). They offered a lot of advantages over ERC20 tokens. It would be great to see that finally in Ethereum.

---

**Dexaran** (2024-11-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/u59149403/48/13764_2.png) u59149403:

> “Cross-Contract NT Transfers” - I fully disagree with your solution here. Instead, this EIP should be implemented such way, that existing contracts should reject transfers of any native tokens, except for ETH. I. e. rejection should be default. I. e. specially designed contracts only should accept other native tokens.

This is the most important thing here - make default behaviour fail-safe.

Again, there are well-known widely adopted practices in software security known as “Security by Default” or “Fail Safe Defaults”

> Security by Default
> Secure by default means that the default configuration settings are the most secure settings possible. This is not necessarily the most user-friendly settings.

> Fail Safe
> This is a security principle that aims to maintain confidentiality, integrity and availability when an error condition is detected. These error conditions may be a result of an attack, or may be due to design or implementation failures, in any case the system / applications should default to a secure state rather than an unsafe state.

[OWASP Developer Guide | Principles of Security | OWASP Foundation](https://owasp.org/www-project-developer-guide/draft/foundations/security_principles/#:~:text=For%20example%20unless%20an%20entity,or%20'Secure%20by%20Default').

If you were to take the approach of allowing NT to be transferred into smart contracts by default without requiring the contract to explicitly declare its ability to handle the transfer, then it would violate two core security principles and cause financial harm to end users.

