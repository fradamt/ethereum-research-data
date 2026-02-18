---
source: magicians
topic_id: 12677
title: Address EIP-4626 inflation attacks with virtual shares and assets
author: Amxx
date: "2023-01-24"
category: EIPs
tags: [erc, token, eip-4626]
url: https://ethereum-magicians.org/t/address-eip-4626-inflation-attacks-with-virtual-shares-and-assets/12677
views: 6442
likes: 6
posts_count: 11
---

# Address EIP-4626 inflation attacks with virtual shares and assets

Address EIP-4626 infaltion attacks with virtual shares and assets

# Introduction

As some of you may know, EIP-4626 is vulnerable to the so-called inflation attacks. This attack results from the possibility to manipulate the exchange rate and front run a victim’s deposit when the vault has low liquidity volume.

This is made possible by the absence of slipage protection in the deposit function. There exist several approaches to mitigate this risk. This includes using a EIP-4626 router, or using dedicated functions like the ones proposed in EIP-5143. However, this still leaves interaction between EOAs and standard EIP-4626 vaults somehow vulnerable.

At OpenZeppelin, we hope to provide an implementation that remains as simple and unopinionated as possible, while also providing the best security possible. As such, we have been working on a solution that would address this issue with minimal impact on the vault.

We are currently in the process of adding what we call a “decimal offset” together with “virtual assets and shares”. This post documents this addition to the vault. We are hoping to gather feedback by the EIP-4626 community because releasing that.

# Reminder: the inflation attack

Glossary:

- Asset or underlying asset: an ERC-20 token that is used by the vault as collateral
- Shares: the ERC-20 token that is used to represent ownership over the vault.

When a vault is not empty, the balance between shares and assets define the vault exchange rate. This rate is usually applied to further operations such as deposits, withdraw, etc. This rate is produced using the `totalAssets` (which is often the balance of te vault in underlying assets) and the vaults `totalSupply` (which is the ammount of shares that exist).

If any of these values is 0, than the rate is not properly defined, and some operations are problematic. That is why, when a vault is empty, the exchange rate is often defined using a fallback. This fallback corresponds to the “default” exchange rate, which is often dictated by the decimals of both contracts.

