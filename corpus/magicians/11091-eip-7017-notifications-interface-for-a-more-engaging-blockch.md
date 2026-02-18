---
source: magicians
topic_id: 11091
title: "EIP-7017: Notifications Interface for a more engaging blockchain"
author: Oli-art
date: "2022-09-28"
category: EIPs
tags: [erc]
url: https://ethereum-magicians.org/t/eip-7017-notifications-interface-for-a-more-engaging-blockchain/11091
views: 2537
likes: 4
posts_count: 22
---

# EIP-7017: Notifications Interface for a more engaging blockchain

# Introduction

With the adoption of web3 applications, an increasing necessity arises to be informed about certain events happening on-chain. Some examples include:

- DAO governance voting on important matters where member’s participation is fundamental.
- DEX informing about a certain price limit being reached, for example a stop-loss or a margin-call.
- An NFT marketplace informing an NFT owner about an offer being made to one of it’s NFTs.
- A metaverse informing about an important event.
- Warning about an ENS domain expiration date approaching.

Users are used to being informed, whether it be about news or updates of their favorite applications. As we are in a time of instant data feeds on social media, instant messaging apps and notifications of events that users care about, notifications are a feature in practically every application that exists in web2. They mostly come to email inboxes, SMSs, inside the applications, or in the notification inbox in the operating system.

If they would be taken away, the engagement on these web2 applications would sink. This is not different with web3 applications: users cannot be left in the dark about what is going on in them. Not only that, for some applications, all that matters is the participation of users on certain events, like governance on a DAO.

This whitepaper aims at proposing a decentralized approach to send and receive notifications from and to ethereum addresses, including smart contracts, in a private and easy way.

# The problem

There are a number of reasons why there isn’t a mainstream notification standard in ethereum and why it’s a lot harder than in web2 applications.

First, let’s list some facts about the nature of ethereum that put to evidence the difficulty of the matter:

- The owner of an address is unknown and no contact information comes with an ethereum address.
- The owner of an address is most of the time unwilling to link personal contact information on the blockchain because of reasons like security, taxation and spam.
- Everything that is published on the blockchain is completely public. Moreover, smart contracts don’t have private keys, so they can’t encrypt or decrypt data.

These are technical reasons that make it harder to do it than in web2. But it’s likely that the biggest reason relies elsewhere.

In web2, most of the user account’s are linked to an email address that is required at sign-up. This makes it easy to send notifications to specific users. This requires no further complexity. In web3, on the other hand, there is no obvious inbox to send notifications to. Every smart contract can define its own event’s to which one can listen to, but for each of them, a change has to be done in the frontend to listen to that specific contract and event structure. This poses a problem of coordination between smart contracts and web3 applications that can notify users.

The true challenge is coming up with a standard that is appealing to use and that dapps all over the ecosystem integrate.

# Solution

A definitive solution would need to overcome these problems without having to rely on a centralized party, as this would involve not only giving out personal information to that party, but trusting them with the notifications they send. It has to allow smart contracts and addresses to broadcast data to other addresses, and for the owner of the addresses to be able to subscribe to any notification sent to their address.

An approach that is both simple, decentralized and easy to implement is to use a notifications smart contract standard to be able to emit notifications to one address or broadcast them to anyone that wants to listen. Whitelists would record all addresses a user wants to allow receiving messages from. This is useful for direct messages from one address to another. Subscription lists would indicate which addresses they want to listen for general broadcasts. This is useful for receiving updates on a project.

The user should not be required to record its whitelist and subscription list on-chain. Anyone can emit notifications to anyone else and the filtering would occur off-chain on the front-end.

If a Smart Contract implements at least one of following events it would be a Notification Contract and, once deployed, it will be responsible for emitting notifications.

```auto
event DirectMsg (address indexed from, address indexed to, string subject, string body)
event BroadcastMsg (address indexed from, string subject, string body)
```

For the DirectMsg events, the contract shall also implement at least one of the following methods. These two functions differ only on the sender. In one, the sender is set as the address executing the function and in the second, as the address of the smart contract emitting the message:

```auto
function senderDirectMsg(address to, string memory subject, string memory body) public

function contractDirectMsg(address to, string memory subject, string memory body) public
```

The same applies to BroadcastMsg event, where the contract shall implement at least one of the following methods:

```auto
function senderBroadcastMsg(address to, string memory subject, string memory body) public

function contractBroadcastMsg(address to, string memory subject, string memory body) public
```

Here’s an example Notification smart contract:

```auto
pragma solidity ^0.8.7;

contract Notifications {

event directMsg(
address from,
address to,
string subject,
string body
);

event broadcastMsg(
address from,
string subject,
string body
);

/**
* @dev Send a notification to an address from the address executing the function
* @param to address to send a notification to
* @param subject subject of the message to send
* @param body body of the message to send
*/
function senderDirectMsg(address to, string memory subject, string memory body) public {
emit directMsg(msg.sender, to, subject, body);
}

/**
* @dev Send a notification to an address from the smart contract
* @param to address to send a notification to
* @param subject subject of the message to send
* @param body body of the message to send
*/
function contractDirectMsg(address to, string memory subject, string memory body) public {
emit directMsg(address(this), to, subject, body);
}

/**
* @dev Send a general notification from the address executing the function
* @param subject subject of the message to broadcast
* @param body body of the message to broadcast
*/
function senderBroadcastMsg(string memory subject, string memory body) public {
emit broadcastMsg(msg.sender, subject, body);
}

/**
* @dev Send a general notification from the address executing the function
* @param subject subject of the message to broadcast
* @param body body of the message to broadcast
*/
function contractBroadcastMsg(string memory subject, string memory body) public {
emit broadcastMsg(address(this), subject, body);
}
}
```

