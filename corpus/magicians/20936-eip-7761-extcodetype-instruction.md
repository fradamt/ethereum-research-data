---
source: magicians
topic_id: 20936
title: "EIP-7761: EXTCODETYPE instruction"
author: pdobacz
date: "2024-09-02"
category: EIPs > EIPs core
tags: [evm, erc-721, account-abstraction, evm-object-format, erc-1155]
url: https://ethereum-magicians.org/t/eip-7761-extcodetype-instruction/20936
views: 253
likes: 10
posts_count: 14
---

# EIP-7761: EXTCODETYPE instruction

Discussion topic for [EIP-7761: EXTCODETYPE instruction](https://eips.ethereum.org/EIPS/eip-7761) (formerly HASCODE, ISCONTRACT)

#### Update Log

- 2024-09-02 initial draft https://github.com/ethereum/EIPs/pull/8838
- 2024-09-11 https://github.com/ethereum/EIPs/pull/8875
- 2024-09-25 Update EIP-7761: Fill Endgame AA's Rationale section by pdobacz · Pull Request #8904 · ethereum/EIPs · GitHub

#### External Reviews

None as of 2024-09-02.

#### Outstanding Issues

None as of 2024-09-02.

## Replies

**wjmelements** (2024-09-09):

The EIP should name the specific EIP that disables EXTCODESIZE rather than the meta EIP for EOF.

---

**shemnon** (2024-09-11):

That would be EIP-3540, and it is already listed.

The [Changes to Execution Sematics](https://eips.ethereum.org/EIPS/eip-3540#changes-to-execution-semantics) section of EIP-3540 is where EXTCODE* is banned in EOF.

---

**wjmelements** (2024-09-11):

It seems much easier to just add back EXTCODESIZE. I haven’t yet found the rationale for removing the `extcode` opcodes.

---

**pdobacz** (2024-09-25):

I distilled some takeaways from a [Eth R&D discord conversation](https://discord.com/channels/595666850260713488/718596092828057631/1284596590681526396) here: [Update EIP-7761: Fill Endgame AA's Rationale section by pdobacz · Pull Request #8904 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/8904) (Endgame AA concerns), hopefully this is accurate. If there are more arguments to be made, let’s continue the discussion here.

---

**frangio** (2024-09-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> It seems much easier to just add back EXTCODESIZE. I haven’t yet found the rationale for removing the extcode opcodes.

Overall the arguments are not very convincing to me either.

[@vbuterin](/u/vbuterin)’s initial proposal was to ban code introspection *of EOF accounts* only, the rationale was very clear, and there was at least an idea of how to migrate legacy accounts. Current EOF seems to have gone way beyond this initial proposal to ban code introspecion *by EOF accounts of all accounts*, with unclear rationale, and to my knowledge no idea of how to eventually migrate.



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png)
    [EOF proposal: ban code introspection of EOF accounts](https://ethereum-magicians.org/t/eof-proposal-ban-code-introspection-of-eof-accounts/12113) [EIPs core](/c/eips/eips-core/35)



> One of the arguments against any EVM changes is that it’s much harder to add features to the EVM than to remove them (eg. the complexities around even removing a little-used opcode like SELFDESTRUCT), and so if the EVM keeps changing, ever-increasing ugliness and complexity is likely to be the outcome.
> One way to greatly reduce this tradeoff is to find a way to automatically convert version n EVM code to version n+1 EVM code every time there is an upgrade (not necessarily immediately; perhaps c…

---

**Amxx** (2025-04-03):

I have a few questions about the return values for this opcode.

- Will we ever want to distinguish EOF versions. Right now it says “2” of EOF regardless of the EOF version. EOF is designed to be versioned, and I think we should expect that at some point, detecting the version might be helpfull if there are incompatibilities.
- How are 7702 delagation handled ? Is the return value that of the targetted delegation ? Is it 0 (EOA) ? IMO this should be clarified.

When I (informally) discussed this opcode, I proposed the following:

- for legacy contracts, return 0x0
- for eof contracts (that start with 0xEF00XX) return the version of the contract, as defined in EIP-3540 (0x01-0xFF)
- for EIP-7702 delegate (that start with 0xEF0100) return 0x100 (this is in continuation of the eof version)
- if there is no code, return 0xFFFFFFFF

---

**pdobacz** (2025-04-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/amxx/48/1647_2.png) Amxx:

> How are 7702 delagation handled ? Is the return value that of the targetted delegation ? Is it 0 (EOA) ? IMO this should be clarified.

This is included in the spec:

> If loaded_code indicates a delegation designator (for example, 0xef0100 as defined in EIP-7702),
>
>
> replace loaded_code with the delegated code.
> deduct gas in accordance with the delegation designation rules

i.e. return value that of the targetted delegation.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/amxx/48/1647_2.png) Amxx:

> for legacy contracts, return 0x0

Some practical intention of this is EOA return value match legacy’s `EXTCODESIZE`, allowing for a quick `ISZERO` check, as the main purpose of `EXTCODETYPE` remains to do the legacy’s `EXTCODESIZE > 0` check.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/amxx/48/1647_2.png) Amxx:

> return the version of the contract, as defined in EIP-3540 (0x01-0xFF)

Leaking the EOF version to the EVM and allowing coupling smart contract codes to it doesn’t sound right to me.

---

**Amxx** (2025-04-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pdobacz/48/3042_2.png) pdobacz:

> Some practical intention of this is EOA return value match legacy’s EXTCODESIZE, allowing for a quick ISZERO check, as the main purpose of EXTCODETYPE remains to do the legacy’s EXTCODESIZE > 0 check.

Would

- if there is no code, return 0x0
- for eof contracts (that start with 0xEF00XX) return the version of the contract, as defined in EIP-3540 (0x01-0xFF)
- for legacy contracts, return 0xFFFFFFFFF

Work better ?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pdobacz/48/3042_2.png) pdobacz:

> Leaking the EOF version to the EVM and allowing coupling smart contract codes to it doesn’t sound right to me.

On of the many usecase of this opcode, and the reason it makes a distinction between EOF and legacy contract is that there is a risk (for EOF contract) to delegate to a legacy contract, and that EOF contract should be able to inspect if something is a contract that they can delegate to, or not.

I’m somehow worried that maybe in version 3 of EOF we introduce something that introduce a similar case where its safe to do something with other EOF contract of version 3, but not version 1 or 2. In that case, we may want EOF contract to detect the version of other EOF contract, which this EIP doesn’t support.

---

**pdobacz** (2025-04-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/amxx/48/1647_2.png) Amxx:

> Would
>
>
> if there is no code, return 0x0
> for eof contracts (that start with 0xEF00XX) return the version of the contract, as defined in EIP-3540 (0x01-0xFF)
> for legacy contracts, return 0xFFFFFFFFF
>
>
> Work better ?

It but does address the `ISZERO` problem. It would still be nice to have the versions ordered for simple comparison, but that can be solved with: return `0x01` for legacy and the entire 3byte `0xEF00<version>` for EOF.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/amxx/48/1647_2.png) Amxx:

> I’m somehow worried that maybe in version 3 of EOF

That is subjective, but I maybe am less worried. I also think that the worrying about the “proxy-accidentally-upgrading-to-legacy-and-bricking” is overstated, as it would indicate that the upgrade is done without proper testing in place. And there are I guess many ways to brick an upgrade, but I’m open to discussing how the particular EOF-to-legacy upgrade case is special, I might be missing sth.

If I put myself in the shoes of a smart contract developer, I have no way today to know if I should be doing my EOF-check like `EXTCODETYPE == 0xEF0001` or `EXTCODETYPE > 0xEF0000`, as I don’t know if EOFv2 will break my assumptions or not. Which boils down to the leaking point I made.

I find it somewhat safer to have `EXTCODETYPE` not be impacted by EOF version at all, even if it absolutely must discriminate btw legacy and EOF. In the unlikely event that discrimination between EOF versions is absolutely necessary for EOFv2, this could be handled by an extra opcode like `EXTEOFVERSION`.

(Actually, I now see that the EIP nails down the specific version of EOF, so it already implies a design like yours, where version will be distinguished! I forgot about that detail, I will propose to explicitly decouple the result from EOF versioning as a counter proposal, or at least we should make it clear what the returned value is intended to discriminate)

---

**Amxx** (2025-04-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pdobacz/48/3042_2.png) pdobacz:

> that can be solved with: return 0x01 for legacy and the entire 3byte 0xEF00 for EOF.

That also sounds great to me

---

**shemnon** (2025-04-03):

I want to say that right now there is no plan for any future incompatible “EOFv2” on the horizon.  All of the features getting serious discussion are all backwards compatible and won’t require a major version bump.

Personally I would be resistive to any new major EOF version in the next 5 years (assuming we ship with our current planned slate include TXCREATE) and a better goal is 10 years.  The best goal is no future EOFv2 and I am optimistic that remains an option.

This feels like something we will want to address in 5-10 years time when we are aware of what the breaking features are and how other contracts may want to interact with them.  So making space *today* for a feature we know nothing about seems a little presumptive.  Changing the EXTCODETYPE return is an option, as is a new version opcode, but we don’t have any idea what the impacts would be, so I think it is best to plan for what is best for today.

---

**frangio** (2025-04-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> I think it is best to plan for what is best for today.

I agree with this though I’d also say that smart contracts have to be deployed today and hopefully continue to be reliable into the future. This means that the semantics of opcodes should be predictable, and that includes how they relate to other aspects of the EVM in current and future versions. I think the best way to achieve that is to make opcode semantics be about observable behavior, rather than implementation details, and extremely specific. EXTCODETYPE arguably goes against both of those guidelines. It is about the implementation details of the account (legacy vs EOF), and in terms of observable behavior it combines two aspects: 1) will the account execute code if I call it, 2) can the account be the target of DELEGATECALL. Based on my guideline before, we should have one opcode for each of those aspects, which would allow for future changes where e.g. an account can be the target of DELEGATECALL but does not execute anything on CALL, however unlikely this might seem now.

