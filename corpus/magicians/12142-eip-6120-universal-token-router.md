---
source: magicians
topic_id: 12142
title: "EIP-6120: Universal Token Router"
author: zergity
date: "2022-12-14"
category: Uncategorized
tags: [erc-721, erc-20, erc1155]
url: https://ethereum-magicians.org/t/eip-6120-universal-token-router/12142
views: 2957
likes: 5
posts_count: 13
---

# EIP-6120: Universal Token Router

ETH is designed with transfer-and-call as the default behavior in a transaction. Unfortunately, ERC-20 is not designed with that pattern in mind and newer standards cannot apply to the token contracts that have already been deployed.

Application and router contracts have to use the approve-then-call pattern which costs additional `n*m*l` `allow` (or `permit`) transactions, for `n` contracts, `m` tokens, and `l` user addresses. These allowance transactions not only cost a lot of user gas, worsen user experience, waste network storage and throughput, but they also put users at serious security risks as they often have to approve unaudited, unverified and upgradable proxy contracts.

The Universal Token Router (UTR) separates the token allowance from the application logic, allowing any token to be spent in a contract call the same way with ETH, without approving any other application contracts.

Tokens approved to the Universal Token Router can only be spent in transactions directly signed by their owner, and they have clearly visible token transfer behavior, including token types (ETH, ERC-20, ERC-721 or ERC-1155), `amountIn`, `amountOutMin`, and `recipient`.

The Universal Token Router contract is counter-factually deployed using EIP-1014 at a single address across all EVM-compatible networks, so new token contracts can pre-configure it as a trusted spender, and no approval transaction is necessary for their interactive usage.



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-6120)





###



A single router contract enables tokens to be sent to application contracts in the transfer-and-call manner instead of approve-then-call.

## Replies

**zergity** (2023-02-03):

New update has been merged with the following changes:

- Using mode for input tokens and flags for action for better visibility
- add IN_TX_PAYMENT input token mode for payment-in-callback style contracts (e.g. Uniswap/v3)
- add ALLOWANCE_BRIDGE as a compatibility input token mode for contracts that directly called transferFrom for pull payment
- add more Sample Usages for Uniswap/v3 swap and liquidity functionalities.

---

**chompomonim** (2023-02-09):