## Sending a notification

To send a notification to any address in ethereum, simply execute a DirectMsg event passing both the receiver, the subject and the message to it.

In case of a project, it may broadcast a message by using the broadcastMsg event. Here, all that is needed is the sender’s address, the message subject and the message body.

## Receiving notifications

To receive notifications we have to go off-chain, as the email services and phone notification centers are outside of it. But this doesn’t mean a centralized approach is necessary, nor that the identity of the user has to go public.

All that needs to be done is to set up a listener to the notifications smart contract and whenever a notification is sent to the address being listened to or broadcasted by an address one is subscribed to, the user gets notified. This is possible to do from any user interface or application. Appealing options are:

- Metamask wallet (in web-browser and mobile app)
- Email service
- In-app push notifications

As the notifications filter is set by the user off-chain, spam can easily be avoided with zero cost to the receiver, but >0 cost for the spammer.

## Encrypted notifications

Blockchains use asymmetric cryptography to operate. Without it, bitcoin could never have existed, as it is what allows users to have a secret and to be able to prove they own it without sharing their secret. What is important here is that asymmetric cryptography is available in ethereum and that we can make use of it for encrypting messages.

As some use cases of ethereum notifications may require privacy of data, this becomes useful.

As all messages are public, an easy way to send a message that is secret is to encrypt it using the receiver’s public key. Then, the receiver can simply decrypt it using its private key. This is what asymmetric cryptography was invented for.

Note that this use case only makes sense when the message is encrypted off-chain. That means that a smart contract could not generate the message since it can’t hold a secret. It should only emit the event holding the message, but it should come from a regular address.

## Integration in web3 applications

A user-friendly approach is for web3 applications to get users to add the app’s smart contract to its subscription list on a web browser plugin. This way, the user is listening to the web3 application smart contract whenever it makes an announcement.

Also, it can add it to its whitelist so that the contract can send a message informing about something specific to the user.

The web3 applications should talk with a browser extension that in turn can listen to the notification smart contract.

## How does it solve the problem?

Currently, in order to listen to the events in a smart contract, a programmer needs to develop a custom listener for the smart contract in question (unless it’s already standardized). This listener then can be integrated into different applications, but usually only if a big percentage of the app’s users needs the feature. Otherwise it doesn’t make sense to have it on the app. Listeners exist for example for token transactions, as they all adhere to a standard so it’s easy to implement for all of them at once.

In case of notifications, there is no easy way to alert a user about an important event.

With the solution presented an app would only need to integrate one update for it to be able to listen to any smart contract that the user needs to listen to. The user must not execute any transaction for this use case, only the sender has to. The cost for broadcasting a message is usually less than 1 dollar at current gas and eth prices and it can reach any number of users.

# A call to action

The solution presented in this whitepaper is likely not the best solution to the problem. Collaboration is what yields the best results. The best way to have collaboration and to deliver a standard to the ecosystem is to develop an Ethereum Improvement Proposal with the idea presented in this paper. The community shall present its veto here on the Ethereum Magicians Forum.

## Replies

**pxrv** (2022-09-29):

Working on a draft implementation

Could the body of the notification be bytes[] instead of string, allows for greater composabilty

---

**Oli-art** (2022-09-29):

Sure!

Thank you [@pxrv](/u/pxrv)

---

**pxrv** (2022-10-01):

The people at Push Protocol (aka EPNS) have designed a really good process around push notifications. You might want to check that out. It solves a lot of problems mentioned in your problem statement.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/oli-art/48/7322_2.png) Oli-art:

> The owner of an address is unknown and no contact information comes with an ethereum address.

The owner of the address is identified by the address itself. IMHP no other contact information should be necessary for sending notifs. The ERC standards should be made around base-cases. If any more contact information is required, thats a prerogative of the dapp itself.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/oli-art/48/7322_2.png) Oli-art:

> The owner of an address is most of the time unwilling to link personal contact information on the blockchain because of reasons like security, taxation and spam.

EPNS solves this problem by allowing users to approve notifications only from specific senders. This again is pseudo-anonymous so the only thing that needs to be disclosed is the address itself.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/oli-art/48/7322_2.png) Oli-art:

> Everything that is published on the blockchain is completely public. Moreover, smart contracts don’t have private keys, so they can’t encrypt or decrypt data.

After an admittedly cursory glance, I couldn’t find out if Push provides an encrypted notif service. This should be a trivial implementation though if reqd.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/oli-art/48/7322_2.png) Oli-art:

> In web3, on the other hand, there is no obvious inbox to send notifications to.

Standardizing a format for notifications (as mentioned in the title of the topic) doesn’t define where those notifications are sent. Push provides a browser extension, and IOS and android apps that act as an inbox for your notifications.

