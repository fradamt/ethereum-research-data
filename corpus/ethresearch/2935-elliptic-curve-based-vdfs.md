---
source: ethresearch
topic_id: 2935
title: Elliptic curve-based VDFs
author: Mikerah
date: "2018-08-15"
category: Sharding
tags: [random-number-generator, verifiable-delay-functions]
url: https://ethresear.ch/t/elliptic-curve-based-vdfs/2935
views: 3590
likes: 15
posts_count: 10
---

# Elliptic curve-based VDFs

I have been going through the VDFs readings list posted by Justin Drake. Here’s a link: https://notes.ethereum.org/52JZtwErThe9KmN6TNd1lg#

I noticed that most of the VDFs constructions so far are based on RSA groups or integer ideals. As a lot of in-use cryptography make heavy use of elliptic curve, would it be good idea to try to build a VDF based on elliptic curves?

## Replies

**vbuterin** (2018-08-15):

If you can find a way how to, sure.

The challenge with elliptic curves is that they have a known group order, so the repeated squaring constructions are trivially short-circuitable.

---

**asanso** (2019-02-21):

So it is a bit late to the party but here it is ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)


      [eprint.iacr.org](https://eprint.iacr.org/2019/166.pdf)


    https://eprint.iacr.org/2019/166.pdf

###

475.59 KB

---

**kladkogex** (2019-02-26):

RSA can be expressed as a bilinear pairing of two mod-prime groups . So I think there should be a way to do to an elliptic VDF by using a pairing of two elliptic curves …

---

**kladkogex** (2019-02-28):

Looks like some people are already working on this


      [eprint.iacr.org](https://eprint.iacr.org/2019/166.pdf)


    https://eprint.iacr.org/2019/166.pdf

###

475.59 KB

---

**asanso** (2019-03-04):

well is the paper I linked above ![:stuck_out_tongue:](https://ethresear.ch/images/emoji/facebook_messenger/stuck_out_tongue.png?v=9)

---

**technocrypto** (2019-03-05):

Personally I’m *way* more interested in post-quantum VDFs than in elliptic curve ones, but ![:woman_shrugging:](https://ethresear.ch/images/emoji/facebook_messenger/woman_shrugging.png?v=9)

---

**burdges** (2019-03-16):

We need post-quantum key exchanges right now because future quantum computers might break messages encrypted today.

We’d prefer post-quantum signatures be deployed at the moment a quantum computer comes online.  We only push for post-quantum signatures sooner because deployment takes ages.  Also, there is a good case that quantum annoying signatures suffice for at least some time after a quantum computer comes online.  And quantum annoying signatures might help prove a quantum computer exists in secret.

There is a much stronger argument that deployed VDFs need only be quantum annoying at the moment a quantum computer comes online.  In essence, we expect that

- the first quantum computers should be too expensive and slow for an attack,
- VDFs are already vulnerable to super-conducting computing, ASICs, better ASICs, etc., which demands more robust usage from deployments.

Both Wesolowski’s and Pietrzak’s VDFs are already quantum annoying, if using the prefered class group instantiation where you hash to p.  Also the isogenies VDF is quantum annoying.  Among the serious VDF proposals, only the RSA VDF is not quantum annoying.

We should eventually devise a real post-quantum VDF that is compact , but we’re looking pretty good right now.

In this vein, VRFs are like signatures in that quantum annoying suffices for now, but we do want a post-quantum VRF eventually.  It’s true hash chaining like RANDAO gives a VRF with singleton domain, except these suck and real VRFs have so many uses in consensus algorithms.  I suppose hash-based signatures and zkSTARKs should both provide VRFs but they’re both too large for consensus protocols.  It’s dubious if lattice-based techniques can ever yield a compact VRF.  Isogenies seem like our best bet for a post-quantum VRF that is both compact and flexible.  I’m super happy the construction in [@asanso](/u/asanso) 's paper gives a quantum annoying VRF .

---

**asanso** (2019-03-18):

Nice analysis . [@burdges](/u/burdges) any chance you can put a link for [@asonnino](/u/asonnino) VRF’s   quantum annoying VRF paper ?

---

**burdges** (2019-03-18):

oops!  I miss-typed your name there [@asanso](/u/asanso), I only meant the same BLS-like verification equation from your paper gives a quantum annoying VRF:

e_X(\psi(G_1), H(m)) = e_Y(G_1, \phi(H(m)))

