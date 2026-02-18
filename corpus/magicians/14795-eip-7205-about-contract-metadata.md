---
source: magicians
topic_id: 14795
title: "EIP-7205: About Contract Metadata"
author: Beatove
date: "2023-06-22"
category: EIPs
tags: [erc]
url: https://ethereum-magicians.org/t/eip-7205-about-contract-metadata/14795
views: 596
likes: 1
posts_count: 3
---

# EIP-7205: About Contract Metadata

Discussion thread for [EIP-7205: About Contract Metadata](https://github.com/ethereum/EIPs/pull/7238)

The standard introduces the ‘about()’ function.

This function empowers contract creators to enrich contract details with essential information like company/personal data, social media links, and tailored extensions for security audits or collection-specific features.

This is an example of what the metadata might return

```auto
{
	"company": "",
	"company_id": "",
	"country": "",
	"contact_mail": "",
	"website": "",
	"documentation": "",
	"marketplace": {
		"banner": "",
		"logo": "",
		"description": ""
	},
	"security_audit": {
		"security_audit_provider": "",
		"audited_report_url": "",
		"audit_date": ""
	},
	"social_links": {
		"twitter": "",
		"instagram": "",
		"discord": "",
		"medium": ""
	}
}
```

## Replies

**pugakn** (2023-07-19):

What is different from using https://docs.opensea.io/docs/contract-level-metadata ?

---

**Beatove** (2023-07-19):

Hello [@pugakn](/u/pugakn) ,

I have a similar idea, but I believe it would be beneficial for the Ethereum community to standardize the function name and also discuss the required parameters. Instead of limiting it to ERC721 and ERC1155 on OpenSea, the contractURI function could be more generalized and applicable to other standards as well.