Building an app that forwards your Push notifications to an email would be an interesting side project - definitely not an EIP.

Happy building ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**Oli-art** (2022-10-01):

I looked at Push Protocol before writing the idea. I find it has several problems that make it more problematic than the EIP I’m proposing. This problems are:

1. Despite what they say, their protocol is not really decentralized, as described in their whitepaper. For example, to send a notification, you send a JSON to their API, which they can then pass over to the users that are listening. This is done off-chain and has no way to be verified. There has to be trust in the server running the protocol.
2. As described in “subscribing-to-channel” section of their whitepaper, their protocol requires subscribers to do a transaction in order to subscribe or unsubscribe. The lists are stored on-chain, which is something that isn’t necessary, as users could choose who to sisten from by doing a filter in the frontend.
3. To ease this problem, they decided to incentivize the subscribers by paying them for subscribing. This is a cost that goes to the entities emitting the messages, as they are required to stake DAI on behalf of the protocol. This is yet another cost to consider.
4. Sending and receiving notifications is not only costly, but involves a process that is unnecessarily tied to their servers. The processes involved are uneasy to implement. Sender’s can’t simply send a message from their smart contract at low cost, but they have to go to a DeFi protocol, create an account, stake DAI, develop a way to deliver the message to the protocol, etc. All of this with poor documentation and transparency.
5. As described in the governance section of their whitepaper, the protocol is not run by users. All decisions will be made by “the Company”. There is no actual governance mechanism in place.

I know I’m biased, but I hope this can be compared to the EIP approach. In my point of view, an ERC standard is what is needed here in order for any project, no matter how small, to implement notifications to it’s users, without extensive development, and in a way that is trustless and decentralized.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pxrv/48/7346_2.png) pxrv:

> Standardizing a format for notifications (as mentioned in the title of the topic) doesn’t define where those notifications are sent. Push provides a browser extension, and IOS and android apps that act as an inbox for your notifications.

This is true. I expect that as an ERC standard arises, wallets could implement it in an easy way, just as how I guess it happend with most of the standards. An EIP here would serve as a foundation for notification protocols, not as a way to deliver them to an inbox. I should keep inboxes out of the reach of the EIP tho, as it’s out of the scope of the EIP.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pxrv/48/7346_2.png) pxrv:

> Building an app that forwards your Push notifications to an email would be an interesting side project - definitely not an EIP.

True. This would be a cool side project. Emails are definitely not to be defined inside an EIP.

Do I edit the idea to include a refutation of Push Protocol and also to clarify the points you mentioned? I’m sorry for asking this. I’m kind of new around here.

Thank you very much for your help [@pxrv](/u/pxrv).

---

**Oli-art** (2022-11-11):

Here’s a draft ready for being submitted.

Please give it some feedback:

[Notification Standard - HackMD](https://hackmd.io/@8zBhFIYDTXyw8DcasfgT0g/SJkmDJTzj)

[@pxrv](/u/pxrv)

---

**wakqasahmed** (2023-03-21):

> As the notifications filter is set by the user off-chain, spam can easily be avoided with zero cost to the receiver, but >0 cost for the spammer.

There could be instances where publisher (sender/broadcaster) would like to send multiple notifications which could cost higher fees. Utilizing batching could save the gas fees in this scenario. Thereafter, it is up to the frontend clients to group them together by timestamp for user friendliness.



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-3074)





###



Allow externally owned accounts to delegate control to a contract.

---

**Oli-art** (2023-05-12):

Here is the EIP pull request (EIP-7017) on ethereum’s GitHub:

https://github.com/ethereum/EIPs/pull/7017

---

**Oli-art** (2023-05-26):

