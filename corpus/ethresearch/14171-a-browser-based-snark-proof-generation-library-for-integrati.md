---
source: ethresearch
topic_id: 14171
title: A browser based snark proof generation library for integrating zk proofs in only a few lines of code
author: madhavanmalolan
date: "2022-11-11"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/a-browser-based-snark-proof-generation-library-for-integrating-zk-proofs-in-only-a-few-lines-of-code/14171
views: 2609
likes: 5
posts_count: 6
---

# A browser based snark proof generation library for integrating zk proofs in only a few lines of code

I’ve packaged snarkjs proof generation for knowledge of the preimage of a hash into a library.

Using the library, the developer only has to write 5 lines of code on javascript front end and 5 lines on Solidity to integrate a zero knowledge proof of preimage to their dapp.

Would love to have a critical code review here!



      [github.com](https://github.com/questbook/browser-snark)




  ![image](https://ethresear.ch/uploads/default/optimized/3X/9/8/98d59830b0f630669ffacb008f06bf0d8c6e5e91_2_690x344.png)



###



generate snark proofs in browser - batteries included

## Replies

**MicahZoltu** (2022-11-12):

Going to be absolutely hell to audit this (like most JS stuff):

[![image](https://ethresear.ch/uploads/default/optimized/2X/f/f210c9217c2f9089132ef02e3c5cb0855168779e_2_482x500.jpeg)image1217×1262 86.4 KB](https://ethresear.ch/uploads/default/f210c9217c2f9089132ef02e3c5cb0855168779e)

You could take an easy win and drop `assert` as a dependency.  That would get rid of a pretty large set of dependencies.  The bigger problem though is `snarkjs` which should be written in plain JS and used as a core library, but instead it has heaps of dependencies.

The problem with having this many dependencies is that it makes auditing incredibly hard, introduces potential supply chain attacks, and leads to problems with licensing:

[![image](https://ethresear.ch/uploads/default/original/2X/9/9d450c1d36fd1facff49ff2147c8cb425ef810f1.png)image308×491 99.5 KB](https://ethresear.ch/uploads/default/9d450c1d36fd1facff49ff2147c8cb425ef810f1)

---

**enricobottazzi** (2022-11-13):

very cool concept! I long thought about something similar. Are you planning to extend it to support other circuits? Using snarkJS in the browser is always painful and it would be great to have an easy-to-use library to extract the most common circuits. I can think of semaphore and zk efficient sig => [GitHub - personaelabs/efficient-zk-sig: Lowering client-side proving cost for private ZK signatures](https://github.com/personaelabs/efficient-zk-sig) as good candidates!

---

**madhavanmalolan** (2022-11-14):

Absolutely that’s the goal. Making circuits and onchain verifiers for most important zk proof verticals.

Next on my radar is semaphore ![:white_check_mark:](https://ethresear.ch/images/emoji/facebook_messenger/white_check_mark.png?v=12)

---

**madhavanmalolan** (2022-11-14):

Thanks for the critical feedback [@MicahZoltu](/u/micahzoltu) !

This is something I hacked together in a day - so surely not optimised. But I hear you - when dealing with security/privacy - there is no slack we can afford.

However, in particular, would like a review of the circom



      [github.com](https://github.com/questbook/browser-snark/blob/3de96213f42b06e870dd7b97e9acab2f0cdd6d05/main.circom)





####



```circom
pragma circom 2.0.0;

include "./circomlib/poseidon.circom";

template Preimage(){
    signal input preimage;
    signal input nonce;
    signal input required;
    signal output result;

    component hash_of_preimage = Poseidon(1);
    hash_of_preimage.inputs[0] =0.7.0 <0.9.0;
library Pairing {
    struct G1Point {
        uint X;
        uint Y;
    }
    // Encoding of field elements is: X[0] * z + X[1]
```

  This file has been truncated. [show original](https://github.com/questbook/browser-snark/blob/3de96213f42b06e870dd7b97e9acab2f0cdd6d05/verifier.sol)

---

**Pandapip1** (2022-11-14):

FYI - since snarkjs uses GPLv3 ([and does not plan to change](https://github.com/iden3/snarkjs/pull/262#issuecomment-1312514495)), it’s not actually usable, since GPLv3 is incompatible with libraries (hence the existence of LGPL).

Don’t use snarkjs until they fix this. You legally can’t, anyway.

