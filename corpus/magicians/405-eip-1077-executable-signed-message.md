---
source: magicians
topic_id: 405
title: EIP-1077 Executable Signed Message
author: alexvandesande
date: "2018-05-18"
category: Web > User Experience
tags: [meta-transactions]
url: https://ethereum-magicians.org/t/eip-1077-executable-signed-message/405
views: 4589
likes: 23
posts_count: 16
---

# EIP-1077 Executable Signed Message

As part of the Executable Signed Message, I’ll be calling people that shown interest in this topic for these threads and want to debate specifics of the scheme…

I’ve updated the spec of [ERC1077](https://eips.ethereum.org/EIPS/eip-1077) based on feedback and conversations with the gnosis team. Right now, the best two references for executable signed messages are:

- Status Identity Gas Relay which has the ability to pay back in tokens
- Gnosis Safe Contract which has the ability to do delegateCall and create opcode, so a contract can be used to deploy a new contract.

I’ve added Gnosis Operation Type to the standard, so that it comprises both. A normal call is 0, so a contract that doesn’t want to support this option can simply leave it at 0.

I’ve also made a few modifications to make it EIP191 compatible, by request of Dan and Gnosis team and removed the nonce as timestamp thing, that was adding unnecessary complexity (feedback by [@arachnid](/u/arachnid)). I have replaced it by adding support for nonce 0 as a nonceless transaction which is more flexible for some cases but uses more memory.

### Topics to discuss:

- How do the multiple deployer parties communicate among each other, specially if you need multiple signatures before posting the message?
- If there is a competition among the deployers and multiple send at the same time, one or more will have their gas burned and incur in a cost which will increase the price of the service for everyone. Is there a way to create a cooperation among them to prevent this?
- How to create the initial contracts? There are some tricks that can be done to save gas cost, and there are some schemes where the user can already have an account address to send funds before deploying the contract, so you don’t need to deploy to inactive users
- What are the gas costs overhead of this scheme and how can we reduce them?

## Replies

**cooganb** (2018-05-18):

Hey all! I approached Alex about this project because we have a bunch of developers learning blockchain and we’re setting this up as a group project.

We’re going to start making a truffle box / npm package that can be used by smaller developers, first as a testnet POC to road-test and find the bumps along the way. Here’s what I’m imagining our first steps will be, open to any and all feedback:

1. Context-specific ether-less account, public-private keys created client-side — Built in React using Consensys LightWallet
2. Signs EIP-191 compliant transaction with newly-generated private key
3. Centralized server wraps up transaction in a relay transaction — (Probably absorbing the cost just for demo sake right now)
4. Centralized server uses factory pattern to deploy an erc-725 identity contract with relayed transaction from user to testnet

---

**alexvandesande** (2018-05-21):

EIP191 requires that messages be hash of these parameters:

`keccak256(byte(0x19), byte(0), from, whatever);`

The initial implementation (based on Status imp) asked the user to sign a string based on this:

`keccak256(byte(0x19), byte(0), from, callPrefix, to, value, dataHash, nonce, gasPrice, gasLimit, gasToken);`

But upon looking at Gnosis I also added OperationType:

`keccak256(byte(0x19), byte(0), from, callPrefix, to, value, dataHash, nonce, gasPrice, gasLimit, gasToken, operationType);`

In order to make it future proof, I suggest adding in the end of the hashes an extra parameter (maybe instead of operationType):

`keccak256(byte(0x19), byte(0), from, callPrefix, to, value, dataHash, nonce, gasPrice, gasLimit, gasToken, extra);`

The purpose of which would be basically making it more future proof.

On solidity, multiple parameters on Keccak are the equivalent of doing concatenation and then hashing… so `keccak256(requiredParam1, requiredParam2, extraParam1, extraParam2);` is the same hash as `keccak256(requiredParam1, requiredParam2, (extraParam1+extraParam2));`

This allows anyone to add any amount of parameters at the end of the message, and still make it compatible with previous implementations.

---

**alexvandesande** (2018-05-28):

In light of the last message, I’ve updated the standard to allow more flexibility in multiple implementations:



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/1120)














