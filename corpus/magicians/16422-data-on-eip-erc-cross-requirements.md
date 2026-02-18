---
source: magicians
topic_id: 16422
title: Data on EIP/ERC Cross-Requirements
author: joeysantoro
date: "2023-11-02"
category: EIPs
tags: [erc, eip]
url: https://ethereum-magicians.org/t/data-on-eip-erc-cross-requirements/16422
views: 1054
likes: 5
posts_count: 2
---

# Data on EIP/ERC Cross-Requirements

Per discussion in [EIPIP meeting 93](https://github.com/ethereum-cat-herders/EIPIP/issues/285)

Here is the data on cross requirements for ERCs and EIPs:

```auto
5 EIPs that require 4 ERCs:
EIP-712 requires: 191
EIP-747 requires: 20, 1046
EIP-2256 requires: 55
EIP-5283 requires: 20
EIP-6493 requires: 191

Unique required ERCs:
20, 55, 191, 1046

41 ERCs that require 16 EIPs:
ERC-165 requires: 214
ERC-820 requires: 214
ERC-1077 requires: 1344
ERC-1167 requires: 211
ERC-1191 requires: 155
ERC-1710 requires: 155
ERC-1812 requires: 712
ERC-1820 requires: 214
ERC-1922 requires: 196, 197
ERC-1923 requires: 196, 197
ERC-2098 requires: 2
ERC-2193 requires: 155
ERC-2400 requires: 155
ERC-2470 requires: 1014
ERC-2525 requires: 1193
ERC-2612 requires: 712
ERC-2770 requires: 712
ERC-3009 requires: 712
ERC-3440 requires: 712
ERC-4361 requires: 155
ERC-4494 requires: 712
ERC-4973 requires: 712
ERC-5139 requires: 155
ERC-5202 requires: 170
ERC-5267 requires: 155, 712
ERC-5375 requires: 155, 712
ERC-5453 requires: 712
ERC-5539 requires: 712
ERC-5559 requires: 712
ERC-5568 requires: 140
ERC-5727 requires: 712
ERC-5805 requires: 712
ERC-5902 requires: 712
ERC-6120 requires: 1014
ERC-6384 requires: 712
ERC-6734 requires: 155, 3220
ERC-6865 requires: 712
ERC-7015 requires: 155, 712
ERC-7511 requires: 7, 211, 3855
ERC-7512 requires: 712
ERC-7550 requires: 712, 1153

Unique required EIPs:
2, 7, 140, 155, 170, 196, 197, 211, 214, 712, 1014, 1153, 1193, 1344, 3220, 3855
```

Seems like in general the cross requirements are a small subset of existing eips and ercs, especially the eips have almost no linking to ercs, and the ercs require a common subset of the eips.

I generated this with the following script:

```auto
import os
import re

# Paths to the directories containing EIP and ERC markdown files
eip_dir = '/path/to/eips'
erc_dir = '/path/to/ercs'

# Load the EIP and ERC numbers from the text files into sets for easy membership checking
with open('eips.txt') as f:
    eips = set(f.read().splitlines())

with open('ercs.txt') as f:
    ercs = set(f.read().splitlines())

# Function to parse required numbers from markdown files
def parse_requirements(md_file):
    with open(md_file, 'r') as file:
        content = file.read()
    matches = re.findall(r'^requires: ([\d, ]+)', content, re.MULTILINE)
    if matches:
        return set(matches[0].replace(' ', '').split(','))
    return set()

# Check EIPs for required ERCs
eip_requires_erc = {}
for eip_number in eips:
    eip_file = os.path.join(eip_dir, f'eip-{eip_number}.md')
    required = parse_requirements(eip_file)
    required_ercs = required & ercs  # Set intersection to find required ERCs
    if required_ercs:
        eip_requires_erc[eip_number] = required_ercs

# Check ERCs for required EIPs
erc_requires_eip = {}
for erc_number in ercs:
    erc_file = os.path.join(erc_dir, f'erc-{erc_number}.md')
    required = parse_requirements(erc_file)
    required_eips = required & eips  # Set intersection to find required EIPs
    if required_eips:
        erc_requires_eip[erc_number] = required_eips

# Sort the eip_requires_erc dictionary by EIP number
sorted_eip_requires_erc = {eip: sorted(eip_requires_erc[eip], key=int) for eip in sorted(eip_requires_erc, key=int)}

# Sort the erc_requires_eip dictionary by ERC number
sorted_erc_requires_eip = {erc: sorted(erc_requires_eip[erc], key=int) for erc in sorted(erc_requires_eip, key=int)}

# Find unique required EIPs and ERCs
unique_required_eips = set()
unique_required_ercs = set()

for req_ercs in eip_requires_erc.values():
    unique_required_ercs.update(req_ercs)

for req_eips in erc_requires_eip.values():
    unique_required_eips.update(req_eips)

# Output the results
print(f"{len(eip_requires_erc)} EIPs that require {len(unique_required_ercs)} ERCs:")
for eip, req_ercs in sorted_eip_requires_erc.items():
    print(f"EIP-{eip} requires: {', '.join(req_ercs)}")

print("\nUnique required ERCs:")
print(', '.join(sorted(unique_required_ercs, key=int)))

print(f"\n{len(erc_requires_eip)} ERCs that require {len(unique_required_eips)} EIPs:")
for erc, req_eips in sorted_erc_requires_eip.items():
    print(f"ERC-{erc} requires: {', '.join(req_eips)}")

print("\nUnique required EIPs:")
print(', '.join(sorted(unique_required_eips, key=int)))
```

eips.txt:

```auto
1
100
101
1010
1011
1013
1014
1015
1051
1052
1057
107
1087
1102
1108
1109
1153
1186
1193
1227
1234
1240
1276
1283
1285
1295
1344
1352
1355
1380
140
141
1418
145
1459
1470
1474
1482
1485
150
152
155
1559
1571
158
1588
160
161
1679
1681
1682
170
1702
1706
1716
1767
1803
1829
1872
1884
1890
1895
1898
1901
1930
1959
196
1962
1965
197
198
1985
2
2003
2014
2015
2025
2026
2027
2028
2029
2031
2035
2045
2046
2069
2070
210
211
2124
214
2159
2200
2228
2242
225
2255
2256
2294
2315
2327
233
2330
234
2364
2378
2384
2387
2458
2464
2474
2481
2488
2515
2537
2539
2542
2565
2566
2583
2584
2593
2657
2666
2677
2681
2696
2700
2711
2718
2733
2780
2786
2803
2831
2844
2926
2929
2930
2935
2936
2937
2938
2970
2972
2976
2982
2997
3
3014
3026
3030
3041
3044
3045
3046
3068
3074
3076
3085
3091
3102
3143
3155
3198
3220
3238
3267
3298
3300
3322
3326
3332
3336
3337
3338
3368
3372
3374
3382
3403
3416
3436
3455
3508
3520
3521
3529
3534
3540
3541
3554
3584
3607
3651
3670
3675
3690
3709
3756
3779
3788
3855
3860
3978
4
4200
4345
4396
4399
4444
4488
4520
4573
4736
4747
4750
4758
4760
4762
4788
4803
4844
4863
4881
4895
4938
5
5000
5003
5022
5027
5065
5069
5081
5133
5283
5345
5450
5478
5593
5656
5749
5757
5792
5793
5806
5920
5988
6
6046
6049
6051
606
607
608
609
6110
6122
615
616
6188
6189
6190
6206
627
6404
6465
6466
6475
649
6493
658
663
665
6690
6780
6789
6800
6810
6811
684
6873
6888
689
6913
6916
695
6953
6963
6968
698
6988
7
7002
7039
7044
7045
706
7069
712
7199
7212
7251
7266
7329
7377
7378
7441
747
7480
7495
7503
7514
7516
7519
7523
7539
758
778
779
8
858
86
867
868
908
969
999
```

ercs.txt

```auto
1046
1056
1062
1066
1077
1078
1080
1081
1123
1129
1132
1154
1155
1167
1175
1178
1185
1191
1202
1203
1207
1261
1271
1319
1328
1337
1363
137
1386
1387
1388
1417
1438
1444
1450
1462
1484
1491
1504
1523
1538
1577
1581
1592
1613
1616
162
1620
1633
165
1710
173
1753
1761
1775
181
1812
1820
1822
1844
190
1900
191
1921
1922
1923
1948
1967
1973
1996
20
2009
2018
2019
2020
2021
205
2098
2135
2157
2193
223
2266
2304
2309
2333
2334
2335
2386
2390
2400
2470
2477
2494
2520
2525
2535
2544
2569
2612
2615
2645
2678
2680
2746
2767
2770
2771
2848
2876
2917
2942
2980
2981
3000
3005
3009
3135
3156
3224
3234
3386
3440
3448
3450
3475
3525
3561
3569
3589
3643
3668
3722
3754
3770
3772
4337
4341
4353
4361
4393
4400
4430
4494
4519
4521
4524
4527
4546
4626
4671
4675
4799
4804
4824
4834
4883
4885
4886
4906
4907
4910
4931
4944
4950
4955
4972
4973
4974
4987
5005
5006
5007
5008
5018
5023
5050
5058
5094
5095
5114
5115
5131
5139
5143
5164
5169
5173
5185
5187
5189
5192
5202
5216
5218
5219
5247
5252
5267
5269
5289
5298
5313
5334
5375
5380
5409
5437
5453
5484
5485
5489
5496
55
5501
5505
5507
5516
5521
5528
5539
5553
5554
5559
5560
5564
5568
5570
5573
5585
5604
5606
5615
5625
5630
5633
5635
5639
5643
5646
5679
5700
5719
5725
5727
5732
5744
5750
5753
5773
5791
5805
5827
5850
5851
5883
5902
5982
600
601
6047
6059
6065
6066
6093
6105
6120
6123
6147
6150
6170
6220
6224
6239
6268
6315
6327
634
6353
6357
6358
6366
6372
6381
6384
6454
6464
6492
6506
6538
6551
6596
6604
6617
6662
6672
6682
67
6734
6735
6785
6786
6787
6806
6808
6809
681
6821
6823
6860
6864
6865
6900
6909
6944
6956
6960
6981
6982
6997
7007
7015
7053
7066
7085
7092
7093
7144
7160
7201
721
7231
725
7254
7303
7401
7405
7406
7409
7412
7417
7425
7432
7444
7484
7507
7508
7511
7512
7521
7522
7528
7535
7540
7550
777
801
820
823
831
875
884
897
900
902
918
926
927
998
```

## Replies

**xinbenlv** (2023-11-10):

Thank you for the great efforts [@joeysantoro](/u/joeysantoro)  This is very helpful.

