---
source: magicians
topic_id: 16153
title: "EIP-7540: Asynchronous ERC-4626 Tokenized Vaults"
author: joeysantoro
date: "2023-10-18"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/eip-7540-asynchronous-erc-4626-tokenized-vaults/16153
views: 9897
likes: 24
posts_count: 24
---

# EIP-7540: Asynchronous ERC-4626 Tokenized Vaults

see [ERC-7540: Asynchronous ERC-4626 Tokenized Vaults](https://eips.ethereum.org/EIPS/eip-7540) for most up to date spec

## Replies

**Mani-T** (2023-10-19):

The Request lifecycle, encompassing Pending, Claimable, and Claimed stages, offers a clear process for asynchronous interactions. This is very useful.

---

**0xfarhaan** (2023-10-19):

Awesome stuff folks great EIP to help standardise this async flow. We’ve had to deal with the exact same problem over at Maple. We’ve had an async flow for redemptions in production since December last year on our 4626 vault that has worked well for us so far. Will share some learnings and feedback in the coming days but the proposal looks good!

---

**tom2o17** (2023-10-19):

Looks [familiar](https://etherscan.io/address/0x5577Cf81459b742Dbfe757f98cB3eD4eD8e7Df30#code) ![:eyes:](https://ethereum-magicians.org/images/emoji/twitter/eyes.png?v=12)

---

**Yakitori** (2023-10-21):

Hi Joey, nice to see you since the days of the Rari hack and the drama that followed.

I’ve been working on a similar design with [Astrolab.fi](http://Astrolab.fi) for cross-chain vaults, which is a likely use case. After some iterations and testing, we decided to ditch this design. Why? Mainly, bad UX.

- There is no way to know how much you’ll get when you request to redeem your share tokens. This creates a lot of moral hazard, as there’s a risk that the users get a lot less than what they thought they would get. In a classic ERC4626, you can estimate it precisely by doing a static call simulation beforehand.
- In the above specs, locking shares when redeeming is optional. Since it’s a very important feature, I think it shouldn’t be optional as it creates ambiguity, or at least have a designated view call, or a specific function name, so the user/integrator to know what expect. Because vaults are often user/retail facing, and the point of this EIP is to standardize them, I believe making it straightforward would have a great value.
- Most vault developers will make it mandatory, to avoid spam from users. A problem arises here in that a user asking for a redeem and locking his shares is “naked”. If, during a bank run, everyone asks to redeem shares, only to see a portion of the requests fulfilled, you can’t sell your remaining claims OTC or to a liquidity pool.

As for [Astrolab.fi](http://Astrolab.fi), we went with a model including an internal stable swap, to process atomically withdrawals. A share token is worth x “virtual asset tokens” that are swapped for the “real asset” tokens in the reserve (that can themselves be invested in a liquid form). This solves the above points:

- You can do a static call to estimate precisely how much you’ll get when withdrawing.
- It is ERC4626 compliant. You can use add a wrapper to set a minAmount to prevent any front-running.
- In case of a bank run, if the internal stableswap gets depleted, convexity kicks in and slippage increases. This also allows buying back discounted share tokens, either by other users, or by the vault itself. Slippage on the way out thus becomes a proxy of time/money arbitrage.
- If large depositors want to redeem without slippage, they can set up a limit order to redeem at their desired price. Or a redemption mechanism similar to what is proposed here can be set up. It has however drawbacks, as explained above.

Vaults with illiquid assets are hard to get right, and I’m happy that we can have this discussion !

---

**0xfarhaan** (2023-10-22):

Hey everyone sharing some thoughts and learnings from our experience running async 4626 vaults at Maple Finance over the past year.

### What we like:

- Acknowledgement of the changing exchange rate between requests for deposit/redemption and the actual deposit/redeem. We’ve also as a result not implemented a withdraw flow as a result. Support the non-inclusion of requestWithdraw and requestMint
- Support that the standard proposes optionality of flows as there may be cases where both redemptions and deposits need to be requested, but this is a case by case basis depending on the RWA in question. (e.g our of business hours deposits can cause APY drag on other LPs).
- Support that the standard doesn’t enforce that yield should stop or continue to accrue during requests and as a result if there is a fixed or variable exchange rate. This is super important as different RWA’s have different requirements and should be left to the implementor.

### Open Questions / Considerations:

- Why not just use approvals instead of introducing an operator param ? The owner can approve an operator ahead of a requestRedemption call and once a redemption is claimable assuming an operator has the appropriate approval amount they can call redeem on behalf of the user. This gives flexibility to the owner to decide who can redeem on their behalf once a redemption is requested, as some RWA assets could take weeks to liquidate and become claimable and a LP might want to change who can claim.

> Requests MUST NOT skip or otherwise short-circuit the claim step. In other words, to initiate and claim a request, a user MUST call both request* and the corresponding claim function separately, even in the same block

- Just to clarify the above quote, a user may request to redeem but in another block once redemptions are processed can the redemptions be pushed directly to the LP as opposed to requiring the claim step? Whilst I agree for smart contract integrations a redeem flow where the owner/operator pull funds via a redeem call is required some LPs may prefer just to have to request the redemption and let the vault operator push funds directly to the LP as part of processing redemptions.

### Closing thoughts:

- Overall supportive of the proposal would like some discussion about the need for an operator.
- Agree figuring out cancellations of requests is complex, we’ve got a specific implementation that works for our redemption mechanism which you can see below.
- Feel free to take a look at our Pool.sol and PoolManager.sol contracts where we implement the requestRedeem and redeem async flows that we’ve had in production for the past year here.

---

**joeysantoro** (2023-10-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yakitori/48/10759_2.png) Yakitori:

> There is no way to know how much you’ll get when you request to redeem your share tokens. This creates a lot of moral hazard, as there’s a risk that the users get a lot less than what they thought they would get. In a classic ERC4626, you can estimate it precisely by doing a static call simulation beforehand.

This is a valid point and at least worth adding to the security considerations. Any mechanism which *requires* asynchronicity by definition cannot quote the user a min amount out and any kind of slippage protection would add too many edge cases and implementation complexity. The core design assumption is that depositors trust the vault as many async vaults have more centralized backend operations. Therefore having the ambiguity is the lesser evil and ok as long as users are aware.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yakitori/48/10759_2.png) Yakitori:

> In the above specs, locking shares when redeeming is optional.

It isn’t optional, the shares must either be locked in the vault or burned depending on implementation details.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yakitori/48/10759_2.png) Yakitori:

> Most vault developers will make it mandatory, to avoid spam from users. A problem arises here in that a user asking for a redeem and locking his shares is “naked”. If, during a bank run, everyone asks to redeem shares, only to see a portion of the requests fulfilled, you can’t sell your remaining claims OTC or to a liquidity pool.

This should also be added to the security section. Vaults may even wrap claims in an NFT or ERC-20 for some secondary liquidity. Still a core aspect of the assumptions and design of the vault.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/0xfarhaan/48/10736_2.png) 0xfarhaan:

> Why not just use approvals instead of introducing an operator param ? The owner can approve an operator ahead of a requestRedemption call and once a redemption is claimable assuming an operator has the appropriate approval amount they can call redeem on behalf of the user. This gives flexibility to the owner to decide who can redeem on their behalf once a redemption is requested, as some RWA assets could take weeks to liquidate and become claimable and a LP might want to change who can claim.

An operator param is better than an approval because the operator param is stored internally in the vault implementation as part of the same call. Requiring users and the vault to maintain a separate approval status for async pending deposits, async pending redeems, and internal shares (which are all not fungible with each other). Some vaults could require operator=msg.sender to remove this implementation complexity.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/0xfarhaan/48/10736_2.png) 0xfarhaan:

