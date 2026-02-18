---
source: magicians
topic_id: 351
title: "ERC-1077 and ERC-1078: The magic of executable signed messages to login and do actions"
author: alexvandesande
date: "2018-05-14"
category: EIPs
tags: [ux, meta-transactions]
url: https://ethereum-magicians.org/t/erc-1077-and-erc-1078-the-magic-of-executable-signed-messages-to-login-and-do-actions/351
views: 15075
likes: 23
posts_count: 28
---

# ERC-1077 and ERC-1078: The magic of executable signed messages to login and do actions

These are two ERCs that I talked about on my talk at UX Unconf:

  [![image](https://img.youtube.com/vi/qF2lhJzngto/maxresdefault.jpg)](https://www.youtube.com/watch?v=qF2lhJzngto&t=113s)



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/1077)














####


      `master` ← `alexvandesande:patch-5`




          opened 03:16PM - 14 May 18 UTC



          [![](https://avatars.githubusercontent.com/u/112898?v=4)
            alexvandesande](https://github.com/alexvandesande)



          [+190
            -0](https://github.com/ethereum/EIPs/pull/1077/files)







Allowing users to sign messages to show intent of execution, but allowing a thir[…](https://github.com/ethereum/EIPs/pull/1077)d party relayer to execute them is an emerging pattern being used in many projects. Standardizing a common format for them, as well as a way in which the user allows the transaction to be paid in tokens, gives app developers a lot of flexibility and can become the main way in which app users interact with the Blockchain.

* [Ethereum Magician's discussion](https://ethereum-magicians.org/t/erc1077-and-1078-the-magic-of-executable-signed-messages-to-login-and-do-actions/351)
* [Talk introducing this at UX Unconf Toronto](https://www.youtube.com/watch?v=qF2lhJzngto)














      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/1078)














####


      `master` ← `alexvandesande:patch-6`




          opened 03:17PM - 14 May 18 UTC



          [![](https://avatars.githubusercontent.com/u/112898?v=4)
            alexvandesande](https://github.com/alexvandesande)



          [+121
            -0](https://github.com/ethereum/EIPs/pull/1078/files)







This presents a method to replace the usual signup/login design pattern with a m[…](https://github.com/ethereum/EIPs/pull/1078)inimal ethereum native scheme, that doesn’t require passwords, backing up private keys nor typing seed phrases. From the user point of view it will be very similar to patterns they’re already used to with second factor authentication (without relying in a central server), but for dapp developers it requires a new way to think about ethereum transactions.

* [Ethereum Magician's discussion](https://ethereum-magicians.org/t/erc1077-and-1078-the-magic-of-executable-signed-messages-to-login-and-do-actions/351)
* [Talk introducing this at UX Unconf Toronto](https://www.youtube.com/watch?v=qF2lhJzngto)












Would love to get feedback. Let’s have this page for general feedback on all proposals, but I suggest making EIP specific feedback direclrty as GitHub comments so that I can address them line by line and change if needed

## Replies

**ricburton** (2018-05-14):

Can we learn something from the way the Gnosis Safe is implemented?



      [github.com](https://github.com/safe-global/safe-smart-account)




  ![image](https://opengraph.githubassets.com/d4ec70d0e80c84d52a5652017fe44952/safe-global/safe-smart-account)



###



Safe allows secure management of blockchain assets.

---

**alexvandesande** (2018-05-14):

Also, uport:

- uPort Meta transactions
- uPort safe Identities

Going to add these to examples

---

**boris** (2018-05-15):

As I said in the room, I don’t see log in / signup using ENS subdomains being any easier than the implementation of OpenID.

The big issue in practice that training users that they could re-use their login proved very hard.

Some users hosted their own OpenID on their own domain. But was essentially a small niche / expert usage only.

Mastodon uses a similar scheme, user@mastodonserver.domain. It’s a very similar use case – one mastodon network ID can be used to login to any other network – if that network allows signups and hasn’t blacklisted the other ID. We might learn from their experiences.

I also see this described flow going to one user owned contract? So there would be extreme correlation of activities. [@alexvandesande](/u/alexvandesande) do you have any thoughts on this issue?

---

**alexvandesande** (2018-05-15):

> The big issue in practice that training users that they could re-use their login proved very hard.

That’s an interesting UX challenge, but I would say that it would be better than the current scheme, which is very user unfriendly. I would say that in order to train users, we should treat the identity like your email. Users are used on using emails as their login, but they usually have to signup or login a new one, which is usually the bad experience of accidentally clicking on the wrong link and then it tells you you can’t login because you already have signed up, and then you have to click signup, type your email **again** and then type a few wrong passwords a few times, until you click forgot password, check your email, see no email was there, check spam messages, check email again, check facebook and forget about it.

Instead, the right interface would be to whenever the user types a name, check if it exists and then use that to give them the option to create a new one or connect to the existing one.

And the big difference is that you don’t need to run your own server, all is on the blockchain. Also, even if you use an app to create an identity and ens login, you are its owner and you can later always register your own name and attach it to it.

> I also see this described flow going to one user owned contract? So there would be extreme correlation of activities. @alexvandesande do you have any thoughts on this issue?

I agree privacy is an open issue we need to think about more solutions. I would imagine that we could for instance, allow the identity to, instead of listing the keys directly, they could list a merkle hash of a list of keys, and then use one of  these keys to move funds in a private coin, therefore enabling privacy.

---

**boris** (2018-05-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/alexvandesande/48/101_2.png) alexvandesande:

> I would say that in order to train users, we should treat the identity like your email.

Again, this was exactly how OpenID was suggested. An identifier that looks a bit like email but isn’t email.

Let’s just say that I’m not confident that ENS subdomains is a usable solution.

I don’t think it’s a bad idea, but I don’t think it’s THE solution that should suck up a lot of energy.

---

**Arachnid** (2018-05-17):

RE 1077 - why not make the signing standard [EIP191](https://eips.ethereum.org/EIPS/eip-191) compatible?

The multipurpose nature of the nonce field seems like a bad idea to me, too. Either pick a new timestamp-based scheme or stick with nonces; trying to overload one field for two purposes seems like unnecessary complexity.

---

**alexvandesande** (2018-05-17):

> RE 1077 - why not make the signing standard EIP191 compatible?

EIP191 is a general signing standard for any data. This proposes a specific set for Executable messages. It should be compatible with 191 as a subset of the more general scheme. (**edit: after re-reading and understanding 191, I will update my ERC to be compatible)

> The multipurpose nature of the nonce field seems like a bad idea to me, too. Either pick a new timestamp-based scheme or stick with nonces; trying to overload one field for two purposes seems like unnecessary complexity.

Fair criticism. I find it useful for some smaller cases: specially because if you signing things that can only be executed in the future, then you cannot sign any new transactions, which might be bad for all sorts of state channel applications. But maybe this is only useful in specific use cases: another more general solution would be to treat “nonce 0” as a flag to ignore nonces and just save the hash of the TX as “executed” and to add the timestamp permission elsewhere in another layer as part of a more general permission scheme.

---

**cwgoes** (2018-05-28):

Executable signed messages are definitely a step in the right direction, but I think we can further generalize this concept. I think a prototypical Ethereum user doesn’t really want to think about *individual* transactions at all - rather, they want to think about *sets* of authorized and unauthorized *state transitions*.

Some examples:

1. I would like to transfer 1 Ether to my friend to pay for dinner, once, now.
2. I would like to transfer 100 DAI to my son next Tuesday, only if his account balance is below 10 DAI, as allowance for dinner with his friends.
3. I would like to authorize my phone to spend Ether from my main account, but only up to 2 Ether per week, in case it gets stolen.
4. I would like to authorize CryptoKitties to transfer 0.1 Ether per month from my account for a “CryptoKitty-of-the-month” promotion, until I cancel this subscription.
5. I would like to only allow transfers of more than 5 Ether if I authorize the transfer from both my laptop and my phone.

Of these, (1) can be done with an Ethereum transaction (or an executable signed message). (2), (3), (4), and (5) require writing custom contracts and complex key management (and are thus beyond the reach of ordinary users).

Not only do I want to separate the notion of transaction “signer” from transaction “deployer”, I want to separate the notion of “transaction” from “state transitions” - I want the ability to, with one signature, authorize an arbitrary, possibly infinite, set of well-specified state transitions.

This can be done by allowing a user to specify some function `v` (for “validate”), which can authorize or reject transactions on the basis of chain state, transaction details, signee(s), and current time.

For each of these examples, this function would do roughly the following:

1. Check the amount, signature, and a nonce/hash for replay protection.
2. Check the timestamp, my son’s account balance, and a nonce/hash for replay protection.
3. Check the signee (key from my phone), a nonce/hash for replay protection, and the running counter for the amount spent this week.
4. Check the destination, amount, and a timestamp for subscription logic (incremented by “a month” each call, so CryptoKitties can charge me no more than once per month).
5. Check the signees (keys from both laptop and phone).

I think we can expand the range of options accessible to the general userbase (with well-constructed application-layer GUI support) by allowing users to sign new versions of an arbitrary, settable transaction validation function (which can itself authorize executable signed messages).

A user’s account contract would then have the following function:

```
execute(
  address to,
  address from,
  uint256 value,
  bytes data,
  uint nonce,
  uint gasPrice,
  uint gasLimit,
  address gasToken,
  bytes messageSignatures,
  bytes validationBytecode,
  uint validationTimestamp
  )
```

`execute` will need to do the following:

- Check that the user has signed keccak256(validationBytecode, validationTimestamp), check that validationTimestamp is strictly greater than any previously stored validationTimestamp, and store validationTimestamp.
- Lazily deploy a new validation contract (only if there was no previous contract for this version of validationBytecode, could even use a global registry).
- DELEGATECALL into the validation contract, providing all the other parameters of execute.

The validation contract can then check transaction amount, destination, signee(s), gas, nonce/timestamp, etc. before executing the transaction, and can confirm any desired invariants after executing a transaction (such as that the contract’s token balance changed by no more than a certain amount).

This model is quite generic; for example, it can replace all the existing ERC20/ERC721 “approve”-style logic, and has the advantage (over “approve”) of placing all the approval information in one place (no need to track all contracts you’ve ever approved), allowing custom approval logic (such as only allowing `transferFrom` to be called by contract A with a destination of contract B), and allowing `approve` and `transferFrom` to be executed in the same transaction.

Definitely requires some fine-tuning, but hopefully the idea is clear enough, let me know what you think. May be better suited for a separate EIP or discussion elsewhere.

---

**alexvandesande** (2018-05-28):

Thanks for the contribution [@cwgoes](/u/cwgoes)! I completely agree with you that we need a broader more generic authorization scheme, but I would propose that this should be done on a key-basis, not per transaction. I like the idea of `validationBytecode`, but maybe it should be per account. Let’s see the CryptoKitty-of-the-month, example:

- User creates a “Kitty of the month” subscription and shares his public keys
- I authorize that account to have access to my wallet contract, but I give it a validationAddress, which is a contract with a standard interface that returns an integer between 0 and, say 1M.
- Every month, user Kitty will sign a transaction to buy the Kitty of the month and then send it to the wallet. For every signature, the wallet will give the details of the transaction to the validation contract, and it will return a number of 0 to 1M
- The wallet sums all the returned amounts and if it doesn’t amount to 1 million or more, then it will revert

So each logic is now contained in a reusable contract and it allows all sorts of schemes:

1. I would like to transfer 1 Ether to my friend to pay for dinner, once, now. Your phone has an authorization key that enables it to transfer up to 1 ether per week, so it allows it to be done with a single signed key
2. I would like to transfer 100 DAI to my son next Tuesday, only if his account balance is below 10 DAI, as allowance for dinner with his friends. Your son has an account that can request more allowance automatically, and it checks if it is own balance (if your son is smart he would make sure that this would be the case by transferring the money out!)
3. I would like to authorize my phone to spend Ether from my main account, but only up to 2 Ether per week, in case it gets stolen. same case as 1.
4. I would like to authorize CryptoKitties to transfer 0.1 Ether per month from my account for a “CryptoKitty-of-the-month” promotion, until I cancel this subscription. Cryptokitty of the month user has authorization to do a single transaction per month only for the purchase of kitties, with a limit
5. I would like to only allow transfers of more than 5 Ether if I authorize the transfer from both my laptop and my phone. Same as 1, but if it goes over the limit the validation contract returns 500k, therefore requiring more than one signature

---

**worldlyjohn** (2018-05-29):

> Again, this was exactly how OpenID was suggested. An identifier that looks a bit like email but isn’t email. Let’s just say that I’m not confident that ENS subdomains is a usable solution.

I don’t think OpenID failed because it was a single identity for the user.  IMO it failed because there was no incentive for websites to adopt this (no users) and no reason for users to adopt (no websites).

Facebook Connect won because publishers (websites) received more information (birthday, gender, etc) on top of email that they would have received if they built their own Auth.  And Users adopted this because it was less friction to click a button and “autofill” then create and remember yet another username/pw combination.

Times have changed, but they also haven’t.  I’d urge anyone thinking about developing SSO/self sovereign identity to think about incentives/motivations for both users and websites to adopt this.

---

**cwgoes** (2018-06-03):

Thanks [@alexvandesande](/u/alexvandesande)!

I agree that splitting up groups of transaction authorizations into separate contracts makes sense, it allows easier management on the part of the user and doesn’t require redeploying one large “validation function” contract every time the user wants to change their authorizations. Moreover, it should be the case that these validation contracts can be shared between users, so a single contract can handle a “CryptoKitty of the month” subscription for all subscribers.

I don’t quite understand the 500K / 1M return integer. Is that a way for the validation contract to tell the account contract whether or not a transaction is valid? Why not just use a boolean, or perhaps a list of keys which need to have signed the transaction?

With grouped authorization contracts as I understand them, the examples could work like the following:

User starts out with an account contract, which exposes an `execute` function as above, but with the additional parameter of `address validationAddress`. In addition to the checks listed above, when `execute` is called, the account contract checks that the calling contract (`msg.sender`) was granted permission by the user to use the specified `validationAddress` (in many cases, `msg.sender` can be anyone, but the `validationAddress` needs to have been explicitly authorized).

1. I would like to transfer 1 Ether to my friend to pay for dinner, once, now. I’ve previously created a “phone validation contract”, and authorized my phone’s public key to use this validation contract. The phone signs a message to transfer 1 Ether, the phone validation contract checks that the transfer amount is less than or equal to 1, and the transaction clears.
2. I would like to transfer 100 DAI to my son next Tuesday, only if his account balance is below 10 DAI, as allowance for dinner with his friends. I’ve previously created an “allowance validation contract” and authorized my son’s public key to use this validation contract. My son signs a message to pay himself allowance, and the “allowance validation contract” checks that the amount is correct and that he hasn’t already withdrawn allowance this week.
3. I would like to authorize my phone to spend Ether from my main account, but only up to 2 Ether per week, in case it gets stolen. Same case as 1.
4. I would like to authorize CryptoKitties to transfer 0.1 Ether per month from my account for a “CryptoKitty-of-the-month” promotion, until I cancel this subscription. I authorize the existing “CryptoKitty-of-the-month” public key to use the “CryptoKitty-of-the-month validation contract”, which checks that the amount is correct, that I’m only charged once per month, and that I get my CryptoKitty.
5. I would like to only allow transfers of more than 5 Ether if I authorize the transfer from both my laptop and my phone. I authorize a multisig validation contract, which can send any transaction but requires signatures from both my laptop and phone public keys (messageSignatures are forwarded to the validation contract).

Is that in line with your model, or did you have something different in mind?

---

**alexvandesande** (2018-06-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cwgoes/48/275_2.png) cwgoes:

> I don’t quite understand the 500K / 1M return integer. Is that a way for the validation contract to tell the account contract whether or not a transaction is valid? Why not just use a boolean, or perhaps a list of keys which need to have signed the transaction?

It should not just return a boolean of either a transaction is valid or not, because there are many cases in which what you want is actually “this transaction requires an additional confirmation from another transaction”. So, for instance, my son can make any purchase up to $100 monthly, but anything up to $250 he needs also my (or my wife’s) approval, and anything over $500 he needs both mom and dad to approve. A boolean, would not suffice there. Or the example you mentioned which for some transactions you need both the laptop and phone to approve.

Returning an integer is therefore more flexible, because then you can have more flexibility: if a transaction requires 4 approvals, each transaction contributes 25% of the sum. Maybe there’s a “master key” that is worth 2 votes, etc.

---

**pet3rpan** (2018-06-11):

We might need a central identity contract manager etc. like a portal to accept claims add keys etc. similar to my crypto wallet except the fund management.

You can then add another field to the delegate call signed data (ERC191) and add the dapp’s authenticated siganture, dapp title and dapp website.

```
Delegated call
    (
        byte(0x19),
        byte(0),
        from,
        to,
        value,
        dataHash,
        nonce,
        gasPrice,
        gasLimit,
        gasToken,
        callPrefix,
        operationType,
        extraHash
        ++ dappSignature,
        ++dappwWebsite,
        ++dappTitle,
    );
```

DappSignature - Something to authenticate the dapp itself, maybe even use something as central certification authority?

If you have these incorporated into the ERC191 delegate call then in the front end identity manager you could potentially monitor the activity of the contract in a more user friendly way vs. strings of hexidecimals

You could even then set warnings, black lists, white lists for authenticated dapps? Ideas

The itunes of dapps ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

---

**pranay01** (2018-09-12):

[@alexvandesande](/u/alexvandesande) Does this scheme mean that a new identity contract is created for each user or that same identity contract can be used for multiple users?

---

**alexvandesande** (2018-09-12):

Each user gets an identity contract (there are cheap ways to do that) which is shared by all apps. But the same identity address can own multiple ens username and a user can choose to own more identities.

---

**pranay01** (2018-09-13):

To clarify, by “user” do you mean a person in meat space or just a public/private key?

> and a user can choose to own more identities

By this do you mean a “user” in meat space can have multiple private keys? Or you mean that a public key (which defines a user) can be associated with multiple identity contracts?

---

**alexvandesande** (2018-09-13):

Any meatspace person or entity can create multiple identities contracts (but they only need one). An identity contract can interact with any number of apps (no need to be one app one account). An identity contract can hold multiple names (but each name can only point to one identity contract back)

---

**pranay01** (2018-09-28):

Got it. Another question, since the private keys send signed transactions to relayers (which are centralised entities), can’t relayer do arbitrary things with this transaction. For example, send this to a contract which is not  an identity contract, etc?

Also, what type of orgs/entities will host these relayers. Can the relayers have any business model (like in case of Dharma relayers) or we expect well respected institutions like EthFoundation etc. to host these relayers.

---

**alexvandesande** (2018-09-28):

> Another question, since the private keys send signed transactions to relayers (which are centralised entities), can’t relayer do arbitrary things with this transaction.

No. The identity will only execute things that are signed by approved keys, so the relayer cannot force the identity to do anything. The only power the relayer has is to refuse service to the user, but that is avoidable because the user can in theory simply use another relayer.

> For example, send this to a contract which is not an identity contract, etc?

Not sure I understand: are you saying that an arbitrary unrelated contract could accept these transactions signed by other people? The message signed includes the identity address, so the identity will only accept messages that were signed to itself. Of course, you can always build another contract that ignores this and accepts signed messages meant for others, but I don’t see why someone would do it.

---

**pranay01** (2018-09-29):

Yes, I was thinking of the scenario where the message is relayed to another contract which accepts the message, but its effectively a denial of service - as  you have pointed out.

So, for this mechanism to work, there needs to be a market for relayers ( basically you should be able to chose another, if one is denying service). For that to happen, relayers should be incentivised in some way, right? So, a commission based model or do expect some other mechanism to incentivise them?


*(7 more replies not shown)*
