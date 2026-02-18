---
source: magicians
topic_id: 12298
title: "EIP-6229: Tokenized Vaults with Lock-in Period"
author: Anderson
date: "2022-12-28"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-6229-tokenized-vaults-with-lock-in-period/12298
views: 1163
likes: 1
posts_count: 2
---

# EIP-6229: Tokenized Vaults with Lock-in Period

Hi ethereum magicians! We are proposing a new EIP:

- EIP Proposal: Tokenized Vaults with Lock-in Period
- Description: This standard is an extension of the EIP-4626 Tokenized Vaults that provides functions to support the lock-in period.
- Stage: draft
- Relate EIPs: EIP-4626 Tokenized Vaults

Please see the pull request in details:



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/6229)














####


      `master` ← `Ankarrr:eip-draft-tokenized-vault-with-lock-in-period`




          opened 06:42AM - 28 Dec 22 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/3/311c957574c7c74b29521f2e3603d195b8f7ebc5.jpeg)
            Ankarrr](https://github.com/Ankarrr)



          [+321
            -0](https://github.com/ethereum/EIPs/pull/6229/files)







This draft EIP is an extension of the EIP-4626 Tokenized Vaults that provides fu[…](https://github.com/ethereum/EIPs/pull/6229)nctions to support the lock-in period.

I used the suggested template: https://github.com/ethereum/EIPs/blob/master/eip-template.md












This proposal is in the draft stage. Any comments and feedback are very welcome and appreciated!

## Replies

**Anderson** (2023-01-16):

According to feedback, I’m considering removing the `VaultStates` to avoid using Enum, and use a boolean to represent the vault’s state. This will be more developer friendly to integrate the vault.

Proposed changes:

1. Remove VaultStates
2. Change state to locked. The specs of locked is described below.

### locked

The current state of the vault. `True` means `LOCKED`, and `False` means `UNLOCKED`.

```auto
- name: state
  type: boolean
  stateMutability: view

  inputs: []

  outputs:
    - name: state
      type: boolean
```

