---
source: ethresearch
topic_id: 836
title: Improve Casper Security thanks to Cold Storage Masternodes
author: Etherbuddy
date: "2018-01-21"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/improve-casper-security-thanks-to-cold-storage-masternodes/836
views: 2285
likes: 3
posts_count: 11
---

# Improve Casper Security thanks to Cold Storage Masternodes

Hello,

I’d like to discuss a way to increase the security of Ethers stored for Casper POS.

A large number of Ethers will be necessary to run a Casper node. As a result, security is a very important issue.

The problem with the proposed implementation is that Ethers will be locked in a smart-contract, which will have the power to inflict penalties.

It means the smart contract will be able to withdraw Ethers from the account.

If something happens, such like a mistake, hacking, virus, middle man attack, spectre attack or anything you can imagine, Ethers might be stolen or lost.

At the same time, there is a very safe and reliable way to improve the security of Ethers stored for POS.

There are currently dozens of successful POS Masternode cryptocurrencies, which also require the deposit of large amount of coins, but in a safe way called “cold storage wallets”.

Masternode coins become more and more popular, with several dedicated websites : https://mntop.co.in , https://masternodes.pro , …

To run a masternode, you have to deposit the required amount of coins (for example 1000 coins), on an account.

It is very safe because you never have to disclose the private key of this account, nor have to sign anything with the private key.

In my opinion, the private key of the account on which huge amounts of coins are stored should never be disclosed until you decide to sell the coins. The private key should be kept safe, on a computer disconnected from the internet, or on a paper wallet. This is cold storage, which is the safest option possible.

As regards the way to implement cold storage security in Casper, just copy the masternode implementation. In order to run a Casper Node, just ask a large amount of Ethers to be deposited on an Ethereum account, without signing any smart contract with the private key.

In order to solve the “nothing at stake” problem, just implement an additional contract : for example, if the ethereum deposit is  1 000 Ethers to run a masternode, just pass a smart-contract on another account on which a small amount of Ethers would be locked (for example 10 Ethers).

The penalties would be applied on these 10 Ethers, without endangering the large deposit of 1 000 Ethers, which would benefit from cold storage security, the private key having never been disclosed in any way.

This implementation has many other advantages, besides from security :

- the large amount of Ethers could be withdrawed at any time, since it wouldn’t be locked in any smart-contract. The node would just be disconnected from the network.
- reach enough decentralization : if Casper is implemented without maximum security of deposits, I fear only the very core of early holders will run a Casper node, that’s to say those who have so many ethers that they can afford to lose 1 000 ethers in case something went wrong. Many secondary investors would feel unsafe to put at stake such large amounts of Ethers, without cold storage. So the system would be very centralized.
- reliability : masternode coins are well established, it’s always a good thing to benefit from proven solutions.
- boost in Ether price : cold storage masternodes are very popular, so implementing this solution in Casper would give an additional boost to the price of Ethers.

## Replies

**Etherbuddy** (2018-01-21):

Technically, people would pass a smart-contract from an account on which 10 Ethers are stored, and accept penalties on this account.

The smart contract would ask them to specify an Ethereum address of their choice, where the 1000 Ethers would be later deposited.

The smart contract would be signed, and the node would be activated by the deposit of 1 000 Ethers on the specified separate account.

This method enables to make sure that the contractor is linked to the 1 000 Ethers, since they are deposited on the account previously specified in the smart contract.

Additionally, this method would be a great opportunity for Ethereum freelancers, since they could invest 10 Ethers and make an agreement with a big Ether holder : freelancers with 10 Ethers would sign the smart contract and manage the node, while the Ether holder would deposit the 1 000 Ethers on the specified separate account. The dividend would be distributed on the account of the node manager freelancer, where the 10 Ethers are deposited, and he would pay a fraction of the dividend to the Ether holder who made the deposit of 1000 Ethers.

Contracts could last 1 month for example, or be unlimited contracts with monthly dividends, provided there are at least 10 Ethers for penalties and a deposit of 1 000 Ethers on the separate account.

So there would be a beneficial market, associating freelancers who are up to run Ethereum nodes, and big Ether holders who look for a passive income with minimum efforts and maximum security of their funds.

