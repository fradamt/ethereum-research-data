---
source: ethresearch
topic_id: 11549
title: A zk-evm specification
author: OlivierBBB
date: "2021-12-20"
category: Layer 2
tags: [zk-roll-up]
url: https://ethresear.ch/t/a-zk-evm-specification/11549
views: 19724
likes: 62
posts_count: 22
---

# A zk-evm specification

*Nicolas Liochon, Théodore Chapuis-Chkaiban, Alexandre Belling, Olivier Bégassat*

Many thanks to *Thomas Piellard*, *Blazej Kolad* and *Gautam Botrel* for their constructive feedback.

Hi all, here is a proposal for an efficient zk-EVM arithmetization which we are starting to implement. Our objective was to satisfy the 3 following design goals:

1. support for all EVM opcodes including internal smart contract calls, error management and gas management,
2. ability to execute bytecode as is,
3. minimal prover time.

We strive to provide an arithmetization that respects the EVM specification as defined in the Ethereum yellow paper. We provide a comprehensive approach which is technically realizable using existing zero-knowledge proving schemes. We would greatly appreciate any feedback you may have!

[ZK_EVM.pdf](/uploads/short-url/3DM8kjFfIG6PHXu4qpYpmujXgme.pdf) (2.1 MB)

## Replies

**vbuterin** (2021-12-23):

This is amazing work!

Are there any even draft implementations of this? How long would you estimate that it would take to prove EVM execution (in seconds per gas)? What would you expect are the least efficient (in seconds per gas) operations?

