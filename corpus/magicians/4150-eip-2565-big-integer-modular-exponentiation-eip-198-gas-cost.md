---
source: magicians
topic_id: 4150
title: "EIP-2565: Big integer modular exponentiation (EIP-198) gas cost"
author: kelly
date: "2020-03-21"
category: EIPs > EIPs core
tags: [gas, eip-2565]
url: https://ethereum-magicians.org/t/eip-2565-big-integer-modular-exponentiation-eip-198-gas-cost/4150
views: 29642
likes: 1
posts_count: 26
---

# EIP-2565: Big integer modular exponentiation (EIP-198) gas cost

---

eip:

title: Big integer modular exponentiation (EIP-198) gas cost

author: Kelly Olson (@ineffectualproperty), Sean Gulley (@sean-sn), Simon Peffers (@simonatsn), Justin Drake ([@justindrake](/u/justindrake)), Dankrad Feist ([@dankrad](/u/dankrad))

discussions-to: TBD

status: Draft

type: Standards Track

category: Core

created: 2020-03-20

Requires:

---

## Simple Summary

The [EIP-198](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-198.md) ‘big integer modular exponentiation’, or `ModExp`, precompile is currently overpriced. Re-pricing this precompile will enable more cost efficient verification of RSA signatures, verifiable delay functions (VDFs), primality checks, and more.

## Abstract

After benchmarking the ModExp precompile, we discovered that it is ‘overpriced’ relative to other precompiles. We also discovered that the current gas pricing formula could be improved to better estimate the computational complexity of various ModExp input variables. To improve the gas cost pricing for this precompile the following options are available:

1. Changing the value of the GQUADDIVISOR parameter in the ModExp pricing formula to bring its costs more in-line with other precompiles
2. Modifying the gas pricing formula to better reflect the computational complexity of ModExp operations
3. Improving the underlying libraries beneath the ModExp Precompile
4. Any combination of (1), (2), and (3)

We recommend **Option (1)** which provides a large practical improvement to gas estimation while keeping implementation complexity low. Options (2) and (3) could also be implemented and would further improve the gas pricing for a broader range of use cases. Additional data can be provided for options (2) and (3) as desired.

## Motivation

Modular exponentiation is a foundational arithmetic operation for many cryptographic functions including signatures, VDFs, SNARKs, accumulators, and more. Unfortunately, the ModExp precompile is currently over-priced, making these operations inefficient and expensive. By reducing the cost of this precompile, these cryptographic functions become more practical, enabling improved security, stronger randomness (VDFs), and more.

## Specification

The current gas pricing formula is defined in EIP-198. This formula divides a ‘computational complexity’ function by a ‘gas conversion’ parameter called ‘GQUADDIVISOR’ to arrive at a gas cost.

### Recommended Option (1): Change value of GQUADDIVISOR

`GQUADDIVISOR` is set to ‘20’ per EIP-198. We recommend changing the value of this parameter to ‘200’.

### Option (2): Modify ‘computational complexity’ function

