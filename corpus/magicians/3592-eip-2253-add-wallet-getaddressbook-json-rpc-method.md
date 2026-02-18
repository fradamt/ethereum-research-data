---
source: magicians
topic_id: 3592
title: "EIP-2253: Add wallet_getAddressBook JSON-RPC method"
author: loredanacirstea
date: "2019-08-27"
category: EIPs
tags: [wallet, json-rpc]
url: https://ethereum-magicians.org/t/eip-2253-add-wallet-getaddressbook-json-rpc-method/3592
views: 3141
likes: 12
posts_count: 16
---

# EIP-2253: Add wallet_getAddressBook JSON-RPC method

Draft Proposal: [Add wallet_getAddressBook JSON-RPC method by loredanacirstea · Pull Request #2253 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/2253)

tl;dr

Address books for wallets are becoming a standard feature, greatly improving usability, while maintaining user ownership on this data.

There is no standardized way for a dApp to leverage this information, with the user’s permission. dApps can use `wallet_getAddressBook` to retrieve strictly the information that they need, in order to process the request.

The current proposal will avoid duplication of effort - dApps will not need to ask the user to create another address book with them. And it also protects the user’s privacy, while increasing usability.

## Replies

**loredanacirstea** (2019-08-27):

[@pedrouid](/u/pedrouid), [@ligi](/u/ligi), [@danfinlay](/u/danfinlay)

---

**karalabe** (2019-08-27):

[@holiman](/u/holiman) Spent a very long time speccing out a secure account management API. I’d really appreciate if we converged on those efforts and not start over. https://github.com/ethereum/go-ethereum/tree/master/cmd/clef

---

**loredanacirstea** (2019-08-27):

I was not aware Clef can manage other accounts than the user’s. E.g. user’s friends accounts are kept in the address book. And Clef’s readme talks about the user’s accounts.

Did I miss anything?

I don’t understand how Clef would work with web wallets (e.g. Metamask), which use Infura or mobile wallets. Can you point me to a reference?

---

**danfinlay** (2019-08-27):

I think this could be very useful for some applications, and is very compatible with the [wallet permissions proposal](https://ethereum-magicians.org/t/web3-login-permissions/3583).

That said, it could also be a privacy leaking vector, so in addition to the ability to grant full access to your address book, it would be nice for wallets to include an address selecting method, maybe `wallet_selectAddresses`. Imagine a file picker: The dialog may require one file, or may permit multiple selections. You might even select a group to selectively disclose. It’s possible this selector could simply be integrated into a primary permissions-request screen instead.

One parameter that might go well with this (and any permission, actually) would be a `justification` field, so that the wallet could provide the justification given by the application for why it is requesting this permission, and what type of selection should be made. It would be up to the wallet to clearly distinguish the app-provided justification from its own presented information.

There is also a question of the data provided in response: Could this be an opportunity for the user to provide their own nicknames for addresses they are aware of? Assign their own icons to accounts they track? Both of these would currently be available from MetaMask’s address book implementation, but for the sake of standardization, we should probably choose something that is available in a variety of contexts.

---

**Arachnid** (2019-08-28):

The idea with clef is to separate APIs that are necessarily part of a node - fetching chain state and submitting transactions - from APIs that are concerned with user accounts - signing, key management etc. The reason for this is that everyone should store their own keys, but not everyone wants to run their own node. Decoupling these makes it possible to do this more easily, and separates concerns.

User specific data like an address book definitely belongs on the Clef side of things, not the node side of things.

---

**loredanacirstea** (2019-08-28):

[@Arachnid](/u/arachnid), yes, I knew the first part - I saw the Clef presentation in an Ethereum Berlin meetup > half a year ago.

> User specific data like an address book definitely belongs on the Clef side of things, not the node side of things.

I agree with this.

[@karalabe](/u/karalabe), [@holiman](/u/holiman), there is no mention of a proposal for retrieving address book items in the Clef repo. I am beginning, not starting over. Plus, any such proposal should be an EIP draft - easily findable by interested parties (e.g. wallets), so they can plan & contribute.

I see that Clef uses the same JSON-RPC standard, so my proposal remains valid. Let’s discuss it:

The data type specced out in Clef, for returning a user’s account is:

```auto
{
  "address": "0xafb2f771f58513609765698f65d3f2f0224a956f",
  "type": "account",
  "url": "keystore:///tmp/keystore/UTC--2017-08-24T07-26-47.162109726Z--afb2f771f58513609765698f65d3f2f0224a956f"
},

```

So, I can add `type` to the data type that I proposed. `WalletAddressBookItem` will therefore have this format:

```auto
{
  "address": "0x0000000000000000000000000000000000000001",
  "type": "account",
  "name": "My Friend"
}
```

**Is the above acceptable?**

[@karalabe](/u/karalabe), on [my PR](https://github.com/ethereum/EIPs/pull/2253#issuecomment-525415022), you said:

> The field filter seems weird on RPC. That’s essentially what GraphQL is for and how it works. I’m not sure it’s a good idea to start introducing GraphQL concepts into the RPC.

**The issue:** dApps may want all the information from an address book item (better UX). But exposing names or other info might pose a privacy risk, so the user can choose not to expose them. I think it is the user’s decision.

**So, what do you propose for solving this problem, if you do not like the `field` parameter?**

---

**loredanacirstea** (2019-08-28):

[@danfinlay](/u/danfinlay), yes - it will work great with your permissions proposal.

> That said, it could also be a privacy leaking vector, so in addition to the ability to grant full access to your address book, it would be nice for wallets to include an address selecting method, maybe wallet_selectAddresses

In my proposal I have the `field` & `count` parameters, which are for dApps to request only a subset of the address book, with only some of the fields.

In the EIP, I also say:

> If the entire address book is requested, the total number of address book items will be shown. If an address book selection is requested, the user will have to select the items from the address book list.
> The wallet will also show radio options for which WalletAddressBookItem optional fields the user wants to expose, if those fields were requested.

My intention was to allow partial selections. **But I can clarify in my proposal that even if the entire address book is requested, the user should be able to make a selection & restrict exposed fields.**

> Could this be an opportunity for the user to provide their own nicknames for addresses they are aware of?

Yes! This is what the `name` field is for.

> Assign their own icons to accounts they track?

I was thinking about icons, but was unsure. Blockies are used currently, and the dApp can just have support for them. But the `icon` field can be added and if it is empty, then the dApp can use a fallback.

**I will add `icon`. Thank you.**

> One parameter that might go well with this (and any permission, actually) would be a justificationfield, so that the wallet could provide the justification given by the application for why it is requesting this permission

I understand the `justification` field would be in the permissions proposal. In which case, I agree. If the `wallet_getAddressBook` is used by the dApp (outside the permissions system), it is probably triggered by a user’s action and the dApp UI should provide the justification.

---

**danfinlay** (2019-08-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arachnid/48/18_2.png) Arachnid:

> The idea with clef is to separate APIs that are necessarily part of a node - fetching chain state and submitting transactions - from APIs that are concerned with user accounts - signing, key management etc.

This was also the motivation of the `wallet_` prefix, [as suggested elsewhere](https://ethereum-magicians.org/t/add-wallet-methods-to-improve-dapp-to-wallet-interaction/1848), and in use by this proposal.

What would be the extra steps that make this very-clef-like?

---

**holiman** (2019-08-29):

The thing to know about Clef, is that there are two separate channels for communications.

1. The external api.  This is where browsers/dapps/external machines issue requests. Everything that traverses this API (either in or out) is considered not sensitive / not personal data. So over this API, there are never things such as paths or passwords, only requests and their responses.
2. The internal api. This is where a user interface application can talk to the clef daemon, over stdin/stdout. It also uses json-rpc. The account info you quote above is from the internal channel, not the external one.

Now, the proposal to add meta-info to wallets/accounts fits perfectly with what I’ve already considered. Some things I’d also like to have are

- Ability to name an account (e.g. “Friend X”),
- Ability to create a ‘stub’ account, which basically says

On the ledger X, at path Y, is account with address Z named “Safe backup”. This enables ‘clef’ know in advance which accounts to auto-derive on the hw wallet, plus serve Z as one of the available accounts.

All in all, I think it fits well with Clef, but some potential privacy concerns must be addressed. In the case of Clef, that’s pretty easy, since there’s always a channel to ask the user about how to move forward.

---

**jennypollack** (2019-08-30):

In the current MetaMask implementation we also store the chainId as part of the addressBookEntry.

I think adding this identifier as a parameter as an optional argument to the request could make sense, possibly with the default set to 1.

---

**loredanacirstea** (2019-08-30):

[@holiman](/u/holiman), my intent for the proposal was to request a user’s list of friends/colleagues/services accounts, not his own accounts, which are now provided through `eth_accounts`. I see that I failed to make this point clear - I will amend the PR. I associated address book with phone book.

Indeed, having meta-info for the user’s accounts is good and the request format & data types should align.

---

**loredanacirstea** (2019-08-30):

[@jennypollack](/u/jennypollack)

I am reluctant to add the `chainId` here, just because an address can be used on multiple chains (I use the same addresses on multiple testnets). And this relies too much on wallet implementations.

But let’s also see other opinions.

---

**ligi** (2019-08-31):

I also signal to not have the chaiId in there as I also use the same key across different chains. If we really need to have chainId in there IMHO it *must* be a list. But even then it becomes messy. Also think about the case that a key is not even used on a chain. I would just leave it out to avoid all these complications.

---

**holiman** (2019-09-02):

No, you made the point clear, I was just a bit carried away by the tangent that I already had in my head.

As I see it, they are related – it’s meta-info about addresses. The info is personal, and can either be about external accounts to which the user does not have the key (friends, favourite dapps etc) and internal accounts.

You’re approaching it from the user-perspective, I’m approaching it from the bottom up. So from my perspective, we’ll need to consider how this info is stored (as part of the keystore? As a separate addressbook?), and from your perspective I think the RPC methods suggested is a good start.

---

**loredanacirstea** (2019-09-03):

[@karalabe](/u/karalabe), now can you fix your comment https://github.com/ethereum/EIPs/pull/2253#issuecomment-525415022, so I can get this proposal merged?

Be aware that your position as a core developer influences others in reading/reviewing EIPs. It is enough to make a comment like that, for people to not even read the EIP content. So, when you misunderstand something, you are expected to fix it.

