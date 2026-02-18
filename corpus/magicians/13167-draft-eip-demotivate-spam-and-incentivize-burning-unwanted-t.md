---
source: magicians
topic_id: 13167
title: "Draft EIP: Demotivate spam and incentivize burning unwanted tokens"
author: hackwithzach
date: "2023-03-04"
category: EIPs > EIPs core
tags: [erc, nft, erc-721, erc-20, burn]
url: https://ethereum-magicians.org/t/draft-eip-demotivate-spam-and-incentivize-burning-unwanted-tokens/13167
views: 1260
likes: 5
posts_count: 13
---

# Draft EIP: Demotivate spam and incentivize burning unwanted tokens

Hi Ethereum Magicians! Forgive me if this has been discussed before, but I wanted to surface a conversation on tokens to help better the Ethereum space.

With Lens Protocol, Disco, Account Abstraction, and innovations happening in the user experience on Ethereum, a new wave of web3 social is emerging. I think an important issue to address immediately is the possibility for bad actors to spam tokens to wallet addresses that hold significant value for members. As we use these decentralized identities in our day to day lives, we should have the right or be rewarded for removing unwanted token transfers into our wallet.

The solution / EIP I’m proposing is outlined below. Please let me know your thoughts!

```auto
EIP:
Title: Introducing a Token Minting Fee and Burn Incentive
Author:
Type: Standards Track
Category: ERC
Status: Draft
Created: March 4th, 2023
Requires:
Replaces:
```

## Abstract

This EIP proposes the introduction of a fee for minting new tokens on the Ethereum chain. The fee would be set at an amount that is sufficient to cover the gas cost of burning a token transaction. Any additional amount above the gas cost would be rewarded to the wallet holder that burns the token. The goal of this proposal is to demotivate spam and incentivize burning unwanted tokens, which can reduce the number of unnecessary tokens on the chain and improve its overall efficiency.

## Motivation

The Ethereum chain has seen a significant increase in the number of tokens being created, many of which are of low quality and have no real use case. This has led to an increase in spam and clutter on the chain, making it more difficult for users to find legitimate projects and transactions. By introducing a fee for minting tokens, we can discourage the creation of low-quality tokens and incentivize token holders to burn unwanted tokens, which can help to reduce the clutter on the chain and improve its overall performance.

## Specification

This EIP proposes the introduction of a fee for minting new tokens on the Ethereum chain. The fee would be set at an amount that is sufficient to cover the gas cost of burning a token transaction. Any additional amount above the gas cost would be rewarded to the wallet holder that burns the token. The fee would be paid in ETH or any other ERC-20 token as determined by the token issuer.

Token issuers would be required to set the minting fee for their token at the time of creation. The fee would be displayed on the token contract and would be visible to all users. The fee would be deducted automatically from the token issuer’s account at the time of minting.

Token holders would be able to burn unwanted tokens by sending them to a designated address. The address would be specified in the token contract and would be publicly visible. When a token is burned, the wallet holder would receive a reward equal to the amount of the minting fee, minus the gas cost of the transaction.

## Rationale

Introducing a fee for minting tokens can help to reduce the number of low-quality tokens on the Ethereum chain and incentivize token holders to burn unwanted tokens. This can lead to a more efficient and streamlined chain, making it easier for users to find legitimate projects and transactions.

By setting the fee at a level that covers the gas cost of burning a token transaction, we can ensure that token issuers are not discouraged from creating legitimate tokens. At the same time, by rewarding token holders for burning unwanted tokens, we can incentivize them to take an active role in maintaining the health and efficiency of the chain.

## Security Considerations

This proposal does not introduce any security risks to the Ethereum chain. The fee for minting tokens would be paid in ETH or any other ERC-20 token, and would be deducted automatically from the token issuer’s account at the time of minting. The reward for burning tokens would also be paid in the same currency, and would be sent to the wallet holder’s address upon completion of the burn transaction.

## References