[We used to do that in our 4.7 release](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v4.7/contracts/token/ERC20/extensions/ERC4626.sol#L146-L169)

---

**Code**

```solidity
function _convertToShares(uint256 assets, Math.Rounding rounding) internal view virtual returns (uint256 shares) {
    uint256 supply = totalSupply();
    return
        (assets == 0 || supply == 0)
            ? assets.mulDiv(10**decimals(), 10**_asset.decimals(), rounding)
            : assets.mulDiv(supply, totalAssets(), rounding);
}
function _convertToAssets(uint256 shares, Math.Rounding rounding) internal view virtual returns (uint256 assets) {
    uint256 supply = totalSupply();
    return
        (supply == 0)
            ? shares.mulDiv(10**_asset.decimals(), 10**decimals(), rounding)
            : shares.mulDiv(totalAssets(), supply, rounding);
}
```

---

The idea of the inflation attack is to tamper with that exchange rate just before a user deposits token to the vaults.

Lets say Alice wants to deposit 1 token (with decimal 18, so 1e18 units) to the vault calling deposit. This is how the attack would unfold.

- The vault is empty.

The exchange rate is the default 1 share per asset

Bob sees Alice’s transaction in the mempool and decide to sandwitch it.
Bob deposits 1 wei to the vault, gets 1 wei of shares in exchange.

- The exchange rate is now 1 share per asset

Bob transfers 1 token to the vault (1e18 units) using an ERC-20 transfers. No shares are minted in exchange.

- The rate is now 1 share for 1e18+1 asset

Alice deposit is executed. Her 1e18 units of token are not even worth one unit of shares. So the contract takes the assets, but mint no shares. Alice basically donated her tokens.

- The rate is now 1 share for 2e18+1 asset

Bob redeem its 1 wei of shares, getting the entire vault assets in exchange. This includes all the token he deposited and transfered plus Alice’s tokens.

The main issue here was that Alice was not able to limit the slippage and make the transaction revert when the shares she got were diluted away. The math here are an extrem example, showing how Alice can lose everything, but other number could leave Alice with an arbitrary small (but not null) amount. So just reverting is the number of shares minted by a deposit is 0 is not solving the attack scenario.

# Proposed mitigation

I believe this issue would be mitigated if the vault represented the shares with more precision that the assets. If shares were not represented with the same 18 decimals as the asset, but with 36, then Alice’s assets would have been represented properly. In order to dilute Alice’s assets, the attacker would have needed to inflate the exchange rate by ad additional factor of 1e18. The attacker donation would have required 1e18 tokens (1e36 wei).

A way to achieve that is to take an additional parameter when constructing the vault, the *decimal offset*. This parameter is used such that the `decimals` exposed by the EIP-4626 vault’s are potentially larger than the underlying asset’s.

In addition, this *offset* is used to add virtual shares and assets to the vault. When computing the exchange rate, the ratio is no longer between `totalAssets()` and `totalSupply()`. It is the ratio between `totalAssets() + 1` and `totalSupply()+10**offset`. Therefore, even when the vault is empty, the rate is properly definned, and no special treatment is need.

If we replay the previous attack scenario with an offset of `9`:

- The vault is empty.

The exchange rate is the default 1e9 share units for each token unit (consequence of the virtual assets and shares)

Bob sees Alice’s transaction in the mempool and decide to sandwitch it.
Bob deposits 1 wei to the vault, gets 1e9 wei of shares in exchange.

- The exchange rate is still 1e9 share units for each token unit

Bob transfers 1 token to the vault (1e18 units) using an ERC-20 transfers. No shares are minted in exchange.

- The rate is now 2e9 share units (1e9 for Bob + 1e9 virtual) for 1e18+2 token units (1 from bob, 1 virtual and 1e18 from the donation), ie about 5e8 token units per share unit

This action inflated the rate by a factor 5e17, but thanks to the offset, we have some precision left to represent Alice’s upcomming deposit

Alice deposit is executed. Her 1e18 units of token are worth 2e9-1 unites of shares.

- The rate is now 4e9-1 share units for 2e18+2 token units. ie about 5e8 token units per share unit

If Alice redeems, she would get almost what she put in, losing only some wei of asset to the rounding.
If Bob redeems, we would only get half of what he donated to the vault, the other half being capture by the vault as he owned only 50% of the shares when the donation happens.

Bob could have made a bigger deposit before the donation, so that he was able to recover a larger fraction of that donation… but that would have increassed the number of shares, requiering an even bigger donation to try to inflate the exchange rate.

# Analysis

By creating a large number of virtual shares (10**offset) we increase by `offset` orders of magnitude the size of the donation necessary to inflate the exchange rate. In addition, the virtual assets/shares captures some of the donation, forcing the attacker to do an bigger deposit, and a bigger donation. If the attacker doesn’t want to lost more than .1% to the vault, it must buy in at least 1000 times what the vault’s virtual asset represent, adding to the `totalSupply()` and increassing the size of its donation by the same factor. Doing so, he decreases the faction lost to the vault, but not the absolute value. The virtual assets and shares effectivelly set a high price that the attacker has to pay to achieve inflation.

# Drawback

While the offset can be set to `0` to have similar decimals between the vault and the underlying asset, and minimize the amount of virtual assets and shares the vaults account for, the presence of 1 unit of virtual asset and 1 unit of virtual share does slightly modify the behavior of the contract.

Any developper that doesn’t like this approach can revert back to the previous one by overiding `_convertToShares` and `_convertToAssets` back to the 4.8 or 4.7 implementation.

# Where we need you

The approach discussed above has been implemented in [this PR](https://github.com/OpenZeppelin/openzeppelin-contracts/pull/3979). We welcome feedback and reviews. If you are a user of EIP-4626 we value your insight. Does this approach make sens to you? Would using it affect you positivelly or negativelly?

# Relevant links

- EIP-4626
- The PR
- Discussion about the attacks, and possible mitigations, on the OZ github
- Similar issue open on the Solmat github
- EIP-5143
- Fei’s ERC4626Router

## Replies

**joeysantoro** (2023-01-25):

This solution seems simple enough and effective! It could be a bit unintuitive to integrators I imagine, and can potentially lead to overflow issues with very large offsets.

One additional option used in [ERC4626/xERC4626.sol at main · fei-protocol/ERC4626 · GitHub](https://github.com/fei-protocol/ERC4626/blob/main/src/xERC4626.sol) is to maintain an internal balance of “assets” rather than using a manipulable instantaneous balance. This would be a slightly larger code lift, and add an additional sstore to each operation from a gas perspective.

---

**albertocuestacanada** (2023-01-25):

+1 to what [@joeysantoro](/u/joeysantoro) said, which is what we do at Yield with all contracts holding tokens and deriving data from them. The gas cost in keeping an internal balance of assets seems a good trade-off to close the attack surface existing in accepting token donations.

---

**Amxx** (2023-01-25):

We considered keeping an internal balance but it breaks some very legitimate use-cases for ERC-4626.

IMO, being able to donate to all the vault shareholders is a feature, not a bug. It can be combined with things like a vesting contract to create “staking” incentives. Also, it raises the question of what to do with tokens that are held by the vault but not accounted for. Are they lost? Do we need some governance to recover them?

Adding asset tracking on top of our code is decently easy to do by just overriding a few functions. Devs can opt into that (we even considered providing this directly). But if it was integrated by default, and someone wanted to opt out, they would likely still have to pay the gas cost of updating something they don’t use.

That is why we did not go for that option.

---

**artdgn** (2023-01-30):

Would “burning” some small amount of initial shares (as in [Uni V2](https://github.com/Uniswap/v2-core/blob/master/contracts/UniswapV2Pair.sol#L119-L124)) to `address(0)` be an insufficient mitigation?

---

**Amxx** (2023-01-30):

It depends on the amount, and the amount of shares you create in exchange. Its equivalent to doing a deposit before the first deposit, which makes frontrunning the very first deposit impossible, and thus makes the attack harder (but not impossible).

This is not generic though, and causes a few technical chalenges. So while we see it as a possible solution, we did not want to make it the default one.

---

**jat9292** (2023-02-07):

I like this solution a lot, as it is more flexible and efficient than the previously proposed ones.

By the way, I think there is a small typo in your mitigation paragraph, `totalAssets() + 10**offset` and `totalSupply()+1` should be replaced by `totalAssets() + 1 ` and `totalSupply()+ 10**offset`. This confused me at first.

I can see just one undesirable corner cases when the asset has 0 decimal (or very few decimals) and each wei of asset has already substantial value, but this is almost never the case, except for the Cryptopunks contract as far as I know.

Also, maybe you should add some reasonable maximum value for the decimal offset to avoid overflows?

---

**sbacha** (2023-02-07):

This is just a variation of the same exploit that can occur when creating a new liquidity pool in uniswap v2. The dapphub audit details this issue, so this is already a known design issue. The solution is to permanently lock the initial deposit in perpetuity.

---

**fubuloubu** (2023-02-18):

Don’t think this is necessary, the issue with Uniswap that requires burning some initial shares is that the pool is devoid of context, and the first deposit sets the initial exchange rate for pair.

Vaults don’t have those issues (the exchange rate is based on internal accounting, not a relationship that needs to be established), and we can use context to establish a better solution.

The root cause of the issue is the ability to manipulate the internal accounting more easily with a relatively low share of a token’s total supply. Ultimately, this is very use case-specific since the means of updating the exchange rate is the real cause of large swings in it’s value, but we can add an additional protection by ensuring the first deposit is at least X tokens (some value small enough not to be a bother to most users, but large enough to limit the effectiveness of exchange rate manipulation when the Vault first starts processing deposits).

This solution would mean that X could never be fully withdrawn (without some sort of alternative mode like a Shutdown where all shares are pushed to redemption), but for most use cases that’s a decent trade-off since Vaults are intended to be long-lasting and inevitably some amount of shares ends up “lost” by it’s owners anyways.

---

Lastly, will mention the paragraph at the bottom of [EIP4626’s Security](https://eips.ethereum.org/EIPS/eip-4626#security-considerations) section:

> Although the convertTo functions should eliminate the need for any use of an EIP-4626 Vault’s decimals variable, it is still strongly recommended to mirror the underlying token’s decimals if at all possible, to eliminate possible sources of confusion and simplify integration across front-ends and for other off-chain users.

Which would discourage the OP’s solution for this scenario as it changes the decimal amounts between the Vault and it’s underlying asset.

---

**pcaversaccio** (2023-02-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fubuloubu/48/2484_2.png) fubuloubu:

> but we can add an additional protection by ensuring the first deposit is at least X tokens

At first sight, I liked this idea, but this feels economically a suboptimal solution after deeply reflecting on it. I mean, essentially, it’s requiring burning money and we should think about alternative solutions that do not require it (money should be considered a scarce and valuable source). Also, depending on the implementation you could have the following use case (from [this](https://blog.openzeppelin.com/pods-finance-ethereum-volatility-vault-audit-2/) audit report):

> For example, if an early user put forth the minimum initial deposit and then the rest of the queue held dust amounts, the same user could withdraw far below the minimum initial deposit amount in the next round and the vault would be back in a vulnerable state. Consider taking steps to ensure the supply of vault shares does not go below the minimum initial deposit amount. One way to do this would be for the Pods Finance team to contribute their own initial deposit to the vault that they can guarantee will not be withdrawn.

So it requires first money as well as a certain trust into the first depositor. Generally, as you already have pointed out, I see the use-case specifics, but the initial minimum deposit strategy can also be considered as use-case specific. So I feel the OP’s solution is more use-case agnostic, but the minimum initial token deposit strategy is “simpler”, complies with the [EIP4626’s Security](https://eips.ethereum.org/EIPS/eip-4626#security-considerations) section, and can be an optimal implementation for certain projects who are willing to commit the funds and which you trust.

---

**fubuloubu** (2023-02-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/pcaversaccio/48/6329_2.png) pcaversaccio:

> essentially, it’s requiring burning mone

In the normal operation this would constitute a minimum balance for the contract. But you could also have a trigger that disallows deposits and unlocks full withdraws so it’s not a problem.

