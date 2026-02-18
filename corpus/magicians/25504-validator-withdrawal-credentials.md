---
source: magicians
topic_id: 25504
title: Validator withdrawal credentials
author: Kuko0419
date: "2025-09-17"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/validator-withdrawal-credentials/25504
views: 57
likes: 0
posts_count: 4
---

# Validator withdrawal credentials

Hello, my name is Rodney Martin.

I am running a validator (index 1517530) and I have faced serious issues since early this year. Around March–April, I had a transaction reversal and multiple transactions got stuck. At the same time, my validator withdrawal credentials were set incorrectly (to a 0x01 address not under my control).

Since then, I have been trying to change the withdrawal credentials back to my own address, but every attempt to broadcast the SignedBLSToExecutionChange JSON has failed with validation errors. I also generated credentials using different tools (ethdo, Wagyu Key Gen, deposit-cli), but none of them were accepted.

Additionally, I have been a victim of theft (unauthorized addresses were set and received my staking rewards). I reported this in GitHub and can provide detailed documentation and evidence in PDF form.

Now I am looking for help to:

1.	Correct my validator withdrawal credentials.

2.	Understand if I can still upgrade/change to a valid address (with the new validator update rules).

3.	Recover or at least secure my validator for future rewards.if someone want know about the the report I did where I expose this robber I will let the link in n the profile …  ["Validator Withdrawal Address Hijacked – Signed Change Ignored, Rewards Redirected to Unauthorized Addresses" · community · Discussion #162012 · GitHub](https://github.com/orgs/community/discussions/162012)  , bc I m really need like big help for organized my stuff and some clarification bc I have been trying so hard my self for more than a year pushing all my strength to the limit learning 24/7 , and all what I have been receiving is attacks from this scam people than destroy my machine , I have a new one now , but I m a little frustrated about all this so but mentally I m ok for do strong textwherever and I m able to do programming if I need and wherever help will be very appreciated if is coming from good people …sorry my words sometime are not good enough in English but I will understand wherever or any contribution for minimum is accepted so …or I will use translate in case np…

I appreciate any guidance from the community or the team.

Thank you,

Rodney Martin

Toronto, Canada

## Replies

**abcoathup** (2025-09-17):

Suggest asking the EthStaker community, either on Reddit or their Discord.

Beware of DMs and scammers.

https://www.reddit.com/r/ethstaker/


      ![image](https://discord.com/assets/favicon.ico)

      [Discord](https://discord.com/invite/ethstaker)





###



Check out the ethstaker community on Discord - hang out with 25935 other members and enjoy free voice and text chat.

---

**Kuko0419** (2025-09-18):

you know if with this update , I m allow to changed the 0x1 to 0x2 with a smart contract , bc I m really don’t know why if I did everything and I even changed my withdrawal credential to 0x1 why the addres of the scam people still in my profile …thanks for the links but for me is very hard trust in anyone ,but thanks a lot for the links…if you can help me with this with just the information is all I will need , if not is ok is appreciated your help as well ..thanks

[![IMG_4703](https://ethereum-magicians.org/uploads/default/optimized/3X/6/c/6c6e57266a58d2bfe3bc0d688a1be4a2acf61361_2_230x500.jpeg)IMG_47031290×2796 251 KB](https://ethereum-magicians.org/uploads/default/6c6e57266a58d2bfe3bc0d688a1be4a2acf61361)

… [

{

“message”: {

“bls_to_execution_change”: {

“validator_index”: 1517530,

“from_bls_pubkey”: “0xa6dbb3648bfcded97b66a48980f1ec441c32ca400a5c65a18b9380c22f8971ad9c52b6a30f66162e58aed3f5ed124900”,

“to_execution_address”: “0xdf09351b70f2a12c0020826fea2ccbb7857a2e99”

}

},

“signature”: “0x973240301102dcd64381005f9bb294b80ba55dbe9cea601073161c67b7b645e33fe12a72347f85ad0eb42de8915f7a0a0ad00388ab4de09bab71e7b41f8aecbfd9dabd4a6eb470323f28b08299d04a8e092e9cbf83f558a2ba673bb1a389269d”,

“metadata”: {

“network_name”: “mainnet”,

“genesis_validators_root”: “0x4b363db94e286120d76eb905340fdd4e54bfe9f06bf33ff6cf3ad27f511bfe95”,

“deposit_cli_version”: “1.1.0”

}

}

]

[![IMG_4703](https://ethereum-magicians.org/uploads/default/optimized/3X/6/c/6c6e57266a58d2bfe3bc0d688a1be4a2acf61361_2_230x500.jpeg)IMG_47031290×2796 251 KB](https://ethereum-magicians.org/uploads/default/6c6e57266a58d2bfe3bc0d688a1be4a2acf61361)

---

**abcoathup** (2025-09-19):

This isn’t anything I can help with.

Check [Ethereum.org](http://Ethereum.org) for where to go for help, Eth Staker is listed there.

[Ethereum support | ethereum.org](https://ethereum.org/community/support/#node-support)