> some LPs may prefer just to have to request the redemption and let the vault operator push funds directly to the LP as part of processing redemptions.

sure the LPs prefer this but is it economical or wise to allow the standard to acommodate the use case?

Too much optionality makes it impossible for integrating smart contracts to intelligently handle all use cases. Is it a two step deposit? what about withdrawals? can the vault push tokens to me at some random time?

Push per LP is generally expensive and intractable, and pull use cases scale much better. Higher abstraction layers such as EIP-712 signatures and smart wallets can handle the second step, but the standard should explicitly not allow this in my opinion.

That being said I am open to having it be allowed if there are better arguments that outweigh the negatives.

---

**sogipec** (2023-10-27):

Thanks for putting this interesting proposal! Makes me think of the work I had started a year ago when we started to think about the idea with Angle (reference [here](https://anglemoney.notion.site/An-ERC4626-Extension-for-Under-Collateralized-Lending-Protocols-c1034110728a4f02b63cc797ceb1463a?pvs=4))

Lots of similar thoughts, notably on the fact that in the process to redeem a request you must account for shares and not assets, which makes it otherwise manipulable. Sometimes wishing I had make this work more broadly available.

I do believe that this EIP provides a better naming than what I had, and the ability to do async deposit as well which I hadn’t thought of in my original work.

So fully supportive of the EIP how it is now on my end, and glad to see all these iterations on the initial idea.

I fear however that the vanilla implementation for a contract under this EIP is going to be trickier than expected. While this EIP provides clarity, there may be a looot of degrees of liberty for people implementing it when it comes to the underlying design choices they can make. This is in fact similar to what you sometimes have for ERC4626 vaults, where when developing contracts you often have to deal with exceptions (e.g dealing with a loss in lending protocol) which force you to find workarounds to respect the standard.

On this note, in my past work, I had shared some ideas of how a `redeemRequest` call could look like under the hood to handle a queue system of multiple redeeming one by one. Happy to share a corresponding implementation if some are interested.

---

**joeysantoro** (2023-10-27):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/s/ee7513/48.png) sogipec:

> I fear however that the vanilla implementation for a contract under this EIP is going to be trickier than expected.

I agree completely. I think the developer framework around this EIP looks a lot more like a guidebook with different implementations than a set in stone OpenZeppelin base contract.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/s/ee7513/48.png) sogipec:

