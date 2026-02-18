---
source: magicians
topic_id: 16416
title: "ERC-7551: Crypto Security Token Smart Contract Interface (\"eWpG\")"
author: hagen
date: "2023-11-02"
category: ERCs
tags: [erc, security-token]
url: https://ethereum-magicians.org/t/erc-7551-crypto-security-token-smart-contract-interface-ewpg/16416
views: 3197
likes: 21
posts_count: 31
---

# ERC-7551: Crypto Security Token Smart Contract Interface ("eWpG")

## Abstract

The compliant representation of securities on a distributed ledger network (“crypto securities”) remains one the most prominent use cases for distributed ledger systems. Up until recent developments such activities were not always fully recognized by local securities laws. This led to different views on what information and functionality they should provide. Germany, as one of the first countries in the world, has enhanced its legal framework to fully cover the issuance of securities in electronic form on a distributed ledger network. This standard aims to capture these legal requirements and use them as a framework to define a smart contract interface that enables interactions with crypto securities on-ledger. This standard is backed by the Federal Association of Crypto Registrars and a result of its task force for standardization.

The interface is supposed to work on top of additional standards that cover the actual storage of ownership of shares of a security in the form of a token (e.g. ERC-20 or ERC-1155). While the scope of the underlying token standard is to provide an interface for transferring the crypto securities and retrieving individual holder balances, this standard provides the following additional functionality needed by wallet providers and exchanges to handle crypto securities:

### Transfer compliance

In the case of crypto securities the smart contract needs to check if a transfer of tokens is compliant. The specification therefore adds a `canTransfer()` and a `canTransferFrom()` function that can be used to check if a transfer would be successful given the current compliance rules.

### Token supply management

In the case of a crypto security the supply of tokens is managed by an operator. Operators are able to issue new tokens via the `issue()` function and they can destroy tokens from an account via the `destroyTokens()` function. The terminology used here intentionally differentiates between mint/burn as the technical process of creating and deleting tokens (not within the  scope of the standard) and issue/destroy as the legal process of crediting or removing a quantity of tokens from the balance of the holder.

### Forced transfers

As the result of a legal action, an operator of the crypto security needs to be able to force a transfer between accounts without requiring the consent of the sender. For this, the `forceTransferFrom()` function can be used. This function can also be used to recover tokens of an account where the private key has been lost.

### Frozen tokens

An operator of the security token is able to freeze the whole or a part of an account’s token balance via the `freezeTokens()` function. As a result, these tokens cannot be transferred until unfrozen again by the operator using the `unfreezeTokens()` function.

### Pausing transfers

The token provides ways for an operator to pause and unpause transfers via the `pause()` function.

### Link to off-chain document

A `paperContractHash` value is added to the smart contract’s storage that is meant to be the SHA-256 hash digest integer value of the full binary of a PDF file representing all necessary  issuance documents.

### Metadata JSON file

A JSON file is stored in the `metaDataJSON` variable that describes metadata about the crypto security in the form of key-value pairs. These metadata shall describe the essential properties of the security in a machine-readable format.

## Motivation

The compliant representation of securities on a distributed ledger network (“crypto securities”) remains one the most prominent use cases for distributed ledger systems. Up until recent developments such activities were not always fully recognized by local securities laws. This led to different views on what information and functionality they should provide. Germany, as one of the first countries in the world, has enhanced its legal framework to fully cover the issuance of securities in electronic form on a distributed ledger network.

While standards like ERC-20 and ERC-1155 provide complete interfaces to interact with utility tokens, in order to represent securities in the form of a token more advanced features are necessary. This is caused by two main characteristics of crypto securities:

- In contrast to utility tokens where transfers usually only require the sender to have a sufficient balance, for crypto securities more complex rules can apply that use other data to determine the validity of a transfer. In many cases, token holders with their respective addresses need to be eligible, for example, according to KYC/AML regulation or qualification of the investor to receive and hold tokens.
- Crypto securities need a trusted operator that is granted certain permissions such as pausing transfers or managing the token supply. This trusted operator is sometimes even recognized by local securities laws and licensed by the authorities.

This standard should facilitate the interaction of wallet software, exchanges as well as crypto security operators with different implementations of crypto securities. For wallets and exchanges, this eases the listing of crypto securities no matter who their issuer or operator is. It also makes sure that in case of an operator becoming unavailable, other operators can step in and take over control of the token, securing the rights of token holders.

