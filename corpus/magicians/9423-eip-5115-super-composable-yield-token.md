---
source: magicians
topic_id: 9423
title: "EIP-5115: Super Composable Yield Token"
author: ayobuenavista
date: "2022-05-30"
category: EIPs
tags: [token, yield-bearing-tokens]
url: https://ethereum-magicians.org/t/eip-5115-super-composable-yield-token/9423
views: 6236
likes: 7
posts_count: 19
---

# EIP-5115: Super Composable Yield Token

---

## EIP: 5115
Title: Super Composable Yield Token
Description: Interface for wrapped yield-generating tokens.
Author: Vu Nguyen (mrenoon), Long Vuong (UncleGrandpa925), Anton Buenavista (ayobuenavista)
Discussions-To:
Status: Draft
Type: Standards Track
Category: ERC
Created: 2022-05-30
Requires: 20

## Abstract

This standard allows for the implementation of a standardized API for wrapped yield-generating tokens within smart contracts. This standard is an extension on the ERC-20 token that provides basic functionality for transferring, depositing, withdrawing tokens, and reading balances.

## Motivation

Yield generating mechanisms are built in all shapes and sizes, necessitating a manual integration every time a protocol builds on top of another protocol’s yield generating mechanism.

ERC-4626 tackled a significant part of this fragmentation by standardizing the interfaces for vaults, a major category among various yield-generating mechanisms.

In this EIP, we’re extending the coverage to include assets beyond ERC4626’s reach, namely:

- Yield-generating assets that have different base tokens used for minting vs accounting for the pool value.

This category includes AMM liquidity tokens (which are yield generating assets that yield swap fees) since the value of the pool is measured in “liquidity units” (for example, √k in UniswapV2, as defined in UniswapV2 whitepaper) which can’t be deposited in (as they are not tokens).
- This extends the flexibility in minting the yield-bearing assets. For example, there could be an ETH vault that wants to allow users to deposit cETH directly instead of ETH, for gas efficiency or UX reasons.

Assets with reward tokens by default (e.g. COMP rewards for supplying in Compound). The reward tokens are expected to be sold to compound into the same asset.

While ERC-4626 is a well-designed and suitable standard for most vaults, there will inevitably be some yield-generating mechanisms that do not fit into their category (LP tokens for instance). A more flexible standard is required to standardize the interaction with all types of yield generating mechanisms.

Therefore, we are proposing Super Composable Yield (SCY), a flexible standard for wrapped yield generating tokens that could cover most mechanisms in DeFi. We foresee that:

- ERC-4626 will still be a popular vault standard, that most vaults should adopt.
- SCY tokens can wrap over most yield generating mechanisms in DeFi, including ERC-4626 vaults for projects built on top of interest-bearing tokens.
- Whoever needs the functionalities of SCY could integrate with the existing SCY tokens or write a new SCY (to wrap over the target interest-bearing token).

### Use Cases

This EIP is designed for flexibility, aiming to accommodate as many yield generating mechanisms as possible. Particularly, this standard aims to be generalized enough that it supports the following uses cases and more:

- Money market supply positions

Lending DAI in Compound, getting DAI interests and COMP rewards
- Lending ETH in BenQi, getting ETH interests and QI + AVAX rewards
- Lending USDC in Aave, getting USDC interests and stkAAVE rewards

AMM liquidity provision

- Provide ETH + USDC to ETHUSDC pool in SushiSwap, getting swap fees in more ETH+USDC
- Provide ETH + USDC to ETHUSDC pool in SushiSwap and stake it in Sushi Onsen, getting swap fees and SUSHI rewards
- Provide USDC+DAI+USDT to 3crv pool and stake it in Convex, getting 3crv swap fees and CRV + CVX rewards

Vault positions

- Provide ETH into Yearn EIP-4626 vault, where the vault accrues yield from Yearn’s ETH strategy
- Provide DAI into Harvest and staking it, getting DAI interests and FARM rewards

Liquid staking positions

- Holding stETH (in Lido), getting yields in more stETH

Liquidity mining programs

