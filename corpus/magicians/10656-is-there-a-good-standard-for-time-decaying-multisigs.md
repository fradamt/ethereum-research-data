---
source: magicians
topic_id: 10656
title: Is there a good standard for time-decaying multisigs?
author: SoundMoney
date: "2022-09-03"
category: Web > Wallets
tags: [wallet]
url: https://ethereum-magicians.org/t/is-there-a-good-standard-for-time-decaying-multisigs/10656
views: 582
likes: 0
posts_count: 3
---

# Is there a good standard for time-decaying multisigs?

I’d like to implement the following multisig smart contract:

- 2/3 multisig until time T
- At time T the multisig becomes a 1/3
- Any signer can increase T

I only want to store ETH for now, but ERC20 support would be a plus.

Would appreciate any code pointers!

Also open to philosophical feedback as to whether this is a good vault. I like it because the vault is not less secure than a standard 2/3 multisig as long as T is extended frequently. And if the owner loses 2 keys, they can recover the vault after T as long as nobody else knows any of the keys.

## Replies

**Pandapip1** (2022-09-03):

Personally, I would have the following properties on it:

- Can send ether and submit arbitrary transactions
- When a key is used, a time delay is set to remove that key from the multisig altogether. This gets cleared when a new time delay for that key is set.
- New keys can be added and old ones removed with a 2/3 supermajority (rounded down)
- Keys can remove themselves

---

**TimDaub** (2022-09-04):

I could imagine EIP-4973 to be helpful here. Among themselves, the parties could “give” or “take” account-bound tokens" that signal membership over a shared account. A contract holding the funds could then be set up such that for withdrawing Ether, a quorum of ABT holders would have to accept the transfer. Additionally, it could be set up where any holder of the ABT may increase T.

