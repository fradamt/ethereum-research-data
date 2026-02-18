---
source: magicians
topic_id: 25567
title: FOCIL Breakout #20, September 23, 2025
author: system
date: "2025-09-23"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/focil-breakout-20-september-23-2025/25567
views: 811
likes: 1
posts_count: 11
---

# FOCIL Breakout #20, September 23, 2025

### Agenda

- Development updates

**Meeting Time:** Tuesday, September 23, 2025 at 14:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1737)

## Replies

**system** (2025-09-23):

### Meeting Summary:

The team reviewed development metrics and testing updates for various projects, including discussions about implementing new metrics, simulating failing inclusion lists, and interop testing between different clients. Progress updates were shared on multiple projects, with specific focus on addressing issues related to slot handling, block proposal failures, and zero-inclusion lists across different clients. The team agreed to maintain bi-weekly meetings and discussed plans for future presentations and implementations, including FOCIL implementation in native roll-ups.

**Click to expand detailed summary**

The team discussed development metrics and testing updates for Fossil. Katya reported adding new metrics to Lodestar and suggested simulating failing inclusion lists to test client behavior. Jihoon proposed using CLI flags and author tests for this purpose. They agreed to implement these tests once Fossil is included in Glamsterdam. Katya mentioned some issues with Lodestar and suggested interop testing with other clients like RISC and Lighthouse. Jihoon noted that Prism needs rebasing work and will start working on it after completing other tasks.

The team discussed updates on various projects, including Katya’s plans to run Lodar and Jihoon’s work on spec tests aiming to complete them by the week. Pelle shared progress on Reth, explaining changes to slot handling and issues with missing inclusion lists, which he is addressing by modifying the code to grab from one slot behind. Pelle also mentioned ongoing work to resolve block proposal failures, which he suspects may be related to inclusion issues, and plans to open a PR for these updates.

The team discussed debugging progress for EL interop and identified potential issues with Geth and Lodestar regarding zero-inclusion lists. They agreed to test metrics dashboard interop between Lighthouse and Lodestar clients, with Katya noting that long-term observation of metrics would be useful for DevOps teams. The group decided to maintain bi-weekly meetings rather than switching to monthly, and Jihoon mentioned that Luca would present an idea about FOCIL implementation in native roll-ups at the next meeting.

### Next Steps:

- Jihoon to finish spec tests and open a PR against Consensus’ spec repo by the end of the week.
- Pelle to fix the issue with Reth grabbing inclusion lists from slot N instead of slot N-1 and open a PR.
- Pelle to investigate why some blocks are missing/not being proposed in Geth and Reth interop.
- Pelle to adjust the seconds per slot value from 6 to 12 for proper inclusion list submission.
- Pelle and Katya to collaborate on adding metrics on the EL side.
- Jihoon to ask Luca to join the next breakout call to share his idea on Fossil in native roll-ups.
- Katya to continue working with the Lodestar team to resolve current issues.
- Katya to explore interop testing with Lighthouse for metrics once Lodestar is running properly.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: G1K$zRYy)
- Download Chat (Passcode: G1K$zRYy)

---

**system** (2025-09-23):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=zRbJyjpRDQw

---

**system** (2025-09-24):

### Meeting Summary:

The team reviewed development metrics and testing updates for various projects, including discussions about implementing new metrics, simulating failing inclusion lists, and interop testing between different clients. Progress updates were shared on multiple projects, with specific focus on addressing issues related to slot handling, block proposal failures, and zero-inclusion lists across different clients. The team agreed to maintain bi-weekly meetings and discussed plans for future presentations and implementations, including FOCIL implementation in native roll-ups.

**Click to expand detailed summary**

The team discussed development metrics and testing updates for Fossil. Katya reported adding new metrics to Lodestar and suggested simulating failing inclusion lists to test client behavior. Jihoon proposed using CLI flags and author tests for this purpose. They agreed to implement these tests once Fossil is included in Glamsterdam. Katya mentioned some issues with Lodestar and suggested interop testing with other clients like RISC and Lighthouse. Jihoon noted that Prism needs rebasing work and will start working on it after completing other tasks.

The team discussed updates on various projects, including Katya’s plans to run Lodar and Jihoon’s work on spec tests aiming to complete them by the week. Pelle shared progress on Reth, explaining changes to slot handling and issues with missing inclusion lists, which he is addressing by modifying the code to grab from one slot behind. Pelle also mentioned ongoing work to resolve block proposal failures, which he suspects may be related to inclusion issues, and plans to open a PR for these updates.

