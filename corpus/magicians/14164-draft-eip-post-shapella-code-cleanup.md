---
source: magicians
topic_id: 14164
title: "Draft EIP: Post-Shapella code cleanup"
author: MikeSylphDapps
date: "2023-05-08"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/draft-eip-post-shapella-code-cleanup/14164
views: 293
likes: 0
posts_count: 1
---

# Draft EIP: Post-Shapella code cleanup

Last month the Shapella upgrade added withdrawal capabilities to mainnet. While there was a lot of interest in this feature initially, it has waned significantly as we have gotten further from the hardfork.

As of this writing the withdrawal queue is completely empty. Users have stopped using this feature entirely!

![image](https://ethereum-magicians.org/uploads/default/original/2X/a/a2ddcc024517efbf3700d0de84a6443a457a90a4.png)

What most likely happened was people saw this new feature available and decided to try it out, but quickly bored of it, preferring the existing “help secure the network” feature over the new “stop helping secure the network” feature. This is not surprising as many of the people in the staking community believe strongly in the merits of decentralization and would be more inclined to continue helping secure Ethereum.

It is a software engineering best practice to remove features that users are no longer using. The benefits:

- It keeps the codebase slim and maintainable. Why complicate your codebase with code that is no longer used?
- It shortens development cycles. With dead code removed no mental energy needs to be expended by teams on how to develop new features that might interact with that dead code.
- It creates a better user experience because it simplifies their mental model of the application. No need to take up a user’s precious brainspace with commands that they don’t intend to use!

Kudos are certainly in order for all the client teams and everyone else who brought withdrawals to mainnet! The entire POS project was a monumental undertaking, so I know you must be heartbroken to see that this particular component of it ended up being a big flop with users. We owe it to you to push through an EIP that reverts each client to its pre-Shappela codebase so you can continue building out the most secure decentralized network out there without the technical debt that comes along with maintaining a feature that no one uses.

Let’s consider a [21st amendment](https://constitution.congress.gov/constitution/amendment-21/#:~:text=The%20transportation%20or%20importation%20into,laws%20thereof%2C%20is%20hereby%20prohibited.)-style EIP.
