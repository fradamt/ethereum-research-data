---
source: magicians
topic_id: 23699
title: EIP‑7702 breaks on‑chain provenance needed for regulated assets
author: nicszerman
date: "2025-04-21"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/eip-7702-breaks-on-chain-provenance-needed-for-regulated-assets/23699
views: 592
likes: 10
posts_count: 22
---

# EIP‑7702 breaks on‑chain provenance needed for regulated assets

**Executive Summary**

**Transfer or tokenized RWA (real-world assets)** often relies on knowing if a wallet is authorized (or not authorized) to perform a state‑changing call. EIP‑7702 breaks this: the signing wallet (the authorizer) no longer surfaces via tx.origin, which makes EIP‑7702 txs not suitable to support transfers for most RWA assets. This severely limits the potential of usage of the EIP‑7702, by parties who are supposed to be the beneficiaries of adopting the EIP-7702, namely wallets, asset issuers, RWA tokenization platforms and DeFi Protocols. Adding one VM‑level field—tx.authorizer—would restore that information without touching existing contracts or privacy, especially when tokens move atomically through pooled contracts (e.g., Uniswap → Morpho).



      [docs.google.com](https://docs.google.com/document/d/1hsaYDyrXYLt84VdHSEn9T3ixagvpQH-8t5DhSqw0Fnk/edit)



    https://docs.google.com/document/d/1hsaYDyrXYLt84VdHSEn9T3ixagvpQH-8t5DhSqw0Fnk/edit

###

EIP‑7702 breaks on‑chain provenance needed for regulated assets Nico Szerman, Sailing Protocol  Discussion: https://ethereum-magicians.org/t/eip-7702-breaks-on-chain-provenance-needed-for-regulated-assets/23699 Executive SummaryTransfer or tokenized...










**Call to Action**

Core developers should **pause finalization of EIP‑7702** until a VM‑level authorizer field (e.g., *tx.authorizer*) is specified.

Passing 7702 unamended would render many RWA and regulated‑finance use‑cases unworkable on Ethereum.

## Replies

**nicocsgy** (2025-04-21):

I left a few comments on the document but overall I don’t think the document defends your assumption that :

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nicszerman/48/5029_2.png) nicszerman:

> EIP‑7702 breaks this: the signing wallet (the authorizer) no longer surfaces via tx.origin, rendering Ethereum incompatible with regulated assets

Unless you provide a precise legal explanation as to why it would render ethereum incompatible with regulated assets, I don’t think it’s very serious to ask such a strong call to action. To delay the entire fork two weeks before the due date would require a much stronger case than the one proposed here. And even if you had such case to make this would open further debates about ethereum upgrades and not necessarily change much IMO.

---

**nicszerman** (2025-04-21):

Several types of assets require some form of allowlisting to access, for example when you create an account in a broker to buy stock of a company. Trading those on DEXes after EIP 7702 becomes impossible because there will be no way to check that the authorizer wallet can trade that asset.

> rendering Ethereum incompatible with regulated assets

Means that using the Ethereum blockchain for regulated assets becomes impossible. This is *not a claim about the asset Ethereum ETH*.

The solution is simple, although it will delay launch of EIP 7702: to surface the authorizer in a field (eg. tx.authorizer).

In the current state, EIP 7702 makes it impossible to use regulated assets on DeFi.

---

**nicszerman** (2025-04-21):

**1. Existing rules require the originator’s wallet on every on‑chain transfer**

• FATF Travel Rule (incorporated into EU Transfer‑of‑Funds Regulation and U.S. FinCEN guidance) obliges intermediaries to record and, when necessary, transmit the **originator and beneficiary wallet addresses** for virtual‑asset transfers over €1 000.

• MiCA / MiFID‑II pilots and multiple SEC S‑1 filings for tokenised securities stipulate that issuers must be able to **trace and, on request, disclose the beneficial owner** of each token movement, and most implementations achieve this with an on‑chain allow‑list.

• Current security‑token contracts therefore enforce a simple invariant inside `transfer()`:

```auto
require(allowList[tx.origin] == true, "sender not authorised");
```

Without a reliable originator field, the check fails and the token breaches supervisory rules.

---

**2. EIP‑7702 removes the only VM‑level originator signal**

Pre‑7702, `tx.origin` always equals the signing EOA, so the rule above works even when tokens pass through DEXes or vaults.

Post‑7702, a gas sponsor can be `tx.origin`, while the real signer is buried in `authorization_list` and never surfaces in the call stack. Once the flow is, for example,

