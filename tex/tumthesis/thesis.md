# Introduction and Background

In this brief section, we introduce the topic of our research and some
of the background knowledge needed to fully understand further
developments. Additionally we present literature we examined while
performing our measurements.

## Introduction

Starlink[^1] is the largest Low Earth Orbiting (LEO) satellite
constellation with more than 4000 satellites currently orbiting around
Earth. It is managed by SpaceX[^2], and its scope is to bring Internet
broadband connection to the most remote and rural areas in the world
while also serving people living in residential districts, currently
typically using a cabled link.

LEO satellites orbit around 550 kilometers from Earth, so naturally, LEO
connections have a lower latency than other satellite-based connections.
SpaceX claims latency is around approximately 25 milliseconds; however
our experiments show that it is often a little higher (approximately 35
milliseconds). It is, though, worth mentioning it might be possible that
using laser links is faster than fiber on Earth due to the higher speed
of light in vacuum and shorter path than undersea fiber, as reported by
Elon Musk himself[@tweet].

Starlink might not be the best solution for people living in residential
areas, as their place is covered by a faster cabled connection and is
probably way cheaper as the infrastructure is more straightforward to
maintain; as of October 2023, Starlink costs 65 USD per month with a
one-time hardware cost of 450 USD. Satellite-based Internet connections
have been around for several years. They are typically based on
geostationary satellites (GEOSAT), orbiting at about 35,000 kilometers.
It is thus natural to expect higher latency when comparing GEOSAT
connections to cabled Internet connections; about around 600
milliseconds for latency, or in other words, Starlink averages  70 RTTs
in the time a GEOSAT connection is able to send a single packet back and
forth.

From a customer perspective, using Starlink is straightforward. After
receiving the hardware, the only needed step is to plug the satellite
dish (see Figure [1.2](#fig:dish){reference-type="ref"
reference="fig:dish"}) and position it in a place with clear access to
the sky. After that, connecting the provided router is enough to browse
the Internet using different devices. Our setup is more straightforward;
the machine we use to run measurements and use the Starlink connection
is directly connected to the dish.

