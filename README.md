
# P2P File Sharing and different Variants

Peer-to-peer system for efficient file sharing task supporting multiple peers to share one file simultaneously across heterogeneous devices and architectures using computer networks concepts and socket programming

---

## Table of Contents


- Module 1: One peer to another peer
- Module 2: Multiple peers to one peer
- Module 3: Corner Cases and flexible features

#### Separate ReadMe attached to each module
---

## Module 1: One peer to another peer
- Tracker-peer architecture

#### Run 

```html
    $ cd 1p2p
    $ py IP.py
    $ py tracker.py
    # py peer.py
```

---

## Module 2: Multiple peers to one peer

- Concurrent sharing of equivalent portion of file using threading

#### Run 

```html
    $ cd p2p_multiple
    $ py IP.py
    $ py tracker.py
    $ run multiple peers on different devices, or as different programs
    # py peer.py
```

![9](https://user-images.githubusercontent.com/46133803/109121371-291f7480-776d-11eb-97bb-08e44b92cb8b.png)

---

## Module 3: Corner Cases and flexible features

-  Flexibility during the change of wifi
-  Working under heterogeneous devices

![1](https://user-images.githubusercontent.com/46133803/109122316-66d0cd00-776e-11eb-99d0-168bd011c20e.png)


#### CornerCases
- What happens to the peer information at tracker when peer disconnects?
- What happens if one peer gets disconnected while sharing a file with another peer?
- What happens if one of the peers goes down while file sharing from multiple peers to one peer?

---

## Demo
[LINK](https://drive.google.com/drive/folders/14uxCkKPaWneU1bpen1CoSMZt1STIS8Bf?usp=sharing) 

#### NOTE: Run the IP.py file to change the corresponding IP address of wifi interface
