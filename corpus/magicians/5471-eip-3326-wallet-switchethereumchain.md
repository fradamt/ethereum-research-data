---
source: magicians
topic_id: 5471
title: "EIP-3326: wallet_switchEthereumChain"
author: rekmarks
date: "2021-03-04"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-3326-wallet-switchethereumchain/5471
views: 13977
likes: 32
posts_count: 17
---

# EIP-3326: wallet_switchEthereumChain

A [draft PR](https://github.com/ethereum/EIPs/pull/3326) has been created for `wallet_switchEthereumChain`, a sibling method of `wallet_addEthereumChain` ([EIP-3085](https://eips.ethereum.org/EIPS/eip-3085), [discussion](https://ethereum-magicians.org/t/eip-3085-wallet-addethereumchain/5469)) and `wallet_updateEthereumChain` ([EIP-2015](https://eips.ethereum.org/EIPS/eip-2015), [discussion](https://ethereum-magicians.org/t/eip-2015-wallet-update-chain-json-rpc-method-wallet-updatechain/3274)).

This is the official discussion thread for EIP-3326.

## Replies

**rekmarks** (2021-03-04):

cc’ing parties I believe to be interested: [@MicahZoltu](/u/micahzoltu), [@wighawag](/u/wighawag), [@pedrouid](/u/pedrouid)

---

**danfinlay** (2021-03-05):

I think this is a fine proposal, with some definite benefit, but I think it leaves some user experience to be desired.

Part of the reason this EIP is needed is because currently the EIP-3085 `wallet_addEthereumChain` method will throw an error when trying to switch the user to a “default” network on MetaMask, and so there is currently no programmatic way to suggest a user switch to a “default” network.

One proposed approach is this EIP as well as a `hasEthereumChain` method, which combined would mean potentially multiple acts of consent to perform this one action:

- Permission to view available networks
- (if the network is not available) Permission to add & switch to network
- (if the network is available) Permission to switch network

Meanwhile, the dapp didn’t need to view *all* networks to complete its intended goal of suggesting a network if it wasn’t present. It could’ve provided that fallback case in its original request.

I think these many actions can be summarized with a single method instead, like a `switchWithOptionalFallbackToAdd` method. The current proposal could be simply extended with an optional parameter to make this possible.

For example, we could provide an optional parameter `fallbackRpc`, which *if the user lacked the requested network* would fall back to triggering the EIP-3085: `wallet_addEthereumChain` logic.

```json
{
  "id": 1,
  "jsonrpc": "2.0",
  "method": "wallet_switchEthereumChain",
  "params": [
    {
      "chainId": "0x5",
      "fallbackRpc": {
        "chainId": "0x5",
        "chainName": "Goerli",
        "rpcUrl": "https://goerli.infura.io/v3/INSERT_API_KEY_HERE",
        "nativeCurrency": {
          "name": "Goerli ETH",
          "symbol": "gorETH",
          "decimals": 18
        },
        "blockExplorerUrl": "https://goerli.etherscan.io"
      }
    }
  ]
}
```

---

**rekmarks** (2021-03-05):

If we want to enable `switchEthereumChain` to fall back to `addEthereumChain`, IMO we should just specify the same parameter object for the former as the latter, and let implementers choose whether to fall back to `addEthereumChain`. I don’t think we need a separate method. Doing it this way should work nicely.

*Edit:* This would mostly obviate the need for `hasEthereumChain` as well, which is problematic anyway from a user privacy perspective. I’d be curious to hear what [@wighawag](/u/wighawag) has to say about that.

---

**MicahZoltu** (2021-03-05):

Why does the dapp need to tell the provider to switch chains?

I feel like we should instead just have the dapp submit the `chainId` along with any request.  For layer 2 and cross-chain applications, the dapps may be sending requests to multiple chains at the same time and switching chains between each request is likely to introduce bugs in the dapp as it would be quite easy to have two parts of your code both switching chains at the same time and then racing to get requests on the wire.

---

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/danfinlay/48/4187_2.png) danfinlay:

> currently the EIP-3085 wallet_addEthereumChain method will throw an error when trying to switch the user to a “default” network on MetaMask, and so there is currently no programmatic way to suggest a user switch to a “default” network

Why does MetaMask fail in this case instead of just returning success?  The dapp wants to ensure that the provider is able to talk to chain ID 1, which is why they call `wallet_addEthereumChain`.  If the provider can *already* talk to chain ID 1, then you can just return success to that call.

---

**rekmarks** (2021-03-05):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> I feel like we should instead just have the dapp submit the chainId along with any request.

