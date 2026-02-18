---
source: magicians
topic_id: 2903
title: "Dapplets: call for related works"
author: Ethernian
date: "2019-03-12"
category: Web > Wallets
tags: [wallet, dapplets]
url: https://ethereum-magicians.org/t/dapplets-call-for-related-works/2903
views: 1426
likes: 2
posts_count: 11
---

# Dapplets: call for related works

Hello all,

We have implemented [#dapplets proposal](https://ethereum-magicians.org/t/dapplets-rethinking-dapp-architecture-for-better-adoption-and-security/2799) as very early stage PoC in ETHParis Hackathon.

See this [video for details](https://twitter.com/Ethernian/status/1104596777519452160).

Now I am trying to review existing proposals and other things that could be related to dapplets in order to take a broader look and define a roadmap for further development.

I have identified following items:

- (EIP-719) Trustless Signing UI Protocol by @MicahZoltu, @Arachnid
- (EIP-712) signTypedData by  @fulldecent, @danfinlay
- EIP typed data translation by @weijiekoh
- NatSpec
- RadSpec

Is there a good implementation of the three EIPs above available?

Is there any other related items that could be important?

please let me know,

## Replies

**fulldecent** (2019-03-12):

Thank you for the ping. I’m involved more in NatSpec than 712. I have made some minor updates on NatSpec last month and I maintain it.

But if we are going to have actual change here then we will require implementation from MetaMask or a competitor.

It’s not like other core EIP initiatives where somebody has an idea and Vitalik pays for its implementation out of the fund.

---

**Ethernian** (2019-03-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fulldecent/48/8663_2.png) fulldecent:

> But if we are going to have actual change here then we will require implementation from MetaMask or a competitor.

Thank you for reply!

I am not going to change standards right now. Just exploring the space currently.

I have no much doubts on adoption because there are clear business incentives for wallets to go this way (if we provide sufficient level of security, of cause).

---

**Ethernian** (2019-03-22):

[@fulldecent](/u/fulldecent),

Even more because you may have different opinion on how current challenges in secure signing may be solved, I would very appreciate your opinion on the draft of the [Dapplets article I have wrote in medium](https://medium.com/@Ethernian/dapplets-part-1-introduce-new-dapp-architecture-for-better-ux-and-security-75a4881b4765).

Could you take a look? The scope of the article is to define the problem and outline possible solution without going into deep technical details. Any critic is appreciated.

---

**fulldecent** (2019-03-22):

Hi, I don’t have a Medium account but I read the TL;DR and the proposed picture at the bottom.

Two issues:

1. Removing Web3 from the dApp and adding a specific vendor… I think this is moving backwards. We should encourage the visitor (and the browser on their behalf) to have web3 services available. Just like we depend on them to have XMLHttpRequest available.
2. You are proposing MetaMask to make changes. This is fun but it wont happen. MetaMask /still/ doesn’t support ERC-721, a large application class on the blockchain. And right now the way the ecosystem works is that everybody wants to reinvent the wheel. Just look at the number of ERCs created. That paper proposes adding a 2+ year delay for the user interface to update every time somebody wants to update a new application.
 2a. One solution is to make the creation of the Signer UI customizable. As in you can design new forms (they can be responsive) and layout the elements on the page. Boom, then you just reinvented what we have today.

**But don’t let me stop you!** I think all this is good ideas, and I’d love to see you try. But the most likely way to make this reality is for you to fork MetaMask and implement this stuff. If your vision requires you wait for other people to implement this stuff then that is unlikely to ever happen.

---

**Ethernian** (2019-03-22):

> You are proposing MetaMask to make changes.

not the case any more. [ETHParis implementation was WalletConnect based.](https://twitter.com/Ethernian/status/1104596777519452160)

> Hi, I don’t have a Medium account

challenge accepted… I should think how to share the draft without expecting medium account.

---

**JamesZaki** (2020-02-05):

Hey [@fulldecent](/u/fulldecent), I always like seeing your posts around tokens etc.

May I suggest a 2a’. That is, a customisable signer UI with the following attributes:

- is signed by the entity creating the smart contract (creating entity)
- on-chain integrity hash
- downloadable to wallet from creating entity
- run in a sandboxed environment in a wallet

access to web3
- tx signing actions decoupled
- whitelisted domains if required

Would you say this reinvents what we have today?

---

**fulldecent** (2020-02-06):

Actually we already have most of that technology!

The missing component is whitelist domains. We need an implementation and standard for that, it can look like:

```auto
interface ERCxxxx {
    enum Permission {None, UNUSED, UriIsAllowed, UriAndSubpathsAllowed, UriAndSubdomainsAndSubpathsAllowed};

    /// @param uri Specified URI to check
    /// @return magic A magic value (....) is returned if the specified URI allows the dApp to run
    /// @note Client should test a URI, all parent paths, and all domain parents for completeness
    function isUriAllowedToRunDapp(string calldata uri) returns (bytes4 magic)
}
```

If you are serious about this, you can implement it, and then write it up, bring me in as coauthor.

All of the other components already exist by convention in NatSpec. By default Solidity stores the source code hash to chain. All worthwhile contracts have their source code published to Swarm. So this means that any client is can do this:

1. Website requests transaction
2. Client looks up target contract address
3. Client uses ERCxxxx to ask if the current URI is authorized for target contract
4. If authorized, client gets target contract source code from Swarm
5. Client parses NatSpec from target contract source code
6. Client renders transaction dialog using interpreted NatSpec

# Work plan:

1. Implement ERCxxxx and standardize it
2. Create client front end (Chrome extension, iOS app, etc) to implement the above
3. ???
4. Profit

---

**JamesZaki** (2020-02-07):

In the case where the signer UI module is referred to by the smart contract (eg tokenURI), would it not be better to store the whitelist off-chain in the module?

Trust-wise it’s no different, but keeps long urls off-chain (although could be reduced with hashes).

On-chain blacklists would make sense though.

My original question was in response to…

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fulldecent/48/8663_2.png) fulldecent:

> 2a. One solution is to make the creation of the Signer UI customizable. As in you can design new forms (they can be responsive) and layout the elements on the page. Boom, then you just reinvented what we have today.

wondering how the proposal was reinventing what we have today?

---

**Ethernian** (2020-02-22):

[@JamesZaki](/u/jameszaki), [@fulldecent](/u/fulldecent),

Guys, thank you for your comments and sorry for delayed answer from my side.

The Wallet Sandbox execution model has many fine aspects regarding chain of trust, execution model and type-to-widget mapping.

I am preparing an article diving into many details of the topic and describing the state of our implementation. I need feedback, because not everything is solved optimal and there are place for improvements.

Hopefully the article will be finalized next week.

I would really appreciate if you could take a look over the draft in progress and give me some feedback. Please let me know if you are interested, I’ll send you a link.

---

**fulldecent** (2021-05-07):

This comment is not aging well. We need to ALLOWlist domains.