As a result, it would increase Ethereum popularity, since a problem with Casper is that Ethereum enthusiasts who don’t own 1 000 Ethers may feel excluded. With the proposed method, it would be possible even for small holders to run a full node, provided they make an agreement with a big Ether holder.

If it happens that the freelancer is not managing the node properly, he would have penalties or little dividend. As a result, the Ether holder would withdraw his deposit and look for another Ethereum freelancer. In my opinion, it would be a dynamic market, with new freelancers entering and trying to build a positive reputation.

---

**ldct** (2018-01-21):

> The penalties would be applied on these 10 Ethers, without endangering the large deposit of 1 000 Ethers, which would benefit from cold storage security, the private key having never been disclosed in any way.

I think this would not have the same economic finality guarantees as casper; if I’m following your example right, two conflicting checkpoints can be finalized, which means >= 1/3 of validators violated a slashing condition, BUT each validator only loses about 1% of their staked eth

---

**Etherbuddy** (2018-01-21):

Let’s assume we have a network of a few hundreds or thousands of validator nodes, which is common for masternodes cryptocurrencies.

The problem is to spot validators who behave badly.

Validators would communicate, and inform other validators when they estimate that one validator behaves badly.

Once a majority, or a supermajority of 2/3 of validators estimates that one validator is fraudulent, they just blacklist this node, which is not difficult to implement.

Spoting and blacklisting a fraudulent node does not cost a lot, so there’s no need for a huge penalty. 10 Ethers, which is 1 % of deposit, is more than enough.

---

**vbuterin** (2018-01-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/etherbuddy/48/586_2.png) Etherbuddy:

> It means the smart contract will be able to withdraw Ethers from the account.

This part is NOT true. The smart contract is able to trigger a slashing condition, which leads to ETH being destroyed and possibly allowing some account to claim 4% of that as a reward, but it cannot withdraw. When you deposit into Casper, you have to specify a withdrawal address which is separate from the staking validation code, and can be a cold storage address; funds can only be withdrawn to this address.

Furthermore, the newest design for Casper includes a feature where the percentage your account loses from slashing is proportional to the number of other validators that got slashed within the last N months, which means that unless a large attack is going on, you will not lose that much, so arguably having the staking key online can be fairly safe especially if you are a small validator.

---

**Etherbuddy** (2018-01-22):

Thanks for reading.

What I meant is that the smart-contract has an access to the Ethers deposited, since it can destroy some of them.

If there is the possibility of an implementation with a pure cold storage, without any access to the funds deposited, then the security is improved.

A cold storage, just like in masternodes implementation, gives the maximum security possible.

The penalties could be applied on a separate account containing a small fraction of the Ethers deposited.

---

**vbuterin** (2018-01-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/etherbuddy/48/586_2.png) Etherbuddy:

> If there is the possibility of an implementation with a pure cold storage, without any access to the funds deposited, then the security is improved.

Yes, but if you don’t have value at risk, then you can’t have economic finality.

---

**Etherbuddy** (2018-01-22):

There are values at risk, the fraction of Ethers stored on the separate account, for example 10 Ethers if the required deposit is 1000 Ethers.

---

**vbuterin** (2018-01-22):

Right, but then the value at risk is quite small even in the case of an attack. Personally I feel like our proposed approach of penalties being proportional to the percentage of other byzantine validators gets most of the best of both worlds here - low risk of funds in the normal case, full cryptoeconomic security in the exceptional attack case.

---

**ashishrp** (2019-09-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> proposed approach of penalties being proportional to the percentage of other byzantine validators

where can i read more about this?

---

**jgm** (2019-09-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/ashishrp/48/3647_2.png) ashishrp:

> where can i read more about this?


      ![](https://ethresear.ch/uploads/default/original/2X/9/9820c4fe404a7e163dc1dc0a8d644cddd3e4bc2a.png)

      [HackMD](https://notes.ethereum.org/@vbuterin/serenity_design_rationale?type=view)



    ![](https://ethresear.ch/uploads/default/original/2X/8/882285f3628ea3784835c306639dd8f62179a6d9.png)

###



# Serenity Design Rationale  See also: the 1.0 design rationale doc from 3-4 years ago https://githu