```auto
Relayer (tx.origin) → UniswapPool → MorphoVault → SecurityToken.transfer()
```

no contract in that path (nor any off‑chain monitor) can recover the invisible signer mid‑transaction. The originator requirement is therefore unmet.

---

**3. A one‑line patch (tx.authorizer) fixes the gap with negligible risk**

• Clients already call `ecrecover` on each `authorization_list` element during transaction validation; surfacing the result as a read‑only field (`tx.authorizer`) is roughly twenty lines of code in geth and has zero gas impact for legacy transactions.

• ERC‑3651 (“warm COINBASE”) shows that late‑stage, consensus‑safe tweaks are feasible when they avert a systemic problem.

---

**4. Why amending 7702 matters—even though today’s DeFi‑native RWA market is small**

Security‑grade RWA tokens on public DeFi are still an **emerging niche (< US$100 M TVL)** precisely because they rely on the `tx.origin` pattern and await broader wallet support.

BlackRock, HSBC‑Orion, BIS blueprints and Coinbase Asset Hub all project **hundreds of billions in tokenised bonds and equities migrating to public chains within two to three years**, conditional on robust on‑chain enforcement of KYC/KYT rules.

If 7702 lands without an authorizer field:

1. New RWA projects will either remain on permissioned chains or build bespoke L2s, slowing Ethereum’s share of the segment.
2. The few early‑stage RWA pilots on mainnet will face costly rewrites or migration.
3. A future hard‑fork will still be required to add the missing signal—only then it will disrupt a far larger user base.

A trivial patch now prevents the ecosystem from choking off an entire asset class before it scales.

---

**5. Requested next step**

Merge the minimal variable `tx.authorizer` (or, failing that, defer 7702 to the next fork). This keeps Ethereum aligned with FATF, MiCA and SEC security‑token practices while preserving all usability gains of EIP‑7702. I am available to supply code, test vectors and detailed legal citations as needed.

---

**matt** (2025-04-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nicszerman/48/5029_2.png) nicszerman:

> 1. Existing rules require the originator’s wallet on every on‑chain transfer
> • FATF Travel Rule (incorporated into EU Transfer‑of‑Funds Regulation and U.S. FinCEN guidance) obliges intermediaries to record and, when necessary, transmit the originator and beneficiary wallet addresses for virtual‑asset transfers over €1 000.
> • MiCA / MiFID‑II pilots and multiple SEC S‑1 filings for tokenised securities stipulate that issuers must be able to trace and, on request, disclose the beneficial owner of each token movement, and most implementations achieve this with an on‑chain allow‑list.
> • Current security‑token contracts therefore enforce a simple invariant inside transfer():
>
>
>
> ```auto
> require(allowList[tx.origin] == true, "sender not authorised");
> ```
>
>
>
> Without a reliable originator field, the check fails and the token breaches supervisory rules.

I think this is just a misunderstanding of what an originator is. The `tx.origin` has nothing to with a token transfer. It *often* coincides with `from` address of a transfer, but it isn’t guaranteed. This was true before EIP-7702 with smart contract wallets and relayers in general. This is true after EIP-7702.

The “originator” should be the `from` or `msg.sender` address during `transfer()` and the beneficiary would be the `to` address. I don’t really see why there would be any disagreement on this statement. If the issue is less th

I am happy to connect with a legal expert on this matter to provide technical assistance in ensuring that `from` is understood to be the financial “originator” of the asset.

---

**nicszerman** (2025-04-21):

`from` / `msg.sender` in `transfer()` is frequently an **intermediary contract** (AMM pool, vault, router).

Today, tokens that need the *ultimate* signer whitelist `tx.origin`, because that field still points to the EOA even when calls are routed through contracts.

Under EIP‑7702 a relayer can become `tx.origin`, so the real signer disappears entirely:

```auto
Relayer (tx.origin) → UniswapPool (from/msg.sender) → transfer()
```

Neither `from` nor `tx.origin` reveals the authorizing wallet, breaking any on‑chain allow‑list.

That is the gap we’re highlighting; a new field (e.g. `tx.authorizer`) would expose the actual signer and solve it.

---

**matt** (2025-04-21):

> from / msg.sender in transfer() is frequently an intermediary contract (AMM pool, vault, router).

These are not intermediary contracts, they are the true owners of the asset. When you put an asset into an AMM pool you receive a claim on portion of the pool and what you can get with that claim will change over time. The origin of the asset is the pool. It has nothing to do with the `tx.origin`. You can follow the graph farther back and see that someone deposited into the pool. There is no issue tracking provenance using this method.

---

**nicszerman** (2025-04-21):

