---
source: magicians
topic_id: 23972
title: "ERC-7943: Universal RWA Interface (uRWA)"
author: xaler
date: "2025-05-01"
category: ERCs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-7943-universal-rwa-interface-urwa/23972
views: 3362
likes: 113
posts_count: 104
---

# ERC-7943: Universal RWA Interface (uRWA)

[github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/1029)














####


      `master` ← `xaler5:add-draft-urwa`




          opened 07:18AM - 01 May 25 UTC



          [![](https://avatars.githubusercontent.com/u/20795374?v=4)
            xaler5](https://github.com/xaler5)



          [+495
            -0](https://github.com/ethereum/ERCs/pull/1029/files)







This EIP defines a minimal and implementation-agnostic interface for Real World […](https://github.com/ethereum/ERCs/pull/1029)Assets (RWAs), intended to unify compliance-related functionality across ERC-20, ERC-721, and ERC-1155 tokens. The interface introduces core primitives (`forceTransfer`, `setFrozen`, `getFrozen`, `isUserAllowed` and `isTransferAllowed`) that support regulated token use cases, such as enforcement actions and transfer restrictions, without prescribing how those policies are implemented.

The standard deliberately omits non-essential and opinionated features such as role-based access control, metadata handling, pausing, or on-chain identity mechanisms. These are left to implementers to integrate as needed, enabling maximum flexibility and reducing surface area for unnecessary gas costs or over-specification. This promotes composability and ease of integration across DeFi and institutional applications without compromising base token behavior.

Author: @xaler5
Discussion: https://ethereum-magicians.org/t/erc-universal-rwa-interface/23972












**Update 07/2025**: This EIP is now in *Review* stage and active feedback and contributions are welcomed. There are active discussions about naming conventions, pausability and metadata handling features, and overall errors / events definitions.

---

This proposal introduces a minimal, standardized interface for Real World Asset (RWA) tokenization that is designed to be maximally compatible across existing token standards such as ERC-20, ERC-721, and ERC-1155. It focuses on providing only the essential compliance and enforcement functions common to regulated assets, without imposing specific implementation patterns or additional optional features.

Non-essential capabilities like pausing, metadata handling, or identity integrations are intentionally excluded from the standard, as they tend to be opinionated and vary greatly depending on the specific RWA use case. This approach ensures broad interoperability and minimal friction for adoption while allowing developers to extend functionality as needed within their own contracts.

## Replies

**xaler** (2025-05-01):

A very basic reference implementation can be found at



      [github.com](https://github.com/xaler5/uRWA)




  ![image](https://opengraph.githubassets.com/398b349ef92b43adb35609897b250780/xaler5/uRWA)



###



Contribute to xaler5/uRWA development by creating an account on GitHub.

---

**xaler** (2025-05-02):

Thanks for the comment [@magicians](/u/magicians)

I fully agree that RWA is a too broad spectrum.

A key challenge is that each type of RWA possesses unique characteristics that necessitate specific on-chain capabilities for proper representation. Consider tokenized shares: they require features like dividend distribution, which implies a need for the token contract to track historical balances. Additionally, shares are often non-fractional, a property not natively supported by a pure ERC-20 without custom additions. Carbon credits, by contrast, have different needs, such as robust metadata handling to accurately reflect emissions data and manage redemption. Varying regulatory requirements further differentiate what’s needed for compliance across different asset classes.

This analysis of diverse asset requirements, coupled with a review of current RWA tokenization standards, strongly suggested me that a monolithic approach is unsuitable. Instead, a modular and flexible architecture is paramount – one that identifies and focuses on the minimal common base layer required by all RWAs, allowing specific features and compliance modules to be built flexibly on top.

Curious to know your thoughts on the specific of the proposed interface

---

**tinom9** (2025-05-02):

First of all, great job on the proposal, it adds great value to make it token-agnostic.

I think it’s difficult to select which permissioning features to include and which to intentionally exclude from the standard.

If we’re aiming for a truly minimal implementation, one could argue that some parts can be omitted, as it could be reduced to a transfer-check standard. Similar to ERC-902 and ERC-1462.

1. Exclude recall, and achieve the functionality through mint and burn. Specificity and simplicity are lost.
2. Exclude isUserAllowed; the same functionality is achieved with isTransferAllowed. Error-handling specificity is lost.

I then believe there are two possible paths for this standard:

1. Universal token transfer check, non-opinionated on the admin or functionality standpoint. Additional ERCs can be built on top to standardize whitelisting, pausing/unpausing, access-control, or other compliance mechanisms.
2. Universal RWA token, with core token functionality embedded: forceTransfer/recall, freezeTokens, frozenBalance. Compliance functionality should be built on top, similarly to the previous option.

I believe a security/RWA/permissioned token standard should be opinionated on the core token functionality.

I propose the following changes:

1. Add mint and burn methods to the interface. Specify that isUserAllowed(to) must be run on mint, and that isUserAllowed(from) must not be run on burn—T-REX-like.
2. Specify that isUserAllowed(to) must be run on recall and that isUserAllowed(from) must not be run on recall.
3. Add freezeTokens, unfreezeTokens, and frozenBalance methods, plus TokensFrozen and TokensUnfrozen events. In my experience, token freezing is always required by regulators. It can be implemented as a separate module, but if we assume isUserAllowed provides the necessary specificity, token freezing should be required too. burn and recall should unfreeze tokens as needed.
4. Prepend errors with an ERCX prefix, similar to ERC-6093.
5. Rename recall to forceTransfer, and Recalled to ForcedTransfer. Recalled has a meaning of returning or withdrawing; I would stick to the core action and call it a forced transfer, regardless of the underlying reason it’s used. This is obviously a nit.

---

**xaler** (2025-05-02):

Thanks a lot [@tinom9](/u/tinom9) for your comments ! Those are extremely valuable.

I think out of the two options we’re converging on the idea of an **Universal RWA token** standard that includes key token-level functionalities but that is also maximally compatible and easy to integrate. Here are my responses to your suggestions and a few clarifying questions to continue the conversation:

---

### Mint and Burn

Your proposal to include `mint` and `burn` functions makes sense in most cases to me, especially in asset classes like equity or tokenized commodities. However, some RWA implementations, such as fixed-supply debt instrument, require immutable supply characteristics. In these cases, `mint` and `burn` may not be applicable at all, or maybe only one of the two.

Would you consider making `mint` and `burn` a **`SHOULD`** requirement in the EIP? This would maintain flexibility for fixed-supply cases while still encouraging standardization for the majority of use cases. Also, specifying that `isUserAllowed(to)` applies to `mint` and `isUserAllowed(from)` is exempt for `burn` makes sense, will integrate this into the description.

---

### Error Prefixes (ERCX)

I really liked your suggestion. I’ll go ahead and include it.

---

### recall/forceTransfer Naming

I completely agree with renaming `recall` to `forceTransfer`. Other terms like *confiscation*, *revocation*, or *recovery* describe **reasons**, not the underlying action, which is indeed a forced movement of assets. But let’s consider also the next topic for the naming part.

---

### Freeze Functionality

I’m on board with supporting freezing functionality, especially since regulatory requirements often mandate it. However, I’d like to clarify the **functional distinction** between `freezeTokens` and `forceTransfer`.

Would you say the difference is that:

- freezeTokens keeps tokens in the wallet but locks them;
- forceTransfer moves the tokens elsewhere?

If so, would it be reasonable to combine both functionalities into a single `forceTransfer`-like method using a **flag** (e.g., `to` address being same as from meaning a freeze or an extra parameter to differentiate between a freeze and a forcedTransfer) ?

(at this point I’d call this function more something like “enforce” with no distinction whether is a forced transfer or a freeze).

Alternatively, do you think **both freezing and forced movement** are fundamentally distinct actions that regulators would want *both* to be present ? Is it one of the two more primitive than the other ?

Would love your thoughts on whether combining them makes sense or if we should define them separately.

---

Thanks again for the constructive discussion!

---

**tinom9** (2025-05-02):

### burn

I don’t see a use case where the `burn` method wouldn’t be necessary for a security or RWA. Pessimistically, every asset should be liquidable at some point, and I only see that happening via the `burn` method.

For me, if included, it should be a `MUST` .

---

### mint

Tokens must be minted at some stage. I think there’s a slight trade-off between minting flexibility (ERC20‑style) and standardization (a defined interface).

For me, if included, it should be a `MUST` , with a `MAY` revert for custom logic (e.g., when the max supply is reached).

---

### freezeTokens / forceTransfer

I think `forceTransfer` main serves for court‑ordered or regulatory transfers—inheritances, seizures, etc.—so there’s almost always a recipient for the assets. It can also serve as a general administrative transfer function, and I don’t see any reason to discourage that use.

On the other hand, I see the `freezeTokens` method used to immobilize assets, during bankruptcy or insolvency proceedings, temporary protective orders, partial claims, etc., with the intention of either unfreezing or forcefully transferring them later.

I believe the debate isn’t so much about merging these functionalities as it is about whether freezing tokens is core enough to be part of the ERC interface. It could be implemented via transfer restrictions—tracking frozen balances in parallel and returning `isTransferAllowed = false` if the transfer exceeds the unfrozen balance.

I’d prefer built‑in freezing functionality in the standard, as I’ve found regulators in Europe consistently requiring it. However, I could also see the case for a separate freezing module, maybe a different ERC, if making this one leaner is a priority.

---

Great job, again!

---

**xaler** (2025-05-05):

Thanks [@tinom9](/u/tinom9) for the follow up !

I’ve done the following changes:

- Changed errors names to adapt to ERC-6093.
- Renamed recall to forceTransfer and Recalled to ForcedTransfer.
- Addressed your feedback on the implementations and examples.

I’ve also adjusted the statements in what integrators should do for transfers,minting and burning. However I still didn’t include the `mint` and `burn` functions for the arguments below.

Been thinking about it for the last two days and slightly discussed this also with [@frangio](/u/frangio) and here some argument that I think still holds for not including those functions within this standard:

- Minting works differently for ERC-20 vs ERC-721/ERC-1155 in the sense that the former doesn’t perform checks on the recipient while the latter usually do.
- Given the different needed parameters (ie amounts and/or tokenIds), building up a standard function interface for all three kind of tokens might sound as redefining how a minting function should look like for an ERC-20 or an ERC-721.
- As previously mentioned, fixed-supply debt might represent an use case where an external or public minting function is not needed, and the supply is determined at constructor time. Additionally, liquidating an RWA doesn’t necessarily imply burning them, as secondary market can make them tradeable against stables or other RWAs. Additionally burning might even be prohibited and not necessary for a use case (ie, is it legit to burn tokenized shares ?)

All of this makes me think that a mint and burn function for regulated assets in the form of ERC-20 / ERC-721 / ERC-1155 might be the scope for another standard and might not be extremely necessary to include it here.

Happy to know both of your thoughts [@frangio](/u/frangio) [@tinom9](/u/tinom9)

---

**tinom9** (2025-05-05):

Thanks again [@xaler](/u/xaler)!

---

### mint / burn

In terms of `mint` and `burn`, I stand on burning, theoretically, being needed in every asset, as any could be liquidated (shares rebuying, company closure/bankruptcy).

Minting should also happen at some point of the lifecycle and I see a point on enforcing fixed-supply through reverts, as opposed to only through constructor mints.

Nonetheless, I believe there are obvious trade-offs for multi-standard token compatibility that, even if up to some extent are implied in this ERC (already using `tokenId` and `amount`), as it aims to be universal, can entangle the implementation.

I am onboard with excluding them to keep the standard simple.

---

### freezeTokens

If we exclude `mint` and `burn`, I think there is a stronger point to consider excluding freezing functionality, in favor of a leaner ERC.

Nonetheless, it’s still an inclusion for me, and I’d be more than happy to propose an implementation in the Github PR, if you’re up to it.

---

### Universality

Making this standard universal is a challenge per se, and I see two paths upcoming for common functionality:

1. Different tokens using different interfaces for common logic:

mint(address to, uint256 amount)
2. mint(address to, uint256 tokenId)
3. mint(address to, uint256 tokenId, uint256 amount)
4. Different tokens converging to a common interface:

mint(address to, uint256 tokenId, uint256 amount)

Only if we expect tokens converging to a common interface, it makes sense to standardize it. And, in that case, although I believe it’s marginally better to include it in the ERC, it’s still valid to standardize it in a different ERC. This applies to both points above.

---

Cheers!

---

**EdwinMata** (2025-05-15):

Thank you for putting forward ERC-7943. The interface strikes a strong balance between minimalism and practical utility, particularly for projects focused on real-world asset tokenization. As someone actively deploying tokenized equity, debt, and revenue-sharing instruments across multiple jurisdictions, I believe there is value in introducing an optional extension to the standard that includes mint, burn, and freeze primitives. These should not be understood as business logic enforcers, but as standardized interfaces to reflect legally binding events on-chain.

Minting in RWA environments is not merely the technical creation of tokens. It often corresponds to a capital increase, a debt issuance, or the execution of a convertible instrument. A function such as mintByAuthority(address to, uint256 amount, bytes calldata legalProof) would enable implementations to link the minting process to a legal resolution or authorizing event, such as a shareholder vote or board approval, without enforcing off-chain dependencies. We have also explored additional interface primitives related to governance and legal signaling, which may be suitable for standardization. If this initial contribution is aligned with the direction of the group, we would be happy to share those in a follow-up.

Burning is likewise tied to legally significant actions such as debt repayment, share redemption, or cancellation resulting from a court order. It also applies to cases of company liquidation, where all equity must be extinguished, and corporate acquisitions, where equity is either cancelled for cash or converted into the acquiring company’s equity. In a tokenized environment, this can involve burning the target company’s tokens and minting new ones representing the acquiring entity’s shares. A function such as burnByAuthority(address from, uint256 amount, bytes calldata justification) would provide a structured and auditable way to perform these actions, with the justification field preserving legal traceability.

Freezing is a recurring requirement in legal and compliance operations. It is used to enforce lock-up agreements, address AML/KYC issues, or comply with legal injunctions. A minimal implementation such as freeze(address user, uint256 amount, uint256 id), to allow for ERC-20 and ERC-1155 granularity, together with frozen(address user) would provide sufficient flexibility for most real-world use cases without dictating internal enforcement mechanisms.

These extensions maintain the neutral and portable nature of ERC-7943. They remain fully optional and non-intrusive for implementers who do not require them. But for those operating under legal, regulatory, or governance obligations, these standardized hooks offer a necessary foundation for compliant and auditable asset management without compromising the core specification.

---

**xaler** (2025-05-17):

Thanks [@EdwinMata](/u/edwinmata)  and [@tinom9](/u/tinom9) for your comments.

After thinking a lot about it I think it makes sense to include a freezing/unfreezing functionality.

The main objective of this EIP is to be universal, maximally compatible and future proof. For this to me it must:

- Be compatible with major token standards
- Include only the essential and common features of a broad spectrum of use cases
- Not opinionate on implementation details

Specifically on the second point, I strongly believe that compliance and enforcement actions are the very backbone of RWAs. In this regard `isUserAllowed` and `isTransferAllowed` meet the need to define compliance criteria while `forceTransfer` is an enforcement action. Freezing is another enforcement action that is quite different even if achieving similar results as `forceTransfer`.

Specifically, freezing is generally associated with temporary actions potentially meant to be reversible. Because of all of this my proposition is:

- Freezing must not alter balanceOf / totalSupply results. Instead it must live in separate functions, parts of the standard.
- There must be a way to freeze and unfreeze + a getter to know the freezing status of a specific account.
- isTransferAllowed must consider frozen amounts in its internal logic
- isUserAllowed might or might not take into account frozen assets in its internal logic
- forceTransfer can transfer frozen assets.
- Freeze and unfreeze have similar restricted access assumptions as forceTransfer

For this I propose adding the following to the interface

```solidity
    /// @notice Emitted when a specific amount of a token ID is frozen for a user.
    /// @param user The address of the user whose tokens are being frozen.
    /// @param tokenId The ID of the token being frozen.
    /// @param amount The amount of tokens frozen.
    event Frozen(address indexed user, uint256 indexed tokenId, uint256 amount);

    /// @notice Emitted when a specific amount of a token ID is unfrozen for a user.
    /// @param user The address of the user whose tokens are being unfrozen.
    /// @param tokenId The ID of the token being unfrozen.
    /// @param amount The amount of tokens unfrozen.
    event Unfrozen(address indexed user, uint256 indexed tokenId, uint256 amount);

    /// @notice Freezes a specified amount of a token ID for a user.
    /// @dev Requires specific authorization. Frozen tokens cannot be transferred by the user.
    /// @param user The address of the user whose tokens are to be frozen.
    /// @param tokenId The ID of the token to freeze. Use 0 for ERC-20.
    /// @param amount The amount of tokens to freeze. Use 1 for ERC-721.
    function freeze(address user, uint256 tokenId, uint256 amount) external;

    /// @notice Unfreezes a specified amount of a token ID for a user.
    /// @dev Requires specific authorization.
    /// @param user The address of the user whose tokens are to be unfrozen.
    /// @param tokenId The ID of the token to unfreeze. Use 0 for ERC-20.
    /// @param amount The amount of tokens to unfreeze. Use 1 for ERC-721.
    function unfreeze(address user, uint256 tokenId, uint256 amount) external;

    /// @notice Checks the amount of a specific token ID that is frozen for a user.
    /// @param user The address of the user.
    /// @param tokenId The ID of the token. Use 0 for ERC-20.
    /// @return frozenAmount The amount of the token ID currently frozen for the user.
    function frozenAmount(address user, uint256 tokenId) external view returns (uint256 frozenAmount);
```

I’m curious to know your thoughts on this, meanwhile I’ll start working to add it in the reference implementation and in the draft of the EIP

---

**codebyMoh** (2025-05-22):

How do we rebuild/create EIP so it can speak the language of real-world finance, law, and ownership?” Inspired from ERC 3643.

Imagine a smart contract that doesn’t just transfer tokens, but enforces UCC Article 9 or Basel III risk-weighted compliance by default.

We have to encode legal frameworks and economic primitives as executable state machines. [@xaler](/u/xaler) mentioned a challange which is RWA possesses unique Characteristic so each offchain contract needs to be rewritten onchain.

---

**xaler** (2025-05-22):

Thanks [@codebyMoh](/u/codebymoh) for your comment!

While I agree that the language should aim to be universal, I believe there’s still value in leveraging the functionalities provided by the standard to enable a dynamic mechanism that adapts to each jurisdiction. What we’re working on is a foundational set of primitives that can be combined and extended to support the kinds of functionalities you’re referring to.

Legislation is often not entirely objective and is subject to interpretation. It also evolves over time and is rarely static. Expecting different jurisdictions to fully converge on a single rule set seems unrealistic to me.

That said, once we establish a solid base, I believe this will provide a flexible framework upon which others can build to meet their specific needs.

On a separate note [@tinom9](/u/tinom9) I’ve included a freezing functionality with the following interface:

```auto
/// @notice Emitted when `setFrozen` is called, changing the frozen `amount` of `tokenId` tokens for `user`.
/// @param user The address of the user whose tokens are being frozen.
/// @param tokenId The ID of the token being frozen.
/// @param amount The amount of tokens frozen.
event FrozenChange(address indexed user, uint256 indexed tokenId, uint256 indexed amount);

/// @notice Error reverted when a transfer is attempted from `user` but the `amount` is bigger than available (unfrozen) tokens.
/// @param user The address holding the tokens.
/// @param tokenId The ID of the token being transferred.
/// @param amount The amount being transferred.
/// @param available The amount of tokens that are available to transfer.
error ERC7943NotAvailableAmount(address user, uint256 tokenId, uint256 amount, uint256 available);

/// @notice Changes the frozen status of `amount` of `tokenId` tokens belonging to an `user`.
/// This overwrites the current value, similar to an `approve` function.
/// @dev Requires specific authorization. Frozen tokens cannot be transferred by the user.
/// @param user The address of the user whose tokens are to be frozen/unfrozen.
/// @param tokenId The ID of the token to freeze/unfreeze.
/// @param amount The amount of tokens to freeze/unfreeze.
function setFrozen(address user, uint256 tokenId, uint256 amount) external;

/// @notice Checks the frozen status/amount of a specific `tokenId`.
/// @param user The address of the user.
/// @param tokenId The ID of the token.
/// @return amount The amount of `tokenId` tokens currently frozen for `user`.
function getFrozen(address user, uint256 tokenId) external view returns (uint256 amount);
```

I’ve also added some reasoning on the naming in the EIP draft to justify the name chosen and the design too.

---

**codebyMoh** (2025-05-23):

Yeah. Static is the start of the legislation contracts to be interpreted, But if each company/individuals start writing offchain contracts with onchain compatibility to compile and interpret would be game changing for the RWA Interface becoming adoptable, Still Country Law’s execution is a long miles to go yet for being on chain.

---

**2facedsquid** (2025-05-23):

Hi [@xaler](/u/xaler) very interesting proposal, I like the universal approach.

One thing to consider adding to the interface is a holding/lockup period. Based on experience working with issuers tokenizing RWAs holding periods come up a lot. It mostly concerns primary offerings where holders of the tokenized assets cannot enter the secondary market until the holding period is over. There could be two types of holding periods a global one which is set based on a timestamp and prevents all holders to transfer until the treshold is reach ( for example one year ) and a holder specific one which enters into effect when the tokens are transfered to the user ( users receives new tokens and they need to hold them for 30 days and once they timestamp is reached they are able to trade ). The timestamp could be changed by a dedicated AccessControl role.

For regulatory purposes it would be also good to consider adding a Pause functionality same as ERC20Pausable. A simple switch which has a dedicated AccessControl role.

One question I have is whats the approach when handling interactions with other smart contracts ( liquidity pools, escrows, swaps ). These contracts will also need to be whitelisted but wouldnt it be better to extend whitelisting with types? This could open the doors for exemptions like tokens which are stored in a liquidity pool cannot be frozen or are not subject to other limitations.

---

**xaler** (2025-05-23):

Hey [@2facedsquid](/u/2facedsquid) !

Thanks for the feedback and comments. I’ll split my reply in two:

On **lockups and pausability**: totally agree these are useful features, especially in RWA use cases. That said, uRWA is intentionally **minimal**. It’s meant to define the *interface*, not a specific policy. Things like gloabal/per-holder timelock periods or pause switches can be easily added on top via `isTransferAllowed` or `isUserAllowed`, so implementers have full freedom without the standard enforcing opinionated mechanisms. Additionally, while some RWA can have global or per holder lockups, other might not necessarily need this feature.

About **whitelisting smart contracts**: this is exactly why the standard is flexible. `isUserAllowed` can be a plain whitelist, a typed one (e.g. roles like KYC’d user, DeFi pool, custodian), or even a blacklist. Same for `isTransferAllowed`. This makes it easy for DeFi protocols to integrate by checking these getters without needing to know the specifics under the hood.

What do you think ?

Thanks again for the feedback, keep it coming!

---

**2facedsquid** (2025-05-28):

I agree to keep it minimal utilizing isTransferAllowed or isUserAllowed is a great design choice. Thank you for the response [@xaler](/u/xaler) it made it more clear for me.

---

**tinom9** (2025-05-29):

Thanks for the updates!

---

[@xaler](/u/xaler), I’m on board with your freezing definition proposal, with a couple of nits:

- Force event instead of FrozenChange.
- ERC7943InsufficientUnfrozenBalance event instead of ERC7943NotAvailableAmount, with more specificity over ERC20InsufficientBalance.
- Enforce token unfreezing on forceTransfer and burning methods.

---

If freezing is added to the standard, I believe the point of adding `mint` and `burn` interfaces is stronger.

---

[@codebyMoh](/u/codebymoh), I believe specific laws and regulations should be handled through the `isUserAllowed` and `isTransferAllowed` interfaces, and modular compliance rules or extensions can be developed and plugged into the leaner ERC-7943 standard.

---

[@2facedsquid](/u/2facedsquid), I envision:

- Lock-ups implemented through isTransferAllowed checks and modular compliance rules.
- Pausability implemented through isTransferAllowed checks. Although I imagine it being a much used feature, so it wouldn’t bother me adding a setPaused method to the standard.

---

I left my detailed suggestions in the ERC draft PR (https://github.com/ethereum/ERCs/pull/1029#issuecomment-2917155603).

---

**xaler** (2025-05-29):

Thanks [@tinom9](/u/tinom9) for your thoughts and suggestions on this.

> Force event instead of FrozenChange.

I agree with this ![:smiley:](https://ethereum-magicians.org/images/emoji/twitter/smiley.png?v=12)

> ERC7943InsufficientUnfrozenBalance event instead of ERC7943NotAvailableAmount, with more specificity over ERC20InsufficientBalance.

I agree with the specificity and probably we should add it as a SHOULD (in case the token doesn’t have specific errors as the ERC20 template by OZ has) not replace the specific errors for insufficient balances (outside the frozen one). However I’m still having some issues with the naming.  “not available” (“unavailable”) suggests a temporary condition like a frozen amount not allowing you to transfer a determined amount while “insufficient” suggest more of a general lack of funds. Indeed if you try to transfer more tokens than the unfrozen one, you technically have a “sufficient” balance, but not an “available” one to be used. What do you think about this argument ? What about changing to “unavailable” instead ?

> Pausability implemented through isTransferAllowed checks. Although I imagine it being a much used feature, so it wouldn’t bother me adding a setPaused method to the standard.

I agree in using `isTransferAllowed`, we might end up doing the error of forcing a `setPaused` and have integrators being forced to integrate this to be compliant with this EIP even if they don’t need it.

Regarding instead the fact of unfreezing when doing `forceTransfer` / `burn`

For `forceTransfer`:

I think the standard should still say that the function `SHOULD` skip freezing validations ( I believe you proposed a “MUST” but I’m curious to know why. If the function actually skips that, then I agree with your suggestion of unfreezing first (and emit an event) before doing the transfer, so that the transfer event doesn’t emit an amount of unavailable tokens. However, the integrators might decide to NOT skip freezing validations in a `forceTransfer`. I am thinking of use cases where there’s an automated penalty system that forcefully transfer tokens out without skipping the freezing status (that might have a higher priority over the penalty system).

For `burn`:

I actually think is dangerous to allow a `burn` to unfreeze. The `burn` function is meant to be either public (anyone can burn) or restricted. In the former case, burning would actually circumvent the freezing status imposed by an authorized party. This would easily translate into frozen assets being on purpose burnt down to avoid any reusage of those by the freezing authority.

Can you clarify why the need of a MUST in `burn` and `forceTransfer` to unfreeze ?

---

**tinom9** (2025-05-30):

> I agree with the specificity and probably we should add it as a SHOULD (in case the token doesn’t have specific errors as the ERC20 template by OZ has) not replace the specific errors for insufficient balances (outside the frozen one). However I’m still having some issues with the naming. “not available” (“unavailable”) suggests a temporary condition like a frozen amount not allowing you to transfer a determined amount while “insufficient” suggest more of a general lack of funds. Indeed if you try to transfer more tokens than the unfrozen one, you technically have a “sufficient” balance, but not an “available” one to be used. What do you think about this argument ? What about changing to “unavailable” instead ?

I used `ERC20InsufficientBalance` to refer to the error as ERC-6093 defines it and OZ implements it, but I meant the underlying error. A phrasing in the ERC-7943 definition could be:

```solidity
    /// @notice Error reverted when a transfer is attempted from `user` with an `amount` less or equal than its balance, but greater than its unfrozen balance.
    /// @param user The address holding the tokens.
    /// @param tokenId The ID of the token being transferred.
    /// @param amount The amount being transferred.
    /// @param unfrozenBalance The amount of tokens that are unfrozen and available to transfer.
    error ErrorName(address user, uint256 tokenId, uint256 amount, uint256 unfrozenBalance);
```

In terms of error naming, I believe “insufficient balance” and “unavailable amount” are synonyms in this context, although the latter has a more temporal component. I slightly prefer “insufficient balance” due to its clarity and ongoing use in ERC-6093, but I see both as valid options.

As I see it, there are 2 ways we can go with this error:

1. Define and specify the error to throw when a user tries to transfer more tokens than they have unfrozen. Either ERC7943InsufficientUnfrozenBalance or ERC7943FrozenAmount.
2. Define a broad and miscellaneous error to throw when the user tries to transfer more tokens than they have available, either due to being frozen, or locked by custom compliance implementation logic. ERC7943UnavailableAmount.

To me, achieving specificity is key, and we should go with the first, keeping additional errors to be defined in extensions, either custom or standardized in other ERCs.

---

> I agree in using isTransferAllowed, we might end up doing the error of forcing a setPaused and have integrators being forced to integrate this to be compliant with this EIP even if they don’t need it.

We might need more context from other industry integrators, but I wouldn’t discard the feature yet. Most security tokens I’ve seen include it.

---

> For forceTransfer:
>
>
> I think the standard should still say that the function SHOULD skip freezing validations ( I believe you proposed a “MUST” but I’m curious to know why. If the function actually skips that, then I agree with your suggestion of unfreezing first (and emit an event) before doing the transfer, so that the transfer event doesn’t emit an amount of unavailable tokens. However, the integrators might decide to NOT skip freezing validations in a forceTransfer. I am thinking of use cases where there’s an automated penalty system that forcefully transfer tokens out without skipping the freezing status (that might have a higher priority over the penalty system).

`forceTransfer` being a permissioned function, is there a case where you may not want to unfreeze tokens to forcefully transfer them out of a wallet and revert? I don’t visualize it.

One thing that concerns me is that, if we don’t impose that `forceTransfer` unfreezes tokens (only if the transfer cannot be fully satisfied with the unfrozen balance), the tokens must be first unfrozen and then forcefully transferred, adding the requirement to execute those calls in batch to avoid being front-run on the forceful transfer by the user.

I see the benefit of imposing the `forceTransfer` implementation in that we don’t end up with a method that behaves differently in different tokens with a core functionality such as token freezing. Either we need to extend the `ForcedTransfer` event to specify which tokens were frozen and which unfrozen, or we need to impose the implementation (`MUST`), if we want integrators to accurately index frozen and baseline balances.

Additional flexibility can be obtained with custom batched actions.

---

> For burn:
>
>
> I actually think is dangerous to allow a burn to unfreeze. The burn function is meant to be either public (anyone can burn) or restricted. In the former case, burning would actually circumvent the freezing status imposed by an authorized party. This would easily translate into frozen assets being on purpose burnt down to avoid any reusage of those by the freezing authority.

We have a different vision of who’s allowed to call `burn`.

I don’t see token holders being able to burn their shares of a company, or other underlying securities. I see token burning always happening from the permissioned side.

If we add permissioned `mint` and `burn` functions to the standard, I’d go the same way than with the `forceTransfer` definition: impose token unfreezing.

If we don’t, I see the benefit of specifying each expected behaviour:

> Burning CAN run validation to prohibit burning more assets than the ones available (difference between balance and frozen amount). For example, in public burning functions.
> Burning CAN bypass freezing validation, in which case it MUST update the freezing status if required, emitting a Frozen event before the Transfer event. For example, in permissioned burning functions.

---

**xaler** (2025-06-02):

Hey [@tinom9](/u/tinom9)

I’ve updated both the reference implementation and EIP draft with following changes:

- Renamed FrozenChange to Frozen
- Added specification about general purpose use of ERC7943NotAllowedUser and ERC7943NotAllowedTransfer
- Changed description and added a note for ERC7943NotAvailableAmount to improve specificity over base standard errors (like ERC20InsufficientBalance).
- Renamed ERC7943NotAvailableAmount to ERC7943InsufficientUnfrozenBalance.

Additionally, to better reflect your concern of indexing the correct unfrozen / frozen amounts during forceTransfers and burn, I’ve added a previousValue and newValue in the Frozen event, so that differences can be tracked. Now if a force transfer or a burn changes the freezing status, the Frozen event will emit both old and new value, so that changes in freezing status can be tracked.

I’ve also updated the EIP and implementation to reflect the error specificity concerns.

> I agree in using isTransferAllowed, we might end up doing the error of forcing a setPaused and have integrators being forced to integrate this to be compliant with this EIP even if they don’t need it. We might need more context from other industry integrators, but I wouldn’t discard the feature yet. Most security tokens I’ve seen include it.

What makes me to hesitate about it is:

- Do all use cases need this ? If we can name a few that don’t neccessarily require it, I wouldn’t go with it.
- OZ already has an historical and battle tested, widely adopted, solution for pausable contracts and it’s easy to think about this as one of the multiple potential extensions of an ERC-7943 minimal token.

> forceTransfer being a permissioned function, is there a case where you may not want to unfreeze tokens to forcefully transfer them out of a wallet and revert? I don’t visualize it.

Yes, cases in which the freezing authority has more power (higher priority) in the entity performing a forced transfer. Those might be two separate entities. You can give `forceTransfer` rights to one or more entities, and `setFrozen` rights to completely different entities. An example might be perpetual contracts where a continous funding mechanism might leverage the `forceTransfer` functionality. In this sense, the `forceTransfer` would be functional to a perpetual contract funding mechanism but might not have the freedom to move more than frozen assets, since those might be seized by goverments or higher level authorities than a smart contract logic for perpetual contracts. What do you thinkg about this ?

Still, the EIP suggests both things now, a forceTransfer and a burning CAN skips the freezing validations, but they also CAN NOT skip those. The most important thing is that if those automatically unfreeze, the must emit a frozen event to reflect that, before the native transfer event.

In general I also gave a general restructure to the document of the EIP to make it more readable and easy to follow.

Let me know how it looks like now to you and thanks for the feedback !

---

**tinom9** (2025-06-09):

### Previous value in Frozen event

> Additionally, to better reflect your concern of indexing the correct unfrozen / frozen amounts during forceTransfers and burn, I’ve added a previousValue and newValue in the Frozen event, so that differences can be tracked. Now if a force transfer or a burn changes the freezing status, the Frozen event will emit both old and new value, so that changes in freezing status can be tracked.

I’m not sure emitting the previous value is necessary. If indexers want to keep track of the difference, they can check against their currently indexed value.

ERC20 tokens already behave by not emitting previous values in allowance nor balance changes. I’d argue the ERC-7943 should behave likewise.

---

### Pausability

> What makes me to hesitate about it [pausability] is:
>
>
> Do all use cases need this ? If we can name a few that don’t neccessarily require it, I wouldn’t go with it.

I’d say the majority of permissioned tokens, of which securities and RWAs should be a subset of, use it.

Doing a minor research about it, I can find:

- Stablecoins:

USDC: paused.
- USDT: paused.

Debt-based:

- Blackrock’s BUILD: isPaused.
- Superstate’s USTB: paused.

Real estate:

- RealT: none found, might be implemented through the processor entity.

Gold:

- Tether Gold: none found, the only other permissioning feature is a blacklist.
- Paxos Gold: paused.

> OZ already has an historical and battle tested, widely adopted, solution for pausable contracts and it’s easy to think about this as one of the multiple potential extensions of an ERC-7943 minimal token.

I agree that there’s no need to standardize it for ease-of-use of the feature, as OZ already has the de-facto standard for pausability.

I’m more concerned about having a clear criteria for what features are included in the baseline ERC. One can argue that token freezing is not necessarily required within the ERC, as it can be enforced through `forceTransfer` and vaults, but that it’s best to standardize it, and that pausability can be enforced through `isTransferAllowed` and extensions, but that it’s also best to standardize it.

I’d aim for what we envision will be the requirements for 90% of the tokens into the baseline ERC, and leave the rest to extensions.

That said, I don’t have enough insights on pausability requirements to take a clear stand on its inclusion. To me, although most tokens have it, it feels operative and not a core token functionality, similarly to upgradeability.

---

### Unfreezing in forced transfers

> Yes, cases in which the freezing authority has more power (higher priority) in the entity performing a forced transfer. Those might be two separate entities. You can give forceTransfer rights to one or more entities, and setFrozen rights to completely different entities. An example might be perpetual contracts where a continous funding mechanism might leverage the forceTransfer functionality. In this sense, the forceTransfer would be functional to a perpetual contract funding mechanism but might not have the freedom to move more than frozen assets, since those might be seized by goverments or higher level authorities than a smart contract logic for perpetual contracts. What do you thinkg about this ?

I’d argue forced transfers are not the correct action for that use-case. I believe it has the same implications than using native ERC20 approvals, as you still depend on the user not front-running you to collect the fees, and using an all-powerful permissioned function to execute core business logic doesn’t seem right.

> Still, the EIP suggests both things now, a forceTransfer and a burning CAN skips the freezing validations, but they also CAN NOT skip those. The most important thing is that if those automatically unfreeze, the must emit a frozen event to reflect that, before the native transfer event.

I agree it’s most important that unfreezing emits the `Frozen` event before the native `Transfer` one, and that it should fix indexing concerns, if `ForcedTransfer` and `Transfer` can only occur with unfrozen balances.

I believe the decision is a trade-off between:

1. Forcing unfreezing in forceTransfer and ensuring standard implementation.
2. Allowing forceTransfer to revert on frozen balances and, therefore, a freezer role to be of higher status than a force transferer role.

I have a preference for option 1, as I don’t see any use-case for option 2 and consider `forceTransfer` a “last resort” permissioning function.

If we can come up with option 2 use-cases, it would make total sense to keep it unopinionated.


*(83 more replies not shown)*