---

**pdobacz** (2025-04-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> I want to say that right now there is no plan for any future incompatible “EOFv2” on the horizon. All of the features getting serious discussion are all backwards compatible and won’t require a major version bump.

While that is true, we do have the version byte in the `0xef0001`, so we already are planning for that. While we shouldn’t do excessive future proofing, I think we still have to commit to some concrete behavior of the new opcode EXTCODETYPE, i.e. at least decide if it will return new values on new EOF versions or not ([like here](https://github.com/ethereum/EIPs/pull/9591)).

By doing that we actually minimize the risk of needing an EOFv2

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> I think the best way to achieve that is to make opcode semantics be about observable behavior, rather than implementation details, and extremely specific. EXTCODETYPE arguably goes against both of those guidelines.

I think I agree with that. Can we consider a design going more in the direction of what [@frangio](/u/frangio) proposes? For example EXTCODETYPE returns 0 for EOA, 1 for legacy and **3** for EOF. This magically makes it a bitflag return, where first bit means “will execute code”, second bit “can be target of EXTDELEGATECALL”, which are observable traits. Also rename it to EXTTRAITS and commit to the future of higher bits that might become used in new upgrades, even in EOFv1 codes deployed after Osaka, so that contract developers are discouraged from doing `EXTTRAITS >= 3`, but rather `EXTTRAITS & <some bit mask> == 1 or 0`

I believe this would also cover what [@Amxx](/u/amxx) asks for.

