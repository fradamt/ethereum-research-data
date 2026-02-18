---
source: magicians
topic_id: 12113
title: "EOF proposal: ban code introspection of EOF accounts"
author: vbuterin
date: "2022-12-12"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eof-proposal-ban-code-introspection-of-eof-accounts/12113
views: 8853
likes: 30
posts_count: 23
---

# EOF proposal: ban code introspection of EOF accounts

One of the arguments against any EVM changes is that it’s much harder to add features to the EVM than to remove them (eg. the complexities around even removing a little-used opcode like `SELFDESTRUCT`), and so if the EVM keeps changing, ever-increasing ugliness and complexity is likely to be the outcome.

One way to greatly reduce this tradeoff is to find a way to automatically convert version `n` EVM code to version `n+1` EVM code every time there is an upgrade (not necessarily immediately; perhaps convert when old code is “touched”, and make sure that all version `n` code is converted to version `n+1` before attempting to implement version `n+2`).

But there are difficulties in the current EVM that make conversion hard:

- Dynamic jumps, which generate code coordinates to jump to at run time, making it hard to transform code
- CODECOPY, EXTCODECOPY and EXTCODEHASH, which read code directly

EOF is an upgrade to the EVM, and so it has the downsides that I mentioned. But there is one way to adjust EOF to make it much better in this regard, by setting the stage for a system where any *future* EVM upgrades do not have these problems, and so force-conversion becomes possible:

**Ban EOF-formatted code from being read with `CODECOPY`, `CODESIZE`, `EXTCODECOPY`, `EXTCODESIZE` and `EXTCODEHASH`**.

Fortunately, EOF bans dynamic jumps already, making code transformations easier. But banning code *reading* would let us go all the way. If we decide to change from the EVM to some other VM (eg. WASM, Cairo…) in the future, it would be possible to automatically transform EVM code into code of the new VM that has equivalent functionality.

Specific changes that would be needed would be:

- Remove CODECOPY and CODESIZE from the EIP-3670 valid opcode list
- The EXTCODECOPY opcode would check if the code it is reading starts with the EIP-3541 magic byte. If it does, it would:

Option 1: act as if the code is zero
- Option 2: raise an exception

