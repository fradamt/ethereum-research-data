---
source: ethresearch
topic_id: 2630
title: Alert! Will Fomo3D destroy Ethereum?
author: toliuyi
date: "2018-07-21"
category: Miscellaneous
tags: []
url: https://ethresear.ch/t/alert-will-fomo3d-destroy-ethereum/2630
views: 13495
likes: 56
posts_count: 49
---

# Alert! Will Fomo3D destroy Ethereum?

The rocket raising dApp, [Fomo3D](http://exitscam.me/), has accumulated more than 17000 ether at present, mostly in last two days. I read the [contract code](https://etherscan.io/address/0xa62142888aba8370742be823c1782d17a0389da1#code) and wondering where the game heading and end up. One possible outcome ( tell me if you find another one ) is the game will attract a huge amount Ethers, and can do it again and again. Not to mention lots of me-too follower.  Ultimately, it will drain all liquidity of Ether and let the winner takes all. Then Ethererum’s network value will be largely destroyed.  And the question is: If a blockchain could be destroyed by an app running on it ( Fomo3D is absolutely valid, no hacking), is that a systemic defect of mechanism design?

I hope I’m wrong, please correct me if you can.

## Replies

**vbuterin** (2018-07-21):

If it just keeps on accumulating ETH, then that would just increase the value of the remaining ETH. If the ETH inside it does get to multimillion levels, then the natural two concerns are (i) someone finally wins, and gets all the money all at once, leading to market instability, and (ii) it gets hacked, with similar consequences.

---

**JustinDrake** (2018-07-21):

As I understand the winner of the jackpot is the last player. Because miners as a group decide who the last player is, my guess is that the jackpot will be won by one or more miners.

The size of the jackpot is already, after a couple weeks, large enough for large mining entities (in particular, mining pools) to attempt to win the jackpot. The game is designed to take a long time to conclude, so mining entities have time to strategise and write custom software implementing their strategy.

If there’s 1M+ ETH at stake my guess is that we will see dirty tactics being played out, such as:

- DoS attacks to temporarily take down mining entities (this could be networking level DDoS, transaction spam, exploiting a 0day, etc.)
- Transaction censorship to prevent changing the last player (e.g. mining empty blocks)
- Deviations from the canonical fork choice rule (block orphaning attacks, 51% attacks)
- Block withholding
- Renting out of mining power (see nicehash.com)
- Bribing contracts and/or collusion among the mining pools

The design space for bribing contracts is quite interesting and under-explored. One could imagine someone setting up a meta contract that breaks the winner-takes-all dynamics with a scheme that trustlessly divides the jackpot winnings among the miners that opt-in to do transaction censorship.

In any case this is uncharted territory, possibly with systemic risk, and it should be interesting to see it play out.

---

**virgil** (2018-07-21):

I too look forward seeing this play out.

---

**haydenadams** (2018-07-21):

Bribing contracts will be difficult since all functions have the modifier:

```
    /**
 * @dev prevents contracts from interacting with fomo3d
 */
modifier isHuman() {
    address _addr = msg.sender;
    uint256 _codeLength;

    assembly {_codeLength := extcodesize(_addr)}
    require(_codeLength == 0, "sorry humans only");
    _;
}
```

---

**haydenadams** (2018-07-22):

All functions with the modifier can’t be called by other smart contracts, only by normal accounts. This makes it much more difficult to coordinate a bribery attack.

In order of likelihood I would guess this ends with:

1. Mining Pool collusion / 51% attack
2. Exit scam through intentional backdoor
3. Hack
4. Stays open for a long long time and continues to accumulate

The last scenario is the most interesting to me, especially if it survives until POS. Has anyone estimated how much it will cost to keep it going for 1-2 years, with the key price increases?

---

**Umiiii** (2018-07-22):

[![WechatIMG163](https://ethresear.ch/uploads/default/optimized/2X/b/ba6569b5b14ec7559e02c3427578ca4dbae846ec_2_690x342.jpeg)WechatIMG163991×492 143 KB](https://ethresear.ch/uploads/default/ba6569b5b14ec7559e02c3427578ca4dbae846ec)

Here are the sheets made by one Chinese participant.

The column means:

Order | All keys | key price | All Invested ETH | Current ETH in Pot(Predicted by current situation) | The minimal Pot(with all select snake team) | The average Pot

---

**toliuyi** (2018-07-23):

I assume you have noticed this. ![:sweat:](https://ethresear.ch/images/emoji/facebook_messenger/sweat.png?v=14)[![WechatIMG328](https://ethresear.ch/uploads/default/optimized/2X/2/2bcaf4bafc4c761fb4569f6d383699d40fc18c89_2_281x499.jpeg)WechatIMG328750×1334 84.1 KB](https://ethresear.ch/uploads/default/2bcaf4bafc4c761fb4569f6d383699d40fc18c89)

---

**nootropicat** (2018-07-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/professionalkiwi/48/1707_2.png) ProfessionalKiwi:

> I read something about contracts that they cannot be caught by that test if a transaction is executed in it’s constructor. Is that correct?

correct, but in this case all that can achieve is locking funds in the contract, as it’s not possible to recreate a suicided contract in the same address.

![](https://ethresear.ch/user_avatar/ethresear.ch/haydenadams/48/944_2.png) haydenadams:

> All functions with the modifier can’t be called by other smart contracts, only by normal accounts. This makes it much more difficult to coordinate a bribery attack.

That doesn’t stop it. It’s always possible to create an arbitrary condition that requires a specific state verified by the state root with the help of BLOCKHASH opcode

The point of that modifier in this contract is to prevent selling keys

![](https://ethresear.ch/user_avatar/ethresear.ch/toliuyi/48/1040_2.png) toliuyi:

> I assume you have noticed this

He probably means ‘storing’ cheap gas in storage.

Using this would be a good thing imo.

---

**toliuyi** (2018-07-23):

Do you mean even the fallback function is guarded by isHuman modifier, it still could be called by a contract successfully? Would you please explain it further?

---

**nootropicat** (2018-07-23):

It can be called during creation, as the contract doesn’t yet contain any code, but msg.sender is set to its future address. However it would be impossible to withdraw funds later as the contract would have a nonzero code size then.

---

**toliuyi** (2018-07-23):

I see. Thanks a lot!

---

**fubuloubu** (2018-07-23):

As long writing contracts is more complicated than implementing these behaviors, I think the exact scamming/[skimming attacks](https://www.reddit.com/r/ethereum/comments/916xni/how_to_pwn_fomo3d_a_beginners_guide/) will continue to be the downfall of contracts trying to build these behaviors, versus it actually working and getting a large enough pot to suffer from these existential attacks. Definitely interesting to analyze however.

More on the security side, this contract used several anti-patterns (on-chain RNG most prominently) but I’m not sure that this specific problem with using code length to determine whether the originating account is a smart contract is among them. I think in general, it’s an anti-pattern to try to handle smart contracts and external accounts differently, but if there was a specific need I would probably use `tx.orgin == msg.sender` instead (as Nick Johnson mentioned in a reply)

Does anyone dispute this as an anti-pattern? Does Nick Johnson’s statement below best capture why this is an anti-pattern we should avoid?

“It shouldn’t matter if you’re being called by a smart contract or an external user, and if it does matter for some reason, you’re probably doing something dumb… [A]nything a contract can do, a miner can do with an external account, since they have total control over transactions in any block they mine.”

I don’t think this is covered in the various “lists of Ethereum bugs” people have floating around, so I would like to make sure this gets into one.

---

**haydenadams** (2018-07-23):

Good reddit thread on the topic:


      ![](https://ethresear.ch/uploads/default/original/3X/e/1/e1ae42106c51c881c83b6e2219e4b0c9d2aa617d.png)

      [reddit.com](https://www.reddit.com/r/ethereum/comments/916xni/how_to_pwn_fomo3d_a_beginners_guide/)





###

---

**Planck** (2018-07-23):

It seems like FoMo3D is exploiting an old game in economics, one that (probably) goes back to John Nash himself. It’s called the Dollar Auction and it’s taught at a lot of business schools (I taught it as a TA at Columbia, which is how I know it). As a result I would suspect that, whether this instantiation gets hacked or not, the game is here to stay. From the research I’ve seen, even repeated versions of this game don’t seem to improve play.

On the positive side things though, it seems like Smart Contracts could–in theory–provide a novel solution.

The basic argument is that Fomo Key purchases have a positive expected value because of the chance that nobody else will buy a new key before the timer expires. As a result of this, if someone can **credibly** commit to buying many keys, then nobody else should have a reason to buy a key at all. This is true since the odds that another key won’t be bought will = 0 which should 0 out their expected value.

Anyway I’m a little jet-lagged so I hope I’m not making some basic mistake, but this seems right. **Much** more difficult than how I’ve laid it out, but right.

I also sketched a preliminary Medium article on this issue, thanks to this thread. [You can read it here if you want](https://medium.com/@admin_44913/fomo3d-and-dangerous-game-theory-97bd5f47ab3b) (I give a shoutout to [@JustinDrake](/u/justindrake) .) Wasn’t sure if linking this ethresear.ch thread was ok, so I didn’t.

---

**PhABC** (2018-07-24):

I wish part of the Ethers sent (e.g. 50%) was destroyed by the smart contract to counterbalance the economical instability that could follow the winning of the pot.

---

**DaveyZ** (2018-07-24):

Please refer to the official FOMO3D wiki [here](https://fomo3d.hostedwiki.co/pages/Fomo3D%20Explained#pot-distribution) to better understand how the pot distribution is performed. Most of the concerns here seem to be centered around market instability by means of one winner receiving all the ETH. This simply is not true and I would have hoped commenters would take the time to read the contract before broadcasting their assumptions, as this creates a sense of baseless FUD.

Upon winning a pot, 48% of the sum of funds is sent to the winner, 2% to the community fund, and a varying amount to the next round, FOMO3D key holders, and P3D tokens which comprises the remaining 50%. The jackpot payout of ETH will indeed occur, but always in proportion to the amount of ETH otherwise redistributed upon a round’s completion. Additionally, there is an element of ETH redistribution during the game itself, as key holders receive ETH “dividends” and airdrops relative to their holdings and buys, respectively. Simply put, there is no singular winner to create market instability- not any more than a whale creating a new position in ETH.

---

**Planck** (2018-07-24):

Thanks for clarification. While you may be right that the network instability is attenuated, the features you mention are still just epiphenomenal to the main War of Attrition engine (at least as far as I can tell.)  This means that if the War of Attrition is “solvable” via a suitably funded commitment contract (like I propose above) the rest of the features don’t really matter going forward. Is this correct in your view?

---

**DaveyZ** (2018-07-24):

Let me first say, I think your reaction to the game was the most accurate and insightful first impression I’ve seen since the first beta release. My comment wasn’t necessarily toward you or anyone in particular, rather the general impression that this is some one-dimensional lottery. With your background, I’m sure you can find multiple elements of game theory within FOMO3D, not to mention the sociological and psychological elements.

Due to timer resets and interaction with unpredictable and/or irrational human behavior (i.e. FOMO), there is no smart contract which could “solve” the game. Each *individual key* (not purchase) that is purchased triggers multiple actions: it increases the duration of the game by 30 seconds (to a maximum of 24 hours), increases the pot size, pays out “dividends” to key holders, and raises the price of subsequent keys. The only feasible ways any particular round could end, in my opinion, do not involve the use of any type of automation. As a reminder, GWEI experiences fluctuation. This will only increase during a battle of transactions, when senders are forced to increase GWEI to an unknown amount in order to ensure their transactions are verified before their competitors. In my opinion, the only way a round can be won will be due to unforeseen lack of interest (infinitely unlikely), network congestion (organic or malicious), collusion amongst players, or a lack of liquid ETH (highly unlikely). Simply put, this game was created for pot size and participation to increase in parallel, therefore avoiding any point of intersection and making a resolution “unsolvable” and entirely anomalistic.

---

**Planck** (2018-07-24):

> Let me first say, I think your reaction to the game was the most accurate and insightful first impression I’ve seen since the first beta release

I appreciate the kind words and your thoughtful response. It sounds like you might be a dev–or at least someone who’s thought about this game for awhile–and you’ve clearly got interesting things to say about it. However, it does still seem to me that the “commitment strategy” I outlined should beat this game in theory and, eventually, in practice.

To wit:

If Zuckerberg irrevocably stakes his fortune on buying key every time the game duration ticks near zero, nobody poorer than Zuck could possibly win (edit: someone with .5 plus epsilon of the voting currency also has strong bargaining power). He’ll only be buying keys when the game is almost over so he will only pay once the contract is petering out. More importantly he should actually be able to (*in theory*) completely eliminate new bids from the start, which would guarantee him the prize for the cost of one key.

But yes, that’s *in theory*. In practice all kinds of things can happen, but note that the contract can also be much cleverer than what I’ve described. It could, for instance, offer some proportion of the prize pool to anyone who reimburses the contract’s *actual* key purchases. Which means that even the F3D Whales may prefer to purchase these “second hand” keys, since they have a *much* higher probability of winning.

Ultimately, I do think it’s solvable with a good smart contract, a media platform, and a suitable stake. But I also *hope* it’s solvable (and I hope you hope so too!)

---

**DaveyZ** (2018-07-24):

You reminded me that I should be very clear I am *not* a developer or even a moderator of any kind. I’m simply someone who has been watching this team closely as I think they have some of the best solidity developers in the world. In the grand scheme of things, I have not seen many multi-billion dollar projects do what this team has done with virtually nothing but time and diligence.

I think you make some great points with your comparison, especially with the potential for a third party market. The unknown human element occurring alongside smart contract game theory is a large part of the excitement I have. I wish everyone viewed this with an open mind instead of bias or wishes of failure. Regardless which of the countless outcomes occur, it will be a very interesting ride– one which will potentially influence other game theory smart contracts. Should it succeed in popularity, this could be the dawn of yet another smart contract application (albeit unexpected) not too different from rise of browser games from the unprecedented creations of Shockwave and Flash.


*(28 more replies not shown)*