The team discussed debugging progress for EL interop and identified potential issues with Geth and Lodestar regarding zero-inclusion lists. They agreed to test metrics dashboard interop between Lighthouse and Lodestar clients, with Katya noting that long-term observation of metrics would be useful for DevOps teams. The group decided to maintain bi-weekly meetings rather than switching to monthly, and Jihoon mentioned that Luca would present an idea about FOCIL implementation in native roll-ups at the next meeting.

### Next Steps:

- Jihoon to finish spec tests and open a PR against Consensus’ spec repo by the end of the week.
- Pelle to fix the issue with Reth grabbing inclusion lists from slot N instead of slot N-1 and open a PR.
- Pelle to investigate why some blocks are missing/not being proposed in Geth and Reth interop.
- Pelle to adjust the seconds per slot value from 6 to 12 for proper inclusion list submission.
- Pelle and Katya to collaborate on adding metrics on the EL side.
- Jihoon to ask Luca to join the next breakout call to share his idea on Fossil in native roll-ups.
- Katya to continue working with the Lodestar team to resolve current issues.
- Katya to explore interop testing with Lighthouse for metrics once Lodestar is running properly.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: G1K$zRYy)
- Download Chat (Passcode: G1K$zRYy)

---

**system** (2025-09-24):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=zRbJyjpRDQw

---

**system** (2025-09-24):

### Meeting Summary:

The team reviewed development metrics and testing updates for various projects, including discussions about implementing new metrics, simulating failing inclusion lists, and interop testing between different clients. Progress updates were shared on multiple projects, with specific focus on addressing issues related to slot handling, block proposal failures, and zero-inclusion lists across different clients. The team agreed to maintain bi-weekly meetings and discussed plans for future presentations and implementations, including FOCIL implementation in native roll-ups.

**Click to expand detailed summary**

The team discussed development metrics and testing updates for Fossil. Katya reported adding new metrics to Lodestar and suggested simulating failing inclusion lists to test client behavior. Jihoon proposed using CLI flags and author tests for this purpose. They agreed to implement these tests once Fossil is included in Glamsterdam. Katya mentioned some issues with Lodestar and suggested interop testing with other clients like RISC and Lighthouse. Jihoon noted that Prism needs rebasing work and will start working on it after completing other tasks.

The team discussed updates on various projects, including Katya’s plans to run Lodar and Jihoon’s work on spec tests aiming to complete them by the week. Pelle shared progress on Reth, explaining changes to slot handling and issues with missing inclusion lists, which he is addressing by modifying the code to grab from one slot behind. Pelle also mentioned ongoing work to resolve block proposal failures, which he suspects may be related to inclusion issues, and plans to open a PR for these updates.

The team discussed debugging progress for EL interop and identified potential issues with Geth and Lodestar regarding zero-inclusion lists. They agreed to test metrics dashboard interop between Lighthouse and Lodestar clients, with Katya noting that long-term observation of metrics would be useful for DevOps teams. The group decided to maintain bi-weekly meetings rather than switching to monthly, and Jihoon mentioned that Luca would present an idea about FOCIL implementation in native roll-ups at the next meeting.

### Next Steps:

- Jihoon to finish spec tests and open a PR against Consensus’ spec repo by the end of the week.
- Pelle to fix the issue with Reth grabbing inclusion lists from slot N instead of slot N-1 and open a PR.
- Pelle to investigate why some blocks are missing/not being proposed in Geth and Reth interop.
- Pelle to adjust the seconds per slot value from 6 to 12 for proper inclusion list submission.
- Pelle and Katya to collaborate on adding metrics on the EL side.
- Jihoon to ask Luca to join the next breakout call to share his idea on Fossil in native roll-ups.
- Katya to continue working with the Lodestar team to resolve current issues.
- Katya to explore interop testing with Lighthouse for metrics once Lodestar is running properly.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: G1K$zRYy)
- Download Chat (Passcode: G1K$zRYy)

---

**system** (2025-09-24):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=zRbJyjpRDQw

---

**system** (2025-09-24):

### Meeting Summary:

The team reviewed development metrics and testing updates for various projects, including discussions about implementing new metrics, simulating failing inclusion lists, and interop testing between different clients. Progress updates were shared on multiple projects, with specific focus on addressing issues related to slot handling, block proposal failures, and zero-inclusion lists across different clients. The team agreed to maintain bi-weekly meetings and discussed plans for future presentations and implementations, including FOCIL implementation in native roll-ups.

**Click to expand detailed summary**

The team discussed development metrics and testing updates for Fossil. Katya reported adding new metrics to Lodestar and suggested simulating failing inclusion lists to test client behavior. Jihoon proposed using CLI flags and author tests for this purpose. They agreed to implement these tests once Fossil is included in Glamsterdam. Katya mentioned some issues with Lodestar and suggested interop testing with other clients like RISC and Lighthouse. Jihoon noted that Prism needs rebasing work and will start working on it after completing other tasks.

