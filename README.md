# OTree Experiment - Coalition Formation

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

> An oTree app for running an economic experiment on coalition formation and ambiguity aversion.

![preview](/preview.png)

## Table of Contents
- [Overview](#overview)
- [Details](#details)
- [Installation](#installation)
- [Usage](#usage)
- [About](#about)
  
## Overview

1. Coalition Formation

In each round, 3 participants are grouped together and negotiate to form a coalition.

The potential coalitions and values are:

- ABC
- AB
- AC
- BC

The main negotiation occurs on the Interaction page:

- Players can propose splits for the 4 potential coalitions
- Other players can accept offers to form coalition
- Chat interface for negotiating
- If no agreement after 10 mins, outside options

The process:

- Propose splits using input boxes
- Submit sends offer to other players
- Players accept own offers automatically
- When all accept, coalition forms
- See accept status, chat to coordinate

Game data stores:

- Formed coalition
- Shares for each player
- Acceptance status
- Chat history

2. Ambiguity Aversion

There are 4 treatments:

- Ambiguity & Loss Frame
- Ambiguity & No Loss Frame
- No Ambiguity & Loss Frame
- No Ambiguity & No Loss Frame

In the main treatments, participants make an investment decision between a risky option and a safe option. Payoffs vary based on treatment.

There are comprehension questions to check understanding before the main tasks.

Participants are randomized into one of the treatments. At the end their bonus payoff is shown.

## Details

Main Coalition Formation App:

- coalition

Main Treatment Apps:

- ambiguity_loss_frame
- ambiguity_no_loss_frame
- no_ambiguity_loss_frame
- no_ambiguity_no_loss_frame

## Installation

Make sure oTree is installed before running the app:

```bash
pip install otree
```

## Usage

To run the app:

1. Direct to the right directory
2. Reset the database: otree resetdb
3. Start the server: otree devserver
4. Go to http://localhost:8000

Make sure to reset the database between test sessions.

## About

This app was built for [Dr. Carpenter](http://community.middlebury.edu/~jcarpent/) and [Dr. Robbett](https://sites.google.com/view/robbett) to test theories of coalition formation and ambiguity aversion in decision making.