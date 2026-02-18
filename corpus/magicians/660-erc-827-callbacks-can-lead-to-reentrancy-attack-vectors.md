---
source: magicians
topic_id: 660
title: ERC-827 callbacks can lead to reentrancy attack vectors
author: jpitts
date: "2018-07-06"
category: Working Groups > Security Ring
tags: []
url: https://ethereum-magicians.org/t/erc-827-callbacks-can-lead-to-reentrancy-attack-vectors/660
views: 2606
likes: 0
posts_count: 2
---

# ERC-827 callbacks can lead to reentrancy attack vectors

This is an interesting case we all can learn from. Smart contract [ERC-827](https://github.com/ethereum/EIPs/issues/827) allows / potentially enables a bad contract security practice.

From [issue comments on the ERC-827 EIP](https://github.com/ethereum/EIPs/issues/827#issuecomment-393872680) by the security researcher:

> We wrote a blog post, how replacing ERC20 with ERC827, can lead to unexpected reentrancy attacks.
> …
>
>
> Given that potential use cases of transferAndCall are unclear, I see the value of our article in clarifying how it should not be used.
> Similar issues apply to approveAndCall, however, given that this functionality does not exist in ERC20 (as you said), we would have had to construct an example with vulnerable code to use it. If you have concrete cases, where approveAndCall is called from a smart contract we would be happy to check.
>
>
> Overall, our intention was just to notify people that special care is needed when using these functions inside a smart contract.
>
>
> – ritzdorf, CTO @ ChainSecurity

---

Related tweets and stories:



      [twitter.com](https://twitter.com/gakonst/status/1015164548431663105)



    ![image](https://pbs.twimg.com/profile_images/1596214564470734849/1Tg5-gNh_200x200.jpg)

####

[@gakonst](https://twitter.com/gakonst/status/1015164548431663105)

  Very interesting reads which I somehow missed, nice finds @chain_security!

tldr: ERC827 callbacks (transferAndCall et al) can lead to reentrancy attack vectors.

https://t.co/b0okX8piYc

https://t.co/aIezvENlo8

cc @arvanaghi @maurelian_ @GNSPS

  https://twitter.com/gakonst/status/1015164548431663105










https://medium.com/chainsecurity/why-erc827-can-make-you-vulnerable-to-reentrancy-attacks-and-how-to-prevent-them-61aeb4beb6bf

---

From OpenZeppelin’s GitHub issue on this:

> It is a really bad practice to allow the abuse of CUSTOM_CALL in token standard.

https://github.com/OpenZeppelin/openzeppelin-solidity/issues/1044

## Replies

**AugustoL** (2018-07-09):

Hello [@jpitts](/u/jpitts), thanks for bringing this up on the ethereum-magicians community.

The issue with `transferAndCall` is that there is no way to verify the actual balance that was transfered, that is why we recommend the use of `approveAndCall` to work with “verified” balance in the EIP description.

Now we have another issue that brings problem when you for example want to work with ERC223 or ERC667 tokens, you can use the fallback functions of this tokens from the ERC827 contract and drain funds of contracts. Example: [erc827/contracts/examples/VaultAttack.sol at master · windingtree/erc827 · GitHub](https://github.com/windingtree/erc827/blob/master/contracts/examples/VaultAttack.sol)

We are working on changes on the standard to prevent this from happening, the main proposal that we have for now is the use of “allowed” callbacks, wich means that the receiver contracts will be able to allow functions to be executed on it.

I think the allowedCallbacks is a good solution, it adds the necessary interface to allow contracts to execute specific and tested arbitrary calls over them. Removing this permission of execute calls on any contract form the token contract, and it adds only a ~50 lines of code.

https://github.com/windingtree/erc827/pull/2

I would like to get some feedback from here.

