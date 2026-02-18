---
source: ethresearch
topic_id: 15553
title: A research on MEV transaction detection using Graph Neural Networks
author: wanify
date: "2023-05-11"
category: Economics
tags: [mev]
url: https://ethresear.ch/t/a-research-on-mev-transaction-detection-using-graph-neural-networks/15553
views: 1673
likes: 4
posts_count: 1
---

# A research on MEV transaction detection using Graph Neural Networks

We are excited to share our paper on MEV detection method using Graph Neural Networks (ArbiNet) ![:grinning_face_with_smiling_eyes:](https://ethresear.ch/images/emoji/facebook_messenger/grinning_face_with_smiling_eyes.png?v=14)


      ![](https://ethresear.ch/uploads/default/original/3X/7/7/7737f9c766957e34da6871902e1e7a9d2aca40f3.png)

      [arXiv.org](https://arxiv.org/abs/2305.05952)



    ![](https://ethresear.ch/uploads/default/optimized/3X/c/d/cd49b65780faf86c14ed9761c9c522acfb73adde_2_500x500.png)

###



The detection of Maximal Extractable Value (MEV) in blockchain is crucial for enhancing blockchain security, as it enables the evaluation of potential consensus layer risks, the effectiveness of anti-centralization solutions, and the assessment of...










Our code, pre-trained models, and preprocessed graphs are available here:



      [github.com](https://github.com/etelpmoc/arbinet)




  ![image](https://ethresear.ch/uploads/default/optimized/3X/5/5/55b4abc9f1e9bfe682e67383b7757db1cece9ad4_2_690x344.png)



###



Contribute to etelpmoc/arbinet development by creating an account on GitHub.










We’ll open-source all of our labeled MEV data (from block 10,000,000 to 17,000,000) in our drive folder After organizing the data.

This work was supported by Ethereum Academic Grants program. Many thanks to [@dankrad](/u/dankrad) [@barnabe](/u/barnabe) for support and assistance.

Abstract of our paper:

The detection of Maximal Extractable Value (MEV) in blockchain is crucial for enhancing blockchain security, as it enables the evaluation of potential consensus layer risks, the effectiveness of anti-centralization solutions, and the assessment of user exploitation. However, existing MEV detection methods face limitations due to their low recall rate, reliance on pre-registered Application Binary Interfaces (ABIs) and the need for continuous monitoring of new DeFi services.

In this paper, we propose ArbiNet, a novel GNN-based detection model that offers a low-overhead and accurate solution for MEV detection without requiring knowledge of smart contract code or ABIs. We collected an extensive MEV dataset, surpassing currently available public datasets, to train ArbiNet. Our implemented model and open dataset enhance the understanding of the MEV landscape, serving as a foundation for MEV quantification and improved blockchain security.

[![Overall Method](https://ethresear.ch/uploads/default/optimized/2X/b/bc6f43866d21b8ca40239d3db71f30899273b830_2_690x167.png)Overall Method3008×732 266 KB](https://ethresear.ch/uploads/default/bc6f43866d21b8ca40239d3db71f30899273b830)

https://twitter.com/a41littlepeople/status/1656490951098142720?s=20
