---
source: ethresearch
topic_id: 12670
title: Faucet Link Directory
author: desy
date: "2022-05-19"
category: Miscellaneous
tags: []
url: https://ethresear.ch/t/faucet-link-directory/12670
views: 21822
likes: 52
posts_count: 56
---

# Faucet Link Directory

I made a link directory of all testnet faucets for Kovan, Rinkeby, Goerli and Ropsten. It monitors liveliness and shows details like drop size and type of sybil protection, so you can get directly to those that are currently working. Let me know of faucets not listed and I will add them.

 → https://faucetlink.to

If you have spare testnet coins, please send some to the faucets with low balance to keep them going. Most that don’t work are just empty but actually work fine…

## Replies

**abcoathup** (2022-05-20):

Need to add Sepolia testnet.

Given the design of the site, rather than having to select a network, then select the actual network you could show the various testnets in one pages as a table.

---

**desy** (2022-05-20):

thought the same at first, but was a bit crowded with all the info in a single table…

good idea with Sepolia, added ![:+1:](https://ethresear.ch/images/emoji/facebook_messenger/+1.png?v=10)

---

**abcoathup** (2022-05-20):

The reason for the single table is to avoid having to make two clicks.  The click to get to the networks should be removed at least.

---

**abcoathup** (2022-05-23):

[@desy](/u/desy) are you on Twitter?  There isn’t a contact link for you on the faucet link website.

---

**desy** (2022-05-24):

You’re right the first button is pretty pointless, although I kinda like how clean the startpage is that way…

I don’t have contact infos for this account, but you can send me a message here on the forum.

---

**pk910** (2022-06-19):

That’s a great page! Thank you ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=10)

I’ve created 2 new instances of my PoW faucet for ropsten & sepolia:

https://ropsten-faucet.pk910.de/

https://sepolia-faucet.pk910.de/

Wallet address is the same as for the other testnets: 0x6Cc9397c3B38739daCbfaA68EaD5F5D77Ba5F455

I’ve added an api to fetch the live drop size from my faucets, as I might need to adjust them based on how fast it gets drained.

You can fetch it via  {faucet-host}/api/getMaxReward  for each faucet ![:grinning:](https://ethresear.ch/images/emoji/facebook_messenger/grinning.png?v=10)

The number returned is the max reward in wei.

---

**desy** (2022-06-21):

Awesome, thanks for adding more networks. Also kudos for using pow, cool to see faucets implementing new ways to prevent sybils.

Your api has been hooked up of course ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=10)

---

**pk910** (2022-08-03):

Hello again ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

I’ve moved the funds from my goerli & sepolia faucets to a separate contract (0xA5058fbcD09425e922E3E9e78D569aB84EdB88Eb) for rate limiting and protection.

Don’t know if you want to include it to the faucet balance? Otherwise it just shows the balance of the hot wallet.