## Specification

The following specification describes events and functions of a token smart contract representing a crypto security.

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “NOT RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119 and RFC 8174.

### General

Tokens MAY be received by externally owned accounts as well as smart contract accounts (“token holders”). An externally owned account or smart contract account MAY be granted special administrative permissions (“operator”). There MAY be more than one operator.

### Functions

#### activeBalanceOf

This function MUST return the unfrozen balance of an account. This balance can be used by the token holder for transfers to other account addresses.

```solidity
function activeBalanceOf(address tokenHolder) external view returns (uint256);
```

#### frozenBalanceOf

This function MUST return the frozen balance of an account. It MUST NOT be possible to transfer frozen tokens to other accounts. The implementation MAY provide other ways to transfer frozen tokens. If the sender’s unfrozen (“active”) balance is less than the amount to be transferred, the `canTransfer()` and `canTransferFrom()` MUST return `false`.

```solidity
function frozenBalanceOf(address tokenHolder) external view returns (uint256);
```

#### paused

This function MUST return `true` if token transfers are paused and MUST return `false` otherwise. If this function returns `true`, it MUST NOT be possible to transfer tokens to other accounts and the `canTransfer()` and `canTransferFrom()` MUST return `false`.

```solidity
function paused() external view returns (bool);
```

#### paperContractHash

This function MUST return the SHA-256 hash digest integer value of the issuance document PDF file. A paper contract hash with the value 0 has a special meaning: As long as it is 0, transfers cannot be unpaused.

```solidity
function paperContractHash() external view returns (uint256);
```

#### metaDataJSON

This function MUST return a JSON object containing metadata about the crypto security in the form of key-value pairs. It MAY be empty.

```solidity
function metaDataJSON() external view returns (string);
```

#### canTransfer

This function MUST return `true` if the message sender is able to transfer `amount` tokens to `to` respecting all compliance, investor eligibility and other implemented restrictions. Otherwise it MUST return `false`.

```solidity
function canTransfer(address to, uint256 amount) external view returns (bool);
```

#### canTransferFrom

This function MUST return `true` if `from` is able to transfer `amount` tokens to `to` respecting all compliance, investor eligibility and other implemented restrictions. Otherwise it MUST return `false`.

```solidity
function canTransferFrom(address from, address to, uint256 amount) external view returns (bool);
```

#### issue

This function MUST increase the balance of  `to` by `amount` without decreasing the amount of tokens from any other holder. This function MUST throw if the sum of `amount` and the amount of already issued tokens is greater than the total supply. It MUST emit a `Transfer` as well as an `TokensIssued` event. Paused transfers MUST NOT prevent an issuance. The `data` parameter MAY be used to further document the action.

```solidity
function issue(address to, uint256 amount, bytes calldata data) external;
```

#### destroyTokens

This function MUST reduce the balance of `tokenHolder` by `amount` without increasing the amount of tokens of any other holder. It MUST emit a `TokensDestroyed` as well as a `Transfer` event. The `Transfer` event MUST contain `0x0` as the recipient account address. The function MUST throw if `tokenHolder`’s balance is less than `amount` (including frozen tokens). It MUST NOT be possible to destroy the supply. It MUST NOT be possible to issue destroyed tokens to other accounts. Paused transfers MUST NOT prevent destroying tokens. The `data` parameter MAY be used to further document the action.

```solidity
function destroyTokens(address tokenHolder, uint256 amount, bytes calldata data) external;
```

#### forceTransferFrom

This function MUST transfer `amount` tokens to `to` without requiring the consent of `from`. The function MUST throw if `from`’s balance is less than `amount` (including frozen tokens). If the frozen balance of `from` is used for the transfer a `TokenUnfrozen` event must be emitted. The function MUST emit a `Transfer` event. The `data` parameter MAY be used to further document the action.

```solidity
function forceTransferFrom(address from, address to, uint256 amount, bytes calldata data) external;
```

#### freezeTokens

This function MUST freeze `amount` tokens of `tokenHolder`. Frozen tokens cannot be transferred to other accounts. The function MUST emit a `TokensFrozen` event. The function MUST throw if `tokenHolder`’s active balance is less than `amount` (excluding already frozen tokens). The `data` parameter MAY be used to further document the action.

```solidity
function freezeTokens(address tokenHolder, uint256 amount, bytes calldata data) external;
```

#### unfreezeTokens