- Ethereum Improvement Proposal 20 (ERC-20): Token Standard
- Ethereum Improvement Proposal 721 (ERC-721): Non-Fungible Token Standard

## Replies

**stevifi** (2023-03-05):

This is actually an issue for wallets to deal with, spam tokens should be filter by the wallets themselves.

A token designed for spam will not voluntarily adopt an EIP who’s purpose is to prevent spam

Making (deploying) a token is no different than deploying any other smart contract so this design you mention seems hard to enforce.

---

**ligi** (2023-03-06):

The EIP should describe how it should work. Currently it only describes the goal - but not how this goal could be achieved. I cannot see any practical approach how this could be done.

---

**stoicdev0** (2023-03-06):

It feels like this could only be achieved by some extension of 721, but being an extension it would be optional so spammers would just not do it. Unless you’re suggesting some change in the core which also doesn’t seem viable to be.

---

**hackwithzach** (2023-03-07):

We would need to modify the EVM and the Ethereum protocol to recognize the zero address `0x0000000000000000000000000000000000000000`, and allow transactions to be sent to these addresses without requiring gas fees to be paid:

1. Modify the EVM to recognize the zero address as a special address that can receive transactions without requiring gas fees to be paid.
2. Modify the Ethereum protocol to include a new consensus rule that requires transactions sent to the zero address to be processed without requiring gas fees to be paid.
3. When a user initiates a burning/transfer transaction to the zero address, the EVM recognizes the zero address and processes the transaction without requiring gas fees to be paid.
4. The transaction is confirmed on the Ethereum network and the specified tokens are burned/transferred to the zero address.

By implementing this solution at the EVM/Ethereum protocol level, burning/transferring tokens to the zero address `0x0000000000000000000000000000000000000000` would become gasless, regardless of the smart contract used to initiate the transaction.

An example I can think of is:

1. Modify the EVM opcode for CALL to recognize the zero address as a special case and bypass the gas cost calculation.

goCopy code

```auto
func opCall(gaspool *core.GasPool, contract *state.Contract, input []byte, value *big.Int) ([]byte, error) {
    // Check if the contract address is the zero address.
    if contract.Address() == common.Address{} {
        // Do not consume gas for zero address calls.
        gaspool.ConsumeGas(0, "CALL to zero address")
        return nil, nil
    }

    // Continue with normal gas cost calculation for non-zero address calls.
    ...
}
```

1. Modify the Ethereum protocol to include a new consensus rule that allows transactions to the zero address to be processed without requiring gas fees to be paid.

goCopy code

```auto
// ApplyTransaction attempts to apply a transaction to the current state of the blockchain.
func ApplyTransaction(tx *types.Transaction, state *state.StateDB, env *EVMEnv) (types.Receipt, error) {
    // Check if the recipient address is the zero address.
    if tx.To() == common.Address{} {
        // Do not require gas for zero address transactions.
        env.gas = new(big.Int).SetUint64(0)
    }

    // Continue with normal gas cost calculation for non-zero address transactions.
    ...
}
```

With these modifications, any transfer or burn transaction to the zero address would become gasless. For example, let’s say we have a token contract with the function `burn(address,uint256)` which allows a user to burn a specific amount of tokens by sending them to the zero address. With the modifications above, a gasless burn transaction would look like this:

solidityCopy code

```auto
function burn(address to, uint256 amount) public {
    // Transfer the tokens to the zero address without requiring gas fees.
    to.call.value(amount)("");

    // Emit a Burn event to record the transaction.
    emit Burn(msg.sender, amount);
}
```

In this example, the `to.call.value(amount)("")` line would transfer the specified amount of tokens to the zero address without requiring gas fees to be paid.

---

**hackwithzach** (2023-03-07):

While wallets can implement filters to prevent spam tokens from being displayed, it is still important to address the root cause of the issue, which is the ability for spammers to create and deploy these tokens in the first place.

Enforcing a solution at the Ethereum protocol level, such as implementing a gasless transfer/burn to the zero address, can provide a more permanent and effective solution. While it may not completely prevent all spam tokens from being deployed, it can make it significantly more difficult for spammers to profit from them.