I think it’s time to define in greater detail how the body of a notification should be standarized. A good read to better understand what a notification needs in order to succesfully fulfill it’s function is this artice: [A Comprehensive Guide to Notification Design | Toptal®](https://www.toptal.com/designers/ux/notification-design)

Most of the topics are regarding frontend and content of the notifications, but a few questions came to my mind regarding `broadcastMsg` events:

- should there be a maximum size for the title and body so that frontend implementations can better accomodate them?
- Should notifications be classified by the three attention levels: high, medium, and low? (so frontends can differentiate between them with colors or where they show them)

Also, two other topics are important to mention:

- If we want notifications to have images, there should also be a standard as how to include them in the message.
- In case of DirectMsg events, they should have the option to be encrypted using the receiver’s public key. The front-end should then recognize this and ask for the receiver to decrypt the message in case it’s encrypted.

To solve all this topics, the body should be standarized, as it is an array of bytes. This is my suggestion for the body’s structure of a `broadcastMsg` event:

```auto
[
"0": "The message itself, a string, with a maximum size of X characters",
"1": "The attention level (1, 2 or 3)",
"2": "An image URI (optional)"
]
```

The maximum number of characters should of course be carfefully discussed based on common sizes used for notifications.

On the other hand, the `DirectMsg` events bodies could be standarized as follows:

```auto
[
"0": "The message itself, a string, with no maximum size",
"1": "Is encrypred (1 or 0)",
"2": "An image URI (optional)"
]
```

Would this be the best way to implement it? Or should the structure be defined as an event arguments instead of inside the body?

---

**Oli-art** (2023-06-17):

I have finally finished testing the protocol with the discord BOT. All functions but the encryption are tested. I also tried to impersonate Vitalik in a malitious contract implementing the event’s and have successfully blocked them in the service that listens to the events.

Also, I found a better way to structure the notifications while testing: having the subject included in the same field as the body. This is because when encrypting the message, you want to have it all encrypted together and inside the message field, with the image and the other data.

I have also added a transaction request as an option. This can be interpreted as a button in the wallets implementing the standard, or as a QR Code otherwise.

Here are the updated message structures:

For broadcasted messages:

```json
[
"0": "The subject of the message, a string, with a maximum size of 50 characters",
"1": "The body of the message, a string, with a maximum size of 300 characters",
"2": "The attention level (1, 2 or 3)",
"3": "An image URL (optional)"
"4": "A transaction request (optional, ERC-681 format)"
]
```

Here is an example:

```auto
[
    "This is an ERC-7017 message",
    "Hey! This is a message being broadcasted to show you how a contract implementing IERC-7017 can notify its users about an important event. Attached, there's an image of an ethereum unicorn and a request for you to send 1 ether to the null address.",
    0x02,
    "https://i.pinimg.com/originals/fc/a3/ee/fca3ee19c83bae8e558bcac23d150001.jpg",
    "ethereum:0x0000000000000000000000000000000000000000?value=1e18"
]
```

or in bytes[]:

```auto
[
    "0x5468697320697320616e204552432d37303137206d657373616765",
    "0x224865792120546869732069732061206d657373616765206265696e672062726f616463617374656420746f2073686f7720796f7520686f77206120636f6e747261637420696d706c656d656e74696e6720494552432d373031372063616e206e6f74696679206974732075736572732061626f757420616e20696d706f7274616e74206576656e742e2041747461636865642c207468657265277320616e20696d616765206f6620616e20657468657265756d20756e69636f726e20616e642061207265717565737420666f7220796f7520746f2073656e64203120657468657220746f20746865206e756c6c20616464726573732e",
    "0x02",
    "0x68747470733a2f2f692e70696e696d672e636f6d2f6f726967696e616c732f66632f61332f65652f66636133656531396338336261653865353538626361633233643135303030312e6a7067",
    "0x657468657265756d3a3078303030303030303030303030303030303030303030303030303030303030303030303030303030303f76616c75653d31653138"
]
```

For direct messages:

```json
[
"0": "The subject of the message, a string. No maximum size enforeced",
"1": "The body of the message. No maximum size enforeced",
"2": "An image URL (optional)"
"3": "A transaction request (optional, ERC-681 format)"
]
```

The events would be as follows, containing the described structures as the “message”:

```auto
/// @notice Send a direct message to an address.
    /// @dev `from` must be equal to either the smart contract address
    /// or msg.sender. `to` must not be the zero address.
    event DirectMsg (address indexed from, address indexed to, bytes[] message, bool is_encrypted);

    /// @notice Broadcast a message to a general public.
    /// @dev `from` parameter must be equal to either the smart contract address
    /// or msg.sender.
    event BroadcastMsg (address indexed from, bytes[] message);
```

---

**delbonis3** (2023-06-20):

This proposal is kinda poorly conceived.  It’s trying to overload addresses for a purpose well outside what they were designed for.  They work well as cryptographic identifiers *within* the context of the EVM but not *outside* of it.  This is partly manifest in how ERC-5630 is kinda a hack and requires that you must have initiated a transaction in order to reveal enough information to do a DH with them, since they’re *hashes* instead of pubkeys.  This also has the consequence that AA smart contract wallet addresses require another layer of hack to make work, requiring fairly involved cryptographic code be put on-chain that will never be *run* on-chain.  Which is probably part of why it’s not a finalized spec and isn’t implemented anywhere.

The root of the issue here is that you’re attempting to use the blockchain as a *messaging* layer when it’s designed for *settlement* operations.

There is a lot to critique about Push but some of the points you make in the EIP aren’t thought through all the way.  Your first point ignores the incentivization infrastructure that Push builds to ensure messages actually get delivered, but then in the third point acknowledge the incentive structure and say that the costs for this system would be too prohibitive, but then entirely ignoring the substantial Ethereum transaction costs that would be associated with *every message*.  You also argue in your second point that subscriptions shouldn’t be managed on-chain (they shouldn’t be), but then go on to propose that instead we *should* be using the chain for *message delivery* instead.

Just think about it realistically, a direct message under this design being a transaction means that every node on the network would have to be involved in that direct message.  This isn’t the first time that people have proposed designs like this, and it never goes anywhere since it’s always going to cost a lot *even with rollups* since they do not reduce DA costs.

Some more specific critiques:

> Note that only broadcasted messages have a maximum subject and body size. This is to facilitate notifications UX and UI, as this would be the main use of broadcasting messages: notifying users about stuff.
>
>
> As tho why 30 characters for the subject and 205 for the body, these are sizes that are long enough for informing a user about an event, but also fit inisde a standard desktop and mobile notification. Here’s an example for your intuition:

This is a bit of a strange restriction to make since it puts UI layer concerns very low down on the infrastructure.  Why even have separate subject and body fields in the container format?  If these messages would be ascii/utf8 in the first place, why not use `\n` or 0x1e (the “record separator”)?  Defining this in terms of characters instead of bytes also means that the cost bounds for using this protocol would depend on the language of the user.  It also implies that these strings would be pre-formatted on-chain, meaning that localization isn’t really possible.  Either that or contracts would have to have localization strings and know about the recipients *language*, which would also very bad for privacy.

The note about mobile notifications is a bit interesting since mobile OSes make heavy restriction on how push notification delivery can work.  Having Metamask running in the background long-pulling from Infura/etc isn’t something that can be made power efficiently and this spec would require a service to be running on a server somewhere that can integrate with the standard push notification delivery infra on whatever platform the user is running on.  This really weakens the “decentralization” value proposition of any design involving on-chain messaging.

> ```auto
> contract ERC7017 is IERC7017 {
> [...contract body...]
> }
> ```

(in the github eip doc)

Why are `walletDM` and `contractDM` separate functions in the first place?  Off-chain this can be inferred.  Same for `walletBroadcast` and `contractBroadcast`.  Why are these even being specified here instead of basing the spec entirely around the event log specification, which is what you’d be using to index the messages anyways?

---

What is the underlying desire for this kind of design?  If this is in service of a dapp you’re working on, why are you designing it to *only* rely on user addresses as the point of reference?  Have you considered approaches like Nostr or using existing chat systems like IRC or Matrix as messaging layers?  There are other projects that use these programmatically for apps to communicate, Matrix being especially interesting.  Have you considered a design where users use their address to attest to a list of identifiers for addresses on those systems which can then be served on BitTorrent/IPFS and/or gossiped?  If you are in a situation where you’re forced to rely on an address and can’t exchange information ahead of time (for some reason), have you considered designs using a contract merely as a *registry* for the above data which is emitted as a log?  Having more information about how you arrived on the design decisions in your proposal would be really important since as it stands it could not be a general purpose solution.

---

**Oli-art** (2023-06-20):

Thank you very much for your feedback [@delbonis3](/u/delbonis3). Here are my thoughts:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/delbonis3/48/9804_2.png) delbonis3:

