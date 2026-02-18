---
source: magicians
topic_id: 17777
title: Interest Rate Swaps
author: samsay
date: "2023-12-31"
category: ERCs
tags: [erc, defi]
url: https://ethereum-magicians.org/t/interest-rate-swaps/17777
views: 2204
likes: 6
posts_count: 14
---

# Interest Rate Swaps

This standard introduces a standardized framework for on-chain interest rate swaps. The proposed standard facilitates the seamless exchange of fixed and floating interest rate cash flows between parties, providing a robust foundation for decentralized finance (DeFi) applications.

https://github.com/ethereum/ERCs/pull/178

```solidity
pragma solidity ^0.8.0;

/**
* @title ERC-7586 Interest Rate Swaps
*/
interface IERC7586 {
    // events
    /**
    * @notice MUST be emitted when interest rates are swapped
    * @param _amount the interest difference to be transferred
    * @param _account the recipient account to send the interest difference to. MUST be either the `payer` or the `receiver`
    */
    event Swap(uint256 _amount, address _account);

    /**
    * @notice MUST be emitted when the swap contract is terminated
    * @param _payer the swap payer
    * @param _receiver the swap receiver
    */
    event TerminateSwap(address indexed _payer, address indexed _receiver);

    // functions
    /**
    *  @notice Returns the IRS payer account address. The party who aggreed to pay fixed interest
    */
    function payer() external view returns(address);

    /**
    *  @notice Returns the IRS receiver account address. The party who aggreed to pay floating interest
    */
    function receiver() external view returns(address);

    /**
    *  @notice Returns the fixed interest rate. It is RECOMMENDED to express the swap rate in basis point unit
    *          1 basis point = 0.01% = 0.0001
    *          ex: if interest rate = 2.5%, then swapRate() => 250 basis points
    */
    function swapRate() external view returns(uint256);

    /**
    *  @notice Returns the floating rate spread, i.e. the fixed part of the floating interest rate. It is RECOMMENDED to express the spread in basis point unit
    *          1 basis point = 0.01% = 0.0001
    *          ex: if spread = 0.5%, then floatingRateSpread() => 50 basis points
    *
    *          floatingRate = benchmark + spread
    */
    function spread() external view returns(uint256);

    /**
    * @notice Returns the contract address of the asset to be transferred when swapping IRS. Depending on what the two parties aggreed upon, this could be a currency, etc.
    *         Example: If the two parties agreed to swap interest rates in USDC, then this function should return the USDC contract address.
    *                  This address SHOULD be used in the `swap` function to transfer the interest difference to either the `payer` or the `receiver`. Example: IERC(assetContract).transfer
    */
    function assetContract() external view returns(address);

    /**
    *  @notice Returns the notional amount in unit of asset to be transferred when swapping IRS. This amount serves as the basis for calculating the interest payments, and may not be exchanged
    *          Example: If the two parties aggreed to swap interest rates in USDC, then the notional amount may be equal to 1,000,000 USDC, etc
    */
    function notionalAmount() external view returns(uint256);

    /**
    *  @notice Returns the interest payment frequency
    */
    function paymentFrequency() external view returns(uint256);

    /**
    *  @notice Returns an array of specific dates on which the interest payments are exchanged. Each date MUST be a Unix timestamp like the one returned by block.timestamp
    *          The length of the array returned by this function MUST equal the total number of swaps that should be realized
    *
    *  OPTIONAL
    */
    function paymentDates() external view returns(uint256[] memory);

    /**
    *  @notice Returns the starting date of the swap contract. This is a Unix Timestamp like the one returned by block.timestamp
    */
    function startingDate() external view returns(uint256);

    /**
    *  @notice Returns the maturity date of the swap contract. This is a Unix Timestamp like the one returned by block.timestamp
    */
    function maturityDate() external view returns(uint256);

    /**
    *  @notice Returns the benchmark in basis point unit
    *          Example: value of one the following rates: CF BIRC, EURIBOR, HIBOR, SHIBOR, SOFR, SONIA, TONA, etc.
    */
    function benchmark() external view returns(uint256);

    /**
    *  @notice Returns the oracle contract address for the benchmark rate.
    *          This contract SHOULD be used to fetch real time benchmark rate
    *          Example: Contract address for `CF BIRC`
    *
    *  OPTIONAL. The two parties MAY agree to set the benchmark manually
    */
    function oracleContractForBenchmark() external view returns(address);

    /**
    * @notice Returns true if the swap is active (not matured or not terminated), false otherwise
    */
    function isActive() external view returns(bool);

    /**
    * @notice Gives agreement to swap IRS. After the contract deployment and prior to the initiation of the first payment, it is imperative for both the `payer` and the `receiver` to invoke this function as an expression of their agreement
    */
    function agree() external;

    /**
    *  @notice Makes swap calculation and transfers the interest difference to either the `payer` or the `receiver`
    */
    function swap() external returns(bool);

    /**
    *  @notice Terminates the swap contract before its maturity date. It is RECOMMENDED to integrate a multisig process to terminate the swap contract.
    *          Both the payer and the receiver MUST sign for the termination to be successful
    */
    function terminateSwap() external;
}
```

