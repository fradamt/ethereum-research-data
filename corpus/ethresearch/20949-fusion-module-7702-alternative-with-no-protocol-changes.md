---
source: ethresearch
topic_id: 20949
title: Fusion Module - 7702 alternative with no protocol changes
author: fichiokaku
date: "2024-11-08"
category: Applications
tags: [account-abstraction]
url: https://ethresear.ch/t/fusion-module-7702-alternative-with-no-protocol-changes/20949
views: 1004
likes: 6
posts_count: 5
---

# Fusion Module - 7702 alternative with no protocol changes

During the development and R&D of [Modular Execution Environments and Supertransactions](https://www.biconomy.io/post/modular-execution-environment-supertransactions), we uncovered an intriguing mechanism that enables Externally Owned Accounts (EOAs) to function similarly to smart accounts. This innovation can be implemented immediately, without waiting for the 7702 Pectra protocol upgrade whilst at same time being compatible. We’ve conducted testing and developed a proof-of-concept. Let’s delve into the details!

## Background

The blockchain community has engaged in extensive discussions, particularly within the Chain Abstraction and Account Abstraction groups, regarding the role of smart account models in the ecosystem and the potential impact of EIP-7702 on user experience.

EOAs remain a fundamental element in blockchain infrastructure and while they represent one of the most prevalent wallet types in current use, EOAs lack several essential features that modern Web3 users consider standard requirements for day-to-day operations.

### Motivation

Smart Contract Accounts (SCAs) represent a significant advancement in blockchain wallet technology, offering programmable functionality that extends far beyond the capabilities of traditional EOAs. The enhanced feature set of SCAs includes:

- Transaction batching
- Spending limits
- Account recovery mechanisms
- Gas fee abstraction
- Cross-chain interoperability
- Automation and scheduled transactions

### Challenges

The current implementation of SCAs presents several operational challenges:

First, the requirement to transfer assets from an EOA to utilize an SCA creates unnecessary friction in the user experience and leads to liquidity fragmentation across accounts.

Second, the proliferation of different smart account providers across Apps fragments the unified wallet experience users have come to expect. This stands in contrast to the traditional EOA model, where users maintain a single wallet address and consolidated balance across multiple blockchain networks.

As illustrated below, the user would have to sign twice to fund their smart account and then start interacting with it. And to make it even worse, the first signature forces user to pay gas themselves, meaning they need to own some native coin. The common 2-step SCA onboarding flow is shown below:

[![Two user signatures, shown in blue, are required for usingthe smart accoun for the first time.](https://ethresear.ch/uploads/default/optimized/3X/0/0/001321d7cef3b7f46547ba624b0d2f7972ba3202_2_669x500.png)test1002×748 42.1 KB](https://ethresear.ch/uploads/default/001321d7cef3b7f46547ba624b0d2f7972ba3202)

*Two user signatures, shown in blue, are required for usingthe smart accoun for the first time.*

Furthermore, the implementation of embedded SCAs within dApps introduces additional complexity to asset management. Users must track and manage assets on an application-by-application basis, while placing trust in each application to maintain accessible interfaces for manual asset management.

### Solution - Fusing EOA & SCA!

Our innovation, which we’ll present shortly, introduces a mechanism that can be utilized today to achieve a virtual merging of EOA and SCA into a single entity. This is accomplished without requiring users to explicitly upgrade their EOA or manually transfer funds to a new address. This breakthrough approach fundamentally resolves the fragmentation, complexity, and user experience challenges that have historically impeded SCA adoption, while maintaining backward compatibility with existing infrastructure.

## EOA Fused

We’ve developed a method that allows users to utilize their EOAs as if they were interacting with a smart account. This is achieved while only requiring a single signature for each action, eliminating the need for manual pre-activations, upgrades, or fund transfers to new addresses.

Our proposal involves precalculating a Smart Account address for each EOA and utilizing it as a *companion* account. This approach builds upon the established mechanism for generating ERC4337 accounts. The innovation in our solution lies in the ability to transfer tokens to the companion Smart Contract Account *and* provide bundlers with all necessary additional instructions (UserOps) to be executed - all with a single signature.

Furthermore, when a user first interacts with our system, the smart contract account is deployed on-demand (lazy deployment), ensuring that even the initial interaction only requires one user signature.

Key concepts of our approach include:

1. Users need not be aware of their smart account wallet.
2. Users continue to use their EOA as their primary wallet, eliminating the need to explicitly move funds elsewhere.
3. Users never grant access to their entire EOA portfolio to execute complex operations on a small amount of tokens they hold.
4. Users sign ONCE for every interaction, providing a full EOA-like experience while utilizing funds from their EOA as if they were directly using the smart account.

The companion smart account processes complex user requests that would not be possible with a standard EOA alone. These include batching multiple operations, interacting with several DeFi protocols simultaneously, and distributing assets to multiple recipients in a single transaction.

### Live Demo

[Demo video](https://x.com/biconomy/status/1854874841465381184?s=46&t=uuLQATgesJ_cHLXm65ix5QP)

### Technical Implementation

*…how is it possible to use EOA as if it was an SCA, before Pectra upgrade?*

We’ve leveraged the fact that appending arbitrary bytes to a valid EVM transaction maintains its validity while including all the appended data on-chain.

For instance, if we’re executing a standard ERC20 transfer function:

```auto
transfer(address to, uint256 amount)
```

We would typically encode this function as:

```auto
callData = abi.encode("transfer", [ address, amount ])
```

resulting in a transaction data structure:

```auto
tx = {
	to: "0xtokenaddress",
	value: 0,
	data: callData
}
```

However, we can append any arbitrary data to the callData field, and the transaction remains valid. The USDC transfer will execute correctly, while the additional appended hex data is simply ignored by the EVM.

This is a fundamental aspect of EVM design and how function selectors operate. For illustration, consider this [test USDC transfer on Sepolia](https://sepolia.etherscan.io/tx/0xb25e84d0530e30fccd47ef82e08532927f727dc8093c2682682501459b971ad8). The transaction transferred 1 USDC, but examining the input data field (viewed as UTF-8) reveals an additional message (image below).

[![Appending ASCII text to a valid ERC20 transaction.](https://ethresear.ch/uploads/default/optimized/3X/d/4/d44022dce5256a8247934b5acedd38258c47c766_2_690x431.jpeg)Appending ASCII text to a valid ERC20 transaction.1445×903 115 KB](https://ethresear.ch/uploads/default/d44022dce5256a8247934b5acedd38258c47c766)

*Appending ASCII text to a valid ERC20 transaction.*

An important consideration is that the user’s signature covers the entire transaction, including all appended extra data. This approach allows us to execute multiple actions simultaneously:

1. Transfer funds (ETH or other ERC-20 tokens) from an EOA to a new address.
2. Include extra data in this action, which is part of the transaction fully signed by the EOA and verifiable on-chain. For example, this extra data could be the UserOp(s) hash to be executed by bundlers.

By setting the destination of transferred funds to the user’s smart account address and including extra data (e.g., a userOp hash for operations to execute on the smart account), we achieve both actions with a single signature.

[![Fusing EOA with companion SCA bundles both deposit and execute operations into a single user signature shown in blue.](https://ethresear.ch/uploads/default/optimized/3X/5/8/5898b020bd637d123be31df4ea4318ddac0f94f5_2_690x418.png)Fusing EOA with companion SCA bundles both deposit and execute operations into a single user signature shown in blue.937×568 45.8 KB](https://ethresear.ch/uploads/default/5898b020bd637d123be31df4ea4318ddac0f94f5)

*Fusing EOA with companion SCA bundles both deposit and execute operations into a single user signature shown in blue.*

The only requirement for this to function is that the user’s companion smart account contains a module capable of verifying a userOp given the fully signed & serialized EVM transactions - which we have developed.

## Fusion Module (7579)

The [Fusion Module](https://github.com/0xPolycode/mee-contracts/blob/901a13962f3becc0afe90c61f720fc6f02464ef8/contracts/validators/FusionValidator.sol) is a standardized 7579 smart account module capable of validating userOps not only by validating userOpHash signatures but also by validating userOps given the fully signed and serialized EVM transaction.

The module maintains universal compatibility with existing ERC-7579 smart account providers while introducing enhanced validation mechanisms, as demonstrated in our reference implementation.

[![Fusion Module](https://ethresear.ch/uploads/default/original/3X/4/0/40fe4c193681061f3bc16d33ba70388cad46bb09.png)Fusion Module581×401 16.3 KB](https://ethresear.ch/uploads/default/40fe4c193681061f3bc16d33ba70388cad46bb09)

When processing a signed EVM transaction as userOp signature, the module executes the following validation sequence:

1. Transaction Parsing
Deconstructs the signed EVM transaction into its constituent components
2. Cryptographic Verification
Performs cryptographic recovery of the transaction signer and validates against the smart account owner’s signature
3. Data Extraction
Retrieves extraData parameters from the transaction data field
4. Hash Verification
Validates the correlation between userOp hash and extraData field contents

Upon successful completion of all validation checks, the userOp achieves on-chain execution eligibility, permitting execution by any entity willing to pay for gas costs.

By utilizing this standardized module, we maintain compatibility with the 4337 infrastructure and enable any smart account provider to implement one-click onboarding and execution, providing users with an experience akin to direct EOA interaction.

## Infrastructure for Fusion Modules

*… or, who’s paying for gas?*

When a user executes an on-chain transaction that approves a userOp, there needs to be an entity willing to submit that userOp to the blockchain, knowing it’s now authorized and ready for execution. This entity must also have a mechanism to collect payment from the user for processing their complex request initiated from the EOA.

The current 4337 infrastructure can’t handle this efficiently due to limitations in how paymasters and bundlers are configured. The existing system expects users to either:

1. Have native coins pre-staked in the EntryPoint contract
2. Receive sponsorship from a paymaster for their operation

[![Regular 4337 bundler will reject companion userOp if funds are on the EOA - bundler doesn’t know EOA & SCA are companions!](https://ethresear.ch/uploads/default/optimized/3X/9/8/988c42cf30c080899e8ca516dcdf1c0d79c90c7a_2_690x452.png)Regular 4337 bundler will reject companion userOp if funds are on the EOA - bundler doesn’t know EOA & SCA are companions!887×582 42 KB](https://ethresear.ch/uploads/default/988c42cf30c080899e8ca516dcdf1c0d79c90c7a)

*Regular 4337 bundler will reject companion userOp if funds are on the EOA - bundler doesn’t know EOA & SCA are companions!*

Neither option works effectively for Fusion because bundlers and/or paymasters aren’t aware that the companion SCA has got the EOA address linked to it - who’s funds could be used for paying for fees and onboarding assets.

On the other hand, user shouldn’t need to manually stake ETH or fund their SCA with paymaster-accepted tokens - after all, we’re aiming for seamless user experience.

This is where **Modular Execution Environments (MEE)** become crucial. Fusion Modules are integrated as first-class citizens within the MEE stack. The MEE infrastructure, which is briefly introduced [here](https://www.biconomy.io/post/modular-execution-environment-supertransactions), enables developers to build applications without concerning themselves with the complexities of transaction execution, whether across one chain or many.

MEE stack supports diverse gas payment models, including scenarios where Fusion Module manages EOA assets through companion SCA accounts.

Rather than standard blockchain transactions, at the heart of MEE, lies a new primitive called S**upertransactions**. Supertransactions can contain multiple userOps that manage a single SCA, and every Supertransaction is uniquely identified by its hash. This architecture aligns perfectly with the Fusion Modules, enabling users to execute complex cross-chain interactions by signing one root Supertransaction hash. For example, users can sign once to approve Supertransaction which:

1. Transfers USDC from their EOA to SCA
2. Transfers a portion of USDC from the SCA to the MEE Node (as gas payment)
3. Swaps remaining USDC for ETH
4. Bridges ETH to another chain and transfer it back to the user’s EOA

These and many other workflows become one-click experiences through the EOA+SCA pass-through model.

To illustrate: consider a user leveraging their EOA as if it were an SCA, without needing to know about the SCA’s existence. They can execute cross-chain swaps, directly approving and spending funds from their EOA, while companion SCA accounts handle the complex operations across multiple chains behind the scenes. The transaction lifecycle of such an operation is laid out below:

[![Single signature user interaction is again shown in blue - where user signed one EVM transaction to both fund their companion SCA AND execute multiple userOps once funded.](https://ethresear.ch/uploads/default/optimized/3X/8/9/8990a9f0e3cccb3c3256b6d1ae2c83eaf4f92f63_2_205x500.png)Single signature user interaction is again shown in blue - where user signed one EVM transaction to both fund their companion SCA AND execute multiple userOps once funded.1137×2766 353 KB](https://ethresear.ch/uploads/default/8990a9f0e3cccb3c3256b6d1ae2c83eaf4f92f63)

*Single signature user interaction is again shown in blue - where user signed one EVM transaction to both fund their companion SCA AND execute multiple userOps once funded.*

After the dApp prepares the Supertransaction, users only need to sign a single ERC20 transfer transaction (highlighted in blue in the diagram above). The MEE stack then handles all operation orchestration and execution across different blockchain networks. Users simply see the end result: the received asset credited to their EOA on the destination chain.

## Advanced Signing Schemes

The upgrade process described above enables an EOA to gain SCA capabilities. However, users must still maintain a balance of native coins in their EOA to execute Supertransactions with a single signature. This limitation stems from the core design of the EVM, where gas fees must be paid from the public address associated with the transaction-signing private key.

However, there’s an interesting workaround. Through extensive exploration of different approaches to appending Supertransaction hash, we’ve discovered several alternative methods that allow users to spend assets from their EOA without paying gas fees directly.

### ERC20Permit (Gasless EOA)

We leverage the ERC20Permit standard for supported tokens (such as USDC) to deliver a seamless, gasless experience where EOAs can execute Supertransactions without even having any ETH on their wallet, while still requiring only one off-chain singature!

ERC20Permit standard allows EOAs to approve spending of the tokens off-chain, by only signing an off-chain message of the following structure:

```auto
PermitMessage = {
	owner,
	spender,
	amount,
	nonce,
	deadline,
};
```

Since the **deadline** parameter is already validated through the smart account/ERC-4337 model during userOp validation and execution (via validAfter and validUntil fields), we can repurpose it as a data carrier. This field stores the Supertransaction hash that fully describes the companion SCA operations that will be approved with the signed Permit Message. The deadline field’s uint256 type conveniently matches bytes32, allowing us to accomplish two objectives with a single off-chain signature:

1. Authorize the smart account to spend ERC20 assets by setting the spender address to be equal to the user’s companion SCA address (limited by the amount parameter) - which is what the ERC20Permit standard enables.
2. Approve smart account operations that can use up to the specified amount of funds from the EOA by setting the deadline value to the given Supertransaction hash.

When using the ERC20Permit signature, Fusion Module SCA module must:

1. Parse the ERC20Permit signature
2. Call the token’s permit() function when necessary
3. Execute the operations defined in the userOp - transferring funds from EOA to SCA and performing any additional specified actions

The paymaster can handle gas fees conventionally, deducting them from the same tokens transferred from EOA to SCA. Importantly, all operations occur effectively as a single atomic step - the user signs once, and this signature covers both gas payment and all user-defined actions.

As an example: let’s look at the example where user wants to transfer USDC from their EOA to some other address, but has no native coin on their wallet. In this case, they could leverage Fusion Module with the MEE stack and perform this operation with a single off-chain signature. The transaction lifecycle of such an operation is laid out below:

[![Single signature user interaction show in blue - where user signed an off-chain ERC20Permit message to both fund their SCA in a gasless way, and then execute userOp once funded.](https://ethresear.ch/uploads/default/optimized/3X/d/e/de3f9e4a5f6f2db10f250cd083176fe7f11f1887_2_259x500.png)Single signature user interaction show in blue - where user signed an off-chain ERC20Permit message to both fund their SCA in a gasless way, and then execute userOp once funded.1137×2156 260 KB](https://ethresear.ch/uploads/default/de3f9e4a5f6f2db10f250cd083176fe7f11f1887)

*Single signature user interaction show in blue - where user signed an off-chain ERC20Permit message to both fund their SCA in a gasless way, and then execute userOp once funded.*

The only interaction performed by the user is highlighted in blue color in flow from above. This means the EOA still feels like an EOA while more complex flow is being approved and executed by the MEE stack.

### Cross-chain Intent Signature (ERC-7683)

Another way of fusing EOA with a companion SCA is by packaging Supertransaction hash together with a signed cross-chain intent which is defined by ERC-7683 standard to have the following off-chain message structure:

```auto
/// @title CrossChainOrder type
/// @notice Standard order struct to be signed by swappers, disseminated to fillers, and submitted to settlement contracts
struct CrossChainOrder {
	/// @dev The contract address that the order is meant to be settled by.
	/// Fillers send this order to this contract address on the origin chain
	address settlementContract;
	/// @dev The address of the user who is initiating the swap,
	/// whose input tokens will be taken and escrowed
	address swapper;
	/// @dev Nonce to be used as replay protection for the order
	uint256 nonce;
	/// @dev The chainId of the origin chain
	uint32 originChainId;
	/// @dev The timestamp by which the order must be initiated
	uint32 initiateDeadline;
	/// @dev The timestamp by which the order must be filled on the destination chain
	uint32 fillDeadline;
	/// @dev Arbitrary implementation-specific data
	/// Can be used to define tokens, amounts, destination chains, fees, settlement parameters,
	/// or any other order-type specific information
	bytes orderData;
}
```

By using the same approach as with the ERC20Permit, we can store the Supertransaction hash inside the `bytes orderData` field and have the signed off-chain intent be used for both the actual intent settlement and the subsequent operations performed once the intent has been settled.

By making Fusion Module compatible with the ERC-7683 standard, we’ve created a powerful synergy that bridges traditional smart contract interactions with intent-based systems. This integration enables users to sign a single intent that can both settle cross-chain operations and trigger complex subsequent actions across multiple chains. The result is a more streamlined, user-friendly experience that maintains the security and flexibility of both systems while significantly reducing complexity for end users and developers alike.

## Implications for Smart Accounts Today

The signature schemes described above demonstrate how single-signature onboarding enables users to interact exclusively with their EOA while utilizing Smart Accounts as a pass-through mechanism.

This architecture enhances the user experience for smart accounts broadly, even when they serve as primary accounts, by enabling one-signature onboarding of EOA assets and operation execution. In essence, the smart account address becomes a true extension of the EOA - any asset in the EOA becomes seamlessly accessible through the Smart Account address.

Our Fusion Module validator currently supports three signature schemes:

1. Plain userOpHash signature
2. Signed EVM transaction signature
3. Signed ERC20Permit message signature

The plain userOpHash signature maintains backwards compatibility, allowing the SCA to work with existing 4337 infrastructure, including bundlers and paymasters processing userOps. The EVM and ERC20Permit schemes extend this functionality, enabling the same SCA to act as a companion account and support Fusion Transactions.

We’ve made the module implementation publicly available in our [GitHub repository.](https://github.com/0xPolycode/mee-contracts/blob/901a13962f3becc0afe90c61f720fc6f02464ef8/contracts/validators/FusionValidator.sol) Through our collaboration with the Rhinestone team, we’re working to have the standardized ERC-7579 module audited and published in the whitelisted modules repository, making it accessible to all smart account providers.

Integration of these modules is straightforward, varying based on the dApp’s specific needs. Developers simply need to modify the userOp signature field in their frontend to enable single-signature EOA interactions that function like native smart account operations.

## 7702 & Fusion - Different Approaches to the Same Problem

We propose this model as a solution that’s implementable today, without waiting for the Pectra upgrade, while supporting almost all features that 7702 will enable as well as being compatible with each other.

There are slight differences in capabilities between these models. Here’s a comparison of the pros and cons:

| 7702 | Fusion |
| --- | --- |
| Converts an EOA to SCA (code gets an access to an EOA in full) | Keeps EOA & SCA separated. |
| Requires an initial signature to activate SCA. | Works immediately - first signature for first action. |
| Supports spending multiple tokens from EOA at once. | Supports spending one token at a time from an EOA. |
| Supports gasless EOA transactions for any token. | Supports spending gasless transactions for ERC20Permit tokens. |
| Always relatively cheap (code is already deployed). | Initially expensive (SCA deployment) and then cheap for subsequent actions. |
| Doesn’t support single-signature multichain operations. | Supports single-signature multichain operations. |

![:sparkle:](https://ethresear.ch/images/emoji/facebook_messenger/sparkle.png?v=14) indicates an advantage over ![:red_circle:](https://ethresear.ch/images/emoji/facebook_messenger/red_circle.png?v=14) according to our assessment.

![:man_shrugging:t2:](https://ethresear.ch/images/emoji/facebook_messenger/man_shrugging/2.png?v=14) indicates: “Uncertain, further testing required”

Evidently, some actions are only possible with 7702, while others can only be performed using the Fusion Module approach. However, at a high level, both approaches address the same issue - how to safely enable EOA to have a SCA functionality.

Importantly, both models are forward-compatible with the general AA roadmap.

It’s often noted that 7702 will enable a gradual transition towards a fully account-abstracted future, as users can upgrade to increasingly complex account implementations on-the-fly.

7702 and the Fusion module differ in that Fusion module maintain separate account spaces: the EOA remains an EOA, while the SCA exists as a companion account, used only to spend funds that the user explicitly approves at the moment of execution.

Conversely, 7702 fully converts the EOA into an SCA - a stateful change. The EOA remains upgraded and points to an SCA implementation until an upgrade to a new account implementation is executed.

While both approaches have their merits and enable EOA accounts to function like SCAs, Fusion Modules allow users to switch between implementations on every request, eliminating the need to store the active implementation.

They can be viewed as a pathway to adopting smart accounts by enabling:

1. Level 1 adoption: Using SCAs as a pass-through only - retaining assets in the EOA unless necessary, and transferring only what’s required to process the request
2. Level 2 adoption: Using SCAs as the primary wallet and onboarding funds by bundling the deposit transaction with the first userOp

## Conclusion

The Fusion Module is a step forward in web3 account evolution, offering immediate benefits while staying compatible with future upgrades.

### Immediate Benefits

- Users can start using smart account features today
- No need to wait for protocol upgrades
- Simple one-signature experience
- Works with existing infrastructure

### Future Compatibility

The Fusion Module is designed to work alongside EIP-7702 when it launches. While 7702 will transform EOAs into SCAs directly, Fusion Module offers a complementary approach by keeping EOAs and SCAs separate but connected. This means:

1. Users can start with Fusion Module today and seamlessly transition to 7702 when ready
2. Projects can build with Fusion Module now, knowing their implementations will remain valid post-7702
3. Some features unique to Fusion (like single-signature multichain operations) will complement 7702’s capabilities

### Path Forward

We see Fusion Module as an important bridge to the future of account abstraction. It enables immediate adoption of smart account features while the ecosystem continues to evolve. Whether users eventually choose to fully upgrade their EOAs with 7702 or continue using the Fusion Module approach, they’ll have the flexibility to choose what works best for their needs.

The module is open source and ready for integration. We invite developers to try it out and help shape the future of wallet interactions in Web3. If you’d like  to enable smart contract capabilities on the EOA for your dapp or wallet, or just test it out, feel free to [reach out here](https://hlp8w9pp2h3.typeform.com/biconomy?typeform-source=ethresearch) and we’ll help!

## Replies

**Quazia** (2024-11-08):

Super interesting proposal! Makes sense but what keeps the MEE honest? Also can you break down what limitation prevents multi token transfers?

It seems messy and error prone to have to support both approaches long term.

---

**fichiokaku** (2024-11-09):

Thanks!

MEE is built as a p2p network of nodes that executes users’ Supertransactions when explicitly approved. The security model has been simplified to only require verification of user approvals on-chain via smart contract accounts, ensuring MEE cannot access user funds under any circumstances.

The main consideration is uptime and reliability, which is why the MEE network implements crypto-economic guarantees. Nodes performing the core execution work can be slashed if they fail to deliver their committed services.

Regarding multi-token transfers, EOAs are limited to spending one token at a time, whether using ERC20Permit off-chain message approvals or on-chain ERC20 transfer operations. This is an inherent limitation if we want to maintain a single user signature per operation. However, since most on-chain activities typically involve spending only one asset from your wallet, our approach covers a significant portion of use cases.

As for EIP-7702 and the two different standards - they complement each other by enabling different features. For instance, you could use an EOA with MEE as if it were an SCA from day one, without requiring specific upgrade approvals from the user as needed with 7702. There’s no additional overhead in maintaining compatibility between this proposal and 7702, as both 7702 and Fusion can utilize the same smart contract account implementation deployed on-chain.

The choice ultimately lies with the user: do you want to fully upgrade your EOA and let code manage your wallet (7702), or would you prefer to use SCA features while keeping your EOA isolated and maintaining precise control over asset spending (Fusion)?

---

**makoto** (2024-11-20):

Hi. Can you also apply for non asset transferring purpose such as SCA updating the ENS record while EOA still owning the name (in other words, no need to transfer ENS name asset to the companion SCA)?

---

**fichiokaku** (2024-11-20):

Yes! As you know, there are two key entities in ENS:

- resolver
- owner

The resolver determines what address the ENS name actually points to, while the owner has administrative control over the domain, including the ability to change the resolution settings and manage other aspects.

If you set the **owner** to a companion Smart Contract Account (SCA), your externally owned account (EOA) can still be the resolved address for the .eth name. This setup provides the flexibility of having the companion SCA manage the domain while enjoying all the benefits of Modular Execution Environment (MEE), such as gas-abstracted and chain-abstracted transactions.