Parameterizing the chain ID is absolutely the destination, but for our own case, we aren’t ready to ship such a provider API just yet. We see it as a potential opportunity to get rid of the injected provider model entirely, so it’s a much bigger and distinct discussion.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> Why does MetaMask fail in this case instead of just returning success? The dapp wants to ensure that the provider is able to talk to chain ID 1, which is why they call wallet_addEthereumChain. If the provider can already talk to chain ID 1, then you can just return success to that call.

Technically speaking, we could do it that way and just avoid this method entirely. We were somewhat concerned about habituating developers to rely on `addEthereumChain` to switch the active chain while chain switching is a concept, but maybe that’s ultimately fine.

In a multi-chain provider world, there chain ID will always have to be parameterized, and there will be no network switching anyway. ![:thinking:](https://ethereum-magicians.org/images/emoji/twitter/thinking.png?v=12)

---

**MicahZoltu** (2021-03-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rekmarks/48/1626_2.png) rekmarks:

> Parameterizing the chain ID is absolutely the destination, but for our own case, we aren’t ready to ship such a provider API just yet. We see it as a potential opportunity to get rid of the injected provider model entirely, so it’s a much bigger and distinct discussion.

What sort of time frame are you imagining for doing it the “right” way?  I’m not a fan of creating standards we know are bad and we don’t plan on keeping around.  A lot of engineering work across the ecosystem will go into supporting this stuff and it sucks to throw that all away shortly after if we can avoid it.  I would *rather* provider and dapp developers instead focus on building things correctly in the first place.

---

**maze** (2021-03-07):

I think there was EIP-2015 but nothing happened: https://github.com/ethereum/EIPs/pull/2015

There will be more and more multichain dapps so this feature becomes more important very quickly

---

**rekmarks** (2021-03-07):

[EIP-2015](https://eips.ethereum.org/EIPS/eip-2015) is not abandoned, it’s just in draft.

It’s supposed to be like [EIP-3085](https://eips.ethereum.org/EIPS/eip-3085) (`wallet_addEthereumChain`) but with update semantics.

---

**maze** (2021-03-08):

I see, thanks. Too bad this is still in draft after being created in May 2019. In my opinion this would be pretty big for multichain dapps ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=9)

---

**rekmarks** (2021-03-10):

You’re not wrong! Everyone involved is just working on a million different things. There’s always room for people willing to chop wood and carry water ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=9)

---

**pedrouid** (2021-03-11):

Personally I always viewed wallet_updateEthereumChain to have multiple behaviors which would remove the need for all these methods to exist in parallel.

Instead of having verbs for has, add, switch and update it would always be the same one.

There is very negligible set of use-cases where a dapps wants to add and/or update a chain without switching.

In fact I would replace all these methods with wallet_changeEthereumChain and it would have the following behavior:

1. if chainId does not exist -> wallet adds new one and switches to it
2. if chainId exists:
2.1. parameters match existing -> switches network
2.2. parameters do not match existing but can be changed -> updates network and switches to it
2.3. parameters do not match existing but cannot be changed -> throws error as a default chain

---

**KBKUN024** (2021-08-18):

Hi! I left a comment in #2944 in github,could you please tell me how to fix that? I’m so confused now,please help ![:joy:](https://ethereum-magicians.org/images/emoji/twitter/joy.png?v=9)

---

**KBKUN024** (2021-08-18):

link is here:[switch_Ethereum chain do](https://github.com/MetaMask/metamask-mobile/issues/2944)

---

**sbacha** (2022-02-07):

EIP4337 is an excellent example of a use case where a dapp would want to add/update a chain without switching

---

**php4fan** (2022-06-18):

This specification is ambiguous about what happens if you **switch to the network that is already the current one**.

I would expect it to immediately return success, and I hope it’s what it does (anything else would be stupid), but the specification doesn’t explicitly say it. Actually, it implicitly says something that could be interpreted to the contrary:

> null is returned if the active chain was switched, and an error otherwise.

This, again, is ambiguous, because if the current network is 123 and you ask to switch to 123, one may say that the chain was *not* switched, and therefore this would be saying that an error would be thrown in this case; or one may say that the active chain was switched from 123 to 123, and therefore null is returned.

---

**Squeebo** (2022-07-21):

EIP-3085 indicates:

> The method MUST return null if the request was successful, and an error otherwise.
> A request to add a chain that was already added SHOULD be considered successful.

I think this applies to EIP-3326 as well;   If the dapp requests to switch chain, and it already matches the selected chain, the expected result is to return null due to success.