- Provide USDC in Stargate, getting STG rewards
- Provide FEI in Tokemak, getting TOKE rewards
- Provide LOOKS in LooksRare, getting LOOKS yield and WETH rewards

Rebasing tokens

- Stake OHM into sOHM/gOHM, getting OHM rebase yield
- Stake BTRFLY into xBTRFLY, getting BTRFLY rebase yield

The EIP hopes to minimize, if not possibly eliminate, the use of customized adapters in order to interact with many different forms of yield-generating token mechanisms.

## Specification

### Generic Yield Generating Pool

We will first introduce Generic Yield Generating Pool (GYGP), a model to describe most yield generating mechanisms in DeFi. In every yield generating mechanism, there is a pool of funds, whose value is measured in **assets**. There are a number of users who contribute liquidity to the pool, in exchange for **shares** of the pool, which represents units of ownership of the pool. Over time, the value (measured in **assets**) of the pool grows, such that each **share** is worth more **assets** over time. The pool could earn a number of **reward tokens** over time, which are distributed to the users according to some logic (For example, proportionally the number of **shares**).

Here are the more concrete definitions of the terms:

**Definitions:**

- asset: Is a unit to measure the value of the pool. At time t, the pool has a total value of TotalAsset(t) assets.
- shares: Is a unit that represents ownership of the pool. At time t, there are TotalShares(t) shares in total.
- reward tokens: Over time, the pool earns nrewards types of reward tokens (nrewards ≥ 0). At time t, TotalRewardsi(t) is the amount of reward token i that has accumulated for the pool up until time t.
- exchange rate: At time t, the exchange rate ExchangeRate(t) is simply how many assets each shares is worth ExchangeRate(t) = TotalAsset(t) / TotalShares(t)
- users: At time t, each user u has sharesu(t) shares in the pool, which is worth assetu(t) = sharesu(t) • ExchangeRate(t)  assets. Until time t, user u is entitled to receive a total of rewardsui(t) reward token i. The sum of all users’ shares, assets and rewards should be the same as the total shares, assets and rewards of the whole pool.

**State changes:**

1. A user deposits assets into the pool, in exchange for new shares that will be created for the user, proportionally to the asset amount being deposited compared to the value of the pool.
2. A user withdraws assets from the pool, by burning their shares, proportionally to the asset amount being burned compared to the value of the pool
3. The pool earns some assets. The exchange rate will simply increase due to the additional assets.
4. The pool earns some reward tokens. The additional reward tokens will be distributed among the users.

**Examples of GYGPs in DeFi:**

| Yield generating mechanism | Asset | Shares | Reward tokens | Exchange rate |
| --- | --- | --- | --- | --- |
| Supply USDC in Compound | USDC | cUSDC | COMP | USDC value per cUSDC, increases with USDC supply interests |
| ETH liquid staking in Lido | stETH | wstETH | None | stETH value per wstETH, increases with ETH staking rewards |
| Stake LOOKS in LooksRare | LOOKS | shares (in contract) | WETH | LOOKS value per shares, increases with LOOKS rewards |
| Stake BTRFLY into xBTRFLY | BTRFLY | xBTRFLY | None | BTRFLY value per xBTRFLY, increases due to rebase rewards |
| Provide ETH+USDC liquidity on Sushiswap | ETHUSDC liquidity (a pool of x ETH + y USDC has sqrt(xy) ETHUSDC liquidity) | ETHUSDC Sushiswap LP (SLP) token | None | ETHUSDC liquidity value per ETHUSDC SLP, increases due to swap fees |
| Provide ETH+USDC liquidity on Sushiswap and stake into Onsen | ETHUSDC liquidity (a pool of x ETH + y USDC has sqrt(xy) ETHUSDC liquidity) | ETHUSDC Sushiswap LP (SLP) token | SUSHI | ETHUSDC liquidity value per ETHUSDC SLP, increases due to swap fees |
| Provide USDC+USDT+DAI liquidity in Curve | 3crv pool’s liquidity (amount of D per 3crv token) | 3crv token | CRV | 3crv pool’s liquidity per 3crv token, increases due to swap fees |
| Provide BAL+WETH liquidity in Balancer (80% BAL, 20% WETH) | BALWETH liquidity (a pool of x BAL + y WETH has x0.8 * y0.2 BALWETH liquidity) | BALWETH Balancer LP token | None | BALWETH liquidity per BALWETH Balancer LP token, increases due to swap fees |

