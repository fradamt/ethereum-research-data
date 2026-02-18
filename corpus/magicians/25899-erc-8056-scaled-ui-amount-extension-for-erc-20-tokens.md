---
source: magicians
topic_id: 25899
title: "ERC-8056: Scaled UI Amount Extension for ERC-20 Tokens"
author: cridmann
date: "2025-10-20"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-8056-scaled-ui-amount-extension-for-erc-20-tokens/25899
views: 345
likes: 6
posts_count: 8
---

# ERC-8056: Scaled UI Amount Extension for ERC-20 Tokens

For the full ERC, see [Add ERC: Scaled UI Amount Extension for ERC-20 Tokens by cridmann · Pull Request #1283 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/1283)

### ABSTRACT

---

This EIP proposes a standard extension to ERC-20 tokens that enables issuers to apply an updatable multiplier to the UI (user interface) amount of tokens. This allows for efficient representation of stock splits, without requiring actual token minting or transfers. The extension provides a cosmetic layer that modifies how token balances are displayed to users while maintaining the underlying token economics.

### MOTIVATION

---

Current ERC-20 implementations lack an efficient mechanism to handle real-world asset scenarios such as stock splits: When a company performs a 2-for-1 stock split, all shareholders should see their holdings double. Currently, this requires minting new tokens to all holders, which is gas-intensive and operationally complex. Moreover, the internal accounting in DeFi protocols would break from such a split.

The inability to efficiently handle this scenario limits the adoption of tokenized real-world assets (RWAs) on Ethereum. This EIP addresses these limitations by introducing a multiplier mechanism that adjusts the displayed balance without altering the actual token supply.

### SPECIFICATION

---

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

#### Interface:

```solidity
interface IScaledUIAmount {
    // Emitted when the UI multiplier is updated
    event UIMultiplierUpdated(uint256 oldMultiplier, uint256 newMultiplier, uint256 setAtTimestamp, uint256 effectiveAtTimestamp);

    // Returns the current UI multiplier
    // Multiplier is represented with 18 decimals (1e18 = 1.0)
    function uiMultiplier() external view returns (uint256);

    // Converts a raw token amount to UI amount
    function toUIAmount(uint256 rawAmount) external view returns (uint256);

    // Converts a UI amount to raw token amount
    function fromUIAmount(uint256 uiAmount) external view returns (uint256);

    // Returns the UI-adjusted balance of an account
    function balanceOfUI(address account) external view returns (uint256);

    // Updates the UI multiplier (only callable by authorized role)
    function setUIMultiplier(uint256 newMultiplier, uint256 effectiveAtTimestamp) external;
}

```

#### Implementation Requirements:

1. Multiplier Precision: The UI multiplier MUST use 18 decimal places for precision (1e18 represents a multiplier of 1.0).
2. Backwards Compatibility: The standard ERC-20 functions (balanceOf, transfer, transferFrom, etc.) MUST continue to work with raw amounts.
3. Event Emission: The UIMultiplierUpdated event MUST be emitted whenever the multiplier is changed.

### REFERENCE IMPLEMENTATION

---

```solidity
contract ScaledUIToken is ERC20, IScaledUIAmount, Ownable {
    uint256 private constant MULTIPLIER_DECIMALS = 1e18;
    uint256 private _uiMultiplier = MULTIPLIER_DECIMALS; // Initially 1.0
    uint256 public _nextUiMultiplier = MULTIPLIER_DECIMALS;
    uint256 public _nextUiMultiplierEffectiveAt = 0;

    constructor(string memory name, string memory symbol) ERC20(name, symbol) {}

    function uiMultiplier() public view override returns (uint256) {
        uint256 currentTime = block.timestamp;
	   if (currentTime >= _nextUiMultiplierEffectiveAt) {
		return _nextUiMultiplier;
   } else {
      return _uiMultiplier;
   }
    }

    function toUIAmount(uint256 rawAmount) public view override returns (uint256) {
	   uint256 currentTime = block.timestamp;
        if (currentTime >= _nextUiMultiplierEffectiveAt) {
        	return (rawAmount * _nextUiMultiplier) / MULTIPLIER_DECIMALS;
        } else {
        	return (rawAmount * _uiMultiplier) / MULTIPLIER_DECIMALS;
   }
    }

    function fromUIAmount(uint256 uiAmount) public view override returns (uint256) {
	   if (currentTime >= _nextUiMultiplierEffectiveAt) {
return (uiAmount * MULTIPLIER_DECIMALS) / _nextUiMultiplier;
   } else {
	return (uiAmount * MULTIPLIER_DECIMALS) / _uiMultiplier;
    }

    }

    function balanceOfUI(address account) public view override returns (uint256) {
        return toUIAmount(balanceOf(account));
    }

    function setUIMultiplier(uint256 newMultiplier, uint256 effectiveAtTimestamp) external override onlyOwner {
        require(newMultiplier > 0, "Multiplier must be positive");

	   uint256 currentTime = block.timestamp;
        require(effectiveAtTimestamp > currentTime, "Effective At must be in the future");

	   if (currentTime > _nextUiMultiplierEffectiveAt) {
	uint256 oldMultiplier = _nextUiMultiplier;
	_uiMultiplier = oldMultiplier;
	_nextUiMultiplier = newMultiplier;
     _nextUiMultiplierEffectiveAt = effectiveAtTimestamp;
     emit UIMultiplierUpdated(oldMultiplier, newMultiplier,    block.timestamp, effectiveAtTimestamp);
   } else {
	uint256 oldMultiplier = _uiMultiplier;
     _nextUiMultiplier = newMultiplier;
     _nextUiMultiplierEffectiveAt = effectiveAtTimestamp;
     emit UIMultiplierUpdated(oldMultiplier, newMultiplier,    block.timestamp, effectiveAtTimestamp);
   }
    }
}

```

### RATIONALE

---

Design Decisions:

1. Separate UI Functions: Rather than modifying the core ERC-20 functions, we provide separate UI-specific functions. This ensures backward compatibility and allows integrators to opt-in to the UI scaling feature.
2. 18 Decimal Precision: Using 18 decimals for the multiplier provides sufficient precision for most use cases while aligning with Ethereum’s standard decimal representation.
3. No Automatic Updates: The multiplier must be explicitly set by authorized parties, giving issuers full control over when and how adjustments are made.
4. Raw Amount Preservation: All actual token operations continue to use raw amounts, ensuring that the multiplier is purely a display feature and doesn’t affect the underlying token economics.

Alternative Approaches Considered:

1. Rebasing Tokens: While rebasing tokens adjust supply automatically, they create complexity for integrators and can break composability with DeFi protocols.
2. Wrapper Tokens: Creating wrapper tokens for each adjustment event adds unnecessary complexity and gas costs.
3. Index/Exchange Rate Tokens confer similar advantages to the proposed Scaled UI approach, but is ultimately less intuitive and requires more calculations on the UI layers.
4. Off-chain Solutions: Purely off-chain solutions lack standardization and require trust in centralized providers.

[![token_value_repr](https://ethereum-magicians.org/uploads/default/optimized/3X/4/f/4fa48fcfa6713c4a79ebc1934c737bfa1567da2d_2_681x500.jpeg)token_value_repr1299×953 98.5 KB](https://ethereum-magicians.org/uploads/default/4fa48fcfa6713c4a79ebc1934c737bfa1567da2d)

[![token_arch_layers](https://ethereum-magicians.org/uploads/default/optimized/3X/e/a/ea7e62af62fca019c82f8f7da02168fb3d3021b1_2_689x436.jpeg)token_arch_layers1292×818 104 KB](https://ethereum-magicians.org/uploads/default/ea7e62af62fca019c82f8f7da02168fb3d3021b1)

### BACKWARDS COMPATIBILITY

---

This EIP is fully backwards compatible with ERC-20. Existing ERC-20 functions continue to work as expected, and the UI scaling features are opt-in through additional functions.

### TEST CASES

---

Example test scenarios:

1. Initial Multiplier Test:

- Verify that initial multiplier is 1.0 (1e18)
- Confirm balanceOf equals balanceOfUI initially

1. Stock Split Test:

- Set multiplier to 2.0 (2e18) for 2-for-1 split
- Verify UI balance is double the raw balance
- Confirm conversion functions work correctly

### SECURITY CONSIDERATIONS

---

1. Multiplier Manipulation

- Unauthorized changes to the UI multiplier could mislead users about their holdings
- Implementations MUST use robust access control mechanisms
- The setUIMultiplier function MUST be restricted to authorized addresses (e.g., contract owner or a designated role).

1. Integer Overflow

- Risk of overflow when applying the multiplier
- Use SafeMath or Solidity 0.8.0+ automatic overflow protection

1. User Confusion

- Clear communication is essential when UI amounts differ from raw amounts
- Integrators MUST clearly indicate when displaying UI-adjusted balances

1. Oracle Dependency

- For automated multiplier updates, the system may depend on oracles
- Oracle failures or manipulations could affect displayed balances

1. Overflow Protection: Implementations MUST handle potential overflow when applying the multiplier.

### IMPLEMENTATION GUIDE FOR INTEGRATORS

---

#### WALLET INTEGRATION

Wallets supporting this standard should:

1. Check if a token implements IScaledUIAmount interface
2. Display both raw and UI amounts, clearly labeled
3. Use balanceOfUI() for primary balance display
4. Handle transfers using raw amounts (standard ERC-20 functions)

**Example JavaScript integration:**

```javascript
async function displayBalance(tokenAddress, userAddress) {
    const token = new ethers.Contract(tokenAddress, ScaledUIAmountABI, provider);

    // Check if scaled UI is supported
    const supportsScaledUI = await supportsInterface(tokenAddress, SCALED_UI_INTERFACE_ID);

    if (supportsScaledUI) {
        const uiBalance = await token.balanceOfUI(userAddress);
        const rawBalance = await token.balanceOf(userAddress);
        const multiplier = await token.uiMultiplier();

        return {
            display: formatUnits(uiBalance, decimals),
            raw: formatUnits(rawBalance, decimals),
            multiplier: formatUnits(multiplier, 18)
        };
    } else {
        // Fall back to standard ERC-20
        const balance = await token.balanceOf(userAddress);
        return {
            display: formatUnits(balance, decimals),
            raw: formatUnits(balance, decimals),
            multiplier: "1.0"
        };
    }
}

```

#### EXCHANGE INTEGRATION

Exchanges should:

1. Store and track the multiplier for each supported token
2. Display UI amounts in user interfaces
3. Use raw amounts for all internal accounting
4. Provide clear documentation about the scaling mechanism

Example implementation:

```javascript
class ScaledTokenHandler {
    async processDeposit(tokenAddress, amount, isUIAmount) {
        const token = new ethers.Contract(tokenAddress, ScaledUIAmountABI, provider);

        let rawAmount;
        if (isUIAmount && await this.supportsScaledUI(tokenAddress)) {
            rawAmount = await token.fromUIAmount(amount);
        } else {
            rawAmount = amount;
        }

        // Process deposit with raw amount
        return this.recordDeposit(tokenAddress, rawAmount);
    }

    async getDisplayBalance(tokenAddress, userAddress) {
        const token = new ethers.Contract(tokenAddress, ScaledUIAmountABI, provider);
        const rawBalance = await this.getInternalBalance(userAddress, tokenAddress);

        if (await this.supportsScaledUI(tokenAddress)) {
            return await token.toUIAmount(rawBalance);
        }
        return rawBalance;
    }
}

```

#### DEFI PROTOCOL INTEGRATION

DeFi protocols should:

1. Continue using raw amounts for all protocol operations
2. Provide UI helpers for displaying adjusted amounts
3. Emit events with both raw and UI amounts where relevant
4. Document clearly which amounts are used in calculations

## Copyright

Copyright and related rights waived via CC0.

## Replies

**gilbertS** (2025-12-09):

Love the work put into standardizing the UI and making a DeFi-compatible alternative for rebase tokens! I’d like to add a few suggestions to keep the interface minimal to accommodate a broader range of use cases.

- totalSupplyUI(): If we are having balanceOfUI, I think this function might be good to add to the standard as well.
- toUIAmount and fromUIAmount: I feel these conversion functions should likely be excluded from the standard or make them optional. This is due to:

Vulnerability to TOCTOU (Time-of-Check-to-Time-of-Use): A change in the UI multiplier between the frontend reading balanceOfUI and calling fromUIAmount to calculate the raw amount used in the transaction could lead to unexpected results.
- Context-Dependent Rounding: Different use cases may require different rounding methods for converting between raw and UI amounts. For example, for depositing tokens into a protocol, the formula amount_deposit = amount_deposit_ui * balance / balance_ui may be preferred to avoid leaving “dust” in the user’s wallet when depositing the maximum amount.

`UIMultiplierUpdated`: Standardizing this event may not be necessary, as some applications may have their UI multipliers update over time or not update at a preset moment. I got a chance to chat with some API providers, and they don’t think the event is required to support UI balance to offer a similar experience to the Solana tokens that use Scaled UI amount extension or the interesting bearing extension.

It may be useful (but probably optional) to emit an event during token transfer for the UI transferred amount, like `TransferWithUIAmount(from,to,amount,uiAmount)`

`setUIMultiplier`: This is an administrative function. I feel it’s better to not be included in the standard.

---

**cridmann** (2026-01-05):

[@gilbertS](/u/gilberts) - thanks for the thoughtful reply.

We support all of your requested changes. We feel the TOCTOU can be mitigated through other ways, but agree that making it optional makes sense.

I’ll go ahead and makes these changes to the proposed RFC in github.

---

**tinom9** (2026-01-06):

Hi [@cridmann](/u/cridmann), congrats on the ERC proposal, much needed for tokenized stocks!

---

### UIMultiplierUpdated Event

```sol
event UIMultiplierUpdated(uint256 oldMultiplier, uint256 newMultiplier, uint256 setAtTimestamp, uint256 effectiveAtTimestamp);
```

I would consider removing the `setAtTimestamp` parameter from the event, since it only conveys information for *when action was triggered* (`block.timestamp`), which can also be checked through the transaction receipt.

`oldMultiplier` could also be removed (available in previously emitted event), but it can be handy to have both at the same time. No strong opinion here.

---

### setUIMultiplier Function

```sol
function setUIMultiplier(uint256 newMultiplier, uint256 effectiveAtTimestamp) external
```

The proposed signature seems fine. A bit opinionated to force the timestamp parameter, but it can be solved by removing the “timestamp in the future” requirement.

I agree with [@gilbertS](/u/gilberts) that there’s an argument for leaving the administrative function (and possibly the event) out of the standard. If we can envision a single setter covering all administrative use-cases, I don’t see a problem leaving it in though.

---

### toUIAmount and fromUIAmount Helpers

Given that both `toUIAmount` and `fromUIAmount` always perform the same operations, and they should never vary from implementations, I’d argue these are not necessary within the standard and should be calculated through libraries:

- Querying uiMultiplier and computing the scaled result off-chain.
- Querying uiMultiplier and using a library to compute the scaled result on-chain.

Both methods are more efficient than their helper counterparts.

I’d consider removing them.

---

### balanceOfUI Function

If we’re having `balanceOfUI` into the standard, I’m aligned with [@gilbertS](/u/gilberts) and I think we should also have `totalSupplyUI`.

Nonetheless, I lean towards making the standard leaner and removing them altogether, as I cannot think of a case to use different rounding. You’d always want to round down.

---

Summarizing, the following interface seems completely fine for the standard and I believe achieves the same client-facing functionality (scaling amounts).

```sol
interface IScaledUIAmount {
    // Returns the current UI multiplier
    // Multiplier is represented with 18 decimals (1e18 = 1.0)
    function uiMultiplier() external view returns (uint256);
}
```

---

**pakim249CAL** (2026-01-09):

I also echo [@gilbertS](/u/gilberts) and believe the administrative function should be left out of the standard. I believe it should be enough to require that the relevant UIMultiplierUpdated is always emitted when the multiplier is changed.

I also agree with [@tinom9](/u/tinom9) that the balanceOfUI could be removed, or considered optional.

Overall, I would agree with [@tinom9](/u/tinom9) ‘s proposed interface, but in addition include the UIMultiplierUpdated event for consumption off-chain.

---

**cridmann** (2026-01-29):

Thanks for your thoughts [@tinom9](/u/tinom9) and [@pakim249CAL](/u/pakim249cal) .

I support removing `setAtTimestamp` from the `UIMultiplierUpdatedEvent` for the reasons cited - good call out. I would endorse leaving the event in the spec itself though, as serves an important function for off-chain indexers.

I’m fine with removing the `toUIAmount` and `fromUIAmount` helpers.

I would endorse with leaving `balanceOfUI` and `totalSupplyUI` in the spec, but am OK with it being optional.

---

**tinom9** (2026-01-30):

Thanks for the update [@cridmann](/u/cridmann)!

`UIMultiplierUpdated` event in the spec seems reasonable for indexers.

`balanceOfUI` and `totalSupplyUI` can be helpful in contracts that are not constrained by bytecode size. Therefore, having them as optional extensions to the base spec seems like a good idea, similarly to how ERC721 and ERC1155 handle optional interfaces.

On a separate topic, I believe the standard would be much more powerful if it didn’t require the scaled amounts to be only used in a UI.

Unfortunately, a lot of tokens currently implement rebasing or other esoteric mechanics to achieve stock splits, management fees, or updated exchange rates, and I tend to think that part of the reason is not having sufficiently standardized and simple methods that achieve the same behaviour: a share amount (the underlying raw amounts), and an asset amount (the scaled amounts), that UIs know how to represent, and that can be used as a source of truth for any business logic from the asset issuer (on-ramping, off-ramping, oracle price consumption, redemptions).

I would consider dropping the UI-specific requirement, renaming UI amounts to scaled amounts, and defining that implementers can use the multiplier as a non-purely cosmetic value. Amount representation in wallets and ERC20 operations will still have the same implications as they currently have.

I would also consider explicitly implementing the ERC165 interface, since the provided JavaScript examples seem to use it.

---

**gilbertS** (2026-02-04):

Hi [@tinom9](/u/tinom9),

Thank you for your valuable input! I also think it makes sense to exclude setAtTimestamp from the event, as this information can usually be obtained from the block timestamp when indexing the event.

Regarding the UI naming discussion, I suggest keeping the current naming. Business logic can differ from token to token and sometimes cannot be captured by a single multiplier. I think it would be best to keep it as a minimal standard, yet one that is complete enough for API providers, Oracle providers, and wallet developers to support.

For token-dependent logic, I think one can compose it with existing or future standards—for example, ERC-4626—when the underlying asset is also another ERC-20 token. Additionally, I think the UI naming echoes Solana’s “UI amount” concept used in the Scaled UI Amount and Interest-Bearing extensions.

