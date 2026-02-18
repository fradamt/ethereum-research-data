---
source: ethresearch
topic_id: 18642
title: "[RFC] Contract-Led Storage-Rent Roadmap"
author: Zergity
date: "2024-02-11"
category: Architecture
tags: [storage-fee-rent, data-structure]
url: https://ethresear.ch/t/rfc-contract-led-storage-rent-roadmap/18642
views: 1660
likes: 1
posts_count: 3
---

# [RFC] Contract-Led Storage-Rent Roadmap

A possible roadmap to user-owned storage (and renting) led by contract development.

(Please let me know if I should go ahead and write detailed design and EIP for this.)

### Goals:

- Data storage is owned by the beneficiary rather than application contracts.

Owners cannot (U)pdate their data but can (D)elete them to manage the state size (and rent) and remove the spam data created by spammers.
- Application contracts have full CRUD control, while users can (D)elete their data without impacting the application’s shared states or other users’ states.
- Optionally, data resurrection can be developed by storage contracts, but there are many ways this roadmap can end up without resurrection at all.

`StorageManager` strategies are led by smart contract development and are open to the community.

- Different storage strategies can be developed and utilized by the applications simultaneously.
- Applications can choose and utilize the desired StorageManager without worrying about the storage implementation.
- Each StorageManager stores all of its application data in its trie and grants proper permissions to each user and application contract.

Execution clients can apply different storage optimization strategies without any protocol upgrade.

Protocol upgrades can be planned in the endgame or not at all depends on the development of the previous steps. (E.g. rent and prune)

### Notes

- Execution clients can optimize storage access by storing all data belonging to an account in a single trie, even across multiple StorageManager contracts.
- Execution clients can incentivize applications to use StorageManager by prioritizing transactions with StorageManager in the EIP-2930 access list.
- Complex storage data rent, prune and resurrection strategies can be developed by the community.
- Data resurrection can be entirely omitted in favor of more socioeconomical mechanisms. For example, a close-to-be-pruned account can be preserved by anyone through payment, and later the preserver can benefit from various forms of compensation provided by the account owner.

### Example

The simplest `StorageManager` implementation that is sufficient for execution clients’ optimization and state pruning.

```plaintext
contract SimpleStorageManager {
  event Update(
    address indexed user,
    address indexed application,
    address indexed key,
    value
  );

  mapping(bytes32 => bytes32) storage s_data;

  // by user
  function delete(address application, bytes32 key) public {
    delete s_data[_key(msg.sender, application, key)];
    emit Update(msg.sender, application, key, 0);
  }

  // by application
  function update(address user, bytes32 key, bytes32 value) publlic {
    s_data[_key(user, msg.sender, key)] = value;
    emit Update(user, msg.sender, key, value);
  }

  function read(address user, address application, bytes32 key) public view returns (bytes32) {
    return s_data[_key(user, application, key)];
  }

  function _key(address user, address application, bytes32 key) internal pure returns (bytes32) {
    return keccak256(abi.encodePacked(user, application, key));
  }
}
```

## Replies

**peersky** (2024-03-03):

Hi [@Zergity](/u/zergity)

It looks interesting for me. Certainly has thoughts inline with my [RFC on user-centric asset model](https://ethresear.ch/t/rfc-fixing-ethereum-ux-with-user-centric-asset-model-erc-versioning/18760/2).

I would suggest updating goals so that it does not mention implementation specific structures, i.e.  *“Various storage management strategies can be defined and led by smart contract developer community”.*

Could you elaborate problem for the execution clients, why this memory mapping pattern would be preferred for them?

**Regarding implementation:**

`_key` function can be modified to return storage in [ERC-7201](https://eips.ethereum.org/EIPS/eip-7201) name-spaced storage compatible way.

Storage protection generally will be a concern here since applications could attempt to find `key` that collides to another app.

Another way to think of this is a factory contract that deploys separate memory implementation for app upon request.

Few benefits of such - Factories could implement granular storage management strategies supporting wider use-case variety such as permissioning application access to create memory on user premise.

---

**Zergity** (2024-03-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/peersky/48/10864_2.png) peersky:

> Could you elaborate problem for the execution clients, why this memory mapping pattern would be preferred for them?

Accessing cold storage in MPT is expensive. Typically, transactions involve only two accounts (the sender and recipient), if all storage belonging to an account (such as ERC20 balances, approvals, etc.) is stored in a single trie node using a flat key-value map, accessing storage becomes significantly more efficient. Consequently, the cost of storage access would scale with the number of participant accounts in a transaction (or block), rather than the data size.

I’m preparing an updated model for the rest of your comments.