On a more technical note, packets sent from a local device go through
the dish, they are relayed to a nearby satellite, and they are sent to a
ground station in view; from that point onwards, packets are routed
normally through the Internet. Figure
[1.1](#fig:gs){reference-type="ref" reference="fig:gs"} shows a sample
ground station. The Ground Station needs to be in proximity for the
satellite to be able to reach it.

SpaceX is also employing Inter Satellite Links, allowing a dish not in
proximity of a Ground Station to communicate by routing packets to
different satellites and relaying them back to Earth as soon as it is
deemed convenient. This is crucial for the maritime version of the
Starlink kit[^3] since it is safe to assume oceangoing ships will often
be in such condition.

![A sample ground station, from
<https://reddit.com/r/SpaceXLounge/comments/hcf4t5/prototype_starlink_terminal_closeups_merrillan_wi/>](img/ground-station.jpeg){#fig:gs
width="0.6\\columnwidth"}

![Our Starlink dish, located in Garching, München,
DE](img/dish.jpeg){#fig:dish width="0.6\\columnwidth"}

![Basic Starlink working, from
[@izhikevich2023democratizing]](img/starlink-101.png){#fig:starlink-101
width="0.6\\columnwidth"}

SpaceX is currently the most popular LEO-based Internet Service
Provider. However, other similar projects exist, such as OneWeb[^4] and
Amazon Project Kuiper[^5]. The former is more enterprise and
government-focused, while the latter aims to be a Starlink competitor,
with the first satellite launches starting now.

The future is bright for LEO-based ISPs; however, we might soon
encounter some problems. Starlink alone has currently 4974[^6]
satellites in orbit, and Project Kuiper plans to launch 3236[^7]; these
two constellations alone account for more than 8000 satellites. This is
increasing the overall brightness of the skies, and debris proliferation
will become more and more of a concern, as reported by Barentine et al.
[@cite-key]

## Background

We will now introduce some concepts we will use later. We briefly
describe the gRPC protocol, as it is used by the dish to communicate
diagnostics and statistics to customers, before describing Two Line
Element Sets, the data format used to encode the satellite's positions.

For the measurement parts, we are using standard Unix tools, like
`ping`, `traceroute`, `iperf`, and we are using Python for scripting
purposes.

### gRPC protocol

gRPC is an RPC (Remote Procedure Call) framework from Google[^8]. It is
the dish API's protocol and is massively employed across different
fields, especially in microservices architectures.

gRPC uses protocol buffers (protobufs) both as Interface Definition
Language and as the format for message interchange; consequently, every
client needs to have a stub providing the server's accessible methods.
Typically this involves generating some `.proto` files are usually
needed, but an alternative approach called *Server Reflection* [^9] is
employed. With Server Reflection, it is feasible to dynamically query
the API to retrieve a list of the accessible methods.

Using a tool like `grpcurl`[^10], it is possible to inspect the service;
furthermore, it is easy to use the gRPC python library[^11] to develop
scripts.

### Two-line Element Sets

Two-line Element Sets (TLEs) is a widely used ASCII-based data format to
encode the position of orbital elements for a given point in time[^12].
We work with TLEs using the Skyfield Library[^13], an elegant astronomy
library for Python. Check Appendix [5](#app:sky){reference-type="ref"
reference="app:sky"} for a sample script to localize a satellite's
position given the Satellite Name. A complete list of Starlink satellite
names can be found at
<https://celestrak.org/NORAD/elements/gp.php?GROUP=starlink>. SATNAME is
a unique identifier.

Knowing a satellite's position at any given time is a very powerful
mechanisms, which allows us to restrict the subset of satellites the
dish may be connected to; it is worth noting that previously, it was
possible to call the `dish_get_context` or similar methods on the API to
retrieve such information, as reported by this Reddit user[^14].
Unfortunately, these methods now either return a `PermissionDenied`
error or are deprecated.

``` {caption="TLE for satellite STARLINK-1007" captionpos="b"}
STARLINK-1007           
1 44713U 19074A   23239.65120160  .00022666  00000+0  15354-2 0  9991
2 44713  53.0553  19.2809 0001296  68.3392 291.7735 15.06406564209327
```

## Related work

Being Starlink a novel technology the existing body of research is
somewhat limited, but papers and tools [^15] are in development, we
created some scripts to work with the dish and to perform some
measurements, you can find them in the very same repository that
contains this report[^16].

From a research perspective, different works provide more insights into
Starlink --- papers like [@pan2023measuring] focus on describing the
infrastructure Starlink uses. In contrast, Izhikevich et al.
[@izhikevich2023democratizing] illustrate a novel approach to make
measurements simpler and cheaper, and Kassem et al.[@browser-side]
focuses on running some client-side measurements with a browser
extension.

Recent work has been carried out on the hardware side, by Wouters
[@glitching] while Ramponi [@quarkslab] focuses on the firmware
perspective and offered valuable insights into the gRPC API.

## gRPC API

Our first approach to the dish is through the web UI reachable at
192.168.100.1; we discover it is getting data from a gRPC API running
directly on the dish, so we decide to spend some time documenting the
available methods we could later use to gather useful additional
information.

The server-reflected gRPC API is running on the dish; we can access it
by querying it at `192.168.100.1:9200` using `grpcurl`[^17], a sample
query to retrieve downlink throughput is:

``` {.bash language="bash"}
rc@gnolmir:~$ grpcurl -plaintext -d '{"get_status":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
{
    "apiVersion": "10",
    ... (output omitted)
}
```

It is then possible to use `jq` to extract the needed fields. We can use
the following command to describe the available services:

``` {.bash language="bash"}
rc@gnolmir:~$ grpcurl -plaintext 192.168.100.1:9200 describe
SpaceX.API.Device.Device is a service:
service Device {
    rpc Handle ( .SpaceX.API.Device.Request ) returns ( .SpaceX.API.Device.Response );
    rpc Stream ( stream .SpaceX.API.Device.ToDevice ) returns ( stream .SpaceX.API.Device.FromDevice );
}
grpc.reflection.v1alpha.ServerReflection is a service:
service ServerReflection {
    rpc ServerReflectionInfo ( stream .grpc.reflection.v1alpha.ServerReflectionRequest ) returns ( stream .grpc.reflection.v1alpha.ServerReflectionResponse );
}
```

Then, describe the single service using the following:

``` {.bash language="bash"}
rc@gnolmir:~$ grpcurl -plaintext 192.168.100.1:9200 describe SpaceX.API.Device.Request
SpaceX.API.Device.Request is a message:
message Request {
    uint64 id = 1;
    string target_id = 13;
    uint64 epoch_id = 14;
    oneof request {
    .SpaceX.API.Device.SignedData signed_request = 15;
    .SpaceX.API.Device.RebootRequest reboot = 1001;
    .SpaceX.API.Device.SpeedTestRequest speed_test = 1003;
    ... (output omitted)
    }
```

Here[^18] is a complete list of available methods as of September 2023.

To simplify scripting, we develop a simple wrapper library around the
gRPC API [^19] and a CLI tool[^20] to use the library in command line.
It should be trivial to add functionality to the library.

Unlike `sparky8512/starlink-grpc-tools`, we do not make any assumptions
about the format used to save data.

After having laid the groundwork to understand the next section, we now
move to the measurements we performed.

# Measurements and Analysis

After getting acquainted with our working environment, we run several
measurements to better understand Starlink internals.

We first try to understand the possible differences in package routing
between Starlink-based and default cabled connections. We then move to
measure the latency and bandwidth of links, and we check whether the
values for bandwidth reported from the API are the same as our machine
reports. Later, we will try to understand whether we can spot physical
layer influences on the latency of connections.

In the second part of our measurements, we explore the satellite part of
the infrastructure. First, we implement tooling to identify satellites
in line of sight of our dish and to detect patterns in satellite
appearances before implementing a side-channel measurement to detect
satellite handovers based on the approach Izhikevich's approach
[@izhikevich2023democratizing].

## Routing

In this section, we delve into the exploration of the routing behavior
in Starlink-based connections; routing refers to the process of
selecting a path across one or more networks[^21]. To investigate such
topic, we use traceroutes; `traceroute (8)` is a tool used to diagnose
problems in a network path; it is used to understand the path IP packets
are taking from one computer (source IP address) to another (destination
IP address).

One of the first experiments we perform is running traceroutes to
several different geographically sparse targets; we retrieve a list of
those from major cloud vendors,[^22], [^23]. We are both using the
`traceroute (8)` standard UNIX tool and a custom python script[^24] to
run traceroutes and save data to CSV files.

We carefully select our target destinations from major cloud vendors.
The reason behind this selection is that these cloud vendors publish
their IP ranges, and their host locations are known. While the precise
location of the final target in complex networks remains challenging to
assess, the last hop in a traceroute often provides a reasonably
accurate approximation. It's worth noting that in private networks, the
hosts often do not respond to ICMP pings, further obscuring the packet's
route.

We run the traceroutes using ICMP, UDP, and TCP protocols using both the
Starlink and the default network interface over several days, and we
save the results to CSV files. Subsequently, we use NetworkX, a Python
package for the creation, manipulation, and study of the structure,
dynamics, and functions of complex networks[^25]. to visualize whether
we can spot some differences in the graphs we create. The following
Figures are some of the representations for traceroutes to certain
specific hosts. While running traceroutes, it is common to retrieve
information for the first 30 hops; however, we decided to limit
ourselves to the first seven hops because we do not receive answers for
further hops.

![Visualizing traceroutes to 4 different hosts from AWS using ICMP, the
left Figure refers to Starlink traceroutes; the right one is the cabled
network interface.](img/tr_aws_icmp.png){#fig:tr_aws_icmp
width="0.6\\columnwidth"}

![Visualizing traceroutes to 4 different hosts from AWS using UDP, the
left Figure refers to Starlink traceroutes; the right is the cabled
network interface.](img/tr_aws_udp.png){#fig:tr_aws_udp
width="0.6\\columnwidth"}

![Visualizing traceroutes to 4 different hosts from AWS using TCP, the
left Figure refers to Starlink traceroutes; the right is the cabled
network interface.](img/tr_aws_tcp.png){#fig:tr_aws_tcp
width="0.6\\columnwidth"}

![Visualizing traceroutes to 4 different hosts from Azure using ICMP,
the left Figure refers to Starlink traceroutes, the right one is the
default network interface.](img/tr_azure_icmp.png){#fig:tr_azure_icmp
width="0.6\\columnwidth"}

Upon analyzing the traceroute data, it is evident that the routing
within the Starlink network exhibits a notably higher degree of
complexity compared to the cabled ISP network traceroutes. While the
default traceroutes show data following relatively straightforward paths
in four different main directions, the Starlink traceroutes display a
more intricate and convoluted routing pattern. Several factors could
contribute to this complexity, including diverse routing decisions and
the possibility of Inter Satellite Routing within the Starlink
constellation.

We are only reporting traceroutes to AWS using the three most common
methods and a traceroute to Azure; more data to visualize can be found
in the accompanying repository[^26].

We do not find any significant differences comparing traceroutes over
different days; we see hops in the same Autonomous Systems; the only
difference we are able to observe is that we reach different hosts
inside AS14593, the Autonomous System SpaceX operates[^27].

The following is a table of hosts reached together and a count of how
many times we reached the target.

              host   count
  ---------------- -------
    206.224.65.204     595
    206.224.65.200     595
    206.224.65.208     549
    206.224.65.182     444
    206.224.65.196     440
    206.224.65.188     360
    206.224.65.129     358
    206.224.65.178     274
    206.224.65.180     235
    206.224.65.184     189
    206.224.65.186     159
    206.224.65.190     151

  : Targets reached inside AS14593 together with the count

We also see some different prefixes in later traceroutes; AS14593
advertises many[^28].

## Latency Analysis

The gRPC API exposes a `get_status` method containing a
`pop_ping_latency_ms` field, so we decide to measure the stability of
latency to the Point of Presence (PoP) -- an artificial demarcation
point or network interface point between communicating entities. A
common example is an ISP point of presence, the local access point that
allows users to connect to the Internet with their Internet service
provider (ISP)[^29].

We know that in AS14593, there are several geographically distributed
hosts containing \"pop\" in their hostname, such as
`customer.dnvrcox1.pop.starlinkisp.net`, the naming scheme suggests the
position of the PoP we are analyzing, in the previous example it is
located in Denver, Colorado. Here[^30] is a brief list of different PoPs
retrieved using censys[^31].

Latency, defined as the time it takes for data to pass from one point on
a network to another[^32], to the PoP is pretty stable, as SpaceX
reports it fluctuates around 35 milliseconds, as we can verify from
Figure [2.5](#fig:vis-latency){reference-type="ref"
reference="fig:vis-latency"}. We are not able to observe any patterns in
latency fluctuation.

![Visualizing latency to the Point of
Presence.](img/latency.png){#fig:vis-latency width="1\\columnwidth"}

## Bandwidth analysis

During our investigations, we analyze bandwidth for two reasons: first,
we want to check whether the data from the API was correct, and then we
want to see whether we can detect any patterns in bandwidth drops.

The first experiment we set up is the following: We start downloading
five Debian ISOs from different mirrors (to neutralize the effect of the
single upload speed of a mirror). While downloading the files, we are
also running a script to extract downlink throughput from the dish and
measuring it simply by getting data from in order to compare the data
reported from the API and the actual bandwidth our machine reports.

Figure [2.6](#fig:vis-bw-15sec){reference-type="ref"
reference="fig:vis-bw-15sec"} shows our results, `bandwidth_bps` is the
data we obtain from , while `downlink_throughput_bps` is the data
reported from the gRPC API. As we can see, the two values are very
similar; this suggests that the dish reports bandwidth correctly.

From [@llc-application], we know the dish seeks better connections, as
satellites move constantly, every 15 seconds. We plot vertical lines
every 15 seconds and shift them to detect whether the bandwidth drops
were happening in 15-second intervals.

![Bandwidth visualization, with vertical red lines every 15
seconds.](img/bw-15seconds.png){#fig:vis-bw-15sec
width="1.0\\columnwidth"}

We repeat the experiments by shifting the red vertical lines and
changing the intervals for collected data, and in the majority of cases,
we see that whenever we draw a vertical red line, we have some drop in
the immediate milliseconds before or after; however, drops also happen
in different intervals. Initially We thought these drops might be
related to satellite handovers, so we investigated further; check
Section [2.7](#sec:sat-hand-drop){reference-type="ref"
reference="sec:sat-hand-drop"}, where we investigate the correlation
between satellite handovers (retrieved using a side-channel) and drops
in bandwidth.

## Physical layer influences on latency

After measuring latency and bandwidth and noticing some drops in
semi-regular intervals, we decided to investigate whether the physical
layer has any influences on latency in some way; our intuition is that
if this is the case, we can approximately detect whether a certain
amount of data is needed before a packet is sent; this means in the
best-case scenario we send the packet we want to reach the Internet
exactly, it fills exactly the size window and it is sent immediately,
worst case scenario we sent the packet when the previous packet was just
sent and we need to wait to fill the window before sending the packet.
Of course, this operation introduces some performance drawbacks in the
worst-case scenario, as the dish might have to delay transmission to
wait for more data.

To verify this hypothesis, we try to send some payload with iPerf[^33]
on the network interface used by Starlink. We send payloads of
increasing sizes (10k, 20k, 50k, 100k, 1M, 10M) and measure the RTT; the
following is a visualization, as we can notice that sending some traffic
does not have an impact.

![Latency variation while sending traffic on the uplink using
iPerf](img/latency_iperf.png){width="0.6\\columnwidth"}

We conclude no such mechanism is enabled on the device, it might be
possible other smarter and better technologies are employed and they
operate at the ideal point and thus are hard to detect.

## Visible Satellites

One of the first measurements we perform with satellites is to retrieve
the subset of satellites the dish might be connected to.

It is up to us to define what \"visible\" means; in our evaluations, we
decide that, knowing the satellites orbit around Earth at around 550
kilometers, it is reasonable to assume a satellite is visible when it is
above the horizon and it is (point to point) not further away than 800
kilometers. The ground truth might be different, but this approximation
allows us to formulate and hypothesis around satellites positions.

The first measurement we set up is the following: every 15 seconds, we
run a script that retrieves all the visible satellites and stores them
in a SQLite database. If we see the same satellite in the iteration
before we update the `timestamp` otherwise, we create a new row in the
database. We use a `relative_ts` (relative timestamp) to enumerate every
measurement (a probe every 15 seconds). To measure visible satellites,
we are running the following script:
`python3 visible-satellites.py -lat 48.2489 -lon 11.6532 -el 0 -d 800`,
where `lat` and `lon` are Garching's coordinates, we are not interested
in using an elevation. The script can be found in the repository
containing this report.

After collecting data for several hours, we plot satellite appearances
to check whether their appearance is following some pattern; Figure
[2.7](#fig:vis-sat-pat){reference-type="ref"
reference="fig:vis-sat-pat"} reveals this is the case; we are able to
observe the same satellites every 12 hours roughly. For some satellites,
we notice some artifacts that might induce to think there is a change in
the pattern, but this is not true; the interval between the appearances
is the same as in the other cases; we are uncertain about the reasons we
are seeing this phenomenon.

![Visualizing patterns in satellite appearances, we roughly see the same
satellite every 12
hours.](img/visualizing-how-long-satellites-are-visible-for.png){#fig:vis-sat-pat
width="1.0\\columnwidth"}

## Detecting Satellite Handovers

Unfortunately, as mentioned earlier, it is impossible to know from the
gRPC API which satellite the dish is connected to.

The Starlink gRPC API, however, exposes a `dish_get_obstruction_map`
method. Following the approach described in Izhikevich's paper
[@izhikevich2023democratizing], we use the information gathered from
polling the endpoint each second to extract the current obstruction map
and visualize satellite handovers. This works because the dish adds a
dot (setting a value to 1) in a 123\*123 matrix whenever it sees a
satellite in that position.

The matrix is cleared whenever the dish is rebooted by setting every
entry to -1; whenever a satellite is detected, the entry is set to 1.

By polling the endpoint frequently enough, we can observe satellite
traces, and by comparing values in the matrices we obtain, we can detect
whether a satellite handover was performed.

Let us assume the following matrices are retrieved at $t_x$ and
$t_{x+1}$, respectively. In the first matrix, we have ones in $(0,2)$
and $(1,3)$; in the second one, we have ones in $(0,2)$, $(1,3)$,
$(2,4)$. This means the new satellite we saw at $t_{x+1}$ is on the same
path as the satellites before. Thus, NO handover was performed.

$\begin{bmatrix}
-1 & -1 & \color{red}1 &           -1 & -1 \\
-1 & -1 &           -1 & \color{red}1 & -1 \\
-1 & -1 &           -1 &           -1 & -1 \\
-1 & -1 &           -1 &           -1 & -1 \\
-1 & -1 &           -1 &           -1 & -1 \\ 
\end{bmatrix}
+
\begin{bmatrix}
-1 & -1 & \color{red}1 &           -1 &           -1 \\
-1 & -1 &           -1 & \color{red}1 &           -1 \\
-1 & -1 &           -1 &           -1 & \color{red}1 \\
-1 & -1 &           -1 &           -1 &           -1 \\
-1 & -1 &           -1 &           -1 &           -1 \\
\end{bmatrix}
=
\begin{bmatrix}
-2 & -2 & 2 &  -2 &           -2 \\
-2 & -2 & -2 &  2 &           -2 \\
-2 & -2 & -2 & -2 & \color{red}0 \\
-2 & -2 & -2 & -2 &            -2 \\
-2 & -2 & -2 & -2 &            -2 \\
\end{bmatrix}$

In this different case, the new satellite we see at $t_{x+1}$ is in a
different location, so a handover must have been performed.

$\begin{bmatrix}
-1 & -1 & \color{red}1 &           -1 & -1 \\
-1 & -1 &           -1 & \color{red}1 & -1 \\
-1 & -1 &           -1 &           -1 & -1 \\
-1 & -1 &           -1 &           -1 & -1 \\
-1 & -1 &           -1 &           -1 & -1 \\
\end{bmatrix}
+
\begin{bmatrix}
-1 & -1 & \color{red}1 &           -1 & -1 \\
-1 & -1 &           -1 & \color{red}1 & -1 \\
-1 & -1 &           -1 &           -1 & -1 \\
-1 & -1 &           -1 &           -1 & -1 \\
1 & -1 &            -1 &           -1 & -1 \\
\end{bmatrix}
=
\begin{bmatrix}
          -2 & -2 & 2 & -2 & -2 \\
          -2 & -2 & -2 & 2 & -2 \\
          -2 & -2 & -2 & -2 & -2 \\
          -2 & -2 & -2 & -2 & -2 \\
\color{red}0 & -2 & -2 & -2 & -2 \\
\end{bmatrix}$

We can observe it is pretty easy to detect whether a handover was
performed; it is sufficient to sum the two matrices and check whether
the $0$ value (there was -1 before, and we currently have 1) is near an
entry whose value is $2$ (at $t_{x}$ value was 1, and at $t_{x+1}$ value
is $1$).

First, we must write a script to extract obstruction maps from the dish.
To achieve this goal, we can use the `nine981.get_obstruction_map` [^34]
function, which returns a JSON response similar to this:

``` {caption="data from the \\texttt{dish\\_get\\_obstruction\\_map} function" captionpos="b"}

{'apiVersion': '9',
 'dishGetObstructionMap': {'minElevationDeg': 10.0,
                           'numCols': 123,
                           'numRows': 123,
                           'snr': [-1.0,
                                   -1.0,
                                   -1.0,
                                   1.0,
                                   1.0,
                                   -1.0,
                                   -1.0,
                ...,
                                   1.0,
                                   1.0,
                                   1.0,
                                   -1.0,\label{sec:sat-hand-drop}

                                   -1.0,
                                   -1.0,
                                   -1.0]}}  
```

We can now extract the values in `map["dishGetObstructionMap"]["snr"]`
and reshape the array in a $123\times123$ with
`np.array(map).reshape(123, 123)`. This allows to visualize the
obstruction map at any given moment; it is a matter of loading the JSON
file we want to visualize and plot it with matplotlib [@Hunter:2007],
code can be found in Listing
[\[listing-obs\]](#listing-obs){reference-type="ref"
reference="listing-obs"} and the visualization is Figure
[2.8](#fig:vis-single-map){reference-type="ref"
reference="fig:vis-single-map"}.

``` {#listing-obs .python language="python" caption="visualizing a single obstruction map" captionpos="b" label="listing-obs"}
import json
import numpy as np
import matplotlib.pyplot as plt

f = "1692089163.json"
map = json.load(open(f))
map = map["dishGetObstructionMap"]["snr"]
map = np.array(map).reshape(123, 123)
plt.imshow(map)
plt.show()
```

![Visualizing a single obstruction map, satellite traces are clearly
visible.](img/single_map.png){#fig:vis-single-map
width="0.5\\columnwidth"}

Following this approach, we can create a simple script to retrieve maps
each second and save them locally; later, we can export images and
create a video to better visualize the phenomenon, we have uploaded a
sample video at <https://www.youtube.com/watch?v=PjfMPr20suw>.

## Correlating Handovers and Drops in Bandwidth {#sec:sat-hand-drop}

We create a simple script to algorithmically detect handovers; we can
use the function `common.detect_handovers`[^35] to detect whether a
handover was performed between two subsequent snapshots; getting all the
handovers is simply a matter of iterating for every JSON file we saved
and running the function on each pair.

We now correlate satellite handovers (the vertical dashed lines) with
the bandwidth measurements we obtained before; we assume we might have
bandwidth drops during handovers.

![Trying to correlate satellite handovers (red vertical lines) with
bandwidth
measurements.](img/correlation_handovers_bw.png){#fig:vis-correlation-handovers
width="1\\columnwidth"}

As we can verify from Figure
[2.9](#fig:vis-correlation-handovers){reference-type="ref"
reference="fig:vis-correlation-handovers"}, handovers do not seem to
impact bandwidth drops. This suggests the dish is employing a
sophisticated technology to perform satellite handovers without leading
to a performance loss, further investigation might be needed to better
understand what is enabling smooth transitions between satellites.

The measurements chapter is, for the moment, concluded; we now move to
wrap up our work.

# Final Remarks and Future Work

Concluding our experiments, we highlight several key insights. First,
the latency to the Point of Presence remains remarkably stable and low
enough even for network-intensive applications, such as online video
gaming. In practice, the average customer, provided they have clear sky
access, is usually more than satisfied with Starlink's performances.
Bandwidth is sustained consistently, even in the presence of satellite
handovers, which do not appear to impact it significantly.

Typically, a Starlink dish maintains contact with approximately eight
satellites at any given moment, making autonomous decisions internally
about which satellite to connect to. It is worth noting that this
satellite count may vary following new launches.

Unfortunately, obtaining deeper insights into the inner workings of the
Autonomous System operated by SpaceX is very hard. Hosts within this
system tend not to respond to standard ping requests, and traceroute
data does not always indicate the path packets take. Another
well-protected link in the chain is the dish itself; many of the methods
available are protected and not accessible to the end-user or are
deprecated. The dish runs an SSH server, but it is impossible to connect
to it as the manufacturer key pair is needed.

Notably, as of 6 October 2023, Project Kuiper has initiated its
satellite launch efforts, thereby advancing its satellite constellation.
By 16 October, the first two Project Kuiper satellites had been fully
activated, efficiently generating power and establishing communication
with the mission operations center.

Future research endeavors may include running our measurements over a
more extended period. Monitoring changes in latency and observing
potential alterations in traceroutes could provide valuable insights,
particularly after the launch of additional satellites. Given the
presence of multiple operators, unusual routing decisions may manifest
in the network's path over time.

Moreover, the methodologies applied in our measurements on Starlink's
dish may be adapted for use with Project Kuiper's dishes as soon as they
are commercialized. While specifics about Project Kuiper's dish remain
undisclosed, it is reasonable to expect it to offer a similar API for
dish data access.

Additionally, exploring the implementation of an IPv6-compatible router
and external access to the dish may facilitate the execution of diverse
measurements, as proposed by Izhikevich et al.
[@izhikevich2023democratizing].

Another interesting topic of research are the recently added Inter
Satellite Links (ISLs). Detecting whether packets are relayed between
satellites can be accomplished by examining the initial hop after the
Starlink Autonomous System. Using ISL routing might make it cheaper for
SpaceX; it is reasonable to assume their operators might want to use
their technology to do some internal routing to later exit the AS, where
they have favorable agreements with other service providers.

# Appendix

``` {.python language="python" caption="the \\texttt{calculate\\_visible\\_satellites} function" captionpos="b"}
def calculate_visible_satellites(
    observer_latitude, observer_longitude, observer_elevation, distance_km
):
    stations_url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=starlink&FORMAT=tle"
    satellites = load.tle_file(stations_url)
    observer = Topos(observer_latitude, observer_longitude, observer_elevation)
    ts = load.timescale()
    t = ts.now()

    # Calculate satellite positions
    positions = []
    for sat in satellites:
        satellite = sat
        position = (satellite - observer).at(t)
        positions.append((sat, position))

    # Filter visible satellites
    visible_satellites = []
    for sat, position in positions:
        alt, az, distance = position.altaz()
        # Satellite is above the horizon
        if alt.degrees > 0 and distance.km < distance_km:
            visible_satellites.append((sat, alt, az))

    return visible_satellites
```

# Skyfield Library {#app:sky}

``` {.python language="python" caption="retrieving a Satellite's position using the Satname" captionpos="b"}

from skyfield.api import load, wgs84

stations_url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=starlink&FORMAT=tle"
satellites = load.tle_file(stations_url)
print("Loaded", len(satellites), "satellites")
by_name = {sat.name: sat for sat in satellites}
satellite = by_name["STARLINK-1007"]

# year, month, day, hour, minute, second
ts = load.timescale()
t = ts.now()
a = satellite.at(t)
lat, lon = wgs84.latlon_of(a)
print("Latitude:", lat)
print("Longitude:", lon)
```

[^1]: <https://starlink.com>

[^2]: <https://spacex.com>

[^3]: <https://starlink.com/business/maritime>

[^4]: <https://oneweb.net>

[^5]: <https://aboutamazon.com/what-we-do/devices-services/project-kuiper>

[^6]: [https://celestrak.org/NORAD/elements/gp.php?GROUP=starlink &FORMAT=tle](https://celestrak.org/NORAD/elements/gp.php?GROUP=starlink &FORMAT=tle){.uri}

[^7]: <https://www.aboutamazon.com/what-we-do/devices-services/project-kuiper>

[^8]: <https://grpc.io>

[^9]: <https://github.com/grpc/grpc/blob/master/doc/server-reflection.md>

[^10]: <https://github.com/fullstorydev/grpcurl>

[^11]: <https://pypi.org/project/grpc/>

[^12]: <https://en.wikipedia.org/wiki/Two-line_element_set>

[^13]: <https://rhodesmill.org/skyfield/>

[^14]: <https://reddit.com/r/Starlink/comments/p84o5i/comment/h9o1elp/>

[^15]: <https://github.com/danopstech/starlink_exporter>,<https://github.com/sparky8512/starlink-grpc-tools>

[^16]: <https://gitlab.lrz.de/netintum/teaching/tumi8-theses/idp-castellotti>

[^17]: <https://github.com/fullstorydev/grpcurl>

[^18]: <https://gist.github.com/rcastellotti/e20630366dfeaeada6cc2680f562f6ac>

[^19]: <https://gitlab.lrz.de/netintum/teaching/tumi8-theses/idp-castellotti/-/blob/main/nine981.py>

[^20]: <https://gitlab.lrz.de/netintum/teaching/tumi8-theses/idp-castellotti/-/blob/main/s.py>

[^21]: <https://www.cloudflare.com/learning/network-layer/what-is-routing/>

[^22]: [ https://gstatic.com/ipranges/cloud.json]( https://gstatic.com/ipranges/cloud.json){.uri},
    <https://ip-ranges.amazonaws.com/ip-ranges.json>,
    <https://microsoft.com/en-us/download/details.aspx?id=53601>

[^23]: [https://docs.oracle.com/en-us/iaas/tools/public_ip_ranges.json ](https://docs.oracle.com/en-us/iaas/tools/public_ip_ranges.json ){.uri}

[^24]: <https://gitlab.lrz.de/netintum/teaching/tumi8-theses/idp-castellotti/-/blob/main/cloud-traceroutes.py>

[^25]: <https://networkx.org/>

[^26]: <https://gitlab.lrz.de/netintum/teaching/tumi8-theses/idp-castellotti-data>

[^27]: <https://bgp.he.net/AS14593>

[^28]: <https://bgp.he.net/AS14593#_prefixes>

[^29]: <https://en.wikipedia.org/wiki/Point_of_presence>,
    <https://networkencyclopedia.com/point-of-presence-pop/>

[^30]: <https://gitlab.lrz.de/netintum/teaching/tumi8-theses/idp-castellotti-data/-/blob/main/pops.json>

[^31]: <https://search.censys.io/>

[^32]: <https://www.cloudflare.com/learning/performance/glossary/what-is-latency/>

[^33]: <https://iperf.fr/>

[^34]: <https://gitlab.lrz.de/netintum/teaching/tumi8-theses/idp-castellotti/-/blame/main/nine981.py#L26>

[^35]: <https://gitlab.lrz.de/netintum/teaching/tumi8-theses/idp-castellotti/-/blob/main/common.py?ref_type=heads#L263>