This function MUST unfreeze `amount` tokens of `tokenHolder`. The function MUST emit a `TokensUnfrozen` event. The function MUST throw if `tokenHolder`’s frozen balance is less than `amount`. The `data` parameter MAY be used to further document the action.

```solidity
function unfreezeTokens(address tokenHolder, uint256 amount, bytes calldata data) external;
```

#### pauseTransfers

If `_paused` is provided as `true` transfers MUST become paused. If `false` is provided, transfers MUST be unpaused. The function MUST throw if `true` is provided although transfers are already paused as well as if `false` is provided while transfers are already unpaused. The function MUST throw if `false` is provided while `paperContractHash` is `0`.

```solidity
function pauseTransfers(bool _paused) external;
```

#### setPaperContractHash

This function MUST update the `paperContractHash` value. `_paperContractHash` MUST be the SHA-256 hash digest integer value of the issuance document PDF file. A paper contract hash with the value 0 has a special meaning: As long as it is 0, transfers cannot be unpaused.

```solidity
function setPaperContractHash(uint256 _paperContractHash) external;
```

#### setMetaDataJSON

This function MUST update the `metaDataJSON` value. `_metaDataJSON` MUST be a JSON data structure containing metadata about the crypto security in the form of key-value pairs. It MAY be empty.

```solidity
function setMetaDataJSON(string calldata _metaDataJSON) external;
```

### Events

#### TokensIssued

This event MUST be triggered when new tokens are issued increasing the `totalSupply`.

```solidity
event TokensIssued(address to, uint256 amount);
```

#### TokensDestroyed

This event MUST be triggered when tokens are destroyed on an account.

```solidity
event TokensDestroyed(address tokenHolder, uint256 amount);
```

#### ForcedTransfer

This event MUST be triggered on a successful call of the `forceTransferFrom()` function.

```solidity
event ForcedTransfer(address indexed from, address indexed to, uint256 amount)
```

#### TokensFrozen

This event MUST be triggered if tokens are frozen for an account.

```solidity
event TokensFrozen(address indexed tokenHolder, uint256 amount);
```

#### TokensUnfrozen

This event MUST be triggered if tokens are unfrozen for an account.

```solidity
event TokensUnfrozen(address indexed tokenHolder, uint256 amount);
```

#### SetPaperContractHash

This event MUST be triggered when the `paperContractHash` value is updated.

```solidity
event SetPaperContractHash(uint256 paperContractHash);
```

#### SetMetaDataJSON

This event MUST be triggered when the `metaDataJSON ` value is updated.

```solidity
event SetMetaDataJSON(string metaDataJSON);
```

### Interface

```solidity
interface IERCXXXX {

	// Events
	event TokensIssued(address to, uint256 amount, bytes data);
	event TokensDestroyed(address tokenHolder, uint256 amount, bytes data);
	event ForcedTransfer(address indexed from, address indexed to, uint256 amount, bytes data);
	event TokensFrozen(address indexed tokenHolder, uint256 amount, bytes data);
	event TokensUnfrozen(address indexed tokenHolder, uint256 amount, bytes data);
	event SetPaperContractHash(uint256 paperContractHash);
	event SetMetaDataJSON(string metaDataJSON);

	// View functions
	function activeBalanceOf(address tokenHolder) external view returns (uint256);
	function frozenBalanceOf(address tokenHolder) external view returns (uint256);
	function paused() external view returns (bool);
	function paperContractHash() external view returns (uint256);
	function metaDataJSON() external view returns (string);
	function canTransfer(address to, uint256 amount) external view returns (bool);
	function canTransferFrom(address from, address to, uint256 amount) external view returns (bool);

	// Operator functions
	function issue(address to, uint256 amount, bytes calldata data) external;
	function destroyTokens(address tokenHolder, uint256 amount,  bytes calldata data) external;
	function forceTransferFrom(address from, address to, uint256 amount, bytes calldata data) external;
	function freezeTokens(address tokenHolder, uint256 amount, bytes calldata data) external;
	function unfreezeTokens(address tokenHolder, uint256 amount, bytes calldata data) external;
	function pauseTransfers(bool _paused) external;
	function setPaperContractHash(uint256 _paperContractHash) external;
	function setMetaDataJSON(string calldata _metaDataJSON) external;
}
```

## Rationale

