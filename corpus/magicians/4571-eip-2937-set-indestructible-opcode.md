---
source: magicians
topic_id: 4571
title: "EIP-2937: SET_INDESTRUCTIBLE opcode"
author: vbuterin
date: "2020-09-04"
category: EIPs
tags: [opcodes]
url: https://ethereum-magicians.org/t/eip-2937-set-indestructible-opcode/4571
views: 3595
likes: 4
posts_count: 12
---

# EIP-2937: SET_INDESTRUCTIBLE opcode

Add a `SET_INDESTRUCTIBLE (0xA8)` opcode that prevents the contract from calling `SELFDESTRUCT (0xff)`.



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/2937/)














####


      `master` ← `vbuterin-patch-2`




          opened 05:25AM - 04 Sep 20 UTC



          [![](https://avatars.githubusercontent.com/u/2230894?v=4)
            vbuterin](https://github.com/vbuterin)



          [+48
            -0](https://github.com/ethereum/EIPs/pull/2937/files)







Add a `SET_INDESTRUCTIBLE` opcode that prevents the contract from calling `SELFD[…](https://github.com/ethereum/EIPs/pull/2937)ESTRUCT`.

When opening a pull request to submit a new EIP, please use the suggested template: https://github.com/ethereum/EIPs/blob/master/eip-template.md

We have a GitHub bot that automatically merges some PRs. It will merge yours immediately if certain criteria are met:

 - The PR edits only existing draft PRs.
 - The build passes.
 - Your GitHub username or email address is listed in the 'author' header of all affected PRs, inside <triangular brackets>.
 - If matching on email address, the email address is the one publicly listed on your GitHub profile.

## Replies

**ytrezq** (2020-09-04):

Should it be permanent or should there be a way to rollback?

---

**vbuterin** (2020-09-05):

The flag set by the opcode would last for the duration of the transaction, so it is temporary (though if the first byte of a contract is the opcode then of course it will trigger every time and be unavoidable, which is the intention).

---

**axe** (2020-09-07):

Can this new OPCODE be used to signal if the contract implement or not self destruct?

If is set to false, then you can’t destroy that specific contract.

Cheers

---

**vbuterin** (2020-09-08):

If the first byte of the code of a contract is this opcode, then that contract cannot selfdestruct.

---

**axe** (2020-09-08):

I’m thinking more into if you have implement the self destruct function the opcode is “true”. Is not if is possible to remove the contract, but more this contract can everything is place to be removed.

Cheers

---

**axe** (2020-09-08):

Basically can we inside a smart contract know that other smart contract can be removed.

Is important in the case when a dev want to whitelist smart contracts on chain.

---

**mudgen** (2020-09-13):

I like this EIP. It makes contracts and libraries safer.

It makes proxy contracts and [diamonds](https://eips.ethereum.org/EIPS/eip-2535) safer because they rely on delegatecall which can pull in code from other contracts.

This EIP prevents delegatecall from accidentally or maliciously destroying proxy contracts and diamonds and prevents the contracts/libraries that proxy contracts and diamonds rely on from disappearing. This is good.

---

**holiman** (2021-01-08):

> The intended use case would be for contracts to make their first byte of code be the SET_INDESTRUCTIBLE opcode if they wish…

However, the spec doesn’t say what should happen if `SET_INDESTRUCTIBLE` is encountered on `PC!=0`

Some other questions.

1. Let’s say we have C with SET_INDESTRUCTIBLE at 0. Contract X does delegatecall(c) && selfdestruct. Does C successfully selfdestruct?
2. Same scenarion with C. What about callcode(c)?

In general, is the `globals.indestructible` scoped? I assume it is (by which I mean it’s journalled, and scope-revertals removes stuff from it)

---

**alu** (2021-01-10):

1. I think that if SET_INDESTRUCTIBLE is encountered on PC!=0, it should be treated as a no-op to avoid any weird edge cases. However, forcing it to be the first byte does make its use case less flexible and I’m open to lifting this restriction.
2. C should not successfully self destruct when using delegatecall if it is set as indestructible.
3. C should also not successfully self destruct when using callcode if it is set as indestructible.

I also believe `SET_INDESTRUCTIBLE` should be implemented as a variable local to each execution frame. I think it is unnecessary to make it a global variable, as the delegatecall/callcode edge case can still be resolved with a local boolean variable implementation.

Proposed update to EIP-2937 spec: https://github.com/ethereum/EIPs/pull/3186

Local variable implementation in geth client: https://github.com/lightclient/go-ethereum/pull/7

---

**dror** (2021-03-30):

I think this EIP is great, as it sets optional restriction/extension rules on the EVM context of future-deployed contracts.

But I think its scope should be extended: There might be other features we would like to enable/restrict in the future.

So I would suggest to add it as “RULES” opcode, which receives a single bitmask param.

the first bit is SET_INDESTRUCTIBLE, with the semantics defined by this EIP.

all other bits are REQUIRED to be zero, and the opcode should REVERT in case any is set.

In a future EIP (and fork), more semantics can be given to those bits, without requiring a new opcode for each.

The downside is that the prefix this new opcode generates is 3 bytes instead of 1: `"PUSH1 1 RULES"`

---

**nikolai** (2021-10-06):

This doesn’t just make proxies / ‘diamonds’ safer, it makes them so much safer that it enables a categorically different mode of interaction where proxy actions / scripts can be properly sandboxed and so trustlessly composed within a single proxy script



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nikolai/48/4312_2.png)
    [`Wand` aka `DSProxy 2.0`](https://ethereum-magicians.org/t/wand-aka-dsproxy-2-0/7221) [Primordial Soup](/c/primordial-soup/9)



> This is a grab bag of proxy contract R&D. I’m publishing this to help bump priority for SET_INDESTRICTUBLE.
> Code sketch and README at time of publishing are copied below:
>
> interface WandAuth {
>   function canCast(address witch, address spell, bytes4 sigil)
>     external returns (bool);
> }
>
> contract Wand {
>   address public root;
>   address public auth;
>   address public code;
>   address public lock;
>
>   function cast(address spell, bytes calldata data)
>     payable public
>       returns (bool bit, byt…

