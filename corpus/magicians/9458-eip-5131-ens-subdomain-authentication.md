---
source: magicians
topic_id: 9458
title: EIP-5131 - ENS Subdomain Authentication
author: wwhchung
date: "2022-06-03"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-5131-ens-subdomain-authentication/9458
views: 3795
likes: 7
posts_count: 23
---

# EIP-5131 - ENS Subdomain Authentication

Following discussion from this twitter thread:



      [twitter.com](https://twitter.com/wwhchung/status/1531812006319206400?s=20&t=Om9F4VBzizz6TJGXadDcCA)



    ![image](https://pbs.twimg.com/profile_images/1580754128611180544/GasOUcW-_200x200.jpg)

####

[@wwhchung](https://twitter.com/wwhchung/status/1531812006319206400?s=20&t=Om9F4VBzizz6TJGXadDcCA)

  1/ Proposal for safe validation of your NFTs, a 🧵

Today, in order to verify that you control an address or own an NFT, you typically sign a message to authenticate (e.g. editing your profile on OpenSea).

  https://twitter.com/wwhchung/status/1531812006319206400?s=20&t=Om9F4VBzizz6TJGXadDcCA










At current, web2 and contracts validate asset ownership and wallet control by requiring you to sign a message or transaction with the wallet that owns the asset.

Examples:

- In order for you to edit your profile on OpenSea, you must sign a message with your wallet address.
- In order to access NFT gated content, you must sign a message with the wallet containing the NFT
- In order to claim an airdrop, you must interact with the smart contract with the qualifying wallet address.

This method of validation is problematic from a security standpoint (interacting with a malicious site or contract can compromise your wallet’s assets) and a convenience standpoint (e.g. if your assets are on a hardware wallet that is not easily accessible).

This EIP proposes a solution which uses the Ethereum Name Service Specification (EIP-137) as a way to link one or more authentication wallets to verify control and asset ownership of a main wallet.

---

Functionally, this would work as follows (assuming the main wallet has an ENS domain and resolver record set).

1. Create subomain record on the main ENS domain, starting with auth[0-9]*
2. Set that record to the new authentication wallet
3. Set the reverse record of the authentication wallet to auth[0-9]*.

Then, on a web client, you determine the linked main wallet whenever the authentication wallet performs an action by:

1. Do a reverse lookup of the authentication wallet to get the ENS name
2. Parse out the main ENS
3. Lookup the address the main ENS resolves to, and that is the wallet you are authenticating for.

Effectively, this is a mechanism to do ‘read only’ authentication.  Note: Steps 1-3 can be performed client side, and the results passed to a smart contract for cheap validation (rather than doing string operations on a smart contract).

---

Q: Why subdomains vs. TXT records?

A: Subdomains allow us to do the reverse resolution strategy outlined above, meaning that it doesn’t require a user to input the address they are trying to authenticate for.  It makes it much easier from a userflow perspective.  If we were using TXT records, you would need another field to input the wallet you are attempting to authenticate as.

## Replies

**wwhchung** (2022-06-03):

Added sample client and solidity code samples.  (note: solidity code is pretty inefficient right now and untested, may need design changes).

https://github.com/manifoldxyz/ens-auth-ethers

https://github.com/manifoldxyz/ens-auth-solidity

---

**Pandapip1** (2022-06-03):

Have you looked at [EIP-1271: Standard Signature Validation Method for Contracts](https://eips.ethereum.org/EIPS/eip-1271)? I think it might be better to change this PR to be more in line with it, to avoid having multiple standards that need to be implemented.

---

**wwhchung** (2022-06-03):

I have and am familiar with it.  This spec is intended to be used in conjunction with something like EIP-1271, and for client side web app and backend server validation as well.

Are you suggesting that the contract side validation uses EIP-1271 for cheap validation after a secure server has validated the auth link exists?  Or am I missing something?

---

**Pandapip1** (2022-06-03):

That is indeed what I am suggesting.

---

**wwhchung** (2022-06-03):

Makes sense.  The reference implementation I wrote assumed that there would not necessarily be a ‘server side’ or secret available, but if they had one, then they could simply do that check and computation server side and use EIP-1271 (which is what we would do).

I modified the EIP to reflect this in the reference implementations section. If it doesn’t look right, do you have any suggestions on how else I should edit it to reflect what we’re discussing?  This is my first EIP, so any help would be appreciated. ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**cxkoda** (2022-06-08):

Moving over parts of the [discussion from the github PR](https://github.com/ethereum/EIPs/pull/5131#issuecomment-1148751791) so it doesn’t get lost after it was merged.

### cxkoda commented

…

Though, I’m still not totally convinced of the approach with subdomains yet. As far as I have understood, the reasoning was that subdomains can be easily linked using reverse records which yield an improved UX when logging into a platform, right? So the platform provider can just look up the reverse record of `authAddress` and knows which `mainENS` we are trying to authenticate for, without any further user interaction. Other than that, the `authAddress` reverse record serves no purpose to my understanding.

IMO, this approach has a few downsides:

- The reverse records need to be set by authAddress. This requires transferring funds and some txs from there and makes hence setting up auth wallets a bit cumbersome (effectively preventing throwaway auths).
- A given authAddress can only be used to authenticate for one mainENS, because reverse records are unique.

Which might be intended? Also I think this is much easier to handle from a platform perspective.

When logging into a service with `authAddress`, the user still has to specify that they want to authenticate for a linked `mainAddress` instead of the current address. So an interaction will be required anyways.

- This could be removed by defaulting that all reverse records starting with auth.* will only ever authenticate for the linked addresses. But this would be needed to be stated explicitly in the proposal.

Txt records, or subdomains without enforced reverse records would not suffer from these drawbacks but require the user to specify which `mainAddress` they want to authenticate for (which can be cached by the platform, wallet, etc though).

Maybe it would make sense to go for a hybrid approach? So if a reverse record exists, go the default route - if not, prompt the user to specify it? Or will that get too cumbersome?

What do you folks think?

### wwhchung commented

I really think getting ppl to specify it manually is kind of cumbersome. I’m expecting user experiences where I can just sign in with a wallet, one-click style, without need to enter further info. I’m also quite lazy, which is why I like piggybacking ENS vs some new protocol.

### cxkoda commented

Fair enough, but in order to get rid of any interaction, the service must always use the linked `mainAddress` over `authAddress` if the reverse record has the correct pattern. So there will be no way to connect with `authAddress` any longer.

Since this behavior is quite important I think it needs to be stated explicitly in the proposal (I hope I didn’t just miss it).

### wwhchung commented

Does it though? Can’t the application treat authAddress authentication as simply signing for authAddress OR mainAddress? That’s how I intended to use it in the app. Prioritize authAddress and if no match then use mainAddress.

### cxkoda commented

> Can’t the application treat authAddress authentication as simply signing for authAddress OR mainAddress?

Wouldn’t that require an unwanted interaction?

Or would you automatically log in using `mainAddress`, but make it manually switchable to `authAddress`?

I think the intended behavior in this case should be stated explicitly in the proposal.

---

**cxkoda** (2022-06-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cxkoda/48/6228_2.png) cxkoda:

> The reverse records need to be set by authAddress. This requires transferring funds and some txs from there and makes hence setting up auth wallets a bit cumbersome (effectively preventing throwaway auths).

This point still bothers me. I think practically excluding throwaway wallets will be an unnecessary hindrance to adoption.

What would you think about running a custom ENS reverse registrar under something like `reverse.eip5131.eth` (maybe even `auth.reverse` if possible), that allows any address to set the reverse record for any other address given a valid ECDSA signature?

This way we could have convenient setup via `mainAddress`, while still maintaining the easy flow via reverse records.

---

**wwhchung** (2022-06-08):

Well, I’m thinking of the application level cases:

1. You are doing a claim, and you require to be in the allowlist to mint:

- This can work by:

Check if the requesting wallet is in the merkle tree, if so, use it, if not
- Check if the linked walllet is in the merkle tree, if so, use it

1. You are doing a web2.0 related gated content access

- This can work by:

Check if the requesting wallet has the requirements, allow if so, if not
- Check if the linked wallet has the requirements, and allow if so

1. Configuring profiles

- This can work by:

Show profiles the signing wallet can access, and ask them to choose
or
- Like on OpenSea, you are on a profile, and if you’re signed into a wallet, the edit button shows if you have access.  You have access simply if the profile is this wallet, or the wallet is linked to the profile’s wallet.

Those are the app cases I can think of, and seem to work reasonably well with minimal user input due to the reverse records being set.  I’m not sure I would put these in the EIP though, because how an app decides to use the knowledge that a wallet is linked should be flexible.

---

**cxkoda** (2022-06-08):

Ah I see where I had my misunderstanding, thanks for the clarification. This seems reasonable.

---

**cxkoda** (2022-06-28):

[@wwhchung](/u/wwhchung) have you given this point any thought yet?

---

**wwhchung** (2022-06-28):

Which point?  There’s a few things we talked about, and I thought I answered something, but I guessed I missed another. ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**cxkoda** (2022-06-28):

Sorry I forgot that replies don’t display as quotes here (and just sent it from my phone).

I was referring to this comment  about a dedicated reverse record registry

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cxkoda/48/6228_2.png) cxkoda:

> This point still bothers me. I think practically excluding throwaway wallets will be an unnecessary hindrance to adoption.
> What would you think about running a custom ENS reverse registrar under something like reverse.eip5131.eth (maybe even auth.reverse if possible), that allows any address to set the reverse record for any other address given a valid ECDSA signature?
>
>
> This way we could have convenient setup via mainAddress, while still maintaining the easy flow via reverse records.

---

**fulldecent** (2022-06-29):

Hi team. I think I am read up-to-date on the design ideas here for EIP-5131 DRAFT.

[![Screen Shot 2022-06-29 at 17.26.37](https://ethereum-magicians.org/uploads/default/original/2X/b/bf733df546f2560f10c45fdf5f1bc2321a0b23a4.png)Screen Shot 2022-06-29 at 17.26.371360×906 30.3 KB](https://ethereum-magicians.org/uploads/default/bf733df546f2560f10c45fdf5f1bc2321a0b23a4)

And some feedback.

- TXT records allow one-to-many and many-to-many logins. We either want to support this or not, and this design choice should be spelled out in the EIP.
- When you “login to OpenSea” you may want to login as auth1.mary.eth or you may want to login as Mary.eth. This should be a choice presented in some dialog box. This choice should be given to the website visitor. And we should specify this in the EIP.
- The discussion above says we DON"T want to specify the main address. But the reference implementation DOES specify the main address.
- Putting Ether into your auth wallet to setup reverse DNS is painful. Think this through.

This comment does not justify a complete audit or review.

---

**wwhchung** (2022-06-29):

[@fulldecent](/u/fulldecent)

Hey there. It’s very possible that the spec wasn’t clearly written or there’s some confusion. So appreciate the response.

The spec is intended to only allow for a one (mainAddress) to many (authAddress) relationship. This is enforced by:

mainENS can allow for many sub records (one to many)

authAddress must set the reverse record to authENS which is a sub record of mainENS.

So, when authAddress signs, it is signing for only mainAddress/mainENS (no popup or selection should be needed).

Conversely, mainAddress should be able to allow for many authAddresses

Does that make sense? If not, how does that differ from your interpretation and which parts would help clarify the EIP to match what I’m describing? Thanks!

---

**wwhchung** (2022-06-29):

[@cxkoda](/u/cxkoda) whats your definition of a throwaway wallet here? From my standpoint, a lot of those signing wallets could end up being throwaway, but would have a tiny bit of eth. Do you mean throwaway from the perspective of being able to configure with no eth? If so, then yes, I agree and maybe needs expansion to allow setting by the mainAddress with a new reverse registry like you said. There might be an even cleverer way though. Possibly setting a record based on a signed message from the authAddress?

---

**fulldecent** (2022-06-30):

Yes, I do understand that this is building a one (mainAddress) to many (authAddress) relationship.

But people are going to question why you didn’t design it a different way. So stating this in the spec can be helpful. For example, ERC-721 specifically mentions that it has anticipated use cases of non-transferrable tokens (i.e. “soulbound tokens”), negative value tokens and other specific applications. It was certainly helpful to have that written down and is still helpful now.

If there is no popup selection that means that a wallet named auth… will be impossible to login to a website that supports EIP-5131. That’s a problem.

---

**wwhchung** (2022-07-01):

Ah. Now I see what you mean. Makes sense and will clarify this in the spec and get back to you.

---

**wwhchung** (2022-07-03):

[@fulldecent](/u/fulldecent) [@cxkoda](/u/cxkoda)

Note: from a UI standpoint, I was thinking that the one-to-many relationship would actually also allow for simple UI, without the need to select the address in many cases.  e.g.

For an NFT management website, you could simply show a list of tokens owned by both the authAddress and the linked mainAddress, with some UI labeling.  Then the client side can determine the appropriate corresponding address WITHOUT any user interaction.

I would imagine that, in Rainbow Wallet, if you were logged in via the auth address, you would see both your NFTs and the NFTs you could sign for.

---

**wwhchung** (2022-07-03):

[@fulldecent](/u/fulldecent) I’ve made some edits to the EIP that hopefully address what you mentioned.  Do you think it’s clear enough or do you think more context is needed (and if so, which areas do you think should be expanded on)?

And going through the thought process, I actually think you can create a UI/UX that doesn’t require additional selectors with this mechanism for many use cases (although you would still need an address selector for a few as well, however I can’t think of many).  Examples:

**NFT staking page, claim pages, access gated pages, etc**

No selector needed. You could simply show all NFTs of both the authAddres and mainAddress, with a little UI label beside each.  When you interact with a given NFT, you simply use the right ‘address’ if the method needs it.

***Web2/Web3 Wallet Based Profiles (e.g. OpenSea profiles)***

No selector needed.  When you go edit a given profile, you simply have to sign with EITHER the mainAddress or any authAddress

In what case do you think a selector is needed?  Seems like most cases can be solved without.

---

**cxkoda** (2022-07-05):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/w/7993a0/48.png) wwhchung:

> Do you mean throwaway from the perspective of being able to configure with no eth?

Sorry for being unspecific - yup setting up auth wallets without transferring funds to them is what I meant.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/w/7993a0/48.png) wwhchung:

> If so, then yes, I agree and maybe needs expansion to allow setting by the mainAddress with a new reverse registry like you said. There might be an even cleverer way though.  Possibly setting a record based on a signed message from the authAddress?

jup that’s exactly what I meant with

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cxkoda/48/6228_2.png) cxkoda:

> What would you think about running a custom ENS reverse registrar under something like reverse.eip5131.eth (maybe even auth.reverse if possible), that allows any address to set the reverse record for any other address given a valid ECDSA signature?

The downside is that the standard reverse resolution of common node packages is no longer applicable. However, the relevant logic can be implement quickly - so this is would only be a small sacrifice.

I think this delegated reverse-resolution registration would warrant an own EIP (or ENSIP?) though as the applications may go beyond the one here. So it might be worth discussing it in a broader context. I could also see it being implemented as an extension to [EIP-181](https://eips.ethereum.org/EIPS/eip-181) ([ENSIP-3](https://docs.ens.domains/ens-improvement-proposals/ensip-3-reverse-resolution)) replacing the registrar for `addr.reverse` with a revised one that supports something like `setNameFor(address for, bytes calldata sig, address owner)`.

This way the standard ENS tooling can again be reused and it the authing scheme presented here would again be fully built on top of ENS.


*(2 more replies not shown)*
