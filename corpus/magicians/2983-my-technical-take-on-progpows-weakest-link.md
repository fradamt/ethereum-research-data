---
source: magicians
topic_id: 2983
title: My technical take on ProgPow's weakest link
author: jcyr
date: "2019-03-25"
category: EIPs
tags: [progpow]
url: https://ethereum-magicians.org/t/my-technical-take-on-progpows-weakest-link/2983
views: 4881
likes: 40
posts_count: 56
---

# My technical take on ProgPow's weakest link

First let me say that I’ve worked extensively with the algorithm, and as far as I’m concerned it is sound and meets its objective of evening the mining playing field. As proposed ProgPow creates a new pseudo random sequence of OpenCL or CUDA code every 10 blocks or so. In order to run on the GPUs this code is just-in-time recompiled at run-time with each new ProgPow period. In an ideal world that would be fine, but compilers (specially optimizing compilers) are incredibly complex beasts and are subject to undiscovered and subtle bugs.

Case in point, while working with ProgPow I stumbled  on such a bug in all current AMD drivers (both Linux and Windows). Progress in resolving the issue at AMD is slow as the bug report was opened and acknowledged some 2 months ago (initially announced by ifdefelse here: https://medium.com/@ifdefelse/progpow-progress-da5bb31a651b) . In that instance the high level code was generated correctly by the miner but for some random sequences and ProgPow periods the generated GPU code was incorrectly compiled. Workarounds where found and implemented, but it got me to thinking… what if something like this had happened on the main net? All of the AMD miners (a majority of which use the driver in question) would start generating invalid solutions for all blocks within any given and unpredictable ProgPow period. Fairly catastrophic events!

Reliance on the dynamic use of 3rd party compilers is the weakest link in the ProgPow chain. OpenCL and CUDA compiler versions can change with any driver release, and ProgPow has many attributes of a compiler fuzz tester. It becomes a prime candidate for exposing these unknown compiler optimization issues. Given the pseudo random nature of the dynamically generated code, the nearly infinite variations, and the fact that it is only compiled at run time, it is nearly impossible to do any advance testing of these code sequences. I wouldn’t ignore the likelihood of such bugs cropping up unpredictably in the future.

## Replies

**gcolvin** (2019-03-25):

I’m placing a link to this discussion on AllCoreDevs because I think it is a potential showstopper.

---

**shemnon** (2019-03-25):

I think very good mitigations exist and are already practiced.

First, full scale impact on a newly introduced bug in a compiler update is unlikely.  There are many strategies for that such as canaries and incremental rollout to address such regular critical bugs.  Microsoft just had one with Windows where entire drives were being corrupted, but it was discovered during incremental rollout. Any DevOps worker that gets an OS, driver, or toolchain update and immediately rolls it out to 100% of the fleet will not be in the industry long.

Second, the impact is limited.  It only affects the hashrate of the particular card vendor on the particular toolchain version.  This would not impact the transactions encoded in the block bodies nor any of the other data, it would only impact the proof of work generation.  If a nightmare scenario hit and half the cards went offline the difficulty would correct itself in a number of hours.  Figure in the fact the program changes every 10 blocks it may self correct sooner.

> it is nearly impossible to do any advance testing of these code sequences

False, the upgrades can be validated well in advance.  The programs are deterministic based only on block number and not on the content of the chain.  Correct hashing can be tested and program performance can be forecasted well in advance of the actual block mining.  Just run the miner with the new targeted block number.  This may become a recommended practice to “future proof” a certain amount of blocks to validate that there will be no compiler problems.

Certainly worth discussing in core devs, but I don’t foresee it becoming a showstopper, but a risk a miner would need to plan around.  The mining community may have a different opinion on this however.

---

**Anlan** (2019-03-25):

What @jean-m-cyr has found is true and and it’s been reported to AMD engineers. The so called “bogus period” flaw affects, actually, only AMD OpenCL compiler. Nvidia OpenCL compiler is not affected. With a trial and error procedure was also found a workaround which (interestingly enough) also slightly improved performance. #pragma unroll 2 on progpowLoop.

This said is pretty easy to test, at current releases of drivers (any), periods from here to 3 or 4 years ahead.

The problem itself is mitigated however. Most of the OpenCL kernels for ethash too are compiled on the fly when the instance of a miner starts: there are some exceptions though when OpenCL kernels are delivered bound to the miner in binary (pre-compiled) format.

In history of software driven miners is not the first time a driver upgrade causes erratic results or serious losses in performance. But when this happens it’s pretty obvious (for miner) to roll back to previous versions while the issue is being reported to respective engineers. AMD for example had to release the so called “BlockChain drivers” to solve several issues caused by increased DAG size.

---

**jcyr** (2019-03-25):

You are correct that OpenCL code is mostly compiled on the fly. The difference is that Ethash code is static and can be thoroughly tested prior to release. Not the case with with pseudo randomly generated code.

---

**salanki** (2019-03-25):

That things can break when you update a driver is a known fact. The number of people who mine and just let Windows Update auto-update their drivers are very small. Most of the network is run in Hive OS, ethOS and vanilla Linux. The two former do rigorous testing before they include a new driver.

With that said, I would recommend that miner software developers include a regression testing mode that runs through a bunch of ProgPoW periods to allow easier testing of new driver testing. Since the programs are pseudo-random and not truly random, one can conclusively test all generated programs ahead of time.

---

**shemnon** (2019-03-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jcyr/48/133_2.png) jcyr:

> Not the case with with pseudo randomly generated code.

The code is deterministic in its output, purely as a function of the block number.  This can be validated and tested in a brute-force fashion in O(n) time.

---

**jcyr** (2019-03-25):

It’s good that you acknowledge the issue and are thinking about ways to mitigate. In assessing the risk however we must also accept that verifying static code, as opposed to dynamically generated pseudo-random code known to stress optimizing compilers, are two entirely different things.

---

**jcyr** (2019-03-25):

So far it has been suggested that all ProgPow periods 2-3 years into the future could be generated and tested prior to release, combined with strict driver and toolchain version verification to guard against potentially incompatible or unverified tools.

Less general, more error prone, but would address the issue.

---

**jcyr** (2019-03-26):

With the progpow period at 10 blocks, and avg. block time at 12 minutes. Testing 2 years worth of ProgPow sequences represents nearly 9,000 test cases!

Then you’d need to test for all architectures, but we already have to do that now.

I’d much rather constrain the number of possible randomized sequences to a number that is still prohibitive for ASICs but that can be statically compiled. Not a new idea, I know. Other aspects of ProgPow such as large state, heavy use of fast on-chip memory already make the algorithm expensive for ASIC.

---

**shemnon** (2019-03-26):

The question is how fast is the compiler.  10ms is 90 seconds.1 second is 2 and a half hours.  Not unreasonable for a final check test.  And what you really care about is the next few months.

---

**Anlan** (2019-03-26):

[@shemnon](/u/shemnon) The speed of the compiler is irrelevant. As compilation is done async while previous compiled kernel is searching its weight is negligible. Just for sake of precision an avg compile time goes from 250ms to 1.2 s depending on CPU and IO speed.

At miner instance startup the compilation happens while DAG is being generated thus, once again, no delays.

---

**jcyr** (2019-03-26):

[@Anlan](/u/anlan) I believe [@shemnon](/u/shemnon) was referring to the time it would take to run the requisite 2-3 years worth of ProgPow period testcases.

---

**jcyr** (2019-03-26):

Not directly related to this specific issue, but another friction point is the Windows DLL hell miner devs would need to contend with. The run-time compiler support DLLs for Nvidia are only included in the CUDA toolkit, a 2+GB download. My understanding of the Nvidia license is that those DLLs can’t be delivered separately from the entire toolkit. The current method of packaging the DLLs with the miner seems to violate the terms of the Nvidia license.

---

**Anlan** (2019-03-26):

Oh I see … but then again the speed of compiler is irrelevant. What really matters is how much time a search kernel takes to find the right nonce which is a matter of the difficulty we target to and the champion machine(s) we use (1 Gpu ? 2 ? 6 ?). Assuming a fixed header hash and a very low diff the whole test can be carried out maybe quicker than 2 hours.

---

**Anlan** (2019-03-26):

In regard of DLLs my initial intention was( and is ) to completely remove any nvidia library in the miner package. Instead it will detect if necessary libraries are installed and eventually it’s up to the end user to install them from vendor. “You have to install CUDA toolkit from …”

---

**jcyr** (2019-03-26):

Sure, you can place the onus on the user to sort things out. I guess my gut feeling is that we are building a cumbersome and fragile construct.

---

**Anlan** (2019-03-26):

I may be well wrong but I don’t see it as a huge problem. While I agree most “occasional” miners are “copy and paste -> next -> next save” almost not knowing what they’re doing, on a development perspective is way easier to mantain a miner which is not bound to particular CUDA releases or Driver versions. Actually mainstream ethminer has a release for CUDA 8, one for CUDA 9.x and one for CUDA 10 due to the nvidia fat loader.

It all ends up in providing the most exhaustive knowledge base.

---

**xazax310** (2019-03-26):

As a miner, I’d like to chime in here and give me a short idea of what a typical miner would look for in a miner program. For the most part, as Andrea has said, many wouldn’t even bother doing extensive testing. A) Does it work? B) Is my hashrate as advertised by the miner? C) Are my submitted pool shares/payout correct for the hashrate. Check off all answers they start using it.

It seems to me test the compiler for years on out in a minersoftware seems wasteful. At most I’d say 6+ month lead time due to the changing landscape of crypto and further bug swatting/fixes. Again it’s not ProgPoW Algorithm that’s the failure here but something with AMD openCL compiler.

[@jcyr](/u/jcyr) Isn’t this something we could test/find out in a Testnet scenario? If there would be some major flaw that could cause any failures because of AMD miners. This would have become fairly evident.

[@Anlan](/u/anlan) I would assume since it’s an AMD openCL issue, the ROCm wouldn’t be affected by this same issue? This is something Linux users, a majority of miners which use, could totally avoid. SMOS, PimpOS, HiveOS, ETHos are popular Linux mining systems many use and I’m sure would use ROCm. I believe HiveOS already does for Vega’s.

---

**jcyr** (2019-03-26):

[@xazax310](/u/xazax310) We ran with this on a testnet for some time before it became evident. And yes, it is not the algorithm that bugs me, but rather it’s increased dependence on 3rd party tools.

---

**greerso** (2019-03-26):

nvrtc is distributable according to https://docs.nvidia.com/cuda/eula/#attachment-a


*(35 more replies not shown)*
