---
source: magicians
topic_id: 5077
title: "ERC-3156: Flash Loans"
author: albertocuestacanada
date: "2020-12-30"
category: ERCs
tags: [defi]
url: https://ethereum-magicians.org/t/erc-3156-flash-loans/5077
views: 6355
likes: 12
posts_count: 22
---

# ERC-3156: Flash Loans

The [ERC-3156](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-3156.md) standard for flash loans is moving to the `Review` stage.

This topic is for discussion of the standard. Please check the EIP, as well as the [ERC3156](https://github.com/albertocuestacanada/ERC3156) repository with ERC-3156 wrappers for popular lenders such as Aave, dYdX, Uniswap and Yield.

The reference implementations and the lender wrappers have all been deployed to Kovan. Feel free as well to kick the tires using the FlashBorrower at 0xeeb0c120bF35fB0793b1c7d0D93230e552020398 contract which has a `flashBorrow` function to initiate flash loans on any ERC-3156 contract, and the necessary callback for at least paying the loan fees and successfully finalizing the loan.

## Replies

**albertocuestacanada** (2021-01-01):

Replying to [MicahZoltu](https://ethereum-magicians.org/t/flash-loan-eip-erc-3156-early-draft/4993/6), which was very kind to review the standard.

> Why does the receiver have to be the same person that gets the callback? What if you want to loan ETH to address X but callback to address Y?

1. Because it is what every implementation of flash loans has independently chosen so far, and adopting the pattern will make the standard easier to understand and adopt.
2. Because the loan will need to be actively returned (presumably by X), so Y would need to callback X or Y would need to transferFrom from X to the lender.

If you want to loan to X and callback to Y, you can just have Y transfer the loan to X. It seems to me that adding an `address callback` parameter to `flashLoan` would add additional complexity and be ignored most of the time.

> Why not allow the caller to decide the callback and provide all of the parameters? They already can query for fee, and the amount being loaned is known to the caller in advance of the call. So you could just do receiver.call(_calldata) which would allow the caller to also decide what method was called.

1. Because specific callback functions are what all flash lenders have independently implemented, which leads us to believe that the standard will be more easily adopted if we follow the pattern.
2. Using onFlashLoan(address sender, ...) allows the flash lender to certify who was the caller of flashLoan, which in turn allows to establish a chain of trust. Using receiver.call(_calldata) trusting the flash lender is not enough to trust that any of _calldata is genuine. We expect that sender would often be the address of an affected account on the receiver.

---

**MicahZoltu** (2021-01-03):

I recommend adding these to the Rationale section.

I don’t think “because it is what other implementations have done” is a good reason though, you should instead find out *why* they did it that way and evaluate if their reasons are good/sound.  Many people do things because it was the first idea that popped into their head, or because the person before them did it that way, or because for their very specific situation it was the optimal solution but that doesn’t translate to other situations.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/albertocuestacanada/48/3057_2.png) albertocuestacanada:

> Because the loan will need to be actively returned (presumably by X), so Y would need to callback X or Y would need to transferFrom from X to the lender.

This seems to be presuming how people will be using the loan platform, which I think is not a good idea.  I would rather see this be designed to be “as compatible with whatever future patterns people come up with” as possible so we don’t have to have yet-another-standard a few years from now when some new pattern becomes commonplace.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/albertocuestacanada/48/3057_2.png) albertocuestacanada:

> Using onFlashLoan(address sender, ...) allows the flash lender to certify who was the caller of flashLoan, which in turn allows to establish a chain of trust. Using receiver.call(_calldata) trusting the flash lender is not enough to trust that any of _calldata is genuine. We expect that sender would often be the address of an affected account on the receiver.

I like this reasoning.  It means that someone can call into a contract via a flash loan (of their choosing as long as it implements this contract).  I can’t think of any uses for this feature at the moment, but as I mentioned above I’m a fan of allowing unforeseen patterns in the future.

---

**albertocuestacanada** (2021-01-06):

Thanks for bringing the questions up, I’m definitely adding all this to the Rationale section.

An use case where the funds receiver and the execution control receiver are different is if I would want to flash borrow from one lender and swap the loan for a different token using Uniswap:

1. Call AaveERC3156.flashLoan(myContract, uniswapPair, dai, 1 ether, data)
2. UniswapPair receives 1 Dai
3. myContract.onFlashLoan(sender, uniswapPair, dai, 1 ether, fee, data) gets executed, which calls uniswapPair.swap
4. … some more things happen …
5. Someone transfers 1 Dai + fee to AaveERC3156