The team discussed updates on various projects, including Katya’s plans to run Lodar and Jihoon’s work on spec tests aiming to complete them by the week. Pelle shared progress on Reth, explaining changes to slot handling and issues with missing inclusion lists, which he is addressing by modifying the code to grab from one slot behind. Pelle also mentioned ongoing work to resolve block proposal failures, which he suspects may be related to inclusion issues, and plans to open a PR for these updates.

The team discussed debugging progress for EL interop and identified potential issues with Geth and Lodestar regarding zero-inclusion lists. They agreed to test metrics dashboard interop between Lighthouse and Lodestar clients, with Katya noting that long-term observation of metrics would be useful for DevOps teams. The group decided to maintain bi-weekly meetings rather than switching to monthly, and Jihoon mentioned that Luca would present an idea about FOCIL implementation in native roll-ups at the next meeting.

### Next Steps:

- Jihoon to finish spec tests and open a PR against Consensus’ spec repo by the end of the week.
- Pelle to fix the issue with Reth grabbing inclusion lists from slot N instead of slot N-1 and open a PR.
- Pelle to investigate why some blocks are missing/not being proposed in Geth and Reth interop.
- Pelle to adjust the seconds per slot value from 6 to 12 for proper inclusion list submission.
- Pelle and Katya to collaborate on adding metrics on the EL side.
- Jihoon to ask Luca to join the next breakout call to share his idea on Fossil in native roll-ups.
- Katya to continue working with the Lodestar team to resolve current issues.
- Katya to explore interop testing with Lighthouse for metrics once Lodestar is running properly.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: G1K$zRYy)
- Download Chat (Passcode: G1K$zRYy)

---

**system** (2025-09-24):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=zRbJyjpRDQw

---

**system** (2025-09-24):

### Meeting Summary:

The team reviewed development metrics and testing updates for various projects, including discussions about implementing new metrics, simulating failing inclusion lists, and interop testing between different clients. Progress updates were shared on multiple projects, with specific focus on addressing issues related to slot handling, block proposal failures, and zero-inclusion lists across different clients. The team agreed to maintain bi-weekly meetings and discussed plans for future presentations and implementations, including FOCIL implementation in native roll-ups.

**Click to expand detailed summary**

The team discussed development metrics and testing updates for Fossil. Katya reported adding new metrics to Lodestar and suggested simulating failing inclusion lists to test client behavior. Jihoon proposed using CLI flags and author tests for this purpose. They agreed to implement these tests once Fossil is included in Glamsterdam. Katya mentioned some issues with Lodestar and suggested interop testing with other clients like RISC and Lighthouse. Jihoon noted that Prism needs rebasing work and will start working on it after completing other tasks.

The team discussed updates on various projects, including Katya’s plans to run Lodar and Jihoon’s work on spec tests aiming to complete them by the week. Pelle shared progress on Reth, explaining changes to slot handling and issues with missing inclusion lists, which he is addressing by modifying the code to grab from one slot behind. Pelle also mentioned ongoing work to resolve block proposal failures, which he suspects may be related to inclusion issues, and plans to open a PR for these updates.

The team discussed debugging progress for EL interop and identified potential issues with Geth and Lodestar regarding zero-inclusion lists. They agreed to test metrics dashboard interop between Lighthouse and Lodestar clients, with Katya noting that long-term observation of metrics would be useful for DevOps teams. The group decided to maintain bi-weekly meetings rather than switching to monthly, and Jihoon mentioned that Luca would present an idea about FOCIL implementation in native roll-ups at the next meeting.

### Next Steps:

- Jihoon to finish spec tests and open a PR against Consensus’ spec repo by the end of the week.
- Pelle to fix the issue with Reth grabbing inclusion lists from slot N instead of slot N-1 and open a PR.
- Pelle to investigate why some blocks are missing/not being proposed in Geth and Reth interop.
- Pelle to adjust the seconds per slot value from 6 to 12 for proper inclusion list submission.
- Pelle and Katya to collaborate on adding metrics on the EL side.
- Jihoon to ask Luca to join the next breakout call to share his idea on Fossil in native roll-ups.
- Katya to continue working with the Lodestar team to resolve current issues.
- Katya to explore interop testing with Lighthouse for metrics once Lodestar is running properly.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: G1K$zRYy)
- Download Chat (Passcode: G1K$zRYy)

---

**system** (2025-09-24):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=zRbJyjpRDQw

