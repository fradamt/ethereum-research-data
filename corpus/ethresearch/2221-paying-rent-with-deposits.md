---
source: ethresearch
topic_id: 2221
title: Paying rent with deposits
author: nickjohnson
date: "2018-06-12"
category: Sharding
tags: [storage-fee-rent]
url: https://ethresear.ch/t/paying-rent-with-deposits/2221
views: 3713
likes: 14
posts_count: 21
---

# Paying rent with deposits

Thinking about storage rent - what about requiring a deposit for all storage used, instead of a rental fee? The deposit can be refunded in its entirety when storage is freed up, and provides a direct financial incentive to free up unused storage, without any of the complexity of tracking rent balances over time, and deleting state for contracts ‘in arrears’. With Casper, there’ll be a very real opportunity cost of locking up your ether, and so a direct financial incentive to design contracts to be conservative with the storage they use.

## Replies

**MicahZoltu** (2018-06-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/nickjohnson/48/157_2.png) nickjohnson:

> With Casper, there’ll be a very real opportunity cost of locking up your ether

I’m not yet convinced that the opportunity of staking in Casper will outweigh the risk of having your ETH controlled by a hot wallet.  With storage, your ETH can be secured by a cold wallet, thus is significantly lower risk.

As a user, I’ll need pretty solid returns from staking to convince me to bring my ETH out of cold storage.  However, having my ETH locked up in a contract that is recoverable by my cold wallet is not really a different risk profile from storing in my cold wallet directly.

---

