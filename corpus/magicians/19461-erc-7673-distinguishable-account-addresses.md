---
source: magicians
topic_id: 19461
title: "ERC-7673: Distinguishable Account Addresses"
author: wjmelements
date: "2024-03-31"
category: ERCs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-7673-distinguishable-account-addresses/19461
views: 1385
likes: 17
posts_count: 10
---

# ERC-7673: Distinguishable Account Addresses

[github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/354)














####


      `master` ← `wjmelements:distinguishable-addresses`




          opened 11:43PM - 31 Mar 24 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/2/2ec0a9961391a073978afe4555db21ceb20b5470.jpeg)
            wjmelements](https://github.com/wjmelements)



          [+373
            -0](https://github.com/ethereum/ERCs/pull/354/files)







When opening a pull request to submit a new EIP, please use the suggested templa[…](https://github.com/ethereum/ERCs/pull/354)te: https://github.com/ethereum/EIPs/blob/master/eip-template.md

We have a GitHub bot that automatically merges some PRs. It will merge yours immediately if certain criteria are met:

 - The PR edits only existing draft PRs.
 - The build passes.
 - Your GitHub username or email address is listed in the 'author' header of all affected PRs, inside <triangular brackets>.
 - If matching on email address, the email address is the one publicly listed on your GitHub profile.












Addressing several recurring topics in this forum, this will improve the resiliency of account addresses against spoofing attacks.



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rook/48/10951_2.png)

      [Patch Proposals For The Ongoing Wallet Homomoroph Attacks](https://ethereum-magicians.org/t/patch-proposals-for-the-ongoing-wallet-homomoroph-attacks/16686) [Security Ring](/c/working-groups/security/14)




> Losses from homomorph walles has suprassed $60m: https://gbhackers.com/create2-bypass-wallet-security-alerts/
> (edit) The above article is mistaken, this has noting to do with the create2 opcode, and rather a shortcut in wallet germination making it easier to search the wallet keyspace for viable wallets to use in this attack.
> Even today I made a transaction, and noticed that a contract was deployed with a wallet that looks very similar to my own. So, clearly there is some shortcut here that al…



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/16173_2.png)

      [ERC: Short Representation for Leading Zeros in Address](https://ethereum-magicians.org/t/erc-short-representation-for-leading-zeros-in-address/17538) [ERCs](/c/ercs/57)




> Hi, as I presented in previous AllWalletDevs about a proposal to represent leading zeros in address which reduces chance of phishing, I am thinking of starting an ERC.
> Motivation
>
> reduce phishing
>
> Specification
> The format will be 0{N}xAA..BBBB, where
>
> N is the number of leading zeros in decimal form
> AA is the two hex digits of two digits since first non-zero hex digit
> BBBB is the last four hex digits
>
> Rationale
>
> We choose 0{N}x format so it can be easily differentiate from 0x
> We choose 2 digit…

## Replies

**wjmelements** (2024-03-31):

[![spoofing-erc](https://ethereum-magicians.org/uploads/default/optimized/2X/1/1bdcac907e52629bb12088fc8965ae08a11ad27d_2_690x351.jpeg)spoofing-erc1460×744 213 KB](https://ethereum-magicians.org/uploads/default/1bdcac907e52629bb12088fc8965ae08a11ad27d)

---

**eawosika** (2024-04-01):

Cross-posting from X for discussion:

> My proposed ERC-55 extension will particularly favor those who are into astrology and want Ethereum address to reflect their identity. Are you a fiery Aries or a strong Libra? Now you can make your Ethereum address reflect that. And you don’t even need to look too far to find suggestions on which emojis to use: https://pinterest.com/pin/the-best-emojis-for-your-zodiac-sign--778559854304614636/

Btw, [@wjmelements](/u/wjmelements) I just went through the [Patch Proposals For The Ongoing Wallet Homomoroph Attacks](https://ethereum-magicians.org/t/patch-proposals-for-the-ongoing-wallet-homomoroph-attacks/16686) discussion thread. I believe that inspired this proposal?

---

**wjmelements** (2024-04-01):

[@bumblefudge](/u/bumblefudge) inspired the proposal.



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/bumblefudge/48/7449_2.png)
    [ERC: Short Representation for Leading Zeros in Address](https://ethereum-magicians.org/t/erc-short-representation-for-leading-zeros-in-address/17538/4) [ERCs](/c/ercs/57)



> If you like Base58-style encoding gymnastics, you are gonna LOVE the multibase project over in IPFS land:

---

**eawosika** (2024-04-01):

I followed the [link](https://github.com/multiformats/multibase/pull/88) in [@bumblefudge](/u/bumblefudge)’s post (just because) and found some explanations of the rationale for adding support for base256 emojis:

> It’s fun and allows us have an almost endless of fun in docs and trolling opportunities.
>
>
> Most of the NFT community likes useless differentiation features, why not giving what they want?

Feels like we should incorporate these considerations into the design of ERC-55 (or the proposed extension). ERCs aren’t always designed from a fun-theoretic perspective, which should make ERC-55 quite special.

---

**wjmelements** (2024-04-01):

I think you are mistaken about erc-55. erc-55 has been around since 2016. This proposal replaces erc-55.

https://eips.ethereum.org/EIPS/eip-55

---

**eawosika** (2024-04-01):

I think I was feeling confused at first when I saw “ERC-55”; I always assumed ERC numbers could only move up. But then I thought “maybe this is a special case”. Eliezer Yudkowsky would be sorely disappointed I didn’t do a better job of [noticing my own confusion](https://www.lesswrong.com/s/zpCiuR4T343j9WkcK/p/5JDkW4MYXit2CquLs) in this case.

---

**bumblefudge** (2024-04-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/eawosika/48/11179_2.png) eawosika:

> ERCs aren’t always designed from a fun-theoretic perspective, which should make ERC-55 quite special.

For the record, multibase has an IANA-style REGISTRY attached to it, and the base256 REGISTRATION was motivated by shits, giggles, and trolling as a kind of thought-experiment testing the limits of the base-encoding system, by someone who wanted to show how UNAMBIGUOUS BIDIRECTIONAL translation between binary and various alphabets could have all kinds of useful properties beyond compaction and disambiguation (in the case of base58btc, for ex.).  I don’t think the tone of the registrant’s PR comments should reflect too negatively on the more serious efforts at translating between the most compact encoding each transport will allow in a multi-transport system.  (It is entirely fair to use it as an argument against permissionless/use-case-neutral registries, tho!)

---

**abcoathup** (2024-04-03):

Given there are a much larger range of emojis, could we not make more use of this range?  base 2048?

“3,782 emojis in the Unicode Standard, as of September 2023.”

From: [FAQ](https://emojipedia.org/faq#how-many)

---

**wjmelements** (2024-04-03):

When there are more standardized emoji I would support that. For 2048 we still have the freedom to deselect less-appropriate emoji like government flags. But 2048 is `2**11` and so the encoding becomes more complex because 11 does not divide 160, as 8. Another disadvantage is in the detection of addresses in the wild; it is important to distinguish an address from a random string of emoji. When there are more than 65536 to choose from it will be convenient for `2**16`. Encoding with base 2048 is still possible of course, and would shorten the address length to 15 characters.