This standard is the result of the standardization working group of the German Federal Association of Crypto Registrars. It’s based on the smart contract implementations of its members. It contains terminology and abstract ideas also published in the EIP-1411 and EIP-3643 standard proposals. Both proposals were considered as alternatives to drafting this standard but were rejected because they seemed not complete or contained features for specific use cases not common to all association members.

This standard should not be understood to be a guideline for developing security token implementations. For a full security token implementation, we expect this standard to be combined with the underlying token itself (e.g. based on EIP-20 or EIP-1155)), permission management and authorization logic for operators, different mechanisms to determine the compliance of a specific token transfer, as well as mechanisms to upgrade the token smart contract logic. In contrast, this interface standard describes minimum requirements for the token smart contract representing a crypto security.

## Security Considerations

The standard specifications don’t include requirements for permission management of operators. Implementations SHOULD make sure that the operator functions can only be executed with sufficient authorization.

In addition, to be able to fix security issues, the token smart contract’s logic SHOULD be upgradable by the operator or another account with sufficient authorization.

The specification puts a lot of trust into the operators because they can manage the token supply and even force transfer token amounts. Therefore, entities managing operator accounts must ensure that they use secure off-chain infrastructures to manage and interact with the smart contract implementation.

## Copyright

Copyright and related rights waived via CC0.

–

