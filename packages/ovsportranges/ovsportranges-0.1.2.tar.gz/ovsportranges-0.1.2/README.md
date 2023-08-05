# ovsportranges

### Description
Openflow requires port ranges to be defined as bitwise matches. This module 
provides an easy way to the port/mask ranges for a specified port range.

As described in the [ovs-ofctl](http://www.openvswitch.org/support/dist-docs-2.5/ovs-ofctl.8.txt) documentation:
> Bitwise  match  on  TCP  (or  UDP or SCTP) source or destination
> port.  The port and mask are 16-bit numbers written  in  decimal
> or  in  hexadecimal prefixed by 0x.  Each 1-bit in mask requires
> that the corresponding bit in port must match.   Each  0-bit  in
> mask causes the corresponding bit to be ignored.

It is recommended to only use this for large ranges that would require a large number of flows.

### Installation
`pip install ovsportranges`

### Basic Usage
``` python
from ovsportrange import OvsPorts

if __name__ == "__main__":
    ovsports = OvsPorts()
    ranges = ovsports.get_port_ranges(1000, 1999)
    for r in ranges:
        print("Port: {}, Bitmask: {}".format(r.port, r.bitmask))
```

### Output
```text
Port: 1000, Bitmask: 65528
Port: 1008, Bitmask: 65520
Port: 1024, Bitmask: 65024
Port: 1536, Bitmask: 65280
Port: 1792, Bitmask: 65408
Port: 1920, Bitmask: 65472
Port: 1984, Bitmask: 65520
```