> but then entirely ignoring the substantial Ethereum transaction costs that would be associated with every message

Here, the objective of DMs is to emit an event to a user when a certain trigger happens inside of a smart contract. So for example to facilitate a custom message to notify about a stop-loss being triggered. Since the contract is executing either way, the extra cost here is marginal, specially if this message is stored off-chain on a URI.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/delbonis3/48/9804_2.png) delbonis3:

> This is a bit of a strange restriction to make since it puts UI layer concerns very low down on the infrastructure. Why even have separate subject and body fields in the container format? If these messages would be ascii/utf8 in the first place, why not use \n or 0x1e (the “record separator”)? Defining this in terms of characters instead of bytes also means that the cost bounds for using this protocol would depend on the language of the user. It also implies that these strings would be pre-formatted on-chain, meaning that localization isn’t really possible. Either that or contracts would have to have localization strings and know about the recipients language, which would also very bad for privacy.

It is recomended to send a json in a URI and store it off-chain. This way it’s not a concern how big the strings are. This was a change, since previously it was specified as a bytes array and all the info was sent trough the chain.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/delbonis3/48/9804_2.png) delbonis3:

> The note about mobile notifications is a bit interesting since mobile OSes make heavy restriction on how push notification delivery can work. Having Metamask running in the background long-pulling from Infura/etc isn’t something that can be made power efficiently and this spec would require a service to be running on a server somewhere that can integrate with the standard push notification delivery infra on whatever platform the user is running on. This really weakens the “decentralization” value proposition of any design involving on-chain messaging.

This is true. I have managed to get it working using Quicknode and set it up to listen to the log topic of the event. Then it pushes the entire transaction to wherever I want. It even listens to different RPC-providers to not have to trust any of them alone. The most centralized part would be the service that the apps listen to for notifications. But just as an RPC-Provider, there doesn´t need to exist just one and I dont think it’s that different as how dApps get their info.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/delbonis3/48/9804_2.png) delbonis3:

> Why are walletDM and contractDM separate functions in the first place? Off-chain this can be inferred. Same for walletBroadcast and contractBroadcast. Why are these even being specified here instead of basing the spec entirely around the event log specification, which is what you’d be using to index the messages anyways?

This is not the specification it’s a reference implementation of how contracts would use the events. It could be deleted as well, since it’s not that relevant.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/delbonis3/48/9804_2.png) delbonis3:

> What is the underlying desire for this kind of design? If this is in service of a dapp you’re working on, why are you designing it to only rely on user addresses as the point of reference? Have you considered approaches like Nostr or using existing chat systems like IRC or Matrix as messaging layers? There are other projects that use these programmatically for apps to communicate, Matrix being especially interesting. Have you considered a design where users use their address to attest to a list of identifiers for addresses on those systems which can then be served on BitTorrent/IPFS and/or gossiped? If you are in a situation where you’re forced to rely on an address and can’t exchange information ahead of time (for some reason), have you considered designs using a contract merely as a registry for the above data which is emitted as a log? Having more information about how you arrived on the design decisions in your proposal would be really important since as it stands it could not be a general purpose solution.