How this relates to uniswap’s permit2 and universal router?


      ![image](https://app.uniswap.org/favicon.png)

      [app.uniswap.org](https://app.uniswap.org/)



    ![image](https://app.uniswap.org/images/1200x630_Rich_Link_Preview_Image.png)

###



Swap or provide liquidity on the Uniswap Protocol

---

**zergity** (2023-02-14):

[chompomonim](https://ethereum-magicians.org/u/chompomonim)

In short, not related at all, I simply use Uniswap for examples, but it’s designed for every kind of application contract.

Uniswap’s Universal Router is only “universal” for Uniswap, not for other applications. Other applications cannot use it for their logic.

Permit2 has two modes, the closest thing to EIP-6120 is the SignatureTransfer mode, but the UX is different, and SignatureTransfer cannot prevent phishing attacks like EIP-6120.

Permit2 requires application contracts to be redesigned entirely, no backward compatibility. EIP-6120 is designed for both new and existing contracts to use.

---

**h4l** (2023-04-10):

(I privately contacted the authors about a vulnerability in the implementation, and have approval to post it here.)

Thanks for this proposal. I found it while investigating possible alternatives to Permit2-type signature schemes. I can see the UX benefits of avoiding the need for authorisations, and the security benefits of being able to show and explicitly guarantee the token outputs of a transaction in a wallet before sending. Although I fear that there is a chicken-and-egg situation here, that unless the scheme has support from wallets to visualise the transaction input and output constraints, users won’t be able to understand what they’re guaranteeing, which could result in them accepting transactions without understanding the implications anyway. And wallets probably need user adoption before they would invest the effort to visualise this kind of interaction.

This makes me wonder if there is, or we collectively need a way to create shared, approved visualisations of contract calls (and likewise for structured signatures), so that wallets could have a generic way of showing a reasonable representation of an action without needing to hand-craft a special case for every call.

More significantly though, while reading the example implementation, **I noticed a vulnerability that allows a contract to withdraw funds held by the router during a call without authorisation**.

The router returns unspent funds to the caller, but doesn’t check if a call is reentrant and doesn’t segregate the funds of concurrent calls, so a reentrant `exec()` call can transfer 0 tokens into the router and the router will refund the reentrant call funds deposited into the router from the outer call.

So if a trusted protocol intentionally executed by the router interacts with any untrusted code, that untrusted code could call back into the router to withdraw funds it wan’t intended to have access to.

I have repo of the issue here: https://github.com/h4l/erc-6120-poc/blob/main/test/UniversalTokenRouter.t.sol

As well as ERC-20s and Eth, this also applies to NFT tokens, but I didn’t implement reproductions for those.

The issue could be mitigated by tight use of the output enforcement feature your contract provides, which does demonstrate the strength of this kind of approach. But I expect that in practice it is not possible to precisely define the exact outputs, whether because the exact result is not known, or because the transaction is one-way, e.g. depositing funds without immediately receiving something equivalent. So a malicious contract could skim off a portion of funds without being caught, or could do things like swap one NFT for another inside a transaction, which may not be caught by output constraints for NFT counts. (e.g. when minting an NFT, the `tokenId` is not always known, so the minted token could be swapped out in the router by an untrusted contract — a rare one for a common one for example.)

---

**zergity** (2023-04-10):

Thank [@h4l](/u/h4l) for reviewing the EIP.

I’ve looked at your POC repo, let me address each part of your comment separately.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/h4l/48/8950_2.png) h4l:

> More significantly though, while reading the example implementation, I noticed a vulnerability that allows a contract to withdraw funds held by the router during a call without authorisation.
>
>
> The router returns unspent funds to the caller, but doesn’t check if a call is reentrant and doesn’t segregate the funds of concurrent calls, so a reentrant exec() call can transfer 0 tokens into the router and the router will refund the reentrant call funds deposited into the router from the outer call.
>
>
> So if a trusted protocol intentionally executed by the router interacts with any untrusted code, that untrusted code could call back into the router to withdraw funds it wan’t intended to have access to.
>
>
> I have repo of the issue here: erc-6120-poc/test/UniversalTokenRouter.t.sol at main · h4l/erc-6120-poc · GitHub
>
>
> As well as ERC-20s and Eth, this also applies to NFT tokens, but I didn’t implement reproductions for those.

By directly or indirectly invoking malicious code in input Action, amounts of tokens that “have already agreed to be spent” by the user can be stolen.

Scope:

- Other users are unaffected.
- Only the token amounts that have been agreed to be spent by that specific transaction can be stolen.
- Only if the transaction does not use Output verification.

There are 2 ways for bad guys to achieve this:

- phishing sites: they don’t need UTR to do this; using ERC20.transfer or UniswapRouter.swap would have the same effect.
- sneak a malicious code in action down the call stack (especially common in DEX aggregators), which is why the Output verification is always recommended for UTR, and to your next point below.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/h4l/48/8950_2.png) h4l:

> The issue could be mitigated by tight use of the output enforcement feature your contract provides, which does demonstrate the strength of this kind of approach. But I expect that in practice it is not possible to precisely define the exact outputs, whether because the exact result is not known, or because the transaction is one-way, e.g. depositing funds without immediately receiving something equivalent. So a malicious contract could skim off a portion of funds without being caught, or could do things like swap one NFT for another inside a transaction, which may not be caught by output constraints for NFT counts. (e.g. when minting an NFT, the tokenId is not always known, so the minted token could be swapped out in the router by an untrusted contract — a rare one for a common one for example.)

As it has been written in the last sentence of the **Motivation** section, non-token results can be checked with a contract call, although it’s not in the `outputs` param.

> With non-token results, application helper contracts can provide additional result-checking functions for UTR’s output verification.

---

**h4l** (2023-04-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/zergity/48/3631_2.png) zergity:

> Scope:
>
>
> Other users are unaffected.
> Only the token amounts that have been agreed to be spent by that specific transaction can be stolen.
> Only if the transaction does not use Output verification.

I agree.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/zergity/48/3631_2.png) zergity:

> There are 2 ways for bad guys to achieve this:
>
>
> phishing sites: they don’t need UTR to do this; using ERC20.transfer or UniswapRouter.swap would have the same effect.
> sneak a malicious code in action down the call stack (especially common in DEX aggregators), which is why the Output verification is always recommended for UTR, and to your next point below.

The difference I see is that normally malicious code would need to be approved by a user to spend their ERC20 — the user sees a transaction to call approve for the malicious contract (even if a phishing site tries to obfuscate what’s happening). With this issue, malicious code inherits the trust the user has for the router, so a user never needs to authorise the malicious contract.

For example, someone could send me a random spam NFT that contains malicious code that tries to call into UTR from its `safeTransferFrom()` function. Normally this contract could do no harm if I transferred it because I wouldn’t approve it to operate anything I care about. But if I transferred it inside a more complex UTR call with several operations, this contract would be able to drain funds from UTR mid way through the operation (if I didn’t set strict output conditions).

If I understand right, I think your saying that a malicious/insecure DEX could route your order through a malicious ERC20 without the user needing to authorise it (because the DEX itself is the one sending the funds), but this is a different situation — here there’s an unbroken chain of trust from the user “trusting” the bad DEX, which then trusts the bad ERC20. But in the situation I describe I think it’s different because the user has no expectation that any arbitrary contract can operate funds in flight. But UTR does in effect trust anything it indirectly calls to withdraw funds. This changes the trust assumptions a developer or user has to make about contracts that are interacted with inside a transaction.

From the EIP:

> The Universal Token Router promotes the security-by-result model in decentralized applications instead of security-by-process .

If the indirect trust I describe is intentional, I feel like this is unnecessarily sacrificing security-by-process as you put it. The security-by-result property is excellent, but I don’t think it needs to come at the expense of security-by-process — having both is better than one or the other.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/zergity/48/3631_2.png) zergity:

