---
source: magicians
topic_id: 19530
title: "ERC-7677: Paymaster Web Service Capability"
author: lsr
date: "2024-04-04"
category: ERCs
tags: [erc, account-abstraction]
url: https://ethereum-magicians.org/t/erc-7677-paymaster-web-service-capability/19530
views: 3362
likes: 5
posts_count: 13
---

# ERC-7677: Paymaster Web Service Capability

Thread to discuss [ERC-7677](https://github.com/ethereum/ERCs/pull/360/files).

## Replies

**hazim-j** (2024-04-10):

Great work on the ERC. At Stackup we’ve been huge advocates for standardisng the Paymaster API. We’ve also thought about what a standardised paymaster API could look like and derived something similar on a high level. Here are some additional thoughts that might also be worth considering.

## Removing chainId in method parameters

Have we considered alternatively including a method like `pm_chainId` or even `eth_chainId` rather than specifying it in the method parameters?

Requiring a `chainId` input assumes that the service is multi chain at the method level which breaks consistency with other infrastructure components (e.g. bundlers and nodes). Having `eth_chainId` may also be ideal since it allows compatibility for a paymaster RPC URL to be used with tools like viem and ethers that will typically call `eth_chainId` to detect network.

Applications can use different API keys provided by the Paymaster service to route to the relevant network which is the current standard pattern for bundler and node providers.

## Challenges with preVerificationGas (pvg)

Generally speaking, I think creating two seperate methods for stub and final `paymasterAndData` (`pnd`) makes sense. Although worth calling out some challenges with this approach.

It can be pretty easy for an incorrectly implemented stub to result in an inufficient `pvg` error due to differences between stub and final `pnd`. Keeping the length equal in both cases is easy enough. But if for instance, the stub has more zero bytes (`0x00`) than the final, this will cause upstream problems like an insufficient `pvg` error.

This was one reason why the current version of Stackup’s `pm_sponsorUserOperation` also returns gas estimates. Additionally, we also had concerns on wether this flow of making an intermediate dummy `pnd` value public would be considered a bad API design due to leaky abstraction.

## Defined types on the context

Leaving the `context` open allows for the most amount of flexibility, but have we also considered what a standard context interface could look like based on common paymaster usecases? This might be worth exploring even if they are optional or defined for the simpler use cases since we could reduce even more ambiguity for developers who want to integrate multiple providers.

## Adding pm_getAddresses

This should be added to easily link a paymaster service to its canonical onchain contract. The application would need to know this if it is required to encode `callData` that requires the paymaster’s contract address (e.g. ERC-20 approvals).

This would also allow the paymasters to cleanly rotate their contracts without breaking downstream applications who would otherwise need to hardcode addresses.

## Adding pm_quotes

This is useful if a paymaster deals with multiple currencies. For instance, if multiple paymasters are accepting payment in an alternative ERC-20 token, it’s useful for a paymaster to provide quotes for the application to compare against before deciding which service to go with.

Even if the Paymaster service is accepting compensation in non-crypto assets that are settled off-chain (e.g. USD, EURO, etc) it could be valuable to also return these exchange rates too.

---

**bumblefudge** (2024-04-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/hazim-j/48/10766_2.png) hazim-j:

> Although worth calling out some challenges with this approach.

Should the ## Rationale section be more detailed or explicit here? I’m generally in support of verbose rationales and non-normative implementer guidelines, tag me if you open a PR on those.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/hazim-j/48/10766_2.png) hazim-j:

> Leaving the context open allows for the most amount of flexibility, but have we also considered what a standard context interface could look like based on common paymaster usecases?

Is this a question for the spec or for reference implementations linked to from the spec? I can imagine reference implementations modeling good behavior by describing the shape and semantics of its `Context` property in their readme files for quick reference? Not sure if the spec should tell anyone they *SHOULD* do that, though?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/hazim-j/48/10766_2.png) hazim-j:

> Requiring a chainId input assumes that the service is multi chain at the method level which breaks consistency with other infrastructure components (e.g. bundlers and nodes)

One man’s breakage is another man’s upgrade path ![:smirk:](https://ethereum-magicians.org/images/emoji/twitter/smirk.png?v=12)

All joking aside, I think the co-authors of this proposal have discussed the breakage and are OK with it.  Would more ## Rationale help here as well?

---

**hazim-j** (2024-04-11):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/bumblefudge/48/7449_2.png) bumblefudge:

> Is this a question for the spec or for reference implementations linked to from the spec? I can imagine reference implementations modeling good behavior by describing the shape and semantics of its Context property in their readme files for quick reference? Not sure if the spec should tell anyone they SHOULD do that, though?

I think defining a few `context` types in a reference implementation could be a good start. Especially for common use cases like “sponsor” (PM sponsors the gas and any compensation is handled offchain between application and provider) or “erc20”.

