---
source: magicians
topic_id: 364
title: "ERC-1080: RecoverableToken Standard"
author: bradleat
date: "2018-05-15"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/erc-1080-recoverabletoken-standard/364
views: 5387
likes: 4
posts_count: 14
---

# ERC-1080: RecoverableToken Standard

I created [ERC-1080](https://github.com/bradleat/EIPs/blob/master/EIPS/eip-1080.md) to start a conversation about a token standard that allows for users to dispute transfers, report and recover lost accounts, and find appropriate resolution in the case of account theft.

With reference to [ERC-792](https://github.com/ethereum/EIPs/issues/792), it is possible to construct a decentralized arbitration system on the Ethereum application layer. This means that this standard can be complemented with such a system or otherwise.

This is very much a draft, I welcome any feedback or suggestions to improve this standard.

## Replies

**jamslevy** (2018-05-17):

[@bradleat](/u/bradleat) thanks for putting up this up. This topic is one that is of great interest to me.

First off, IMO it is a mistake to initially include chargebacks in the scope. By definition chargebacks involve two parties making somewhat valid claims (more so than theft for example) and the only reason that credit cards can handle chargebacks is because they charge payment fees and make money from interest rates. Just my two cents on that.

It seems like the most important part of ERC-1080 is missing, which is the actual manipulation of balances once a claim is approved. I’ve given some thought about how to best do this. First, there is bound to be attempts at fraud, and fraud/abuse is more difficult when the process is slow. So I’d make the default be that this process of recovering funds needs to take a while to complete and tokens can configure that differently if they want.

It’s important to also notify any potential parties involved, so part of this process could be to first send at least one and possibly more transactions with no value to the addresses involved with encoded data message notifying them of the situation and linking to a claim ticket where they can make a counter claim. They would need to show ownership of the address involved so you don’t have random people making these counter claims.

Also instead of changing the balance all at once, it would be best to first start deducting very small amounts over time such as a certain amount per day, and then possibly to increase the amount deducted but to cap these amounts so that in the event of a very large claim, the process will take a long time to complete, which is meant to deter attempts at fraud and the possibility of successful fraud. There could potentially be some ways to increase this rate, such as providing documentation that meets a higher tier of evidence.

You’d also want to audit the process to make sure that at no time will there be the ability for someone to game the process for a net increase in tokens, such as somebody pretending to have lost their key and attempting to move their funds during the recovery process and take advantage of a race condition such that they end up with more tokens than they started with. At all times there should be no net increase in tokens.

Also there is the possibility of the token taking a fee, particularly for the manual arbitration aspect. A reasonable default would be anywhere from 2-5% of the recovered tokens. This helps to fund the arbitration and also to deter abuse of the system, especially if the fee needs to be paid upfront with the claim.

I’d be happy to help with implementing any of what is described above.

---

**bradleat** (2018-05-18):

Thanks for the feedback. I’d appreciate the help in getting an implementation built.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jamslevy/48/232_2.png) jamslevy:

> First off, IMO it is a mistake to initially include chargebacks in the scope. By definition chargebacks involve two parties making somewhat valid claims (more so than theft for example) and the only reason that credit cards can handle chargebacks is because they charge payment fees and make money from interest rates. Just my two cents on that.

A chargeback for the purposes of the proposal is to allow for the recovery tokens sent to the wrong address, but also for dealing with more complex issues such as getting money back if some item purchased was never delivered. However, this is up to the implementer and the arbitration agreement used.

Perhaps a different name would be better here.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jamslevy/48/232_2.png) jamslevy:

> It’s important to also notify any potential parties involved, so part of this process could be to first send at least one and possibly more transactions with no value to the addresses involved with encoded data message notifying them of the situation and linking to a claim ticket where they can make a counter claim.

The events are meant to allow the parties involved to receive notifications.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jamslevy/48/232_2.png) jamslevy:

> They would need to show ownership of the address involved so you don’t have random people making these counter claims.

What situation are you talking about? Stolen account or a lost account?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jamslevy/48/232_2.png) jamslevy:

> Also instead of changing the balance all at once, it would be best to first start deducting very small amounts over time such as a certain amount per day, and then possibly to increase the amount deducted but to cap these amounts so that in the event of a very large claim, the process will take a long time to complete, which is meant to deter attempts at fraud and the possibility of successful fraud. There could potentially be some ways to increase this rate, such as providing documentation that meets a higher tier of evidence.

Is this for lost or stolen accounts? I wonder if this is an implementation detail that should be left to the arbitration or resolution mechanism involved.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jamslevy/48/232_2.png) jamslevy:

