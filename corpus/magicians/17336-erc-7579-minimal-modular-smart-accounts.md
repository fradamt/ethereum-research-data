---
source: magicians
topic_id: 17336
title: "ERC-7579: Minimal Modular Smart Accounts"
author: kopykat
date: "2023-12-14"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-7579-minimal-modular-smart-accounts/17336
views: 5251
likes: 24
posts_count: 29
---

# ERC-7579: Minimal Modular Smart Accounts

Discussion for [Add ERC: Minimal Modular Smart Accounts by zeroknots · Pull Request #163 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/163/files).

The  proposal outlines the minimally required interfaces and behavior for modular smart accounts and modules to ensure interoperability across implementations.

## Replies

**Aboudjem** (2023-12-16):

Hey [@kopykat](/u/kopykat) ![:wave:](https://ethereum-magicians.org/images/emoji/twitter/wave.png?v=12)

Nice work on ERC-7579, I’ve opened a PR proposing a few enhancements aimed at boosting its adaptability and future-proofing the standard:

- Added a function for dynamic module type identification: function getModuleTypes(address module) external view returns (uint256[]);.
- Added guidelines for module state management during installation and uninstallation.
- Emphasized the importance of having at least one active Validation Module for security.
- Suggested standardized procedures for module installation/uninstallation.

I have a couple of questions:

- Are module types in ERC-7579 meant to be fixed, or could we consider making them more flexible for future module types?
- What might be the limitations of adopting a less specific approach to module types?

![:+1:](https://ethereum-magicians.org/images/emoji/twitter/+1.png?v=12)

---

**jhfnetboy** (2023-12-17):

Great job!

It is a good idea to build an extensible model on a minimal modular contract account!

I will follow this discussion.

Thanks!

---

**kopykat** (2023-12-17):

Thanks, I have left some comments on [the pr](https://github.com/zeroknots/ERC-minimalisticMSA/pull/1).

To your questions:

1. What do you mean by fixed? The module types ids already assigned should not be reused and the modules defined should not be given new ids. However, our intention is that if there are further module types in the future then extensions to ERC-7579 should define the next module type ids as the next available integer (eg 5 currently). I see that this is not actually clearly stated in the standard so this is something we could add for further clarity
2. What do you mean by less specific approach to module types?

---

**Aboudjem** (2023-12-17):

Thanks [@kopykat](/u/kopykat).

1. By ‘fixed’ I meant whether the module types are rigidly set in the standard or if there’s room for adding new types dynamically in the future.
2. As for the ‘less specific approach,’ I was considering if having a flexible framework for module types might be beneficial, allowing future expansions without altering the core standard. This could include general functions for module management applicable to all types, enhancing adaptability.

My intention isn’t to overhaul the entire standard, as it’s quite solid already. I’m just considering future adaptability. Let me know if this approach seems feasible and valuable in your view

---

**kopykat** (2023-12-17):

1. Yes, types should be extended by builders and/or future standards. We could add a note for this on the ERC to make it more explicit
2. I think module type ids being extensible is already a good step towards this. On the point of more generalized functions, I’ve replied on your pr but tldr is that we got feedback early on that having dedicated functions per module type was preferred for verbosity and because adding a new module type would need an account upgrade anyways, but the main downside I can see with this approach is just the overhead of 2 more functions for every new module type

---

**yaonam** (2023-12-19):

![image](https://github.githubassets.com/favicons/favicon.svg)

      [GitHub](https://github.com/erc7579/erc7579-implementation/discussions/1)



    ![image](https://opengraph.githubassets.com/9d0f7a15ca190028e675a80604d57c8b99a19b671f200f152bcbb01056331cea/erc7579/erc7579-implementation/discussions/1)

###



[Here module refers to validator, executor, and hooks.] Idea Change function isModuleInstalled(address) external returns (bool) to function isModuleInstalled(address, bytes calldata) external retur...










Linking the discussion about adding a secondary param to module checkers to allow for more flexibility with module handling.

---

**wjmelements** (2023-12-20):

I have a tentative design for modular accounts that would be powered by `SETCODE`. It would be easy to splice code in and out with `SETCODE`.

---

**kopykat** (2023-12-20):

Interesting - is there any timeline already for the `SETCODE` EIP?

---

**wjmelements** (2023-12-20):

I hope it will be in Prague but ACDE priorities are unpredictable.

---

**kopykat** (2024-01-27):

Hey everyone, we wanted to share some updates to the standard. We are considering a simplification of the execution functions and the account config functions to both simplify the standard and make it more future proof. Check out the prototype here: [GitHub - erc7579/uMSA](https://github.com/erc7579/uMSA)

---

**webthethird** (2024-03-08):

[@kopykat](/u/kopykat) Re: the [dependence on ERC-4337](https://eips.ethereum.org/EIPS/eip-7579#dependence-on-erc-4337), I am just starting to work on a modular smart account on zkSync using their native AA, and I would like to use this ERC without the dependency. Do you have any recommendations for me?

---

**kopykat** (2024-03-09):

In general, ERC-7579 has two areas of dependency on ERC-4337:

- assumption that a tx is split into separate validation and execution phases
- the usage of the validateUserOp function

The former is pretty key to ERC-7579 so more work would need to be done there to figure out how to make the standard work for account abstraction solutions where this is not the case (but afaik it is the same in the case of zkSync).

The latter is pretty easy to go around, ie to not use `validateUserOp` but a validation function with another interface and input args. I’m not super familiar with how zkSyncs AA works but happy to chat more on telegram (@konradkopp).

---

**wjmelements** (2024-04-01):

I don’t want for this ERC to call itself minimal. There is nothing minimal about this design.

---

**kopykat** (2024-04-01):

It is minimal on the context of modular smart accounts, which are quite complex considering both the interoperability and security aspects. Happy to take any feedback on how the standard could be more minimal.

---

**wjmelements** (2024-04-01):

Look into the 2byte ABI.

---

**wjmelements** (2024-04-01):

The 2byte ABI is the minimal modular smart account design. It used to upgrade via `CREATE2` and `SELFDESTRUCT` and I hope to restore it via `SETCODE`. It is more modular than anything that can be built with solidity because new subprograms can be directly concatenated.

Examples of contracts using the 2byte abi:

- https://etherscan.io/address/0x00000000009e50a7ddb7a7b0e2ee6604fd120e49
- https://etherscan.io/address/0x0000e0ca771e21bd00057f54a68c30d400000000

A contract using a similar 1byte abi:

- https://etherscan.io/address/0x6b75d8af000000e20b7a7ddf000ba900b4009a80

There are more, but I suspect that the number of transactions using the 2byte ABI exceeds the number of transactions using erc-4337.

---

**matthiasgeihs** (2024-06-21):

Hi, why do you require backwards compatibility to ERC-1271?

ERC-1271’s `isValidSignature` interface feels a bit outdated as it does not receive any metadata (e.g., compared to ERC-4337’s `validateUserOp` which gets the full userOp).

Wouldn’t it be fine if compatibility with ERC-1271 would be just optional?

---

**kopykat** (2024-06-21):

As far as I know, 1271 is the only at least somewhat widely used way to have contracts sign messages. Are there any other ways that are adopted?

You could also add additional data into the 1271 data and then have the validator decode it but dapps would need to know how to encode this.

---

**0xlynett** (2024-08-24):

nitpick: `supportsAccountMode` should be `supportsExecutionMode`, as that function is not mentioned anywhere except here:

> Accounts are NOT REQUIRED to implement all execution modes. The account MUST declare what modes are supported in supportsAccountMode (see below) and if a mode is requested that is not supported by the account, the account MUST revert.

---

**kopykat** (2024-08-24):

Thanks for spotting this. We renamed `supportsAccountMode` to `supportsExecutionMode` but seems like we forgot to change this occurrence. Should be fixed now


*(8 more replies not shown)*
