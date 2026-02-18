---
source: magicians
topic_id: 18535
title: "RIP-7614: Expose call stack to contracts"
author: canercidam
date: "2024-02-07"
category: RIPs
tags: [evm, precompile, rip]
url: https://ethereum-magicians.org/t/rip-7614-expose-call-stack-to-contracts/18535
views: 3577
likes: 66
posts_count: 31
---

# RIP-7614: Expose call stack to contracts

Hi Magicians! ![:mage:](https://ethereum-magicians.org/images/emoji/twitter/mage.png?v=12) ![:magic_wand:](https://ethereum-magicians.org/images/emoji/twitter/magic_wand.png?v=12)

We would like to propose an improvement to increase visibility in L2 EVM execution.

https://github.com/ethereum/RIPs/pull/10

**What are the proposed changes?**

We propose a new call stack implementation to record opcodes, addresses and function selectors and expose them through a precompiled contract interface.

If implemented, the precompile will give protocols deeper visibility into addresses involved at any point in execution. The added visibility enables more robust exploit prevention mechanisms, including transaction screening.

**Why are we recommending this and how do we believe the user/developer experience will be improved?**

- This improvement is rooted in the authors’ common goal to prevent smart contract exploits.
- Transaction screening is an emerging and promising exploit prevention approach. Here’s an example - a DeFi protocol may screen incoming transactions against a negative reputation list and/or for anomalous activity outside of normal user behavior, and revert transactions deemed malicious.
- Unfortunately, transaction screening techniques are susceptible to evasion. DeFi protocols only have visibility into msg.sender and tx.origin fields of a transaction, meaning hackers can hide behind various proxies.
- We are recommending this improvement to enable more robust security mechanisms that collectively deliver great protection for DeFi protocols and user funds.

Eager to hear the community’s thoughts and feedback on this improvement. Your insights will be invaluable in refining the RIP. We’re looking forward to an insightful discussion!

## Replies

**aneurablock** (2024-02-07):

Hello Magicians community,

For the past two years, we’ve been working on machine learning models that enable the earliest detection of hacks, including zero-days, based on opcodes. Therefore, exposing the call stack to contracts opens the door to blocking malicious contract calls without affecting daily business operations. This allows for the creation of a new ecosystem of protection where different companies work with products that can detect and block malicious attacks, thereby protecting and enhancing the blockchain ecosystem. At NeuraBlock, **we are fully in support with [@canercidam](/u/canercidam)** of the need to implement opcode recording, addresses, and function signatures by exposing them through a precompiled contract interface to prevent attacks and avoid the obfuscation of malicious transactions.

---

**Idan-Levin** (2024-02-07):

This pre-compile is really important because the way the EVM is built today, exploit prevention solutions are really easy to avoid by using proxy contracts.

And if this won’t be changed, it just increases the motivation to insert a centralized middleman that can process the chain of contract calls offchain, and then to act as a firewall - which only opens the door to opaque policies and potential offchain censorship. Visibility into the contract calls history onchain is important so that threat prevention solutions will also live onchain, and not with opaque offchain logic.

---

**ernestognw** (2024-02-07):

I’m pretty sure this is the correct approach for on-chain security prevention. Right now we rely on off-chain mechanisms for security.

Thanks for putting everything together [@canercidam](/u/canercidam) !

---

**tkstanczak** (2024-02-08):

COI disclosure: I am a Forta Council member and Forta team has been working on preparing the proposal

I have reviewed the proposal contents, suggested some improvements to the early versions that were taken into account.

I support bringing the idea for the discussion at the core devs call as any topics on improvement of user security would be welcome.

---

**assafIronblocks** (2024-02-08):

as on-chain firewall builder i can say that having the ability to get the call trace can benefit on-chain security - which means more decentralized centric solutions (like on-chain phishing-blocker / sandwich-blocker) can use that without compromising the web3 ethos.

this ability can be used also for other purposes along with the security - account abstraction users and protocols can benefit from this especially with its first phases.

---

**hal2001** (2024-02-09):

Full disclosure: I am a Forta Council member and the Forta team preview this proposal with me.

My views: transaction screening is becoming critically important for exploit mitigation. We need these features on L2s as L2 usage grows—we won’t be able to safely scale L2 applications without these techniques.

This proposal seemingly has few downsides, and a lot of upside. Feels like an easy win for the ETH ecosystem.

---

**kaspaw** (2024-02-09):

I really like the effort and it’s definitely a step in the right direction. Without a deeper insight into the call stack, I doubt there is a way to effectively block malicious transactions on-chain.

This proposal does not compromise our ethos. It merely provides the devs with information that wouldn’t be accessible to them otherwise.

I support this idea. Thanks [@canercidam](/u/canercidam) for starting the discussion

---

**ArielTM** (2024-02-10):

This is a step in the right direction. On-chain prevention has proven to be the only way to effectively block malicious exploitation of smart contracts. Allowing observability to the call stack is one of the strongest tools in the protection arsenal

---

**kladkogex** (2024-02-12):

Arguments against would be

*- it can break composability and enable censorship. Basically a dapp would be able to censor other dapps along the call chain. *

*- it can enable new harder-to-analyze attacks since the attackers would be able to analyze stack info*

*- complexity of resulting code would make security audits more expensive*

Overall, modern languages that target security go into making things more simple vs making them more complex.

---

**ajbealETH** (2024-02-12):

Thanks [@kladkogex](/u/kladkogex). Can you expand on why security audits would be more expensive as a result of L2s adopting this precompile? The authors were envisioning this being implemented at the chain level, not the dapp level.

---

**kladkogex** (2024-02-13):

Well the price of the security audit depends on the complexity of stack.

If inside the code there are security protection that read information from outside the current function, auditing these protections will be really hard.

---

**ulerdogan** (2024-02-13):

It’s definitely a new approach for precompiles in terms of implementation and use-case, congrats on the proposal.

My questions are:

- It would be really nice to see some example use-cases by dApps to understand your vision for utilizing this precompile. Then, it will be easier to imagine how this is useful. I am curious how generalized precautions can be detected by utilizing CallStack. Also, even if generating CallStack is a negligible overhead, how do you expect the gas costs of utilizing CallStack. As a dApp developer, I can’t imagine how the CallStack can be analyzed or dApps can be designed to predict security issues.
- How much do you think this development appeals to all developers? I feel like it’s an additional and a bit complex security responsibility.
- Do you plan to provide the exact specs of the precompile contract itself? It should be defined in the proposal without the need for reference implementation.

My recommendation is:

I expect the precompiles as pure functions to replace some other functions in a smart contract which consumes huge amount of gas or be able to execute some functionalities that cannot be achieved by Solidity etc. Also, the reference implementation itself shows that this precompile should have a divergent implementation than other precompiles.

- Is there a specific reason that you have used a precompiled contract to expose the CallStack?
- Can the same functionality be provided by a new Opcode?

---

**canercidam** (2024-02-13):

Thanks a lot for the feedback [@ulerdogan](/u/ulerdogan) -  great questions!

> It would be really nice to see some example use-cases by dApps to understand your vision for utilizing this precompile. Then, it will be easier to imagine how this is useful. I am curious how generalized precautions can be detected by utilizing CallStack. Also, even if generating CallStack is a negligible overhead, how do you expect the gas costs of utilizing CallStack. As a dApp developer, I can’t imagine how the CallStack can be analyzed or dApps can be designed to predict security issues.
> How much do you think this development appeals to all developers? I feel like it’s an additional and a bit complex security responsibility.

The screening mechanism implemented in the target/victim protocol contract (e.g. with the help of a Solidity library) would be retrieving the call stack through the precompile interface. So it could either be adopted with custom screening logic or by using a screening library that uses the precompile.

Such screening logic would need to do checks on the addresses i.e. read storage. Transactions of a regular user is simple enough that the amount of addresses and the call stack depth remains at a low level. So the gas cost of screening (precompile call + checks) remains small. If screening cost somehow scales, then it only hurts an attacker that sends a complex transaction. In any case, we consider these checks out of scope of this proposal since the only goal is providing more visibility to the protocol contracts. ![:slightly_smiling_face:](https://ethereum-magicians.org/images/emoji/twitter/slightly_smiling_face.png?v=12)

> Do you plan to provide the exact specs of the precompile contract itself? It should be defined in the proposal without the need for reference implementation.

The proposal has two technical components: a call stack, and a precompile interface that exposes it. We outline in the Specification:

- how the call stack should be defined and updated, without definining concrete client implementation details,
- how the precompile interface should encode the call stack data and return to the caller in EVM.

We could do a little bit more explaining in the Specification if you feel that some bits are unclear.

> Is there a specific reason that you have used a precompiled contract to expose the CallStack?
> Can the same functionality be provided by a new Opcode?

Same question crossed my mind during the development of this proposal and, yes, the same functionality could be provided as an opcode but there are two challenges with it:

- Adopting a new opcode is much harder than adopting a new precompiled contract. Testing custom opcodes are not easy and Solidity compiler would require changes to support it.
- Evolving a precompiled contract is easier. If a future proposal suggests that the call data should be extended with new fields, then the encoding logic would have to change. Maintaining backwards compatibility after such changes in a precompiled contract is easier as all we have to do would be making the precompile accept a flag to turn on the new fields, and keep the old encoding if the flag is not provided. Maintaining this with an opcode looks harder.

---

**mratsim** (2024-02-14):

I don’t see how you would even start to prove this in ZK in an efficient manner.

When proving something with dynamic size, you need to prove all code paths, all sizes.

Here, everything is dynamic and as gas cost increases, you would have an exponential amount of possible states to prove.

This looks also like quite tricky to get right, test and fuzz and looks like very bug prone. In regular programming, manipulating the stack is very tricky to get right, see discussions around longjmp and setjmp.

In general, opcodes that are non-deterministic are avoided in the EVM, which is why there are proposal such as [EIP-3690: EOF - JUMPDEST Table](https://eips.ethereum.org/EIPS/eip-3690) ([EIP-3690: EOF - JUMPDEST Table](https://ethereum-magicians.org/t/eip-3690-eof-jumpdest-table/6806)) to ease execution analysis. This precompile goes in the complete opposite direction.

Finally all the other precompiled contracts are pure functions, with very well understood results. This one looks like even more complex than feu SELFDESTRUCT.

---

**canercidam** (2024-02-14):

Hi [@mratsim](/u/mratsim), thanks a lot for the feedback! We find the adoption of this precompile by zkEVM rollups very important.

We are proposing a call stack that is:

- completely separate from the stack used in every call frame,
- is a singleton per EVM transaction simulation and not redefined every frame,
- manipulated only by CALL, CALLCODE, DELEGATECALL and STATICCALL opcodes upon enter (push) and exit (pop),
- exposed through a precompiled contract interface.

> When proving something with dynamic size, you need to prove all code paths, all sizes.

> Here, everything is dynamic and as gas cost increases, you would have an exponential amount of possible states to prove.

If execution of CALL, CALLCODE, DELEGATECALL and STATICCALL can be proven, I wonder why the call stack could not be, given that the call stack state at any point could be deriven by looking at the opcodes that appear in the trace.

> This looks also like quite tricky to get right, test and fuzz and looks like very bug prone. In regular programming, manipulating the stack is very tricky to get right, see discussions around longjmp and setjmp.

We propose that it is only the opcodes which I listed above manipulate the call stack - nothing else. The variety of pushed and popped data is very limited and it is done by the opcodes. Would you still agree that it is still hard to test and bug prone?

> Finally all the other precompiled contracts are pure functions, with very well understood results. This one looks like even more complex than feu SELFDESTRUCT.

The “precompile” is an interface that merely reflects the current state of the call stack. It only encodes an array of elements, which is a very predictable process. The reason why we choose a precompile interface is because it looks easier to adopt and evolve.

We are very curious to know if there is anything we can do to make the call stack and the precompile more ZK friendly. Looking forward to hearing more suggestions about this, thanks!

---

**rpolysec** (2024-02-14):

I don’t understand the implementation enough to comment, but after reading the dialogue here I’m also interested in seeing several concrete examples of how widely useful this would be. I’ve spent a lot of time in detection engineering for traditional cyber security and often we look for the OS to expose features that we think will make detection easier and after much effort we find there are actually very few use cases. I would like to see half a dozen or more concrete use cases with teams of developers outside of OpenZeppelin and Forta demonstrating how this would be a game changer vs. what is currently possible.

I’m also quite concerned about potential abuses. I would need a whole lot more detail before being comfortable supporting this.

---

**shemnon** (2024-02-14):

Some specific feedback on the RIP

- The scope of the operations needs to be expanded, at least to CREATE and CREATE2, as those also create message frames.  Perhaps make it a general statement like “All operations that create a new message frame MUST push a Call to the CallStack. In the Cancun fork specification this list is CALL, CALLCODE, DELEGATECALL, STATICCALL, CREATE, CREATE2, and the initial call frame of a transaction.”
- There needs to be a way to distinguish create transactions from call transactions.  Perhaps a pseudo opcode?
- What about contracts that are hand written, or Fe, or other languages that do not follow the Solidity ABI? Such as MoveVM cross compiled to EVM, for example? Will signature checks be validated against new languages?
- How are function signatures identified?  There is a large amount of Solidity ABI explicitly required by this spec, which is not good. A section describing how to retrieve that independent of anything outside the EVM needs to be included.  such as “The signature is the first four bytes of the call data for the message frame for CALL style opcodes, zero extended if necessary.  For Create style opcodes it is

”.  But per the prior point, are these reliable function signatures?
- The function signatures can be faked, or collisions found. Access to the entire input arguments may be needed.
- Java used to rely on stack checking extensively in it’s Applet sandbox defenses. The string of Applet exploits in the early 2010s usually involved a previously unknown and clever way to overcome the stack checking. Considering how composable Ethereum is I expect a lot of the techniques are portable.

---

**0xalpharush** (2024-02-14):

I would like to see several specific examples of how this would be used in practice perhaps with past hacks as an example. It’s not really clear what class of bugs this is meant to prevent and why catching them at runtime is preferable to during development using static and/or dynamic analysis. Potentially, simple mechanisms like the one used by Arbitrum Stylus to detect reentrancy at runtime could be used depending on the motivation.

As it stands, aside from preventing interactions with specific addresses based on off-chain heuristics, I would argue that any security property that is violated is incorrect in it of itself and would warrant fixing instead of relying on this functionality. Adding precompiles that are only enabled on rollups involves rollups e.g. Arbitrum and Optimism each configuring their forks of go-ethereum to activate in hard forks and I haven’t seen any discussion of alternatives that would be more straightforward to maintain and not risk consensus issues e.g. activating the precompile on mainnet or prematurely on the rollups.

Additionally, I think that the added complex of reasoning about call stacks for developers, tooling (fuzzers and formal verification, for instance), and ZK proving (as others already noted) is under appreciated. For instance, the dynamic cost of calling the precompile is just one more consideration that must be examined carefully on top of the already complex gas accounting in the EVM and how it interfaces with Solidity. Now, every tool must implement support for this standard and have the ability to toggle it on/off based off the rollup and EVM version. This has already been error prone coordinating across solc, hardhat/foundry, and rollups for PUSH0; however, this could be said for any RIP and maybe is a separate discussion.

---

**ajbealETH** (2024-02-14):

Thanks for the feedback [@rpolysec](/u/rpolysec). Just a reminder that the precompile by itself is neutral. It is simply exposing call stack data to protocols that is already available to the caller, block builders, etc.

One exciting use case for the precompile is supporting exploit prevention; however, it must be paired with a screening solution (of which there are several that benefit from this add’l visibility) before it can have an impact. The authors aren’t suggesting a specific approach - there are pros and cons to negative reputation, positive reputation and anomaly-based screening. Screening is possible today, but it’s less robust than it could be due to the limited visibility dapps have into the call stack.

We’ll pull together some material on the impact on exploits. In the meantime, would like to understand some of the abuse patterns you are thinking about. Can you share more?

---

**ArielTM** (2024-02-14):

Some thoughts about how this will improve security:

1. Efficient Reentrancy guard - Today, reentrancy guard is implemented using modifiers and a dedicated storage slot. Using the precompile will enable a more gas-friendly reentrancy check and will also reduce the problems caused by bad integration of the current reentrancy guard solutions (we’ve summarized some of the less effective reentrancy guard integration here - https://www.spherex.xyz/post/reentrancy-guard-2-0 )
2. Static Reentrancy Guard - Utilizing the precompile will introduce, for the first time, a countermeasure to combat static reentrancy attacks (which wasn’t possible since reentrancy guard uses a storage slot) - see https://www.youtube.com/watch?v=8D5ZJyU-dX0 )
3. In the context of SphereX - We have a unique approach of analyzing a given protocol history and checking during execution of future transactions that the transaction effect on the protocol doesn’t differ from how the protocol used to operate (in a nutshell). Let’s take the Poly hack as example. Our on-chain engine would have been able to notice, using the precompile, that this is the first time putCurEpochConPubKeyBytes was called from EthCrossChainManager (of course, this would have been detectable using msg.sender, but think of the generalized case) and actually revert this transaction

We’ve analyzed numerous of previous hacks and proved our solution could have prevented them. Using the precompile increases the number of ways we can check transactions against the protocol history.


*(10 more replies not shown)*
