---
source: magicians
topic_id: 14979
title: "ERC-7281: Sovereign Bridged Tokens"
author: arjunbhuptani
date: "2023-07-07"
category: ERCs
tags: [token]
url: https://ethereum-magicians.org/t/erc-7281-sovereign-bridged-tokens/14979
views: 12301
likes: 39
posts_count: 30
---

# ERC-7281: Sovereign Bridged Tokens

Discussion thread for [Add EIP: Sovereign Bridged Token by ArjunBhuptani · Pull Request #7281 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/7281)

EIP-7281 (aka xERC20) proposes a minimal extension to ERC-20 to fix problems with token sovereignty, fungibility, and security across domains.

The proposal introduces:

1. A burn/mint interface to the token callable by bridges allowlisted by the token issuer.
2. Configurable rate limits for the above
3. A “Lockbox”: a simple wrapper contract that consolidates home chain token liquidity and provides a straightforward adoption path for existing ERC20s

Under this proposal, ownership of tokens is shifted away from bridges (canonical or 3rd party) into the hands of token issuers themselves.

Token issuers decide which bridges to support for a given domain, and iterate on their preferences over time as they gain confidence about the security of different options. In the event of a hack or vulnerability for a given bridge (e.g. today’s Multichain hack), issuer risk is capped to the rate limit of that bridge and issuers can seamlessly delist a bridge without needing to go through a painful and time-intensive migration process with users.

This proposal also fixes the broken UX and incentives around bridging:

- Bridges now compete on security to get better issuer-defined rate limits for a given token, incentivizing them to adopt the best possible security and trust-minimization practices.
- Bridges can no longer monopolize on liquidity, a strategy that asymmetrically favors projects with significant capital to spend on incentives.
- Crossdomain token transfers no longer incur slippage, leading to better predictability for users and an easier pathway for crossrollup composability for developers.
- Liquidity and security scalability issues associated with adding many new domains are mitigated. New rollups no longer need to bootstrap liquidity for each supported asset - this is particularly important as we are rapidly heading towards a world with 1000s of interconnected domains.

ERC-7281 attempts to be compatible with:

1. All existing tokens through the Lockbox wrapper
2. Existing 3rd party bridges that widely support a burn/mint interface.
3. Canonical bridges for popular domains. We investigated Arbitrum, Optimism, Polygon, ZkSync, GnosisChain and found that in most cases there was a straightforward (and permissionless!) pathway to support xERC20s.

## Replies

**william** (2023-07-07):

This is super cool – do you have a reference implementation for this ERC?

---

**a6-dou** (2023-07-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arjunbhuptani/48/9974_2.png) arjunbhuptani:

> Add EIP: Sovereign Bridged Token by ArjunBhuptani · Pull Request #7281 · ethereum/EIPs · GitHub

the proposal looks very interesting! especially the aggregation part! (would be even nicer if u could share some metrics here)

Indeed I have some concerns, while providing token issuers with the ability to choose which bridges to support can offer advantages in terms of control and risk management, it can also potentially lead to the concentration of funds in a limited set of solutions. Token issuers may have biases or motivations that go beyond technical metrics when selecting bridges, which could influence users’ decision-making. This could reduce diversity and limit the number of available options for users.

The EIP proposal, with its fragmentation and aggregation solution, may indeed make using the bridge supported by the token a more economically attractive option due to potential savings. This can create an economic incentive for users to prefer the bridge selected by the token issuer, even if alternative bridges exist. Users may prioritize cost savings and convenience, which could result in a concentration of liquidity and usage in the chosen bridge.

---

**ss-sonic** (2023-07-08):

This is good and I feel it can be more robust if we have a pathway to accommodate these concerns:

The proposed system adds additional fault points by enabling multiple bridges to mint assets, increasing complexity & risk.

Concentration of power with the protocol owner could potentially lead to unenforced protocol behavior. A compromised key management system could magnify this risk.

Remembering our experience with router bridge tokens (https://arbiscan.io/address/0x8413041a7702603d9d991f2c4add29e4e8a241f8#code) - enabling the protocol to grant minting rights to various bridges introduced risks should the protocol behave improperly.

With vast value already locked in the current system, it’s crucial that any solution thoroughly addresses existing challenges.

Let’s consider we’re developing this and aiming to decentralize the process of mint permissioning. However, potential issues arise:

Using a DAO to allocate minting rights sounds like a solid solution, but it presents its own challenges.

Imagine a protocol deploys its token on Ethereum and aims to bridge it to Polygon. At first, no tokens exist on Polygon.

DAO voting on Ethereum can facilitate deployment, while also granting initial minting rights to a bridge on Polygon, say, the Polygon bridge.

This bridge now becomes a role setter for the token contract, assigning itself as the minter.

If the DAO then decides to shift the minting role to Connext through Ethereum voting, this can be accomplished via the Polygon bridge.

Here’s the vulnerability - the Polygon bridge emerges as a single point of failure. If compromised, the setter permissions become jeopardized, potentially leading to the same issues we’re trying to circumvent.

We need a more robust method that prevents such risks without introducing a new set of vulnerabilities.

---

**THE_DOCTOR** (2023-07-09):

“Indeed I have some concerns, while providing token issuers with the ability to choose which bridges to support can offer advantages in terms of control and risk management, it can also potentially lead to the concentration of funds in a limited set of solutions. Token issuers may have biases or motivations that go beyond technical metrics when selecting bridges, which could influence users’ decision-making. This could reduce diversity and limit the number of available options for users.”

Spot on.

I agree with this response from a6-dou that this proposal is not aligned with the intended objective. Despite the assertion in a Twitter post that this is not an attempt to create a monopoly, it appears that the proposal indeed aims to achieve such dominance. This approach parallels the practices of Web 2 companies that leverage regulation to impede competition and innovation. It seems to stem from a place of fear and reflects contradictory messaging, particularly when considering Connext Network’s aspiration to become the “http of Web 3”. While pursuing ambitious goals is commendable, utilizing regulation to discourage technologically superior competitors contradicts the principles upheld by Web 3.

Additionally, if I possess an asset, why am I restricted from providing liquidity to the bridge of my choice? It is condescending to assume that liquidity providers for existing bridges lack understanding of the associated risks, especially given the availability of avenues where such risks are disclosed, as demonstrated by resources like [L2BEAT – The state of the layer two ecosystem](https://l2beat.com/bridges/tvl). This approach also fails to address the possibility of a secure bridge’s liquidity pool being hacked. I can recall the substantial loss of wealth incurred due to the Nomad Bridge hack, which was touted as the most secure bridge ever created. Regrettably, no apology or acknowledgement has been received for that incident.

In summary, let the free market determine the outcomes. Avoid introducing regulations that lead to industry monopolization, protecting inferior technologies behind artificial barriers. As both a liquidity provider and a user of multiple bridges, it is worth noting that at least two bridges have already resolved the slippage issue when transferring between rollups, particularly relevant in the context of this Ethereum forum.

---

**zhiqiangxu** (2023-07-10):

Basically sounds good, the only thing that may be hard to actually carry out is to set a reasonable rate limit for each bridge. Should the limit be 1M $, 10M $ or 100M $? It’s hard to decided, and that’s why it’s not often rolled out by bridges.

Currently each bridge deploys its own `xERC20`, which causes the above mentioned issues, but their security is isolated, say, the attack to bridge `A` won’t affect the home chain assets of bridge `B`. This is not the case if the home chain assets are pooled together.

---

**auryn** (2023-07-10):

I’m generally supportive of this proposal, but I have a small handful of concerns.

1. How would this work for tokens that don’t have some governance layer? WETH, for example.
2. This grants some additional, perhaps unwanted, governance power to the issuers of tokens that do have governance mechanisms. In some cases the issuer may be unable or unwilling to actually exercise this power.
3. It also probably implies some metagovernance layer to decide which account should have bridge governance rights over a given token, since you couldn’t just relay on owner() existing and being correct for every token.

---

**gpersoon** (2023-07-10):

Hi Arjun, I think its a good idea, however the deployment and management of these xTokens will not be trivial to do. I’ve summerized my thoughts in this post: [Manage bridged tokens on a large number of chains - HackMD](https://hackmd.io/@gpersoon/ManageBridgedTokens)

---

**arjunbhuptani** (2023-07-10):

Thanks for the responses all! Great to see that folks are interested in this approach. ![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=12)

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/w/b19c9b/48.png) william:

> This is super cool – do you have a reference implementation for this ERC?

Yep! There’s a reference implementation listed in the final section of the EIP draft. Also linking it [here](https://github.com/defi-wonderland/xTokens/blob/dev/solidity/contracts/XERC20.sol)!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/a6-dou/48/9169_2.png) a6-dou:

> Indeed I have some concerns, while providing token issuers with the ability to choose which bridges to support can offer advantages in terms of control and risk management, it can also potentially lead to the concentration of funds in a limited set of solutions. Token issuers may have biases or motivations that go beyond technical metrics when selecting bridges, which could influence users’ decision-making. This could reduce diversity and limit the number of available options for users.

To clarify: In the current paradigm, token issuers are *already* making decisions on bridges based on liquidity rather than on security or technical reasons. The ERC-7281 approach explicitly *removes* moats around concentration of funds as issuers now solely base bridge decisions around the rate limits they are comfortable with.

In other words, the goal of this approach is specifically to solve the exact problem you are talking about.

Please let me know if I’m misunderstanding your point here!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ss-sonic/48/9982_2.png) ss-sonic:

> Here’s the vulnerability - the Polygon bridge emerges as a single point of failure. If compromised, the setter permissions become jeopardized, potentially leading to the same issues we’re trying to circumvent.
>
>
> We need a more robust method that prevents such risks without introducing a new set of vulnerabilities.

To summarize your points, it sounds like you (as well as [@gpersoon](/u/gpersoon) and [@auryn](/u/auryn)) are correctly pointing out that there is increased administrative overhead involved associated with deploying and managing tokens across chains on an ongoing basis.

Totally agree here! However, I think this is a solvable problem:

1. First, it’s important to posit that governance risks around controlling deployed crosschain tokens already exist. However, they are currently owned by the minting bridge, and not by the project. This is one of the key problems that this approach attempts to resolve.
2. Governing a token implementation across chains involves fundamentally the same functionality as a DAO controlling its own protocol across chains. A growing number of DAOs are already doing this using multisigs and/or canonical bridges.
3. You’re right that introducing a dependency even on a canonical bridge is less than ideal. The proposal was largely designed with rollups in mind, where trusting the canonical bridge for governance is less controversial. HOWEVER, based on real world data from how DAOs are operating currently, I think this problem can be solved with Multi Message Aggregation (MMA) approaches like Hashi, and/or using a configurable optimistic delay for crosschain messages within which a DAO-elected security council could veto a fraudulent message.

Note: Connext is working on public goods tooling that layers on top of canonical bridges for (3) ourselves because we need it for our own upcoming crosschain token deployment and governance. We plan to release this to the public once ready. I also know of several other projects doing the same.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/t/839c29/48.png) THE_DOCTOR:

> In summary, let the free market determine the outcomes. Avoid introducing regulations that lead to industry monopolization, protecting inferior technologies behind artificial barriers. As both a liquidity provider and a user of multiple bridges, it is worth noting that at least two bridges have already resolved the slippage issue when transferring between rollups, particularly relevant in the context of this Ethereum forum.

I’m not quite sure how to respond to this. I think you may have some **very** deep misunderstandings about how ERC7281 works. In fact, it actually very specifically encourages open competition in the exact way that you describe. ![:thinking:](https://ethereum-magicians.org/images/emoji/twitter/thinking.png?v=12)

Maybe to summarize, ERC7281:

- Makes it possible for token issuers to allow bridges to mint/burn tokens, set rate limits for how much each bridge and mint/burn, and iterate on those preferences over time.
- Is totally bridge agnostic and widely compatible. You can see this in the implementation.
- Creates a level playing field where different technical approaches can compete in an open way on support, rather than the current model where token issuers are locked into one option forever.
- Reduces the cost/slippage of bridging overall for the entire space, and makes  it possible for tokens to expand to 100s or 1000s of chains.

I don’t currently see how the above approach in any way creates a monopoly for any organization. I’m also not sure what you mean by regulation - this is a opt-in just like all ERCs. ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

P.S. Re: projects that have already solved slippage; this is typically done by taking another end of the tradeoff spectrum between liquidity, fungibility, and security. For example, Connext used to support slippage free transactions via an RFQ system, but this introduced the need to rebalance tokens between chains making it challenging for anyone other than institutional market makers to provide liquidity.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/zhiqiangxu/48/9990_2.png) zhiqiangxu:

> Basically sounds good, the only thing that may be hard to actually carry out is to set a reasonable rate limit for each bridge. Should the limit be 1M $, 10M $ or 100M $? It’s hard to decided, and that’s why it’s not often rolled out by bridges.

This is a good open question. I expect that over time issuers will iterate on rate limit configurations and best practices will emerge. The best way to model in the time being is for token issuers to model and evaluate the economic tradeoffs between user demand for transfers vs amount the issuer feels comfortable backstopping in the event of a hack.

Note: the rate limits should specifically stop the pooled risk you mention as the total loss per bridge is capped which emulates the security surface area of having fragmented liquidity in the first place.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/auryn/48/1044_2.png) auryn:

> How would this work for tokens that don’t have some governance layer? WETH, for example.

It doesn’t. The core goal of this proposal is to solve for the tradeoff space between liquidity/fungibility and security specifically for longer tail assets where those tokens do not have sufficient fee revenue from organic volume to sustain LPs for many many different chains. WETH doesn’t suffer from this problem as it’s one of the most frequently bridged assets out there aside from USDT and USDC.

Longer term, I think there’s an argument to be made that LSDs like wstETH are likely to be used as the “transport” layer for crosschain interactions and/or WETH will be replaced by staked versions of ETH entirely. But not sure yet what the right answer is here yet!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/auryn/48/1044_2.png) auryn:

> It also probably implies some metagovernance layer to decide which account should have bridge governance rights over a given token, since you couldn’t just relay on owner() existing and being correct for every token.

This is definitely a central challenge. How this works currently is that each bridge independently owns and maintains a registry that maps assets between chains, and works directly with DAOs to update that mapping.

Wonderland (who built the reference implementation) and I have chatted a bit about creating a central public good registry (a TCR?!) for the above, but it’s a very very hard problem and potentially completely impossible to make permissionless.

Another approach - and this is what we’re recommending currently - is to simply do the token deployments themselves across chains, originating from the DAO and setting up all relevant config as part of the same transaction.

---

**geogons** (2023-07-11):

Overall I am very supportive of this proposal, especially for long-tail assets as you mentioned [@arjunbhuptani](/u/arjunbhuptani)

Maybe mentioning this more explicitly could be helpful. There are many arguments why this model would not fit WETH/USDC/USDT/WBTC which are the assets that people think of when it comes to bridging.

However, this model has a lot of merit for all other assets.

Setting the limits by the issuers is a great feature. Something we currently see on Gnosis Chain Omnibridge for example: Token issuers ask the bridge governance to adjust the limits of their tokens for a variety of reasons

One thing that can be a bit cumbersome: Token issuers need to assess and understand the security model of the bridges they give rights for minting/burning of the token. And they need to do this for multiple chains. A sort of guidance with templates and recommendations would be helpful imo.

