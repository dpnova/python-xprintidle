# python-xprintidle
A cffi wrapper around xprintidle.

This uses a modified version of xprintidle.c from https://github.com/pmaia/xprintidle-plus - I'm fairly sure I've satisfied the GPL but not 100% sure. Please let me know if there's an issue!

Usage/docs coming soon.

For now:

```
import xprintidle
print xprintidle.idle_time()
```

## Requires

* libX11
* libXss
* a c compiler and python dev headers

## Installation

`pip install xprintidle`
