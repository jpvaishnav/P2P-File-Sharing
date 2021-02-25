
# P2P File Sharing and Different Variants

Peer-to-peer system for efficient file sharing task supporting multiple peers to share one file simultaneously across heterogeneous devices and architectures using computer networks concepts and socket programming

---

### Table of Contents


- [Module 1: One peer to another peer](#Module 1: One peer to another peer)
- [Module 2: Multiple peers to one peer](Module 2: Multiple peers to one peer)
- [Module 3: Corner Cases and flexible features](#Module 3: Corner Cases and flexible features)

---

## Module 1: One peer to another peer
- Tracker-peer architecture

## Run 

```html
    $ cd 1p2p
    $ py IP.py
    $ py tracker.py
    # py peer.py
```

---

## Module 2: Multiple peers to one peer

- Concurrent sharing of equivalent portion of file using threading

## Run 

```html
    $ cd p2p_multiple
    $ py IP.py
    $ py tracker.py
    $ run multiple peers on different devices, or as different programs
    # py peer.py
```


## Module 3: Corner Cases and flexible features

-  Flexibility during the change of wifi
-  Working under heterogeneous devices

#### CornerCases
- What happens to the peer information at tracker when peer disconnects?
- What happens if one peer gets disconnected while sharing a file with another peer?
- What happens if one of the peers goes down while file sharing from multiple peers to one peer?

---
