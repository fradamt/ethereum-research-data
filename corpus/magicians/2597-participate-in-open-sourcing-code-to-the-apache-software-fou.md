---
source: magicians
topic_id: 2597
title: Participate in open sourcing code to the Apache Software Foundation
author: atoulme
date: "2019-02-06"
category: Protocol Calls & happenings > Announcements
tags: [open-source, apache]
url: https://ethereum-magicians.org/t/participate-in-open-sourcing-code-to-the-apache-software-foundation/2597
views: 1421
likes: 6
posts_count: 9
---

# Participate in open sourcing code to the Apache Software Foundation

Hey folks,

We are moving to donate Cava (https://www.github.com/consensys/cava) to the Apache Software Foundation.

Here is the original mailing list thread: https://t.co/EEskrGUutS

Here is the proposal on the incubator wiki: https://wiki.apache.org/incubator/CavaProposal

We’re looking for volunteers to join the project and help build a vibrant community around this code.

Please ask away any questions here and consider joining the mailing list to signal interest.

Thank you!

## Replies

**boris** (2019-02-06):

Probably of interest to [@ligi](/u/ligi) who does lots of Kotlin stuff.

---

**ligi** (2019-02-06):

Thanks for the ping. I am aware of cava and respect the work (especially the devp2p implementation).

That said:I do not see myself joining this community directly. Background: I started [KEthereum](https://github.com/walleth/kethereum) with a similar scope around one year before cava was born. The KEthereum project has more contributors and more stars. Also I am not sure about the name - I like KEthereum (Kotlin + Ethereum) better than Cava (Consensys + Java)

On a last note: cava is java focused. So you can use it with Kotlin through the java/kotlin interoperability - but only in JVM projects. With KEthereum I try to keep everything pure Kotlin so it could (in the future) also be used in MutiPlatform projects.

Still I respect the work on cava - the above are just reasons why I do not see myself joining the cava community as I see the intention of this call.

Wonder if a merge of cava into web3j could be another way to go?

---

**atoulme** (2019-02-06):

Hi [@ligi](/u/ligi), thanks for your reply!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ligi/48/28_2.png) ligi:

> Thanks for the ping. I am aware of cava and respect the work (especially the devp2p implementation).
> That said:I do not see myself joining this community directly.

We have a few ways you can participate with the Apache processes.

You can be listed as an interested developer. It will help signal that the project is of interest to you yet you do not want at this time to contribute.

You can be listed as an initial committer. In exchange for initial commit rights, we expect as a volunteer that you will care for the project, by contributing, voting releases and new committers, and providing feedback on the project mailing list.

> Background: I started KEthereum with a similar scope around one year before cava was born. The KEthereum project has more contributors and more stars. Also I am not sure about the name - I like KEthereum (Kotlin + Ethereum) better than Cava (Consensys + Java)

Yes, part of the proposal covers changing the name. We welcome any feedback in reviewing this proposal.

> On a last note: cava is java focused. So you can use it with Kotlin through the java/kotlin interoperability - but only in JVM projects. With KEthereum I try to keep everything pure Kotlin so it could (in the future) also be used in MutiPlatform projects.

Well understood. More power to you.

> Still I respect the work on cava - the above are just reasons why I do not see myself joining the cava community as I see the intention of this call.
> Wonder if a merge of cava into web3j could be another way to go?

That’s not what’s being discussed here, but I’d be happy to engage with the web3j community and see if they’d be interested in contributing to Cava, of course!

---

**lookfirst** (2019-02-09):

[@ligi](/u/ligi) If you’re going to include others code, you should at least credit the source.


      [github.com](https://github.com/walleth/kethereum/blob/master/base58/src/main/kotlin/org/kethereum/encodings/Base58.kt)




####

```kt
@file:JvmName("Base58")

package org.kethereum.encodings

/**
 * Base58 is a way to encode addresses (or arbitrary data) as alphanumeric strings.
 * Compared to base64, this encoding eliminates ambiguities created by O0Il and potential splits from punctuation
 *
 * The basic idea of the encoding is to treat the data bytes as a large number represented using
 * base-256 digits, convert the number to be represented using base-58 digits, preserve the exact
 * number of leading zeros (which are otherwise lost during the mathematical operations on the
 * numbers), and finally represent the resulting base-58 digits as alphanumeric ASCII characters.
 */

import org.kethereum.hashes.sha256
import java.util.*

private const val ENCODED_ZERO = '1'
private const val CHECKSUM_SIZE = 4

```

  This file has been truncated. [show original](https://github.com/walleth/kethereum/blob/master/base58/src/main/kotlin/org/kethereum/encodings/Base58.kt)








vs.


      [github.com](https://github.com/corda/corda/blob/master/core/src/main/java/net/corda/core/crypto/Base58.java)




####

```java
package net.corda.core.crypto;

import net.corda.core.KeepForDJVM;

import java.math.BigInteger;
import java.util.Arrays;

/**
 * Base58 is a way to encode Bitcoin addresses (or arbitrary data) as alphanumeric strings.
 *

 * Note that this is not the same base58 as used by Flickr, which you may find referenced around the Internet.
 *

 * Satoshi explains: why base-58 instead of standard base-64 encoding?
 *

- Don't want 0OIl characters that look the same in some fonts and
 * could be used to create visually identical looking account numbers.
- A string with non-alphanumeric characters is not as easily accepted as an account number.
- E-mail usually won't line-break if there's no punctuation to break at.
- Doubleclicking selects the whole number as one word if it's all alphanumeric.

```

  This file has been truncated. [show original](https://github.com/corda/corda/blob/master/core/src/main/java/net/corda/core/crypto/Base58.java)

---

**ligi** (2019-02-09):

IANAL - but this is only the documentation/definition of base58. The code is a complete different programming language.

---

**lookfirst** (2019-02-09):

You don’t need to be a lawyer, you just need to read the license and follow what it says. It isn’t magical or difficult to understand.

Here is the relevant sections:

“Derivative Works” shall mean any work, whether in Source or Object form, that is based on (or derived from) the Work and for which the editorial revisions, annotations, elaborations, or other modifications represent, as a whole, an original work of authorship. For the purposes of this License, Derivative Works shall not include works that remain separable from, or merely link (or bind by name) to the interfaces of, the Work and Derivative Works thereof.

**4. Redistribution** . You may reproduce and distribute copies of the Work or Derivative Works thereof in any medium, with or without modifications, and in Source or Object form, provided that You meet the following conditions:

1. You must give any other recipients of the Work or Derivative Works a copy of this License; and
2. You must cause any modified files to carry prominent notices stating that You changed the files; and
3. You must retain, in the Source form of any Derivative Works that You distribute, all copyright, patent, trademark, and attribution notices from the Source form of the Work, excluding those notices that do not pertain to any part of the Derivative Works; and
4. If the Work includes a “NOTICE” text file as part of its distribution, then any Derivative Works that You distribute must include a readable copy of the attribution notices contained within such NOTICE file, excluding those notices that do not pertain to any part of the Derivative Works, in at least one of the following places: within a NOTICE text file distributed as part of the Derivative Works; within the Source form or documentation, if provided along with the Derivative Works; or, within a display generated by the Derivative Works, if and wherever such third-party notices normally appear. The contents of the NOTICE file are for informational purposes only and do not modify the License. You may add Your own attribution notices within Derivative Works that You distribute, alongside or as an addendum to the NOTICE text from the Work, provided that such additional attribution notices cannot be construed as modifying the License.

You may add Your own copyright statement to Your modifications and may provide additional or different license terms and conditions for use, reproduction, or distribution of Your modifications, or for any such Derivative Works as a whole, provided Your use, reproduction, and distribution of the Work otherwise complies with the conditions stated in this License.

---

**ligi** (2019-02-09):

Thanks for pointing this out. Was not aware it also applies to documentation. Just credited bitcoinj for this.

My thinking was that this is the definition was base58 is - so it is OK - but you are right - this should also be credited. Is now done.

Will give Andreas Schildbach a mate next time I see him for the late attribution of this and think this should be OK.

---

**lookfirst** (2019-02-09):

Thanks so much [@ligi](/u/ligi). Licenses are important, otherwise we wouldn’t bother putting them on our work at all. Respecting each others hard work and giving / getting credit for everything we contribute is part of what keeps open source so fun and exciting.

