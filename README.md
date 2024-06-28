# RepCl.py
A python implementation of Replay Clocks (RepCl), inspired by [replay-clocks](https://github.com/shaanzie/replay-clocks).

## Dependencies
None! :D

## Usage
Run `./main.py <proc_id_A> <proc_id_B>` and `./main.py <proc_id_B> <proc_id_A>` in two separate shells and watch the magic unfold.

`proc_id`s are integers used to uniquely identify processes. This script also runs a socket on the same port as `proc_id`, so you might want to choose non standard port numbers above 1024.
