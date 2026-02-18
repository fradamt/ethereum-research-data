---
source: magicians
topic_id: 640
title: "EIP-1193: Ethereum Provider JavaScript API"
author: ryanio
date: "2018-07-02"
category: Working Groups > Provider Ring
tags: [eip-1193]
url: https://ethereum-magicians.org/t/eip-1193-ethereum-provider-javascript-api/640
views: 14487
likes: 41
posts_count: 62
---

# EIP-1193: Ethereum Provider JavaScript API

Hey everyone,

After synthesizing the discussions in ethereum/interfaces#16 and EIP 1102, we’ve come up with a proposal to standardize an Ethereum Provider API.

[Here is a link to the EIP.](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1193.md)

We would like to encourage discussion here with feedback and comments or suggestions for improvement.

We will be working on an initial implementation in Mist this week.

Cheers!

## Replies

**ryanio** (2018-07-02):

The opening post had a max limit of links, so here are the links to the relevant discussions:

[ethereum/interfaces#16](https://github.com/ethereum/interfaces/issues/16)

[EIP 1102](https://github.com/ethereum/EIPs/pull/1102)

---

**MicahZoltu** (2018-07-02):

All evergreen browsers support async/await and Promises now and there are polyfills for promises when not available.  I recommend having `ethereum.send` return a promise and not take a third parameter, rather than continuing to follow the legacy JS paradigm of callbacks.

---

The API needs to be specified in a lot more detail.  As currently specified there is not enough information available.  Personally, I would recommend including TypeScript definitions for everything and be ultra-specific.  For example, does `params` array support numbers or only 0x prefixed hex encoded numbers?

Is the provider API expected to match the JSON-RPC API exactly or is it limited in what is supported?

Does the ethereum provider support the pub-sub methods (stuff that normally only works over a persistent connection like a websocket)?

---

**MicahZoltu** (2018-07-02):

I recommend constraining the `error` in the `ethereum.send` callback to be of type `Error` (and strictly specifying this).  Writing client code to interface with this will be much simpler if the client has a strong guarantee of the types it can receive.

On a similar vein, is the `result` just whatever the JSON-RPC sent back?

---

**MicahZoltu** (2018-07-02):

`ethereum.on('network_changed', ...)` and `ethereum.on('account_changed', ...)` would remove the top two causes for frequent polling of the provider.

---

**ryanio** (2018-07-03):

> All evergreen browsers support async/await and Promises now and there are polyfills for promises when not available. I recommend having ethereum.send return a promise and not take a third parameter, rather than continuing to follow the legacy JS paradigm of callbacks.

Sounds good to me.

> Personally, I would recommend including TypeScript definitions for everything and be ultra-specific. For example, does params array support numbers or only 0x prefixed hex encoded numbers?

Sure we can look into providing TypeScript definitions with the EIP.

Open to discussion about supporting numbers, I think it would be fine.

> I recommend constraining the error in the ethereum.send callback to be of type Error (and strictly specifying this).

Sure.

> On a similar vein, is the result just whatever the JSON-RPC sent back?

I think it would be smart to.

> ethereum.on(‘network_changed’, …) and ethereum.on(‘account_changed’, …) would remove the top two causes for frequent polling of the provider.

Open to adding these events, they seem important from the perspective of an app. Could we resend the ‘connect’ event if the network changes or new accounts are connected?

---

**MicahZoltu** (2018-07-03):

If you want to re-use connect, it seems like sending `end` then `connect` would be more correct?

The problem with re-using the `connect` event is that dapps can’t constrain how much state they destroy based on context.  For example, when the account changes I may retain internal dapp state of logs I have fetched (like trading history), but I may delete state related to the specific account (like balance), but when the network changes I may blow away all state.

For network change, I can’t think of any state I would want to retain but there may be value in having a special event for it so the dapp can appropriately message the user about what happened, whereas an end-connect pair is a bit ambiguous as to what happened (maybe the user disabled the browser plugin, or the browser restarted, or they changed networks, or they got logged out and back in).

---

**MicahZoltu** (2018-07-03):

Re: numbers

Whether the API supports numbers or not IMO depends on whether the API is just trying to wrap the existing JSON-RPC API or if it plans on providing an entire *NON LEAKY* new API on top of it.  Just using JSON-RPC is *way* simpler in terms of engineering required and the spec.  Creating a new API that doesn’t suck would be a significantly better dapp developer experience, though it would mean that dapps need to implement JSON-RPC separately.

I dislike the JSON-RPC API personally, so I’m not outright against creating a new API, but I do not think that task should be undertaken lightly or done half-way.  For now, unless someone expresses a strong interest in championing a whole new non-leaky API and can prove that they can succeed my vote is to just have this be a thin wrapper around JSON-RPC.

If this is a thin wrapper around JSON-RPC API, then we should *not* accept numbers because the JSON-RPC API does not (should not?) accept numbers.

---

**ryanio** (2018-07-03):

Re: events, gotcha. accountsChanged definitely seems appropriate to start. By the way in Mist we allow you to connect multiple accounts at once.

For networkChanged, it might make sense to stick to ‘end’ then ‘connect’ because I don’t think any node can instantly switch like that without ‘rebooting’ by ending the network session first. We could just always re-pass the ethereum provider on ‘connect,’ and then the dapp can check the ethereum.info object to see if the network (or anything else) is different than what they were already on.

Re: JSON-RPC API, yes I think a thin wrapper is best.

The JSON-RPC [spec](https://www.jsonrpc.org/specification) says that it supports the four primitive types of JSON: Strings, Numbers, Booleans, and Null. I think it makes sense to just pass the params directly to the node as given, I don’t see a benefit in interfering…thoughts?

---

**MicahZoltu** (2018-07-03):

JSON-RPC spec supports string, number, boolean, null, but the Ethereum JSON-RPC API does not (I believe).  For most of its payloads it only supports numbers hex encoded as a string.  I think there are a few places where it accepts/excepts an actual number, but it is unclear where these are other than by poking at it.

If this is going to be a thin wrapper around the Ethereum JSON-RPC API then you are right, it is probably best to have `params` in `ethereum.send` just be an `Array<any>`.

```auto
// JSON-RPC requests
ethereum.send(method, params): Promise
```

I think this should change to

```auto
// JSON-RPC requests
ethereum.send(method: string, params: Array): Promise;
```

Note in particular that it returns a promise of `any`. If an error occurs during processing, then the promise will be rejected with an `Error` from the provider.  If an error comes back from the JSON-RPC API call, then `response.error` will be wrapped in a JS `Error` and the promise rejected with that.  If no errors occurs then the promise will resolve with whatever was in the JSON-RPC `response.result`.  (all of this should be spelled out clearly using MUST wording like:

> If the Ethereum JSON-RPC API returns response object that contains an error property then the Promise MUST be rejected with an Error object containing the response.error.message as the Error message, response.error.code as a code property on the error and response.error.data as a data property on the error.
>
>
> If an error occurs during processing, such as an HTTP error or internal parsing error then the Promise MUST be rejected with an Error object containing a human readable string message describing the error and SHOULD populate code and data properties on the error object with additional error details.
>
>
> If there is no error on the response and there is a result on the response then the promise MUST resolve with the response.result object untouched by the implementing wrapper.

Though, after typing the above I realize that some providers may not be interfacing with an external JSON-RPC API provider and instead may be fulfilling requests themselves, so someone should probably reword that to indicate that the above apply only if your provider is wrapping external calls, and if your wrapper is not talking to an external JSON-RPC API provider then it should ensure that the promise is rejected with an `Error` that matches the above shape in the case of an error or it should resolve with an object that matches the JSON-RPC API object as specified in the Ethereum JSON-RPC documentation.

---

**ryanio** (2018-07-03):

Thanks Micah, just updated with your helpful contributions.

Let me know if there are any other considerations!

I will keep working on writing out the MUST spec for the pub-sub subscriptions and events.

---

**bitpshr** (2018-07-03):

Thanks for working to formalize a provider API [@ryanio](/u/ryanio)! I think this looks good so far. After a quick verbiage review, I’d suggest removing the note about the provider request return value in the “summary” section since this is covered by EIP-1102. I’d also suggest modifying the “usage” section slightly to only show provider API usage, not how it’s requested.

---

**frozeman** (2018-07-09):

Why doesn send talks about JSON RPC? The ideas of this provider is to hide the JSON RPC stuff behind the provider, and therefore only accept method and params. In the future there can be other means by which the browser or middle ware talks to a node.

---

**frozeman** (2018-07-09):

I am not convinced of the requesting of ethereum providers. They should be there by default. As for protecting the users privacy we simply don’t return any accounts (only an empty array), until the user allows accounts to be visible. Without accounts, the dapp can only access common information from the blockchain which is not a problem.

Also from a usability perspective, nobody wants to click OK for every website he visits.

---

**ryanio** (2018-07-09):

> Why doesn send talks about JSON RPC? The ideas of this provider is to hide the JSON RPC stuff behind the provider, and therefore only accept method and params. In the future there can be other means by which the browser or middle ware talks to a node.

The `send` method does only accept `method` and `params`.

> I am not convinced of the requesting of ethereum providers. They should be there by default. As for protecting the users privacy we simply don’t return any accounts (only an empty array), until the user allows accounts to be visible. Without accounts, the dapp can only access common information from the blockchain which is not a problem.

We should have more discussion around this, what do other people think? I do think [EIP 1102](https://eips.ethereum.org/EIPS/eip-1102) makes a good argument for the behavior against fingerprinting attacks. I also like the idea of having a standard way you can explicitly request the provider and expect to receive it, instead of relying on it being available in the global namespace.

I don’t think a dapp should have automatic access to the provider due to the potential for abuse (a rogue dapp sending `eth_getBlockByNumber` 10000 times locking up your machine before you even understand what’s going on.) We could introduce rate limiting in the provider, or maybe how the nodes are designed to handle something like that, but I don’t think a normal webpage should have default access to a provider.

> Also from a usability perspective, nobody wants to click OK for every website he visits.

I believe you only visit a small number of dapps, and giving explicit permission the first time you visit a new dapp is okay for most users in such a sensitive environment.

---

**frozeman** (2018-07-11):

The spam attacks from a dapp is a valid concern, but you could do that with javascript today as well. Simply open a 1000 alert windows. Though as we have seen browser protect against that, so could Mist and others, when the see that to many requests are fired by one dapp…

I think usability and easy access by dapps is key. Similar like the `chrome` object, which is also just “there”. But i am happy to hear more opinions on that.

---

**MicahZoltu** (2018-07-15):

I believe the argument for not revealing web3 enabled browser is that it gives away information about the user, particularly that they use ETH.  This allows advertisers to target you more specifically as well as allows attackers to create more targeted attack vectors (for example, that don’t show up for non-web3 users to reduce the time until they are found).

This is similar to user agents, in that by telling Google I am using Firefox via User Agent, it can advertise to me to use Chrome.  Similarly, an attacker can have their attack only execute against Chrome users that are vulnerable to the attack, and lie dormant for Firefox users.

---

**bitpshr** (2018-07-16):

[@frozeman](/u/frozeman): Without sidetracking the discussion around the actual provider API, I feel strongly that exposing either a provider object or `web3` globally by default is objectively different than the Chrome browser exposing a `chrome` global (or any other global on the `window` object.) A browser-specific utility object like `chrome` offers no identifying information beyond browser brand, which is already deducible by other means. The mere presence of an Ethereum-specific object uniquely identifies Ethereum users regardless of whether an account is exposed. A more-accurate comparison of this behavior would be if your fiat bank blindly injected an identifying object on every website you visited so any site could know what bank you specifically used (and in some cases, your account number.) MetaMask recently saw a wave of successful, high-profile phishing attempts that specifically targeted users based on `web3` availability. Like [@MicahZoltu](/u/micahzoltu) said, the genesis of opt-in exposure is privacy, not spam-prevention.

Further, [EIP-1102](https://ethereum-magicians.org/t/eip-1102-opt-in-provider-access/414) lays out a protocol for user-approved provider access, but it doesn’t mandate any specific UX. For example, what if dapp browsers cached which sites a user has approved so it’s a one-time approval? It’s still possible to provide a near-“always there” experience while still maintaining necessary user privacy and giving them control over which sites know they’re Ethereum users.

[@ryanio](/u/ryanio): I think the API is coming together very nicely. Do you plan to define the proposed `eth_changeNetwork` RPC method, or is this outside the scope of this proposal?

---

**ryanio** (2018-07-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/bitpshr/48/190_2.png) bitpshr:

> @ryanio: I think the API is coming together very nicely. Do you plan to define the proposed eth_changeNetwork RPC method, or is this outside the scope of this proposal?

Thanks! Hm, I’m not sure if it’s outside scope, but after thinking about it since every implementing provider will need to handle the request differently, we could include a spec line like this under `send`:

> If the method eth_changeNetwork is sent with params [networkId: String], the implementing provider MUST change the network and on success MUST emit the event networkChanged with the new networkId. If the provider cannot handle changing to the requested network or encounters any other error in the changing process, the provider MUST reject the Promise with an Error object containing a human readable string message describing the error and SHOULD populate the code and data properties on the error object with additional error details.

What do you think?

---

**bitpshr** (2018-07-21):

I think the `eth_changeNetwork` specification as written above makes sense. However, since this proposal is meant to be specific to the JavaScript provider API, not the underlying RPC API, I worry slightly about this newly-suggested method getting lost. I’d suggest proposing this change directly to the RPC specification, and then retroactively updating the abstracted JavaScript API via this proposal.

---

**ryanio** (2018-07-22):

That sounds like a good idea. After finishing our implementation in Mist, I will see if I can propose `eth_changeNetwork` as an addition to the RPC specification. Thanks again for your help.


*(41 more replies not shown)*