### Super Composable Yield Token Standard

**Overview**

Super Composable Yield is a token standard for all GYGPs. Each Super Composable Yield token represents **shares** in a GYGP and allows for interacting with the GYGP via a standard interface

All SCY tokens:

- MUST implement ERC20 to represent shares in the underlying GYGP.
- MUST implement ERC-20’s optional metadata extensions name, symbol, and decimals, which SHOULD reflect the underlying GYGP’s accounting asset’s name, symbol, and decimals.
- MAY implement EIP-2612 to improve the UX of approving SCY tokens on various integrations.
- MAY revert on calls to transfer and transferFrom if a SCY token is to be non-transferable.
- The ERC-20 operations balanceOf, transfer, totalSupply, etc. SHOULD operate on the GYGP “shares”, which represent a claim to ownership on a fraction of the GYGP’s underlying holdings.

**Definition of base tokens**

Base tokens are tokens that could be deposited to mint SCY tokens (and hence, to enter the underlying GYGP), or redeemed when burning SCY tokens (and hence, exiting the underlying GYGP). Essentially, base tokens are implicitly converted into units of **assets** when deposited or redeemed, to conform to state change #1 and #2 of the GYGP definition above.

There could be multiple base tokens in a SCY. This allows for maximum flexibility in how to mint SCY to enter the underlying yield generating pool. For example, both BAL and WETH (and even BALWETH LP token) could be used to mint the SCY token for BALWETH Balancer pool (by providing single-sided liquidity).

As such, base tokens are not necessarily the same as the asset (which is a key difference between SCY and ERC-4626).

**Interface**

```auto
interface ISuperComposableYield {
    enum AssetType {
        TOKEN,
        LIQUIDITY
    }

    event Deposit(
        address indexed caller,
        address indexed receiver,
        address indexed tokenIn,
        uint256 amountDeposited,
        uint256 amountScyOut
    );

    event Redeem(
        address indexed caller,
        address indexed receiver,
        address indexed tokenOut,
        uint256 amountScyToRedeem,
        uint256 amountTokenOut
    );

    event ClaimRewards(address indexed caller, address indexed user, address[] rewardTokens, uint256[] rewardAmounts);

    event ExchangeRateUpdated(uint256 oldExchangeRate, uint256 newExchangeRate);

    function deposit(
        address receiver,
        address tokenIn,
        uint256 amountTokenToPull,
        uint256 minSharesOut
    ) external returns (uint256 amountSharesOut);

    function redeem(
        address receiver,
        uint256 amountSharesToPull,
        address tokenOut,
        uint256 minTokenOut
    ) external returns (uint256 amountTokenOut);

    function claimRewards(address user) external returns (uint256[] memory rewardAmounts);

    function exchangeRateCurrent() external returns (uint256);

    function exchangeRateStored() external view returns (uint256);

    function getRewardTokens() external view returns (address[] memory);

    function yieldToken() external view returns (address);

    function getBaseTokens() external view returns (address[] memory);

    function isValidBaseToken(address token) external view returns (bool);

    function assetInfo()
        external
        view
        returns (
            AssetType assetType,
            address assetAddress,
            uint8 assetDecimals
        );

    function name() external view returns (string memory);

    function symbol() external view returns (string memory);

    function decimals() external view returns (uint8);
}
```

**Methods**

```auto
function deposit(
    address receiver,
    address tokenIn,
    uint256 amountBaseIn,
    uint256 minAmountScyOut
) external returns (uint256 amountScyOut);
```

This method will first pull `amountTokenToPull` of `tokenIn` (a **base token**), and use the floating amount `tokenIn` in the SCY contract to deposit to mint new **shares**.

The ideal way to deposit is to send `tokenIn` in first, then call the `deposit` function with `amountTokenToPull = 0`. This pattern is similar to UniswapV2 (and UniswapV3) pools, which allow for better composability and gas efficiency by minimizing token transfers. For example, a router contract could swap from some other token to `tokenIn` which is sent directly to the SCY contract before `deposit` is called.

