---
source: magicians
topic_id: 21866
title: "ERC-7826: Quantum Supremacy Bounty"
author: nikojpapa
date: "2024-11-26"
category: ERCs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-7826-quantum-supremacy-bounty/21866
views: 75
likes: 1
posts_count: 2
---

# ERC-7826: Quantum Supremacy Bounty

This ERC proposes a puzzle that only quantum computers will be able to solve. It is generatable and verifiable on the blockchain and requires zero trust. Anyone who is able to solve it proves that powerful quantum computers have been created, which then flips a flag in the contract so that Ethereum users can switch to quantum secure verification schemes. A bounty will be sent to the solver, who additionally secures themselves as a (potentially the first) known achiever of quantum supremacy, a feat for which all major players (Google, IBM, etc.) have been striving for decades.

Full details provided in the ERC link: [Add ERC: Quantum Supremacy Bounty by nikojpapa · Pull Request #731 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/731). Only the abstract and motivation are provided here in order to adhere to the character limits of this post.

## Abstract

This proposal introduces a smart contract containing a classically intractable puzzle that is expected to only be able to be solved using quantum computers.

The contract is funded with ETH, which can only be retrieved by solving the problem.

On-chain applications can then watch this contract to be aware of the quantum advantage milestone of solving this puzzle.

For example, Ethereum smart contract wallets can, using custom verification schemes such as those based on ERC-4337, watch this contract and fall back to a quantum secure signature verification scheme if and when it is solved.

The contract, then, serves the two purposes of (1) showing proof of a strict quantum supremacy[[1]](#footnote-53245-1) that is strong enough to

indicate concerns in RSA and ECDSA security, and (2) acting as an indicator to protect Ethereum assets by triggering quantum-secure

signature verification schemes.

## Motivation

Quantum supremacy[[1:1]](#footnote-53245-1) is a demonstration of a quantum computer solving a problem that would take a classical computer an infeasible amount of time to solve.

Previous attempts have been made to demonstrate quantum supremacy, e.g. Kim[[2]](#footnote-53245-2), Arute[[3]](#footnote-53245-3) and Morvan[[4]](#footnote-53245-4),

but they have been refuted or at least claimed to have no practical benefit, e.g. Begusic and Chan[[5]](#footnote-53245-5), Pednault[[6]](#footnote-53245-6),

and a quote from Sebastian Weidt (The Telegraph, “Supercomputer makes calculations in blink of an eye that take rivals 47 years”, 2023).

Quantum supremacy, by its current definition, is irrespective of the usefulness of the problem.

This EIP, however, focuses on a stricter definition of a problem that indicates when an adversary may soon or already be able to bypass current Ethereum cryptography standards.

This contract serves as trustless, unbiased proof of this strong quantum supremacy by generating a classically intractable problem on chain,

to which even the creator does not know the solution.

Since quantum computers are expected[[7]](#footnote-53245-7) to break current security standards,

Ethereum assets are at risk. However, implementing quantum-secure

protocols can be costly and complicated.

In order to delay unnecessary costs, Ethereum assets can continue using current cryptographic standards and only fall back

to a quantum-secure scheme when there is reasonable risk of security failure due to quantum computers.

Therefore, this contract can serve to protect one’s funds on Ethereum by acting as a trigger that activates when

strong quantum supremacy has been achieved by solving the classically intractable puzzle.

1. ```csl
{
  "type": "misc"
  "id": 1,
  "author"=[{"family": "Preskill", "given": "John"}],
  "DOI": "10.48550/arXiv.1203.5813",
  "title": "Quantum computing and the entanglement frontier",
  "original-date": {
    "date-parts": [
      [2012, 11, 10]
    ]
  },
  "URL": "https://doi.org/10.48550/arXiv.1203.5813"
}
```

 ↩︎ ↩︎
2. ```csl
{
  "type": "article"
  "id": 2,
  "author"=[{'family': 'Kim', 'given': 'Youngseok'}, {'family': 'Eddins', 'given': 'Andrew'}, {'family': 'Anand', 'given': 'Sajant'}, {'family': 'Wei', 'given': 'Ken Xuan'}, {'family': 'van den Berg', 'given': 'Ewout'}, {'family': 'Rosenblatt', 'given': 'Sami'}, {'family': 'Nayfeh', 'given': 'Hasan'}, {'family': 'Wu', 'given': 'Yantao'}, {'family': 'Zaletel', 'given': 'Michael'}, {'family': 'Temme', 'given': 'Kristan'}, {'family': 'Kandala', 'given': 'Abhinav'}],
  "DOI": "10.1038/s41586-023-06096-3",
  "title": "Evidence for the utility of quantum computing before fault tolerance",
  "original-date": {
    "date-parts": [
      [2023, 06, 15]
    ]
  },
  "URL": "https://doi.org/10.1038/s41586-023-06096-3"
}
```

 ↩︎
3. ```csl
{
  "type": "article"
  "id": 3,
  "author"=[{"family": "Arute", "given": "Frank"}, {"family": "Arya", "given": "Kunal"}, {"family": "Babbush", "given": "Ryan"}, {"family": "Bacon", "given": "Dave"}, {"family": "Bardin", "given": "Joseph C."}, {"family": "Barends", "given": "Rami"}, {"family": "Biswas", "given": "Rupak"}, {"family": "Boixo", "given": "Sergio"}, {"family": "Brandao", "given": "Fernando G. S. L."}, {"family": "Buell", "given": "David A."}, {"family": "Burkett", "given": "Brian"}, {"family": "Chen", "given": "Yu"}, {"family": "Chen", "given": "Zijun"}, {"family": "Chiaro", "given": "Ben"}, {"family": "Collins", "given": "Roberto"}, {"family": "Courtney", "given": "William"}, {"family": "Dunsworth", "given": "Andrew"}, {"family": "Farhi", "given": "Edward"}, {"family": "Foxen", "given": "Brooks"}, {"family": "Fowler", "given": "Austin"}, {"family": "Gidney", "given": "Craig"}, {"family": "Giustina", "given": "Marissa"}, {"family": "Graff", "given": "Rob"}, {"family": "Guerin", "given": "Keith"}, {"family": "Habegger", "given": "Steve"}, {"family": "Harrigan", "given": "Matthew P."}, {"family": "Hartmann", "given": "Michael J."}, {"family": "Ho", "given": "Alan"}, {"family": "Hoffmann", "given": "Markus"}, {"family": "Huang", "given": "Trent"}, {"family": "Humble", "given": "Travis S."}, {"family": "Isakov", "given": "Sergei V."}, {"family": "Jeffrey", "given": "Evan"}, {"family": "Jiang", "given": "Zhang"}, {"family": "Kafri", "given": "Dvir"}, {"family": "Kechedzhi", "given": "Kostyantyn"}, {"family": "Kelly", "given": "Julian"}, {"family": "Klimov", "given": "Paul V."}, {"family": "Knysh", "given": "Sergey"}, {"family": "Korotkov", "given": "Alexander"}, {"family": "Kostritsa", "given": "Fedor"}, {"family": "Landhuis", "given": "David"}, {"family": "Lindmark", "given": "Mike"}, {"family": "Lucero", "given": "Erik"}, {"family": "Lyakh", "given": "Dmitry"}, {"family": "Mandr{\\`a}", "given": "Salvatore"}, {"family": "McClean", "given": "Jarrod R."}, {"family": "McEwen", "given": "Matthew"}, {"family": "Megrant", "given": "Anthony"}, {"family": "Mi", "given": "Xiao"}, {"family": "Michielsen", "given": "Kristel"}, {"family": "Mohseni", "given": "Masoud"}, {"family": "Mutus", "given": "Josh"}, {"family": "Naaman", "given": "Ofer"}, {"family": "Neeley", "given": "Matthew"}, {"family": "Neill", "given": "Charles"}, {"family": "Niu", "given": "Murphy Yuezhen"}, {"family": "Ostby", "given": "Eric"}, {"family": "Petukhov", "given": "Andre"}, {"family": "Platt", "given": "John C."}, {"family": "Quintana", "given": "Chris"}, {"family": "Rieffel", "given": "Eleanor G."}, {"family": "Roushan", "given": "Pedram"}, {"family": "Rubin", "given": "Nicholas C."}, {"family": "Sank", "given": "Daniel"}, {"family": "Satzinger", "given": "Kevin J."}, {"family": "Smelyanskiy", "given": "Vadim"}, {"family": "Sung", "given": "Kevin J."}, {"family": "Trevithick", "given": "Matthew D."}, {"family": "Vainsencher", "given": "Amit"}, {"family": "Villalonga", "given": "Benjamin"}, {"family": "White", "given": "Theodore"}, {"family": "Yao", "given": "Z. Jamie"}, {"family": "Yeh", "given": "Ping"}, {"family": "Zalcman", "given": "Adam"}, {"family": "Neven", "given": "Hartmut"}, {"family": "Martinis", "given": "John M."}],
  "DOI": "10.1038/s41586-019-1666-5",
  "title": "Quantum supremacy using a programmable superconducting processor",
  "original-date": {
    "date-parts": [
      [2019, 08, 24]
    ]
  },
  "URL": "https://doi.org/10.1038/s41586-019-1666-5"
}
```

 ↩︎
4. ```csl
{
  "type": "misc"
  "id": 4,
  "author"=[{"family": "Morvan", "given": "A."}, {"family": "Villalonga", "given": "B."}, {"family": "Mi", "given": "X."}, {"family": "Mandr\u00e0", "given": "S."}, {"family": "Bengtsson", "given": "A."}, {"family": "V.", "given": "P."}, {"family": "Chen", "given": "Z."}, {"family": "Hong", "given": "S."}, {"family": "Erickson", "given": "C."}, {"family": "K.", "given": "I."}, {"family": "Chau", "given": "J."}, {"family": "Laun", "given": "G."}, {"family": "Movassagh", "given": "R."}, {"family": "Asfaw", "given": "A."}, {"family": "T.", "given": "L."}, {"family": "Peralta", "given": "R."}, {"family": "Abanin", "given": "D."}, {"family": "Acharya", "given": "R."}, {"family": "Allen", "given": "R."}, {"family": "I.", "given": "T."}, {"family": "Anderson", "given": "K."}, {"family": "Ansmann", "given": "M."}, {"family": "Arute", "given": "F."}, {"family": "Arya", "given": "K."}, {"family": "Atalaya", "given": "J."}, {"family": "C.", "given": "J."}, {"family": "Bilmes", "given": "A."}, {"family": "Bortoli", "given": "G."}, {"family": "Bourassa", "given": "A."}, {"family": "Bovaird", "given": "J."}, {"family": "Brill", "given": "L."}, {"family": "Broughton", "given": "M."}, {"family": "B.", "given": "B."}, {"family": "A.", "given": "D."}, {"family": "Burger", "given": "T."}, {"family": "Burkett", "given": "B."}, {"family": "Bushnell", "given": "N."}, {"family": "Campero", "given": "J."}, {"family": "S.", "given": "H."}, {"family": "Chiaro", "given": "B."}, {"family": "Chik", "given": "D."}, {"family": "Chou", "given": "C."}, {"family": "Cogan", "given": "J."}, {"family": "Collins", "given": "R."}, {"family": "Conner", "given": "P."}, {"family": "Courtney", "given": "W."}, {"family": "L.", "given": "A."}, {"family": "Curtin", "given": "B."}, {"family": "M.", "given": "D."}, {"family": "Del", "given": "A."}, {"family": "Demura", "given": "S."}, {"family": "Di", "given": "A."}, {"family": "Dunsworth", "given": "A."}, {"family": "Faoro", "given": "L."}, {"family": "Farhi", "given": "E."}, {"family": "Fatemi", "given": "R."}, {"family": "S.", "given": "V."}, {"family": "Flores", "given": "L."}, {"family": "Forati", "given": "E."}, {"family": "G.", "given": "A."}, {"family": "Foxen", "given": "B."}, {"family": "Garcia", "given": "G."}, {"family": "Genois", "given": "E."}, {"family": "Giang", "given": "W."}, {"family": "Gidney", "given": "C."}, {"family": "Gilboa", "given": "D."}, {"family": "Giustina", "given": "M."}, {"family": "Gosula", "given": "R."}, {"family": "Grajales", "given": "A."}, {"family": "A.", "given": "J."}, {"family": "Habegger", "given": "S."}, {"family": "C.", "given": "M."}, {"family": "Hansen", "given": "M."}, {"family": "P.", "given": "M."}, {"family": "D.", "given": "S."}, {"family": "Heu", "given": "P."}, {"family": "R.", "given": "M."}, {"family": "Huang", "given": "T."}, {"family": "Huff", "given": "A."}, {"family": "J.", "given": "W."}, {"family": "B.", "given": "L."}, {"family": "V.", "given": "S."}, {"family": "Iveland", "given": "J."}, {"family": "Jeffrey", "given": "E."}, {"family": "Jiang", "given": "Z."}, {"family": "Jones", "given": "C."}, {"family": "Juhas", "given": "P."}, {"family": "Kafri", "given": "D."}, {"family": "Khattar", "given": "T."}, {"family": "Khezri", "given": "M."}, {"family": "Kieferov\u00e1", "given": "M."}, {"family": "Kim", "given": "S."}, {"family": "Kitaev", "given": "A."}, {"family": "R.", "given": "A."}, {"family": "N.", "given": "A."}, {"family": "Kostritsa", "given": "F."}, {"family": "M.", "given": "J."}, {"family": "Landhuis", "given": "D."}, {"family": "Laptev", "given": "P."}, {"family": "-M.", "given": "K."}, {"family": "Laws", "given": "L."}, {"family": "Lee", "given": "J."}, {"family": "W.", "given": "K."}, {"family": "D.", "given": "Y."}, {"family": "J.", "given": "B."}, {"family": "T.", "given": "A."}, {"family": "Liu", "given": "W."}, {"family": "Locharla", "given": "A."}, {"family": "D.", "given": "F."}, {"family": "Martin", "given": "O."}, {"family": "Martin", "given": "S."}, {"family": "R.", "given": "J."}, {"family": "McEwen", "given": "M."}, {"family": "C.", "given": "K."}, {"family": "Mieszala", "given": "A."}, {"family": "Montazeri", "given": "S."}, {"family": "Mruczkiewicz", "given": "W."}, {"family": "Naaman", "given": "O."}, {"family": "Neeley", "given": "M."}, {"family": "Neill", "given": "C."}, {"family": "Nersisyan", "given": "A."}, {"family": "Newman", "given": "M."}, {"family": "H.", "given": "J."}, {"family": "Nguyen", "given": "A."}, {"family": "Nguyen", "given": "M."}, {"family": "Yuezhen", "given": "M."}, {"family": "E.", "given": "T."}, {"family": "Omonije", "given": "S."}, {"family": "Opremcak", "given": "A."}, {"family": "Petukhov", "given": "A."}, {"family": "Potter", "given": "R."}, {"family": "P.", "given": "L."}, {"family": "Quintana", "given": "C."}, {"family": "M.", "given": "D."}, {"family": "Rocque", "given": "C."}, {"family": "Roushan", "given": "P."}, {"family": "C.", "given": "N."}, {"family": "Saei", "given": "N."}, {"family": "Sank", "given": "D."}, {"family": "Sankaragomathi", "given": "K."}, {"family": "J.", "given": "K."}, {"family": "F.", "given": "H."}, {"family": "Schuster", "given": "C."}, {"family": "J.", "given": "M."}, {"family": "Shorter", "given": "A."}, {"family": "Shutty", "given": "N."}, {"family": "Shvarts", "given": "V."}, {"family": "Sivak", "given": "V."}, {"family": "Skruzny", "given": "J."}, {"family": "C.", "given": "W."}, {"family": "D.", "given": "R."}, {"family": "Sterling", "given": "G."}, {"family": "Strain", "given": "D."}, {"family": "Szalay", "given": "M."}, {"family": "Thor", "given": "D."}, {"family": "Torres", "given": "A."}, {"family": "Vidal", "given": "G."}, {"family": "Vollgraff", "given": "C."}, {"family": "White", "given": "T."}, {"family": "W.", "given": "B."}, {"family": "Xing", "given": "C."}, {"family": "J.", "given": "Z."}, {"family": "Yeh", "given": "P."}, {"family": "Yoo", "given": "J."}, {"family": "Young", "given": "G."}, {"family": "Zalcman", "given": "A."}, {"family": "Zhang", "given": "Y."}, {"family": "Zhu", "given": "N."}, {"family": "Zobrist", "given": "N."}, {"family": "G.", "given": "E."}, {"family": "Biswas", "given": "R."}, {"family": "Babbush", "given": "R."}, {"family": "Bacon", "given": "D."}, {"family": "Hilton", "given": "J."}, {"family": "Lucero", "given": "E."}, {"family": "Neven", "given": "H."}, {"family": "Megrant", "given": "A."}, {"family": "Kelly", "given": "J."}, {"family": "Aleiner", "given": "I."}, {"family": "Smelyanskiy", "given": "V."}, {"family": "Kechedzhi", "given": "K."}, {"family": "Chen", "given": "Y."}, {"family": "Boixo", "given": "S."}],
  "DOI": "10.48550/arXiv.2304.11119",
  "title": "Phase transition in Random Circuit Sampling",
  "original-date": {
    "date-parts": [
      [2023, 04, 21]
    ]
  },
  "URL": "https://doi.org/10.48550/arXiv.2304.11119"
}
```

 ↩︎
5. ```csl
{
  "type": "misc"
  "id": 5,
  "author"=[{"family": "Begušić", "given": "Tomislav"}, {"family": "Kin-Lic Chan", "given": "Garnet"}],
  "DOI": "10.48550/arXiv.2306.16372",
  "title": "Fast classical simulation of evidence for the utility of quantum computing before fault tolerance",
  "original-date": {
    "date-parts": [
      [2023, 06, 28]
    ]
  },
  "URL": "https://doi.org/10.48550/arXiv.2306.16372"
}
```

 ↩︎
6. ```csl
{
  "type": "misc"
  "id": 6,
  "author"=[{"family": "Pednault", "given": "Edwin"}, {"family": "Gunnels", "given": "John A."}, {"family": "Nannicini", "given": "Giacomo"}, {"family": "Horesh", "given": "Lior"}, {"family": "Wisnieff", "given": "Robert"}],
  "DOI": "10.48550/arXiv.1910.09534",
  "title": "Leveraging Secondary Storage to Simulate Deep 54-qubit Sycamore Circuits",
  "original-date": {
    "date-parts": [
      [2019, 08, 22]
    ]
  },
  "URL": "https://doi.org/10.48550/arXiv.1910.09534",
  "custom": {
    "additional-urls": [
      "https://api.semanticscholar.org/CorpusID:204800933"
    ]
  }
```

 ↩︎
7. ```csl
{
  "type": "article"
  "id": 7,
  "author"=[{"family": "Castelvecchi", "given": "Davide"}],
  "DOI": "10.1038/d41586-023-00017-0",
  "title": "Are quantum computers about to break online privacy?",
  "original-date": {
    "date-parts": [
      [2023, 01, 06]
    ]
  },
  "URL": "https://doi.org/10.1038/d41586-023-00017-0"
```

 ↩︎

## Replies

**nikojpapa** (2024-11-26):

The ERC mentions a post by Anoncoin. I saw the rules about not having links in the ERC that do not have DOIs, so I will provide it here instead. [RSA UFO](https://anoncoin.github.io/RSA_UFO/). If anyone has a suggestion on putting it in the ERC, let me know!