PR: [Add ERC: Crypto Security Token Smart Contract Interface by itinance · Pull Request #85 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/85)

## Replies

**Joachim-Lebrun** (2023-11-02):

copying my comment from [Add ERC: Crypto Security Token Smart Contract Interface by itinance · Pull Request #85 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/85)

> Hello,
>
>
> I couldn’t help but notice that the interfaces you’re describing closely resemble those in ERC-3643. Since both standards appear to address similar functionalities, I believe that leveraging the existing ERC-3643 might be more beneficial for the broader community.
>
>
> In the spirit of advancing the industry cohesively, minimizing redundancy in standards can be incredibly valuable. Instead of introducing a new standard, why not consider building upon the established foundation of ERC-3643?
>
>
> If you’re keen to explore this further, I encourage you to visit the ERC-3643 Association. Your insights and perspectives would be highly valued, and the association always welcomes new members interested in contributing to the standard’s evolution. If you have proposed modifications or unique viewpoints, they would certainly be appreciated and considered by the community.
>
>
> Looking forward to potentially collaborating and integrating our efforts towards a unified standard.

---

**hagen** (2023-11-02):

Hi [@Joachim-Lebrun](/u/joachim-lebrun)

thank you very much for reaching out!

We fully agree that we should minimize redundancy. But the ERC-3643 is integrating the OnchainID as a mandatory way of managing the permissions. The Members of the Association decided that permission management should be part of the implementation and might differ because of different use cases, business models and given infrastructure to integrate in.

Furthermore, in my **personal opinion**, ERC-3643 addresses too many aspects for a single token standard and should have been split into smaller parts, with each ERC covering only one specific aspect in accordance with the **Single Responsibility Principle**. Currently, ERC-3643 also encompasses the Trusted Issuers Registry, Identity Registry, Token Lifecycle, and Topic Claims, which represents a very broad approach that goes far beyond our actual requirements.

I am happy to discuss this and other topics.

---

**Joachim-Lebrun** (2023-11-02):

Thank you for your prompt response and for sharing your perspectives.

While I appreciate the rationale behind your decision to propose a new standard, I’d like to highlight a few critical points:

1. Similarity and Ethical Considerations: It is noticeable that every function described in your proposed interfaces has an equivalent in ERC-3643, essentially mirroring its functionality. However, there is no mention or acknowledgment of ERC-3643 in your proposal. In the realm of open-source and CC0 copyright license, ethical considerations are paramount. Acknowledging sources and building upon existing work, rather than replicating it, is essential for the integrity and collaborative progress of the community.
2. Compatibility and Terminology: The proposed standard alters function names from those established in ERC-3643, which has implications for compatibility. For instance, your issue() and destroyTokens() functions correspond to the mint() and burn() functions in ERC-3643. By deviating from established terminology, which aligns with prior token standards like ERC-20, ERC-721, and ERC-1155, the proposed standard risks creating unnecessary fragmentation and incompatibility with existing systems developed for ERC-3643.
3. Community Engagement: ERC-3643 is currently in the “review” status, yet there has been no attempt from your side to communicate concerns or participate in the ongoing discussions surrounding ERC-3643, either on the Ethereum Magicians forum or within the ERC-3643 association, of which Token Forge is a member. Constructive engagement and collaboration in the standard crafting process are crucial for the evolution of meaningful and widely accepted standards.
4. Onchain Identity vs. Wallet Whitelisting: Your reluctance to use on-chain identity contracts and preference for relying solely on wallet addresses raises concerns. It’s important to note that OnchainID is not a proprietary solution; it is a set of audited, open-source smart contracts. It’s currently referred to as OnchainID simply because it hasn’t been formalized into its own ERC yet. However, the ERC-3643 association is planning to propose it as a standalone ERC in the upcoming months.
Moving away from on-chain identity management towards wallet whitelisting seems like a regression. On-chain identity-based management is crucial for automating compliance efficiently. For instance, setting country-specific investor limits or enforcing transaction volume caps per investor becomes challenging, if not impossible, with wallet whitelists. An identity-based approach is necessary to enable such automated on-chain compliance measures effectively. By understanding that OnchainID is an open-source, non-proprietary solution, the benefits it brings to the table in terms of compliance and automation become even clearer.
5. Violation of EIP-1 Standards and Principles: In proposing a new standard that closely mirrors an existing one without substantial or necessary differentiation, there is an apparent deviation from the guiding principles of EIP-1. EIP-1 emphasizes the importance of creating standards that address unique needs, promote innovation, and avoid unnecessary duplication. The proposal in question, while presenting similar functionalities as ERC-3643, does not introduce innovative or distinct features that warrant a separate standard. This approach not only fragments the ecosystem but also detracts from the collaborative spirit that EIP-1 advocates. Standards should build upon each other, advancing the ecosystem, rather than creating parallel paths that lead to the same destination with little added value.

In light of these points, I strongly believe that building upon and enhancing the existing ERC-3643 standard, rather than introducing a parallel one with similar functionalities but divergent implementation, would be more beneficial for the community as a whole. Collaboration, acknowledgement of existing work, and community engagement are key to advancing the industry in a unified and constructive manner.

I am open to further discussions and hope we can find common ground to move forward collaboratively.

---

**Aboudjem** (2023-11-02):

I agree with [@Joachim-Lebrun](/u/joachim-lebrun) 's point. It seems a bit off to copy **ERC-3643**, remove a feature, and pitch it as a new standard.

By that logic, I could also make a new standard from ERC-20 by just removing the `transferFrom` function.

It’s important to build on our joint efforts in the community instead of creating overlapping standards.

---

**moinlars** (2023-11-03):

Thanks for sharing your opinion on the proposal. It’s good to see this engagement and your concerns with regards to your proposed standard are understandable.

1. Similarity and Ethical Considerations: While the standard uses similar terminology I think it’s a bit stretched to claim some kind of copyright for common industry terminology that I think has been commonly used for some years. It has also been used in the ERC1400 standard proposal for example.
2. Compatibility and Terminology: The issue and destroy functions have a different purpose than mint and burn. The issue and destroy don’t necessarily mint new tokens or delete them. It leaves freedom of implementation to achieve the issuance or redemption of new securities.
3. Community Engagement: There haven’t been any active discussions on your proposal for months since very recently which also just included “re-activating” the pull request. Therefore, we thought it would be better to create a new proposal than trying to change a different approach with the same goal. Besides that, we’re of course open to constructive discussions.
4. Onchain Identity vs. Wallet Whitelisting: I don’t think using on-chain identities is a bad idea and it’s in fact compliant to the standard proposal here. It’s just that it’s not so widely used in the industry at the moment that we thought it to be necessary to standardize.
5. Violation of EIP-1 Standards and Principles: In my view, there are very distinctive differences to the ERC3643 proposal that justify the creation of a new standard proposal as we’ve tried to explain in the rationale. The goal of this proposal is to have an open standard with a minimum set of requirements for security tokens that leaves as much freedom of implementation where possible. Its primary focus is to provide a simple interface to interact with security tokens. In my understanding, the ERC3643 proposal tries to give as much guidance for implementation as possible. Therefore, I would say that both standards complement each other very well. I think it would be beneficial to resolve the naming mismatches so that both proposals work well in combination.

Cheers, Lars (Co-author)

---

**MarkusKluge** (2023-11-03):

I agree with [@moinlars](/u/moinlars) . For example, ERC-3643 requires mandatory compatibility with ERC-20. The law, which was essentially the reason we built this EIP, introduces different legal statuses for securities in relation to their owners and owner types. Although there is still an open discussion about whether this must or should be implemented at the level of smart contracts, we want to keep the option open to utilize the possibilities offered by ERC-1155 and to map these different legal statuses via token IDs. We are currently working on another EIP that reflects this, based on the first EIP.

This is just one reason why we decided to create a more open EIP, not forcing compatibility or integration with existing standards that could restrict flexibility in implementation.

I really like the way ERC-3643 approaches the challenges of building compliant securities. But as I have already said, I feel the restrictions are too stringent. Looking forward to a fruitful discussion.

Cheers, Markus (Co-author)

---

**Joachim-Lebrun** (2023-11-03):

Thank you for your detailed response. It’s vital to maintain a rigorous dialogue to ensure that the Ethereum community moves forward cohesively and with the best standards in place. Allow me to address each point in turn:

1. Similarity and Acknowledgment: While it’s understood that certain terminologies have become industry-standard, the concern extends beyond lexical choices. The core issue is the overlap in functionalities without acknowledgment of pre-existing standards, specifically ERC-3643. While ERC-3643 was mentioned nowhere in your proposal, the functions it outlines seem to be echoed in your proposal with minor modifications. This lack of acknowledgment can be misleading and is, at best, a disservice to collaborative efforts within the Ethereum community. As for ERC-1400, its non-adoption into the official repositories further emphasizes the importance of due process and community agreement in standard proposals.
2. Compatibility and Functionality: It’s important to emphasize that ERC-3643 allows for flexibility in implementation, including subscription/redemption through smart contracts. Assigning the agent role to a contract that can invoke mint/burn functions can achieve what you propose without reinventing the wheel. Additional metadata can also be implemented in conjunction with ERC-3643’s functions. Thus, proposing a standard with different nomenclatures only serves to fragment the ecosystem unnecessarily.
3. Community Engagement and Transparency: The stagnation of ERC-3643 was a deliberate pause for auditing and perfecting the standard, not a lack of interest or community engagement. The resurgence and removal from stagnant status coincided with the completion of this crucial process. During this time, ERC-3643 has been instrumental in tokenizing significant asset value and has garnered substantial community support, including the formation of a dedicated association. It’s concerning that Token Forge, as an association member and active participant, did not voice any concerns until now. This late-stage dissent appears disingenuous and seems to suggest an underlying agenda not aligned with the community-driven ethos of the ERC-3643 association.
4. Onchain Identity and Compliance: The pushback against on-chain identity in favor of wallet whitelisting underestimates the complexities of applying comprehensive compliance rules. On-chain identities are not just a feature; they are a necessary component for automating compliance on a public ledger, enabling a secure, efficient, and transparent system. Your proposal’s silence on this critical aspect leaves significant gaps in its applicability to real-world compliance needs.
5. Standard Justification and EIP-1 Principles: While your proposal claims to aim for minimal requirements and freedom of implementation, this intent is not mutually exclusive with what ERC-3643 provides. If the unique selling point of your standard is the addition of transaction metadata, then it should be presented as an extension or complement to ERC-3643, not as a standalone standard that duplicates existing functionality. Moreover, to align with EIP-1, it would be fitting to refactor your proposal to make it clear that it’s designed to interface with ERC-3643 tokens, thereby bringing value-add to the existing infrastructure rather than fracturing it.

In conclusion, while innovation and the introduction of new ideas are the bedrock of the Ethereum community, the fragmentation of standards without substantive or differentiated improvements goes against the grain of our collective goal. It would be more beneficial for the community to enhance existing standards and collaborate on shared objectives, rather than pursue parallel efforts that lead to unnecessary bifurcation.

We remain open to a constructive dialogue and hope that we can align our efforts to strengthen the Ethereum ecosystem as a united front.

---

**Joachim-Lebrun** (2023-11-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/markuskluge/48/16060_2.png) MarkusKluge:

> I agree with @moinlars . For example, ERC-3643 requires mandatory compatibility with ERC-20. The law, which was essentially the reason we built this EIP, introduces different legal statuses for securities in relation to their owners and owner types. Although there is still an open discussion about whether this must or should be implemented at the level of smart contracts, we want to keep the option open to utilize the possibilities offered by ERC-1155 and to map these different legal statuses via token IDs. We are currently working on another EIP that reflects this, based on the first EIP.
>
>
> This is just one reason why we decided to create a more open EIP, not forcing compatibility or integration with existing standards that could restrict flexibility in implementation.
> I really like the way ERC-3643 approaches the challenges of building compliant securities. But as I have already said, I feel the restrictions are too stringent. Looking forward to a fruitful discussion.

We welcome all voices in this discussion, recognizing that each perspective adds value to the debate on how we can best advance the Ethereum ecosystem. However, it’s crucial to maintain transparency about affiliations and to engage with the community in a manner that promotes trust and collective progress.

Regarding the points raised by [@moinlars](/u/moinlars):

The compatibility of ERC-3643 with ERC-20 is by design, to ensure a broad base of compatibility and to leverage the substantial infrastructure already developed around ERC-20 tokens. This does not preclude the use of ERC-1155 for specific use cases, but rather, it ensures that securities tokens can be integrated into the vast majority of existing wallets, exchanges, and other infrastructure without friction.

The concern about potential restrictions is noted. However, the design of ERC-3643 intentionally provides a balance between compliance with legal frameworks and the flexibility for innovation. The mandatory compatibility is not intended as a limitation but as a foundation upon which further innovations can be built, including those that cater to varying legal statuses of securities and their owners. It is a common platform from which we can extend and integrate additional features, such as those offered by ERC-1155, without reinventing the core functionalities each time.

ERC-3643 was conceived and has been iterated upon with broad community input and with an eye towards real-world application and legal compliance. It would be valuable to explore how your concerns about “restrictions” can be addressed through extensions or complementary standards, rather than a wholesale new EIP that risks fragmenting the community and diluting the robustness of our collective solutions.

To your latest point, the introduction of legal statuses and owner types is an intriguing direction and certainly warrants exploration. I would suggest that this exploration is done in the context of how it can enhance and interoperate with ERC-3643, which already has significant traction and industry support.

As a new participant in this forum, your engagement is appreciated, but I also encourage you to consider the broader context in which these standards operate. It is the interoperability, widespread adoption, and community consensus that will ultimately determine the success and utility of any standard.

Let’s aim for a synergistic approach that builds upon established work, enhancing and expanding it where necessary, rather than creating parallel tracks that may lead to inefficiencies and confusion in the market.

---

**MarkusKluge** (2023-11-05):

Thank you for pointing out the transparency of my role. I thought that the use of my real name, the fact that this name is listed as a co-author in the draft, and the use of the we-form in my post implicitly made my role transparent. I have added my role to the post to avoid further misunderstandings.

I understand the intention to create a standard that fits the current infrastructure. However, the currently available infrastructure only represents parts of the use cases of digital securities. In some use cases, the price of implementing a solution with unneeded compatibility may be too high and market participants may then tend towards another closed silo solution. This is to be avoided.

We certainly did not make our proposal to create inefficiency and uncertainty in the market. The willingness to discuss the concerns regarding the limitations mentioned is much appreciated.

Perhaps this discussion will help to further increase acceptance of the standards.

Let’s talk

---

**moinlars** (2023-11-06):

[@Joachim-Lebrun](/u/joachim-lebrun) It was neither our intention to draw on existing work without acknowledging it nor to take any credit for it. We’ve adapted the “Rationale” section to make it more transparent how the standard was created.

Nonetheless, I want to emphasize that I’m convinced that this proposal is by no means a mere copy of ERC-3643 and follows a distinct and unique approach.

I agree that both proposals have overlapping objectives and I’m happy to discuss how we can align our efforts.

---

**SamWilsn** (2024-01-12):

How does the `pause` function interact with the forced transfer family of functions? It sounds like pausing would prevent forced transfers, but I’m not sure that’s intended.

---

**SamWilsn** (2024-01-12):

`paperContractHash` is oddly specific. Would it maybe be more useful to use an ipfs content id?

---

**SamWilsn** (2024-01-12):

Generally speaking, we recommend not specifying functions that only the operator has access to. The prime example being `mint`/`burn` from ERC-20 tokens.

Since the operator will have deployed the contract, they’ll know how to interact with those operator-only functions. No one else needs to understand them.

This comment is directed at functions like `setMetaDataJSON` and `pauseTransfers`.

---

**moinlars** (2024-06-18):

Hi [@SamWilsn](/u/samwilsn), thanks for sharing your feedback ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

> How does the pause function interact with the forced transfer family of functions? It sounds like pausing would prevent forced transfers, but I’m not sure that’s intended.

Indeed, pausing transfers should not affect forced transfers. As both functionalities can be controlled by the operator, it would not make sense to restrict forced transfers on a paused token contract, I guess. What do you think?

---

**moinlars** (2024-06-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> paperContractHash is oddly specific. Would it maybe be more useful to use an ipfs content id?

So, the idea would be to upload the document to IPFS and replace the document hash with the content ID? Do you have a proposal on how to make it “protocol-agnostic” so that we don’t rely on the availability of IPFS protocol?

---

**moinlars** (2024-06-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> Generally speaking, we recommend not specifying functions that only the operator has access to. The prime example being mint/burn from ERC-20 tokens.
>
>
> Since the operator will have deployed the contract, they’ll know how to interact with those operator-only functions. No one else needs to understand them.
>
>
> This comment is directed at functions like setMetaDataJSON and pauseTransfers.

A core rationale of the standard was to also allow interoperability between operators so that if a operator fails to provide the service, another operator can step in with less effort. Do you think that might be enough reason to keep them specified. Also, as we’re on a public ledger I would not expect the smart contract code including the interface to be a secret.

---

**SamWilsn** (2024-06-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/moinlars/48/10847_2.png) moinlars:

> pausing transfers should not affect forced transfers.

You should clarify this in the document then.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/moinlars/48/10847_2.png) moinlars:

> So, the idea would be to upload the document to IPFS and replace the document hash with the content ID?

Pretty much, yes!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/moinlars/48/10847_2.png) moinlars:

> Do you have a proposal on how to make it “protocol-agnostic” so that we don’t rely on the availability of IPFS protocol?

The [IPFS CID](https://docs.ipfs.tech/concepts/content-addressing/) is a hash of the document, so even if IPFS ceases to exist, you can always use the CID to verify that a given file matches. The benefit of using a CID over a plain hash is that, if desired, you can upload/retrieve it.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/moinlars/48/10847_2.png) moinlars:

> A core rationale of the standard was to also allow interoperability between operators so that if a operator fails to provide the service, another operator can step in with less effort. Do you think that might be enough reason to keep them specified.

That is an excellent reason to keep them specified. Should make that apparent in the document, if it isn’t already.

---

**ivica** (2024-06-18):

[@MarkusKluge](/u/markuskluge) [@moinlars](/u/moinlars) Great to see this being published as ERC draft!

Some suggestions:

For better symmetry and readability

- rename destroyToken to terminate
- rename freezeTokens to freeze (you’re also not saying issueToken)
- rename unfreezeTokens to unfreeze (same reasons as above)

Remove getter/setter for paperContractHash and let it be part of metaDataJSON as “documentHash”. This way you can also keep it extensible and also add ipfs links or whatever, if needed.

“paperContractHash” also sounds a little bit weird.

Would the ERC need to specify what the json metadata should be?

Moreover, can you please elaborate more on how you would be using this ERC in combination with ERC-1155, especially in regard that you can have different tokenIds in ERC-1155.

PS. I am wondering why I can not find ERC-7551 on [eip.ethereum.org](http://eip.ethereum.org)?

---

**moinlars** (2024-06-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> The IPFS CID is a hash of the document, so even if IPFS ceases to exist, you can always use the CID to verify that a given file matches. The benefit of using a CID over a plain hash is that, if desired, you can upload/retrieve it.

I’m not very experienced with using IPFS. From a short look into the docs, I can see that [CIDs are hash digests where the input data is not only the hash but also IPFS related data](https://docs.ipfs.tech/concepts/content-addressing/#cids-are-not-file-hashes).

A paper contract hash is the checksum of the issuance conditions document. Most of the time this will be a PDF file. Maybe we can think in that direction to come up with a more specific name for it?

---

**moinlars** (2024-06-19):

Hi [@ivica](/u/ivica), thanks for taking the time to feedback ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ivica/48/12670_2.png) ivica:

> For better symmetry and readability
>
>
> rename destroyToken to terminate
> rename freezeTokens to freeze (you’re also not saying issueToken)
> rename unfreezeTokens to unfreeze (same reasons as above)

Some existing implementations and standards have functions that allow to freeze an account address, meaning any balance that currently exists or will be sent to the address. The idea was to make it clear that we really mean freezing some quantity of the token, let’s say 100 tokens and we’re not freezing the account address.

The same logic applies to `destroyTokens`. Here I would argue additionally that `terminate` may be misunderstood to terminate the smart contract as a whole.


*(10 more replies not shown)*
