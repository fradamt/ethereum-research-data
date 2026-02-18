---
source: magicians
topic_id: 16690
title: "ERC 7710: Smart Contract Delegation"
author: danfinlay
date: "2023-11-19"
category: Web > Wallets
tags: [erc, wallet, account-abstraction, devconnect]
url: https://ethereum-magicians.org/t/erc-7710-smart-contract-delegation/16690
views: 5888
likes: 40
posts_count: 35
---

# ERC 7710: Smart Contract Delegation

Edit: I have updated the title of this post to reflect that it evolved into a concrete ERC, with greater specificity, and this thread is the official discussion post for that ERC. Original title is below:

**Title: Towards More Conversational Wallet Connections: A Proposal for the `redeemDelegation` Interface**

Expands on ideas first shared in this talk at the Wallet UX Unconference in Istanbul 2023:

https://streameth.org/watch?event=wallet_unconference&session=65b8f8d6a5b2d09b88ec192f

Hello Ethereum Community,

I’m reaching out following my presentation at the Devconnect 2023 Istanbul UX Unconference. For those who couldn’t attend, I plan to share a video of that talk shortly. The focus of my presentation, and the reason for this post, revolves around reimagining how wallet connections could be more conversational and user-centric in the Ethereum space.

I’m here not just to propose an idea but to initiate a dialogue about how we can collectively enhance user interactions within our ecosystem. The concept I’m about to introduce is very much in its infancy and open to evolution, especially with insights from this community.

**The Core Challenge**

Our current model of initiating connections by exposing a user’s public address has several drawbacks, including vulnerability to phishing and the pressure on application developers to maintain complex indexing infrastructures. This system tends to favor well-established assets, creates barriers for newer entries, and has been tending wallets towards more and more centralized infrastructure to try to combat scams and add readability to an interaction pattern that is inherently unreadable and prone to excessive disclosure.

One way to improve user coherence and reduce reliance on centralized infrastructure is to put the site connection back in the user’s hands, and empower them to issue “session keys” for the dapp connection. These interactions can be explored if we first have a standard method for contract accounts to issue arbitrary session permissions (which can hopefully grow and evolve as an ecosystem).

One way session permissions can be issued is by giving a site a mechanism to request the type of asset it needs to proceed, and then giving the user an ability to select the set of assets/permissions that they want to share (requiring additional deliberative steps for the user, and reducing the risk of confirmation-fatigue).

**Introducing `redeemDelegation`**

To address these issues, I propose an abstract Solidity interface named `redeemDelegation`. Here’s a preliminary look at the interface. It’s very much a draft, and meant to start conversation:

```solidity
function redeemDelegation(
    address onBehalfOf,
    TxParams calldata txParamsToCall,
    bytes authorization
) public;
```

The intent behind `redeemDelegation` is to enable contract accounts to adopt diverse authorization logics, thereby allowing for tailor-made and user-directed authorization when connecting to websites. This approach diverges from the current norm of websites dictating transactions, sometimes through obscure allowance methods, and could reduce the dependence on centralized infrastructures.

**Envisioning Diverse Applications**

With `redeemDelegation`, we could explore various innovative models:

1. The Powerbox/File-Picker Approach: This model would enable sites to request specific permissions, with users having the freedom to select assets and set boundaries for site interactions. This not only empowers users but also eases the burden on developers.
2. AI/LLM-Enabled Interactions: Imagine users specifying authorization terms in their own language, and AI models translating these into tangible authorization parameters. This could make for a more intuitive and user-friendly experience.

**A Collaborative Journey Ahead**

This concept is not just about a new interface; it’s about rethinking our approach to user interactions in the Ethereum ecosystem. It requires not only new code but also new ways of thinking and building.

I look forward to your thoughts, critiques, and suggestions. Let’s collaboratively explore how we can make wallet connections more secure, intuitive, and user-friendly.

Thank you for your time and consideration.

Best regards,

Dan Finlay, MetaMask

## Replies

**danfinlay** (2023-11-19):

I want to just add: I think this is valuable to standardize around because while many wallets are creating session key standards right now, if we want applications to be able to request those session keys but not be locked into a single wallet, we need to be willing to converge around a common interface.

---

**danfinlay** (2023-11-19):

I was originally going to roll this together with a provider/RPC method also for requesting this session information, but at the Wallet Unconference a reasonable point was made: We might want that method to also abstract chain/execution-environment away, and so I will be working on a proposal for that at the CAIP level next. I consider this a bit of a prerequisite for an Ethereum contract acount to participate in that type of connection interaction.