Note the example is for existing Uniswap contracts, but any implementations where users push tokens to contracts, instead of contracts pulling tokens from users, will also apply here.

The current ERC3156 implementation could implement the same functionality with this flow:

1. Call AaveERC3156.flashLoan(myContract, dai, 1 ether, data{uniswapPair})
2. myContract receives 1 Dai
3. myContract.onFlashLoan(sender, token, value, fee, data{uniswapPair}) gets executed, which calls dai.transfer and uniswapPair.swap
4. … some more things happen …
5. Someone transfers 1 Dai + fee to AaveERC3156

Allowing the receiver of the funds and the receiver of the execution control to be different allows, in some cases, to remove one `transfer` from the transaction. In exchange it requires an extra parameter in both `flashLoan` and `onFlashLoan`.

I have the feeling that in most cases `receiver` and `executor` would be the same contract, so I’m not too keen extra parameters that would be ignored most of the time and that at best would save some gas, without enabling any new capabilities. I’m not too opposed, either.

If you think it’s worth it, I can ask [@fifikobayashi](/u/fifikobayashi), @hexonaut and the rest of the people that have been involved for their input on this. Maybe they can think of a use case where this would be really useful.

---

**albertocuestacanada** (2021-01-06):

[@MicahZoltu](/u/micahzoltu), I’ve extended the ERC with a new paragraph on the trust levels for the arguments of `onFlashLoan`, as well as a guideline on how to make sure they are genuine. I can’t post links today, sorry.

The goal is for users to be certain on what the arguments represent, and what they need to do if they are going to use them.

I think that you should also be aware of how flash loans are used to refinance debt. DefiSaver has an example that you will find interesting. I would post the link but the forum software is stupid and doesn’t let me. Google LoanShifterTaker.sol, line 103.

I believe that refinancing implementations will be commonplace in the near future. Refinancing is also a more complex use case of flash loans than arbitraging, since it involves manipulating the accounts of different users in different platforms. In refinancing implementations, packing arguments into `data` is often required, and the contents of the `data` argument must therefore be completely trusted.

---

**Amxx** (2021-01-07):

Small remark about the flash mint reference implementation, I think you should reflect the flashSupply function to consider the totalSupply limit. Also, not all tokens are available, so I’d rewrite as:

```auto
function flashSupply(address token) external view override returns (uint256) {
    return token == address(this) ? type(uint256).max - totalSupply() : 0;
}
```

---

**albertocuestacanada** (2021-01-07):

Thanks [@amxx](/u/amxx)! Fixed now.

---

**albertocuestacanada** (2021-01-07):

The reference implementations included inline can also be found at my ERC3156 repository

Of note are the ERC-3156 wrappers for existing flash lenders, also to be found at my ERC3156 repository.

Other implementations include WETH10 and MakerDAO MIP-25.

---

**BoringCrypto** (2021-01-10):

Currently implementing flash loans for BentoBox (part of Sushi) and trying to adhere to this draft. A few comments:

Renamed FlashBorrowerLike to IFlashBorrowerLike to indicate it’s an interface

We want to support loaning multiple assets in a single call. So IFlashBorrowerLike looks like this:

```
interface IFlashBorrowerLike {
	function onFlashLoan(address sender, address[] calldata tokens, uint256[] calldata amounts, uint256[] calldata fees, bytes calldata) external;
}
```

Currently the assets get delivered to the receiver. This is not always ideal. If you want to swap them first, you may want them delivered directly to a SushiSwap pair contract. So including a `loaner` and a `receiver` provides the flexibility for this and saves on gas.

We have this so far:

```
function  flashLoan(address loaner, address[] calldata tokens, uint256[] calldata amounts, address[] calldata receivers, bytes  calldata data) public {
	...
	IFlashBorrowerLike(loaner).onFlashLoan(msg.sender, tokens, amounts, fees, data);
```

Also found this:

`function flashSupply(address token) external external returns (uint256);` has external twice. Should this be marked as view? Same goes for flashFee.

---

**albertocuestacanada** (2021-01-13):

Thanks a lot for your feedback, [@BoringCrypto](/u/boringcrypto). After some enquiries, I think that batch flash loans are a feature that although it might not be the most common use case, they are relevant enough to have a place in the standard.

I think that the most common receiver implementations will use a single asset, and all flash mints will lend only one asset as well. I don’t want to force them to implement batch flash loans as that would mean a lot of clutter in their code.