This function will convert the amount of `tokenIn` into some worth of assets and deposit this amount into the SCY contract for the recipient, who will receive `amountSharesOut` of SCY tokens (**shares**).

- MUST emit the Deposit event.
- MUST support ERC-20’s approve / transferFrom flow where tokenIn are taken from receiver directly (as msg.sender) or if the msg.sender has ERC-20 approved allowance over the base token of the receiver.
- MUST revert if amountScyOut < minAmountScyOut (due to deposit limit being reached, slippage, or the user not approving enough tokenIn to the SCY contract, etc).

```auto
function redeem(
    address receiver,
    uint256 amountSharesToPull,
    address tokenOut,
    uint256 minAmountBaseOut
) external returns (uint256 amountBaseOut);
```

This function will redeem the exact SCY token (**shares**) from the SCY contract. The **assets** are converted into `amountBaseOut` of `baseTokenOut`. Most implementations will require pre-approval of the SCY contract with the SCY token.

- MUST emit the Redeem event.
- MUST support ERC-20’s approve / transferFrom flow where the shares are burned from receiver directly (as msg.sender) or if the msg.sender has ERC-20 approved allowance over the shares of the receiver.
- MUST revert if tokenOut < minTokenOut (due to redeem limit being reached, slippage, or the user not approving enough amountSharesToPull to the SCY contract, etc).

```auto
function claimRewards(address user) external returns (uint256[] memory rewardAmounts);
```

This method sends all the available claimable rewards to the user as is, with the amounts in the list being in the same order as `getRewardTokens`.

- MUST emit the ClaimRewards event.
- MAY return one or multiple rewards to the user.
- MAY return zero rewards to the user.

```auto
function exchangeRateCurrent() external returns (uint256);
```

This method updates and returns the latest **exchange rate**, which is the **exchange rate** from SCY token amount into asset amount, scaled by a fixed scaling factor of 1e18.

- MUST return ExchangeRate(tnow) such that ExchangeRate(tnow) • scyBalance / 1e18 = assetBalance.
- MUST NOT include fees that are charged against the underlying yield token in the SCY contract.

```auto
function exchangeRateStored() external view returns (uint256);
```

This read-only method returns the last saved value of the exchange rate.

- MUST return the value of exchangeRateCurrent() of a past timestamp where it was last updated in the contract
- MUST NOT include fees that are charged against the underlying yield token in the SCY contract.
- MUST NOT revert.

```auto
function yieldToken() external view returns (address);
```

This read-only method returns the underlying yield-generating token (representing a GYGP) that was wrapped into a SCY token.

- MUST return a token address that conforms to the ERC-20 interface, or zero address
- MUST NOT revert.
- MUST reflect the exact underlying yield-generating token address if the SCY token is a wrapped token.
- MAY return 0x or zero address if the SCY token is natively implemented, and not from wrapping.

```auto
function getRewardTokens() external view returns (address[] memory);
```

This read-only method returns the latest list of all reward tokens.

- MUST return ERC-20 token addresses.
- MUST NOT revert.
- MAY return an empty list, one, or several token addresses.
- MAY return additional reward tokens over time, depending on when underlyingYieldToken supports more or less reward tokens.

```auto
function getBaseTokens() external view returns (address[] memory);
```

This read-only method returns the list of all base tokens that can be used to deposit into the SCY contract.

- MUST return ERC-20 token addresses.
- MUST return at least one address.
- MUST NOT revert.

```auto
function isValidBaseToken(address token) external view returns (bool);
```

This read-only method checks whether a token address entered is a base token that can be used to mint SCY.

- MUST NOT revert.

```auto
function assetInfo()
        external
        view
        returns (
            AssetType assetType,
            address assetAddress,
            uint8 assetDecimals
        );
```

This read-only function returns useful information about the asset, intended for front-ends or off-chain systems to display balances and information about the asset.

`decimals` is the decimals to format asset balances.

Convention for `assetType` and format of the `info` field:

- If asset is an ERC20 token: `assetType = 0`, `assetAddress` is the address of the token.

