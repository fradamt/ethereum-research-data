---
source: ethresearch
topic_id: 17452
title: Deep learning-based solution for smart contract vulnerabilities detection
author: Mirror
date: "2023-11-17"
category: Security
tags: []
url: https://ethresear.ch/t/deep-learning-based-solution-for-smart-contract-vulnerabilities-detection/17452
views: 985
likes: 1
posts_count: 1
---

# Deep learning-based solution for smart contract vulnerabilities detection

Read the original article：

https://www.nature.com/articles/s41598-023-47219-0

**key Message:**

Compared to static tools with fixed rules, deep learning doesn’t rely on predefined rules, making it adept at capturing both syntax and semantics during training, learning vulnerability features more accurately.

[![image](https://ethresear.ch/uploads/default/optimized/2X/3/385a0fc75bb27bf2bb79a4884919bba807f7f318_2_690x304.jpeg)image1920×848 139 KB](https://ethresear.ch/uploads/default/385a0fc75bb27bf2bb79a4884919bba807f7f318)

**Main Results:**

The proposed Optimized-CodeBERT model achieves the highest recall compared to these static tools.

The proposed Optimized-CodeBERT model outperforms other deep learning models, reaching the highest F1 score in comparison.

Improved the model’s performance in vulnerability detection by obtaining feature segments of the vulnerability code.

The CodeBERT pretrained model is employed to represent text, thereby improving semantic analysis capabilities.

[![image](https://ethresear.ch/uploads/default/optimized/2X/b/b94f7af6fba622c159a1c14f5f60eccdfb489411_2_540x500.jpeg)image1920×1777 143 KB](https://ethresear.ch/uploads/default/b94f7af6fba622c159a1c14f5f60eccdfb489411)

**Methods:**

Study type: Experimental

Study aim:  Exploring the detection capabilities of deep learning models in smart contract vulnerability detection, assessing whether they outperform traditional static analysis tools.

[![image](https://ethresear.ch/uploads/default/optimized/2X/d/d31bfb0a33b7b58d86b5dad23002213ada9017ec_2_362x500.jpeg)image1594×2200 121 KB](https://ethresear.ch/uploads/default/d31bfb0a33b7b58d86b5dad23002213ada9017ec)

**Experiments:**

A solution is introduced which is based on deep learning techniques. It contains three models: Optimized-CodeBERT, Optimized-LSTM, and Optimized-CNN.

Training with feature segments of vulnerable code functions to retain critical vulnerability features.

The proposed Optimized-CodeBERT pretrained model for text representation in data preprocessing.

[![image](https://ethresear.ch/uploads/default/optimized/2X/2/29c2236fd56b1045fb3912f7ea94cff612ff4aff_2_684x500.png)image968×707 109 KB](https://ethresear.ch/uploads/default/29c2236fd56b1045fb3912f7ea94cff612ff4aff)