A proposed ‘complexity’ function can be found at the following [spreadsheet](https://docs.google.com/spreadsheets/d/1Fq3d3wUjGN0R_FX-VPj7TKhCK33ac--P4QXB9MPQ8iw/edit?usp=sharing)

Code defining an improved complexity function can be provided as needed, but this option is not recommended at this time.

### Option (3): Replace libraries used by ModExp precompiles

ModExp benchmarks for different libraries can be found at the following [spreadsheet](https://docs.google.com/spreadsheets/d/1Fq3d3wUjGN0R_FX-VPj7TKhCK33ac--P4QXB9MPQ8iw/edit?usp=sharing)

While alternative libraries can provide improved performance, this option is not recommended at this time.

## Rationale

### Recommended Option (1): Change value of GQUADDIVISOR:

Changing the value of this parameter from 20 to 200 will reduce the gas cost of this precompile by a factor of 10 with minimal implementation changes. With this change, the cost of the ModExp precompile will have a higher cost (gas/second) than other precompiles such as ECRecover.

[![](https://ethereum-magicians.org/uploads/default/optimized/2X/6/674eb9fa0cbca92c5fd2c5396fff8d59b4c62308_2_624x349.png)1600×897 109 KB](https://ethereum-magicians.org/uploads/default/674eb9fa0cbca92c5fd2c5396fff8d59b4c62308)

### Option (2): Modify ‘computational complexity’ formula

A proposed ‘complexity’ function can be found at the following [spreadsheet](https://docs.google.com/spreadsheets/d/1Fq3d3wUjGN0R_FX-VPj7TKhCK33ac--P4QXB9MPQ8iw/edit?usp=sharing).

[![](https://ethereum-magicians.org/uploads/default/optimized/2X/5/51674d9d1a927b63322983afe04b52e12343e837_2_401x500.png)1224×1526 84.9 KB](https://ethereum-magicians.org/uploads/default/51674d9d1a927b63322983afe04b52e12343e837)

The new complexity function has a better fit vs. the execution time when compared to the current complexity function. This better fit is because the new complexity formula accounts for the use of binary exponentiation algorithms that are used by ‘bigint’ libraries for large exponents. You may also notice the regression line of the proposed complexity function bisects the test vector data points. This is because the run time varies depending on if the modulus is even or odd.

While modifying the computational complexity formula can improve gas estimation at a medium implementation cost, we do not recommend it at this time.

### Option (3): Improving the ModExp precompile implementations

[![](https://ethereum-magicians.org/uploads/default/optimized/2X/0/0d2846ae1172149b8d7b55ca4bda8d81de1e5ba4_2_624x237.png)1600×607 275 KB](https://ethereum-magicians.org/uploads/default/0d2846ae1172149b8d7b55ca4bda8d81de1e5ba4)

Replacing the underlying library can improve the performance of the ModExp precompile by 2x-4x for large exponents, but comes at a high implementation cost. We do not recommend this option at this time.

## Test Cases

As no underlying algorithms are being changed, there are no additional test cases to specify.

## References

[EIP-198](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-198.md)

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).

## Replies

**kelly** (2020-03-31):

This EIP has now been approved to be merged under ‘draft’ status here: https://github.com/ethereum/EIPs/pull/2565

Additional comments or feedback are appreciated.

---

**holiman** (2020-09-08):

So, afaiu, option 2 was accepted for YOLOv2 integration.

Specification:

> GQUADDIVISOR is set to 20 per EIP-198. We recommend changing the value of this parameter to 3 to account for the changes in the recommended ‘computational complexity’ formula above.

Think this is poorly specified. Changing it from `20` to `3` increases the gascost. So as I understand it, the spec should *really* say

> Implement formula changes from Option 1.
> Change GQUADDIVISOR (defined as 20 in EIP-198) to 3.

---

**holiman** (2020-09-08):

The EIP is very vague in other respects aswell. For example, (but the same thing is in several places) - here’s a snippet from option 1:

> In addition to modifying the mult_complexity formula as above, we also recommend wrapping the entire function with a minimum gas price of 100 to ensure that a minimum amount of gas is used when the precompile is called e.g. max(100,floor(mult_complexity(x)/GQUADDIVISOR))

That’s an example of where a vital point in the spec is almost an afterthought in a footnote placed after the test-vector link. The EIP should clearly assert the specification, and say

> In addition to modifying the mult_complexity formula as above, the entire function is wrapped to guarantee a minimum gas price of 100 :
>
>
>
> ```auto
>     return max(100,floor(mult_complexity(x)/GQUADDIVISOR))`
> ```

But the example there doesn’t match even so - because it omits the ` * max(ADJUSTED_EXPONENT_LENGTH, 1)` part from the original spec?

The original 198 spec is

```auto
floor(mult_complexity(max(length_of_MODULUS, length_of_BASE)) * max(ADJUSTED_EXPONENT_LENGTH, 1) / GQUADDIVISOR)
```

So shouldn’t the example be

```auto
x = max(length_of_MODULUS, length_of_BASE)
y = floor(mult_complexity(x) * max(ADJUSTED_EXPONENT_LENGTH, 1) / GQUADDIVISOR)
return max(100, y)
```

?

---

**holiman** (2020-09-08):

For option 1, you link to a spreadsheet which contains the expected gas costs. However, for option 2, you link [here](https://docs.google.com/spreadsheets/d/1Fq3d3wUjGN0R_FX-VPj7TKhCK33ac--P4QXB9MPQ8iw/edit?usp=sharing), and I can’t seem to find the reference gas costs for option 2. Could you please provide those too?

Ideally, have an appendix on the form

| testcase | EIP-198 gas | 2565 opt  1 gas | 2565 opt 2 gas |
| --- | --- | --- | --- |
| modexp_nagydani_1_square | 204 | 100 | 100 |
| … |  |  |  |

Ah wait, this is a total mess.

So the [EIP](https://eips.ethereum.org/EIPS/eip-2565) says:

> Recommended Option (1): Modify ‘computational complexity’ function and add minimum gas cost
> Recommended Option (2): Change value of GQUADDIVISOR
> GQUADDIVISOR is set to 20 per EIP-198. We recommend changing the value of this parameter to 3 to account for the changes in the recommended ‘computational complexity’ formula above.

But the description *here*, on this forum, says

> Recommended Option (1): Change value of GQUADDIVISOR:
> GQUADDIVISOR is set to ‘20’ per EIP-198. We recommend changing the value of this parameter to ‘200’.
> Option (2): Modify ‘computational complexity’ function

So,

1. the options are turned around,
2. and the GQUADDIVISOR new value is 3 on the EIP, and 200 here.

I have no idea what to make of this.

- I guess we leave the formula as is,
- but modify GQUADDIVISOR to 200,
- and do we also skip adding a minimum gas cost?

Furthermore,

> Option (3): Replace libraries used by ModExp precompiles

That option has no place in the EIP – it’s a good recommendation to have if you’re presenting material to the ACD, but there’s no consensus change involved. IMO it should be removed from the EIP.

---

**kelly** (2020-09-08):

Hi [@holiman](/u/holiman) - thanks for the feedback. I saw some other similar suggested feedback from [@MicahZoltu](/u/micahzoltu) as well and will clarify the EIP to make it more spec-focused than proposal focused. I will incorporate your suggested changes as well and include an appendix with the updated test vectors and post back here once an updated PR is made in the next day or two. Thanks for the feedback.

---

**tkstanczak** (2020-09-22):

[@holiman](/u/holiman) do you have a link to the test vectors? I have been asking for it for a while but the spreadsheet only seems to contain some data about the test vectors but not the exact values

also - which libraries are considered fast enough to support it? the spreadsheet verifies Geth, gmp and OpenSSL. The gmp library is GPL licensed so we cannot use it.

---

**kelly** (2020-09-22):

Hey [@tkstanczak](/u/tkstanczak) - my apologies as I have been slow to update the EIP as I’ve been consumed with a few other things. I will update this post tomorrow with a link to the updated EIP along with the updated test vectors. As for libraries, most big integer libraries are of sufficient performance, though the Rust modular exponentiation is slow. OpenSSL is Apache2 licensed and I believe that GMP is now LGPL.

---

**kelly** (2020-09-23):

Hi [@holiman](/u/holiman) and [@tkstanczak](/u/tkstanczak). The updated EIP is now available in this PR: https://github.com/ethereum/EIPs/pull/2892. It includes test vectors as suggested. [@holiman](/u/holiman) I’ve also created a prototype of the proposed changes to Geth here: https://gist.github.com/ineffectualproperty/9811fbe573eae600420c93336d379038

Please let me know if anything remains unclear or if you have any recommendations to improve it.

---

**kelly** (2020-09-23):

**Updated EIP 09/23/20**

## Simple Summary

The EIP-198 ‘big integer modular exponentiation’, or `ModExp`, precompile is currently overpriced. Re-pricing this precompile will enable more cost efficient verification of RSA signatures, verifiable delay functions (VDFs), primality checks, and more.

## Abstract

After benchmarking the ModExp precompile, we discovered that it is ‘overpriced’ relative to other precompiles. We also discovered that the current gas pricing formula could be improved to better estimate the computational complexity of various ModExp input variables. To improve the gas cost pricing for this precompile, this EIP specifies:

1. A change to the mult_complexity formula to better reflect the computational complexity of ModExp operations
2. A change to the value of the GQUADDIVISOR parameter in the ModExp pricing formula to bring its costs more in-line with other precompiles
3. A minimum cost to call the precompile to prevent underpricing for small inputs

## Motivation

Modular exponentiation is a foundational arithmetic operation for many cryptographic functions including signatures, VDFs, SNARKs, accumulators, and more. Unfortunately, the ModExp precompile is currently over-priced, making these operations inefficient and expensive. By reducing the cost of this precompile, these cryptographic functions become more practical, enabling improved security, stronger randomness (VDFs), and more.

## Specification

The current gas pricing formula is defined in EIP-198 as follows:

```auto
floor(mult_complexity(max(length_of_MODULUS, length_of_BASE)) * max(ADJUSTED_EXPONENT_LENGTH, 1) / GQUADDIVISOR)
```

As of `FORK_BLOCK_NUMBER` make the following changes to the pricing formula for the ModExp precompile:

### 1: Modify the mult_complexity function

The current complexity function, as defined in EIP-198 is as follow:

```auto
def mult_complexity(x):
    if x <= 64: return x ** 2
    elif x <= 1024: return x ** 2 // 4 + 96 * x - 3072
    else: return x ** 2 // 16 + 480 * x - 199680
```

where is `x` is `max(length_of_MODULUS, length_of_BASE)`

This complexity formula was meant to approximate the difficulty of Karatsuba multiplication. However, we found a better approximation for modelling modular exponentiation. We recommend the following formula to better estimate the computational complexity for varying input values:

```auto
def mult_complexity(x):
    ceiling(x/8)^2
```

where is `x` is `max(length_of_MODULUS, length_of_BASE)`. `x` is divided by 8 to account for the number of limbs in multiprecision arithmetic.

### 2. Change value of GQUADDIVISOR

`GQUADDIVISOR` is set to `20` per EIP-198. We recommend changing the value of this parameter to `3` to account for the changes in the recommended ‘computational complexity’ formula above.

### 3. Set a minimum price for calling the precompile

We recommend wrapping the entire function with a minimum gas price of 200 to ensure that a minimum amount of gas is used when the precompile is called e.g. `max(200,floor(mult_complexity(max(length_of_MODULUS, length_of_BASE)) * max(ADJUSTED_EXPONENT_LENGTH, 1) / GQUADDIVISOR))`

## Rationale

### 1. Modify ‘computational complexity’ formula to better reflect the computational complexity

A comparison of the current ‘complexity’ function and the proposed function against the execution time can be seen below:

[![](https://ethereum-magicians.org/uploads/default/optimized/2X/5/51674d9d1a927b63322983afe04b52e12343e837_2_401x500.png)1224×1526 84.9 KB](https://ethereum-magicians.org/uploads/default/51674d9d1a927b63322983afe04b52e12343e837)

The new complexity function has a better fit vs. the execution time when compared to the current complexity function. This better fit is because the new complexity formula accounts for the use of binary exponentiation algorithms that are used by ‘bigint’ libraries for large exponents. You may also notice the regression line of the proposed complexity function bisects the test vector data points. This is because the run time varies depending on if the modulus is even or odd.

### 2. Change the value of GQUADDIVISOR

After changing the ‘computational complexity’ formula it is necessary to change `QGUADDIVSOR` to bring the gas costs inline with their runtime. We recommend changing the value from ‘20’ to ‘3’. With this change, the cost of the ModExp precompile will have a higher cost (gas/second) than other precompiles such as ECRecover.

[![](https://ethereum-magicians.org/uploads/default/optimized/2X/5/5c96c90bfe966669e3a06da46ea7a00fd3cc2f77_2_690x376.png)1944×1060 158 KB](https://ethereum-magicians.org/uploads/default/5c96c90bfe966669e3a06da46ea7a00fd3cc2f77)

### 3. Set a minimum gas cost to prevent abuse

This prevents the precompile from underpricing small input values.

## Test Cases

There are no changes to the underlying interface or arithmetic algorithms, so the existing test vectors can be reused. Below is a table with the updated test vectors:

| Test Case | EIP-198 Pricing | New Pricing |
| --- | --- | --- |
| modexp_nagydani_1_square | 204 | 200 |
| modexp_nagydani_1_qube | 204 | 200 |
| modexp_nagydani_1_pow0x10001 | 3276 | 341 |
| modexp_nagydani_2_square | 665 | 200 |
| modexp_nagydani_2_qube | 665 | 200 |
| modexp_nagydani_2_pow0x10001 | 10649 | 1365 |
| modexp_nagydani_3_square | 1894 | 341 |
| modexp_nagydani_3_qube | 1894 | 341 |
| modexp_nagydani_3_pow0x10001 | 30310 | 5461 |
| modexp_nagydani_4_square | 5580 | 1365 |
| modexp_nagydani_4_qube | 5580 | 1365 |
| modexp_nagydani_4_pow0x10001 | 89292 | 21845 |
| modexp_nagydani_5_square | 17868 | 5461 |
| modexp_nagydani_5_qube | 17868 | 5461 |
| modexp_nagydani_5_pow0x10001 | 285900 | 87381 |

## Security Considerations

The biggest security consideration for this EIP is creating a potential DoS vector by making ModExp operations too inexpensive relative to their computation time.

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).

---

**holiman** (2020-09-23):

I’m not getting the same numbers. Let’s consider `modexp_nagydani_pow0x10001`:

```auto
length_of_MODULUS = 64
length_of_BASE = 64
multComplexity(64) = 1
1 * max(16, 1) = 16
16 / 3 = 5
min(200,5) = 200
   TestPrecompiledModExpEip2565/nagydani-1-pow0x10001-Gas=200: contracts_test.go:105: nagydani-1-pow0x10001: gas wrong, expected 341, got 200
```

---

**kelly** (2020-09-23):

[@holiman](/u/holiman) My apologies! I had a mix-up with bytes and bits. Could you please try the following update to represent the size of a limb in bytes (previously was 64 as I had incorrectly represented it in bits).

```auto
def mult_complexity(x):
    ceiling(x/8)^2
```

---

**holiman** (2020-09-24):

Yep, now the numbers match up. I made a PR for geth: https://github.com/ethereum/go-ethereum/pull/21607

---

**shemnon** (2020-10-02):

Where can we get the new test vectors seen on the spreadsheet (v1->v52, or new test vector 1 through new test vector 52)?

---

**kelly** (2020-10-06):

Hey [@shemnon](/u/shemnon) - I’m unfortunately unable to find the underlying values that were generated for the performance analysis as it looks like I only saved the lengths in the excel sheet at the time. This EIP does not propose the addition of any new test vectors, rather merely updates the calculated gas for the existing set of test vectors as shown above. You can find the most recent EIP updates here: https://github.com/ethereum/EIPs/pull/2892. The references to the Excel spreadsheet performance analysis have been removed at the request of the EIP repository maintainers.

On last weeks ACD call it was suggested that Besu and Nethermind teams should run a benchmark to understand the performance of their ModExp libraries as Geth has done. If it possible to provide a benchmark for the 15 existing test vectors I’d be happy to run them through the new pricing formula to ensure that pricing stays above ~15M gas/second and doesn’t present any DoS risk for the Besu client. Please let me know if I can help answer any other questions.

---

**kelly** (2020-10-06):

An update has been pushed to the EIP based on feedback: https://github.com/ethereum/EIPs/pull/2892

A Python implementation has been added for clarity here: https://gist.github.com/ineffectualproperty/60e34f15c31850c5b60c8cf3a28cd423

---

**kelly** (2020-10-08):

The EIP has been merged as last call and can be viewed here: https://eips.ethereum.org/EIPS/eip-2565

[@shemnon](/u/shemnon) and [@tkstanczak](/u/tkstanczak) it would be great if you could benchmark your existing ModExp precompile with the existing EIP-198 test vectors (https://raw.githubusercontent.com/ethereum/go-ethereum/master/core/vm/testdata/precompiles/modexp.json) to ensure that this repricing doesn’t cause any gas issues for the Besu or Nethermind clients. If you post them here I can create a table with the gas/second using the proposed pricing scheme. The original EIP was run on a 4th gen Intel i7 but any modern laptop/desktop should be sufficient to run the benchmark.

---

**kelly** (2020-10-08):

Following up on an off-forum conversation with [@timbeiko](/u/timbeiko). The Besu team has now implemented the EIP-2565 gas pricing and is seeing the correct results for all test vectors.

---

**poojaranjan** (2021-01-07):

[Peep an EIP-2565 with Kelly Olson](https://youtu.be/riBALRAw1Mw)

---

**MicahZoltu** (2021-03-08):

Migrating discussion from [Update EIP-2565 to clarify specification by ineffectualproperty · Pull Request #2892 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/2892#issuecomment-792239908) to here:

[@tkstanczak](/u/tkstanczak)

> Hi, my intuition is that the complexity of the calculation is defined by the last 32 bits more than the first 32 bits, hence the more granular calculation there? (length -32) * 8 (ignoring zeros) + last_32_very detailed.
>
>
> Now I also think that maybe the author felt that the last n - 32 bits may be assumed to be filled and we do not care about bits set so much but for the first 32 bits it defines the number of iterations much more…
>
>
> Would be great to confirm with authors as the spec is not entirely clear here but it may have consequence for potential attacks?
>
>
> I have changed it on nethermind to match Geth’s calculation (which may or may not be correct interpretation of the ‘&’ logic in the spec.

[@holiman](/u/holiman)

> I still think this EIP should be updated to be more clear about the formula. Both @tkstanczak, @karalabe and myself found it very hard to read, as opposed to the earlier phrasing from EIP-198.

[@kelly](/u/kelly)

> I can revert @MicahZoltu’s suggested changes to the specification so that is consistent with EIP-198 in the next day or two which should hopefully clear up any confusion

---

**MicahZoltu** (2021-03-08):

> Would be great to confirm with authors as the spec is not entirely clear here

[@tkstanczak](/u/tkstanczak) In what way is the spec not entirely clear?  It is written in Python and thus extremely precise.

---

> I still think this EIP should be updated to be more clear about the formula.

[@holiman](/u/holiman) Same question as above, additional feedback on what specifically you find unclear about the provided ~10 lines of python would be more valuable than “I like the old one better”.  Python is extremely specific, English is not.

---

A relevant comic to lighten the discussion:

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/c/c0a78cf5465e9e0f75c9d32363b7e8975f6c03aa_2_530x500.jpeg)image650×613 146 KB](https://ethereum-magicians.org/uploads/default/c0a78cf5465e9e0f75c9d32363b7e8975f6c03aa)


*(5 more replies not shown)*