> Happy to share a corresponding implementation if some are interested.

Would love to see this!

---

**signalxu** (2023-10-31):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/joeysantoro/48/5147_2.png) joeysantoro:

> Certain use cases are only asynchronous on one flow but not the other between Request and redeem. A good example of an asynchronous redemption Vault is a liquid staking token. The unstaking period necessitates support for asynchronous withdrawals, however, deposits can be fully synchronous.

Hey, joey, thx for sharing! For the majority of LST protocol, their vault asset is Native ETH not ERC20, would like to know how could this standard could be used for LST protocol?

---

**devops199fan** (2023-10-31):

There is another EIP for native ETH based 4626 vaults: [EIP-7535: ETH (Native Asset) Tokenized Vault](https://ethereum-magicians.org/t/eip-7535-eth-native-asset-tokenized-vault/16068)

---

**0xfarhaan** (2023-11-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/joeysantoro/48/5147_2.png) joeysantoro:

> An operator param is better than an approval because the operator param is stored internally in the vault implementation as part of the same call. Requiring users and the vault to maintain a separate approval status for async pending deposits, async pending redeems, and internal shares (which are all not fungible with each other). Some vaults could require operator=msg.sender to remove this implementation complexity.

My main concern is with approvals an owner can revoke and give another operator the approval in order to process the redemption request. In the context of RWA assets redemption lead times could be hours to weeks if not longer and having the owner locked into a specific operator is problematic.

I see two potential ways forward, one is with approvals as already discussed or alternatively a nested mapping where the owner stores the operator e.g

```auto
function pendingRequestRedeem(address owner, address operator) returns (uint256 shares)
```

this way an owner can go back and change the operator that would service their redemption once it becomes claimable.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/joeysantoro/48/5147_2.png) joeysantoro:

> sure the LPs prefer this but is it economical or wise to allow the standard to acommodate the use case?
>
>
> Too much optionality makes it impossible for integrating smart contracts to intelligently handle all use cases. Is it a two step deposit? what about withdrawals? can the vault push tokens to me at some random time?
>
>
> Push per LP is generally expensive and intractable, and pull use cases scale much better. Higher abstraction layers such as EIP-712 signatures and smart wallets can handle the second step, but the standard should explicitly not allow this in my opinion.
>
>
> That being said I am open to having it be allowed if there are better arguments that outweigh the negatives.

That is fine in our case we see using both but as long as the EIP requirement is fulfilled I don’t see any harm in protocols extending the standard further (lol) to support differing use cases.

If you folks need any help with writing the reference implementation let me know, Maple are heavy users of the 4626 vaults already (with async flows) and would be happy to contribute to getting this across the line.

---

**Amxx** (2023-11-28):

I just learned about this ERC and I’m very interrested.

My understanding is that assets that are Pending can be queried using the `pendingDepositRequest` and  `pendingRedeemRequest` function, where as the assets that are Claimable can be queried using the ERC4626 `maxDeposit` and `maxRedeem` functions. However, users have no way to know when the assets/shares will become Claimable.