Imagine a Uniswap V3 pool for USDT ↔ TSLA (tokenised Tesla stock).

When Alice swaps USDT for TSLA, the TSLA contract’s `transfer()` runs with

```auto
msg.sender == UniswapPool   // the pool contract
```

The **only** on‑chain signal that Alice herself authorised the move is

```auto
tx.origin == Alice          // the signing EOA
```

Security‑grade tokens rely on that check to decide whether the transfer is valid.

EIP‑7702 lets a gas relayer replace `tx.origin`, destroying this provenance link and making it impossible to vet the swap in real time—dramatically setting back on‑chain finance for regulated assets.

---

**frangio** (2025-04-21):

The use of `tx.origin` in this way is a workaround that breaks in simple cases without need to invoke EIP-7702. For example, this token would not be tradeable on CoW Swap today, because in CoW Swap an order is authorized by the token holder via a signature and submitted on chain by a solver (a relayer). This doesn’t break the token or its provenance, it just makes the token unusable with CoW Swap. Similarly, EIP-7702 doesn’t break this kind of token, it just introduces another context where the token can’t be used.

EIP-7702 is at most reinforcing the fact that this workaround is not a full solution to the problem.

Additionally, this doesn’t seem right:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nicszerman/48/5029_2.png) nicszerman:

> The only on‑chain signal that Alice herself authorised the move is
>
>
>
> ```auto
> tx.origin == Alice          // the signing EOA
> ```

The real signal that Alice has authorized the move is the fact that `transfer` or `transferFrom` succeeded. When those functions execute, the token is free to store any additional information it may need to process further transactions. I don’t believe that `tx.origin` is the only way this can be implemented.

Could you provide links to contracts in use that implement this kind of logic?

---

**nicszerman** (2025-04-22):

**Clarifications**

1. tx.origin is not perfect, but it’s the only real‑time signal available.
Compliance‑grade tokens (ERC‑1400 / 1404 variants) gate transfers with require(allowlist[tx.origin], "unauthorised")
That lets them flow through AMMs and vaults while still blocking meta‑transactions, which are uncommon in retail wallets today. CoW Swap is therefore intentionally unsupported by those issuers.
2. EIP‑7702 removes even that best‑available fallback.
After 7702 a gas sponsor can replace tx.origin, so the same contract reverts on every ordinary delegated‑wallet swap—not just on edge‑case relayers. The “exception” becomes the default path.
3. “Transfer success is the proof” isn’t enough.
The token must decide before state mutation whether the actor is authorised. Recording extra data after transfer() succeeds can’t retroactively block an illegal move.
4. tx.authorizer resolves all cases—including CoW Swap and sponsored wallets.
With an explicit authoriser field:

- AMM / vault routing continues to work.
- CoW Swap orders can be routed through the user’s EOA (authoriser == signer) and pass the same single check.
- Issuers avoid a patchwork of bespoke exceptions.

On‑chain RWA projects have been biding their time for the ecosystem to mature, and until now the best practical guard was an allow‑list on `tx.origin`. EIP‑7702 removes that guard entirely. Introducing `tx.authorizer` not only restores it—it upgrades it into a fully composable solution that also supports CoW‑Swap–style meta‑txs and smart‑wallet sponsorship.

---

**matt** (2025-04-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nicszerman/48/5029_2.png) nicszerman:

> The token must decide before state mutation whether the actor is authorised. Recording extra data after transfer() succeeds can’t retroactively block an illegal move.

In your example, Alice swaps USDT for TSLA. Why can `transfer()` not check the `to` address of the transfer? I don’t see why it matters for security tokens who is paying for the gas.

---

**nicszerman** (2025-04-22):

Because the `to` address may be a smart contract controlled by Alice. Without *a link* to Alice (the existing tx.origin), it will be impossible to know at the ERC-20 level if the transfer should go through.

---

**hrkrshnn** (2025-04-22):

[@nicszerman](/u/nicszerman) I don’t have full context here; I’ve only taken a cursory look at this issue.

