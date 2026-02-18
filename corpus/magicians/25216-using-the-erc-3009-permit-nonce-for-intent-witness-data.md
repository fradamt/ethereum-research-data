---
source: magicians
topic_id: 25216
title: Using the ERC 3009 permit nonce for intent witness data
author: wjmelements
date: "2025-08-22"
category: ERCs
tags: [security, token-approval]
url: https://ethereum-magicians.org/t/using-the-erc-3009-permit-nonce-for-intent-witness-data/25216
views: 179
likes: 4
posts_count: 2
---

# Using the ERC 3009 permit nonce for intent witness data

I am interested in soliciting feedback from the community, particularly from anyone who has a lot of experience with token permitting and intents. I understand there are other permit/intent/meta-TX solutions; feel free to mention them, but in this thread I mainly want to discuss this one. This idea could either be brilliant or dangerous, and so I do not want to rely on my own limited understanding.

#### Intended behavior

In ERC 3009, the nonce is a free variable. The only restriction on it is that it cannot match a previous nonce, and the recommended usage is for the nonce to be random.

#### Limitation

ERC 3009 cannot convey the intent for a payment, and so must sign twice, once for the permit, and once for the intent.

#### Goal

In order to reduce the number of user signatures, I would like to pack a full user intent into the token permit, in the style of Permit2 `witness` data. Then another actor, such as a paymaster, could fulfill the intent from just a permit signature.

#### Method

For ERC 3009 permits, the `nonce` can pack `witness` data for the recipient, including another `nonce` field, so the recipient contract could verify the user’s intent.

For example, if the ERC 3009 recipient were a DEX, the ERC 3009 `nonce` might be structured like

```auto
struct BuyIntent {
    IERC20 token;
    uint256 minOut;
    bytes32 nonce;
};
bytes32 erc3009Nonce = keccak256(abi.encode(BUY_INTENT_TYPEHASH, buyIntent.token, buyIntent.minOut, buyIntent.nonce));
```

Thereby the DEX could reconstruct the nonce before `receiveWithAuthorization`, and know that the permit nonce was generated with those parameters. The intent, a limit order in this case, is conveyed in the ERC3009 `nonce` field.

#### Security Considerations

A malicious client may prompt the user without conveying how the nonce is generated. While they would still know which token they were approving and how much, the intent could be malicious. This category of attacks is called [Signature Phishing](https://support.metamask.io/stay-safe/protect-yourself/wallet-and-hardware/signature-phishing/). Its scope can be limited by encouraging users only to use official client software, preferably with checksums and content-addressing, but there are plenty of ways users can compromise themselves. The danger is amplified because the field in the ERC3009 typeHash is merely called `nonce` and might look fine. However once you are compromised to this extent, there may be better ways to steal your assets.

## Replies

**frangio** (2025-08-23):

Indeed, I’ve seen this used:



      [github.com/base/commerce-payments](https://github.com/base/commerce-payments/blob/3f77761cf8b174fdc456a275a9c64919eda44234/src/collectors/ERC3009PaymentCollector.sol#L48)





####

  [3f77761cf](https://github.com/base/commerce-payments/blob/3f77761cf8b174fdc456a275a9c64919eda44234/src/collectors/ERC3009PaymentCollector.sol#L48)



```sol


1. address payer = paymentInfo.payer;
2. uint256 maxAmount = paymentInfo.maxAmount;
3.
4. // Pull tokens into this contract
5. IERC3009(token).receiveWithAuthorization({
6. from: payer,
7. to: address(this),
8. value: maxAmount,
9. validAfter: 0,
10. validBefore: paymentInfo.preApprovalExpiry,
11. nonce: _getHashPayerAgnostic(paymentInfo),
12. signature: _handleERC6492Signature(collectorData)
13. });
14.
15. // Return any excess tokens to payer
16. if (maxAmount > amount) SafeERC20.safeTransfer(IERC20(token), payer, maxAmount - amount);
17.
18. // Transfer tokens directly to token store
19. SafeERC20.safeTransfer(IERC20(token), tokenStore, amount);
20. }
21. }


```










I agree that this is not ideal. Something that could be interesting is for a protocol to only accept this kind of signature for small USDC amounts (for the UX benefits of single signature flows), and to force larger amounts or other tokens through Permit2 or a scheme that provides full transparency in the wallet of what’s being signed.

Obviously another way to abuse ERC-3009 signatures for phishing is to place a malicious address in the `to` parameter, and with the current sad state of wallets and their implementation of EIP-712 I don’t think that would raise more alarms than a malicious nonce. In an ideal world, the `to` parameter would be shown next to some sort of security score at the moment of signing to mitigate that attack vector, which is not possible/easy with the nonce.

