---
source: magicians
topic_id: 2586
title: Natspec->Radspec
author: ligi
date: "2019-02-04"
category: Web > Wallets
tags: [wallet]
url: https://ethereum-magicians.org/t/natspec-radspec/2586
views: 1115
likes: 4
posts_count: 10
---

# Natspec->Radspec

Moving this discussion from twitter to the magicians so we are not limited in character count:

https://twitter.com/izqui9/status/1092428328491982848

My current questions:

- Are the radspec keywords documented somewhere? when googling for “@tokenAmount” or “@formatPct” I only find usages but no documentation. Would especially be interested in a list of possible keywords.
- who can publish to the registry - in natspec it was part of the solidity compilation - not yet sure how this would work for radspec
- as @pedrouid correctly mentioned - while attacking this problem we could also think about localisation

## Replies

**izqui** (2019-02-04):

> Are the radspec keywords documented somewhere? when googling for “@tokenAmount” or “@formatPct” I only find usages but no documentation. Would especially be interested in a list of possible keywords.

https://twitter.com/izqui9/status/1092448010758512640

> who can publish to the registry - in natspec it was part of the solidity compilation - not yet sure how this would work for radspec

The registry needs to be designed and we can get as crazy as our imagination takes us. I think to get started something fairly centralized is fine, you just need a way to prevent spam and encourage submissions for the most used smart contracts. I was thinking a model where you have bonded curators/maintainers that ‘merge’ contributions that get rewarded. Changing an existing description should be way harder than adding a new one.

Radspec strings for new contracts can be extracted from solidity files in the same way as Natspec strings do, so they are also part of the Solidity source code hash swarm link at the end of the bytecode.

> as @pedrouid correctly mentioned - while attacking this problem we could also think about localisation

Absolutely. This is the format I thought of when adding meta-radspec string support and hardcoding some strings in the package. It would be trivial to convert it into an object in which lang identifiers are the keys and the localized strings are the value:



      [github.com/aragon/radspec](https://github.com/aragon/radspec/pull/55/files#diff-1b6b9fc7882ad4fc606bd4e46ad9991e)














####


      `master` ← `meta-radspec`




          opened 02:57PM - 04 Feb 19 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/f/f9b9b56a4d7e6778c90a7dd88d132645bb7bb495.jpeg)
            izqui](https://github.com/izqui)



          [+2001
            -1389](https://github.com/aragon/radspec/pull/55/files)







The `@radspec` helper allows to recursively execute radspec as part of a radspec[…](https://github.com/aragon/radspec/pull/55) string. These strings should be either included in the radspec package or loaded from a trusted registry, as the recursive nature of this feature could be used to crash radspec with an infinite loop.

---

**pedrouid** (2019-02-04):

If we keep radspec operations basic enough we might not need it to be done on client-side

`@tokenAmount(self, $3)` could be replaced by `div($3, pow(10, self.decimals))`

---

**izqui** (2019-02-04):

I totally get your point, but if you look at the actual implementation of the helper you will be surprised at how non-trivial it is to properly format token amounts ![:sweat_smile:](https://ethereum-magicians.org/images/emoji/twitter/sweat_smile.png?v=9)


      [github.com](https://github.com/aragon/radspec/blob/master/src/helpers/tokenAmount.js)




####

```js
import BN from 'bn.js'
import { toUtf8 } from 'web3-utils'
import { ERC20_SYMBOL_BYTES32_ABI, ERC20_SYMBOL_DECIMALS_ABI, ETH } from './lib/token'
import { formatBN, tenPow } from './lib/formatBN'

export default (eth) =>
  /**
   * Format token amounts taking decimals into account
   *
   * @param {string} tokenAddress The address of the token
   * @param {*} amount The absolute amount for the token quantity (wei)
   * @param {bool} showSymbol Whether the token symbol will be printed after the amount
   * @param {*} precision The number of decimal places to format to. If set, the precision is always enforced.
   * @return {Promise}
   */
  async (tokenAddress, amount, showSymbol = true, precision) => {
    const amountBn = new BN(amount)
    const fixed = !!precision

    let decimals
```

  This file has been truncated. [show original](https://github.com/aragon/radspec/blob/master/src/helpers/tokenAmount.js)

---

**pedrouid** (2019-02-04):

Yeah, because I didn’t include the symbol and precision. Honestly I don’t mind so much about the off-chain computation of the metadata. Currently it’s much worse so this definitely is a significant improvement. No need to be purist now as we should move this to be adopted as soon as possible

---

**ligi** (2019-02-04):

Was just talking to chriseth about this and we think creating a registry is not really needed. We can just fix natspec (remove the dependency to/usage of JS - seems(*1) to be not really used anyway) - solidity is not actually doing something with the JS expressions - just piping them through.

So the JS stuff could just be removed from natspec and we should be done.

That said: it would not really solve the localisation problem.

(*1) - we should gather some data on this

---

**izqui** (2019-02-04):

If you remove JS, you need to add a way to perform basic data transformations so the descriptions can be useful UI. This is why we built radspec.

---

**ligi** (2019-02-04):

Sure - but this can be added to NatSpec. Having NatSpec and RadSpec at the same time makes things quite ugly. No real reason to fork here - just improve/fix whats there already.

---

**izqui** (2019-02-04):

Radspec is just Natspec but it uses its own DSL rather than JS’ evals for executing code. Radspec strings are placed in Solidity code in the same place that Natspec strings are, so all the Natspec extractors (solc included) work with Radspec out of the box.

---

**ligi** (2019-02-04):

But why would you need the registry then?

