---
source: magicians
topic_id: 8624
title: What happens to wallets when we die?
author: web3warren
date: "2022-03-16"
category: Web > Wallets
tags: [nft, wallet, gas, beneficiary, death]
url: https://ethereum-magicians.org/t/what-happens-to-wallets-when-we-die/8624
views: 971
likes: 4
posts_count: 4
---

# What happens to wallets when we die?

A secure beneficiary feature which transfers access to a wallet from its current passphrase to a new passphrase after a custom period of wallet inactivity, likely 1-5 years. This feature may be customized or deactivated by accessing the wallet with the owner’s original passphrase at any time prior to exceeding their chosen inactivity limit.

This feature allows the owner security and peace of mind by never needing to share their current passphrase with anyone. The replacement passphrase is presented upon activation of the beneficiary feature so it can be shared with someone or stored elsewhere without fear of the owner’s wallet being compromised while they’re still using it.

Put simply, the beneficiary feature is a passphrase reset activated upon wallet inactivity. Since the passphrase changes to a predetermined passphrase there’s no need to transfer the contents to a different wallet and pay gas/fees. **No longer will wallets go lost and unopened when folks die!** I’ll be able to leave my NFT collection to my family without concern. ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

*Feel free to follow me on Twitter @ web3warren*

## Replies

**high_byte** (2022-05-22):

that’s one use of social recovery. of course this will require smart wallets.

---

**SoundMoney** (2022-09-03):

This is possible today without any changes to Ethereum - I just don’t know of any solutions with a good UX.

On a technical level, you could do the following:

- Code a smart contract that holds and controls your Ethereum assets (ETH, ERC20s, ERC721s, …)
- The smart contract has two roles, admin role and lawyer role
- Admin is you. You don’t share this key with anyone. As long as you’re alive, you can control all the assets in the smart contract without limitations.
- There is a time-decay lock that enables the lawyer role to take control of the assets, but only after time T
- Admin can always extend T

In practice, you can set T to a year in the future, and as long as you’re alive you extend T every year, by a year. If you die then your family has to wait for a maximum of one year to access the assets. Obviously you can also give the lawyer key to a family member directly.

---

**zergity** (2025-11-26):

It’s possible now with EIP-7702, see [InheritableEOA: inheritance/recovery over inactivity (with EIP-7702)](https://ethereum-magicians.org/t/inheritableeoa-inheritance-recovery-over-inactivity-with-eip-7702/25382)