- If asset is liquidity of an AMM (like √k  in UniswapV2 forks), `assetType = 1`, `assetAddress` is the address of the LP token.

- MUST reflect the underlying asset’s decimals if at all possible in order to eliminate any possible source of confusion or be deemed malicious.
- MUST conform to the conventions for assetType and info.
- MUST NOT revert.

**Events**

```auto
event Deposit(
    address indexed caller,
    address indexed receiver,
    address indexed tokenIn,
    uint256 amountDeposited,
    uint256 amountScyOut
);
```

`caller` has converted exact base tokens into SCY (shares) and transferred those SCY to `receiver`.

- MUST be emitted when base tokens are deposited into the SCY contract via deposit method.

```auto
event Redeem(
    address indexed caller,
    address indexed receiver,
    address indexed tokenOut,
    uint256 amountScyToRedeem,
    uint256 amountTokenOut
);
```

`caller` has converted exact SCY (shares) into base tokens and transferred those base tokens to `receiver`.

- MUST be emitted when base tokens are redeemed from the SCY contract via redeem method.

```auto
event ClaimRewards(
    address indexed caller,
    address indexed user,
    address[] rewardTokens,
    uint256[] rewardAmounts
);
```

`caller` has claimed user rewards and transferred them to the user.

- MUST be emitted when rewards are claimed from the SCY contract via claimRewards method.

```auto
event ExchangeRateUpdated(uint256 oldExchangeRate, uint256 newExchangeRate);
```

The `exchangeRateCurrent` is updated to the latest exchange rate.

- MUST be emitted when the exchange rate is updated in the SCY contract via exchangeRateCurrent method.

**“SCY” Word Choice:**