Additionally, it is important to note that a token designed for spam may not voluntarily adopt an EIP to prevent spam. However, if a hard fork were to be implemented at the Ethereum protocol level, this would become a mandatory requirement for all tokens on the new chain.

---

**hackwithzach** (2023-03-07):

While a new extension or standard, such as an extension of ERC-721, could be helpful in preventing spam tokens, it is not a complete solution on its own. As you pointed out, it would be optional for token creators and therefore spammers could simply choose not to adopt it.

Implementing a gasless transfer/burn to the null address, however, would be a more effective solution. By making it more expensive to transfer spam tokens, spammers would be less incentivized to create and deploy them in the first place. Additionally, this solution could be enforced at the protocol level without requiring any changes to individual token contracts, making it more feasible to implement.

While a new extension or standard could be helpful in preventing spam tokens, it is not a complete solution on its own. Implementing a gasless transfer/burn to the null address would be a more effective and feasible solution that could be enforced at the protocol level.

---

**ligi** (2023-03-07):

This is not possible on multiple levels:

- allowing a tx that does not cost anything opens DOS Vectors and people can bloat the state - also why would miners even include such a TX - would really not work like this
- to send a token to the zero address you do not interact with the “contract at the zero address” (there is no contract there) - the zero address for such a burn would just be a parameter to a contract - so it would also not work from this angle.

---

**ligi** (2023-03-07):

So I really do not see any way to do this on the protocol level - it needs to be done on layers above. Same as with spam in emails - also not handled on the protocol level.

---

**hackwithzach** (2023-03-07):

It’s true that allowing transactions that do not cost anything can open up DOS vectors and potentially bloat the state, which is a valid concern.

However, it’s important to note that implementing a gasless transfer/burn to the null address can be done in a way that doesn’t compromise the security of the network. For example, the gasless transfer/burn could be limited to a certain number of transactions per block, or it could be subject to a minimum gas limit to prevent spam.

Also it would require a token to exist in a wallet for the gasless burn function to execute, making it still difficult and costly for a DOS attack.

As for why miners would include such a transaction, it’s possible that they could be incentivized to do so if there is demand from users for this functionality. Additionally, as I mentioned earlier, implementing this feature could be enforced at the protocol level, meaning that miners would be required to include these transactions as part of the consensus rules.

Regarding the parameterization of the null address, it’s true that the null address itself is not a smart contract and thus cannot be interacted with directly. However, it’s still possible to pass the null address as a parameter to a contract function that would implement the transfer/burn functionality. This approach would allow for a gasless transfer/burn without requiring any changes to the null address itself.

---

**ligi** (2023-03-08):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/h/b2d939/48.png) hackwithzach:

> This approach would allow for a gasless transfer/burn without requiring any changes to the null address itself.

no - it would not allow this

---

**asdnlasdlkj** (2023-03-08):

This is a terrible idea, just give it up dude. Please learn more about Ethereum before suggesting any further ideas.

---

**LucasGrasso** (2023-03-11):

Hello there. Yes, I see the issue that you’re presenting. I’ve developed a SBT token standard and it aids this with a “double-signature” feature. You have to “accept”/“claim” the token to it be added to your wallet.



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lucasgrasso/48/6893_2.png)

      [ERC-5516: Soulbound, Multi Token Standard](https://ethereum-magicians.org/t/eip-5516-soulbound-multi-token-standard/10485) [ERCs](/c/ercs/57)




> ERC5516
> Co-Authored with: @MatiArazi
>
> This is the discussion thread for EIP-5516 (Currently in Review):
> This EIP proposes a standard interface for non-fungible double signature Soulbound multi-tokens. Previous account-bound token standards face the issue of users losing their account keys or having them rotated, thereby losing their tokens in the process. This EIP provides a solution to this issue that allows for the recycling of SBTs.
> This EIP was inspired by the main characteristics of the E…

