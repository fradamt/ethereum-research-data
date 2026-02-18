---
source: magicians
topic_id: 3274
title: "EIP-2015: Wallet Update Chain JSON-RPC Method (`wallet_updateChain`)"
author: pedrouid
date: "2019-05-14"
category: EIPs
tags: [wallet, json-rpc]
url: https://ethereum-magicians.org/t/eip-2015-wallet-update-chain-json-rpc-method-wallet-updatechain/3274
views: 5434
likes: 25
posts_count: 19
---

# EIP-2015: Wallet Update Chain JSON-RPC Method (`wallet_updateChain`)

Following up on this discussions of the `wallet_` namespaced methods, I’ve published a draft for the `wallet_updateChain` method first proposed [here](https://ethereum-magicians.org/t/add-wallet-methods-to-improve-dapp-to-wallet-interaction/1848/31).

The EIP-2015 describes how to format a request to switch chains and the best practices to handle it and display it to the user.

https://github.com/ethereum/EIPs/pull/2015

## Replies

**pedrouid** (2019-05-14):

The EIP is looking good so far and I’m happy with the specification to be implemented.

I would only suggest that we keep JSON-RPC requests consistent and only use hexadecimal encoded values on the parameters.

Just as `eth_chainId` returns the `chainId` value hex encoded, we should also pass this parameter and `networkId` on `wallet_updateChain` value hex encoded.

However as [@danfinlay](/u/danfinlay) pointed out [here](https://github.com/ethereum/EIPs/pull/2015#issuecomment-491943421), the EIP-747 uses decimal values but I since this EIP is also on Draft, I personally would like to suggest to change it also to have only hexdecimal values.

---

**ligi** (2019-05-14):

thanks for the initiative! +1 for hex encoding and the change to 747

2 thoughts on this EIP:

should nativeCurrency get a (optional) decimals? There might be chains that don’t default to 18 here

should we make rpcURL to an array so we can pass multiple (redundancy) - we also have an array for it in https://github.com/ethereum-lists/chains

It can still just use one or even an empty array - just makes it more flexible

---

**pedrouid** (2019-05-14):

Good point! Let’s add the decimals for the nativeCurrency and default it to 18.

I’m also happy with turning the rpcUrl field into an array. It will most likely include one url but makes it more flexible

---

**wighawag** (2019-05-20):

Thanks for the proposal. That will be very valuable for applications that require to act on multiple chain.

Regarding, `rpcUrl`, this parameter should be optional as purely decentralised app will have nothing to provide for it.

---

**ligi** (2019-05-20):

yea - perhaps we should completely drop rpcUrl to not encourage going down this centralized path any further …

---

**pedrouid** (2019-05-21):

In this scenario it does not necessarily mean that we are taking a centralized path here.

We are communicating to the wallet to switch to a different chain. This chain could be know or unknown to the Wallet. As I described on the EIP as part of the best practices, the Wallet should resort to a known node if it has the same chainId, otherwise it should use the provided rpcUrl.

Thus we are using the rpcUrl as fallback so it should be a requirement to provide this fallback endpoint in case the Wallet doesn’t have any known nodes to connect to.

---

**ligi** (2019-05-21):

I think it leads us a bit more in direction centralization and I cant wait for the day the whole RPC-mess is gone …

But it might be a bit of an bold move to remove it from here. So let’s keep it - it is optional anyway if we have it as an array as the array could be empty.

---

**pedrouid** (2019-05-21):

Alright, let’s make it into an array and optional

---

**ligi** (2019-05-21):

with an array it is already optional - the array can have a size of 0 - I think that’s cleaner - less cases to check

---

**ligi** (2019-05-22):

thinking about this more made me realize a “name” parameter can be really helpful so the wallet can display what chain the user is on in a more human way.

---

**pedrouid** (2019-05-22):

Agreed, however I would make make it optional since this is metadata. Which also makes me realize that nativeCurrency should also be optional since it’s also metadata.

Hence the interface would be as follows:

```auto
interface NativeCurrency {
    name: string;
    symbol: string;
    decimals: number;
}

interface Eip2015Params {
    chainId: number;
    networkId: number;
    rpc: string[];
    name?: string;
    nativeCurrency?: NativeCurrency;
}

interface Eip2015Request {
    id: number;
    jsonrpc: '2.0';
    method: 'wallet_updateChain';
    params: [ Eip2015Params ];
}
```

PS - we still haven’t decided formally if the `chainId` and `networkId` should be decimal numbers or hexdecimal strings

---

**wighawag** (2019-05-23):

I think name and native currency are dangerous parameter as an app could trick the user into thinking it is sending 1 token while it is actually sending 1000. or it is sending a token name X while it is actually some more valuable tokens (from another chain)

Similarly the name of the network could trick the user it is operating on a testnet while it operate on a valuable chain

I think the wallet should either support a network or refuse to switch. Letting the app choose is risking user’s fund.

In that case, rpcUrl would not be useful neither,

This would leave only chainId and networkId

And an error would be returned if the wallet do not support it.

I understand though the appeal for developers to let existing wallet support new chains as this remove the need to wait for support (which can take forever).

Maybe we could require wallet to display a warning for unknown chains with the parameters being proposed by the application.

---

**pedrouid** (2019-05-27):

There is a lot of measures that the Wallet can use to protect the user from attacks, I’ve described a few in the EIP itself.

Most importantly the Wallet can query `eth_chainId` and `net_version`, through the rpc url, verify the respective provided values. Secondly, the Wallet could query the chainId.network for the name and nativeCurrency fields and use those instead if present.

I understand the attack vectors that you are describing and they are valid points. But this is an ERC, it’s a coordination mechanism between projects to expand the scope of what’s possible today yet still completepy optional for projects to adopt. In this case this is a `wallet` namepsaced method and the goal is to interoperate between Dapps and Wallets and it would better to have a standard for it that we all follow instead of using ad-hoc solutions.

---

**wighawag** (2019-05-27):

Hi [@pedrouid](/u/pedrouid) I am not against the proposal by itself. I think this is a great addition and I am myself building an application that would benefit from it. I am just against the idea of letting the applications provide parameters that could trick users.

> the Wallet can query ‘eth_chainId’ and ‘net_version’, through the rpc url, verify the respective provided values.

My concern was about the network name, not the chainId. The chainId will restrict what tx is possible thanks to chainId replay protection. But if a name like “rinkeby testnet” is presented, the user might not read that the chainId used is actually 1 (mainnet). If the wallet can verify the name is valid, it could have provided it in the first place, without the need for the application to provide it. Hence why I think the name should not be provided by the application and the same apply for nativeCurrency

> But this is an ERC, it’s a coordination mechanism between projects to expand the scope of what’s possible today yet still completepy optional for projects to adopt.

The fact that it is an ERC does not change the fact that as it stands, the proposal open up security issues.

> the Wallet could query the chainId.network for the name and nativeCurrency fields and use those instead if present.

chainid.network could be compromised. We surely do not want the security of the user’s wallet to depend on it.

But if your wallet really want to do that, then we do not need the parameters (nativeCurrency, name) to be provided by the application then. The chainID would be sufficient for the wallet to fetch the rest via that mechanism.

rpcUrl would still be needed though for wallets that want to support unknown network.

So if we want to let application provide their own rpc URL and the chainID is unknown to the wallet itself, I would prescribe in the proposal that such wallet need to show a warning that the user is connecting to an unknown network and they should verify the chainID.

---

**pedrouid** (2019-05-27):

Agreed, I think it would be reasonable to only provide the `chainId` and `networkId` and have the Wallet take care of the rest using their own resources, such as their own chainId registry or a public one, like the `chainId.network`.

```auto
interface Eip2015Request {
    id: number;
    jsonrpc: '2.0';
    method: 'wallet_updateChain';
    params: [{
        chainId: number,
        networkId: number
    }];
}
```

I would love to hear your feedback on this proposed change. cc [@ligi](/u/ligi) [@danfinlay](/u/danfinlay)

---

**rekmarks** (2020-10-30):

Haha, this is awesome. We’ve talked about this internally at MetaMask for some time, and over the course of the last year have re-treaded this discussion without realizing it. For example, we talked about using [chainId.network](https://chainId.network) to mitigate (or outright prevent) the kinds of attacks described by [@wighawag](/u/wighawag) just the other day!

I have more thoughts about the specification that I’ll summarize in the next few days. This is happening though!

---

**SamWilsn** (2023-05-15):

[@Pandapip1](/u/pandapip1) I’d suggest rewording:

> The wallet_updateEthereumChain method returns true if the chain was successfully added or switched to, and an error with code 4001 if the user rejected the request.

to:

> The wallet_updateEthereumChain method returns true if the active chain matches the requested chain, regardless of whether the chain was already active or was added to the wallet previously. If the user rejects the request, it must return an error with code 4001.

I find it less ambiguous. Since it changes the meaning of the paragraph, I’m making the suggestion here instead of on your PR.

---

I’m also quite sad to see the examples removed.

---

**Pandapip1** (2023-06-11):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> I’m also quite sad to see the examples removed.

Don’t worry, they will be re-added before I move it to last call!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> The wallet_updateEthereumChain method returns true if the active chain matches the requested chain, regardless of whether the chain was already active or was added to the wallet previously. If the user rejects the request, it must return an error with code 4001.

That wording does seem better.