> As it has been written in the last sentence of the Motivation section, non-token results can be checked with a contract call, although it’s not in the outputs param.
>
>
>
> With non-token results, application helper contracts can provide additional result-checking functions for UTR’s output verification.

Thanks for clarifying this, I was meaning to ask about that, as I didn’t see a way to call a verifying contract via outputs.

---

**zergity** (2023-04-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/h4l/48/8950_2.png) h4l:

> For example, someone could send me a random spam NFT that contains malicious code that tries to call into UTR from its safeTransferFrom() function. Normally this contract could do no harm if I transferred it because I wouldn’t approve it to operate anything I care about. But if I transferred it inside a more complex UTR call with several operations, this contract would be able to drain funds from UTR mid way through the operation (if I didn’t set strict output conditions).
>
>
> If I understand right, I think your saying that a malicious/insecure DEX could route your order through a malicious ERC20 without the user needing to authorise it (because the DEX itself is the one sending the funds), but this is a different situation — here there’s an unbroken chain of trust from the user “trusting” the bad DEX, which then trusts the bad ERC20. But in the situation I describe I think it’s different because the user has no expectation that any arbitrary contract can operate funds in flight. But UTR does in effect trust anything it indirectly calls to withdraw funds. This changes the trust assumptions a developer or user has to make about contracts that are interacted with inside a transaction.
>
>
> From the EIP:
>
>
>
> The Universal Token Router promotes the security-by-result model in decentralized applications instead of security-by-process .

If the indirect trust I describe is intentional, I feel like this is unnecessarily sacrificing security-by-process as you put it. The security-by-result property is excellent, but I don’t think it needs to come at the expense of security-by-process — having both is better than one or the other.

Excellent put. And applying non-reentrancy to the UTR would be sufficient for this. We’ll need to carefully consider if we miss any use-case by doing so.

---

**zergity** (2023-04-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/h4l/48/8950_2.png) h4l:

> Although I fear that there is a chicken-and-egg situation here, that unless the scheme has support from wallets to visualise the transaction input and output constraints, users won’t be able to understand what they’re guaranteeing, which could result in them accepting transactions without understanding the implications anyway. And wallets probably need user adoption before they would invest the effort to visualise this kind of interaction.

Support from wallets is great to have, but it’s not necessary. Without wallet support, UTR is just another “router” that multiple applications can share. It naturally has a ripple effect: the more applications use it, the more useful/attractive to other applications.

We planned to use it as part of our protocol, once it’s audited and put to use, other applications can just tag along and piggyback off the UTR without putting their users at unnecessary risk. The front-end code of piggybacking applications can perform like this:

1. if a user has her token approved to the UTR, use UTR
2. if a user has her token approved to their router, use their router
3. otherwise, ask user to approve their router

Applications can deploy their own *limited* UTR versions, that are only allowed to interact with their contracts while piggybacking on the public UTR.

When the UTR is battle-tested and well-proven to the community, wallets will support it, (which again, is a nice addition, not a requirement). Besides, supporting UTR is simply supporting arbitrary ABI-decoded transactions, which I personally think should be standard by now.

---

**h4l** (2023-04-10):