I think that the best solution is to include a batch flash loan extension to ERC3156. It works as the single asset one but uses arrays for tokens, amounts and fees. The caveat, though, is that to be ERC3156 compliant if you implement batch flash loans you must also implement the single asset interface.

```auto
interface IERC3156BatchFlashLender is IERC3156FlashLender {
    function batchFlashLoan(
        address receiver,
        address[] tokens,
        uint256[] amounts,
        bytes calldata data
    ) external;
}

interface IERC3156BatchFlashBorrower is IERC3156FlashBorrower {
    function onBatchFlashLoan(
        address sender,
        address[] calldata tokens,
        uint256[] calldata amounts,
        uint256[] calldata fees,
        bytes calldata data
    ) external;
}
```

Please have a look at the updated EIP (PR3181) and let me know your thoughts.

---

**BoringCrypto** (2021-01-15):

Great, I’ll rename it accordingly… took a closer look at the fineprint today, some more feedback:

“If the loan cannot be executed `flashFee` MUST revert.” - Since we’re already exposing flashSupply, is this really needed? I understand this this would be nice, but maybe change this to SHOULD so if we don’t, we’re still compliant? Flashloans aren’t the MAIN feature of the contract, and code space is limited and less code = more room for optimizations.

Keep in mind that is these functions are called as view functions, their values may no longer be valid by the time a transaction uses them and if they are called from another contract, you would wish to minimize gas usage, so this check is not relevant (as you’ve most likely already retrieved totalSupply), but just adds gas.

How will you know that the optional batchFlashLoan is implemented from another contract?

“The `batchFlashLoan` function MUST revert if the length of the `amounts` and `tokens` arrays differ.” - I know these kind of checks are commonly used by Solidity devs, but unless there is a security risk or a missed param can cause loss of funds (such as transfer to address(0)), why include this? I don’t see any harm here. Using address(0) as token will fail, and 0 as amount will just loan nothing. I chose to simply assume the tokens length is correct, if there are more amounts, they will be ignored, if there are less, I’ll have to check what happens… not sure if solidity does bounds checking.

“The `batchFlashLoan` function MUST include a `fees` argument to `onBatchFlashLoan` with the fee to pay for each individual `token` and `amount` lent.” - may want to mention that the order should be the same. I don’t care, but just for completeness.

In Rationale, is this out of date? " `flashFee` reverts on unsupported tokens, because returning a numerical value would be incorrect."

And that brings us to the big dilemma: PULL or PUSH the returned funds…

PULL

Upsides:

- You can rely directly on token.balanceOf(address(this)) in the lender for logic.

Downsides:

- The receiver must approve the tokens. If the receiver also approves tokens for another reason to the lender, some tokens will cause issues as the approve has to be changed to 0 before it can be set again.
- If users approve to the lender to interact with other functionality on that contract, users are at risk of a grieving attack stealing fees that could drain their entire balance. All the ways I can think of to mitigate this will add contracts/gas.

PUSH

Upsides:

- More flexibility to optimize and reduce number of transfers needed.
- No need to approve. No risk of grieving.

Downsides:

- You have to keep track of the token balance expected in the contract. Some contracts do this already, such as UniSwap V2 (reserves), while other, such as cTokens? do not.
- Care must be taken that there are no reentrancy issues
- Care must be taken that a batch with the same token twice doesn’t cause issues.

Neither is perfect, but since we already track the balances in the contract, we are going with PUSH. Once we confirm that our code is secure, there are only upsides left for the user of the flashLoans (lower gas and more flexible). Initially we had pull, but the grieving attack issue made us switch. Happy to reconsider if someone can suggest a good solution to the grieving problem.

Anyway, great work on this EIP… not an easy one ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

---

**MicahZoltu** (2021-01-15):