Similar situation for [goerlifaucet.com](http://goerlifaucet.com) faucet balance…

They’ve spread their funds to 8 wallets and use them in parallel:

0x5Ff40197C83C3A2705ba912333Cf1a37BA249eB7

0x87c9B02A10eC2CB4dcB3b2e573e26169CF3cd9Bf

0x7Ed746476A7F6520BABD24eeE1fDbCD0F7FB271f

0x631E9B031b16b18172a2B9D66C3668A68a668d20

0xEDaf4083F29753753d0Cd6c3C50ACEb08c87b5BD

0x2031832e54a2200bF678286f560F49A950DB2Ad5

0xA7E4EF0a9e15bDEf215E2ed87AE050f974ECD60b

0x3C352eA32DFBb757CCdf4b457E52daF6eCC21917

They’ve also increased their drop size to 0.25

And I’ve seen another faucet for Sepolia:

https://faucet-sepolia.rockx.com/ (Sepolia / 0.1 ETH / Twitter / 0x0d731cfabC5574329823F26d488416451d2ea376)

---

**pk910** (2022-08-04):

And two more for Ropsten/Goerli/Kovan/Rinkeby:

https://bitszn.com/faucets.html  (0x6432741b9525f5f341D74787C5E08cb9Fa2bB807 for all testnets)

https://www.allthatnode.com/faucet/ethereum.dsrv  (0x08505F42D5666225d5d73B842dAdB87CCA44d1AE for all testnets, but drained on all ![:frowning:](https://ethresear.ch/images/emoji/facebook_messenger/frowning.png?v=12) )

---

**kkonrad** (2022-08-06):

hey folks, thanks for building this. as a major thank you for donating your test eth back to the faucets, we created an nft collection that you can mint for free. check it out https://faucetdonors.xyz/

[@desy](/u/desy) it’d super cool if you could link back on the faucetlink.to. we also link to you on https://faucetdonors.xyz/

[@pk910](/u/pk910) you made it to the leaderboard ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

simply click mint ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**pk910** (2022-08-06):

Heya [@kkonrad](/u/kkonrad)

Thanks for the appreciation. I’m claiming it when gas costs are lower ![:smiley:](https://ethresear.ch/images/emoji/facebook_messenger/smiley.png?v=12)

Where is that total amount (4121.0Ξ for me) coming from?

I’ve developed the faucet, but didn’t own enough funds to run it ![:sweat_smile:](https://ethresear.ch/images/emoji/facebook_messenger/sweat_smile.png?v=12)

So its all coming from one or two funders per network ![:man_shrugging:](https://ethresear.ch/images/emoji/facebook_messenger/man_shrugging.png?v=12)

But I can’t see the addresses of q9f or roninkaizen on the list (they’ve funded all currently active faucets on goerli)

---

**Hugo0** (2022-08-07):

Hey hey [@pk910](/u/pk910)

Here’s all txs with your address:

[![image](https://ethresear.ch/uploads/default/original/2X/0/02a454d2cc1da763d94d561b47be3b6e62dc290a.png)image664×886 38.5 KB](https://ethresear.ch/uploads/default/02a454d2cc1da763d94d561b47be3b6e62dc290a)

The bulk of it seems to be two transactions in the Sepolia testnet at block 1333849. Please let me know if you think something is wrong here! We’d have to review the methodology ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)

Also, re minting costs, I’m not sure what’s wrong with Metamask, but it tends to estimate 10x higher transaction costs than it actually ends up being. Gas fees are ~200k, which is like 2-3 bucks depending on price. Not sure if maybe the merkle tree is the confusion source here.

Are these the addresses or q9f & roninkaizen? I’ll look into what’s happening there

- 0xe611a720778a5f6723d6b4866F84828504657181 (q9f)
- 0x00933A786Ee4d5d4592c0D1cF20B633C6A537f5f (ronin)

---

**pk910** (2022-08-07):

Heya,

Seems like you’re processing transactions twice ![:laughing:](https://ethresear.ch/images/emoji/facebook_messenger/laughing.png?v=12)

The 2000 ETH transaction on sepolia is there twice and the 80 ETH transaction on ropsten too.

You should filter out duplicate transaction hashes.

Also just handling incoming transactions seems a little unfair… In my case I had used 2k ETH I mined myself for the initial funding on sepolia, but later transfered 1k back as I got a proper funding from a genesis fund holder… I’d subtract amounts transfered back to a address after funding from the funding balance ![:wink:](https://ethresear.ch/images/emoji/facebook_messenger/wink.png?v=12)

So for me it’d be a total amount of 1101 ETH only.

Goerli address for q9f is 0xe0a2bd4258d2768837baa26a28fe71dc079f84c7

(Funding TX 0xb4e5018869f2dd9a06b9e01d06acece29489f122632198c18ff2e3323550c933

& 0x9ed3f4a571de2abc739eaec4eefe45c22c93dd38901962b520064240fe7e6b08)

I don’t know his mainnet wallet address and cannot verify q9f.eth is really q9f ![:sweat_smile:](https://ethresear.ch/images/emoji/facebook_messenger/sweat_smile.png?v=12)

Goerli wallet for ronin is 0x9d525e28fe5830ee92d7aa799c4d21590567b595

(Funding TX: 0x28b44cc6206a16b4f4624b5b1914dbce2c81c73da08c7db058789d7fa66d250b)

His mainnet address is 0x00933A786Ee4d5d4592c0D1cF20B633C6A537f5f

Hmm, that’s a little bit off-topic… I think you should create a separate thread ![:smiley:](https://ethresear.ch/images/emoji/facebook_messenger/smiley.png?v=12)

---

**desy** (2022-08-10):

[@pk910](/u/pk910) updated ![:+1:](https://ethresear.ch/images/emoji/facebook_messenger/+1.png?v=12)

[@kkonrad](/u/kkonrad) cool! is there a threshold to qualify for mint? Problem may be that only a few people have sizeable amounts of testnet coins. Imo anyone holding a larger amount of testnet eth should send some to faucets regardless… It’s just 2 clicks, get your shit together testnet whales lol

---

**kkonrad** (2022-09-07):

Being in the top 1000 qualifies you. Does it not work for you?

---

**pk910** (2022-10-21):

Heya,

Found another faucet for Goerli:

https://unitap.app/  (Goerli / 1 ETH / BrightID / 0xb3A97684Eb67182BAa7994b226e6315196D8b364)

I’ve seen you’ve cleaned up your page a bit and showing min-max ranges for drop sizes now ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

If you like you can show the min amount for my faucets too.

You can fetch it via {faucet-host}/api/getFaucetConfig which returns a json with all the configuration parameters. “minClaim” & “maxClaim” are the interesting ones for your site ![:wink:](https://ethresear.ch/images/emoji/facebook_messenger/wink.png?v=12)

---

**desy** (2022-10-29):

[@kkonrad](/u/kkonrad) i was testing with a new address but didn’t make it in the list, I assume it’s a static snapshot?

[@pk910](/u/pk910) cool, hooked it up ![:+1:](https://ethresear.ch/images/emoji/facebook_messenger/+1.png?v=12) sad to see your faucet becoming harder to use, I guess there’s a lot of idle hashpower sitting around since the merge ![:neutral_face:](https://ethresear.ch/images/emoji/facebook_messenger/neutral_face.png?v=12) Maybe reduce the minimum claim limit?

I have removed 3 of the empty faucets which would get drained if they’d receive coins (not enough sybil resistance or drop size too high). All the remaining ones are safe to fill, friendly reminder for whales to do so. This has been a problem for years, causing developers to waste countless hours engaging with dead or throttled faucets. Not sure why this is even an issue.

---

**pk910** (2022-10-30):

Yea, it’s unfortunately getting harder every day as more people are “mining” ![:frowning:](https://ethresear.ch/images/emoji/facebook_messenger/frowning.png?v=12)

There is a hard limit of 2000 GöETH per day and the difficulty adjusts automatically to meet this limit.

The total hashrate currently almost doubles every week.

I’d be happy to increase the limit, but unfortunately I personally don’t own much goerli funds and I want to prevent it from being drained too fast.

I’ve lowered the min amount a little bit, but I need to make sure there are not too many transactions, or it’ll be stuck…

---

**desy** (2022-10-31):

Simply increasing the limit will probably not help that much, since most funds get drained by a few people with outsized hashpower. I think the only solution is to shift some weight towards other methods… How about letting users solve additional captchas during mining, and use the number of solved captchas as some multiplicator of the hashrate?

---

**pk910** (2022-11-05):

Hmm, that would require constant monitoring of the page for captchas that ‘randomly’ pop up…

I think that’s too much for any user ![:smiley:](https://ethresear.ch/images/emoji/facebook_messenger/smiley.png?v=12)

And I actually don’t think it’s all mined by a few people with heavy machines.

There are thousands of sessions every day, most residential IP ranges (hosting & proxy IPs don’t get anything). I think it’s real demand as there are many people migrating their stuff from the deprecated testnets (rinkeby & ropsten).

There are also “Incentivized Testnets” of various projects that introduce additional load on goerli as they offer being included on a mainnet airdrop for testing their stuff…

It was decided a few days ago that there won’t be any technical change to fix the funding situation on goerli.

developers should head over to the sepolia testnet instead.

I think goerli will slowly die in the next year and that’s unfortunately very bullish for fund sellers in the meantime ![:frowning:](https://ethresear.ch/images/emoji/facebook_messenger/frowning.png?v=12)

Especially because of that steady growing financial benefit for collecting goerli funds, the rewards of my faucet won’t be higher again anytime in future - it’ll rather be even lower.

There are currently ongoing efforts to launch a new ephemeral testnet for stakers to test validators without relying on goerli. Let’s see how this goes ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

Btw: faucetlink shows the alchemy faucet as not working, but it is working ![:wink:](https://ethresear.ch/images/emoji/facebook_messenger/wink.png?v=12)


*(35 more replies not shown)*
