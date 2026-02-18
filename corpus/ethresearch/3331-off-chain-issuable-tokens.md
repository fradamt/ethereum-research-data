---
source: ethresearch
topic_id: 3331
title: Off-chain Issuable Tokens
author: danfinlay
date: "2018-09-12"
category: Layer 2 > State channels
tags: []
url: https://ethresear.ch/t/off-chain-issuable-tokens/3331
views: 3801
likes: 10
posts_count: 10
---

# Off-chain Issuable Tokens

Cross-posted from a slightly more live version [on github](https://github.com/danfinlay/Ethereum-Off-Chain-Issuable-Tokens).

# Off-chain Issuable Tokens

Some tokens have a central issuing authority, like for coins in an online game, which may only gain interesting value meriting an on-chain transaction once they accrue in a significant quantity.

In cases like this, issuance can be performed in an offchain manner that maintains on-chain trustlessness.

State channels require an initial deposit because it is assumed that the sender has a limited quantity of tokens. In the case of a centralized issuer, you have an implicit infinite deposit of tokens, and this allows tokens to be counterfactually issued with a simple signed message.

An example issuance message, signed by the issuer might look like this:

```auto
struct IssuanceMessage {
  address recipient;
  uint amount;
  uint issuanceBlock; // could also use time stamp
}
```

The issuanceBlock or time stamp is used so that once a message is used to mint and redeem some tokens, no message before that redemption block height is valid. This ensures redeemers are always incentivized to only try to redeem their most recent message, and cannot replay messages.

This requires the issuer to recognize when tokens are redeemed, and restart their `amount` counter for messages sent to that user.

A sample extension to the token interface would be a method such as:

```auto
function redeemPromisedTokens(bytes payload, uint8 v, bytes32 r, bytes32 s) public returns (bool);
```

## Pseudolidity Implementation

```auto
contract OffchainIssuableToken is MintableToken {

  mapping (address => uint) latestWithdrawBlock;

  struct IssuanceMessage {
    address recipient;
    uint amount;
    uint issuanceBlock;
  }

  function redeemPromisedTokens(bytes payload, uint8 v, bytes32 r, bytes32 s) public returns (bool) {
    assert(verify(payload, v, r, s));

    IssuanceMessage memory msg = parse(payload, v, r, s);

    // Ensure user submits the latest message they have
    // to prevent replay attacks:
    assert(msg.issuanceBlock > latestWithdrawBlock[msg.sender]);
    latestWithdrawBlock[msg.sender] = this.blockNumber;

    mint(msg.recipient, msg.amount);
  }
}
```

## Wallet Implementation

Wallets could store these messages and display them like tokens, and they would not need to be privately held unless privacy were a goal, because the only thing the message could be used for would be issuing these tokens.

## Use Cases

An AI company wants to reward online participants for training its web interface, and wants to issue tokens for each attempt without an on-chain transaction.

Personal currencies that are backed primarily by an individual’s trust, so the threat of inflation is already accounted for in the risk of holding that coin.

An organization wants to crowdfund in person, in cash, and give out certificates for token redemption without bothering with on-chain transactions, especially when (like with some crowd-funding ventures) the project may not complete, and the tokens may not be worth redeeming anyway.

Casual or localized token experiments: Selling a gift card

This pattern also works when offline, so even in a low-internet environment, if a person or entity has the ability to sign minting messages for a token that has a known value, they could sign these messages as a way to pay someone “once they’re online”.

## Possible other features

The signed message could include a reference to the issuing contract, to allow the issuing key to issue multiple different tokens.

There could be a `redeemAndSend` method so that a user can both redeem their tokens and send some of them in a single transaction.

The token contract is given the power to verify signatures and enforce issuance however it wants. There could be a list of approved issuers, and individual issuers could even have issuance limits to tranche liability of compromised issuing keys.

If a withdraw period + unainamous signatures were added (like in a traditional state channel), then the tokens issued could also be bi-directionally exchanged, without ever making an on-chain transaction.

## Replies

**nginnever** (2018-09-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/danfinlay/48/1084_2.png) danfinlay:

> The issuanceBlock or time stamp is used so that once a message is used to mint and redeem some tokens, no message before that redemption block height is valid. This ensures redeemers are always incentivized to only try to redeem their most recent message, and cannot replay messages.

The timestamp isn’t exactly the reason a receiver of a unidirectional payment channel is incentivized to claim the latest state but you’re on the right track. It’s because the latest state contains the highest value of token transfer. You could remove the timestamp from your state and have your contract check…

`assert(msg.amount > balance[msg.sender]);`

This way you wouldn’t have to reset the off-chain balance or have to witness exits either. Always track a total balance issued and have the parent contract only send the difference of the latest withdrawal recorded and the current state provided. Think that should work ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**danfinlay** (2018-09-12):

Ah, good solution. The withdraw did have the awkward quality of interrupting payments.

---

**danfinlay** (2018-09-13):

I added the suggested change to the linked github repo.

---

**yahgwai** (2018-09-17):

Just to check my understanding, this will only work if mint() can be relied upon to always succeed? So there can be no limitations on mint. eg maximum token supply?

---

**PhABC** (2018-09-17):

I think this is really interesting Dan and would love to see more people doing this.

I implemented something very similar early 2018 with Josh Crites from Consensys, but in our case, the tokens users could redeem where non-transferable. Works as follow :

1. X number of admins sign a message for user Y
2. Once user Y has enough signature, Y calls redeemTokens() function.
3. the redeemTokens() verify all the signatures, makes sure enough are valid and mint the signed amount of tokens to the user.

Admins can keep signing messages with the same nonce to increment amount minted. One use case we had in mind was a twitter bot that sends signed message to users that retweet/like a certain account, where the bot increments the amount for a given nonce until the user goes on-chain and redeems the token. Then the nonce is increment and process is repeated, like you describe.

This project is not completed nor audited, but there is definitely code people could reuse. Project can be found here : https://github.com/PhABC/participation-token/blob/master/README.md

.

---

**nginnever** (2018-09-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/yahgwai/48/759_2.png) yahgwai:

> So there can be no limitations on mint. eg maximum token supply?

This is an interesting question. I think what Dan proposes in this post assumes that the supply would inflate indefinitely, but I wonder if we could cap this as well.

This may involve some questions posted here [Why Smart Contracts are NOT feasible on Plasma](https://ethresear.ch/t/why-smart-contracts-are-not-feasible-on-plasma/2598) as in order to cap the total supply we would need the layer2 contracts to be able to track a total supply number in a decentralized way. This is difficult because of the ownership of that supply count and what happens to it upon exit.

I’ll put some more thought into this and reply if I come to anything interesting.

---

**danfinlay** (2018-09-17):

I think capping issuance is a reasonable extension, given an understanding of its limitations:

- If the issuing key has an issuance cap, there is no guarantee a given message can be redeemed for those tokens (the key could always issue up to its cap to another address, and that other address could race to redeem tokens).
- Adding issuance caps could still be a way of isolating the risk associated with storing a token-issuing key on an internet-connected computer. A second, cold(er) account could be used for renewing the issuing key’s permissions.
- Issuing keys could not be used twice, and discarded after their limit has been issued, creating higher chances of message redeem-ability, although this higher chance would be opaque to message recipients.

It might make sense to include a well defined protocol for that error (issuance limit exceeded) before this would be finalized into any sort of EIP-ready interface. Maybe it could take advantage of [ERC 1066 status codes](https://ethereum-magicians.org/t/erc-1066-ethereum-status-codes-esc/283).

There could also be a simple smart contract defined that receives a token allowance, using the standard token `approve(address spender, uint tokens)` method, and allows any user to issue off-chain allowances as messages using a similar message format.

And of course, those messages could be nested to allow trees of permitted spending á-la trustlines: https://gist.github.com/danfinlay/73b6ffd11aea5a85767fe20c6ad868c5

---

**yahgwai** (2018-09-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/danfinlay/48/1084_2.png) danfinlay:

> If the issuing key has an issuance cap, there is no guarantee a given message can be redeemed for those tokens

I think this changes the proposition quite considerably. A redeemer now needs to trust the the issuer to not over-issue, and the following would no longer hold:

![](https://ethresear.ch/user_avatar/ethresear.ch/danfinlay/48/1084_2.png) danfinlay:

> issuance can be performed in an offchain manner that maintains on-chain trustlessness.

This does make sense in the context of the trustlines link though, I get where you’re coming from now.

---

**danfinlay** (2018-09-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/yahgwai/48/759_2.png) yahgwai:

> I think this changes the proposition quite considerably. A redeemer now needs to trust the the issuer to not over-issue, and the following would no longer hold:

Kindof, but if you’re trusting a key with no limit on the tokens it issues already, there’s already a large component of trusting its integrity: On one side the danger is someone else getting issued your tokens, on the other side is the danger of the tokens being diluted into oblivion.

If a key’s limit is reached because it was compromised, a good token issuing body would establish a new key and retroactively pay the tokens it had meant to before the hack.

Anyways, I agree that the type of trustlessness is reduced with an issuance limit, but I think it’s worth pointing out there’s already a ton of trust involved when dealing with centrally-issued tokens.