**nickjohnson** (2018-06-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> I’m not yet convinced that the opportunity of staking in Casper will outweigh the risk of having your ETH controlled by a hot wallet. With storage, your ETH can be secured by a cold wallet, thus is significantly lower risk.
>
>
> As a user, I’ll need pretty solid returns from staking to convince me to bring my ETH out of cold storage. However, having my ETH locked up in a contract that is recoverable by my cold wallet is not really a different risk profile from storing in my cold wallet directly.

You still incur the opportunity cost of not being able to use those funds for anything as long as they’re locked up paying for storage.

---

**MicahZoltu** (2018-06-12):

The main point of my argument wasn’t that your proposed solution was bad, just that that particular piece of the argument doesn’t hold water IMO since it is yet to be seen whether or not the yield of staking even fully offsets the risk of holding your assets in a hot wallet.

---

**vbuterin** (2018-06-13):

In the most recent Casper FFG implementation, a compromise of your hot wallet will only cost a large portion of your funds in the case that very many other users get compromised (or attack) at the same time. So it’s a much smaller risk than actually putting all of your funds in the hot wallet.

---

**clesaege** (2018-06-13):

I like the idea, as it’s simpler to make people “pay” by inflation than to actually remove some ETH.

It’s also a better incentive than gas refund as gas refund can only be used to, at best, divide the cost of a transaction by two, providing really little incentive for cleanup.

On a precedent, you can see that Augur switched from making inactive token holder loose funds, to increasing the total supply and rewarding active token holders (see: https://www.augur.net/whitepaper.pdf).

However the disadvantage of requiring a deposit, is that the capital lockup costs decreases with inflation making it tends toward 0 (but quite slowly).

---

**kfichter** (2018-06-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> a compromise of your hot wallet

Is it more like a hot key that votes on behalf of some funds instead of a key that directly controls the funds?

---

**clesaege** (2018-06-13):

Yeah, that how I see it. It does not need to be implemented in casper, but people would use staking smart contracts requiring different keys for different actions.

---

**MicahZoltu** (2018-06-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/clesaege/48/533_2.png) clesaege:

> Augur switched from making inactive token holder loose funds, to increasing the total supply and rewarding active token holders

It turns out this was a mistake and the system is very likely switching to “use-it-or-lose-it” sometime after launch.  ![:cry:](https://ethresear.ch/images/emoji/facebook_messenger/cry.png?v=12)

---

**MicahZoltu** (2018-06-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/clesaege/48/533_2.png) clesaege:

> people would use staking smart contracts requiring different keys for different actions.

Ah, clever.  So the contract may limit “withdraw funds” action to a cold key or multisig, while “vote for block” would be done with a hot key?  And since the damage that can be done via voting wrong is limited, this limits the risk of the staker.

---

**clesaege** (2018-06-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> It turns out this was a mistake and the system is very likely switching to “use-it-or-lose-it” sometime after launch.

I’m not sure it’s a mistake, but they may increase the inflation rate (5% everytime there is a fork is really low, I think something like 50-100% when there is a fork is reasonable).

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> Ah, clever. So the contract may limit “withdraw funds” action to a cold key or multisig, while “vote for block” would be done with a hot key? And since the damage that can be done via voting wrong is limited, this limits the risk of the staker.

Yeah, that’s how I’d do it.

---

**MicahZoltu** (2018-06-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/clesaege/48/533_2.png) clesaege:

> I think something like 50-100% when there is a fork is reasonable).

I don’t want to hijack this thread any more than I already have, but if you want to discuss this more in depth feel free to hop into Augur Discord server or DM me here (assuming DMs here are a thing)!

---

**jvluso** (2018-06-14):

The point of rent is that accounts that use more storage space time need to pay more, and accounts that use less storage space time need to pay less. Simply relying on inflation for the cost would mean that accounts that have more tokens would be paying more, not accounts that use more storage. Rent also allows unused dust accounts to be cleaned up, and relying on inflation or even a deposit does not solve that.

---

**nickjohnson** (2018-06-14):

Right; I’m not suggesting using inflation, but rather opportunity cost. Locking up funds always imposes an opportunity cost, and the ability to recover those unused funds provides an integrated incentive to free up storage.

---

**PhABC** (2018-06-19):

Isn’t this basically the current model but instead of redeeming your deposit as a gas refund, you get ETH back directly?

---

**nickjohnson** (2018-06-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/phabc/48/35_2.png) PhABC:

> Isn’t this basically the current model but instead of redeeming your deposit as a gas refund, you get ETH back directly?

It has a couple of important differences:

- Refunds would not be limited to half the gas used, providing a real incentive to free up used space.
- Refunds would be denominated in Ether, not in Gas.

We’d need some way to set a consistent ether price for the deposit for each storage slot, however - perhaps a voting mechanism for miners along the lines of gas limit voting. We can’t allow miners to set it as they wish like with the gas price, because that would lead to miners including their own and their friends’ transactions for free.

---

**PhABC** (2018-06-20):

Right, so we would need a new type of gas in a way, one used for storage related operations (`SSTORE`) and one for computation related operations. Could call the former *crystals* :D.

Would the refund go to `msg.sender` still? If so, it seems like this approach would be a non-breaking change. I’m not sure if it provides a bigger incentive than current model however, since with the current refund, contract owner can resell the available gas refund at arbitrary price, allowing them to control the revenue they make. I can definitely see benefits however, where public methods to free storage would be called very quickly, which is good.

I like this approach and would be happy to see some tests and incentive related analyses.

---

**nickjohnson** (2018-06-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/phabc/48/35_2.png) PhABC:

> Right, so we would need a new type of gas in a way, one used for storage related operations ( SSTORE ) and one for computation related operations. Could call the former crystals :D.

Rather than another type of gas, I think you’d just have consensus ‘slot price’. Any SSTORE to a previously empty slot would cost that much ether, and the balance would be stored against the contract’s deposit balance.

We would need to establish how this is paid for (is there a ‘storage slot limit’? Is it deducted from gas based on the current gas rate instead?)

![](https://ethresear.ch/user_avatar/ethresear.ch/phabc/48/35_2.png) PhABC:

> Would the refund go to msg.sender still? If so, it seems like this approach would be a non-breaking change.

It would, yes. It’s up to contract authors to manage deletion in a way that makes sense.

![](https://ethresear.ch/user_avatar/ethresear.ch/phabc/48/35_2.png) PhABC:

> I’m not sure if it provides a bigger incentive than current model however, since with the current refund, contract owner can resell the available gas refund at arbitrary price, allowing them to control the revenue they make.

I don’t think gastoken-like contracts are a practical mechanism right now, due to the complexity and the fact they require additional upfront gas and only refund up to half the total. I certainly don’t think they affect peoples’ decision making around contract design and storage costs.

---

**PhABC** (2018-06-20):

> We would need to establish how this is paid for (is there a ‘storage slot limit’? Is it deducted from gas based on the current gas rate instead?)

Deduced from gas*gasPrice seems like the most UX friendly and subtle imo. What would be the rational for a ‘storage slot limit’?

> Due to the complexity and the fact they require additional upfront gas and only refund up to half the total.

Even with the deposit scheme you propose, users need to pay *some* gas for the storage operation. If the refund was 100%, then you open the door to DDos (someone just storing and freeing storage slots). The current gas refund could be 20k, which means you would be receiving 75% of what you initially paid (accounting for the 5k gas cost of `SSTORE` when clearing the storage slot), which could be OK, but not sure if that’s a potential DDos vector as well.

---

**nickjohnson** (2018-06-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/phabc/48/35_2.png) PhABC:

> Deduced from gas*gasPrice seems like the most UX friendly and subtle imo. What would be the rational for a ‘storage slot limit’?

You cannot make the storage cost depend on gas price, or miners can bloat the state at will. You could have a consensus-determined (in ether, not gas) cost per slot, then bill it as a variable amount of gas in order to use that accounting mechanism.

The alternative is to charge the sender for storage slots separately, in which case they need some way to specify the most they’re prepared to pay.

![](https://ethresear.ch/user_avatar/ethresear.ch/phabc/48/35_2.png) PhABC:

> Even with the deposit scheme you propose, users need to pay some gas for the storage operation. If the refund was 100%, then you open the door to DDos (someone just storing and freeing storage slots). The current gas refund could be 20k, which means you would be receiving 75% of what you initially paid (accounting for the 5k gas cost of SSTORE when clearing the storage slot), which could be OK, but not sure if that’s a potential DDos vector as well.

There’d still be a gas cost for the opcodes themselves, but refunds are in ether, not in gas. There’s no DoS vulnerability, because it doesn’t allow you to increase the total amount of work done in a block.

---

**PhABC** (2018-06-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/nickjohnson/48/157_2.png) nickjohnson:

> You cannot make the storage cost depend on gas price, or miners can bloat the state at will. You could have a consensus-determined (in ether, not gas) cost per slot, then bill it as a variable amount of gas in order to use that accounting mechanism.
>
>
> The alternative is to charge the sender for storage slots separately, in which case they need some way to specify the most they’re prepared to pay.

Sorry, I should’ve been clearer. This is indeed what I meant. The cost per storage slot is fixed (denominated in ETH), which could be reflected as a dynamical gas amount based on gas price. Hence, you need to provide more gas at lower gas price, but at least it would be hidden from users since easily predictable by UX.

