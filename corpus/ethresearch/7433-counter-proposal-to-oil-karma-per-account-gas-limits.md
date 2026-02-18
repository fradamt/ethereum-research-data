---
source: ethresearch
topic_id: 7433
title: "Counter-proposal to oil/karma: per-account gas limits"
author: vbuterin
date: "2020-05-15"
category: Execution Layer Research
tags: []
url: https://ethresear.ch/t/counter-proposal-to-oil-karma-per-account-gas-limits/7433
views: 3400
likes: 7
posts_count: 14
---

# Counter-proposal to oil/karma: per-account gas limits

## Ideas this is a counter-proposal to

- Oil: adding a second fuel source to the EVM (pre-EIP)
- https://gist.github.com/holiman/8a3c31e459ee1bff04256bc214ea7f14

## Background

Currently, there are many reasons why we want to increase the gas cost of many operations. Most particularly, we want to massively increase (eg. by 3-10x) the gas cost of BALANCE, EXT*, SLOAD and other operations that access state, both because we want to bound witness size and because we want to bound the harm that could be caused by known DoS attack vectors. However, increasing gas costs is dangerous, because contracts sometimes call other contracts with fixed gas limits, and so if gas costs are increased by a hard fork, applications that worked before may cease to work.

The oil/karma proposals linked above solve this by introducing two classes of gas, “gas” and “oil” (or “karma”). Gas works as before, and gas costs of operations are never changed upward. Any new/increased gas costs are instead added as oil costs. A transaction aborts if the total (gas+oil) spending exceeds the total tx gaslimit, and the gas payment is based on gas+oil spent. **Importantly, if A calls B, A can restrict how much gas B spends (as today), but A cannot restrict how much oil B spends**.

The proposal solves the problem, but IMO does so at the expense of a great increase in complexity and is very inelegant in how it solves the problem, because one would still somehow need to bound how much oil the child call burns if it is untrusted (see below).

### Stepping back: why do we even need gas-bounded subcalls?

One simple fix to this problem is to make *all* gas into oil; that is, when A calls B, **make it so that A is *always* forced to entrust B with the ability to spend all remaining gas**. And it turns out that *most applications already work this way*; there are relatively few exceptional cases where A assigns a limited quantity of gas to B.

There are two cases:

1. The 2300 gas limit baked into ETH-sending transactions, intended to allow a log to be generated
2. Cases where A does not trust B

(2) is surprisingly rare; the main example of this used today is “meta-transactions”, where Bob wants a call to be made to B but has no ETH, so Bob signs an authorization that allows Alice to make a call that (i) calls B and (ii) withdraws some ERC20 token from Bob to Alice. The contract A that implements this procedure *needs to* limit gas allocated to B, because otherwise Bob could grief Alice by constructing a B that consumes all the gas, preventing the ERC20 token transfer in the second half of the transaction from being made.

My counter-proposal aims to provide alternate solutions to both (1) and (2). I will focus on (2) first.

### The proposal

- Option 1: Allow a transaction to specify a table T: {account: gaslimit}. A call to an account A in T would only be assigned a maximum of T[A] gas, and otherwise calls would be assigned all the remaining gas.
- Option 2: Allow a transaction to specify a parameter 0 <= r <= 63 (representing the fraction r/64), where if an EVM instance has X remaining gas and it makes a call, the call would only be given X * r // 64 gas, so the parent would still be guaranteed to have X * (64-r) // 64 gas remaining
- Option 3: allow a transaction to specify a parameter M; the gas given to all child calls is multiplied by M
- Option 4: just change the 63/64 constant introduced in https://github.com/ethereum/EIPs/issues/114 to 3/4

The intent of options (1, 2, 3) is to move the choice of how much gas to give to child calls to the transaction sender, allowing the transaction sender to specify how much they trust the accounts that are being child-called into. Option (4) is a “dumber” but simpler fix; it ensures that in *any* call there will always be enough gas to do many things both in the child call and after the child call, and any gas cost increase can be dealt with by the transaction sender simply upping the global gas limit.

### Alternatives to the 2300 gas minimum

The 2300 gas minimum was originally put into place to ensure that if an account receives ETH it can log this fact; this is useful for eg. wallets. And indeed, 2300 gas is not sufficient to do anything but issuing one or two logs. I propose two options that solve this problem but avoid enshrining a single gas limit:

- Option 1: the transaction sender specifies the gas minimum, and to avoid introducing re-entrancy issues we add a rule that an ETH-transferring call that provides 0 additional gas does not allow the child call to make any state changes (ie. it’s similar to STATICCALL except it can log)
- Option 2: we remove the 2300 gas entirely (or don’t touch it), and instead add an explicit log every time any account receives ETH for any reason (including the currently not-covered case, self-destructs).

## Replies