> You’d also want to audit the process to make sure that at no time will there be the ability for someone to game the process for a net increase in tokens, such as somebody pretending to have lost their key and attempting to move their funds during the recovery process and take advantage of a race condition such that they end up with more tokens than they started with. At all times there should be no net increase in tokens.

For sure.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jamslevy/48/232_2.png) jamslevy:

> Also there is the possibility of the token taking a fee, particularly for the manual arbitration aspect. A reasonable default would be anywhere from 2-5% of the recovered tokens. This helps to fund the arbitration and also to deter abuse of the system, especially if the fee needs to be paid upfront with the claim.

For sure.

Perhaps making the functions that start disputes `payable` would allow for this fee for to be taken.

I think we’ll know more about what we need when we start an implementation.

I see the first step as writing an implementation that basically has a “GOD” address which is able to resolve disputes in any fashion it wants. At this point in time it might makes sense to add some dispute resolution functions to the proposal itself.

The next step would be to utilize a decentralized arbitration process (something like ERC-792) to write another implementation. This will also inform the proposal.

---

**jamslevy** (2018-05-20):

> What situation are you talking about? Stolen account or a lost account?

If I lost my private keys, I need some way to show that I did lose my private key and am not trying to steal funds from someone else. Fraud is the challenge for recovering tokens.

> I wonder if this is an implementation detail that should be left to the arbitration or resolution mechanism involved.

My preference is for very reasonable conventions, with the possibility of configuration. This allows contract owners to do what they want, but doesn’t require them to do so. In terms of what the conventions are, I’d opt for defaults that aim to eliminate fraud and abuse, at the expense of very quick recovery.

---

**bradleat** (2018-05-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jamslevy/48/232_2.png) jamslevy:

> If I lost my private keys, I need some way to show that I did lose my private key and am not trying to steal funds from someone else. Fraud is the challenge for recovering tokens.

So the interface basically allows anyone to make a claim on an account as being lost.

The first test to pass is that the account actually is lost. That’s why the accounts have a configurable amount of time for someone to basically do anything else with the account to override its status as being lost. The second test is the arbitration or the human factor. The standard say that the implementer MUST provider a resolution mechanism.

There is a different standard process for theft and for chargebacks (reversals).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jamslevy/48/232_2.png) jamslevy:

> My preference is for very reasonable conventions, with the possibility of configuration. This allows contract owners to do what they want, but doesn’t require them to do so. In terms of what the conventions are, I’d opt for defaults that aim to eliminate fraud and abuse, at the expense of very quick recovery.

I think we’ll know more about the conventions if we start to build a RecoverableToken.

---

**TheRedWizard** (2018-05-22):

Charge back should work as following

payments have a time window in which they can be disputed. during this window the transfer is in a pending state (This allows off chain legal systems to see intent).  If a payment is disputed in the window payment is then in a disputed state and no-one owns the money.

This can be resolved in a few ways

Both sides can agree to a resolution, (payment is cancelled, payment is split (a partial chargeback), or the payment goes through).

Both sides can agree to a 3rd party arbitrator, they both grant a third account the right to resolve the payment (this mechanism will have to be added to the interface).

If neither parties can agree to a resolution, and an arbitrator is not chosen within a certain window (a year maybe, shorter?, configurable?) then default resolution should occur.

If the payment is only disputed by the payer, and the other side does nothing, the payment is cancelled (obv).  This solves the problem of sending to non-existing / accidental accounts.

User’s can accept a default arbitrator, these can be provided by anyone implementing the interface.  This could be any off chain service or 3rd party that is mutually agreed upon, and maybe existing law firms / arbitration companies can offer this as a service.

---

**MicahZoltu** (2018-05-22):

Claim lost can be handled by a smart wallet, and such a smart wallet can work for *any* token or ETH which (IMO) makes it a strictly better solution.  In fact, I actually have a smart wallet that does this already (it just doesn’t have a UI, hence no one uses it but me).  I recommend removing that from this EIP and having this one focus on theft resolution.

---

**jamslevy** (2018-05-22):

Does this smart wallet use a CLI? it woukd be good to have people adopt these solutions, likely not mutually exclusive with this ERC

---

**MicahZoltu** (2018-05-22):

Nope, just a smart contract deployed to mainnet.  I actually don’t remember the address the factory is deployed at as I have only bookmarked my instance of the wallet (probably easier to just redeploy it yourself anyway): https://github.com/Zoltu/recoverable-wallet/blob/master/contracts/recoverable-wallet.sol

Note: Wallet needs to be updated to support some of the new token standards.  It also probably *should* be updated to support arbitrary contract calls (would help people who accidentally transfer ownership of goods the contract doesn’t natively understand to it).

Note2: It also should be audited professionally.  ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

---

**bradleat** (2018-05-22):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/m/958977/48.png) MicahZoltu:

> In fact, I actually have a smart wallet that does this already (it just doesn’t have a UI, hence no one uses it but me).  I recommend removing that from this EIP and having this one focus on theft resolution.

After some more thinking, I think there is a way to make the lost and theft resolution process the same thing. In either case I think that having a standard for how these processes can work is a good thing.

I’ll write up the thought soon.

---

**bradleat** (2018-06-08):

If we allow other contracts to be delegated permission for transferring an account to another address, we get theft and lost account recovery mechanisms.

This means that at account setup (and other times with a time delay), a user can give other accounts weight in a vote to decide if their account was stolen or lost and to select a new controlling account.

These accounts could be cold storage wallets, some bonded commercial services, governments, some interesting contract.

An interesting idea would to also allow undeployed contracts with known hashes to be selected as a delegate.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/t/ac91a4/48.png) TheRedWizard:

> Charge back should work as following
>
>
> payments have a time window in which they can be disputed. during this window the transfer is in a pending state (This allows off chain legal systems to see intent).  If a payment is disputed in the window payment is then in a disputed state and no-one owns the money.

Sounds good. I guess the dispute resolution process owns the money.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/t/ac91a4/48.png) TheRedWizard:

> This can be resolved in a few ways
>
>
> Both sides can agree to a resolution, (payment is cancelled, payment is split (a partial chargeback), or the payment goes through).

So without arbitration both sides can just agree to something? Perhaps its better to just wrap this in an arbitration agreement to save the complication.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/t/ac91a4/48.png) TheRedWizard:

> Both sides can agree to a 3rd party arbitrator, they both grant a third account the right to resolve the payment (this mechanism will have to be added to the interface).
>
>
> If neither parties can agree to a resolution, and an arbitrator is not chosen within a certain window (a year maybe, shorter?, configurable?) then default resolution should occur.

This part is very important to the game of it all.

I think it makes sense for there to be a payment/fee to propose arbiters that is only taken if both sides do not propose an intersecting arbiters list. This ensures there is something at stake. Moreover, it creates a cost for buy side or sell side scamming.

How the fees are set should be a topic of research. More fees less scams, but more expensive recoveries. What is the optimal point for this tradeoff?

The default resolution should be to wait for the two parties to propose an intersecting arbiter list.

Another idea would be to allow accounts to precommit to arbiters during setup. This would allow signaling around trusted arbiters to develop.

**Account property setup and modification rules will be very important.** Modifications to the initial setup obviously cannot take place immediately. They will probably have to be delayed by the length of the rule they replace. For instance, if I say my account transfers are pending for 1 week, any change to this property cannot clear for at least one week.

On that specific point, I think allowing individual transfers to opt for pending times longer than the default length is an interesting feature. It allows for escrow. Keeping with the theme of per-transaction settings, overriding the list of default arbiters for a particular transfer is interesting. However, it makes the next point very important:

**The intersection of chargebacks and stolen accounts is particularly sensitive**

I would say that if an account is stolen or lost, resolution of that process takes precedence over chargeback resolution. The chargeback will then be resolved with the arbiters set by the new owner of the account.

That means a thief cannot steal an account and select friendly arbiters to recover the funds. The new account will have the ability to select the arbiters used for the resolution. It does allow a thief to lock money of stolen accounts into the default resolution process for arbiter selection. However, it will cost the thief money (if we follow the rule that selecting non-intersecting arbiter groups costs money).

*Perhaps in addition to a default amount or rate, any party (or just the sender) should be able to increase the fee of selecting an arbiter group for chargebacks up to the amount of the transaction*

---

**satyamakgec** (2018-08-07):

This EIP is very much needed but specifically for the case when the user lost its private key of wallet then how do you think to verify the ownership of the account when the user is claiming the lost of wallet ? This is the major challenge I am thinking to implement this EIP.

---

**bradleat** (2018-08-15):

I am close to have an updated spec made. I’ll post the update here when I have it.

---

**bradleat** (2021-02-04):

It’s been awhile, but if anyone is interested on discussing the chargeback portion of this standard please see the following thread:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/bradleat/48/216_2.png)
    [Chargeback Tokens](https://ethereum-magicians.org/t/chargeback-tokens/5292) [Primordial Soup](/c/primordial-soup/9)



> Awhile ago I submitted an EIP for a Recoverable Token Standard, but it appears that since then this issue has been better addressed by wallets such as Argent or Gnosis Safe.
> Building on this work, I was motivated to solve the other part of the EIP which was dealing with a standard for chargebacks. This concept will be important for users who wish to spend their tokens (such as DAI) in exchange for goods or services that they fear may not be delivered.
> The basic concept is that we create a virt…