---

**kdenhartog** (2023-11-19):

+1 to what you’re proposing here as a step forward. I do think it would be useful to consider how this might work with multi tenant smart contract wallets too. In this case, I suspect we’ll need support for stating the index of the address as well which means we may also need an optional 4th parameter for indicating to the smart contract which index is granting this permission.

---

**danfinlay** (2023-11-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kdenhartog/48/7035_2.png) kdenhartog:

> I do think it would be useful to consider how this might work with multi tenant smart contract wallets too.

Is the type of multi-tenant account you’re talking about one where each account still has a unique address via a proxy, or no? If not, any link to standards related to addressing the latter type?

---

**kdenhartog** (2023-11-20):

Originally I wasn’t thinking about it in that way although an upgrade path to that would be incredibly useful (especially to prevent account freezing in the smart contract) at the tradeoff of the user managing their own smart contract/control their account more if they want.

Instead I’m thinking about it as a maps all the way down scenario.

E.g.

smart contact address maps to a “bank smart contract” which contains an individual identifier for each user called a bank account. Each user bank account then contains an identifier that maps to each session key. So, when user A with an EOA wants to send to user B who’s got a bank account they can send to smart contract identifier+bank account identifier kind of like how tradfi has a routing number and bank account number. When the smart contract receives the funds it updates the index of the user based on the identifier.

When user B wants to spend they can sign with any session key and submit to a bundler (probably hosted by the EOA wallet but not required). Each session key would map to an EOA account managed by the wallet and now we’ve effectively moved to a basic session key model with AA all managed by EOA wallet providers. The best part is because EOA wallets are helping to manage all this they can leverage their economies of scale to combine users transaction bundling in a way that incentivizes migration away from EOAs too.

The way in which you get more complex logic would be to use a proxy contract as you suggested. Originally I was just thinking all bank account get forced to use the same logic but that breaks a lot of the useful delegation primitives for no reason. If there’s a way we could just point to a single instance of a Authz validator contract that relies on state in the bank contract too then it would mean only a single instance needs to be deployed for everyone at the beginning and as users want their own bespoke Authz logic they can update over time. Alternatively the bank can also just update the default for users.

I’ve got to play catchup on some other work, so I’m hoping just writing about this for now is good enough for other people to understand until I can make a PoC to show what I mean by multi tenant wallets better.

---

**danfinlay** (2023-11-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kdenhartog/48/7035_2.png) kdenhartog:

> I’m thinking about it as a maps all the way down scenario.

I *think* my example interface could handle this situation:

```auto
function redeemDelegation(
    address onBehalfOf,
    TxParams calldata txParamsToCall,
    bytes authorization
) public;
```

In this scenario, any contract can implement the `redeemDelegation` method and allow an authorized `msg.sender` to submit its `bytes authorization` to it in order to send a transaction `onBehalfOf` another account. It doesn’t *really* matter if that other account is a proxy account, or some NFT held within the `onBehalfOf` contract, what matters is that by submitting a valid payload to an authorized & authorizing contract, a recipient is able to invoke some given `TxParams`.

---

**0xInuarashi** (2023-11-29):

in your vision, are functions of this interface intended to be single use (consume txdata, end) or are they moreso intended for some abstracted “allowance” functions ?

also im not sure how this would be uniquely more useful (in the instance where they are still single use transactions) than interpretting calldata into conversational language for users?

---

**danfinlay** (2023-11-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/0xinuarashi/48/8484_2.png) 0xInuarashi:

> in your vision, are functions of this interface intended to be single use (consume txdata, end) or are they moreso intended for some abstracted “allowance” functions ?

As abstracted allowance functions, because this can inherently also have call-count restrictions, making it work the other way if needed, making it more open ended, potentially supporting intent-style permissions.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/0xinuarashi/48/8484_2.png) 0xInuarashi:

> im not sure how this would be uniquely more useful (in the instance where they are still single use transactions) than interpretting calldata into conversational language for users?

These are two different approaches to achieving some kind of safety. A couple advantages to this interaction pattern are:

This approach doesn’t rely on disclosing any information to the site (like your account & tx history) before granting it relevant permissions, improving privacy and reducing cherry-picking phishing attacks.

