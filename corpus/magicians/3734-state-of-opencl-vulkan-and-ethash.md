---
source: magicians
topic_id: 3734
title: State of OpenCL, Vulkan, and Ethash
author: wschwab
date: "2019-10-30"
category: Working Groups > Ethereum 1.x Ring
tags: [mining]
url: https://ethereum-magicians.org/t/state-of-opencl-vulkan-and-ethash/3734
views: 4743
likes: 6
posts_count: 10
---

# State of OpenCL, Vulkan, and Ethash

Hi! I seem to have fallen down a rabbit hole, and thought the Magicians might be a good place to find more information. This is a new topic for me, so there may be some gross misunderstandings. If there are, I’d love to get set straight.

The current Ethash miners seem to be using OpenCL or CUDA for mining. CUDA doesn’t work on AMD, so for AMD the current option is only OpenCL. OpenCL on AMD means relying on AMD’s drivers, which are, um, famously ungood. Mesa (open-source graphics suite on Linux) already performs at least as well as the proprietary drivers. The problem is that Mesa hasn’t implemented OpenCL, only OpenGL (and Vulkan, see below). As in, Mesa has the graphics layer (OpenGL), but not the compute (which is what mining needs).

Enter Vulkan. Vulkan has its own compute layer, though I don’t think it has been integrated with OpenCL ([yet](https://github.com/google/clspv)). Searching [vulkan compute](https://duckduckgo.com/?q=vulkan+compute) turns up existing code leveraging Vulkan’s compute, and there’s even an existing [XMR miner written for Vulkan](https://github.com/enerc/VulkanXMRMiner).

A Vulkan Ethash miner would allow miners to use a more robust open-source suite to power their GPUs, especially with regards to AMD hardware. This may allow entry to more hobbyist miners. Increased efficiency from GPUs (assuming Vulkan outperforms current CUDA and OpenCL implementations) should theoretically raise the difficulty of making a profitable ASIC.

Should there be an initiative to try to persuade Ethash miners to incorporate Vulkan?

Right now there isn’t OpenCL - Vulkan interoperability, though I linked Google’s project above. I’m assuming that once there is OpenCL support, Ethash miners would all work with Vulkan out of the box. That may make it hard to incentivize work. Then again, OpenCL support hardly seems around the corner. The XMR Vulkan miner utilized Vulkan’s own intermediate language to build their miner. I don’t know how formidable a task it would be to write new ones, or port the XMR miner’s. Perhaps the XMR team should be reached out to?

Another thing to bear in mind is the looming presence of Proof-of-Stake. I do not know to what extent it has disincentivized Ethash miner development, but further work is almost certainly justified since 1) the Eth 1.x chain may yet live on inside of Eth 2, and 2) even if it doesn’t , other blockchains use Ethash.

So that’s it for now. I wanted to get a conversation rolling on this, and I’m interested in what the community thinks. Looking forward!

## Replies

**chfast** (2019-10-31):

In practice for AMD GPUs assembly kernels compiled offline to binaries are used: https://github.com/ethereum-mining/ethminer/tree/master/libethash-cl/kernels. They have proved to be better than OpenCL compiled by any compiler. I don’t think using Vulcan instead of OpenCL make any sense.

Secondly, not many people are interested in developing mining software in open-source model.

---

**wschwab** (2019-10-31):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/chfast/48/3235_2.png) chfast:

> In practice for AMD GPUs assembly kernels compiled offline to binaries are used

Do you mean that Ethminer is using the AMDGPU-PRO drivers for microcode, but not for their OpenCL implementation? I’ll readily admit that I’m more than a bit out of my depth here. I know that Ethminer relies on the proprietary AMD drivers (AMDGPU-PRO), and I know the library that you linked to is called `libethash-cl`, which leads me to assume that it has some kind of relationship with OpenCL. You have a better handle on the process than me, it seems - could you descibe the process in a bit more detail?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/chfast/48/3235_2.png) chfast:

> Secondly, not many people are interested in developing mining software in open-source model.

It could be I didn’t explain myself well. No one would need to completely open-source their miner. The drivers needed to make the miner work would be open-source. I gave some reasons why I think that’s a good thing above.

---

**chfast** (2019-10-31):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wschwab/48/1041_2.png) wschwab:

> Do you mean that Ethminer is using the AMDGPU-PRO drivers for microcode, but not for their OpenCL implementation? I’ll readily admit that I’m more than a bit out of my depth here. I know that Ethminer relies on the proprietary AMD drivers (AMDGPU-PRO), and I know the library that you linked to is called libethash-cl , which leads me to assume that it has some kind of relationship with OpenCL. You have a better handle on the process than me, it seems - could you descibe the process in a bit more detail?

OpenCL is used to communicate with GPU, but the kernel is not compiled by the compiler from the GPU driver. Kernels are already precompiled and only binaries are loaded. And they are written in GPU assembly, not in OpenCL C.

---

**wschwab** (2019-10-31):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/chfast/48/3235_2.png) chfast:

> OpenCL is used to communicate with GPU

So my question is,I would’ve thought that introducing a library for using Vulkan (SPIR-V) to communicate with the GPU would be beneficial. Is there some merit to that?

If so, how might such a thing be accomplished?

---

**chfast** (2019-10-31):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wschwab/48/1041_2.png) wschwab:

> So my question is,I would’ve thought that introducing a library for using Vulkan (SPIR-V) to communicate with the GPU would be beneficial. Is there some merit to that?

No. We already have assembly code for kernels. Using SPIR-V is a step backward.

---

**wschwab** (2019-10-31):

Ah! I think I’m getting it now. SPIR-V is the layer for what is actually running on the GPU, which Ethminer is already doing in assembly. OpenCL is the layer which bridges between the computer and the GPU. Is that right?

(Looking back, I probably should’ve figured that out earlier.)

---

**chfast** (2019-10-31):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wschwab/48/1041_2.png) wschwab:

> Ah! I think I’m getting it now. SPIR-V is the layer for what is actually running on the GPU, which Ethminer is already doing in assembly. OpenCL is the layer which bridges between the computer and the GPU. Is that right?

SPIR-V is a language (actually is Intermediate Representation, IR) that is later “compiled” by the GPU driver to assembly that runs directly on GPU. In Ethminer, we already have this end assembly representation (they are different for different GPU series).

SPIR-V would be useful providing that the compiler included in the GPU driver is good enough to produce the final representation that performs the same as the assembly kernels from Ethminer. Then using SPIR-V (or any other language) would be better because you can target newer GPUs which we don’t have assembly kernels for.

Still, I believe not many people are interested in this work. That’s what I meant by the “open-source” comment. I don’t mean the open-source licenses. The Ethminer project stopped being developed because there was not interest nor support in continuing working on it.

---

**wschwab** (2019-10-31):

Thanks a bunch, [@chfast](/u/chfast)! Your posts have helped me understand the situation much better. One last comment, a bit more off-topic:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/chfast/48/3235_2.png) chfast:

> The Ethminer project stopped being developed because there was not interest nor support in continuing working on it.

While this is a shame, I’m not entirely certain that this is about open-source. Claymore doesn’t seem to have updated since roughly the same time as Ethminer, and I’m none too certain that any of the other closed-source miners are being developed in a meaningful way. It’s hard for me to prove that, but it is certainly the feeling I’ve gotten.

---

**ecclesias** (2019-11-05):

I’d personally like to see something developed with Vulkan…

