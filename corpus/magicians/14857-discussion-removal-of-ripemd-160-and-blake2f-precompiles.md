---
source: magicians
topic_id: 14857
title: "Discussion: Removal of `RIPEMD-160` and `blake2f` Precompiles"
author: pcaversaccio
date: "2023-06-28"
category: Magicians
tags: [precompile, cryptography]
url: https://ethereum-magicians.org/t/discussion-removal-of-ripemd-160-and-blake2f-precompiles/14857
views: 3938
likes: 17
posts_count: 20
---

# Discussion: Removal of `RIPEMD-160` and `blake2f` Precompiles

The precompile [RIPEMD-160](https://www.evm.codes/precompiled#0x03?fork=shanghai) has been called [1,317 times](https://etherscan.io/txsInternal?a=0x0000000000000000000000000000000000000003&m=advanced) since Ethereum’s inception, and [blake2f](https://www.evm.codes/precompiled#0x09?fork=shanghai) has been called [1,228 times](https://etherscan.io/txsInternal?a=0x0000000000000000000000000000000000000009&m=advanced) since its go-live as part of the Istanbul hard fork on December 7 2019 (block number [9,069,000](https://etherscan.io/block/9069000)).

I would like to propose an EIP to remove these two precompiles, as these two precompiles have not found real-world traction and the EVM should be optimised for simplicity and not carry along too many technical debt. Prior to doing so, I would like to hear what arguments there might be against such a removal. As an important note, zcash has changed their cryptography in the meantime to not (or plan to not) even use `BLAKE2b` anymore if I understand correcty (using mostly `BLAKE2s` and planning to use `BLAKE3`).

PS: I’ve tweeted about this [here](https://twitter.com/pcaversaccio/status/1674052563556073480).

**EDIT 1:** Based on more accurate data provided by [@thevaizman](/u/thevaizman) (thanks a lot again!), we have the following number of calls:

- ripemd160: 612,441 (the most recent call on Jun-27-2023 and the oldest call on Jul-03-2016).
- blake2f: 22,131 (the most recent call on Oct-06-2022 and the oldest post-Istanbul call on Jan-25-2021).

[![RIPEMD-160](https://ethereum-magicians.org/uploads/default/optimized/2X/7/7305caf44194c4c8f98a68a0c6b8be18ea0f83ec_2_690x371.png)RIPEMD-1602110×1137 73.6 KB](https://ethereum-magicians.org/uploads/default/7305caf44194c4c8f98a68a0c6b8be18ea0f83ec)

[![Blake2f](https://ethereum-magicians.org/uploads/default/optimized/2X/b/bc7ec2f845078a41651ab681431112b45dbac2ae_2_690x356.png)Blake2f2033×1050 89.7 KB](https://ethereum-magicians.org/uploads/default/bc7ec2f845078a41651ab681431112b45dbac2ae)

**EDIT 2:** My EIP-7266 PR on *Remove `blake2f` (`0x09`) Precompile* can be found  [here](https://github.com/ethereum/EIPs/pull/7266) and the merged draft version on the EIP website [here](https://eips.ethereum.org/EIPS/eip-7266).

## Replies

**ulerdogan** (2023-06-28):

Are there any downsides to still holding these contracts in EVM? On the other hand, removing them may create backward compatibility issues.

---

**pcaversaccio** (2023-06-28):

Well, we got the famous EVM Equivalence competition by numerous L2s, why do they need to introduce two precompiles that are more or less not even used on Ethereum mainnet for years? The `blake2f` hasn’t been used for 265 days and was introduced in [EIP-152](https://eips.ethereum.org/EIPS/eip-152). If you read the motivation and understand that zcash has changed their cryptography in the meantime to not (or plan to not) even use `BLAKE2b` anymore (using mostly `BLAKE2s` and planning to use `BLAKE3`), it doesn’t make sense to keep this precompile. `RIPEMD-160` was introduced to be Bitcoin-compatible in the sense to generate Bitcoin addresses for verification (see e.g. [here](https://github.com/ethereum/btcrelay)). But also that use-case seems deprecated for years. Ofc this is a backwards-incompatible breaking change,  but why should the EVM continue to support deprecated use cases?

---

**ulerdogan** (2023-06-28):

Thanks, understood. While it is easier for rollups running L1 clients/codes directly, it seems these precompiles are adding unnecessary complexity for zk-rollups and especially future changes to the EVM.

---

**prestwich** (2023-06-28):

ripemd160 is necessary for Bitcoin light clients, which have been broadly deployed. It is also in somewhat  regular use by [some user](https://etherscan.io/address/0x0000000000be6d8381e3a01c19e3b3c2b6d9c7cd#internaltx) interfacing with arbitrum

See my comment re blake2 f-function here:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/prestwich/48/2870_2.png)
    [EIP #?: add precompile for Blake2s/Blake3](https://ethereum-magicians.org/t/eip-add-precompile-for-blake2s-blake3/12407/2) [EIPs](/c/eips/5)



> As one of the people who initially pushed for EIP-152 and helped write it, I think a post-mortem is long overdue. I may write a full one for a blog sometime, but here’s the condensed version:
> Fundamentally EIP-152 failed for 2 reasons
>
>
> Politicization of the proposal led to a weird technical design.
> Implementing the F function instead of the hashfunction was political nonsense. It should never have been done. It led to a bad result for everyone.
>
>
> Envisioned use cases were not validated befo…

---

**Philogy** (2023-06-28):

ripemd160 as a function has merit although I think the discussion should center around whether it merits being an enshrined part of the EVM in the form of a precompile.

Considering its limited use it might be worth removing it as a precompile, trading off the gas efficiency of the limited applications that use it in exchange for removing EVM technical debt. The function will still be “available”, it’ll simply require devs to access via some application-level Solidity/Yul library.

I think an important question is also how these precompiles could be deprecated in a manner that doesn’t compromise these limited applications. Do we insert bytecode implementations of the precompiles at their address or delete them entirely, opting to modify the applications calling the function instead?

---

**prestwich** (2023-06-28):

`ripemd160` is a launch feature of the EVM, and its implementation in geth is about 20 lines, because it’s simply delegated to the go std library. Why do you think it’s “tech debt”?

Inserting bytecode is a lot more debt than leaving the precompile in, as it requires permanent HF code paths to insert a static program into state at a configurable height. The work on that feature alone is far more risky than just not touching the precompile.

For blake2f, we have a high degree of confidence that no running application is using it. We should favor changing the precompile behavior to be a dataless revert and give passive applications that rely on it a 6-12 month lead time.

---

**pcaversaccio** (2023-06-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/philogy/48/4714_2.png) Philogy:

> I think an important question is also how these precompiles could be deprecated in a manner that doesn’t compromise these limited applications. Do we insert bytecode implementations of the precompiles at their address or delete them entirely, opting to modify the applications calling the function instead?

For `blake2f`, I see it like [@prestwich](/u/prestwich) [here](https://ethereum-magicians.org/t/eip-add-precompile-for-blake2s-blake3/12407/2):

> …we should deprecate, evaluate past usage, and deactivate in some post-Shanghai fork. It can be used as a safe & uncontroversial testflight for deprecating and removing EVM features.

For `ripemd160` am not sure yet, but I believe that it can be zk-proven if needed and no precompile anyways needed? Maybe here we could give applications 12-18 months lead time.

---

**pcaversaccio** (2023-06-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/prestwich/48/2870_2.png) prestwich:

> ripemd160 is a launch feature of the EVM, and its implementation in geth is about 20 lines, because it’s simply delegated to the go std library. Why do you think it’s “tech debt”?

The EVM should be optimised for simplicity and future-proofness. Mostly unused legacy code should not be supported at one point since it can lead to further maintenance issues and unnecessary additional complexity for (future) EVM implementations ([an example](https://github.com/ethereum/go-ethereum/blob/master/core/state/statedb.go#L749)). Also, the mentioned [ripemd160](https://pkg.go.dev/golang.org/x/crypto/ripemd160) is deprecated and not optimised anyways. Thus, I think it’s “debt” in the sense, that it’s an unnecessary carry-along.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/prestwich/48/2870_2.png) prestwich:

> Inserting bytecode is a lot more debt than leaving the precompile in, as it requires permanent HF code paths to insert a static program into state at a configurable height. The work on that feature alone is far more risky than just not touching the precompile.

Agreed.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/prestwich/48/2870_2.png) prestwich:

> For blake2f, we have a high degree of confidence that no running application is using it. We should favor changing the precompile behavior to be a dataless revert and give passive applications that rely on it a 6-12 month lead time.

Sounds reasonable to me.

---

**thevaizman** (2023-06-29):

[@pcaversaccio](/u/pcaversaccio) - as mentioned before on twitter, here’s the data about calls (internal and external) to `ripemd-160` and `blake2f`. Made it available for you as a csv if you want to further explore ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

blake2f - [here](https://docs.google.com/spreadsheets/d/e/2PACX-1vTia-usyhUKyWVMRdJrvmNcEAbW5ODRKKPH3xtT6r78C5Mj3TUOHkKZkPGf4EtSQ9DlSfyshpkfIxMY/pub?output=csv)

riipemd-160 - [here](https://docs.google.com/spreadsheets/d/e/2PACX-1vTbxsLW5tkwEbFQWcDVI-DP5E-kfRVwT5622tTX6vIcWcjp5w64DjJjU49qYdOljWyvNyaVW9gRpxg1/pub?output=csv)

---

**pcaversaccio** (2023-06-29):

Thanks a lot, highly appreciated! I updated my summary accordingly and added some visualisations. My original plan doesn’t change however ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=12)

---

**Philogy** (2023-06-30):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/prestwich/48/2870_2.png) prestwich:

> Inserting bytecode is a lot more debt than leaving the precompile in, as it requires permanent HF code paths to insert a static program into state at a configurable height. The work on that feature alone is far more risky than just not touching the precompile.

Good point, I suppose the discussion around `ripemd-160` should center around whether to remove it as a whole or leave it in.

---

**prestwich** (2023-06-30):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pcaversaccio/48/6329_2.png) pcaversaccio:

> The EVM should be optimised for simplicity and future-proofness. Mostly unused legacy code should not be supported at one point since it can lead to further maintenance issues and unnecessary additional complexity for (future) EVM implementations (an example ).

This example is great, because it illustrates why a hard fork increases complexity permanently. The code to handle a pre-Byzantium state must be included in the post-Byzantium client, indefinitely (until regenesis amen). This code could not be removed if rmd160 were removed, as the pre-byzantium blocks would still need to be processed. And rmd160 could not be removed from EVM, as it is necessary to validate old blocks. Instead we would have to add special handling code for the switchover from rmd160-present to rmd160-absent. The attempt to decrease complexity via a HF results in an increase of complexity to the codebase

My rec to remove blake2f is to use it as a test for deactivations, to better understand how we can safely do it, and how much complexity it adds. rmd160 is significantly less-safe to remove

---

**hmijail** (2023-07-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pcaversaccio/48/6329_2.png) pcaversaccio:

> The blake2f hasn’t been used for 265 days

Going a bit meta… I’m surprised that this is considered a reason to deprecate anything at the EVM level, *and* that “future-proofing” is used as a motivation.

If I had ETH in a contract using a random precompile, stopped paying attention, and came back after 3 years, is it possible that I’d find the EVM has been changed, my contract no longer works and my ETH is lost? This is shocking.

I thought that anything at the depth of the EVM is practically forever and that efforts are made to stay backwards-compatible, both because one needs to be able to re-run history and because removing anything implies a hard fork that only adds complexity - as [@prestwich](/u/prestwich) mentioned.

And I thought that this intention of being backwards compatible is what yields “future-proofing”. As an example, IIRC, discussions about changing gas prices for opcodes were very careful about what could get broken in past contracts.

So my question is: is there any “standard” about what can be deprecated?

And, if the real goal is to avoid “extra” work for L2 implementations, why not limit the discussion to L2?

---

**pcaversaccio** (2023-07-04):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/h/90ced4/48.png) hmijail:

> If I had ETH in a contract using a random precompile, stopped paying attention, and came back after 3 years, is it possible that I’d find the EVM has been changed, my contract no longer works and my ETH is lost? This is shocking.

If you read the Yellow Paper carefully, it states *these are so-called ‘precompiled’ contracts, meant as a preliminary piece of architecture that may later become native extensions*. I’m not going to enter the discussion about whether precompiles were a failure or not (IMHO yes), but precompiles are on purpose, not native extensions. Furthermore, if you read the EIP draft carefully, I also state that *one of the reasons why [EIP-152](https://github.com/ethereum/EIPs/blob/c55b0b2fc1beb35c3f23a92c3af59783fb58f673/EIPS/eip-152.md) has failed is that the envisioned use cases were not validated before inclusion*. This is just true and thus `blake2f` will never transition into a native opcode.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/h/90ced4/48.png) hmijail:

> So my question is: is there any “standard” about what can be deprecated?

There is no standard nor protocol but that’s exactly for what this precompile removal could be leveraged. In my EIP draft I write: *The precompile `blake2f` (`0x09` ) can be safely used as a test run for the phase-out and removal of EVM functions.* Also, we should give applications sufficient time before removing this.

Eventually, there is an effort for versioning the EVM via [EOF](https://eips.ethereum.org/EIPS/eip-3540). Let’s say the EVM is forever, but time evolves and possibilities and applications change, we can’t pack the full future use cases right now into 256 opcodes and a couple of precompiles. The EVM should be simple and future-proof given it’s current state and don’t overload it with functionalities and technical debt. For that we need a proper solution (which might be EOF versioning).

---

**prestwich** (2023-07-04):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/h/90ced4/48.png) hmijail:

> If I had ETH in a contract using a random precompile, stopped paying attention, and came back after 3 years, is it possible that I’d find the EVM has been changed, my contract no longer works and my ETH is lost? This is shocking.

Shocking. Won’t somebody think of the children’s smart contracts.

A contract may break in any given hard fork due to gas scheduling or gas semantics updates. Breakages have occurred several times in the past, and breakages are explicitly part of the future roadmap with, e.g. EIP-4758. The EVM is mutable on purpose, and no specific behavior is 100% reliable

Technically any HF is a breaking change to the extent that any contract could hypothetically inspect the EVM behavior. Adding a precompile at all could be a breaking change, as any contract could call a precompile and rely on it returning nothing. Changing any gas schedule item could be breaking, as a contract may introspect its own gas usage. Hard fork designers asses the level of breakage risk, and if too high design a mechanism (like EIP-2930) to mitigate the risk

---

**hmijail** (2023-07-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/prestwich/48/2870_2.png) prestwich:

> Shocking. Won’t somebody think of the children’s smart contracts.

Not sure what to make of this. Would you prefer me to say “mildly amused”? No, I’m shocked. Particularly with the unbothered “oh counts were wrong by a factor of 20x-60x but the plan remains”.

And I don’t get the point of the next 2 paragraphs. Yes, the EVM can be changed, so let’s just change it? The very EIPs you mention are great examples of taking care that the backward compatibility effects are minimal. Impact analysis for EIP-4758:

> The analysis revealed that disabling or neutering SELFDESTRUCT opens a security risk to uninformed users of a contract used by Pine Finance.
> …
> Based on the analysis, I will suggest trying to preserve SELFDESTRUCT when switching to Verkle trees.

Protecting even uninformed users! Yeah, that is *shockingly* good.

Further than that, the whole discussion thread in there is about mitigating possible problems and adding corner cases to disrupt as little as possible - starting with previous failed EIPs. Somehow they missed that “the EVM is mutable on purpose”, you’d think?

> Technically any HF is a breaking change to the extent that any contract could hypothetically inspect the EVM behavior.

Oh FFS.

---

**pcaversaccio** (2023-07-20):

As a quick update, my EIP got merged and is now available [here](https://eips.ethereum.org/EIPS/eip-7266) (`Draft` status).

---

**Philogy** (2023-08-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pcaversaccio/48/6329_2.png) pcaversaccio:

> Eventually, there is an effort for versioning the EVM via EOF . Let’s say the EVM is forever, but time evolves and possibilities and applications change, we can’t pack the full future use cases right now into 256 opcodes and a couple of precompiles. The EVM should be simple and future-proof given it’s current state and don’t overload it with functionalities and technical debt. For that we need a proper solution (which might be EOF versioning).

Not sure I understand how versioning would solve the backwards-compatibility issues without compromising on the ability to remove tech debt from Ethereum. If the chain has to support multiple versions of the EVM at the same time don’t you have to maintain all features past and future of the EVM?

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/h/90ced4/48.png) hmijail:

> If I had ETH in a contract using a random precompile, stopped paying attention, and came back after 3 years, is it possible that I’d find the EVM has been changed, my contract no longer works and my ETH is lost? This is shocking.

I agree with [@hmijail](/u/hmijail) here, the backwards-incompatible deprecation of `SELFDESTRUCT` that is going to be included in Cancun also similarly surprised me. Maybe I and the general public have to recalibrate our imagination of Ethereum but I always held the belief that one of Ethereum’s most interesting capabilities was the ability to built immutable applications that may survive for decades if not centuries.

I understand it’s a hard balance to strike between removing tech debt and backwards compatibility, maybe we need a meta EIP around how & when features are deprecated.

---

**pcaversaccio** (2023-08-30):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/philogy/48/4714_2.png) Philogy:

> f the chain has to support multiple versions of the EVM at the same time don’t you have to maintain all features past and future of the EVM?

In this context, I was referring to the `latest` EVM version. Yes, my understanding is as well that you have to keep supporting multiple versions with all its features, but the `latest` version itself should not contain any technical debt and provide all instructions for the envisioned use cases.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/philogy/48/4714_2.png) Philogy:

> Maybe I and the general public have to recalibrate our imagination of Ethereum but I always held the belief that one of Ethereum’s most interesting capabilities was the ability to built immutable applications that may survive for decades if not centuries.

Well with EOF versioning this will still be possible, but I think the ossification of the EVM takes a lot of previous iterations and I don’t think we’re there yet…