**holiman** (2020-05-15):

There are a couple of problems that I foresee with this (but it might just be that I have missed something).

So, consider an hypothetical token, which has a `burn`, which sends you back the ether:

```auto
function burn(amount int){
    assert(balances[msg.sender] > amount);

    if !msg.sender.send(amount).gas(0){
        revert()
    }
    balances[msg.sender] -= amount
}
```

The code above looks like it would not be safe against reentrancy, but it de-facto is, since `send` only has `0` gas, which becomes `2300` on the receiving end. This may be bad practice, but it’s still an invariant that has been around forever: “A 0->2300 CALL cannot modify state”.

With options 1,2,3, you put `origin` in charge of gas forwarding, meaning that the (potentially malicious) transaction signer can change the behaviour of the (target) contract, and turn what today is not a vulnerable contract into a vulnerable contract.

Regarding Option 4, I don’t really understand it.

So, to handle the now vulnerable contracts, we obviously need to do something about the `2300` gas limit.

- Option 1 (EDITED): Yes, this would probably work, in most cases. I know that Serpent once upon a time added a little bonus on top of the 2300. If there are such contracts around, they would not benefit from the “0-2300 means no state changes” rule.
- Option 2: I think the contract-types broken by 1884 would be broken again :

EIp-1884. Example 1: (SLOAD + LOG)

```auto
  function () public onlyIfRunning payable {
    require(isApproved(msg.sender));
    LogEthReceived(msg.sender, msg.value);
  }
```

Example 2 (2 SLOAD):

```auto
    modifier onlyICO() {
        require(now >= icoStartDate && now < icoEndDate, "CrowdSale is not running");
        _;
    }
```

---

**vbuterin** (2020-05-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/holiman/48/4014_2.png) holiman:

> The code above looks like it would not be safe against reentrancy, but it de-facto is, since send only has 0 gas, which becomes 2300 on the receiving end. This may be bad practice, but it’s still an invariant that has been around forever: “A 0->2300 CALL cannot modify state”.

Right, this is why the part of my proposal that deals with the 2300 gas case involves making such calls STATICCALLs (except they can also log).

> I know that Serpent once upon a time added a little bonus on top of the 2300. If there are such contracts around, they would not benefit from the “0-2300 means no state changes” rule.