“SCY” (pronunciation: */sʌɪ/*), an abbreviation of Super Composable Yield, was found to be appropriate to describe a broad universe of composable yield-bearing digital assets.

## Rationale

EIP-20 is enforced because implementation details such as transfer, token approvals, and balance calculation directly carry over to the SCY tokens. This standardization makes the SCY tokens immediately compatible with all EIP-20 use cases.

EIP-165 is not explicitly mentioned to be supported as there are no optional methods in this standard. It is expected for all methods defined in the interface to be implemented.

EIP-2612 can optionally be implemented in

order to improve the UX of approving SCY tokens on various integrations.

The `exchangeRateStored` read-only method serves as a rough estimate of the prevalent exchange rate since the last update. It is included for frontends, wallets, and applications that need an estimate on the exchange rate of SCY tokens into assets, not an exact value possibly including slippage or other fees as this would require them doing a state update and spending gas. For applications that need an exact exchange rate, the `exchangeRateCurrent` mutable function can be used.

## Backwards Compatibility

This EIP is fully backwards compatible as its implementation extends the functionality of ERC-20, however the optional metadata extensions, namely `name`, `decimals`, and `symbol` semantics MUST be implemented for all SCY token implementations.

## Security Considerations

Malicious implementations which conform to the interface can put users at risk. It is recommended that all integrators (such as wallets, aggregators, or other smart contract protocols) review the implementation to avoid possible exploits and users losing funds.

The method `exchangeRateStored` returns an outdated estimated value and does not confer the exact current exchange rate of asset per share. Should accuracy be needed, `exchangeRateCurrent` should be used instead, and in addition, will update `exchangeRateStored`.

`decimals` in `assetInfo` must strongly reflect the underlying asset’s decimals if at all possible in order to eliminate any possible source of confusion or be deemed malicious.

`underlyingYieldToken` must strongly reflect the address of the underlying wrapped yield-generating token. For a native implementation wherein the SCY token does not wrap a yield-generating token, but natively represents a GYGP share, then the address returned MAY be a zero address. Otherwise, for wrapped tokens, you may introduce confusion on what the SCY token represents, or may be deemed malicious.

## Copyright

Copyright and related rights waived via CC0.

## Replies

**SamWilsn** (2022-06-03):

You might want to add explicit support for [EIP-165](https://eips.ethereum.org/EIPS/eip-165).

---

**ayobuenavista** (2022-06-06):

Thanks for the suggestion. Our team discussed this briefly. Since we don’t have optional methods, we didn’t find a need to support EIP-165. In other words, protocols integrating EIP-5115 should expect all the methods in the interface to be implemented.

---

**ayobuenavista** (2022-06-06):

To add, you can view some of the sample implementations here: https://github.com/pendle-finance/pendle-scy-sample/

---

**SamWilsn** (2022-06-06):

EIP-165 isn’t about indicating which methods are implemented, but rather which interfaces. You can use EIP-165 to determine whether an arbitrary address claims to support `ISuperComposableYield` as a whole.

For example, imagine adding a token to your wallet. With EIP-165, the wallet can go out and discover if the token is EIP-5115 compatible, and if so, display specific extra UI elements for yield tokens.

---

**tarif** (2022-06-10):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ayobuenavista/48/5982_2.png) ayobuenavista:

> To add, you can view some of the sample implementations here: https://github.com/pendle-finance/pendle-scy-sample/

Thank you for sample link.

zaun

---

**marcelomorgado** (2022-06-21):

Hi, well done!

One thing that isn’t too clear for me is regarding the AMM GYGP examples:

For instance:

`Supply USDC in Compound` has USDC as Asset (ok this is straightforward)

But `Provide ETH+USDC liquidity on Sushiswap` mechanism hasn’t ETH and USDC as assetS? Why referring to sqrt(xy) math? I mean, aren’t the “Asset(s)” the underlying asset(s) of a mechanism?

**asset**: Is a unit to measure the value of the pool. At time *t*, the pool has a total value of *TotalAsset(t)* **assets**. Isn’t the ETH+USDC balance of the pool its value measure?

Could you clarify that for me?

Thanks!

---

**marcelomorgado** (2022-06-21):

Another question also regarding AMM, shouldn’t deposit allows depositing more than one token simultaneously? Let’s taking as an example a pair pool that exists but has no liquidity, user won’t be able to perform a swap like [this](https://github.com/pendle-finance/pendle-scy-sample/blob/main/contracts/SuperComposableYield/SCY-implementations/PendleJoeLpSCY.sol#L46).

Thanks again

---

**ayobuenavista** (2022-06-22):

> Isn’t the ETH+USDC balance of the pool its value measure?

Yes. For AMMs, when you deposit ETH and USDC into a pool, you get an LP token back which represents your share of the ETH+USDC pool balance. The value of the pool is measured in liquidity, which is √k (or √x · y). x and y in this case represent ETH and USDC in the pool. When fees collected in the pool increase, √k increases. So valuing the pool by √k is no different from valuing the pool by its ETH+USDC balance.

---

**ayobuenavista** (2022-06-22):

For AMMs, the base tokens that can be defined for deposing, e.g., for an ETHUSDC-SCY, ETH or USDC or ETHUSDC LP. You can define the SCY to only accept LP tokens as input. Accepting other base tokens is more of a convenience for the user and implementation can be flexible enough to accommodate different base tokens and different checks, such as a pool not having enough liquidity for zapping in.

Which is already accounted for in the example [here](https://github.com/pendle-finance/pendle-scy-sample/blob/main/contracts/SuperComposableYield/SCY-implementations/PendleJoeLpSCY.sol#L44).

---

**marcelomorgado** (2022-06-23):

Got you Anton, thanks

Would you say that EIP-5115 is more suitable for wrapping yield generating pools instead of used as the interface for yield generation pools implementation?

Best

---

**ayobuenavista** (2022-06-23):

Newer yield generating pools can definitely adopt it as their native interface. But yes, you can think of EIP-5115 as more of a wrapping standard for existing yield generating pools.

---

**alberqo** (2022-08-09):

This question may expose me as a neophyte, but does “fully” backwards compatible mean ***fully*** backwards compatible? For example, could a contract designed to receive ERC-20 tokens presumably receive SCYT’s?

Further, what do your gas cost estimates look like for wrapping **shares** into SCYTs, and transacting/permissioning with said SCYTs?

This looks like interesting work!

---

**ayobuenavista** (2022-08-10):

All questions are always welcome! ![:smiley:](https://ethereum-magicians.org/images/emoji/twitter/smiley.png?v=12)

As SCY is extending ERC20, whichever dapp is supporting ERC20, SCY can be used there too, e.g. DEXes, money markets, other DeFi dapps, etc.

As for gas estimations, it depends on the SCY implementation, as each SCY differs on which underlying protocol it represents and the method. For example, something as simple as wrapping an aToken (i.e. aUSDT) from Aave migh be 100k-150k gas. But since SCY also allows other base tokens such as USDT, SCY will do the complete process where USDT is deposited into Aave for aUSDT and then stored in the SCY contract. That can cost upwards of 300k gas.

For transfers/approvals, the gas cost should be about the same as your typical ERC20 token.

---

**magicSpoon** (2022-08-31):

Hi all! ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

[@ayobuenavista](/u/ayobuenavista) based on my interpretation of the EIP description, I imagined a SCY based on Sushiswap WETH/USDC pool that would work as follows:

**Deposit**

- Send 1 ETH (passing address(0) as the tokenIn and inserting the payable modifier to the deposit method, which however does not alter the ABI/selector of the method),
- wrap ETH in Weth
- 0.5 Weth would be swapped into USDC
- addLiquidity using Weth/USDC generating the LP token and so the shares .

Same thing directly using Weth (instead of ETH) or USDC as `tokenIn`.

**Redeem**

While for `redeem` would be done:

- remove liquidity burning LP tokens
- the extracted amount other than the tokenOut would be swapped to get only tokenOut amount → Ex. Remove liquidity LP Weth/USDC → swap USDC in Weth → you get only Weth → if tokenOut is equal to address(0) Weth is unwrapped in ETH → you get ETH

Is this a correct implementation of the EIP? thanks

---

**magicSpoon** (2022-09-04):

Hey [@ayobuenavista](/u/ayobuenavista) any news about my previous message ? thanks!! ![:grin:](https://ethereum-magicians.org/images/emoji/twitter/grin.png?v=12)

---

**ayobuenavista** (2022-09-05):

Hi [@magicSpoon](/u/magicspoon). You are correct on the deposit/redeem workflow, and we would do it the same way as well. Also just a heads up, we’re about to release Pendle V2, which integrates with different SCYs. So you’d be able to see the different implementations.

---

**magicSpoon** (2022-09-05):

Thank you very much [@ayobuenavista](/u/ayobuenavista) for your reply ![:grin:](https://ethereum-magicians.org/images/emoji/twitter/grin.png?v=12), where can I find info about PendleV2? (Is it pendle.finance??) Will you write something here in this discussion?

Also, again referring to the example with the SushiSwap WETH-USDC pool, I had three questions about Ethereum:

1. will you use address(0) as the supportedToken to define that it is pure ETH?
2. again in the case of the sushiswap pool in the example, will the baseTokens then be 3? address(0), WETH, USDC?
3. at this point wouldn’t it be better to include the modifier payable to the deposit method in the draft EIP by default?

thanks again ![:slightly_smiling_face:](https://ethereum-magicians.org/images/emoji/twitter/slightly_smiling_face.png?v=12)

---

**ayobuenavista** (2022-09-05):

We have not announced anything major yet regarding V2 yet, but it should be very soon. Once we do, I’ll post all the relevant links here.

> will you use address(0) as the supportedToken to define that it is pure ETH?
> We’ve seen some protocols use address(0) and some use the alias 0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE. If we are to use a common alias to denote the native currency, then address(0) might be more preferred since it appears more neutral. Currently, we’re still using address(0). If ever this recommendation changes, we will update the EIP to mention this.

> again in the case of the sushiswap pool in the example, will the baseTokens then be 3? address(0), WETH, USDC?

Yes, with address(0) denoting ETH.

> at this point wouldn’t it be better to include the modifier payable to the deposit method in the draft EIP by default?

The standard allows the flexibility for the SCY token itself to handle wrapping/unwrapping natively. But this is not required. So whether to make it payable/non-payable is also flexible. I guess we can just make it clearer in the standard by adding `MAY be payable` for deposit().

Also, we will have an update on the EIP soon based on the feedback we’ve gathered.

