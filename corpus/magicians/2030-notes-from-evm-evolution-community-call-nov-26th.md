---
source: magicians
topic_id: 2030
title: Notes from EVM Evolution Community Call Nov 26th
author: boris
date: "2018-11-27"
category: Magicians > Primordial Soup
tags: [community-call, evm-evolution]
url: https://ethereum-magicians.org/t/notes-from-evm-evolution-community-call-nov-26th/2030
views: 1713
likes: 1
posts_count: 2
---

# Notes from EVM Evolution Community Call Nov 26th

Today we had an [evm-evolution](/tag/evm-evolution) Community Call. The [full transcript is on HackMD](https://hackmd.io/g0yKhTn3TYaThqFWVjF4Ow) and the original [agenda / discussion is on Github](https://github.com/spadebuilders/community/issues/14).

*Perhaps Community Call agendas should be posted on here in the first place, rather than Github? Still experimenting!*

A lot of the discussion was with the Trail of Bits team and their needs / the needs of the security & assurance community in tools that help analysis. Their SlithIR is designed for this. More discussion and clarity on how LLVM, various intermediate representation (IR) formats, EVM, and eWASM work together in the future is needed.

I’ll paste in the end of the agenda discussion from [@gcolvin](/u/gcolvin) on an implementation plan:

> On reinspection, Aleth version is now EVM-C wrapped, and EVM 1.5 code fairly recently removed. So I’d say that path of least resistance is to get EIP-615 working in Aleth again and then port to Parity via EVMC.

Greg is the author of EIP615 and had some code around this last year.

Below are the action items I captured:

## Action Items

### Plan an All EVM Call



      [github.com/spadebuilders/community](https://github.com/spadebuilders/community/issues/20)












####



        opened 10:45PM - 26 Nov 18 UTC



          closed 03:13AM - 26 Mar 19 UTC



        [![](https://ethereum-magicians.org/uploads/default/original/2X/a/aebcc628e5b9c425f8c817670e259726bdcd884e.png)
          bmann](https://github.com/bmann)





          planned


          evmevolution







We had ETC Cooperative on the Community Call #14. There are many other blockchai[…]()ns that run EVM or EVM compatible smart contracts.

Can we coordinate and collaborate more broadly among all these chains to get a better VM for everyone?

Making a list of EVM compatible chains / clients and who to contact is likely the first step. Will create a markdown file for that in this repo.












- Need to make a list of EVM compatible clients / chains and gather contacts
- Brooke / Boris will meet with ETCDEV contacts as well

### Get clarity on ETH 1.x roadmap around EVM1.5 and eWASM



      [github.com/spadebuilders/community](https://github.com/spadebuilders/community/issues/19)












####



        opened 10:36PM - 26 Nov 18 UTC



          closed 01:57PM - 27 Nov 18 UTC



        [![](https://ethereum-magicians.org/uploads/default/original/2X/a/aebcc628e5b9c425f8c817670e259726bdcd884e.png)
          bmann](https://github.com/bmann)





          evmevolution







As part of working on EVM, would like more clarity about ETH1.x roadmap and eWAS[…]()M.

As per Casey's post on EthMagicians, there is this line:

> (3) improved developer experience with VM upgrades including EVM 1.5 and Ewasm

EIP615 is specifically called out -- great to see that there seems to be good consensus around this already.

In a tweetstorm, [Martin Koeppelman says](https://twitter.com/koeppelmann/status/1066009676331053056?s=21):

> WASM early in limited form as a pre-compile...

No idea what this means. Talk to @lrettig and others to find out more.












Goal is to have EVM Evolution support this process and provide expertise from security, VM, and other experts. The question marks here likely need a discussion with [@lrettig](/u/lrettig), others from the eWASM team. Not sure where to look for this information or where discussion is happening.

### What is the process of rolling out EIP615 Static Jumps and other EVM opcode additions



      [github.com/spadebuilders/community](https://github.com/spadebuilders/community/issues/18)












####



        opened 10:31PM - 26 Nov 18 UTC



          closed 02:02AM - 01 Mar 19 UTC



        [![](https://ethereum-magicians.org/uploads/default/original/2X/a/aebcc628e5b9c425f8c817670e259726bdcd884e.png)
          bmann](https://github.com/bmann)





          in progress


          evmevolution







Write up a high level set of steps to help explain how new EVM opcodes get rolle[…]()d out. Focus on [EIP615 Static Jumps](https://github.com/ethereum/EIPs/issues/615).












- First high level notes / process here Process of rolling out EIP615 Static Jumps and other EVM opcode additions - HackMD
- Will create tracking issues for this process – e.g. PR against Yellow / Jello paper is the likely next step

---

General consensus continues to be that EIP615 is valuable and should get implemented, and that more learning / explanation around VMs and IRs to be done.

Further explanation to the wider community is needed on how [SlithIR](https://github.com/trailofbits/slither/wiki/SlithIR) – an intermediate representation designed for analysis for security purposes – is highly useful, and that Yul and/or LLVM are lower level IRs that can be used for performance optimization, but don’t help with security analysis.

Some discussion on funding and funding sources. Trail of Bits applied to EF with Slither / SlithIR tools, wasn’t approved. Trail of Bits happy to put some time in and collaborate with SPADE, others in moving this forward.

Brooke has a personal TO DO to correct / clarify some statements around EVM and eWASM designs.

Boris [working on diagrams](https://docs.google.com/presentation/d/1UDW1KsNc5w8xaFLWaisn_ZFqWcflZHWs-_FUpDq_2kk/edit#slide=id.g4957478a19_0_0) to help communicate – Dan shared some SlithIR and related writing that is helpful.

## Replies

**boris** (2018-11-27):

[@lrettig](/u/lrettig) just posted the eWASM working group proposal [Ewasm working group proposal for Eth 1.x](https://ethereum-magicians.org/t/ewasm-working-group-proposal-for-eth-1-x/2033)

Which answers some of the questions about the precompile comment that didn’t make any sense.

I’ll close the tracking issue I had opened.

So essentially this means EVM side by side with eWASM in clients so that eWASM is used to execute precompiles.

