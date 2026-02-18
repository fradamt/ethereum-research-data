---
source: magicians
topic_id: 14551
title: Numbered Accounts
author: dcposch
date: "2023-06-03"
category: EIPs > EIPs interfaces
tags: [erc, chain-id]
url: https://ethereum-magicians.org/t/numbered-accounts/14551
views: 793
likes: 2
posts_count: 1
---

# Numbered Accounts

# Tl;dr

This is a rough sketch of a new **address format** and a corresponding **wallet contract interface**.

It would, of course, interoperate with existing accounts. Wallets can opt in to the new address format to achieve a simplified user experience.

Pros of the new format:

- Minimalist. Numbered accounts that live on a single chain, optionally restricted to specific assets
- Cheap. 4337 contract wallet, but without having to deploy a separate contract for each user. Instead,  one “bank” contract supports many numbered accounts.
- Easy to write. Short number instead of long hex

# The problem

The semantics of an Ethereum account are maximalist, and can’t be restricted cleanly.

An account (regardless of whether it’s an EOA or a CREATE2 contract wallet):

- Exists, implicitly, on all EVM chains
- Can receive any asset, anywhere. No way to opt out.

**As a result, every wallet in practice needs to give users the ability to *send* any asset, on any chain.** Otherwise, some users will accidentally transfer non-supported assets into their account and be irate when they can’t get them back out. The minimum UX complexity for a wallet is therefore high.

This creates a user education and UX challenge. It’s hard for people to wrap their mind around the full scope of what an Ethereum account is. It’s also hard to display to a user, concisely, what their account contains.

Many UIs use centralized token lists to make the problem tractable, and as a mitigation against spam token airdrops.

**Traditional accounts are easier to explain.** What’s in a Chase checking account? A single balance, denominated in dollars. What’s in a Robinhood account? Publicly traded securities.

In each case, there’s a known universe of assets, easy to summarize in a sentence, each with a well-defined balance. Questions like “list everything in my account” and “what is the total value” have a tractable, finite answer.

Ethereum accounts currently contain an unbounded 2D grid of (chain x asset).

# Proposed solution

This is a rough sketch of a new **address format** and a corresponding **contract standard**.

### Numbered accounts each exist on a single chain

Optionally, they can also restrict which assets they can contain.

Numbered accounts are addressed by a “routing number” and “account number”, by analogy to traditional account.

Example: **`1001-123`** for routing 1001, account 123.

### Routing numbers are assigned by a singleton contract on mainnet

Let’s call it `RouteRegistry`. Each routing number points to a pair (chain ID, address) which is the “bank” contract for that routing number.

Each routing number also has an owner address. If the owner is set, then that owner can update the record, leaving open the possibility to migrate all accounts under that routing number to a different chain. If the owner is 0x0, then that routing number is immutable. The usual tradeoff between flexibility and governance risk applies.

(Finally, to support clean transaction histories, the RouteRegistry will enforce uniqueness of the reverse lookup. If a particular contract address was once registered as routing number 1001, it can never later be registered as a different number.)

### Bank contracts assign account numbers on the chosen chain

Each bank contract follows an interface along the following lines.

```auto
struct Account {
   /* Always nonzero. If account > 0, then addr must implement IBank. */
  address addr;
  /* Account number (positive), or 0 for standard Ethereum account. */
  uint256 account;
}

/** Each routing number points a bank contract. */
interface IBank {
  function hasAccount(uint256 account) external view returns (boolean);
  function canTransfer(address token) external view returns (boolean);
  function send(Account from, Account to, address token, IDsAndAmounts amounts, bytes auth) external;
  function receive(Account from, Account to, address token, IDsAndAmounts amounts) external;

  // Send and Receive events reporting (from, to, token, amount)
}
```

Let’s look at the three possible cases.

1. Transfer in (ethereum address to numbered account). Call receive on the recipient bank. The bank contract will call transferFrom on the token contract.
2. Transfer out (numbered account to ethereum address). Call send on the sender bank. to.account is 0. The bank will call transferFrom on the token contract, sending assets to to.addr. (The auth parameter contains bank-specific authentication to prove that the caller is allowed to spend from from.account.)
3. Transfer between numbered accounts. Call send on the sender bank. to.account is positive. The bank will call receive on the recipient bank, which will call transferFrom on the token contract. (The auth parameter works same as above.)

Individual banks are welcome to implement additional functionality, such as swaps. The standard only specifies transfers, since these must work uniformly across banks.

## Example

(Placeholder. I could put an example of how to implement a minimalist DaiBank, where each account has a balance denominated in DAI.)

## Numbered accounts, permits, and ERC-4337

Details TBD, but bank contracts should integrated with 4337 so that transfers can be sent as user ops.

Transfers between numbered accounts always run in a single transaction. Same with transfer out. As long as the token supports `Permit`, transfer in should run in a single transaction as well, and well-implemented wallets should be able to confirm them in a single user interaction.

## Assets supported

Which asset contracts are supported is up to each bank contract. A typical bank might support a single ERC20 (eg “DaiBank” for a payments wallet) or some combination of ERC20, ERC721, and ERC1155 standard contracts.

A bank can also support tokens that don’t implement any of those standards, like the CryptoPunk contract.

## UX implications

- Lets say 1001 is a DAI bank. It’s not possible to accidentally send your ape to 1001-123. It’s also not possible to accidentally transfer DAI to 1001-123 on the wrong chain.
- Typing in 1001-123, or reading it over the phone, is easier than a 40-character Ethereum address.
- If bank 1001 only supports a single asset, then you can display a complete summary of what account 123 contains in a single number, just like a fiat bank account.
 Difference of course is that it’s global and permissionless. The account inherits all of the nice properties of the underlying chain, just with intentionally reduced flexibility.
- If bank 1002 supports arbitrary assets, then you can still display a complete account summary from a single chain. An account has exactly, say, 2 RAI, not (1 RAI on mainnet + 2 on Arbitrum).
- Better (less scary) L2 support. Exchanges currently ask for both a destination address and chain when withdrawing. Then, if the chain is anything other than mainnet, they display a warning along the lines of “ensure your wallet is compatible with Optimism”. If a user enters a numbered account, the chain can be selected automatically (non-editable) and no warning is necessary.
- Better (less scary) sends. The contract spec allows a wallet or exchange to check that the destination account is valid and supports the asset you’re about to send.
