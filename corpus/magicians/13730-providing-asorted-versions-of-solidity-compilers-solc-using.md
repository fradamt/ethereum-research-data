---
source: magicians
topic_id: 13730
title: Providing asorted versions of solidity compilers (solc) using Nix
author: hellwolf
date: "2023-04-08"
category: Magicians > Tooling
tags: []
url: https://ethereum-magicians.org/t/providing-asorted-versions-of-solidity-compilers-solc-using-nix/13730
views: 472
likes: 0
posts_count: 1
---

# Providing asorted versions of solidity compilers (solc) using Nix

**TLDR; get started in few steps:**

1. Install the “Nix: the package manager” if you haven’t or not using NixOS.
2. Enable Nix Flake following the instruction in the link, e.g.:
add experimental-features = nix-command flakes to your ~/.config/nix/nix.conf.
3. Have any solc version available in your shell by running e.g.:
nix shell github:hellwolf/solc.nix#solc_0_4_26 github:hellwolf/solc.nix#solc_0_8_19

**Full readme & repository**

https://github.com/hellwolf/solc.nix/
