---
source: magicians
topic_id: 20896
title: Rollback tokens - a patch to unauthorized erc20 transfers
author: 0xRobinR
date: "2024-08-26"
category: Uncategorized
tags: [erc, token, wallet, erc-20]
url: https://ethereum-magicians.org/t/rollback-tokens-a-patch-to-unauthorized-erc20-transfers/20896
views: 175
likes: 2
posts_count: 7
---

# Rollback tokens - a patch to unauthorized erc20 transfers

> this discussion focuses on the very basic component of every hack stack, erc20 token

**a** rollback token gives an address or a contract a time period to roll back an erc20 transaction, if the transaction is not rolled back within the time period, the transaction is considered valid and cannot be rolled back.

one of the main advantages of using the rollback token standard in cold wallets or long-term asset holding wallets is the added layer of security it provides without compromising accessibility. cold wallets are typically used to store large amounts of cryptocurrency securely over long periods, with minimal interaction with the blockchain.

by incorporating the rollback feature, users gain the ability to reverse any unauthorized transactions within a set time frame, significantly reducing the risk of permanent loss due to hacks or mistakes. this is particularly valuable for long-term holders who may not frequently monitor their wallets.

the rollback token ensures that even if a cold wallet is compromised, the owner has a window of opportunity to reclaim their assets, making it an ideal solution for safeguarding long-term investments. this mechanism can offer peace of mind to asset holders, knowing that their funds are protected against unforeseen security breaches without needing to actively manage their wallets on a day-to-day basis.

the rollback token standard integrates zero-knowledge proofs, specifically zk-STARKs, to enhance security and privacy in reversing compromised transactions. by using zk-STARKs, the system allows users to assign and verify a helper address (`sahayak`) without exposing sensitive information. this ensures that rollback operations are conducted in a secure, decentralized, and trustless manner, protecting long-term holdings from unauthorized access. zk-STARKs were selected for their scalability, efficiency, and the absence of a need for a trusted setup, making them ideal for this implementation.

---

# why?

