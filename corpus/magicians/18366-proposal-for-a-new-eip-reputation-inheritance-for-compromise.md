---
source: magicians
topic_id: 18366
title: "Proposal for a new EIP: Reputation Inheritance for Compromised Accounts"
author: lukema95
date: "2024-01-29"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/proposal-for-a-new-eip-reputation-inheritance-for-compromised-accounts/18366
views: 548
likes: 0
posts_count: 3
---

# Proposal for a new EIP: Reputation Inheritance for Compromised Accounts

The proposal aims to enhance account security while preserving the valuable transaction history and reputation associated with an Ethereum address.

## Background:

The current state of Ethereum poses a potential risk to users if their account’s private key is leaked or stolen. While abandoning the compromised account may seem like the most straightforward solution, it often results in the loss of valuable transaction records, accumulated reputation, and missed opportunities such as airdrop rewards from various projects.

## Proposal Overview:

I am introducing the concept of the “Ghost” contract, a solution designed to allow users to reroute their accounts to new addresses while preserving their historical transaction records and reputation. The mechanism involves registering backup addresses and choosing one of them as the new route for the account. This way, even if the original account’s private key is compromised, users can redirect their activities to a new, secure address.

## Ghost Contract Implementation:

Below is a simplified version of the Ghost contract implemented in Solidity:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

contract Ghost {
  mapping(address => address[]) public registry;
  mapping(address => address) public router;

  event Register(address, address[]);
  event Route(address, address);

  constructor() {}

  function register(address[] memory _registry) external {
    address[] memory registed = registry[msg.sender];
    require(registed.length == 0, "user already registed");
    for (uint i = 0; i  0, "user has not registered yet");
    require(router[msg.sender] == address(0), "user already routed");

    for (uint i = 0; i < _registry.length; i++) {
      if (to == _registry[i]) {
        router[msg.sender] = to;
        emit Route(msg.sender, to);
        break;
      }
    }

    require(router[msg.sender] != address(0), "address is not in the registery");
  }

  function queryRoute(address _account) external view returns (address) {
    address redirection = router[_account];
    if (redirection == address(0)) {
      return msg.sender;
    }

    return redirection;
  }
}
```

## How It Works:

1. Users register a list of backup addresses using the register function.
2. Users choose one of the registered addresses to route their transactions through using the route function.
3. The queryRoute function allows anyone to query the current route for a specific account.

## Benefits:

- Enhanced account security in the event of a compromised private key.
- Preservation of transaction history and reputation.
- Continued eligibility for airdrops and rewards based on the account’s historical activity.

## Replies

**CedarMist** (2024-01-31):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lukema95/48/11548_2.png) lukema95:

> The current state of Ethereum poses a potential risk to users if their account’s private key is leaked or stolen. While abandoning the compromised account may seem like the most straightforward solution

Excellent, a new attack vector, permanently turning my account into a ‘Ghost account’ against my will and stealing all future airdrops & accumulated reputation from my existing account with no way for me to get it back even though ‘buut I have the key’.

This sounds severely and fundamentally flawed …

---

**bumblefudge** (2024-01-31):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/cedarmist/48/11033_2.png) CedarMist:

> Excellent, a new attack vector, permanently turning my account into a ‘Ghost account’ against my will

I’m not sure I would go so far as “severely flawed” until I’ve heard more, but I would definitely agree that this attack vector is serious and could well be a dealbreaker making this EIP not worth writing if no satisfactory mitigations/strategies can be proposed.

To put it another way, maybe the “### Security Considerations” section needs to be written and workshopped a bit (in-thread, for example) before it’s worth starting the EIP process?

