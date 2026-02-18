---
source: ethresearch
topic_id: 8619
title: Implementation of Gonzalez-Llamas fully homomorphic encryption (obfuscation soon)
author: haael
date: "2021-02-02"
category: Cryptography
tags: []
url: https://ethresear.ch/t/implementation-of-gonzalez-llamas-fully-homomorphic-encryption-obfuscation-soon/8619
views: 1900
likes: 3
posts_count: 7
---

# Implementation of Gonzalez-Llamas fully homomorphic encryption (obfuscation soon)

So I wanted to announce that I finished the first version of FAPKC0 cipher and Gonzalez-Llamas homomorphic cipher based on it.

FAPKC is a family of ciphers based on composition of finite automata. Since finite automata are computational devices, they can do more than just encryption, so homomorphic operations are possible, and also functional encryption and white-box obfuscation.

This cryptosystem is extremely robust, fast and easy to use. It should be possible to obfuscate actual programs written in programming languages, not some abstract algebraic description of the problem.

Homomorphic encryption could be used to enhance Ethereum with privacy features, like a smart contract with secret state.

Some minor modifications to Gonzalez-Llamas homomorphic scheme could yield a working obfuscation algorithm. With obfuscation a whole new set of possibilities open, that will have huge impact on Ethereum and other blockchains.

- Obfuscation could be used to speed up boot time of nodes joining the network. Instead of verifying the blockchain from the beginning, they could rely on a trusted proof that certain checkpoint is valid.
- Obfuscation could be used to offload execution of smart contracts to the user itself. Miners will not have to execute contracts (only ensure the order of the methods called), the users will excersise their own computing power.
- Obfuscation could be used to control resources outside the blockchain, if the obfuscated program is embedded the credentials.

Please test the code here:



      [github.com](https://github.com/haael/white-box-fapkc)




  ![image](https://ethresear.ch/uploads/default/optimized/3X/5/5/55879819720290e84b9f3c0bdc96482f76329114_2_690x344.png)



###



White-box cryptography based on FAPKC algorithm










(Please run the script `automaton.py`.)

I wrote a simple program that converts ASCII strings to lowercase. The script can perform conversion to lowercase on ciphertext.

I am calling for feedback! Anyone who wants to help, please contact me.

## Replies

**kladkogex** (2021-02-02):

Hey Bartosz,

This is fantastic!

Can you give some simple examples of what can be done using this, and also computational requirements and running time  ![:imp:](https://ethresear.ch/images/emoji/facebook_messenger/imp.png?v=9)

---

**haael** (2021-02-02):

You can do everything that can be represented as finite automaton, that means any algorithm that uses constant number of variables (no unbounded lists).

To calculate the running time, you have to count the number of instructions that take to run your program. The real speed will have to be measured on AES implementation. For now I just made a program converting text to lowercase that has 85 instructions and its homomorphic image has 53k instructions, that means about 600-fold slowdown. Still, it takes under a second to run.

I made a JIT compiler with LLVM to speed up the execution of the automaton itself (encryption, decryption, homomorphic operations), so it’s blazingly fast. The biggest bottleneck for now is the key generation, which can take several dozen minutes. Also, the automata need an optimization pass, which is very slow and sometimes will never finish, so an improvement is necessary.

Will you be interested in helping? Can you try to run it? Also, would you like to write a paper with me, or do you know someone who would be interested?

---

**sherif** (2021-02-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/haael/48/5400_2.png) haael:

> Homomorphic encryption could be used to enhance Ethereum with privacy features, like a smart contract with secret state.

Interesting, but what is the drawbacks from making the sate secret without witnesses.

---

**Levalicious** (2021-02-14):

Correct me if I’m wrong, but isn’t FAPKC3 considered insecure since 2008 or so? Are there plans to use FAPKC4? Also, has there been any analysis on whether this is pq safe?

---

**haael** (2021-02-14):

FAPKC0, 1 and 2 were broken completely.

FAPKC3 is broken, but not completely.

FAPKC4 is a modification of FAPKC3 and is secure, there are also extensions of FAPKC4 and even cryptosystems beyond FAPKC based on the same principle (factorization problem). Even RSA may be used here.

I am looking for someone to make an analysis and possibly to write a paper. Are you interested, or could you recommend someone who would be?

---

**haael** (2021-02-14):

Certain users would have access to the contract state, the ones who have the keys. Other than that, the network would be able to enforce rules, even without the private keys.

