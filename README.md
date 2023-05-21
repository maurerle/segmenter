# segmenter

This project contains the segment watchdog as well as the geo segmenter.
Using these two is a possible solution to the missing scalability of large BATMAN networks.

Instead of requesting the user to download the matching firmware based on the installation region or selecting the region in the installation procedure, this is a server side approach which limits which wireguard tunnel lets a gluon-node in.

## functionality

The project is splitted into two parts, the geosegmenter which is run manually and the watchdog which runs on every supernode as a service.

### Geosegmenter

The geosegmenter uses a directory of shapefiles used to separate the mesh-network into regions.
By using the nodes.json from a meshviewer, the coordinates of gluon-nodes, where available, are used to determine the matching region/segment.

The geosegmenter can be configured through environment variables or at the top of the file.
It can be executed on demand running 

```bash
export CLONE_URL="https://github.com/ffac/peers-wg"
export HTTP_NODE_URL="http://url/to/nodes.json
export REPOSITORY="/etc/peers-wg"
./geosegmenter.py
```

### Segment-Watchdog

The watchdog runs as a service and monitors the visible BATMAN gateways on a supernode.
If two gluon-nodes from different segments can see each other, the gateway of the other segment becomes visible on the first supernode (and vice versa).
Then the device which sits in the segment with lower priority is then moved to the segment with higher priority, so that both devices are in the same segment and the mesh clouds are splitted correctly.
Moving the gluon-node to the different segment is done by changing the allowed wireguard server port, by moving its public key to a different folder in the keys repository (e.g. https://github.com/ffac/peers-wg). The client then reconnects into the new segment.



```bash
export CLONE_URL="https://github.com/ffac/peers-wg"
export HTTP_NODE_URL="http://url/to/nodes.json
export REPOSITORY="/etc/peers-wg"
./watchdog.py
```


## related projects

Historically, domains were named "segment" in ffac, but the usage is the same, except that the user does not manually decide the used segment.
Other approaches to tackle scalability in BATMAN by reducing the number of devices in one mesh cloud are:

* manually [using config-mode-domain-select and multidomain support in gluon](https://gluon.readthedocs.io/en/latest/features/multidomain.html#via-config-mode)
* [ffh-obedient-meshing](https://github.com/freifunkh/ffh-packages/pull/6)
* [hood-selector](https://gluon.readthedocs.io/en/latest/package/gluon-hoodselector.html)