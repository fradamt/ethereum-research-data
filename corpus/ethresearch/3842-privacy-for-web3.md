---
source: ethresearch
topic_id: 3842
title: Privacy for web3
author: kaibakker
date: "2018-10-17"
category: UI/UX
tags: []
url: https://ethresear.ch/t/privacy-for-web3/3842
views: 2198
likes: 10
posts_count: 5
---

# Privacy for web3

I am pretty sure most people don’t want to connect their public information and their financial situation, for as long as ethereum exisits. But web3 and new Dapps make it super easy to connect your social profile through peepeth and your erc20 and eth holdings. I wanted to start a discussion about how Dapps and Dapp browsers should change.

Using different addresses for different Dapps would be a great start. And creating methods to avoid connections from your existing accounts should be default. How can we make ethereum a little bit more private for the average user?

## Replies

**vbuterin** (2018-10-18):

Using different addresses by default is definitely a good idea. The main challenge is how to send funds from one’s “main account” to these different addresses without linking them; to achieve real privacy gains some kind of mixing solution seems necessary.

---

**MihailoBjelic** (2018-10-18):

User privacy is one of the main topics (if not the main one) in the whole digital identity research space.

On the Ethereum side, I believe uPort is at the forefront of these efforts. You might want to check [this post](https://medium.com/uport/the-3-parts-of-identity-in-a-dynamic-world-f94724c2bae9), as well as all the other stuff they do/publish.

---

**Cygnusfear** (2018-10-19):

Connecting addresses to identity is something that is really important to me developing [ethtective](http://www.ethtective.com). The topic is quite the double edged sword. I’ll try to describe what I am currently thinking, because I do believe this is a broad and complex topic.

There is a great public benefit to this: Increasing public availability of information levels the playing field for unsophisticated actors by organising the information for them. This means that ‘investigations’ can be carried out by regular users; they can see who hacked them and then report to law enforcement / exchanges. Accessibility to this information means that they do not have to trust/pay intermediates/third-parties to do this work for them/inform them. They can check and verify themselves. As a tool for educating users on economic/financial information I consider the availability and collation of this data absolutely invaluable.

Aragon, for example, desires to be (radically) transparent. The Ethereum network is public by default so they (and the public) immediately benefit from these properties. Journalists, investigators, law enforcement etc. all benefit from the public availability of this data (cum-ex, panama papers). Personally I think this is a very strong and important impetus, because this makes it much easier to hold companies and institutions accountable by pressuring them to use this default transparency of the network. If you are explicitly looking for privacy, you *will* move to a private/privacy chain.

On the scale of individual users however: I am getting feedback from users who are surprised about/previously unaware of ‘what you can see on the blockchain’. For new users this is legitimately frightening. And reports of crypto-millionaires being robbed and even murdered are real consequences of people’s financial situation being doxxed.

But this is an issue that cannot be addressed by web3 apps, but needs to be addressed by wallets. Wallets are the de facto custodian-apps that users put their funds and trust in; users should never delegate that trust to other web3 apps (which can claim ad hoc legitimacy that users will be unable to verify). We see initiatives by several wallets to build scam/hack lists, which [@pedrouid](/u/pedrouid) and I are trying to make more accessible to developers and easier to manage with [a proposal for a curated metadata registry](https://ethereum-magicians.org/t/erc-1357-address-metadata-json-schema/).

A wallet should be the only entity that is required to identify the user. So the onus is on the wallets to assist users in managing their identities, ‘privacy settings’ and educating them on the public visibility of the transaction. [@ligi](/u/ligi) called this ‘digital hygiene’, which I think is a great term. Certain fancy upcoming ‘persistent script’ wallets will implement (traditional) security features such as daily withdrawal limits, draining to rescue wallets, thus I can only imagine them to be in a position to offer private transactions through mixers/snarks as a default feature.

There is another real world footnote; FAANG explicitly makes it hard for users to care about privacy. Privacy options are buried deep in their settings to protect their income. I think wallets have different economic incentives, thus users privacy settings can align with *how transparent they can be*. This will also change why users *choose* to give away their privacy. In a certain sense, the desire for privacy is very much an indicator of how vulnerable people are to [wrench attacks](https://xkcd.com/538/).

This is definitely a topic with real consequences. The previous bullrun (I say it this way, because it will happen very fast once it does), a massive amount of uneducated users were suddenly dropped into MyEtherWallet, lost private keys, got scammed, sent wrong transactions, lost funds, became angry, spammed developers and…(wait for it)… UX became important. If you want to ‘bank the unbanked’ then you are forced to design for ‘blockchain illiterates’. These upcoming new users should be protected with very strong defaults until they decide to choose otherwise. Wallets will (by design) be trusted by users and replace the ‘source of trust’ that banks offer, they will compete on usability and security features.

**tl;dr** web3 apps cannot be trusted to give any security or privacy guarantees, the responsibility for privacy and security is with the wallets.

I see web3 apps generating an account for the user, and the user deciding later to connect it to their funds (with an informative notice from the wallet as to what this entails) as the best way to approach this currently.

Relevant:

- Digital hygiene to use different dApps with different keys
- Human Readable Machine Verifyable transactions.
- Alex van de Sande’s Universal Logins
- Meta-transactions
- https://metaconnect.me

---

**eolszewski** (2018-10-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Using different addresses by default is definitely a good idea. The main challenge is how to send funds from one’s “main account” to these different addresses without linking them; to achieve real privacy gains some kind of mixing solution seems necessary.

If you could pay for transactions with ERC20s, we could create an SPV from something like Monero to Ethereum whereby you burn Monero and are credited on the Ethereum chain to the address specified in transaction metadata. Hasn’t something like this previously been proposed?