But if the use case you are trying to achieve is limiting who can trade a certain asset on a market maker / AMM, the best way to do that is to deploy the pool, such as on Uniswap, with a custom hook. Here’s an example of such a hook I found with a quick search: [GitHub - blackbera/whitelist-hook](https://github.com/blackbera/whitelist-hook). Coinbase even has a product that uses this: https://x.com/coinbase/status/1902031823900647583

---

**gaavar** (2025-04-22):

Please review the full discussion. It provides a lot of important context.

Allowlisting via a hook doesn’t work since the `to` address (receiver) can be another smart contract controlled by Alice (referring to the thread conversation above). In the current EIP-7702 proposed changes, the `tx.origin` can be a gas sponsor, which doesn’t reveal the authorizer i.e. Alice. And if allowlists have to be done for even contracts (for the `to` or receiver), such pools are useless since AMMs and other contracts cannot use such pools without extensive allowlisting.

---

**gaavar** (2025-04-22):

I would urge the contributors to pay more attention to critically **understanding** the issue first and then **addressing** the gap this EIP introduces, as presented in this discussion,  rather just pushing for this upgrade to happen for sentimental reasons.

---

**Ivshti** (2025-04-22):

Have you considered that Alice may not have a signing EOA? Alice may be a P256 verifying contract, Alice may be a DAO, Alice may be a multisig of multiple private keys all owned by Alice.

There’s no such thing as a strict “signing EOA”

It’s deeply entranched in the Ethereum concept (and now reinforced by EIP-7702)

The only true way to do allow lists is based on the caller (msg.sender). tx.origin is irrelevant

---

**hrkrshnn** (2025-04-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gaavar/48/14984_2.png) gaavar:

> Allowlisting via a hook doesn’t work since the to address (receiver) can be another smart contract controlled by Alice (referring to the thread conversation above). In the current EIP-7702 proposed changes, the tx.origin can be a gas sponsor, which doesn’t reveal the authorizer i.e. Alice. And if allowlists have to be done for even contracts (for the to or receiver), such pools are useless since AMMs and other contracts cannot use such pools without extensive allowlisting.

You can whitelist based on who is trading and also who gets to receive (i.e., in both directions).

Do you have links to contracts / addresses that would break after this upgrade?

---

**nicszerman** (2025-04-22):

message from matt, the EIP author:

> So what i understand is this flow doesn’t work post 7702:
>
>
> Alice wants to buy TSLA via a proxy like a some directed fund (yearn?). They are KYC’d so they think they can purchase. They deposit USDC or ETH to the proxy and the proxy tries to buy the TSLA from uniswap, however, the proxy isn’t KYC’d and so the proposed fix of using to in transfer() would fail, even though Alice is KYC’d.
>
>
> There is no great way of getting the info to the token that it is actually going to be owned by Alice via the proxy.
>
>
> My biggest pushback might be that this flow might simply not be possible. One thing is for sure that using to allows normal people to go to uniswap and buy RWAs if they are on an allow list. If they want a proxy to know they are the owners w/o going awry with allow listing, we either need i) the asset to flow through Alice before going to the pool to ensure provenance or ii) the proxy needs to gate to only allow KYC’d entities and they it itself can become allow listed and the above flow will directly work

---

**yaonam** (2025-04-22):

I think it is undisputed that RWAs are important, just that the unfortunate timing of this discussion also requires consideration. Would love to find a solution that works for everyone.

Assuming:

- Whitelisting of initial token transferer is sufficient for KYC (the initial address whether it be EOA, multisig, AA, etc.).
- RWA token supports custom logic (as evidenced by the tx.origin check above).

Could **transient storage** work as a solution? The transfer function can contain something along the lines of

```auto
require(whitelist[msg.sender] || checkIfUnlockedViaTload());
unlockViaTstore();
// Proceed with transfer
```

Then the flow Alice → DEX → … → DEX → recipient works. Correct me if I’m misunderstanding something.

---

**matt** (2025-04-22):

So here are my thoughts on the matter:

1. The protocol you have proposed is using tx.origin in a way that is not consistent with the communicated evolution of Ethereum and AA. You mention yourself that the protocol does not work with GSN / ERC-4337 due to relayers. We have been saying for a while that this is the direction Ethereum is heading, so building a protocol around this is unfortunately short-sighted.
2. We have provided you a few potential ways to avoid using tx.origin. By using to in transfer() users can get most of the basic functionality for RWAs like buying them from an AMM and directly holding them. If it is necessary to have more complicated protocols, each of those protocols be KYC’d and then KYC all of their users. It might also be possible to use transient storage as @yaonam mentioned.
3. The changes you have proposed for 7702 do not even achieve what you want. Setting the code is only the beginning of the lifecycle of the operation, in the future they can get relayed like a 4337 account using a normal transaction. So your protocol is broken even under that. The only reason your system works is because you’ve overloaded the meaning of tx.origin.

---

**nicszerman** (2025-04-22):

Thanks. Re point 3: even when the tx is relayed, the user EOA will be in the call stack, right? so tx.authorizer would work then?


*(1 more replies not shown)*