Otherwise I could potentially see how this becomes the main friction point for an application to onboard multiple providers when all of them have slightly different context requirements for essentially the same use case.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/bumblefudge/48/7449_2.png) bumblefudge:

> One man’s breakage is another man’s upgrade path
>
>
> All joking aside, I think the co-authors of this proposal have discussed the breakage and are OK with it. Would more ## Rationale help here as well?

Definitely agree this should be added to the rationale. If this is intended to be an upgrade path, I would also like to know what the end goal is? To also play devil’s advocate, does it make sense to include it in this ERC rather than maintaining the status quo and pushing for that in different proposal?

---

**lsr** (2024-04-11):

> Removing chainId in method parameters

I think we agree that we need to specify some constraint that allows for wallets to communicate with the paymaster service about intended chain id. As I see it we have 2 options:

1. Require a chain id as part of paymaster service requests (as is specified in the current ERC draft)
2. Require that paymaster service URLs are for a single chain (the current loose standard)

In my opinion, option (1) is the correct place for this abstraction. Option (2) seems like an odd constraint to put on service providers. What if someone wants to architect their services such that a single URL can be multichain? Option (1) allows for that with pretty much no downside to providers who use a single URL per chain, they would just need to accept an additional parameter that they can ignore. When an app developer who uses a URL-per-chain provider wants to submit a request to a different chain, they can just swap out the URL accordingly.

Given this, I don’t think I understand the need for the `pm_chainId` method (or maybe that is a separate point).

> Defined types on the context

Your point on developers integrating multiple providers is interesting, and one I hadn’t considered. My gut feeling is that providers will want to offer too many different additional services-with equally many different abstractions-for this to be feasible. But maybe I haven’t explored here enough, will do some more asking around.

> Adding pm_getAddresses

I admittedly am not as familiar with ERC-20 paymaster flows, but this sounds useful. Is the ERC-20 flow you’re describing the main use case here? Or can you think of other use cases where a wallet would need this information? In any case I’ll read more on the ERC-20 flow and report back with more of an opinion.

> Adding pm_quotes

This seems like a pretty advanced use case and my gut feeling is that this shouldn’t be part of this initial proposal for paymaster service standardization. But again let me read up some more on the ERC-20 flow and maybe will feel differently.

---

**hazim-j** (2024-04-12):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/l/58956e/48.png) lsr:

> This [pm_quotes] seems like a pretty advanced use case and my gut feeling is that this shouldn’t be part of this initial proposal for paymaster service standardization. But again let me read up some more on the ERC-20 flow and maybe will feel differently.

I agree it does increase the complexity of the spec. But given a few assumptions I think a case for it could be made. Put aside the ERC-20 use case for a moment and consider a simpler example of a paymaster sponsoring gas for an application and any compensation is settled off-chain in USD.

Assumptions being:

- Applications will want to integrate multiple paymasters for redundancy.
- Applications will want to be able to make comparisons between providers to lock in optimal gas prices.
- Paymaster’s are likely adding a fee for providing their service which can come in the form of a percentage added to the exchange rate of ETH to USD.

Given those conditions, something like `pm_quotes` allows for a flow where an application can programmatically decide on the best provider based on who is offering the most competitive exchange rate. At Stackup we’ve also worked with wallet teams that are in production who have these exact requirements.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/l/58956e/48.png) lsr:

> My gut feeling is that providers will want to offer too many different additional services-with equally many different abstractions-for this to be feasible. But maybe I haven’t explored here enough, will do some more asking around.

That’s a fair point too and would agree that it may just be too early to converge on a few well defined context types right now. This is probably something worth initially exploring within a reference implementation as [@bumblefudge](/u/bumblefudge) mentioned above.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/l/58956e/48.png) lsr:

> I admittedly am not as familiar with ERC-20 paymaster flows, but this sounds useful. Is the ERC-20 flow you’re describing the main use case here? Or can you think of other use cases where a wallet would need this information? In any case I’ll read more on the ERC-20 flow and report back with more of an opinion.

Yes, in practice the ERC-20 example has been the main use case. Although another use case I can think of is for any indexer that needs to link a paymaster address from a `UserOperationEvent` back to a known provider.

---

**lsr** (2024-04-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/hazim-j/48/10766_2.png) hazim-j:

> Given those conditions, something like pm_quotes allows for a flow where an application can programmatically decide on the best provider based on who is offering the most competitive exchange rate. At Stackup we’ve also worked with wallet teams that are in production who have these exact requirements.

The more I think about this the more I feel that it should not be included as part of this ERC. I understand the use case and could definitely see it as its own proposal. The goal here is to define the standard necessary for app developers to sponsor their users’ transactions, so ultimately `pm_quotes` seems out of scope.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/hazim-j/48/10766_2.png) hazim-j:

> Yes, in practice the ERC-20 example has been the main use case. Although another use case I can think of is for any indexer that needs to link a paymaster address from a UserOperationEvent back to a known provider.

`pm_getAddresses` seems pretty necessary, we can add this.

---

**DavidKim** (2024-04-21):

Great work on the ERC.

Good to see that paymaster API standardization. It was also a topic we at TrustWallet strongly suggested and discussed with Dror and Tom at Denver as well.

Here are some of the thoughts that might be worth being considered:

1. The initial architecture(image below) without the Backend of the app validating the UserOp is very dangerous. It will make the fund drain quickly - I think it will be insecure for real world case.

- To have the above model, I think it would be better for the standard to clearly suggest that validation should happen at the Paymaster Serivce level.

[![2024-04-21 23.47.25](https://ethereum-magicians.org/uploads/default/optimized/2X/5/5b16265babfb511e22fdbd31d5f0108afdb2ae05_2_690x462.jpeg)2024-04-21 23.47.251280×858 53.4 KB](https://ethereum-magicians.org/uploads/default/5b16265babfb511e22fdbd31d5f0108afdb2ae05)

1. Using a separate gas estimation call without using the paymaster’s estimation. I think the reality atm is that wallets rely on Bundlers/Paymasters for gas estimation of UserOperation. I think there is a room more more consideration whether relying on Wallets for gas estimation actually enhances the efficiency/accuracy.

It has the drawback of making multiple more API calls and interaction just for this.

- there might be risks for Paymasters if they approve for UserOp that doesn’t know how much gas it will consume.

- This will be simplified if the Paymaster just return the gas estimation

But I still understand the point that it potentially provides more options from Wallet perspective, but the trade-offs should be considered - both from Efficiency, Security, Accuracy perspective.

1. I understand this standard enforces EIP 5792 for communication, but I think this doesn’t have to be fully bound to that. It can be done much simpler(e.g., injecting js object for wallets to detect, etc)

---

**livingrockrises** (2024-05-15):

Is the ERC ready for standardisation around ERC-20 flows?

would like to contribute on pm_quotes

Biconomy team has nicely made specs for pm_getFeeQuotes couple of months ago. We yearned for a standard but weren’t aware about these efforts.

---

**derek** (2024-05-17):

[@livingrockrises](/u/livingrockrises) with the ERC20 flow, there’s no interaction needed between the DApp and the wallet right?  The wallet would simply let the user pay gas in ERC20s.

Unless you are referring to paying gas with a DApp token?  So like the DApp would let the wallet know that it can provide a ERC20 paymaster for its own DApp tokens?

---

**lsr** (2024-05-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/livingrockrises/48/9264_2.png) livingrockrises:

> Is the ERC ready for standardisation around ERC-20 flows?

Yeah I think we can try to add ERC-20 flows into this ERC.

For the ERC-20 flow I think we would need `pm_quotes` as described by [@hazim-j](/u/hazim-j) above and `pm_getAddresses`, which returns paymaster addresses with a `type` (`verifying` or `erc20`).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/livingrockrises/48/9264_2.png) livingrockrises:

> Biconomy team has nicely made specs for pm_getFeeQuotes couple of months ago. We yearned for a standard but weren’t aware about these efforts.

Would you be able to share what you currently have for `pm_getFeeQuotes` here? Would be great to have you contribute.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/derek/48/12233_2.png) derek:

> @livingrockrises with the ERC20 flow, there’s no interaction needed between the DApp and the wallet right? The wallet would simply let the user pay gas in ERC20s.

[@derek](/u/derek) yeah generally wallets can provide their own ERC-20 paymasters. But dapps could pass in a `paymasterService` URL that responds to `pm_getAddresses` with their own ERC-20 paymasters.

So in your example, my dapp could pass in a paymaster service URL that has a paymaster address that supports my dapp’s token. So then the user could pay with my dapp’s token even though the wallet-defined ERC-20 paymaster might not support it.

I’m realizing now we would also need some way to know which tokens an ERC-20 paymaster supports. I think we could do this by having `erc20` type addresses returned by `pm_getAddresses` also list out supported chains / token addresses. So something like

```json
// pm_getAddresses response
"result": {
  "0x2105": { // chain id
    "0x5FF12344b0FDCD4123430c7CF57E578a026d2789": { // paymaster address
      "type": "erc20",
      "supportedTokens": [ // token addresses
        "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "0x6B175474E89094C44Da98b954EedeAC495271d0F"
      ]
    },
    "0x57361344b0FDCD4123430c7CF57E578a026d2789": {
      "type": "verifying"
    }
  },
  ...
}
```

Wallets could alternatively infer supported tokens by the `pm_quotes` response but I think having it returned explicitly like above would be better.