**The `EXTCODEHASH` and `EXTCODESIZE` opcodes**, when acting on code that starts with the [EIP-3541](https://eips.ethereum.org/EIPS/eip-3540) magic byte, can be treated in two different ways:

- Option 1a: return zero
- Option 1b: throw an exception
- Option 2: no change, but we make a commitment that the EXTCODEHASH and EXTCODESIZE opcodes returns the keccak and size of the full code, and these values may change as code gets upgraded

Some optional additions (which could be added later) include:

- The code reading opcodes could have their functionality changed to read the data section of the code, or the empty string if the data section is absent (EIP-3540 gives EOF-formatted contracts the right to have up to one data section)
- A CREATE4 opcode that copies the code of an existing address (in a similar way to how DELEGATECALL works), though it could still use a memory slice for the data field. The “recommended” pattern for developers would be that new code templates would get pushed with a manual transaction, and anything automated would just copy a template. Use cases like creating lots of contracts with small modifications (eg. user wallets with different public keys) would be accomplished with this data field.

## Replies

**Pandapip1** (2022-12-12):

I like this idea, but I wonder if there’s a simpler way to do this. Here’s my naive idea: different “EVM versions,” where changes to opcodes apply only to new EVM versions (unless there’s a good reason not to). I imagine there’s a good reason why this isn’t a good idea, but I’d just like to throw it out there anyway.

---

**SamWilsn** (2022-12-12):

Why do we need to disable the code reading opcodes to enable this? Couldn’t we preserve the original bytes alongside any transpiled version? I assume it’s to save storage space, and if so, how bad would it be to keep both?

---

Did you exclude `CODESIZE` (`0x38`) and `EXTCODESIZE` (`0x3B`) intentionally?

---

How do we plan to handle existing non-EOF contracts? Turn them off? Keep the current introspectable EVM forever, but only ever keep one opaque EVM?

---

**vbuterin** (2022-12-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pandapip1/48/5511_2.png) Pandapip1:

> I like this idea, but I wonder if there’s a simpler way to do this. Here’s my naive idea: different “EVM versions,” where changes to opcodes apply only to new EVM versions (unless there’s a good reason not to). I imagine there’s a good reason why this isn’t a good idea, but I’d just like to throw it out there anyway.

The problem with having new versions is that the EVM spec would need to keep having those versions, and so as the EVM keeps evolving the de-facto spec size that clients have to implement will keep increasing forever. This is what I am desperately hoping we can get away from.

> Why do we need to disable the code reading opcodes to enable this? Couldn’t we preserve the original bytes alongside any transpiled version? I assume it’s to save storage space, and if so, how bad would it be to keep both?

I guess this could work, though it would come at a cost of an extra 24000 bytes per account. It would also be much less elegant. Like, it seems clear to me that the correct way to do this if we created the EVM from scratch would be to have an executable-but-opaque code section and a readable-but-unexecutable data section, and my data field proposal tries to move the EVM in this direction.

Obviously when we convert *existing* (pre-EOF) contracts into some new EVM version, we would need to put the entire old code into the data field for backwards-compatibility reasons.

> How do we plan to handle existing non-EOF contracts? Turn them off? Keep the current introspectable EVM forever, but only ever keep one opaque EVM?

My first instinct is:

Stage 1: keep the current EVM around, and work on the EOF EVM, so we have two versions (and temporarily three versions during upgrades)

Stage 2, when we have more spare time: do the work to translate existing EVM contracts into the EOF EVM, and accept the inefficiencies (redundancy from the entire code being in the data field, and having to transalate every dynamic jump into a case-switch-like statement with a jump table)

> Did you exclude CODESIZE (0x38) and EXTCODESIZE (0x3B) intentionally?

Ah no, it was a mistake to exclude those.

---

**xinbenlv** (2022-12-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> One way to greatly reduce this tradeoff is to find a way to automatically convert version n EVM code to version n+1 EVM code every time there is an upgrade (not necessarily immediately;

I wonder if this goal conflicts with the other goal that a given contract address will always behave the same, and if so, how do we resolve this conflict.

[For example](https://ethereum-magicians.org/t/almost-self-destructing-selfdestruct-deactivate/11886/13): In the case when some developers use SELFDESTRUCT for upgrade pattern in EVM version n, then the EVM version n+1 bans SELFDESTRUCT. how do we picture the “auto-convert” work in this case?

---

**vbuterin** (2022-12-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/16173_2.png) xinbenlv:

> For example: In the case when some developers use SELFDESTRUCT for upgrade pattern in EVM version n, then the EVM version n+1 bans SELFDESTRUCT. how do we picture the “auto-convert” work in this case?

There are two possible paths:

1. Make a complicated judgement call between transition costs and long-term simplicity, like we are doing today with SELFDESTRUCT.
2. Try really hard to find a way to transform code to have equivalent behavior but not use the opcode.

One example of (2) would be, if we decide that `KECCAK` should be a precompile and not an opcode, then code could be transformed so that every use of the `KECCAK` opcode gets turned into a precompile call. There are nuances around doing this (particularly, you’d need to agree on a region of memory to use, and `MSIZE` would have to be translated), but it could be done, and the transformation could even be formally proven.

So having a non-introspectable EVM increases the tradeoff space to be between 3 options (accept transition costs, accept long-term ugliness, do a possibly more complicated code transformation) rather than just 2 options.

---

**xinbenlv** (2022-12-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> if we decide that KECCAK should be a precompile and not an opcode, then code could be transformed so that every use of the KECCAK opcode gets turned into a precompile call. There are nuances around doing this (particularly, you’d need to agree on a region of memory to use, and MSIZE would have to be translated), but it could be done, and the transformation could even be formally proven.

Thanks for offering the examples and thoughts.

The examples can be categorized in two groups:

1. Like deprecating SELFDESTRUCT: the kind of change introduced to EVM that cause a behavior change which have no equivalent in newer version
2. Like hypothetically change KECCAK from opcode to precompile, this kind of change that have equivalent in newer version.

More often than less I saw those changes that could making EVM cleaner is done by removing an existing opcode, another example [EIP-2488: Deprecate the CALLCODE opcode](https://eips.ethereum.org/EIPS/eip-2488). A lot of time they don’t seem to have a future equivalent, which is the intention of such deprecations.

Now if we ban code introspection, it seems we will be on the path to define a new abstract level above opcode, regardless of we like it or not, because we need to have some layer semantically developers and client implementation can agree on what they mean. E.g. in the the `KECCAK` case, a new abstraction layer is implied in the description when you offer the example, that when developer use something like “KECCAK”, there is a mutual consensus developers convey to EVM implementations that they need to achieve KECCAK behavior regardless whether its’ archived by precompile or opcode.

If this hypothesis is true (that there will be an abstract layer), there is a possibility that ultimately the potential new abstract layer becomes hard to remove feature from. I wonder…

---

**vbuterin** (2022-12-12):

> e.g. in the the KECCAK case, a new abstraction layer is implied that when developer use something like “KECCAK”, there is a mutual consensus they convey to EVM implementations that they need to achieve KECCAK behavior regardless whether its’ archived by precompile or opcode. If this hypothesis is true, there is a possibility that ultimately the potential new abstract layer becomes hard to remove feature from. I wonder…

Isn’t that higher abstract layer just solidity (and vyper, and…)? Of course it’s difficult to remove features from those languages, though it’s easier than removing from consensus, because existing applications keep working the way they worked before.

> Like deprecating SELFDESTRUCT: the kind of change introduced to EVM that cause a behavior change which have no equivalent in newer version

Well *actually*, you could do something crazy, like turn every contract that contains `SELFDESTRUCT` into a delegatecall forwarder whose storage has an internal nonce that gets keccaked into storage accesses and that gets incremented every time a “selfdestruct” happens so that the contract gets a new storage space. Though to be fair, that would be exceedingly complicated and it would require a bunch of off-chain tooling to update.

---

**xinbenlv** (2022-12-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> Isn’t that higher abstract layer just solidity (and vyper, and…)?

If we can agree per this proposal there *WILL* be a higher abstract layer, it could be solidity or vyper or anything, but there difference is that:

Today before this proposal: solidity and vyper doesn’t need to agree upon each other because they know they will agree on the layer of EVM (execution layer) which is the layer enforcing a “semantic layer for identical code behavior” (I’d avoid using “consensus” with “layer” in this discussion in case people confuse it with “the consensus layer”)

After this proposal: the new higher abstract layer becomes the new semantic layer for identical code behavior.

It seems possible as we are getting rid of the old devil blocking EVM upgradability by introducing this

new semantic layer for identical code behavior as a new possible devil which is still hard to deprecate feature. It seems to me that the hardship to deprecate features in EVM is not because its in EVM, but because it is in some layer that require (1) consensus of meanings between clients and code and (2) backward compatibility. There seem to be a dilemma between (1) and (2).

---

**vbuterin** (2022-12-12):

OK then I guess I’m not sure I understand what you mean by “higher abstract layer”.

You don’t actually need any kind of higher layer to be able to show that a transformation `t(version N code) -> {version N+1 code}` preserves equivalence. You just directly show that the outputted code executed in version N+1 has equivalent behavior to the inputted code executed in version N.

This is similar to how you can convert between kilometers and miles without having some “higher layer” of abstract farawayness that everyone agrees on as an ultimate benchmark of distance. You just provide the transformation between distance in kilometers and distance in miles, and show that it’s a consistent one.

---

**Recmo** (2022-12-12):

I like how a stricter adherence to Harvard architecture allows transparently upgrading the contract bytecode. Two not yet mentioned instructions that break strict Harvard are `CREATE` and `CREATE2`. Here the payload is dynamically generated EVM bytecode to be deployed. In case of `CREATE2` to be deployed at a payload dependent address.

Two solutions I see:

1. When upgrading contracts containing CREATE, keep the original bytecode but translate on each deploy. This is semantically conservative and reasonable straightforward. And can be done two ways:
1a. The translation can be part of the n+1 EVM semantics. So n+1 EVM has some method to do translation that get called as part of translated CREATE. But this somewhat defeats the goal of getting rid accumulating ugliness.
1b. Alternatively, the translation process itself can be compiled into the translated n+1 EVM contract. This translates the CREATE opcode into a much more complicated device. (It also has the odd side effect of turning the translator into a sort of Quine if the payload contains a CREATE opcode, as it would now have to output itself.)
2. Assume that payloads are mostly static, maybe with some template substitutions for constants. (IIRC this is overwhelmingly the case). In this case we could translate the payload itself as part of the translation process.

I like the Quine solution, because it’s clearly the most awesome.

For future EVM versions we can avoid this by replacing CREATEs with a “copy existing contract as template” opcode. Maybe this is already part of the EOF proposal and I missed it.

---

**vbuterin** (2022-12-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/recmo/48/2516_2.png) Recmo:

> For future EVM versions we can avoid this by replacing CREATEs with a “copy existing contract as template” opcode. Maybe this is already part of the EOF proposal and I missed it.

It’s in my proposal!

> A CREATE4 opcode that copies the code of an existing address (in a similar way to how DELEGATECALL works), though it could still use a memory slice for the data field. The “recommended” pattern for developers would be that new code templates would get pushed with a manual transaction, and anything automated would just copy a template. Use cases like creating lots of contracts with small modifications (eg. user wallets with different public keys) would be accomplished with this data field.

As for how to deal with the fact that (i) `CREATE` and `CREATE2` still exist, and (ii) we have to push new templates to chain *somehow*, I can see a few ideas:

- Ban CREATE and CREATE2 from being used by or creating EOF-enabled contracts, but still allow contract creation transactions to create such contracts. To support cross-chain compatibility of template addresses, we could add a flag to contract creation transactions that makes their address generation CREATE2-style.
- Just accept that CREATE and CREATE2 can create code from bytes, and make it really clear to developers (and mandatory in solidity/vyper) that they should not be using those opcodes directly in applications.

---

**xinbenlv** (2022-12-14):

Thank you [@vbuterin](/u/vbuterin) for response.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> This is similar to how you can convert between kilometers and miles without having some “higher layer” of abstract farawayness that everyone agrees on as an ultimate benchmark of distance.

In your example of `kilometers` and `miles`, the higher layer of abstract farawayness that everyone agrees on, is the conversion rate between `kilometers` and `miles`. Converting kilometers into miles falls in to the Category 2 of below

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/16173_2.png) xinbenlv:

> (Category) 1. Like deprecating SELFDESTRUCT: the kind of change introduced to EVM that cause a behavior change which have no equivalent in newer version
> (Category) 2. Like hypothetically change KECCAK from opcode to precompile, this kind of change that have equivalent in newer version.

The `kilometers` and `miles` example doesn’t apply to the case when we try to *remove a behavior that has no equivalent*. For example, the attempt to remove SELFDESTRUCT is more like when we previously support `newton` in our measurement and we want to deprecate the ability to use newton or any type of force measurement, but only use `kilometers` or `miles`.

Unless your argument is that Category 2 is an empty set which I think is arguable…

---

**vbuterin** (2022-12-14):

Right, so I’m saying that `SELFDESTRUCT` *does* have an equivalent if we really really try hard: turn the whole contract into a delegatecall forwarder so you can switch code and use an incrementing nonce to create a new storage space every time the contract gets “re-created”. But it’s a stretch, and it’s probably not actually worth it to try to do that. It’s more an example to illustrate that I think the set of situations in which you can backwards-compatibly remove stuff by rearranging code is larger than it might seem.

---

**moodysalem** (2023-01-03):

I think the changes proposed here should be fully specified and adopted before EOF is included in a hard fork. Maintaining multiple versions of the EVM in perpetuity negates some of the benefit of other proposals that allow clients to [remove code for older versions of the EVM](https://eips.ethereum.org/EIPS/eip-4444#motivation). I also think the testing matrix grows exponentially when you have to consider multiple EVM versions for each HF (until something like [EIP-4444](https://eips.ethereum.org/EIPS/eip-4444) is adopted and sufficient time passes). It’s possible the performance gained from removing old code from EL clients is more than that of EOF in its current form.

For `EXTCODECOPY`, `EXTCODEHASH`, `EXTCODESIZE`, my initial preference is they raise an exception when acting on EOF code. I don’t know of a case where these would be used for arbitrary addresses except to check whether the address contains code, which is an [anti-pattern](https://consensys.github.io/smart-contract-best-practices/development-recommendations/solidity-specific/extcodesize-checks/) anyway. I think returning 0 could be dangerous/surprising behavior for a lot of contracts that use these opcodes. However, IIRC [solidity adds an EXTCODESIZE check for external function calls that do not return values](https://github.com/ethereum/solidity/issues/12204), which could mean incompatibility between existing non-EOF and new EOF code.

`CREATE4` also would be one of the best features of EOF. Uniswap V1-V3 each created thousands of max size contracts containing the same code, except for the immutables. The large overhead of even the simplest minimal proxy meant this was the most gas-efficient implementation of the factory pattern. Side note, I’d also appreciate removing the init code hash factor from the address computation (rather it’s something like creator address + salt.)

---

**frangio** (2023-01-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/moodysalem/48/4982_2.png) moodysalem:

> I don’t know of a case where these would be used for arbitrary addresses except to check whether the address contains code, which is an anti-pattern anyway.

The anti-pattern is to rely on codesize = 0 for some security purpose, to prevent some kind of abuse that a contract could execute.

But there are other very common use cases. What you mention about Solidity is one of them. The other are ERCs like ERC-721 that execute a callback on the receiver of a token and expect the callback to succeed and return a specific value, but only if the receiver is a contract with codesize > 0.

So raising an exception would be very bad in both of those cases, as would returning 0.

A potentially good alternative that works with both use cases would be to basically return a boolean value depending on whether the codesize is zero or non-zero, maybe represented as `0` and `uint256_max` or some large value.

---

**moodysalem** (2023-01-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> A potentially good alternative that works with both use cases would be to basically return a boolean value depending on whether the codesize is zero or non-zero, maybe represented as 0 and uint256_max or some large value.

Agree with this approach for `EXTCODESIZE`, also mentioned [here](https://notes.ethereum.org/@ipsilon/eof2-proposal#Introspection) for reference.

For `EXTCODECOPY`, `EXTCODEHASH`, what value would make sense to use? I don’t know of use cases for these opcodes with arbitrary addresses, but one use case for `EXTCODECOPY` I’ve seen in the wild is for [clones with immutables](https://github.com/wighawag/clones-with-immutable-args/blob/96f785571b534764094e268f7e608c393e88f7b6/src/ClonesWithImmutableArgs.sol#L108-L109)

---

**frangio** (2023-01-05):

For a little bit `EXTCODEHASH` was more efficient than `EXTCODESIZE` so there are some contracts that use the former to implement the check that I mentioned before. Instead of `codesize > 0` they would check `codehash not in [0, keccak256("")]`.

To preserve compatibility with those contracts `EXTCODEHASH` could return those two values in the same cases it does today, and a fixed third value if the account has non-empty code. Or it could collapse `0` and `keccak256("")` into the same return value to indicate empty code, this distinction has always been weird to me anyway.

I haven’t seen other use cases for this opcode or for `EXTCODECOPY`.

---

**bobsummerwill** (2023-01-06):

" One way to greatly reduce this tradeoff is to find a way to automatically convert version `n` EVM code to version `n+1` EVM code every time there is an upgrade (not necessarily immediately; perhaps convert when old code is “touched”, and make sure that all version `n` code is converted to version `n+1` before attempting to implement version `n+2` )."

I am afraid that I have to say this is an absolutely terrible idea.   Transpiling of bytecode POST DEPLOY?  That is such an over-complex approach to something which is a simple maintenance problem.

New opcodes can be added without the need for bumping the EOF version number.   Versions only change for non backwards-compatible changes, and those will affect the semantics in a major way anyway.

I’m getting vibes here of:

“What Killed the Linux Desktop”



      [tirania.org](https://tirania.org/blog/archive/2012/Aug-29.html)





###



Miguel de Icaza's Blog










How is this any worse than the absolute rafts of conditionals in other parts of the protocol (like gas costs)?  The EVM is not that complex.

These warts are the cost of backwards compatibility and are only paid once, by the developers who are maintaining this platform to contain the complexity for the benefit of the developers building on top.

It’s exactly the same as the Windows/MacOS example in the Desktop Linux story.  No, it isn’t sexy, but that is the cost of building a stable platform.    We had exactly the same situation for central tools and libraries at EA.   You need to support the union of all the versions and configurations which all of your end users are using.   And yeah, that can be a lot of warts and conditionals messing up the simplicity of your beautiful code, but those are the table stakes.

Windows contains patches for specific applications, and patches for bugs in specific hardware.  That is why you can still run binaries from decades ago.

Most important libraries have a massive test matrix, but guess what - computers are great at running automated tests.   Most of this stuff is massively parallizable.   Pay the entry fee.

Windows does not even CLAIM to be immutable, but it is a great example for what is required for the kind of stability we claim to aspire to.

(Incidentally - I think the goal of minimizing/removing introspection is a good one.  It is just the post deploy transpiling that I have a major issue with.  IMHO you just want to deploy once and you are done.  Everything leading into that - smart contact language, compiler code gen, optimizations, etc is baked into that bytecode and you have to live with it).

---

**holiman** (2023-01-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/bobsummerwill/48/730_2.png) bobsummerwill:

> Incidentally - I think the goal of minimizing/removing introspection is a good one. It is just the post deploy transpiling that I have a major issue with

This resonates with me: I totally don’t disagree with minimizing introspection. But the idea of transpiling live code seems like a theoretical solution which will never be performed in practice, because it’s such a huge slog. It’s in the same area of complexity as converting to verkle.

---

**shemnon** (2023-01-06):

I’m not sure I would classify EOFv1 as a separate VM.  eWASM?  Absolutely, and that may be setting the stage for many long-time-engineers perspective on the possible scope of the changes.

I veiw EOFv1 as a variant of the original frontier VM (aka legacy vm).  The main VM semantics are identical (stack, gas, message frames).  As far as I’ve read clients still use the same core evaluation loop, just with new OpCodes (the same means we’ve added opcodes for nearly a decade now).

What we are changing is the storage format and the code validation rules.  Parts of the whole, but still tightly intertwined with the original VM definition.  Code functions is the biggest structural change and IMHO has the largest potential to change how we view the EVM.

If we did fully deprecate the frontier EVM we would lose JumpDest validation and maybe some structure designed to support both legacy and EOF forms of storage.  It’s not a fundamentally different codebase.


*(2 more replies not shown)*
