---
source: magicians
topic_id: 15596
title: Ethereum yellowpaper metathread
author: RenanSouza2
date: "2023-08-29"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/ethereum-yellowpaper-metathread/15596
views: 908
likes: 9
posts_count: 7
---

# Ethereum yellowpaper metathread

Hey everyone, I am currently working in updating the yellowpaper to more current specifications, so far this are the EIPS I am including in it

London

EIP-1559: Fee market change for ETH 1.0 chain

EIP-3198: BASEFEE opcode

EIP-3529: Reduction in refunds

EIP-3541: Reject new contracts starting with the 0xEF byte

EIP-3554: Difficulty Bomb Delay to December 1st 2021

Gray Glacier

EIP-5133: Delaying Difficulty Bomb to mid-September 2022

Paris

EIP-3675: Upgrade consensus to Proof-of-Stake

EIP-4399: Supplant DIFFICULTY opcode with PREVRANDAO

Shanghai

EIP-3651: Warm COINBASE

EIP-3855: PUSH0 instruction

EIP-3860: Limit and meter initcode

EIP-4895: Beacon chain push withdrawals as operations

EIP-6049: Deprecate SELFDESTRUCT

Also, there are some mismatches between the yellowpaper and the specifications, EIP684 was born aout of it. What I want to know from you is, what changes/additions/subtractions would you make in the yellowpaper?

Also, this threat itself is an attempt to organize efforts in this front, I’m open to suggestions

## Replies

**RenanSouza2** (2023-08-29):

One suggestion I would like to make is to have one yellowpaper for consensus layer and another one for execution layer, let me know what everyone thinks

---

**Mani-T** (2023-08-31):

Nice idea. Separate papers could allow for more accurate and up-to-date documentation of each layer, reducing discrepancies and confusion.

---

**RenanSouza2** (2023-09-02):

Another reason I want to do that is because other chains tend to change the consensus and keep the execution mostly the same, this way this yellowpaper-EL could still be useful for more than Ethereum

---

**JoakimEQ** (2023-09-05):

Great idea! Let me know if I can help!

---

**ronyszu** (2023-09-18):

Let me know if I can help too!

---

**RenanSouza2** (2023-09-21):

Finnaly got to some writing,

my modifications can be found at [GitHub - RenanSouza2/yellowpaper at ravamp/1559](https://github.com/RenanSouza2/yellowpaper/tree/ravamp/1559), as the branch name says I am first doing EIP 1559,

Any suggestions or remarks are appreciated ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