## Replies

**wjmelements** (2024-01-02):

This seems to require a new contract for each swap. Are interest rate swaps never fungible? Is it impossible or undesirable to subdivide a position?

If it is non-fungible it can inherit the nonfungible token standard ERC721. Otherwise it can inherit ERC20.

Either way I suspect there is a gas advantage to having multiple swap agreements tracked per deployment.

---

**samsay** (2024-01-02):

Hello [@wjmelements](/u/wjmelements),

The same contract is used for all the cashflows agreed upon by the two parties. If each IRS cashflow is seen as a token, then it should be non fungible, since the floating rate depends on a benchmark rate which fluctuates. It should then inherit the ERC721 standard. However, since for an IRS swap the token just represents a cash flow and not the interest rate to be exchanged, then it can be a fungible token, and the ERC7586 can inherit the ERC20 standard.

So if we consider the case 4 IRS swaps must be realized during the contract lifetime, then one can issue 4 fungible tokens (ERC20), one for each swap. Each time a swap is realized, 1 token is burned.

Encoding multiple swap agreements per contract deployed has some advantages, however, an IRS swap is a derivative contract between two parties, with terms and conditions defined therein. Allowing the same contract to track multiple swap agreements means having different terms and conditions, and different IRS swap participants per contract. This can lead to legal and technical issues.

---

**samsay** (2024-01-03):

Hello [@wjmelements](/u/wjmelements),

Here is the tokenization process for the proposed IRS standard

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/8/8a1cab3cd62471d01346e3ab24e6a273b425d13a_2_690x174.png)image2056×520 85.3 KB](https://ethereum-magicians.org/uploads/default/8a1cab3cd62471d01346e3ab24e6a273b425d13a)

---

**samsay** (2024-01-28):

The notional tokenization is not necessary since the notional amount is not exchanged. Therefore, only the `Swap Cash Flows` are tokenized buy issuing ERC-20` tokens to both, the buyer and the payer. And each time a swap happens, one token is burned from the two counterparties wallet.

---

**SamWilsn** (2024-03-05):

Bit of bikeshedding on the name of functions:

- If payer always agrees to pay fixed interest, it might be more clear to developers if the name included “fixed” in some way?
- Similarly, if receiver always pays floating interest, maybe including “floating” in the function would be nice.

This is just a suggestion coming from a software developer; feel free to ignore if you like.

---

**SamWilsn** (2024-03-05):

On `swapRate` and `spread`, how do you indicate the fixed point representation? You recommend “basis points”, but don’t make it mandatory. If a contract needs those numbers to perform a calculate, it needs to be able to convert between different representations.

[ERC-20](https://eips.ethereum.org/EIPS/eip-20) has `decimals` for that purpose, for example.

---

**SamWilsn** (2024-03-05):

You might want to mention [ERC-165](https://eips.ethereum.org/EIPS/eip-165) somewhere. It’s useful for third parties to identify what a particular contract supports.

---

**BorisB** (2024-03-07):

Hi samsay

Why do we need to tokenize the notional amount? the notional amount should never be transferd

---

**samsay** (2024-03-08):

Hello [@BorisB](/u/borisb),

You’re right, we don’t need to tokenize the notional amount. This has been removed in the EIP. Only the Swap Cash Flows is tokenized in the new version.

---

**samsay** (2024-03-08):

Hello [@SamWilsn](/u/samwilsn),

This is how fixed and floating interest payers are named. Of course, I could make these functions more clear for developers by using `fixed` and `floating` in their name.

---

**samsay** (2024-03-08):

`swapRate` and `spread` are both percentage, and are usually expressed in basis points unit that I explained what it is in the Interface. The use of `basis points` to express these rates is just a `RECOMMENDATION` since this is widely used in Capital Market. Therefore, other units can be used such as the ERC-20 `decimals` (1E-18).

For calculation:  1 basis point = 0.01% = 0.0001

This is also explained in the standard

---

**SamWilsn** (2024-03-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samsay/48/6130_2.png) samsay:

> The use of basis points to express these rates is just a RECOMMENDATION since this is widely used in Capital Market. Therefore, other units can be used such as the ERC-20 decimals (1E-18).

That makes sense, but I didn’t see a function that returned the representation the particular contract is using. I’d expect to see something like `swapRateDecimals()`?

---

**samsay** (2024-03-09):

Ohh sorry, I haven’t added it. Going to do that right now.

Thank you

