---
source: magicians
topic_id: 10419
title: "EIP-5478: CREATE2COPY Opcode"
author: qizhou
date: "2022-08-17"
category: EIPs > EIPs core
tags: [opcodes, gas, shanghai-candidate]
url: https://ethereum-magicians.org/t/eip-5478-create2copy-opcode/10419
views: 2687
likes: 3
posts_count: 11
---

# EIP-5478: CREATE2COPY Opcode

---

## eip: 5478
title: CREATE2COPY Opcode
description: Reducing the gas cost of contract creation with existing code
author: Qi Zhou ()
discussions-to:
status: Draft
type: Standards Track
category: Core
created: 2022-08-17
requires: 1014, 2929



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/5478/files)














####


      `master` ← `qizhou:patch-11`




          opened 06:00PM - 17 Aug 22 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/e/ec489df73b8873547715c8a2f21986ca2b83d33c.jpeg)
            qizhou](https://github.com/qizhou)



          [+49
            -0](https://github.com/ethereum/EIPs/pull/5478/files)







When opening a pull request to submit a new EIP, please use the suggested templa[…](https://github.com/ethereum/EIPs/pull/5478)te: https://github.com/ethereum/EIPs/blob/master/eip-template.md

We have a GitHub bot that automatically merges some PRs. It will merge yours immediately if certain criteria are met:

 - The PR edits only existing draft PRs.
 - The build passes.
 - Your GitHub username or email address is listed in the 'author' header of all affected PRs, inside <triangular brackets>.
 - If matching on email address, the email address is the one publicly listed on your GitHub profile.

## Replies

**high_byte** (2022-09-30):

that’s a great idea. but instead of introducing a new opcode, did you try to implement this by creating a constructor that accepts an address (and parameters) and uses extcodecopy (instead of calldata)? you will still pay for memory expansion but I think it might be cheaper still. also this works around introducing a new opcode.

---

**qizhou** (2022-10-03):

Thanks for the comment.  We could definitively use `extcodecopy` to exactly copy the code from another contract in `init_code` of `CREATE/CREATE2`, however, this means that for every byte in the code to be copied, the tx needs to pay 200 gas.  For example, copying a contract with 10K bytes code will cost 200 * 10K = 2M gas!

The `CREATE2COPY` opcode addresses this issue by charging only 2600 (for cold account access).  This would save the gas cost from 2M to 2600.

I hope this could explain.  Feel free to let me know if you have further question.

---

**high_byte** (2022-10-04):

(correction in the posts below)

---

I’m not sure where you brought that 200 gas comes from.

I ran a test, please correct me if I’m wrong:

```auto
PUSH1 0x40 ; len
PUSH1 0x00 ; dst offset
PUSH1 0x00 ; src offset
ADDRESS    ; addr to copy from (address(this))
EXTCODECOPY
PUSH1 0x00 ; just to verify it was copied properly
MLOAD
```

execute by the running the following:

```auto
evm --json --code 604060006000303c600051 run

{"pc":0,"op":96,"gas":"0x2540be400","gasCost":"0x3","memSize":0,"stack":[],"depth":1,"refund":0,"opName":"PUSH1"}

{"pc":2,"op":96,"gas":"0x2540be3fd","gasCost":"0x3","memSize":0,"stack":["0x60"],"depth":1,"refund":0,"opName":"PUSH1"}

{"pc":4,"op":96,"gas":"0x2540be3fa","gasCost":"0x3","memSize":0,"stack":["0x60","0x0"],"depth":1,"refund":0,"opName":"PUSH1"}

{"pc":6,"op":48,"gas":"0x2540be3f7","gasCost":"0x2","memSize":0,"stack":["0x60","0x0","0x0"],"depth":1,"refund":0,"opName":"ADDRESS"}

{"pc":7,"op":60,"gas":"0x2540be3f5",**"gasCost":"0x70"**,"memSize":0,"stack":["0x60","0x0","0x0","0x7265636569766572"],"depth":1,"refund":0,"opName":"EXTCODECOPY"}

{"pc":8,"op":96,"gas":"0x2540be37f","gasCost":"0x3","memSize":96,"stack":[],"depth":1,"refund":0,"opName":"PUSH1"}

{"pc":10,"op":81,"gas":"0x2540be37c","gasCost":"0x3","memSize":96,"stack":["0x0"],"depth":1,"refund":0,"opName":"MLOAD"}

{"pc":11,"op":0,"gas":"0x2540be379","gasCost":"0x0","memSize":96,"stack":["0x604060006000303c600051000000000000000000000000000000000000000000"],"depth":1,"refund":0,"opName":"STOP"}

{"output":"","gasUsed":"0x87","time":128667}
```

I have marked in bold the gas used by EXTCODECOPY: 0x70 for 2 words (0x40). notice that for 3 words (0x41~0x60) the gas cost is increase by 6 to 0x76.

---

**qizhou** (2022-10-04):

The 200 gas per byte is from `CREATE2/CREATE2`, where the code here only copies the code in memory, but the code is not yet stored as a contract code.  Hope this could explain.

---

**high_byte** (2022-10-05):

Ah my mistake.

I understand now; I interpreted each byte to copy as the cost of EXTCODECOPY. you were talking about deposit gas price, here’s a reference:



      [github.com](https://github.com/wolflo/evm-opcodes/blob/main/gas.md#a9-f-code-deposit-cost)





####



```md
# Appendix - Dynamic Gas Costs

### A0-0: Intrinsic Gas
Intrinsic gas is the amount of gas paid prior to execution of a transaction.
That is, the gas paid by the initiator of a transaction, which will always be an externally-owned account, before any state updates are made or any code is executed.

Gas Calculation:
- `gas_cost = 21000`: base cost
- **If** `tx.to == null` (contract creation tx):
    - `gas_cost += 32000`
- `gas_cost += 4 * bytes_zero`: gas added to base cost for every zero byte of memory data
- `gas_cost += 16 * bytes_nonzero`: gas added to base cost for every nonzero byte of memory data

### A0-1: Memory Expansion
An additional gas cost is paid by any operation that expands the memory that is in use.
This memory expansion cost is dependent on the existing memory size and is `0` if the operation does not reference a memory address higher than the existing highest referenced memory address.
A reference is any read, write, or other usage of memory (such as in a `CALL`).

Terms:
- `new_mem_size`: the highest referenced memory address after the operation in question (in bytes)
```

  This file has been truncated. [show original](https://github.com/wolflo/evm-opcodes/blob/main/gas.md#a9-f-code-deposit-cost)

---

**qizhou** (2022-10-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/high_byte/48/11480_2.png) high_byte:

> I understand now; I interpreted each byte to copy as the cost of EXTCODECOPY. you were talking about deposit gas price, here’s a reference

Yes, that is exactly the EIP is optimizing for ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**wjmelements** (2022-10-06):

My attempt at something like this was [Skinniest CREATELINK by wjmelements · Pull Request #2185 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/2185)

I think there are benefits to recognizing that many contracts might have identical code.

---

**qizhou** (2022-10-07):

Agree!  I think CREATE2COPY and CREATELINK can co-exist as they serve a bit different purposes:

- CREATE2COPY can be used to create a contract with a constructor, which initializes contract storage based on ctor logic;
- CREATELINK can be used to create a “blank” contract.  The contract may be have a initialize() method to initialize the storage such as owner, initial parameters, etc.

---

**k06a** (2022-10-07):

This EIP seems very limited due fact of popularity of “immutable” values, since they are part of the byte code.

---

**qizhou** (2022-10-07):

If there are “immutable” values, then the `contract_code` will be generated by `init_code`, which will be generally different even though most of the parts are the same.  Yes, we cannot save any store cost of the contract anymore in this case.

However, it depends on which type of contract we want to copy, e.g., in the smart wallet case, if the operator wants to create millions of such smart wallet contracts with minimal storage cost, then the operator may optimize the contract so that all values are either `const` or in local storage.

