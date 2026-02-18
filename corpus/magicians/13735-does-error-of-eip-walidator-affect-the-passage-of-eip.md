---
source: magicians
topic_id: 13735
title: Does error of `EIP Walidator` affect the passage of eip?
author: shadow001
date: "2023-04-09"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/does-error-of-eip-walidator-affect-the-passage-of-eip/13735
views: 615
likes: 3
posts_count: 9
---

# Does error of `EIP Walidator` affect the passage of eip?

EIP Walidator:

```auto
Error: error[markdown-rel-links]: non-relative link or image
```

I found that the markdown of eip contains external links, and this error will appear, and there is a w-ci tag. How should this be resolved.

## Replies

**Perrin** (2023-04-10):

Hi, please can you share a link?

---

**shadow001** (2023-04-12):

Link as follows:



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/6239)














####


      `master` ← `JessicaChg:master`




          opened 01:42PM - 30 Dec 22 UTC



          [![](https://avatars.githubusercontent.com/u/117890123?v=4)
            JessicaChg](https://github.com/JessicaChg)



          [+302
            -0](https://github.com/ethereum/EIPs/pull/6239/files)







When opening a pull request to submit a new EIP, please use the suggested templa[…](https://github.com/ethereum/EIPs/pull/6239)te: https://github.com/ethereum/EIPs/blob/master/eip-template.md

We have a GitHub bot that automatically merges some PRs. It will merge yours immediately if certain criteria are met:

 - The PR edits only existing draft PRs.
 - The build passes.
 - Your GitHub username or email address is listed in the 'author' header of all affected PRs, inside <triangular brackets>.
 - If matching on email address, the email address is the one publicly listed on your GitHub profile.












I need to use an external link to illustrate W3C’s format definition of RDF statements.But I’m not sure if this error would affect the review of the EIP.

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/8/87abd8d6e6b9139b99c24437fb4264a63479c3c7_2_690x284.png)image1888×778 88.8 KB](https://ethereum-magicians.org/uploads/default/87abd8d6e6b9139b99c24437fb4264a63479c3c7)

---

**shadow001** (2023-04-21):

[@Perrin](/u/perrin) Do you know how to solve this problem?

Looks like the last meeting that has ended didn’t edit our eip, not sure if it has something to do with our eip containing the w-ci tag.

https://github.com/ethereum-cat-herders/EIPIP/issues/225

---

**shadow001** (2023-04-21):

[@poojaranjan](/u/poojaranjan)

Hello, our EIP has been modified, how can we add our EIP to the next editing meeting, let the editors review the latest modification to advance EIP to the next stage.

---

**poojaranjan** (2023-04-25):

Please add PR [Here](https://github.com/ethereum-cat-herders/EIPIP/issues/228).

---

**NicolasBierman** (2023-04-26):

This may be caused by the fact that your document has external links that are not relative. To fix this error, you need to update the links in your document to be relative. Relative links begin with a dot, such as ./myimage.png or ./mydocument.pdf. This means that they refer to the current directory. If you use the w-ci tag, this may indicate that your document is undergoing continuous integration and validation (CI/CD) as part of some development process. In that case, you may need to set up your validation process so that it only checks relative references. If you can’t change the links in the document or customize the validation process, you can try using absolute links, which specify the full path to the file or resource, starting at the root of your domain. For example, https://example.com/images/myimage.png.

---

**shadow001** (2023-05-03):

Thanks, We have removed the external links. Can you consider merging the request?

---

**poojaranjan** (2023-05-03):

Looks like the edits suggested by the editor have been made. If there aren’t any further edits left, one of the reviewers will merge the PR. In case the pull request isn’t merged before the next meeting, please add that to the [comment](https://github.com/ethereum-cat-herders/EIPIP/issues/231) and I’ll add it to the agenda.