I will be working on this and come back here. I didn’t quite know all of the solutions you mention.

---

**delbonis3** (2023-06-20):

> So for example to facilitate a custom message to notify about a stop-loss being triggered.

Sure, but why wouldn’t a `event StopLossTriggered(uint64 triggerId)` event not be entirely sufficient for this?  I don’t really see how that example is a justification for this design.

> It is recomended to send a json in a URI and store it off-chain.

But why is there even a need to have the URIs on-chain in the first place?  All of the behavior could be built into the user’s app and identify the activity they should be notifying the user about based entirely on what’s already there.  If the goal is communication between users via their instances of the app/client, there’s dozens of alternatives.

> I have managed to get it working using Quicknode and set it up to listen to the log topic of the event. Then it pushes the entire transaction to wherever I want. It even listens to different RPC-providers to not have to trust any of them alone. The most centralized part would be the service that the apps listen to for notifications. But just as an RPC-Provider, there doesn´t need to exist just one and I dont think it’s that different as how dApps get their info.

This is still a worse situation than how Push is planned to work if I understand it correctly, and reliant on the APIs of particular providers.  You might as well be using AWS to push out the notifications using the typical platform-specific push notification APIs.  This technique you’re describing here would work just as well for the `StopLossTriggered` example, and you could set up some scheme for making it entirely generic to the kind of event since once an event is identified and sent off to wake up the app service you can pull in whatever other data you need.

---

**Oli-art** (2023-06-20):

The issue here is specificity. There could be thosands of different types of notifications possible, each with their own event. Some of them can be specific to only one contract with a few users. It’s just not viable to have wallets or any other kind of app keep up with all the diversity of events. That’s why the standard comes in. If there is something to be notified to the user, it’s done trough this event. And all apps can understand it and have it be truly engaging, with images and even buttons.

There are other solutions like you said. The thing is when you compare web2 to web3, you need to be notified either on your mail or on the OS, but in one or two places, all apps in the same place. In web3 you don’t give your email, you’re usually on a web application with no way to notify the user to an inbox where it can manage them all. It’s all over the place. With this protocol, the app has the user’s address, and it will get it on the place it most wants to: email, cellphone, crypto wallet, discord…

As for the way I managed the events to notify the user, there can be a better way, of course. It can take a bit more work to implement a better solution. This was just a test (a discord BOT actually ![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=12))

---

**delbonis3** (2023-06-20):

> It’s just not viable to have wallets or any other kind of app keep up with all the diversity of events.  That’s why the standard comes in. If there is something to be notified to the user, it’s done trough this event.

But this is the part you don’t understand.  If the user receives a message from a smart contract they’ve never interacted with before, how should they even know how to interact with it?  Why should they care?  You’re going to say that the message would include the information, but why is it *the smart contract* that’s sending it to them?  Why aren’t you defining some spec for offchain delivery of messages.

If this is the use-case (contracts wanting to notify users that haven’t interacted with them before), why aren’t you defining some spec for a contract to declare information about itself *once*, like how to interpret its emitted event logs, that a Metamask instance can just programmatically process every other time it needs to without checking things on-chain?

Let’s look at it another way, if the contract emits an event log that the user already knows about and it / their Metamask client *already knows* how to interpret the event logs richly, then gas and log costs involved in writing the URI to an additional message event log are *entirely wasted* and they’ll never even inspect the log message.  But instead, the design spends gas on having thousands of computers have to keep a copy of the data around forever (until we have history expiry) which will never be looked at by the intended recipient in the first place.  For the `StopLossTriggered` example, this use-case *never* make sense since the user('s wallet) would already have to know about and interact with the smart contract to place the stop loss order in the first place.

> There are other solutions like you said. The thing is when you compare web2 to web3, you need to be notified either on your mail or on the OS, but in one or two places, all apps in the same place. In web3 you don’t give your email, you’re usually on a web application with no way to notify the user to an inbox where it can manage them all. It’s all over the place.

It seems like you’re defining “web2” and “web3” as being two entirely different worlds with no overlap and considering any technology that exists as being in only one of these two rigid boxes, and never neither or both.  There are better ways to accomplish what you’re describing, I gave you some that are decentralized (Matrix, IRC, XMPP, Nostr, etc.), there are others, with bridges to other platforms/protocols.

> With this protocol, the app has the user’s address, and it will get it on the place it most wants to: email, cellphone, crypto wallet, discord…

As I asked before, if *this* was the goal, why aren’t you proposing a way to integrate existing messaging infrastructure that can be integrated directly into the user’s Metamask client to provide to dapps and allow users to interact with each other and some way to attest to those identities/handles in other messaging systems with their addresses?  Email, SMS, Discord are *far* from ideal user interfaces for interacting with smart contracts, we have dedicated clients that provide better functionality for this, but it would work in that system.

The use-cases you’ve proposed don’t really make sense since there’s always alternatives or don’t match onto how these protocols are used in practice.  What is this *specifically* for and why don’t *any* of the alternatives work?  Why is this the single best solution despite the great cost that using this would have?

---

**Oli-art** (2023-06-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/delbonis3/48/9804_2.png) delbonis3:

> But this is the part you don’t understand. If the user receives a message from a smart contract they’ve never interacted with before, how should they even know how to interact with it?

What do you mean interact with it? The event log has a particular topic that matches the standard. If the contract implements it, then the event will get passed to a notification service.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/delbonis3/48/9804_2.png) delbonis3:

> If this is the use-case (contracts wanting to notify users that haven’t interacted with them before),

This is not the usecase. They can have interacted with them or not. But off-chain, they must declare their interest on this contract’s events. In case of DMs, it’s up to the app how to fiter them. They can filter out the untrusted / unverified contracts, unless they are whitelisted by the user.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/delbonis3/48/9804_2.png) delbonis3:

> Why should they care?

The user can subscribe to addresses in the client and only see the broadcasts from the addresses it cares about. In case the messages are directed to the user, there also exist whitelisting.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/delbonis3/48/9804_2.png) delbonis3:

> why aren’t you defining some spec for a contract to declare information about itself once, like how to interpret its emitted event logs

This is not that easy. How would a contract declare this? Also, this would be way more restrictful for the message, as it would allways have to have the same structure. What if you want to emit a notification about a unique event (like practically all broadcasting messages would)?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/delbonis3/48/9804_2.png) delbonis3:

> Let’s look at it another way, if the contract emits an event log that the user already knows about and it / their Metamask client already knows how to interpret the event logs richly, then gas and log costs involved in writing the URI to an additional message event log are entirely wasted and they’ll never even inspect the log message.

Yes, in the case metamask already interprets the event, like with erc-20 events, there is no need to implement this standard. Like I have explained, this is to address a diverse set of web3 applications with their specific functions.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/delbonis3/48/9804_2.png) delbonis3:

> As I asked before, if this was the goal, why aren’t you proposing a way to integrate existing messaging infrastructure that can be integrated directly into the user’s Metamask client to provide to dapps and allow users to interact with each other and some way to attest to those identities/handles in other messaging systems with their addresses?

I feel like I’m repeating myself over and over again. The focus here is far from just a messaging system to let users communicate between themselves, but a system to let CONTRACTS notify users in an engaging way (that even has the ability to request for on-chain actions). A contract must inform this IF and ONLY IF the conditions are met inside the contract. Doing this logic outside of the EVM is not ideal, as the notifications will not be liked in such a verifieable way to this conditions, different in every application.

---

**delbonis3** (2023-06-26):

There’s a lot here and it’s redundant to address specific replies to some points above, I’ll address the broader points that gets to the root of issues.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/oli-art/48/7322_2.png) Oli-art:

> This is not that easy. How would a contract declare this? Also, this would be way more restrictful for the message, as it would allways have to have the same structure. What if you want to emit a notification about a unique event (like practically all broadcasting messages would)?

It’s can be very easy.  Let’s say we define the spec such that the contract can emit an event  (maybe on creation, maybe when we upgrade a proxy, maybe on some other trigger) with some structure `AttestNotificationFormatter(string uri)` and anyone that wants to understant the event notification formatting can query it.  The URI would resolve (probably on IPFS) to some description of formatting rules, which could be some arbitrary format, but as a toy example we can structure it like this example:

```json
[
    {
        "event_signature": "StopLossTriggered(uint64 id)",
        "filter": "contract.getOrderData(event.id).address == wallet.address", // used to filter out events that aren't actually directed to the user, perhaps this should be in a more machine-readable format, this shouldn't be full javascript
        "icon": "ipfs://QmMyDappSomething/icon.ico",
        "title": "Stop-loss order triggered (My Dapp)",
        "message": "A stop-loss order for {{contract.getOrderData(event.id).amount}} {{contract.getOrderData(event.id).asset.symbol()}} was triggered.", // again, this could be a more machine-readable format
        "click": "ipfs://QmMyDappSomething/#order-{{event.id}}" // used to bring up the order in the dapp itself, which can display all the information the user might want to care about
    }
]
```

And then when a wallet interacts with a contract it can check if it ever emitted the formatter attestation event and, if it exists, would prompt the user if they want to register the notification handler for the events the contract might emit.  The user could go into the settings and remove the event handler from a list whenever they wanted to.  This is just an example to illustrate how it could function, a practical spec would be more thorough and precise about how the filtering and formatting should be specified.

But it gets better, the notification handler doesn’t even need to be specified on-chain.  As part of the web3 provider API there could be a method for dapps to register event notification handlers with the user’s wallet for particular contracts like the above without any involvement on-chain at all!  Or it could even be a `<meta/>` tag in the HTML structure instead of being a javascript API, which makes it even more machine readable.  It would satisfy all possible use-cases you’ve provided, *and* it would be able to be reused in different kinds of message passing systems like services that trigger unifiedpush notifications.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/oli-art/48/7322_2.png) Oli-art:

> I feel like I’m repeating myself over and over again. The focus here is far from just a messaging system to let users communicate between themselves, but a system to let CONTRACTS notify users in an engaging way (that even has the ability to request for on-chain actions). A contract must inform this IF and ONLY IF the conditions are met inside the contract.

