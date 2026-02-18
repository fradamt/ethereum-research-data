---
source: magicians
topic_id: 19099
title: Only using EVM contracts to solve web2 platform recharge issues with comprehensive advantages
author: ZWJKFLC
date: "2024-03-07"
category: ERCs
tags: [erc, evm]
url: https://ethereum-magicians.org/t/only-using-evm-contracts-to-solve-web2-platform-recharge-issues-with-comprehensive-advantages/19099
views: 457
likes: 0
posts_count: 1
---

# Only using EVM contracts to solve web2 platform recharge issues with comprehensive advantages

Nowadays, CEX uses a very complex system to achieve payment collection, which requires precautions against issues such as key security.

I have a solution now, which is to type ETH/TOKEN to an address without changing user interaction, and then implement this set of functions only in the form of a contract, and it is very easy for developers to develop. I would like to ask, is there any significance in doing it, or is there anyone who needs it?

Only use contracts to implement the following functions and features

```plaintext
 getwalletadd(
    address Withdrawal_address,uint256 order/account/path
) public view return(address Payment_address)
//Get the address where users can make payments
//Withdrawal_address：It means the final payment address where eth/token goes.
//order/account/path：Transaction order or account ID on the web2 platform
//Payment_address：The address where consumers need to send money

imputationeth(address Withdrawal_address,uint256[] orders/accounts/paths)
//Collect Payment_address's eth to Withdrawal_address
```

User interaction habits have not changed during the entire process.

The secret key of Withdrawal_address is not required and eth can collect Withdrawal_address

And only contracts are used to ensure security. Only a single-digit interface is needed to access evm payment eth/token, and the gas fee is much lower than CEX. No maintenance costs required.