Moving discussion from [Erc3156 review by alcueca · Pull Request #3203 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/3203#issuecomment-760925909) to here as this is a more appropriate venue:

> Consider adding support for flash lending ETH by making token == SENTINEL mean ETH in all functions.

> I don’t see an issue reserving address(1) as a sentinel for ETH in this context, but how would you go about it?
>
>
> I don’t think I can add it to the interfaces, and adding it to the reference implementation would complicate things, apart from being just a suggestion.
>
>
> Should it be just be an statement (“If Ether is supported address(1) MUST be used to denote it”)?

---

I think a statement like you have would work great:

> For all functions above, address(1) is used as a sentinel value for Ether.  If the token parameter is address(1) then the function should be processed as defined except using Ether instead of a token.

Maybe another similar statement for the borrower interface.

---

**albertocuestacanada** (2021-01-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boringcrypto/48/3164_2.png) BoringCrypto:

> “If the loan cannot be executed flashFee MUST revert.” - Since we’re already exposing flashSupply, is this really needed? I understand this this would be nice, but maybe change this to SHOULD so if we don’t, we’re still compliant? Flashloans aren’t the MAIN feature of the contract, and code space is limited and less code = more room for optimizations.
>
>
> Keep in mind that is these functions are called as view functions, their values may no longer be valid by the time a transaction uses them and if they are called from another contract, you would wish to minimize gas usage, so this check is not relevant (as you’ve most likely already retrieved totalSupply), but just adds gas.
>
>
> …
>
>
> In Rationale, is this out of date? " flashFee reverts on unsupported tokens, because returning a numerical value would be incorrect."

I should change the statement to “If the token is not supported `flashFee` MUST revert.”

`flashFee` is there only to tell you what the fee would be, not whether the loan will succeed. It can’t return 0 if the token is not supported, because that would be false. Returning MAX would also be false. So reverting seems to be the only option.

Some users will use the `flashFee` function prior to executing the flash loan to check whether they can afford it, or even to compare between different providers.

---

**albertocuestacanada** (2021-01-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boringcrypto/48/3164_2.png) BoringCrypto:

> How will you know that the optional batchFlashLoan is implemented from another contract?

I would suggest lenders implement ERC165 if they want their services to be discoverable, but wouldn’t go as far as mandating it.

---

**albertocuestacanada** (2021-01-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boringcrypto/48/3164_2.png) BoringCrypto:

> “The batchFlashLoan function MUST revert if the length of the amounts and tokens arrays differ.” - I know these kind of checks are commonly used by Solidity devs, but unless there is a security risk or a missed param can cause loss of funds (such as transfer to address(0)), why include this? I don’t see any harm here. Using address(0) as token will fail, and 0 as amount will just loan nothing. I chose to simply assume the tokens length is correct, if there are more amounts, they will be ignored, if there are less, I’ll have to check what happens… not sure if solidity does bounds checking.

Agree, we are overreaching here, I’ll remove it.

---

**albertocuestacanada** (2021-01-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boringcrypto/48/3164_2.png) BoringCrypto:

> “The batchFlashLoan function MUST include a fees argument to onBatchFlashLoan with the fee to pay for each individual token and amount lent.” - may want to mention that the order should be the same. I don’t care, but just for completeness.

I like completeness, fixed.

---

**poojaranjan** (2021-01-20):

EIP-3156: Flash Loans with Alberto Cuesta Cañada - https://youtu.be/R9wQ1FoV6HU

---

**albertocuestacanada** (2021-02-07):

[@BoringCrypto](/u/boringcrypto) raised the point that there are no events in the specification.

While all state changes are covered by the underlying `Transfer` events, it will be quite difficult for any analytics setup to extract the flash loans out of those generic events, and emitting one `FlashLoan` event would make things quite easier.

My take is that this event should not be compulsory, but that if present it should follow a consistent format between ERC3156 implementations.

---

**albertocuestacanada** (2021-02-12):

After a discussion with [@MicahZoltu](/u/micahzoltu) we agreed that while having a standard event for flash loans would be useful, having optional elements in an ERC leads to confusion. Therefore such an event would be best defined in its own (very short) EIP.

---

**mass59** (2021-03-26):

receiver.call(_calldata)

---

**PaulRBerg** (2023-01-12):

Hey [@albertocuestacanada](/u/albertocuestacanada), great work with EIP-3156.

I was reading the standard, and I stopped at the “Flash lending security considerations” section. I wonder why does it mention an EOA in this context?

> If an unsuspecting contract with a non-reverting fallback function, or an EOA, would approve a lender implementing ERC3156, and not immediately use the approval …

It is true that the EVM does not revert on calls made to EOAs, but high-level Solidity does. In particular, your reference implementation [FlashLender.sol](https://github.com/alcueca/ERC3156/blob/b4521a4e33199846c24a9ba0fea2b0a36a21860b/contracts/reference/FlashLender.sol#L57) does:

```solidity
receiver.onFlashLoan(msg.sender, token, amount, _fee, data) == CALLBACK_SUCCESS,
```

Where `receiver` is a function param of type `IERC3156FlashBorrower`.

Therefore, the approval vulnerability only applies to an EOA if the lender contracts uses a vanilla `address` type, and performs a low-level call to `receiver`. But this should not be the case in the vast majority of EIP-3156 implementations.

Do you think that it would be worth it to add a note about this in the standard?


*(1 more replies not shown)*