You paint a promising picture, I hope your vision plays out!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/zergity/48/3631_2.png) zergity:

> Applications can deploy their own limited UTR versions, that are only allowed to interact with their contracts while piggybacking on the public UTR.

That’s an interesting idea, I’ll have to think about this. Are you thinking that a user transaction would start from the public UTR (to make use of existing token approvals) then immediately call into the App’s own UTR to do the actual work?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/zergity/48/3631_2.png) zergity:

> When the UTR is battle-tested and well-proven to the community, wallets will support it, (which again, is a nice addition, not a requirement). Besides, supporting UTR is simply supporting arbitrary ABI-decoded transactions, which I personally think should be standard by now.

It certainly should be possible for wallets to look up and decode calls using a database like https://www.4byte.directory/ . I feel like it’s still necessary to have a layer above this to explain the implications of a function call to a user, particularly when you have chain of several calls. I’ve not used it myself, but I recall hearing that the Fuel VM allows transactions to consist of multiple calls, I wonder what they do to present that to users. Perhaps this is an area where AI and Crypto can mix in a genuinely useful way — using an LLM AI to generate descriptions of an arbitrary sequence of function calls…

---

**zergity** (2023-04-24):

New update has been merged to greatly simplify the standard by focusing only on token allowance, and let adapter contracts handle the rest of the complexity:

- remove action.flags and its usages
- remove amountInSource and its usages
- rename amountInMax to amountIn
- remove ALLOWANCE and *_FROM_ROUTER modes
- input mode now only have 3 values: PAYMENT, TRANSFER, and CALL_VALUE
- add UTR.discard function to discard a portion of pending payment

Tokens should not be transferred to the UTR in the new standard. An entire **Security Considerations** section is dedicated to [@h4l](/u/h4l) exploit in [GitHub - h4l/erc-6120-poc](https://github.com/h4l/erc-6120-poc)

The Compatibility section suggests the usage of Helper/Adapter contracts:

> Additional helper and adapter contracts might be needed, but they’re mostly peripheral and non-intrusive. They don’t hold any tokens or allowances, so they can be frequently updated and have little to no security impact on the core application contracts.

---

**h4l** (2023-04-30):

I like the sound of this simplification! I’ve not looked through in detail yet, but I hope to soon.

When skimming through just now I noticed what I think would have been another problem with the previous design that is not possible in this simplified version. Similarly to the re-entrancy issue, I think it would have been possible for an attacker to use `Action` to have the router call `someERC20Token.approve(attacker, MAX)` to grant itself an approval to operate a token owned by the router. Then in a later transaction from another user, if the attacker could arrange for its code to be invoked, it could have transferred tokens out of the router using its previously-created approval. As I say, this is not possible now that the router does not hold tokens.

Related to the above — and I’ve not thought about this in any real depth — but in principle, users of the router can effectively act as its owner, so they can do things like call [ERC1820Registry.setInterfaceImplementer()](https://eips.ethereum.org/EIPS/eip-1820) (or just `setManager()`) to register their own contracts. It seems like this would only be a problem in very limited/specific situations, but in general, users sharing control of an address with the ability to take arbitrary actions as the address does leave open a long tail of potential edge cases.

---

**zergity** (2023-05-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/h4l/48/8950_2.png) h4l:

> When skimming through just now I noticed what I think would have been another problem with the previous design that is not possible in this simplified version. Similarly to the re-entrancy issue, I think it would have been possible for an attacker to use Action to have the router call someERC20Token.approve(attacker, MAX) to grant itself an approval to operate a token owned by the router. Then in a later transaction from another user, if the attacker could arrange for its code to be invoked, it could have transferred tokens out of the router using its previously-created approval. As I say, this is not possible now that the router does not hold tokens.

Yes, that should be the same exploit, which I’ve tried to addressed by the last update.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/h4l/48/8950_2.png) h4l:

> Related to the above — and I’ve not thought about this in any real depth — but in principle, users of the router can effectively act as its owner, so they can do things like call ERC1820Registry.setInterfaceImplementer() (or just setManager()) to register their own contracts. It seems like this would only be a problem in very limited/specific situations, but in general, users sharing control of an address with the ability to take arbitrary actions as the address does leave open a long tail of potential edge cases.

Yes, it’s problematic if applications misuse the UTR and mess up user data ownership, but I’d say that it’s no different from other *sharing* contracts. For example, those same mistakes can also happen with [multicall](https://github.com/mds1/multicall) contracts.