---

**arjunbhuptani** (2023-07-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/geogons/48/6415_2.png) geogons:

> Maybe mentioning this more explicitly could be helpful. There are many arguments why this model would not fit WETH/USDC/USDT/WBTC which are the assets that people think of when it comes to bridging.

Good point! Will add a note about WETH explicitly into the ERC. Though note that USDT, and WBTC are both actually in-scope for this approach as both have issuers. (USDC also has an issuer but already has their own in-house solution).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/geogons/48/6415_2.png) geogons:

> Something we currently see on Gnosis Chain Omnibridge for example: Token issuers ask the bridge governance to adjust the limits of their tokens for a variety of reasons

This is a really good data point.

---

**Mani-T** (2023-07-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/arjunbhuptani/48/9974_2.png) arjunbhuptani:

> Token issuers decide which bridges to support for a given domain, and iterate on their preferences over time as they gain confidence about the security of different options. In the event of a hack or vulnerability for a given bridge (e.g. today’s Multichain hack), issuer risk is capped to the rate limit of that bridge and issuers can seamlessly delist a bridge without needing to go through a painful and time-intensive migration process with users.

Nice proposal, this is really meaningful.

---

**bendi** (2023-07-17):

I’m overall a fan of this proposal and supportive of it, especially its implications for long tail governance assets, where ScopeLift does a lot of work. A few questions that come to mind, some of which might be pretty dumb, so forgive me if so:

1. I don’t see an obvious way the xERC20 on chain A maps to xERC20 on chain B and chain C, etc… Is the relationship between deployed token contracts on each chain purely a matter of social consensus/bridge configuration?
2. For a project that adopts xERC20 out of the gate, is there any single asset that can be considered the “base” or “home” asset? How is this defined, if at all?
3. Is the limit a rate limit or a cap? It uses the word rate limit but sounds like a cap.
4. What does recovering from the inevitable instance of a hack look like for an xERC20 implementation if one of thew whitelisted bridges is compromised and goes rogue?

Thanks for pushing this forward [@arjunbhuptani](/u/arjunbhuptani). Excited to see where the conversation goes.

---

**arjunbhuptani** (2023-08-03):

Thanks so much Ben! (and apologies for the slow reply - totally forgot about your response here ![:sweat_smile:](https://ethereum-magicians.org/images/emoji/twitter/sweat_smile.png?v=12)). These are great questions.

> I don’t see an obvious way the xERC20 on chain A maps to xERC20 on chain B and chain C, etc… Is the relationship between deployed token contracts on each chain purely a matter of social consensus/bridge configuration?

In the ideal case, we would have some form of public registry/mapping of all tokens across chains. However, doing this permissionlessly is quite a challenge because it can easily become an attack vector as incorrect/spoofed mappings would mean funds stolen from every bridge.

I’m still trying to think through if there’s a safe, public goods way to solve this problem (maybe a TCR?!?), but in the meantime the next best option seems to be fuzzy social consensus and each bridge maintaining their own independent mapping by working directly with token issuers - this is how bridges maintain token mappings today anyway.

> For a project that adopts xERC20 out of the gate, is there any single asset that can be considered the “base” or “home” asset? How is this defined, if at all?

There doesn’t have to be!

In the long term (1000s of domains, with users never  needing to know/care what domain they’re on), needing to have a “home” chain in general likely becomes an outdated concept.

> Is the limit a rate limit or a cap? It uses the word rate limit but sounds like a cap.

Token issuers provide two params when setting limits: a `ratePerSecond` and `maxLimit`.

When a bridge mints or burns a token, the token implementation checks to see that the `amount` being minted or burned is less than the lower of `currentLimit` or `maxLimit`, where `currentLimit` is calculated as:

```auto
currentLimit_T1 = currentLimit_T0 + ratePerSecond * (block.timestamp_T1 - block.timestamp_T0)
```

(another way to say this is that there’s an “approved limit” that the bridge can mint/burn that grows at `ratePerSecond` to the `maxLimit`)

> What does recovering from the inevitable instance of a hack look like for an xERC20 implementation if one of thew whitelisted bridges is compromised and goes rogue?

Important to note: xERC20 doesn’t save token issuers from this outcome. Ultimately we still do need to fix & commoditize underlying bridge security. However, this approach does let token issuers limit fallout if/when it does happen.

For a token issuer dealing with a bridge hack:

1. The issuer should immediately set the minting and burning limits of the compromised bridge to 0 (i.e. delist the bridge)
2. From here, issuer should assess the damage done to underlying token value - this will be the lower of currentLimit or maxLimit at the time of the hack.
3. If the issuer has intelligently chosen limits, the total loss should only be some of the underlying token value. It would be up to the issuer at this point to figure out if/how they can plug this hole to (if using a lockbox) restore the 1:1 ratio between outstanding xERC20s and ERC20s in lockbox OR (if not using a lockbox) restore the original price/value of the token.

One simple way to accomplish (3) is for token issuers to buy back and burn outstanding xERC20s in the market equal to the amount of tokens stolen in the attack.

---

**sullof** (2023-08-04):

The same concern was addressed and solved for NFT with Wormhole721 ([GitHub - ndujaLabs/wormhole721: An implementation of Wormhole native protocol for ERC721 NFTs](https://github.com/ndujaLabs/wormhole721)) which extends the Wormhole-tunnel ([GitHub - ndujaLabs/wormhole-tunnel](https://github.com/ndujaLabs/wormhole-tunnel)) to send a payload on the other chains, using exactly a process of mint-burn. The protocol can be adapted very easily to be used with ERC20 — since the tunnel is agnostic and sends a generic payload on the other chain.

---

**radek** (2023-10-18):

Proposing a minor change in naming:

use `function setBridgeLimits()`

instead of `function setLimits()`

SetLimits is too vague  and collides with other custom ERC20 features.

---

**parseb** (2023-10-29):

Felt like a Karen today and wrote something about this.

In short, this to me seems to transfer **power from token owners to token issuers**.

- It makes out of owners, users.
- If adopted as a standard, opens chain sanctioning season.
(Might as well set ofac.eth as admin and point to address(0) for tron chainid.)
- Adds more risk and sense-making work than it solves for. Arguably ofc.

https://mirror.xyz/parseb.eth/2yPllA0MItcPj68HLIJUyWoHYpozTz9SX_skrlzWJeY

Where do I pick as I exit the “did my part” badge?

---

**nearpointer** (2023-10-30):

Hey everyone, I appreciate the introduction of xERC20 and all the discussion on the subject. It’s a commendable step forward in enhancing the decentralized ecosystem and I am overall supportive of the idea. [@arjunbhuptani](/u/arjunbhuptani)

However, I do share some reservations, particularly concerning the significant control bridges have over the burn and mint processes of native tokens. The balance between security and user control is delicate, and it’s crucial to explore solutions that empower token owners while ensuring the integrity of the cross-chain transactions.

I was wondering what are your thoughts on a possible solution where any token owner can initiate a burn on the source chain by calling for example a burnX function on the ERC20 contract itself, generating a unique burn receipt. This receipt, along with the originating contract’s address, can be sent over any bridge to a corresponding token contract on another chain. Each contract will maintain a mapping of corresponding contracts on all other chains and can validate the “origin contract” and the content of the payload itself before minting.

It probably adds a little bit more to an otherwise simple token contract but maybe each token becoming its on ‘bridge’ in a way is something worth exploring?

With that said, super pumped to see the journey of xERC20 from here on out. Let’s keep the dialog going!

---

**radek** (2023-12-14):

Creating the stablecoin I like this idea. It would have to be further elaborated in order to ensure crosschain replay protection (of minting on multiple target chains).

IMHO burn receipt idea leads to other direction from xERC20.

More thinking about that, I can imagine having such bridge mechanism on top of xERC20 - effectively combining both.

---

**radek** (2023-12-19):

[@arjunbhuptani](/u/arjunbhuptani) can you pls comment this adjustement?

---

**SamWilsn** (2024-03-07):

Generally speaking, we encourage standards to omit functions that can only be called by the owner/deployer of a contract (like `setLimits` and presumably `setLockbox`) because the owner of a contract can be expected to understand the specifics of a particular implementation. There’s no need for interoperability.


*(9 more replies not shown)*
