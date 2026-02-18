---
source: ethresearch
topic_id: 9613
title: Kate commitments in ETH
author: g11in
date: "2021-05-25"
category: Cryptography
tags: [polynomial-commitment]
url: https://ethresear.ch/t/kate-commitments-in-eth/9613
views: 2599
likes: 7
posts_count: 4
---

# Kate commitments in ETH

Hi Guys,

just bringing attention to a document I collated regarding proposed use of Kate Commitments in ETH. Hope it makes it makes it easy for you to get the context regarding the same.


      ![](https://ethresear.ch/uploads/default/original/2X/0/0e059a8feebbdf6b4348f5049c9408cfc998331c.png)

      [HackMD](https://hackmd.io/yqfI6OPlRZizv9yPaD-8IQ?view)



    ![](https://ethresear.ch/uploads/default/optimized/3X/c/d/cd231863ebeb783c60343a8e1e943178c5cb44c7_2_690x362.jpeg)

###










Happy to discuss and learn more here through conversations on the topic ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)

## Replies

**kladkogex** (2021-05-25):

Whats the best opensource library for Kate commitments?

---

**g11in** (2021-05-25):

You can easily find the sample code for reference here (this also includes the python code links).



      [github.com](https://github.com/protolambda/go-kzg)




  ![image](https://ethresear.ch/uploads/default/optimized/3X/9/7/9793048697b5e67770de5ee1dd493d61110438f1_2_690x344.png)



###



FFT, data-recovery and KZG commitments, a.k.a. Kate commitments, in Go - *super experimental*










most of operations are on the BLS curve so the BLS libraries that ETH POS clients are using should do the trick as they would also have the pairing function, currently used for verifying attestation aggregation (i think).

---

**g11in** (2021-06-06):

updated the [notes section](https://hackmd.io/yqfI6OPlRZizv9yPaD-8IQ?view#Note31-t-can-be-treated-as-Hash-of-t-as-obtaining-t-from-t-is-discrete-log-problem-known-to-be-intractable-for-secure-curves) with more properties of kate, for better understanding.