Agree, though I do think that a small amount of one-time disruption is an acceptable compromise for moving toward a more long-term sustainable model. (btw [the most recent version of serpent](https://github.com/ethereum/serpent/blob/d460382f56003b9d56bafafe930f8b606d4b039f/rewriter.cpp#L153) doesn’t add the bonus ![:smiley:](https://ethresear.ch/images/emoji/facebook_messenger/smiley.png?v=12), an [older version](https://github.com/ethereum/serpent/blob/9a189da426377f62eee5d17db21cf314235736a7/rewriter.cpp#L153) does add a 5000 bonus but I *really* doubt anyone used it…)

> Option 2: I think the contract-types broken by 1884 would be broken again

Not sure I understand; what would be broken? Note that the STATICCALL rules do not prohibit *reading* state or for that matter making internal self-calls (though the internal self-calls of course also become static).

---

**holiman** (2020-05-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Agree, though I do think that a small amount of one-time disruption is an acceptable compromise for moving toward a more long-term sustainable model

I agree. I just wanted to point it out that the possibility (that contracts assume no-reentrancy on low gas provided) exists

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Option 2: I think the contract-types broken by 1884 would be broken again

Not sure I understand; what would be broken?

I guess Option 2 wasn’t fully clear to me. But let’s say we want to increase LOG or SLOAD to something very high. How does option 2 handle the case where a contract wants to check sender against a whitelist, and reject otherwise.

The oil/karma proposal seems IMO to give us a lot of freedom, since we suddenly gain an *unobservable* (so contract semantics cannot make decisions based on it) and *global* gas meter. Whereas this proposal removes/changes some of the rules regarding gas forwarding, but adds more special cases. I find this one a bit harder to reason about in a general sense.

---

**vbuterin** (2020-05-16):

Huh, I didn’t realize there were contracts that explicitly checked ETH senders against a list and accepted or rejected the transfers based on that result.

I’m inclined to say that’s a bad pattern and especially since we already broke it we should just ban it (if you want to do weird conditional transfers like that, just make a proper function call, or do any checking logic on the caller-side).

That is, more strictly enshrine the idea that calling and pure-transferring ETH are different operations, and if you purely transfer ETH, there’s nothing substantive that the recipient can do.

> The oil/karma proposal seems IMO to give us a lot of freedom, since we suddenly gain an unobservable (so contract semantics cannot make decisions based on it) and global gas meter. Whereas this proposal removes/changes some of the rules regarding gas forwarding, but adds more special cases. I find this one a bit harder to reason about in a general sense.

The thing that makes it harder for me to reason about with oil/karma is that calculating how much gas you’re entrusting the destination contract with becomes a complicated game; essentially, the max resources that the destination contract can burn is equal to the assigned gas multiplied by the highest ratio of oil cost to gas cost in any transaction. This seems… highly unintuitive.

Even worse, in the meta-transactions use case (BTW do you know of any other use cases of untrusted calls?), it basically means that the max gas capacity of a meta-transaction becomes 10 million divided by whatever the max oil/gas cost ratio is, so meta-transactions become much weaker than regular transactions, and protocol upgrades that increase the max oil/gas ratio would also make the max meta-transaction gas lower, potentially suddenly excluding some applications from meta-transactions. I could see eg. a STARK version of tornado cash (it’s a use case that has both high gas costs *and* needs meta-transactions) falling victim to this pretty quickly.

---

**holiman** (2020-05-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> contracts that explicitly checked ETH senders against a list and accepted or rejected the transfers based on that result.
>
>
> I’m inclined to say that’s a bad pattern and especially since we already broke it we should just ban it (if you want to do weird conditional transfers like that, just make a proper function call, or do any checking logic on the caller-side).

I think there are a few cases where this would be used.

1. For KYC/AML purposes, where a whitelist of approved users/buyers are listed. However, in this case the caller should be able to do a regular method invocation with arbitrary gas.
2. In crowdsales, there might be e.g. some background ‘wallet’, without all the other crowdsale-functionality. After the crowdsale is over. or during some events in the crowsale, the crowdsale contract sends off the funds to the backend wallet. The backend wallet prevents ‘anyone’ from sending funds there, to minimize risk of crowdsale participants erroneously sending funds to the wrong destination. In this case, where you have a “Admin User → Crowdsale contract → Backend wallet”, it might not be possible to ‘salvage’ from the end point, causing stuck funds.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> since we already broke it we should just ban i

We didn’t *quite* already break it. With `700`, you can still do an `SLOAD` and a `LOG`, but the margins are slim indeed. If we bump `700` much more, we *will* break it fully.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The thing that makes it harder for me to reason about with oil/karma is that calculating how much gas you’re entrusting the destination contract with becomes a complicated game; essentially, the max resources that the destination contract can burn is equal to the assigned gas multiplied by the highest ratio of oil cost to gas cost in any transaction.

Here’s one item where oil/karma differs, I think. I don’t anticipate gas/oil to have anything but 1:1 ratio. If you always start out with getting just as much karma as you already have gas, then it’s still simple. Once we modify the tx format, you can buy extra karma. But I admit that I haven’t fully fleshed that whole part out.

I need to consider the meta-tx case more, to fully understand that gotchas there.

---

**vbuterin** (2020-05-18):

> Here’s one item where oil/karma differs, I think. I don’t anticipate gas/oil to have anything but 1:1 ratio. If you always start out with getting just as much karma as you already have gas, then it’s still simple. Once we modify the tx format, you can buy extra karma. But I admit that I haven’t fully fleshed that whole part out.

I don’t understand this paragraph. Suppose that currently the cost of SLOAD is 800, but we *want* SLOAD to have a cost of 4000 for witness size minimization. If gas costs don’t change, this means that a contract spending 2 million gas would be able to burn `4000 * (2 million / 800)` = 10 million of whatever the limiting resource is. Hence, a 2m gas call would be able to halt any transaction, and so metatransactions would not safely be able to have >=2m gas.

---

**holiman** (2020-05-18):

In that case, we would have the `gascost` of `SLOAD` remain at `800`, but set the karma-cost to be `4000`. Each SLOAD would eat `800 gas` and `4K` karma. A user supplying `2M` gas would thus have `2M` karma, and be able to do `2M/4K` ops before running out of karma.

---

**vbuterin** (2020-05-18):

Wait… then what’s the difference compared to just increasing the gas cost, and possibly adding a mandatory minimum gas equal to the gas cost of the most expensive operation?

---

**holiman** (2020-05-18):

The difference is that contracts can’t throttle the karma, so the origin can always just add more if it runs out at some internal call. So broken flows can be un-broken by the tx sender.

---

**wighawag** (2020-05-18):

Hi,

While I definitely think ethereum CALL opcodes and gas behavior could be improved, I am not sure karma or the counter proposals brought here really bring much value.

From my understanding the idea behind  karma is just to allows contract to continue using opcode pricing assumption  (that is in gas, not in karma) in their code.

While this might sounds good in theory, I am not sure we should actually care about contract that have hard-coded gas assumption in their code.

If we talk about

> “moving toward a more long-term sustainable model”

then we can simply stop hardcoding gas opcode pricing assumption and I think the message is already clear by now.

What would be interesting to know though is why the authors of such contract decided to hardcode such assumption and if it was because of certain lack of features in the EVM that we could then fulfil.

Regarding meta transaction, while the griefing attack is a possible scenario that metatx relayer need to consider, they are normally able to compute the outcome before submitting. It is indeed true that they still run the risk of state change between the time they submit the tx and the time it get mined, but then this is not unique to having not enough gas : the metatx user could have submitted the same tx to another relayer, user could have removed all its fund from the relay repayment mechanism,.etc…

In the metatx case, **the gas limit specified as part of the inner call has actually a more important role** : protecting the meta tx signer that its meta-tx is executed with the exact amount specified by its signed message. In other word, the gas limit act here as a lower bound. Else the relayer could maliciously make the inner call fails while getting paid as a result (due to 63/64 rule).

As [EIP-1930](https://github.com/ethereum/EIPs/issues/1930) points out, such “strict gas semantic for call” is not possible to do it today without relying on tricks (relying on the 63/64 rules) or specific opcode pricing (by computing the amount of gas required to perform the call). See details in EIP-1930.

None of the proposals here would help.

In regard to the scenario where the upper bound is useful, they are usually circumvented by the “favor pull over push transfers” approach. The idea behind it is already that we should not trust the recipient. And that’s why I think the strict call semantic advocated in 1930 might be all we need: contract either give 63/64 or give a specific amount (in which case, if that amount is not available it fails). The latter might be useful only for meta-tx in which case a potential improvement could be to support meta-tx at the native level, so we could have one simple rule : every call gives 63/64 (though I would advise against making any assumption on that particular value being forever the same)

On the subject though, gas and call opcodes have other issues. I describe some of them in my blog here : https://ronan.eth.link/blog/ethereum-gas-dangers/ .

For example, it would be useful if a contract could know whether an inner call failed because of a lack of gas (instead of another type of failure) so it could revert the whole tx knowinggly.

This would not allow “push transfer” to be safe but this could ensure that a inner call is not interpreted wrongly as a genuine failure when it actually did not receive enough gas.

---

**vbuterin** (2020-05-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/wighawag/48/177_2.png) wighawag:

> In the metatx case, the gas limit specified as part of the inner call has actually a more important role : protecting the meta tx signer that its meta-tx is executed with the exact amount specified by its signed message. In other word, the gas limit act here as a lower bound. Else the relayer could maliciously make the inner call fails while getting paid as a result (due to 63/64 rule).

OK this is a fair point. Basically, the problem is that we are trying to protect against misreporting on both sides. The meta tx signer specifies an amount of gas `G` that they claim is sufficient to execute their tx. The signer needs an assurance that the tx actually will be executed with `G` gas, and not less. Meanwhile the relayer needs an assurance that they will actually be spending `G` gas on the meta tx and not more.

So the two sides need to negotiate and agree on `G`, and for that agreement to be enforceable. The current way to enforce `G` is to have the meta tx signer only approve payment to a specific contract that puts `G` gas on the sub-call. But all of these proposals make `G` flexible at origin level and unreadable at contract level, and so they break this approach. One approach would be to make it possible to read the *total* gas in the transaction, and have the contract call verify (i) that the total gas is `G + buffer` and (ii) that the origin called the contract directly and nothing else in between (this would require new opcodes). But this seems complicated, and also dumb developers *could* write applications that freeze in place specific total-gas checks that would lead to future hard forks breaking the applications.

So this leads to a philosophical question: why not just implement none of these proposals, keep tweaking gas costs as needed for sustainability as we’ve done before, and just publicly state the social norm that you should never hardcode gas limits into a contract, and all inputs to `CALL` that are not just “send all gas” should have gas values provided by the transaction?

---

**dankrad** (2020-05-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> So this leads to a philosophical question: why not just implement none of these proposals, keep tweaking gas costs as needed for sustainability as we’ve done before, and just publicly state the social norm that you should never hardcode gas limits into a contract, and all inputs to CALL that are not just “send all gas” should have gas values provided by the transaction?

I actually do think that this is the best solution for opcode gas adjustments! Anything else enshrines the notion that you can somehow rely on gas behaving in a certain way which is a bad social contract, which has already been broken. We’d need to define what exactly the limits for adjustments are which is just weird.

---

**wighawag** (2020-05-21):

Exactly, but we still need to have a proper way to handle strict gas semantic for meta-tx (EIP-1930) or even better handle meta-tx natively via new opcodes or transaction format.

That is another topic though. Here are some links on EIP-1930 discussion:

- https://ethereum-magicians.org/t/erc-1930-allows-specification-of-a-strict-amount-of-gas-for-calls/3132
- https://github.com/ethereum/EIPs/issues/1930

it would be great if we could progress on this as this is a relatively simple improvement

