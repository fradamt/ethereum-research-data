---
source: magicians
topic_id: 21841
title: "Making Ethereum alignment legible: Wallets"
author: polymutex
date: "2024-11-25"
category: Magicians > Primordial Soup
tags: [erc, wallet, security, privacy, standardization]
url: https://ethereum-magicians.org/t/making-ethereum-alignment-legible-wallets/21841
views: 910
likes: 36
posts_count: 12
---

# Making Ethereum alignment legible: Wallets

In the spirit of the “Making Ethereum alignment legible” [@vbuterin](/u/vbuterin) blog post, I am looking to create an “L2Beat for wallets” website.

The goal is to compile a list of desirable attributes that a wallet *should* have, and then to analyze the landscape of currently-existing wallet software and analyze whether they meet these attributes.

[![An Ethereum wallet in the infinite garden](https://ethereum-magicians.org/uploads/default/optimized/2X/9/9222b901f9c58f8ff4fc4cd94abd7124362d4dee_2_500x500.jpeg)An Ethereum wallet in the infinite garden1024×1024 180 KB](https://ethereum-magicians.org/uploads/default/9222b901f9c58f8ff4fc4cd94abd7124362d4dee)

**Prior art**: `WalletBeat dot fyi` (cannot directly link to it due to Discourse permissions) exists. It currently focuses on very practical features (“Do you support mobile? Can you switch chain to `SOME_PARTICULAR_L2`?”). I am looking to extend it.

In this post, I am looking to collect **desirable *attributes*** from wallet software, rather than specific *implementations* that can accomplish those attributes. To illustrate the distinction:

| Attribute | Specific implementation |
| --- | --- |
| Does it use a free and open-source license? | MIT-licensed |
| Can it send a transaction without third parties? | Support broadcasting via own node |
| Does it cryptographically verify the chain state? | Uses Helios as a light client |
| Is the wallet’s monetization strategy transparent? | Charges user-visible fee on swaps |
| Can it withdraw the user’s assets from L2s trustlessly? | Supports self-sequencing on SOME_PARTICULAR_L2 |

*Note: In some of the attributes below, some specific implementations that could satisfy this attribute are listed in case where this would otherwise not be obvious.*

##  List of desirable wallet attributes

Here is the list I have come up with so far. I welcome feedback on this.

The list is broken down in broad categories that roughly correspond to “Ethereum values”, in no particular order:

- Standards adherence: A wallet should adhere to Ethereum standards. This means it should implement well-accepted EIPs and ERCs, and interoperate well with the Ethereum ecosystem.
- Security: A wallet should be secure. This means it should protect the user’s assets.
- Privacy: A wallet should be private. This means it should not leak the user’s private information without consent.
- Self-sovereignty: A wallet should be self-sovereign. This means the wallet’s features should work reliably without making assumptions about the honesty or availability or third parties.
- User experience: A wallet should provide a good user experience. This means it should make the obvious thing easy, and make it more difficult to shoot oneself in the foot.
- Transparency: A wallet should be transparent. This means the way it functions should be publicly scrutable.

###  Security

A wallet should be secure. This means it should protect the user’s assets from thefts, hacks, scams, and other risks.

- Chain verification: Does the wallet bundle a light client to verify L1 state?
- Transaction simulation: Can the wallet simulate transactions and show the effect of a user’s transaction prior to being signed?
- Scam alerts: Does the wallet alert the user about potentially fraudulent transactions they are about to sign?
- Verified backup: Does the wallet verify that the user understands and has backed up the factors used to sign transactions?
- Account recovery: Can users recover their account if they forget one of the factors used to sign transactions?
- Audits: Has the source code recently been audited?

###  Privacy

A wallet should be private. This means it should not leak the user’s private information without consent, and should offer to interact with the Ethereum protocol as privately as possible.

- Private sending: Does the wallet support sending funds privately?

Examples: Built-in support for stealth addresses or Privacy Pools.

**Private receiving**: Does the wallet support receiving funds privately?

- Examples: Built-in support for stealth addresses or Privacy Pools.

**Private spending**: Does the wallet leak information when spending privately-received funds? *(Not desirable)*

- Examples: Stealth address labeling, anonymous broadcasting of Privacy Pools transactions.

**IP address leak**: Can a third party learn associations between IP addresses and Ethereum addresses? *(Not desirable)*
**Identifying user information**: Does the wallet transmit user information to third parties? *(Not desirable)*

- Example: Some wallets may collect their users’ email address.

**Multi-address correlation**: When configured with multiple Ethereum addresses, can a third party learn that these addresses collectively belong to the same person? *(Not desirable)*

###  Self-sovereignty

A wallet should be self-sovereign. This means the wallet’s features should work reliably without making assumptions about the honesty or availability or third parties.

- Self-hosted node: Can users use their own Ethereum node for L1 interactions?
- Transaction censorship: Can users self-broadcast a transaction without being blocked by a third party?
- L2 withdrawals: Can users withdraw their funds from L2s trustlessly?
- Trustless frontends: Can users use popular dapps trustlessly?

Examples: Built-in IPFS support, ENS domain name resolution, ERC-6860 frontend support.

###  Transparency

A wallet should be **transparent**. This means the way it functions and it is developed should be publicly scrutable.

- Source visibility: Is the source code visible to the public?
- Open-source licensing: Is the source code licensed under an open-source license?
- Funding transparency: Is the wallet transparent about its monetization strategy, if any?

Examples: VC funding disclosures, token allocation transparency, user-visible swap/onramp fees.

*(Note: The above does not include “audits”, because that is already covered under Security.)*

###  User experience

A wallet should provide a **good user experience**. This means it should make the obvious thing easy, and make it more difficult to shoot oneself in the foot.

- Chain auto-switching: Does the wallet automatically switch to the correct chain necessary to do so?
- Chain abstraction: Does the wallet assist the user in (transparently) bridging assets (either L1-to-L2, L2-to-L1, or L2-to-L2)?
- Address resolution: Does the wallet resolve named addresses when sending assets?

Examples: ENS domain name resolution when sending funds.

**Non-native gas payments**: Can users pay transaction fees in assets other than the chain’s native gas token?
**Permission revoking**: Does the wallet assist in monitoring and revoking token permissions?

###  Standards adherence

A wallet should adhere to Ethereum standards. This means it should implement well-accepted EIPs and ERCs, and interoperate well with the Ethereum ecosystem.

- Browser integration standards: Does the wallet support EIP-1193, EIP-2700, EIP-6963? (For browser-based wallets only)
- EOA compatibility: Does the wallet support EOAs?
- Account abstraction: Does the wallet support insert-your-favorite-AA-ERC-here wallets?
- Address standards: Does the wallet support ERC-3770 addresses?
- Login standards: Does the wallet support ERC-4361 (Sign-In with Ethereum)?
- Token standards: Does the wallet support and display ERC-20, ERC-721, and ERC-1155 tokens?

## Replies

**abcoathup** (2024-11-26):

Some existing resources to look into:



      [wtf.allwallet.dev](https://wtf.allwallet.dev)





###



A testing framework for Ethereum wallets.











      ![](https://ethereum-magicians.org/uploads/default/original/2X/3/3ab80833ee3c7a5068143290cf0998bb94a3135e.png)

      [Coinspect Security](https://www.coinspect.com/wallets)



    ![](https://ethereum-magicians.org/uploads/default/optimized/2X/a/a26cf3a040b59496b0c9fa46fbfad0536667a870_2_690x362.png)

###



Coinspect's Wallet Ranking sets a benchmark for web3 safety.

---

**julianor** (2024-11-29):

Thanks for the link to our crypto wallet security ranking [@abcoathup](/u/abcoathup)

Vitalik emphasizes making Ethereum alignment more legible by breaking it down into specific, measurable criteria.

Our wallet testing methodology aligns with this vision by decomposing web3 wallet security into specific categories. Our work makes wallets’ “security” alignment axis more formalized and legible.

We’ll keep Coinspect’s Wallet Security Ranking and its detailed checklists updated. Please visit coinspect com /wallets/testing/ and our blog posts to learn more about the methodology and objectives.

We are here to answer any questions and collaborate towards the Ethereum alignment vision.

---

**nicocsgy** (2024-12-05):

Great post [@polymutex](/u/polymutex) ,

So I have this note [Ideas for a Wallet Dashboard - HackMD](https://notes.ethereum.org/@niard/Ideas_Wallet_Dashboard) that I wanted to finish but it’s been sitting on my to do list for a month now ![:sweat_smile:](https://ethereum-magicians.org/images/emoji/twitter/sweat_smile.png?v=12) . I’ll update it in the next days with more AA, and lightclient content. I’m glad to see that the idea is getting more and more traction. With your post and all those docs (new one by Vitalik [What I would love to see in a wallet](https://vitalik.eth.limo/general/2024/12/03/wallets.html) ![:tea:](https://ethereum-magicians.org/images/emoji/twitter/tea.png?v=12) ), I feel like we are getting closer to depict a great dashboard that would help to shepherd the wallets.

So to anyone that would like to build such a wallet dashboard **feel free to reach out to me**. [@polymutex](/u/polymutex) If you are interested my DMs are open here and everywhere else.

Disclaimer, as mentioned in the note, I won’t propose an implementation nor help with the execution (as I don’t think that should be my role and also don’t have the bandwidth). But I’m happy to help the brainstorming of criteria and open my network of wallet people to make it happen !

Now it’s building time, fellow ethereans — let the journey to better Ethereum wallets begin!

---

**polymutex** (2024-12-06):

Hello everyone and thanks a lot for the responses!

The Wallet Test Framework and the Coinspect security rankings are great resources. They are scoped to one particular aspect (testing in one, security in the other) so they do that really well, but nonetheless I believe a need exists for a broader-scope wallet comparison tool beyond testing & security. That comparison tool should definitely link to those rankings as well where it makes sense. Thanks [@julianor](/u/julianor) for maintaining it!

[@nicocsgy](/u/nicocsgy) Thanks for the link! Looks like it’s all quite well aligned with this post too. And yes, Vitalik’s latest blog post has prophetic timing. Will DM you. I have already started building the dashboard by sending pull requests to the existing WalletBeat-dot-fyi website, with the goal to extend it to cover these criteria and those that others have suggested and to make it more extensive and detailed the way L2Beat breaks down all the dimensions of L2s. I’ve also created a /walletbeat Farcaster channel where I am posting updates about this effort. (Sorry for the lack of links, I don’t think I have permission to link to websites yet.)

---

**nicocsgy** (2024-12-16):

Hello,

Glad to see various dashboards, ([Wallet Security Ranking | Coinspect Security](https://www.coinspect.com/wallets) and https://www.walletbeat.fyi). However, I wonder if the link with a company that sells wallet related product is enough to entangle the incentives. At least, it changes the perceived credible neutrality of the project. Ideally, a team that maintains a dashboard has experience in the wallet world but little to no economic incentive. I wonder if those projects could spin out as independent organisations ? That being said, I also think that we’re better served by having a surplus of dashboards.

---

**moritz** (2025-01-08):

Hey everyone, just catching up on this thread ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12) It’s exciting to see discussions about this topic pick up over the past weeks!

We launched walletbeat.fyi last year as a Fluidkey side project. We were getting frustrated with the level of ENS support in many leading wallets, and wanted to highlight wallets that do a good job at implementing important standards and features.

I’m really excited by the work [@polymutex](/u/polymutex) has been doing on Walletbeat 2.0 in order to compare wallets in-depth.

[@nicocsgy](/u/nicocsgy) - we would be happy to spin out Walletbeat as an independent organisation / hand it over to an existing independent org. This was our intent since launching Walletbeat.

The problem today is that outside of [@polymutex](/u/polymutex) doing a lot of great work, there aren’t any contributions. The first step in my view would be to have an active community maintaining and enhancing the dashboard, to which the project can then fully be handed over.

---

**Atenika.Protocol** (2025-01-09):

i owuld add Custom abi support or itnerface import like for ERCs similar to chianlist … for mature users ofc.

---

**beringela** (2025-01-25):

This is a great idea. Walletbeat doesn’t seem to be very up to date (eg says Rabby has no mobile client).

Some UX things:

1. One feature I’d like to see listed, not sure how to measure it though, is “integration quality”. It is so frustrating having wallets not connect to sites, they don’t popup when you press connect and so on. It’s important, but is that the wallets “fault” or the sites fault or wallet connect or something else?
2. I was surprised to find Rabby doesn’t let me display fiat values in anything but USD yet. I had taken it for granted that every wallet would do that but not so (well not today).
3. Some wallets are more developer friendly than others. Eg to see what test chain you are looking at, what custom tokens you have.

---

**Antoine-Sparenberg** (2025-02-10):

Would love to see such a framework open to all Ethereum wallets, not only EVM ones

---

**julianor** (2025-04-28):

FYI we keep the Wallet Security Ranking updated. We tested 74 wallets:


      ![image](https://www.coinspect.com/favicon.ico)

      [Coinspect Security – 28 Apr 25](https://www.coinspect.com/blog/wallet-security-ranking-results-april-2025/)



    ![image](https://www.coinspect.com/og/social-image-wallet-security-ranking-results-april-2025.png)

###



The second edition of Coinspect’s Crypto Wallet Security Ranking is live featuring 74 wallet apps across iOS, Android, and browser extensions.

---

**lucemans** (2025-04-29):

Wanted to share an update here on where we are at.

Walletbeat has received a wide variety of contributions from 24+ contributors ![:saluting_face:](https://ethereum-magicians.org/images/emoji/twitter/saluting_face.png?v=15)

Refreshed **homepage** covering everything you need to know **at a glance**:

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/7/780a3435e5ef8758046158da802ff4205472b294_2_690x357.png)image1912×992 222 KB](https://ethereum-magicians.org/uploads/default/780a3435e5ef8758046158da802ff4205472b294)

As well as a page **for each wallet** covering all **aplicable criteria**:

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/8/8a398bdac16e5156cc1bd145ea6e05345b8c097d_2_690x358.png)image1914×994 124 KB](https://ethereum-magicians.org/uploads/default/8a398bdac16e5156cc1bd145ea6e05345b8c097d)

You can visit the page to see how each wallet compares at [wallet.page](https://wallet.page)

We have also migrated git repository and the current repository lives at:

[walletbeat/walletbeat](https://github.com/walletbeat/walletbeat)

Will share a more public statement (expanding on all this) on the socials soon aswell as slide in some dm’s in hopes to reachout to as many wallets as possible.

Hope to share more progress soon™ and welcome contributions of all sorts and kinds ![:folded_hands:](https://ethereum-magicians.org/images/emoji/twitter/folded_hands.png?v=15)

PS; for some reason 80% of these sentences start with a ‘W’… W I guess.

