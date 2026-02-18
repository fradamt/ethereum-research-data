---
source: ethresearch
topic_id: 4530
title: Spam protection with probabilistic payments and cheap doublespending protection
author: DennisPeterson
date: "2018-12-09"
category: Applications
tags: []
url: https://ethresear.ch/t/spam-protection-with-probabilistic-payments-and-cheap-doublespending-protection/4530
views: 2666
likes: 0
posts_count: 5
---

# Spam protection with probabilistic payments and cheap doublespending protection

A somewhat overlooked way to scale small transfers is probabilistic payments. To pay you ten cents, I can give you a ticket with a 1% chance of paying ten dollars, and it only goes on chain if it pays out.

To make this work, we need a good source of randomness, and protection against replays. One method is to use block hashes and target particular blocks, though this will require us to record blockhashes in a more persistent way. If we assume users post a “current” hash to a contract, indexed by the hash of their email address, then we can use a hash onion per recipient. The sender signs sha3(receiver, targetHash, randomNumber) where targetHash is the current hash. The receiver takes the preimage of the targetHash, hashes it with the sender’s random number, and if the result is below a threshold then he submits the signed message and preimage to the contract and gets paid. The contract sets the preimage as the new “current” hash.

Vitalik [posted](https://blog.ethereum.org/2014/09/17/scalability-part-1-building-top/) in 2014 that it’s easy to doublespend against something like this, and suggested a large penalty bond, payable if the sender’s funds are insufficient upon redemption. We can do without that for some applications, like voluntary tips. In that situation a doublespend isn’t necessarily malicious; if the tip has a 1% chance of paying off, the user can reasonably deposit only enough funds to pay off a single tip while sending two concurrently, ignoring the 1/10,000 chance that both pay out.

For spam protection, we can make the doublespend problem go away entirely. Clients can require a probabilistic payment from unknown senders; let’s assume a penny per email makes spam unprofitable, and use a 1/1000 chance of getting $10.

A spammer may attempt to get around this by depositing only $10 and sending a million emails referencing that deposit. Naive recipients would have no way to tell.

But there’s an easy way to counter this: have the email client attempt to redeem the payment immediately, but wait an hour before showing the unsolicited email to the user. If most recipients do this, the spammer’s deposit is likely to go to zero in that hour. In that case, discard the email. This means the only person who reads the email is the one who got paid $10 to do so.

There’s no happy medium that helps the spammer. Even if he deposits $10,000, there’s an almost 50% chance that too many redemption attempts will succeed; then he reaches only a thousand people, paying $10 for each. To be confident of reaching a large number of people he needs a deposit large enough that it’s unlikely to run out. Thus the best he can do is pay an expected penny per email.

## Replies

**PhABC** (2018-12-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/dennispeterson/48/1675_2.png) DennisPeterson:

> have the email client attempt to redeem the payment immediately, but wait an hour before showing the unsolicited email to the user.

If all clients try to redeem the payment immediately, isn’t this a serious griefing factor for recipients, assuming by “reedeming” you imply an on-chain transaction.

What about requesting a PoW proof that receivers can verify? One could make the PoW cost sufficiently high such that generating signatures for more than one recipient would cost most than the value contained in the ticket. It does increase costs paid for users, but it would improve the UX by not requiring deposits for each recipient.

---

**DennisPeterson** (2018-12-11):

> not requiring deposits for each recipient

Not sure what you mean here but just to clarify: we don’t need a separate deposit for each recipient, just enough deposited to be confident of paying the 1/1000 recipients whose tickets are redeemable.

You have a good point on griefing. 1000 of the one million recipients would see (offline) that the ticket will pay off, and send a transaction to the network attempting to collect. Only one would actually collect, so this would indeed be annoying.

However, that’s only the case if the spammer actually sends emails with insufficient deposits. Since this is much more expensive per actual reader ($10 instead of a penny), it’s more likely that spammers would deposit enough to actually pay the 1 in 1000 recipients whose tickets are redeemable. If that costs too much for them, then they have no profitable option.

Of course if someone’s sole purpose is to grief recipients, that’s another matter. If that happens often, a simple defense is to attempt on-chain redemption after a random delay instead of immediately (and only if the deposit is still there). I *think* it’d work for each user to make their own determination of the most profitable range of random delay, balancing the race to get the deposit against the waste of gas when they lose.

A nice side benefit is that the same system enables voluntary user-to-user tips.

For spam protection alone, PoW is definitely another option, though it’s not perfect; see Vitalik’s post here: [Conditional proof of stake hashcash](https://ethresear.ch/t/conditional-proof-of-stake-hashcash/1301)

---

**yondonfu** (2018-12-11):

> The receiver takes the preimage of the targetHash, hashes it with the sender’s random number

Does the preimage have to correspond to the current `targetHash` value stored in the contract or does it just need to correspond to the `targetHash` value included in the sender’s signature over `sha3(receiver, targetHash, randomNumber)`?

> The contract sets the preimage as the new “current” hash.

Instead of using a hash onion per receiver, could the receiver just generate a new `targetHash` value (with knowledge of its preimage) and provide that when redeeming a winning ticket?

---

**DennisPeterson** (2018-12-11):

For both questions, the answer is that we have to prevent replay attacks.

1. If the preimage only had to correspond to the targetHash in the sender’s message, then the receiver could redeem the sender’s message again and again until sender runs out of money.
2. If the receiver could generate a new targetHash value arbitrarily, as long as it’s different than the previous one, then sender could alternate between two targetHash values, replaying the sender’s message every other time.

Replays could also be prevented by storing all the targetHash values used so far, and checking that each one is new. But using a hash onion eliminates the need for that storage, by forcing sender to set a specific new and random targetHash.

Another approach is to include a nonce in the message. Whenever the receiver redeems/sets a new arbitrary hash, the nonce increments, and the next message has to match that nonce.

I found it slightly more convenient to use a hash onion because the receiver can send just one value that functions as both preimage and new targetHash; since the receiver has to store that preimage anyway, he might just as well store the root of the hash onion instead. Having the root, it’s very fast to iterate through thousands of hashes to get the required preimage, assuming you’re using a dapp UI rather than working directly with the contract.

A drawback to the hash onion is that you eventually run out of hashes. To deal with that, either have users change to a new address, or add a nonce to the hash onion scheme, where a normal redemption sets targetHash to the preimage, but a separate function lets the user initialize a new hash onion and increment the nonce.