Comprehending arbitrary bytecode is an inherently hard problem, and most modern solutions rely on introducing new centralized systems for helping analyze this potentially inscrutable data. These systems are prone to censorship and downtime, are not available to offline signers, and are not able to represent all kinds of actions that an application might want to perform on a user’s behalf. By inverting the order of proposals, the user is able to understand what they are putting at risk with potentially no external dependency, while still permitting the application to perform arbitrary actions on their behalf.

---

**0xInuarashi** (2023-11-30):

I see, great points!

In this flow, at what point and how, would the contract account approve the delegation and/or submit the delegation?

---

**MarkosHelp** (2023-12-07):

Fascinating proposal on the redeemDelegation interface for Ethereum wallet connections! I’m impressed with the idea of shifting the control of site connections back to the user, allowing for the issuance of session keys to dapps. The concept of varying authorization logic for contract accounts sounds promising for enhancing user-controlled and personalized authorization. The Powerbox/File-Picker model and AI/LLM-supported interactions are particularly intriguing. They seem to offer a more intuitive and user-friendly approach. This forward-thinking initiative could significantly reshape user interactions within the Ethereum ecosystem. Eager to see how this develops and the impact it will have!

---

**danfinlay** (2023-12-15):

Sorry for being so late, but here is the talk that introduced this pattern!: [Decoding the Enigma: A Model for Transaction Safety](https://app.streameth.org/devconnect/wallet_unconference/session/decoding_the_enigma_a_model_for_transaction_safety)

---

**danfinlay** (2023-12-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/0xinuarashi/48/8484_2.png) 0xInuarashi:

> In this flow, at what point and how, would the contract account approve the delegation and/or submit the delegation?

In response to a site initiating a request for some type of permission. The difference is the app would define its request by needs (not knowledge of the user), and the user would select appropriate permission on their side before returning a response.

---

**karandeep** (2023-12-21):

Here is a Proof of Concept (POC) that I did a week ago. You can view the demonstration video [Demo Video](https://www.loom.com/share/82da0751471c4cffb0cdbfff764c6b0b) and access the demo app [Demo App](https://zero-trust-basic-nft-dapp.vercel.app/).

It appears that this discussion revolves around a similar flow. The POC involves a complete client-side interaction, where the dapp interface requests permissions/scopes for the user’s account. The user then grants permissions based on their comfort level. This process creates a scoped session commitment on the blockchain, enabling the user to perform actions approved within that scope using the dapp interface.

I am interested in discussing this further if it aligns with the topic of conversation mentioned above.

---

**Praneeth** (2024-01-27):

Would it be possible same interface support things like closing out a session voluntarily (akin to course_notify) or maybe also a time-based one? Not sure if there might need to be more session state stored in the contract account related to user sessions.

---

**kopykat** (2024-02-03):

Very interesting discussion. How does the idea around redeeming delegation fit into existing smart contract accounts with a modular architecture, eg Safe, ZeroDevs Kernel or the Biconomy account? It seems like the modular approach to signature validation in these accounts tries to achieve a similar goal as the architecture described above.

---

**mcoso** (2024-02-21):

I think it could work quite well together. A specific plugin thats works with modular accounts could be created to support this extensible feature, redeem delegation. But whats good about generalizing the redeem delegation function is it doesn’t lock anyone into anything. Ex. it doesn’t force you to have a modular smart account

---

**tomarsachin2271** (2024-02-28):

Not able to access this link, can you please check. Link opens up this page

[![Screenshot 2024-02-29 at 12.28.51 AM](https://ethereum-magicians.org/uploads/default/optimized/2X/1/10c37702af95c2fe85f47ba7f6ca928bf3bae416_2_690x392.png)Screenshot 2024-02-29 at 12.28.51 AM2030×1156 104 KB](https://ethereum-magicians.org/uploads/default/10c37702af95c2fe85f47ba7f6ca928bf3bae416)

---

**bumblefudge** (2024-02-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tomarsachin2271/48/11205_2.png) tomarsachin2271:

> Not able to access this link, can you please check.

I think [this is the recording he means](https://streameth.org/watch?event=wallet_unconference&session=65b8f8d6a5b2d09b88ec192f), but his talk was broken up across multiple sessions, so it might make more sense to try multiple of them for full context (and Q&A):

https://streameth.org/devconnect/wallet_unconference

---

**danfinlay** (2024-03-12):

Thanks! Updated the OP.

---

**danfinlay** (2024-03-12):

This proposal is intended to provide a unified interface that can be exposed from any smart account, allowing us to advance towards a safer dapp-wallet connection while unimpeding the innovation of smart accounts.


*(14 more replies not shown)*