IMO there should be a standard discovery mechanism to helps users (and front end) understand the duration/delay of async operations.

---

**joeysantoro** (2023-12-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/amxx/48/1647_2.png) Amxx:

> IMO there should be a standard discovery mechanism to helps users (and front end) understand the duration/delay of async operations.

This is difficult to enforce for off-chain use cases which could have arbitrary delays. Are you suggesting some kind of view function like “expected delay” which is global to the vault or a method which is scoped to specific request IDs?

I’m open to including this if it is either optional or includes a magic value for “unknown delay”

---

**blablalf** (2024-01-11):

Hello!

I post this message on behalf of the Amphor Labs dev team.

[Amphor](https://amphor.io/) is a DeFi app based on an epoch system. Basically, we are buidling ERC4626 vaults with a deposits/withdrawals window open between epochs. At the end of an epoch, the vault opens for deposits/withdrawals and shares price is updated.

Since we would like our users to be able to deposit while the vault is closed, we are interested in asynchronous deposits and redeems.

We started to implement an ERC7540 vault with the following specificities:

- Requests are distinguished by epoch so the requestId is actually an epochId.
- When we go through a new epoch we accept requests all at once. At this moment, we incorporate the underlying in the strategy and we mint the shares.

We met the following problems:

- Batching of request approval doesn’t properly work: There is no Deposit event emitted meanwhile the underlying is incorporated into the strategy. Likewise, waiting for users to call “Deposit” to incorporate the funds/ mint shares seems suboptimal.
- The deposit and redeem functions of the ERC7540 break the flow described into the 4626 one. The ERC4626 deposit function is supposed to take underlying and return shares, but in the ERC7540 the role of this function is to claim a deposit.
There is the same problem with the redeem function. Using the Deposit and redeem functions for the claiming actions is ambiguous.
This leads other ERC4626 functions to be unadapted and therefore breaks the ERC4626 standard.

We emit the following ideas to respectively mitigate these problems:

- We would mint the shares and emit the Deposit event when the request is treated (when the underlying is incorporated into the strategy).
We would therefore create and emit a ClaimDeposit event into the function which would serve to claim the shares after an accepted deposit request.
Likewise, we would use the same system for the redeem part (i.e emit the Withdraw event when the request is treated and so when the underlying is not anymore incorporated into the strategy. We would also create and emit a ClaimWithdraw event into the function which serves to claim the underlying after an accepted redeem request).
- ERC7540 should extend the capacities of the 4626, not modify them. Thus, we would conserve the native synchronous flow using deposit/redeem and add requestDeposit/claimDeposit and requestRedeem/claimRedeem functions for the asynchronicity. The synchronous flow could be disabled using maxDeposit = 0 which would therefore not represent asynchronous requests anymore.
The ERC4626 elements would therefore conserve their initial role.
- Following the last following point, we also emit the idea of a potential additional event emitted when a request is treated.
 In case of deposit request:

```yaml
- name: AsyncDeposit
  type: event

  inputs:
    - name: requestId
      indexed: true
      type: uint256
    - name: requestedAssets
      type: uint256
    - name: acceptedAssets
      type: uint256
```

 In case of redeem request:

```yaml
- name: AsyncRedeem
  type: event

  inputs:
    - name: requestId
      indexed: true
      type: uint256
    - name: requestedShares
      type: uint256
    - name: acceptedShares
      type: uint256
```

 This event would simplify the link between a request and its author (especially if the request is treated into a different transaction of the one where shares are transferred to/from the receiver/owner).

We hope that this feedback will help.

---

**jeroen** (2024-05-28):

Sharing an update here as some changes have been merged into ERC-7540, and hopefully it is close to ready for finalization now. See [ERC-7540: Asynchronous ERC-4626 Tokenized Vaults](https://eips.ethereum.org/EIPS/eip-7540) for the latest version. Summarizing the changes:

- Operator functionality was added, inspired by ERC-6909: Minimal Multi-Token Interface. This enables integrations that manage requests for other users to rely on the accounting system of the asynchronous Vault, while still having full control to submit new requests and claim assets/shares after a request is fulfilled.
- Overloaded deposit/mint methods are now required, that include an additional argument for the request owner. This enables operators to claim on behalf of another user.
- Callbacks were removed. The same goals can be reached by the operator model, with reduced complexity.
- Request owner/receiver parameters in the request and claim methods were all renamed to controller for consistency. The controller parameter in the request* methods becomes the owner of the request and is allowed to claim the request later.
- Typos were fixed across the spec, and the request ID parameter was added to the claimable* and pending* methods, where it was erroneously missing.

---

**kos** (2024-08-15):

Hey, can someone please clarify the statement:

> The interface is fully backward compatible with ERC-4626.

I agree that deposit flow is preserved and backward compatible, i.e. it can be called 4626 deposit:

> deposit(uint256 assets, address receiver)

and supports 7540 deposit flow in the same time as a combination of:

> requestDeposit(uint256 assets, address controller, address owner)

and

> deposit(uint256 assets, address receiver, address controller) / mint(uint256 shares, address receiver, address controller)

Selectors of deposit/mint methods are different [deposit(uint256,address)/mint(uint256,address) → deposit(uint256,address,address)/mint(uint256,address,address)].

Whereas redeem flow breaks 4626 standard, because 4626 redeem/witdhraw functions:

> withdraw(uint256 assets, address receiver, address owner) / redeem(uint256 shares, address receiver, address owner)

and corresponding 7540 ones:

> withdraw(uint256 assets, address receiver, address controller) / redeem(uint256 shares, address receiver, address controller)

have the same selectors [withdraw(uint256,address,address) / redeem(uint256,address,address)] for both 7540 and 4626 standards.

Also I found some inaccuracies throughout the text of standard like:

> MUST emit the RequestDeposit event.

and later:

> Events → DepositRequest

The same typo for “RequestRedeem” event.

Also it is not clearly stated how the hashes are calculated in the section “ERC-165 support”:

> 0xe3bc4e65
> 0xce3bbe50
> 0x620ee8e4

It is unclear in which cases for 0xe3bc4e65 param it should returns true.

Thanks.

---

**jeroen** (2024-08-15):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/k/c5a1d2/48.png) kos:

> I agree that deposit flow is preserved and backward compatible, i.e. it can be called 4626 deposit:

To these points, check the Request Flows section: [ERC-7540: Asynchronous ERC-4626 Tokenized Vaults](https://eips.ethereum.org/EIPS/eip-7540#request-flows) It describes the incompatibilities.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/k/c5a1d2/48.png) kos:

> Also I found some inaccuracies throughout the text of standard like:

Good catch! Those are indeed 2 minor typos. Will check if they can still be fixed despite the standard already being finalized.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/k/c5a1d2/48.png) kos:

> Also it is not clearly stated how the hashes are calculated in the section “ERC-165 support”:

I hope we will soon have 1 or more good reference implementations, that will clarify this. For now, you can look at [liquidity-pools/src/ERC7540Vault.sol at main · centrifuge/liquidity-pools · GitHub](https://github.com/centrifuge/liquidity-pools/blob/main/src/ERC7540Vault.sol#L278) and the corresponding test [liquidity-pools/test/unit/ERC7540Vault.t.sol at main · centrifuge/liquidity-pools · GitHub](https://github.com/centrifuge/liquidity-pools/blob/main/test/unit/ERC7540Vault.t.sol#L89) for an example.

---

**kos** (2024-08-18):

Hi [@jeroen](/u/jeroen), thanks for your reply.

According to implementation you provided I only found a confirmation of the statement that 7540 breaks 4626 via redeem flow.

I mean if I already have 4626 vault contract and the clients performing deposit/redeem operations on it, then extending the contract with 7540 standard will break redeeming of shares so that existing clients must be updated to call requestRedeem() before any redeem/withdraw. However deposit flows will work seamlessly.

I think it would be really good to preserve 4626 backward compatibility having a little other naming for overriden methods:

asyncRedeem()

asyncWithdraw()

and similarly for deposit ones for symmetry however it is not necessary there.

---

**jeroen** (2024-08-18):

The ERC-7540 standard has already been finalized so these changes cannot be made anymore.

---

**kos** (2024-08-18):

Then it would be great to explicitly specify it in the section [ERC-7540: Asynchronous ERC-4626 Tokenized Vaults](https://eips.ethereum.org/EIPS/eip-7540#backwards-compatibility) that redeem flow is not backward compatible .


*(3 more replies not shown)*
