---
source: ethresearch
topic_id: 3405
title: A potential attack vector on PoS based smart contract platforms
author: gloine
date: "2018-09-17"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/a-potential-attack-vector-on-pos-based-smart-contract-platforms/3405
views: 1672
likes: 8
posts_count: 6
---

# A potential attack vector on PoS based smart contract platforms

There is one problem which has been bugging me recently. Let’s say I create a smart contract on which users can stake Ether in the same way Casper staking is done, and reward them slightly better than what they can earn from Casper staking. Wouldn’t an economically optimal behavior be moving to this new contract and increase their profit?

In this case, I am afraid the attacker can simply pay for the total amount of transaction fee for the whole network and halve the network security for a given period (+staking period, say Casper profit is 5% a year, doing this for half a year will require 2.5% of the stake amount). If the attacker pays for double of the fee amount, the security (i.e. total amount of deposit for PoS) will become 1/3, and so on.

I think this is a very similar issue to decentralized oracle - it seems to be impossible to obtain a safe decentralized data feed oracle mechanism which is independent of the value of the data feed (i.e. expected profit by faking the feed). In other words, if Ethereum starts to host valuable DApps whose operation requires staking some Ether, the security of the network would be affected by unwanted staking competition between the DApp and the network itself.

How do you think? Should DApps staking Ether be refrained from?

## Replies

**gloine** (2018-09-19):

Hmm…does anybody think there is a hole in the logic above? I have given some more thoughts to it - we expect the total amount of Casper stake does not increase indefinitely since the profit rate decreases as the amount of stake increases. Perhaps if an attacker opened up a new contract and promised the same profit, the number of participants would increase too, making the attack more expensive. However I think the amount of capital willing to participate in the staking process is a continuous function of the profit rate, thus the impact would be minimal unless the attacker proposes a significantly higher profit rate.

---

**dlubarov** (2018-09-19):

I think the argument makes sense in theory. Are you envisioning a smart contract that pretends to be doing something innocuous, but its true motive is to weaken Casper’s security? Or are you concerned that even if the malicious motive is transparent, stakers may selfishly stop staking and enter the contract anyway?

If the contract is pretending to be innocuous, I feel like it’d be hard to justify needing massive deposits. What sort of legitimate use cases can you think of? Perhaps some cryptocurrency which uses Ethereum as a base layer, but has its own PoS consensus mechanism, using ETH tokens as the unit of stake? But the currency would need to be massively successful in order to justify Casper-scale deposits, so developing and promoting the currency would be a huge undertaking.

If the motive is transparent, in theory we could still have a tragedy of the commons, where many selfish stakers participate anyway to maximize their own gain. In practice, I expect most large organizations would not participate out of fear of legal repercussions, but maybe a lot of individuals would. Individuals could participate secretly (perhaps using a mixer + Tor for network privacy), but secrecy is more difficult for large organizations.

Also if the motive is transparent, at least we would have a heads up that the attack is coming, so delays could be added to exchange withdrawals, cross-chain swap systems, etc. for extra safety. That would give responders more time to detect a double spend attack, freeze any withdrawals, and organize an emergency hard fork to sort things out.

---

**vbuterin** (2018-09-19):

If some stakers drop out to join the attack contract, the staking interest rate offered to the rest will rise, and more will come in to take their place. So I don’t see this as being a very large concern.

---

**gloine** (2018-09-19):

I was thinking about potential attack vectors at first, but realized later that this could happen accidentally by some successful dapps requiring Ether stakes with higher expected return (e.g. Fomo3D type of dapps?). Attackers may wait patiently and grab those opportunities to compromise the system. I am sure the community can detect it since we will see the amount of PoS staking being reduced over a few months. Thus, no problems if we plan for a hard fork in this case, but it would be better if this could be systemically prevented.

---

**gloine** (2018-09-19):

Thank you for pointing this out! So the actual interest rate attackers need to pay to halve the security is sqrt(2) ~= 1.414 times of the current interest rate, and sqrt(3) ~= 1.732 times for making it 1/3. Those should be the interest rates in equilibrium - in this case, the amount of stake on the attack account should increase significantly due to the higher interest rate. There should be some rules between the interest rate and the total amount of deposit in bank accounts…perhaps 3-4 times more deposit for 1.414 times interest. Then the attacker needs to pay 2.5% * 1.414 * 3-4 = 10~14% of the total stake amount to halve the security, which feels expensive enough for me - so I am done.