There’s also the issue of getting the actual `paymasterAndData` field, as in practice it seems it’s not just the ERC-20 address.

One potential solution that comes to mind: we could use the `pm_getPaymasterStubData` / `pm_getPaymasterData` `context` parameter. The main problem is that the `context` param usually comes from the app, but we wouldn’t know that a user is using an ERC-20 paymaster until we enter the wallet context. So the proposal would be for the wallet to add something to the `context` param before calling `pm_getPaymasterStubData` / `pm_getPaymasterData` like below:

```typescript
pm_getPaymasterData([
  userOp,
  entrypoint,
  chainId,
  {...appContext, type: 'erc20', token: '0x...'} // type and token added by wallet
])
```

Lmk what you all think on the proposed additions or if you have other ideas in mind.

---

**lsr** (2024-05-18):

Hey, thanks for your reply!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/davidkim/48/13667_2.png) DavidKim:

> The initial architecture(image below) without the Backend of the app validating the UserOp is very dangerous. It will make the fund drain quickly - I think it will be insecure for real world case.
>
>
> To have the above model, I think it would be better for the standard to clearly suggest that validation should happen at the Paymaster Serivce level.

Yeah we allude to this in the security considerations section but can make it more explicit. Will add something more clear to the spec.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/davidkim/48/13667_2.png) DavidKim:

> Using a separate gas estimation call without using the paymaster’s estimation. I think the reality atm is that wallets rely on Bundlers/Paymasters for gas estimation of UserOperation. I think there is a room more more consideration whether relying on Wallets for gas estimation actually enhances the efficiency/accuracy.
>
>
> It has the drawback of making multiple more API calls and interaction just for this.
>
>
>
>
> there might be risks for Paymasters if they approve for UserOp that doesn’t know how much gas it will consume.
>
>
>
>
> This will be simplified if the Paymaster just return the gas estimation
>
>
>
>
> But I still understand the point that it potentially provides more options from Wallet perspective, but the trade-offs should be considered - both from Efficiency, Security, Accuracy perspective.

In practice we found that paymaster services were just not reliable enough to provide gas estimations. The wallet ultimately knows which bundler will be used to submit user ops, so gas estimates should come from that bundler to provide the most accurate gas estimates. This is not just a design opinion either, the paymaster services providing insufficient gas estimates completely blocks successfully submitting user ops. Therefore I believe the flow in the spec is a must. Happy to discuss if you have something else in mind though.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/davidkim/48/13667_2.png) DavidKim:

> I understand this standard enforces EIP 5792 for communication, but I think this doesn’t have to be fully bound to that. It can be done much simpler(e.g., injecting js object for wallets to detect, etc)

I wouldn’t say this *enforces* EIP-5792 for communication. Anyone is free to suggest other proposals for initiating this flow ![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=12). I can imagine other use cases for the paymaster RPC methods, and I’m sure there could be other ways to go about this from the wallet’s perspective. This proposal is just focused on the EIP-5792 approach.

---

**DavidKim** (2024-06-11):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/l/58956e/48.png) lsr:

> In practice we found that paymaster services were just not reliable enough to provide gas estimations. The wallet ultimately knows which bundler will be used to submit user ops, so gas estimates should come from that bundler to provide the most accurate gas estimates. This is not just a design opinion either, the paymaster services providing insufficient gas estimates completely blocks successfully submitting user ops. Therefore I believe the flow in the spec is a must. Happy to discuss if you have something else in mind though.

In my opinion, it might be worth noting the fact that Paymaster vendors return the gas estimation to limit a UserOperation from spending arbitrary amount of funds for gas.

It could create an attack vector for Paymasters if we allow this flow at an ERC level.

In practice, StackUp and Biconomy share that Paymaster Service API provides more accurate gas estimation because they have full context on the logic of the Paymaster compared to their Bundler Endpoint IF the UserOp is using their Paymaster.

I suggest to separate gas estimation call to the Bundler as optional for this ERC.

This could help free up design choices depending on the preference of the Wallet vendor.

(Also, most Paymaster API Service providers also Provide Bundler services, so I don’t think Paymaster Service actually lacks far behind when it comes to its performance to perform gas estimation)

If we make this optional, we can embrace the Wallet Vendor’s autonomy e.g., for cases when the Wallet relies more on Bundler or wants to set custom gas limits for specific actions, etc.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/l/58956e/48.png) lsr:

> I wouldn’t say this enforces EIP-5792 for communication. Anyone is free to suggest other proposals for initiating this flow . I can imagine other use cases for the paymaster RPC methods, and I’m sure there could be other ways to go about this from the wallet’s perspective. This proposal is just focused on the EIP-5792 approach.

Great to know it’s not enforced! I think it might be worth noting in the ERC that EIP-5792 is recommended but not a must and is optional.

