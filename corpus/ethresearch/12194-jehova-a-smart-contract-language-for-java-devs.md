---
source: ethresearch
topic_id: 12194
title: "Jehova: A Smart-Contract language for Java Devs"
author: jeyakatsa
date: "2022-03-13"
category: Execution Layer Research
tags: []
url: https://ethresear.ch/t/jehova-a-smart-contract-language-for-java-devs/12194
views: 2285
likes: 0
posts_count: 2
---

# Jehova: A Smart-Contract language for Java Devs

[![Jehova-Logo](https://ethresear.ch/uploads/default/optimized/2X/2/203819c111de8af0c0f5959e9ab9c92ef33320bc_2_172x110.jpeg)Jehova-Logo1800×1154 32.4 KB](https://ethresear.ch/uploads/default/203819c111de8af0c0f5959e9ab9c92ef33320bc)

### Jehova: A Smart-Contract Language for Java Developers

### Abstract

Siphoning advice aggregated from a few core developers from within the Ethereum Foundation, the best path to traverse in order for Java-like fundamentals to be abstracted and compiled into the EVM, is for a brand-new programming language to be erected capable of running Java-like programs on the EVM: *Jehova*.

### Motivation

Currently, there are 200 thousand Solidity/Ethereum Developers and 7 million Java Developers Worldwide respectfully. Thus, allowing Smart-Contracts to be built in a language familiar with Java developers would help onboard more developers into the Ethereum Ecosystem.

### Production Goal

The main goal is for Smart-Contracts on Ethereum to be built with Java tools like Gradle as to remain relevant with Java clients like Consensys with plans to expand to build tools like Maven and Jenkins in order to remain independent from any client in the future.

### Progress

Work has started with an elated progression and completion time for the basic grammar and semantics to be completed before the end of 2022, more info can be found within the [Research & Development](https://github.com/jeyakatsa/jehova/tree/main/R%26D-files) paper.

---

### Language Examples

#### Smart-Contract Storage example in Solidity

```solidity
pragma solidity >=0.4.16 <0.9.0;

contract SimpleStorage {
    uint storedData;

    function set(uint x) public {
        storedData = x;
    }

    function get() public view returns (uint) {
        return storedData;
    }
}
```

#### Smart-Contract Storage example in Jehova

```java
public class SimpleStorage {
    private Uint256 storedData;

    public void setStoredData (Uint256 storedData) {
        this.storedData = storedData;
    }

    public Uint256 getStoredData () {
        return storedData;
    }
}
```

---

#### forked from:

- Java Smart Contract Abstraction for Ethereum

## Replies

**setunapo** (2022-03-23):

Will Jehova be compiled to EVM opcode?

What is the compiler?