Are you sure that all the operations (including calls and returning from calls) actually do cost O(1) constraints (or at most O(log(n)) per operation?

---

**tchapuischkaiban** (2021-12-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/olivierbbb/48/2536_2.png) OlivierBBB:

> Hi all, here is a proposal for an efficient zk-EVM arithmetization which we are starting to implement

> ```
> This is amazing work!
> Are there any even draft implementations of this?
> How long would you estimate that it would take to prove EVM execution (in seconds per gas)?
> What would you expect are the least efficient (in seconds per gas) operations?
> ```

We don’t have such an estimate as of now - we are just starting the implementation. We think however that the prover time will likely be dominated by commitment generation - of which there are very many. It also means that there will be a lot of parallelization. As for the second per gas efficiency, we believe that the least efficient operations would be those that involve modular arithmetics (MOD, ADDMOD, MULMOD), on 256 bits, as they involve a significant number of costly word comparison operations.

> Are you sure that all the operations (including calls and returning from calls) actually do cost O(1) constraints (or at most O(log(n)) per operation?

That is an excellent question: while, for a given clock cycle, the total number of constraints to verify does not depend on the opcode being executed- for some opcodes (CALL/RETURN opcodes for instance), the execution spans multiple clock cycles, which increases the total size of the commitments to generate. For instance, for a CALL opcode, one has to prove/verify that the whole CALLDATA has been loaded correctly in the new execution environment - the number of clock cycles will scale linearly with the length of the CALLDATA. Besides, one has to initialize the new RAM (and in some cases the new Storage) of the contract being called - the number of clockcycles will scale linearly with the total maximum size of the RAM (in EVM words) at the end of execution of the called contract (for the storage it will scale linearly with the number of storage cells accessed). A similar reasoning applies to the RETURN opcode as the number of clockcycles needed to process the opcode depends on the total length of the data returned to the caller contract.

Thanks a lot for your feedback. Please don’t hesitate if you have any other comment on the specification, or if you would like us to clarify some points !

---

**climb-yang** (2021-12-28):

[@tchapuischkaiban](/u/tchapuischkaiban)  Hello, I found a suspected error while reading the paper, is there a mistake in the memory address here?[![image](https://ethresear.ch/uploads/default/optimized/2X/9/9c60b5bca796a078f96a8884a852d3d31a939ed1_2_690x87.png)image2442×308 126 KB](https://ethresear.ch/uploads/default/9c60b5bca796a078f96a8884a852d3d31a939ed1)

---

**tchapuischkaiban** (2021-12-29):

There is a small typo here indeed. The memory address range should be [0x13a2; 0x1**3**ab] for the location of the returned values (instead of [0x13a2; 0x1**2**ab]). Is it what you were thinking about ? Thanks for pointing this out !

Besides, there is another typo for the second interval, the address range should be [0xaa**b**e, 0xaac**7**] instead of [0xaace, 0xaac**3**].

---

**MicahZoltu** (2021-12-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/tchapuischkaiban/48/8147_2.png) tchapuischkaiban:

> there is another typo for the second interval, the address range should be [0xaace, 0xaac7]

As a matter of convention, shouldn’t the smaller number in the range come first?

---

**JiangXb-son** (2021-12-30):

Hi, I think the address range should be [0x13a2, 0x13aa] which include nine bytes, the same as [0xaabe, 0xaac7]

---

**HAOYUatHZ** (2021-12-30):

Is there any link (for example, on arxiv/iacr) if this paper get revised?

---

**tchapuischkaiban** (2021-12-31):

> Hi, I think the address range should be [0x13a2, 0x13aa] which include nine bytes, the same as [0xaabe, 0xaac7]

[@JiangXb-son](/u/jiangxb-son), No, 0x13aa - 0x13a2 == 8, while 0xaac7 - 0xaabe == 9.

> Is there any link (for example, on arxiv/iacr) if this paper get revised?

[@HAOYUatHZ](/u/haoyuathz) We haven’t put the document on arXiv/iacr or submitted it to a conference. We may do it in the future though. Of course, we will publish the link here if it happens.

---

**spapinistarkware** (2022-01-02):

In word comparison, I see you used a table from 256x256 of all byte comparisons. Couldn’t you have a single table from 256 to positive/negative, and plookup on B1-B2 instead?

Maybe this will even let you do this comparison in 16bit words instead.

---

**OlivierBBB** (2022-01-03):

Hi [@spapinistarkware](/u/spapinistarkware), you raise an interesting point! It seems to me that your solution works and allows for a smaller lookup table indeed, but would also require slightly restructuring the constraints of the Word Comparison module. We would either have to do

- 2 separate plookup checks (one to verify the “Bytehood” of B1 and B2, a second one to verify the sign of their difference),
- or verify the “Bytehood” of B1 and B2 in the execution trace itself and perform 1 plookup check to get the sign of the difference,
- or do everything directly in the execution trace.

Currently our one plookup proof takes care of both “Bytehood” check and the comparison bit `B1 < B2`. I’m not sure which solution is best.

---

**JiangXb-son** (2022-01-04):

Supposed to be a closed interval?     isn`t it?

Looking for your reply

---

**JiangXb-son** (2022-01-05):

Hi, [@OlivierBBB](/u/olivierbbb)  I have a question that on page17, the Prev_PC at step104 should be 92?

---

**tchapuischkaiban** (2022-01-07):

> Supposed to be a closed interval? isn`t it?
> Looking for your reply

Judging from the numerical example this interval is closed on its left bound and open for the right bound (indeed, we should correct the right range symbol)

> Hi, @OlivierBBB I have a question that on page17, the Prev_PC at step104 should be 92?

No, 93 is the right value here: when we return from the smart contract being called, we have to execute the instruction that comes immediately after CALL (which is at PC 93)

Following the same logic, the previous PC for the steps 355-360 should be 355 (that’s another typo).

---

**JiangXb-son** (2022-01-10):

Ok， I know the ideas. thanks, [@tchapuischkaiban](/u/tchapuischkaiban) for your reply.

---

**Softcloud** (2022-01-13):

[@tchapuischkaiban](/u/tchapuischkaiban) Hi, I have some questiions about ram:

1. As described in example 2.1.2, if read/write a word which interior offset is not 0, parent will dispatch two task, let child read/write one word address after another which means child read/write only one word address each time. But why 6.1 say “Store to/load from the memory at most 32 bytes at two consecutive word addresses”? If child read/write only one word address each time, shouldn’t CRAM_BWd_Offset always be equal to Curr_Wd_Offset?
2. In child ram, data is read/write word by word or byte by byte in a row?

---

**franck44** (2022-01-13):

This is great and very detailed descriptions of the operational mode.

If there is an operational semantics for this zk-extension, it could be fed into existing models of the EVM, e.g. the K-framework. [https://github.com/kframework/evm-semantics](https://K-EVM)

This may help designing a prototype implementation/simulator quickly and, as the K-tools generate the simulator you may be able to debug/tune the semantics.

---

**spartucus** (2022-01-17):

Nice spec ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

> To improve the readability of this paper, we have chosen to provide full constraint systems for a few (representative) modules only, which we strive to describe as comprehensively as possible. Other modules, like the main execution trace and the storage module, have been fully designed - however, given the complexity of these components, we chose to postpone slightly their publication. If interested, you may contact us directly for more information on these modules.

Could you please see if you can share the other modules you designed? My curiosity is piqued. Thanks!

---

**tchapuischkaiban** (2022-01-17):

> @tchapuischkaiban Hi, I have some questiions about ram:
>
>
> As described in example 2.1.2, if read/write a word which interior offset is not 0, parent will dispatch two task, let child read/write one word address after another which means child read/write only one word address each time. But why 6.1 say “Store to/load from the memory at most 32 bytes at two consecutive word addresses”? If child read/write only one word address each time, shouldn’t CRAM_BWd_Offset always be equal to Curr_Wd_Offset?
> In child ram, data is read/write word by word or byte by byte in a row?

@[Softcloud](https://ethresear.ch/u/Softcloud):

- First note that, in any case (even if the interior offset is 0), the parent RAM will treat the RETURN operation (the one of example 2.1.2, and any operation that requires interaction between two different memories) using a succession of READ/WRITE requests to the child RAM. Besides, you are right: what is described in the example 2.1.2 is an optimization. If the starting reading interior offset is non zero, we have deliberately chosen to read the last bytes of the first word of the called contract returned memory to perform more efficiently the further READ operations (that would have a zero starting interior offset) - hence, we do not exploit deliberately the fact that one can read/write at most two consecutive word addresses. This read/write at two consecutive word addresses property is however very useful for operations like MSTORE/MLOAD as they can be sent as a single request to the child RAM.
- In the child RAM we can read/write single bytes of the 32-byte words contained at word multiple addresses - hence, in a single row we can either read/modify a single byte of a 32-byte word, or read/replace the full 32-byte word contained at a given word multiple address (optimization for requests that have a zero interior offset).

> This is great and very detailed descriptions of the operational mode.
> If there is an operational semantics for this zk-extension, it could be fed into existing models of the EVM, e.g. the K-framework.
> This may help designing a prototype implementation/simulator quickly and, as the K-tools generate the simulator you may be able to debug/tune the semantics.

@[franck44](https://ethresear.ch/u/franck44), thanks a lot for your positive feedback, we will have a look at the K-framework !

> Could you please see if you can share the other modules you designed? My curiosity is piqued. Thanks!

@[spartucus](https://ethresear.ch/u/spartucus), we will provide the full low level module design in another publication that would be accompanied with some performance metrics from our implementation.

---

**Sin7Y-research** (2023-03-24):

Sin7y Labs, the research team behind Ola, has made a Chinese translation of this paper. I’ll attach it here for anyone who is interested. Please let us know if you have any questions.



      [github.com](https://github.com/Sin7Y/consenSys-zkevm-whitepaper-chinese)




  ![image](https://ethresear.ch/uploads/default/optimized/3X/2/1/216c67209a25707ecbb2581373226f8efbdbdf63_2_690x344.png)



###



Contribute to Sin7Y/consenSys-zkevm-whitepaper-chinese development by creating an account on GitHub.

---

**OlivierBBB** (2023-03-24):

This is interesting, thank you for this effort. Have you had a look at our [updated spec](https://ethresear.ch/t/a-zk-evm-specification-part-2/13903)? Besides some general ideas nothing of the document from this post / thread will make it into our zk-evm. BTW: the updated spec I linked to previously is also out of date (e.g. we redid arithmetic from the ground up.)


*(1 more replies not shown)*