You’re repeating yourself because you’re ignoring the core of the issue here.  **Blockchains are not messaging layers.**  Blockchains are for settlement.

Are you familiar with the OSI model of the internet protocol stack?

[![](https://ethereum-magicians.org/uploads/default/original/2X/8/802768010436929a923ac76c00b926ffdc83b5f3.jpeg)560×456 39.1 KB](https://ethereum-magicians.org/uploads/default/802768010436929a923ac76c00b926ffdc83b5f3)

If we wanted to map analogous roles for mechanisms in dapps/blockchains/etc into a model like this, we could think of smart contracts existing at the transport layer.  They’re built on top of a strong foundation (execution (EVM) → network, consensus (ethash, Casper) → data link, p2p network (devp2p, libp2p) → physical).  But just as humans don’t typically directly write bytes out over TCP, humans don’t typically directly interact with smart contracts.  There’s *always* some software in between that interprets the low-level machine data structures into a representation we can understand, and translating user actions back down to the low-level machine messages.  Notifications for users are very much an application-layer concern, since they’re specifically involved in the *human* interface, and the transport layer simply does not have the context or capability to cater to those needs.

What you’re describing in this EIP would be almost like if web servers also sent you a web browser when you loaded a page, so that your computer would know how to interpret the web page, just in case you didn’t already have one.  This is redundant because it’s wasting a lot of effort since most people already have the means to view web pages if they’re making web requests.

You’re taking a very spec-first way of designing specifications that ignores how well-designed smart contract systems actually are designed/build/used in practice.  You still haven’t (as far as I’ve seen) considered/addressed how the *costs* of using a messaging standard like this in a smart contract ought to be dealt with, and these kinds costs are why nobody builds smart contracts in this way.  The slight convenience of going about it this way are absolutely dominated over by how much it would cost to actually use, a cost that would likely have to be borne by users who would be turned off by the higher costs.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/oli-art/48/7322_2.png) Oli-art:

> Doing this logic outside of the EVM is not ideal, as the notifications will not be liked in such a verifieable way to this conditions, different in every application.

In what way is the current way of doing things not ideal?  How do we even define ideal?  Don’t presuppose that an ideal implementation of something *must* be using a blockchain.

People manage fairly well to support their use cases without a scheme like this.  What’s the issue with how this problem is currently solved?

---

**SamWilsn** (2023-09-20):

Fair warning: I haven’t read any of the previous conversation. That said, here are a few non-editorial related comments:

- If I understand Solidity (and it’s very likely I don’t), the name of the event is used in the log+bloom filter, while the name of the interface is not. Since Message is very likely to be used in unrelated smart contracts, this increases the amount of filtering client applications have to do. I might suggest a more unique/explicit event name?
- Does including from in the event make sense? The event will contain the emitting contract and transaction hash, so it’ll be trivial to retrieve that information. I doubt clients will be able to trust from at all anyway.
- Using a JSON blob on-chain is very expensive. I’d recommend using a URL only as the data field, preferably an IPFS link.
- Are “characters” supposed to be octets or unicode codepoints?

---

**wakqasahmed** (2023-10-01):

Would like to contribute to add some more use-cases.

- Any notification having CTA (Call to Action) e.g. claim certificates, message to collaborate on something anonymously, make yourself known to somebody for some reason (like for social recovery wallets, guardians contact each other in case of death of the funds holder) (Why we need wide adoption of social recovery wallets)

PR Raised: [Added more use cases by wakqasahmed · Pull Request #1 · Oli-art/EIPs · GitHub](https://github.com/Oli-art/EIPs/pull/1)

---

**Oli-art** (2023-12-08):

Thanks [@delbonis3](/u/delbonis3) for the idea.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/delbonis3/48/9804_2.png) delbonis3:

> It’s can be very easy. Let’s say we define the spec such that the contract can emit an event (maybe on creation, maybe when we upgrade a proxy, maybe on some other trigger) with some structure AttestNotificationFormatter(string uri) and anyone that wants to understant the event notification formatting can query it. The URI would resolve (probably on IPFS) to some description of formatting rules, which could be some arbitrary format, but as a toy example we can structure it like this example:

I can picture this working well in practice. At least for directed messages, this would be quite a useful approach. As for broadcasts for all interested users to listen to, I can picture a formatter with no filter and a message that is an URI so it can unique for every broadcast. For example: `"message": "ipfs://QmMyDappSomething/#message-{{event.id}}"`.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/delbonis3/48/9804_2.png) delbonis3:

> But it gets better, the notification handler doesn’t even need to be specified on-chain. As part of the web3 provider API there could be a method for dapps to register event notification handlers with the user’s wallet for particular contracts like the above without any involvement on-chain at all!

True! This is a great idea. As smart contracts are usually intereacted with from a web application, the description and formatting rules could be suggested by the apps. Then, when you receive the notification, it would include the web app url that suggested you use that formatting. The user should trust that app.

---

**Oli-art** (2023-12-08):

Thanks [@wakqasahmed](/u/wakqasahmed), loved that usecase idea!

I can’t access the vitalik.ca link. It seems like it’s no longer available, but I would like to read more about it.


*(1 more replies not shown)*