####


      `master` ← `alexvandesande:patch-6`




          opened 02:41PM - 28 May 18 UTC



          [![](https://avatars.githubusercontent.com/u/112898?v=4)
            alexvandesande](https://github.com/alexvandesande)



          [+20
            -6](https://github.com/ethereum/EIPs/pull/1120/files)







When opening a pull request to submit a new EIP, please use the suggested templa[…](https://github.com/ethereum/EIPs/pull/1120)te: https://github.com/ethereum/EIPs/blob/master/eip-X.md

We have a GitHub bot that automatically merges some PRs. It will merge yours immediately if certain criteria are met:

 - The PR edits only existing draft PRs.
 - The build passes.
 - Your Github username or email address is listed in the 'author' header of all affected PRs, inside <triangular brackets>.
 - If matching on email address, the email address is the one publicly listed on your GitHub profile.












Now some fields are optional if your contract doesn’t care for them, but if you ignore some fields, you must add an extra hash at the end to make yours compatible with other future implementations. While this thread isn’t getting a lot of attention, I’ve been having conversations via email, skype etc (and keep referring people back to this to keep this alive)

---

**pet3rpan** (2018-05-29):

[@alexvandesande](/u/alexvandesande) Replying to your ERC1077, you talk about user pain points and developer pain points.

I would like to add that, we should always be focusing on achieving the best user experience at all costs. (I assume we are talking about consumer facing applications) User pain points will need to be solved first (or items that drive business goals). Only once that those are satisfied, the developer pain points in creating the best experience should **then** be addressed. (not saying we shouldn’t think about them but just highlighting the priorities). We should be optimising for the development of great user experiences not just optimising for code to be pushed.

Product trade offs between ux and dev resources are a matter of economics and should be considered aside all together.

Take care when considering the user pain points and the developer pain points.

---

**juniset** (2018-05-29):

Hey All! Julien from Argent here.

We’ve been working on a Wallet with ETH less accounts for the past 6 months and are very excited to see some of these ideas being standardised.

One possible area of improvement that is not addressed by the current version is the possibility for the ‘key’ to be a smart contract itself. The use case is that of e.g. a recovery where User A with WalletA would like to authorise User B with WalletB do to a recovery on its Wallet. In that scenario the signed message would be signed with a key (say keyB) authorised to sign on behalf of WalletB, and WalletA needs to reconcile the signature by keyB with WalletB.

One possible solution is to use the ‘extra’ field to pass the address on behalf of which the message was signed, or add an additional parameter to the call.

---

**pet3rpan** (2018-05-29):

[@juniset](/u/juniset) So the private key would kinda be like beach ball where it is passed back and forth amongst the user dapps to sign transactions?

---

**pet3rpan** (2018-05-29):

Also [@everyone](/groups/everyone) here, what do you think about relying on emails for login / registration? Current systems depend on it for confirmation emails and account recovery. How can we transition people into using new mental models of dealing with signing things etc.

---

**alexvandesande** (2018-05-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pet3rpan/48/189_2.png) pet3rpan:

> We should be optimising for the development of great user experiences not just optimising for code to be pushed.

Could you be more specific? I generally agree with this sentiment, but most UX challenges are actually deeper than just skin deep and the purpose of this standard is to allow these challenges to be surmounted.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/juniset/48/632_2.png) juniset:

> One possible area of improvement that is not addressed by the current version is the possibility for the ‘key’ to be a smart contract itself. The use case is that of e.g. a recovery where User A with WalletA would like to authorise User B with WalletB do to a recovery on its Wallet. In that scenario the signed message would be signed with a key (say keyB) authorised to sign on behalf of WalletB, and WalletA needs to reconcile the signature by keyB with WalletB.

Juni, you don’t need the key to be a smart contract for that. Both Gnosis and Status are doing social recovery keys, where you authorize X users to reset your wallet. The way to do that is that Wallet A, when doing a recovery process, can check if key B that signed the message, is authorized to do so by wallet B. No need to complicate things.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pet3rpan/48/189_2.png) pet3rpan:

> So the private key would kinda be like beach ball where it is passed back and forth amongst the user dapps to sign transactions?

Yes, that’s the idea.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pet3rpan/48/189_2.png) pet3rpan:

> what do you think about relying on emails for login / registration?

Emails are centralized services. I think one way in which one can use email is actually to add a “central recovery key” option, in which users from company A say they trust keys from company A to reset their keys. That interaction and recovery request can be done via email, and the company can confirm their identity by email.

Of course, as soon as users have enough devices on the system so that they are effectively multisig, they should switch recovery options.

---

**pet3rpan** (2018-05-30):

Another thought I had: How we design these systems and user experiences will change along with cheaper gas execution costs. While it may cost $5 in gas fees to claim an ens or execute a smart contract, it might cost fractions of a cent in the future. Along with this shift, people’s attitudes towards signing transactions might change.

Ether and gas might fade into the background just like internet data. Earlier on, internet data was way more expensive and you paid a monthly subscription for say 15gigabites of data. With expensive data and a low total bandwith, streaming a movie or playing a 2hr youtube video had be a careful consideration. This is the opposite today where we hardly care as much, we use data more liberally and don’t monitor data usages.

Just some food for thought

---

**alexvandesande** (2018-05-30):

> How we design these systems and user experiences will change along with cheaper gas execution costs

Good point. We design a lot of things today trying to optmize for cheaper gas. The big drawback of this signed approach is that it might end up in more costly transactions (need to benchmark how much) but it might not matter in the long term

---

**cooganb** (2018-05-30):

Hey all! Students at Hatch worked on a very basic way to generate Ethereum addresses and keys without passwords, seed phrases, etc., store them locally and use them to sign messages. We’re hoping to build-out the Solidity side to take notes from Gnosis Identity Relay contract.

It’s a very simple implementation, but we’re hoping to continue working on it (after some great input from [@alexvandesande](/u/alexvandesande) yesterday!) and wrap it up as an npm package or truffle box. Please check out the repo link! Comment, PR, etc. etc.



      [github.com](https://github.com/HatchCrypto/unilogin)




  ![image](https://opengraph.githubassets.com/484574a967c15976a27164703e129cc5/HatchCrypto/unilogin)



###



Signup / Login Design Pattern with Minimal Ethereum Front-End Schema










Please note: These are front-end developers who have learned blockchain concepts & practices over the past five weeks. This was done in a mini-sprint that lasted about a day and half culminating in Alex’s visit!

---

**cooganb** (2018-08-07):

I know this thread has been quiet, but I wanted to post another project here:

https://github.com/austintgriffith/bouncer-proxy

Austin has built a nice working demonstration of transaction forwarding (a concept I’ve found tricky to explain to students) with a nice UI (which we all love!). I’m going to try and work with him on getting it to EIP-1077 standards, notably getting ERC-191 signed message parameters into the workflow.

---

**jpitts** (2018-09-02):

FYI, I created a link page of projects relating to meta transactions: https://github.com/jpitts/eth-community-discussions/blob/master/meta-transactions.md

---

**cooganb** (2018-09-05):

This is amazing! Thank you.

---

**cooganb** (2018-10-23):

Gave a talk yesterday for 8btc and hyped meta-transactions & universal login. It was written up here (in Mandarin), linked to repos at the bottom!

https://m.8btc.com/article/296078