in recent times, there have been many cases of people losing their tokens [due to a mistake](https://support.metamask.io/hc/en-us/articles/4404062349979-Accidentally-sending-funds-to-the-wrong-address) in the transaction, [due to a scam](https://www.cnbc.com/2022/01/06/crypto-scammers-took-a-record-14-billion-in-2021-chainalysis.html), or [due to a hack](https://www.reuters.com/technology/hackers-steal-around-100-million-cryptocurrency-binance-linked-blockchain-2022-10-07/). for a blockchain to handle this type of scams, large amount of hacks, it needs to be rolled back to the previous state to accumulate/reverse all the funds, as it was with ethereum that created ETC after [hackers stole around $50 million from DAO](https://www.forbes.com/advisor/investing/cryptocurrency/what-is-ethereum-classic/)

and more recently, [the wazirx hack](https://wazirx.com/blog/preliminary-report-cyber-attack-on-wazirx-multisig-wallet/)

now the point is, after that, billions of dollars in crypto has been hacked and scammed from various blockchains. and many of them didn’t rolled back, causing users and organizations to suffer great losses.

the rollback token standard proposes, ***instead of rolling back the entire blockchain, one can just undo the transfer transaction within a time period, safeguarding the assets that were compromised.***

with rbts,

- anyone can reverse their compromised token transfers
- crypto hacks can be minimized to 0
- new layer of security will be added on-chain
- no losses to anyone

---

# how?

rollback token standardizes an existing erc20 token with a rollback feature. behind the curtains, the process starts with assigning an helper address Y (`sahayak`) to the address X, when the latter is compromised or hacked, rbt tokens transferred to the exploiter can be reversed back using the helper address.

using zero-knowledge proofs, one can assign its helper in a way without exposing its details. only the sahayak will have the proof to prove its ownership over reversing transfers.

hold on, wouldn’t the exploiter transfer to another address again? no! that’s the catch (and a security level check), for the tokens to be reflected in the balance, the same time period will be considered.

```auto
struct TransferStruct {
    address to;
    uint256 amount;
    uint256 timestamp;
}

/**
    @dev get specific transfer details for the address
    @return TransferStruct
**/
mapping( address => mapping( uint => TransferStruct )) public transfers;
mapping( address => uint ) public transferCount;

... isValid( address account, uint tid ) internval view returns ( bool ) {
    uint lockPeriod = IRBOracle( _oracle ).getReversePeriod();
    uint locked = _transfers[account][tid].timestamp.add( lockPeriod );

    return block.timestamp > locked;
}

... getAmount( address account, uint tid ) internal view returns ( uint256 amount ) {
    amount = transfers[msg.sender][tid].amount;
}

... balanceOf( address account ) {
    uint256 balances = 0
    for ( uint i = 0; i < transferCount[account] i ++ ) {
        balances = isValid( account, i ) ? getAmount(account, i) : 0;
    }
}
```

rbt will work using these components, `rbtOracle`, `rbtWrapper`, `rbtToken`, `rbtSahayak`

### rbtSahayak

***“sahayak” signifies a role of support and assistance in different contexts, where one person helps another in their tasks or responsibilities***

a normal EOA address, or a contract address, that can be assigned to an EOA or a contract address.

### rbtToken

logical token for rolling back the transaction, implementing all the existing methods of the ERC20 standard, with the below added methods

```auto
function rollBack(uint tid) external;
function getTransfer(uint tid) external view returns (TransferStruct memory);
```

`rollBack(uint tid)` will rollback the `tid` transfer happened

`getTransfer(uint tid)` will return the transfer details of `tid` transfer

### rbtWrapper

to wrap an existing erc20 token to rbt

### rbtOracle

this will be the captain of our ship, handling the core part of managing `rbtSahayak` (the helper) to an address. an EOA can assign its sahayak by giving their ownership proof using signature, and contract address can issue by verifying its owner() or contract creator ownership.

```auto
rbtOracle.register( bytes memory signature, address sahayak ) // for EOA
rbtOracle.assign( bytes memory signature, address contractAddress, address sahayak) // for contract address
```

once it’s registered to the oracle, the `sahayak` will be able to reverse the rbt token transfers within the time period set by the oracle.

for verifying the `sahayak` address, we will be using zkSTARK for verifying proofsg without using a trusted base, which will receive the proof given at the time of assigning the sahayak, and verify the proof with the public inputs, and return the result.

```auto
function verify( bytes memory proof, Commitment memory publicInputs ) public view returns ( bool ) {
    return verifier.verify( proof, publicInputs );
}
```

extended features

- one address can only have one sahayak
- the sahayak can have its own sahayak ( long chain layered can be created )
- incase of updating the sahayak, [ discussion required ]

*note: functions defined may vary (just for overview purpose)

let’s discuss this, for adding as an improvement or using at advance level, I might think this will help to reduce some amount of unauthorized token transfer hacks ![:slightly_smiling_face:](https://ethereum-magicians.org/images/emoji/twitter/slightly_smiling_face.png?v=15)

## Replies

**0xRobinR** (2024-08-26):

at first, I thought of it as an extended erc20 token standard, it can also be implemented as a wrapper protocol on existing erc20 tokens, wrap your existing assets and hold it

---

**0xRobinR** (2024-08-27):

[@vbuterin](/u/vbuterin) [@SamWilsn](/u/samwilsn) [@abcoathup](/u/abcoathup) any views on this?

---

**SamWilsn** (2024-08-27):

I’m sorry, this is outside my area of expertise.

---

**abcoathup** (2024-08-28):

I don’t see how a rollback token can be safely used (as compared with held).  If you accepted it as payment in a contract or did a swap then it can be potentially rolled back.

So the use case appears limited to holding.  Wrap a token in your wallet, and if the wrapped token is transferred you can attempt a rollback.  But the unwrapping should be behind a timelock, so why not store tokens in a timelocked vault and not have to deal with the rollback mechanism.

---

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/0xrobinr/48/9258_2.png) 0xRobinR:

> any views on this?

Recommend not tagging people.  People will feedback if they find it interesting.

---

**0xRobinR** (2024-08-28):

apologies for the “tagging” ![:sweat_smile:](https://ethereum-magicians.org/images/emoji/twitter/sweat_smile.png?v=12)

the concept works in a way to protect every hacks that could ever happen, as at the very basic level, it’s always a erc20 token that gets targetted.

think of a centralized exchange deposit mechanism, the deposit of ***X*** token is not considered valid until ***n*** block confirmations, rollback token has the same implementation in a decentralized way, transfer will take ***n*** blocks/minutes/hours to be valid, and if it’s unauthorized transfer, then reverting it easily using the “saviour” address linked to the ***from*** address, which is hidden by zk, within that interval.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/abcoathup/48/2073_2.png) abcoathup:

> so why not store tokens in a timelocked vault and not have to deal with the rollback mechanism.

there’s no issue with a timelock contract, but what will you do if your wallet is compromised, after the specific lock period, when the assets are released, it would eventually be transferred to the hacker address.

i know it sounds childish, but if this mechanism integrated correctly, it could prevent most of the hacks.

---

**abcoathup** (2024-08-28):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/0xrobinr/48/9258_2.png) 0xRobinR:

> but if this mechanism integrated correctly, it could prevent most of the hacks.

It can only practically be used for holding.  Spending & swapping are unsafe unless contracts implement checks that the token is outside the rollback window.  For this reason I don’t see it getting adoption as a token extension.

Wrapping existing tokens for long term holding maybe a use case but I think it would be a hard sell to get people to do it.

