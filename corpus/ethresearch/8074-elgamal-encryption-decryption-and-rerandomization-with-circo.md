---
source: ethresearch
topic_id: 8074
title: ElGamal encryption, decryption, and rerandomization, with circom support
author: weijiekoh
date: "2020-10-06"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/elgamal-encryption-decryption-and-rerandomization-with-circom-support/8074
views: 4452
likes: 5
posts_count: 5
---

# ElGamal encryption, decryption, and rerandomization, with circom support

[MACI anonymization](https://ethresear.ch/t/maci-anonymization-using-rerandomizable-encryption/7054) requires ElGamal cryptographic functions in zero knowledge. Support for anonymization in MACI will come sometime in the future, but I took a stab at implementing its required building blocks:



      [github.com](https://github.com/weijiekoh/elgamal-babyjub)




  ![image](https://ethresear.ch/uploads/default/optimized/3X/e/6/e616f908ae9d28dc2162da130a29f17318d52370_2_690x344.png)



###



Contribute to weijiekoh/elgamal-babyjub development by creating an account on GitHub.










This library implements ElGamal encryption, decryption, and rerandomization in Typescript for the BabyJub elliptic curve. It also provides decryption and rerandomization circuits written in circom.

A quick note about how it encodes plaintext. We define a plaintext value as a BigInt in the BabyJub finite field. To encrypt it, we need to first convert it into a safe BabyJub elliptic curve point. Instead of using a map-to-curve function, the `encodeToMessage` function generates a random value r, computes g ^ {r}, and outputs both g ^ {r} and the x-increment e that must be added to the plaintext to obtain the x-value of g ^ {r}.

The ciphertext is therefore two elliptic curve points and one field element: (c_1, c_2, e).

After decrypting (c_1, c_2) to obtain the elliptic curve point m, we convert it to the original plaintext by computing m_x - e where m_x is the x-coordinate of m.

I’d love any feedback and suggestions on how to improve it. Thanks to [@kobigurk](/u/kobigurk), [@snjax](/u/snjax), and others in the iden3 Telegram group for their help.

## Replies

**MayaDot** (2023-08-30):

I see the decryption and rerandomization, but not the encryption. Does it exist?

Thanks!

---

**stanbar** (2023-12-19):

I couldn’t find the encryption circuit either. But this is what I came up with:

```auto
pragma circom 2.1.2;

include "../lib/circomlib/circuits/bitify.circom";
include "../lib/circomlib/circuits/escalarmulfix.circom";
include "../lib/circomlib/circuits/escalarmulany.circom";
include "../lib/circomlib/circuits/babyjub.circom";

template ComputeC2() {
    signal input r1Bits[253];
    signal input r2;
    signal input messageScalar;
    signal input recipentPublicKey[2];
    signal output xout;
    signal output yout;
    signal output xDelta;

    signal rP[2] <== EscalarMulAny(253)(p <== recipentPublicKey, e <== r1Bits);

    var BASE8[2] = [
        5299619240641551281634865583518297030282874472190772894086521144482721001553,
        16950150798460657717958625567821834550301663161624707787222815936182638968203
    ];

    signal r2Bits[253] <== Num2Bits(253)(r2);
    signal randomPoint[2] <== EscalarMulFix(253, BASE8)(r2Bits);

    (xout, yout) <== BabyAdd()(x1 <== rP[0], y1 <== rP[1], x2 <== randomPoint[0], y2 <== randomPoint[1]);

    xDelta <== randomPoint[0] - messageScalar;
}
```

---

**0xjei** (2024-02-04):

I am bringing up this discussion again because I believe it may be of interest to everyone in here.

The teams at 0x3327 and Privacy & Scaling Explorations (PSE) collaborated on an MVP a few months ago. Although the work is currently on pause but planned (according to the MACI roadmap). Feedback and suggestions on the current design of the solution would be greatly appreciated. I hope will soon become a reality to provide unconditional voter privacy in MACI.

All relevant information can be found in the issue #796 on the MACI repository - kudos to Sam for bringing everything together!

---

**PulpSpy** (2024-02-04):

A few quick comments:

- Elgamal relies on DDH assumption which is only conjectured to hold over BabyJub
- This paper has an implementation (in Zkay not in Circom) and useful information in the appendix: https://files.sri.inf.ethz.ch/website/papers/sp22-zeestar.pdf
- https://github.com/eth-sri/zkay/blob/920e883c095f456770c03606021c728b34497f42/zkay/transaction/crypto/elgamal.py#L32
- Note it is exponential Elgamal, not normal Elgamal

