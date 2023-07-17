# IDP Castellotti

## sample usage for `common.traceroute`
!! make sure to configure the correct interface!!

```python
import socket
from common import traceroute
from scapy.all import *
# conf.route.add(net="0.0.0.0/0", gw="192.168.1.1") # interface config in our case
hostname = "garr.it"

hops = traceroute(hostname, verbose=0)
for i, hop in enumerate(hops):
    print(f"{i} = {hop} -> {socket.getnameinfo((hop, 0), 0)[0]}")

hops = traceroute(hostname, l4=UDP(sport=RandShort(), dport=53), verbose=0)
for i, hop in enumerate(hops):
    print(f"{i} = {hop} -> {socket.getnameinfo((hop, 0), 0)[0]}")

    hops = traceroute(hostname, l4=ICMP(), verbose=0)
    for i, hop in enumerate(hops):
        print(f"{i} = {hop} -> {socket.getnameinfo((hop, 0), 0)[0]}")
```


## `main.ipynb`

A simple notebook to test stuff implemented in other files


## `pop_ping_latency.py`
This script can be used to extract pop ping latency from the dish, it is meant to be used while creating some traffic with iperf, to do so: start iperf in server mode on an host with `iper3 -s` 
and send some data with `iperf3 -c <YOUR_IP> -u -b  <YOUR_BW> -t  300`, make sure to set a route for your ip to send traffic trhough the right interface, in our case `ip route add 138.246.253.20 via 192.168.1.1`. Additionally here is a script I used to run iperf with different bandwidths:
```bash
#!/bin/bash
set -xe

bandwidths=("10k" "20k" "50k" "100k" "1M" "10M")
server_ip="138.246.253.20"
duration=300

for bandwidth in "${bandwidths[@]}"; do
  iperf3 -c "$server_ip" -u -b "$bandwidth" -t "$duration"
done
```


## `visible-satellites.py`

Get all visible satellites, where "visible" is defined as above the horizon and within the distance passed as parameter, following are garching's coordinates

```bash
python3 visible_satellites.py -lat 48.2489 -lon 11.6532 -el 0 -d 800 
```



Starlink gRPC api
===

####  `grpcurl -plaintext 192.168.100.1:9200 describe`

```bash
rc@gnolmir ~> grpcurl -plaintext 192.168.100.1:9200 describe
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
#### `grpcurl -plaintext 192.168.100.1:9200 describe SpaceX.API.Device.Request`

```bash
rc@gnolmir ~> grpcurl -plaintext 192.168.100.1:9200 describe SpaceX.API.Device.Request
SpaceX.API.Device.Request is a message:
message Request {
  uint64 id = 1;
  string target_id = 13;
  uint64 epoch_id = 14;
  oneof request {
    .SpaceX.API.Device.SignedData signed_request = 15;
    .SpaceX.API.Device.RebootRequest reboot = 1001;
    .SpaceX.API.Device.SpeedTestRequest speed_test = 1003;
    .SpaceX.API.Device.GetStatusRequest get_status = 1004;
    .SpaceX.API.Device.AuthenticateRequest authenticate = 1005;
    .SpaceX.API.Device.GetNextIdRequest get_next_id = 1006;
    .SpaceX.API.Device.GetHistoryRequest get_history = 1007;
    .SpaceX.API.Device.GetDeviceInfoRequest get_device_info = 1008;
    .SpaceX.API.Device.GetPingRequest get_ping = 1009;
    .SpaceX.API.Device.SetTrustedKeysRequest set_trusted_keys = 1010;
    .SpaceX.API.Device.FactoryResetRequest factory_reset = 1011;
    .SpaceX.API.Device.GetLogRequest get_log = 1012;
    .SpaceX.API.Device.SetSkuRequest set_sku = 1013;
    .SpaceX.API.Device.UpdateRequest update = 1014;
    .SpaceX.API.Device.GetNetworkInterfacesRequest get_network_interfaces = 1015;
    .SpaceX.API.Device.PingHostRequest ping_host = 1016;
    .SpaceX.API.Device.GetLocationRequest get_location = 1017;
    .SpaceX.API.Device.GetHeapDumpRequest get_heap_dump = 1019;
    .SpaceX.API.Device.RestartControlRequest restart_control = 1020;
    .SpaceX.API.Device.FuseRequest fuse = 1021;
    .SpaceX.API.Device.GetPersistentStatsRequest get_persistent_stats = 1022;
    .SpaceX.API.Device.GetConnectionsRequest get_connections = 1023;
    .SpaceX.API.Device.StartSpeedtestRequest start_speedtest = 1027;
    .SpaceX.API.Device.GetSpeedtestStatusRequest get_speedtest_status = 1028;
    .SpaceX.API.Device.ReportClientSpeedtestRequest report_client_speedtest = 1029;
    .SpaceX.API.Device.InitiateRemoteSshRequest initiate_remote_ssh = 1030 [deprecated = true];
    .SpaceX.API.Device.SelfTestRequest self_test = 1031;
    .SpaceX.API.Device.SetTestModeRequest set_test_mode = 1032;
    .SpaceX.API.Device.SoftwareUpdateRequest software_update = 1033;
    .SpaceX.API.Device.EnableDebugTelemRequest enable_debug_telem = 1034;
    .SpaceX.API.Device.DishStowRequest dish_stow = 2002;
    .SpaceX.API.Device.DishGetContextRequest dish_get_context = 2003;
    .SpaceX.API.Device.DishSetEmcRequest dish_set_emc = 2007;
    .SpaceX.API.Device.DishGetObstructionMapRequest dish_get_obstruction_map = 2008;
    .SpaceX.API.Device.DishGetEmcRequest dish_get_emc = 2009;
    .SpaceX.API.Device.DishSetConfigRequest dish_set_config = 2010;
    .SpaceX.API.Device.DishGetConfigRequest dish_get_config = 2011;
    .SpaceX.API.Device.StartDishSelfTestRequest start_dish_self_test = 2012;
    .SpaceX.API.Device.DishPowerSaveRequest dish_power_save = 2013;
    .SpaceX.API.Device.DishInhibitGpsRequest dish_inhibit_gps = 2014;
    .SpaceX.API.Device.WifiSetConfigRequest wifi_set_config = 3001;
    .SpaceX.API.Device.WifiGetClientsRequest wifi_get_clients = 3002;
    .SpaceX.API.Device.WifiSetupRequest wifi_setup = 3003;
    .SpaceX.API.Device.WifiGetPingMetricsRequest wifi_get_ping_metrics = 3007;
    .SpaceX.API.Device.WifiGetDiagnosticsRequest wifi_get_diagnostics = 3008;
    .SpaceX.API.Device.WifiGetConfigRequest wifi_get_config = 3009;
    .SpaceX.API.Device.WifiSetMeshDeviceTrustRequest wifi_set_mesh_device_trust = 3012;
    .SpaceX.API.Device.WifiSetMeshConfigRequest wifi_set_mesh_config = 3013 [deprecated = true];
    .SpaceX.API.Device.WifiGetClientHistoryRequest wifi_get_client_history = 3015;
    .SpaceX.API.Device.WifiSetAviationConformedRequest wifi_set_aviation_conformed = 3016;
    .SpaceX.API.Device.WifiSetClientGivenNameRequest wifi_set_client_given_name = 3017;
    .SpaceX.API.Device.WifiSelfTestRequest wifi_self_test = 3018;
    .SpaceX.API.Device.TransceiverIFLoopbackTestRequest transceiver_if_loopback_test = 4001;
    .SpaceX.API.Device.TransceiverGetStatusRequest transceiver_get_status = 4003;
    .SpaceX.API.Device.TransceiverGetTelemetryRequest transceiver_get_telemetry = 4004;
  }
  reserved 1018, 1025, 1026, 3011, 3014;
}
```

#### `grpcurl -plaintext 192.168.100.1:9200 describe SpaceX.API.Device.Response`

```bash
rc@gnolmir ~> grpcurl -plaintext 192.168.100.1:9200 describe SpaceX.API.Device.Response
SpaceX.API.Device.Response is a message:
message Response {
  uint64 id = 1;
  .SpaceX.API.Status.Status status = 2;
  uint64 api_version = 3;
  oneof response {
    .SpaceX.API.Device.RebootResponse reboot = 1001;
    .SpaceX.API.Device.SpeedTestResponse speed_test = 1003;
    .SpaceX.API.Device.GetDeviceInfoResponse get_device_info = 1004;
    .SpaceX.API.Device.GetNextIdResponse get_next_id = 1006;
    .SpaceX.API.Device.GetPingResponse get_ping = 1009;
    .SpaceX.API.Device.SetTrustedKeysResponse set_trusted_keys = 1010;
    .SpaceX.API.Device.FactoryResetResponse factory_reset = 1011;
    .SpaceX.API.Device.GetLogResponse get_log = 1012;
    .SpaceX.API.Device.SetSkuResponse set_sku = 1013;
    .SpaceX.API.Device.UpdateResponse update = 1014;
    .SpaceX.API.Device.GetNetworkInterfacesResponse get_network_interfaces = 1015;
    .SpaceX.API.Device.PingHostResponse ping_host = 1016;
    .SpaceX.API.Device.GetLocationResponse get_location = 1017;
    .SpaceX.API.Device.GetHeapDumpResponse get_heap_dump = 1019;
    .SpaceX.API.Device.RestartControlResponse restart_control = 1020;
    .SpaceX.API.Device.FuseResponse fuse = 1021;
    .SpaceX.API.Device.GetConnectionsResponse get_connections = 1023;
    .SpaceX.API.Device.StartSpeedtestResponse start_speedtest = 1027;
    .SpaceX.API.Device.GetSpeedtestStatusResponse get_speedtest_status = 1028;
    .SpaceX.API.Device.ReportClientSpeedtestResponse report_client_speedtest = 1029;
    .SpaceX.API.Device.InitiateRemoteSshResponse initiate_remote_ssh = 1030 [deprecated = true];
    .SpaceX.API.Device.SelfTestResponse self_test = 1031;
    .SpaceX.API.Device.SetTestModeResponse set_test_mode = 1032;
    .SpaceX.API.Device.SoftwareUpdateResponse software_update = 1033;
    .SpaceX.API.Device.EnableDebugTelemResponse enable_debug_telem = 1034;
    .SpaceX.API.Device.DishStowResponse dish_stow = 2002;
    .SpaceX.API.Device.DishGetContextResponse dish_get_context = 2003;
    .SpaceX.API.Device.DishGetStatusResponse dish_get_status = 2004;
    .SpaceX.API.Device.DishAuthenticateResponse dish_authenticate = 2005;
    .SpaceX.API.Device.DishGetHistoryResponse dish_get_history = 2006;
    .SpaceX.API.Device.DishSetEmcResponse dish_set_emc = 2007;
    .SpaceX.API.Device.DishGetObstructionMapResponse dish_get_obstruction_map = 2008;
    .SpaceX.API.Device.DishGetEmcResponse dish_get_emc = 2009;
    .SpaceX.API.Device.DishSetConfigResponse dish_set_config = 2010;
    .SpaceX.API.Device.DishGetConfigResponse dish_get_config = 2011;
    .SpaceX.API.Device.StartDishSelfTestResponse start_dish_self_test = 2012;
    .SpaceX.API.Device.DishInhibitGpsResponse dish_inhibit_gps = 2013;
    .SpaceX.API.Device.WifiSetConfigResponse wifi_set_config = 3001;
    .SpaceX.API.Device.WifiGetClientsResponse wifi_get_clients = 3002;
    .SpaceX.API.Device.WifiSetupResponse wifi_setup = 3003;
    .SpaceX.API.Device.WifiGetStatusResponse wifi_get_status = 3004;
    .SpaceX.API.Device.WifiAuthenticateResponse wifi_authenticate = 3005;
    .SpaceX.API.Device.WifiGetHistoryResponse wifi_get_history = 3006;
    .SpaceX.API.Device.WifiGetPingMetricsResponse wifi_get_ping_metrics = 3007;
    .SpaceX.API.Device.WifiGetDiagnosticsResponse wifi_get_diagnostics = 3008;
    .SpaceX.API.Device.WifiGetConfigResponse wifi_get_config = 3009;
    .SpaceX.API.Device.WifiSetMeshDeviceTrustResponse wifi_set_mesh_device_trust = 3012;
    .SpaceX.API.Device.WifiSetMeshConfigResponse wifi_set_mesh_config = 3013 [deprecated = true];
    .SpaceX.API.Device.WifiGetClientHistoryResponse wifi_get_client_history = 3015;
    .SpaceX.API.Device.WifiSelfTestResponse wifi_self_test = 3016;
    .SpaceX.API.Device.WifiGetPersistentStatsResponse wifi_get_persistent_stats = 3022;
    .SpaceX.API.Device.TransceiverIFLoopbackTestResponse transceiver_if_loopback_test = 4001;
    .SpaceX.API.Device.TransceiverGetStatusResponse transceiver_get_status = 4003;
    .SpaceX.API.Device.TransceiverGetTelemetryResponse transceiver_get_telemetry = 4004;
  }
  reserved 1018, 1026, 2025, 3011, 3014;
}
```

#### `grpcurl -plaintext 192.168.100.1:9200 describe SpaceX.API.Device.ToDevice`
```bash
rc@gnolmir ~ [1]> grpcurl -plaintext 192.168.100.1:9200 describe SpaceX.API.Device.ToDevice
SpaceX.API.Device.ToDevice is a message:
message ToDevice {
  oneof message {
    .SpaceX.API.Device.Request request = 1;
    .SpaceX.API.Device.HealthCheck health_check = 2;
  }
}

```

#### `grpcurl -plaintext 192.168.100.1:9200 describe SpaceX.API.Device.FromDevice`
```bash
rc@gnolmir ~> grpcurl -plaintext 192.168.100.1:9200 describe SpaceX.API.Device.FromDevice
SpaceX.API.Device.FromDevice is a message:
message FromDevice {
  oneof message {
    .SpaceX.API.Device.Response response = 1;
    .SpaceX.API.Device.Event event = 2;
    .SpaceX.API.Device.HealthCheck health_check = 3;
  }
}
```



### grpcurl requests not working

```bash
rc@gnolmir:~$ grpcurl -plaintext -d '{"set_test_mode":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
ERROR:
  Code: PermissionDenied
  Message: Permission denied
  ```
```bash
rc@gnolmir:~$ grpcurl -plaintext -d '{"dish_set_config":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
ERROR:
  Code: PermissionDenied
  Message: Permission denied
  ```
```bash
rc@gnolmir:~$ grpcurl -plaintext -d '{"transceiver_if_loopback_test":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
ERROR:
  Code: Unimplemented
  Message: Unimplemented
  ```
```bash
rc@gnolmir:~$ grpcurl -plaintext -d '{"wifi_set_client_given_name":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
ERROR:
  Code: Unimplemented
  Message: Unimplemented: *device.Request_WifiSetClientGivenName
  ```
```bash
rc@gnolmir:~$ grpcurl -plaintext -d '{"wifi_set_aviation_conformed":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
ERROR:
  Code: Unimplemented
  Message: Unimplemented: *device.Request_WifiSetAviationConformed
  ```
```bash
rc@gnolmir:~$ grpcurl -plaintext -d '{"wifi_get_client_history":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
ERROR:
  Code: Unimplemented
  Message: Unimplemented: *device.Request_WifiGetClientHistory
  ```
```bash
rc@gnolmir:~$ grpcurl -plaintext -d '{"wifi_set_mesh_device_trust":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
ERROR:
  Code: Unimplemented
  Message: Unimplemented: *device.Request_WifiSetMeshDeviceTrust
  ```
```bash
rc@gnolmir:~$ grpcurl -plaintext -d '{"wifi_get_ping_metrics":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
ERROR:
  Code: Unimplemented
  Message: Unimplemented: *device.Request_WifiGetPingMetrics
  ```
```bash
rc@gnolmir:~$ grpcurl -plaintext -d '{"wifi_get_diagnostics":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
ERROR:
  Code: Unimplemented
  Message: Unimplemented: *device.Request_WifiGetDiagnostics
  ```
```bash
rc@gnolmir:~$ grpcurl -plaintext -d '{"speed_test":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
ERROR:
  Code: Unimplemented
  Message: Unimplemented: *device.Request_SpeedTest
 ```
```bash
rc@gnolmir:~$ grpcurl -plaintext -d '{"dish_set_emc":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
ERROR:
  Code: PermissionDenied
  Message: 
  ```
```bash
rc@gnolmir:~$ grpcurl -plaintext -d '{"dish_get_emc":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
ERROR:
  Code: PermissionDenied
  Message: 
  ```
```bash
rc@gnolmir:~$ grpcurl -plaintext -d '{"get_persistent_stats":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
ERROR:
  Code: Unimplemented
  Message: Unimplemented: *device.Request_GetPersistentStats
```
```bash
rc@gnolmir:~$ grpcurl -plaintext -d '{"fuse":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
ERROR:
  Code: Unimplemented
  Message: Unimplemented: *device.Request_Fuse
 ```
 ```bash
rc@gnolmir:~$ grpcurl -plaintext -d '{"get_heat_dump":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
Error invoking method "SpaceX.API.Device.Device/Handle": error getting request data: message type SpaceX.API.Device.Request has no known field named get_heat_dump
```
```bash
rc@gnolmir:~$ grpcurl -plaintext -d '{"set_sku":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
ERROR:
  Code: Unimplemented
  Message: Unimplemented: *device.Request_SetSku
 ```
```bash
rc@gnolmir:~$ grpcurl -plaintext -d '{"update":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
ERROR:
  Code: Unimplemented
  Message: Unimplemented: *device.Request_Update
```
```bash
rc@gnolmir:~$ grpcurl -plaintext -d '{"authenticate":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
ERROR:
  Code: PermissionDenied
  Message: Invalid challenge
```
```bash
rc@gnolmir:~$ grpcurl -plaintext -d '{"dish_inibit_gps":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
Error invoking method "SpaceX.API.Device.Device/Handle": error getting request data: message type SpaceX.API.Device.Request has no known field named dish_inibit_gps
```
```bash
rc@gnolmir:~$ grpcurl -plaintext -d '{"wifi_set_config":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
ERROR:
  Code: Unimplemented
  Message: Unimplemented: *device.Request_WifiSetConfig
```
```bash
rc@gnolmir:~$ grpcurl -plaintext -d '{"wifi_get_config":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
ERROR:
  Code: Unimplemented
  Message: Unimplemented: *device.Request_WifiGetConfig
```
```bash
rc@gnolmir:~$ grpcurl -plaintext -d '{"wifi_get_config":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
ERROR:
  Code: Unimplemented
  Message: Unimplemented: *device.Request_WifiGetConfig
```
```bash 
rc@gnolmir:~$ grpcurl -plaintext -d '{"get_ping":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
ERROR:
  Code: Unimplemented
  Message: Unimplemented: *device.Request_GetPing
```
```bash
rc@gnolmir:~$ grpcurl -plaintext  -d '{"restart_control":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
ERROR:
  Code: Unimplemented
  Message: Unimplemented: *device.Request_RestartControl
```
```bash
rc@gnolmir:~$ grpcurl -plaintext -d '{"get_log":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
ERROR:
  Code: Unimplemented
  Message: Unimplemented: *device.Request_GetLog
```
```bash
rc@gnolmir:~$ grpcurl -plaintext -d '{"get_network_interfaces":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
ERROR:
  Code: Unimplemented
  Message: Unimplemented: *device.Request_GetNetworkInterfaces
```
```bash
rc@gnolmir:~$ grpcurl -plaintext -d '{"ping_host":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
ERROR:
  Code: Unimplemented
  Message: Unimplemented: *device.Request_PingHost
```
```bash
rc@gnolmir:~$ grpcurl -plaintext -d '{"enable_debug_telem":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
ERROR:
  Code: Unimplemented
  Message: Unimplemented: *device.Request_EnableDebugTelem
```
```bash
rc@gnolmir:~$ grpcurl -plaintext -d '{"wifi_get_clients":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
ERROR:
  Code: Unimplemented
  Message: Unimplemented: *device.Request_WifiGetClients
```
```bash
rc@gnolmir:~$ grpcurl -plaintext -d '{"wifi_setup":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
ERROR:
  Code: Unimplemented
  Message: Unimplemented: *device.Request_WifiSetup
```
```bash
rc@gnolmir:~$ grpcurl -plaintext -d '{"transceiver_get_telemetry":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
ERROR:
  Code: Unimplemented
  Message: Unimplemented
```
```bash
rc@gnolmir:~$ grpcurl -plaintext -d '{"get_connections":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
ERROR:
  Code: Unimplemented
  Message: Unimplemented: *device.Request_GetConnections
```
```bash
rc@gnolmir:~$ grpcurl -plaintext -d '{"get_next_id":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
ERROR:
  Code: Unimplemented
  Message: Unimplemented: *device.Request_GetNextId
```
```bash  
rc@gnolmir:~$ grpcurl -plaintext -d '{"speed_test":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
ERROR:
  Code: Unimplemented
  Message: Unimplemented: *device.Request_SpeedTest
```
```bash  
rc@gnolmir:~$ grpcurl -plaintext -d '{"get_ping":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
ERROR:
  Code: Unimplemented
  Message: Unimplemented: *device.Request_GetPing
```
```bash
rc@gnolmir:~$ grpcurl -plaintext -d '{"get_network_interfaces":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
ERROR:
  Code: Unimplemented
  Message: Unimplemented: *device.Request_GetNetworkInterfaces
```

```bash
rc@gnolmir:~$ grpcurl -plaintext -d '{"transceiver_get_telemetry":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
ERROR:
  Code: Unimplemented
  Message: Unimplemented
```
```bash
rc@gnolmir:~$ grpcurl -plaintext -d '{"transceiver_get_status":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
ERROR:
  Code: Unimplemented
  Message: Unimplemented
```
```bash
rc@gnolmir:~$ grpcurl -plaintext -d '{"get_location":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
ERROR:
  Code: PermissionDenied
  Message: GetLocation requests are not enabled on this device
```
```bash
rc@gnolmir:~$ grpcurl -plaintext -d '{"dish_get_context":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
ERROR:
  Code: PermissionDenied
  Message: Permission denied
```
```bash
rc@gnolmir:~$ grpcurl -plaintext -d '{"software_update":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
ERROR:
  Code: FailedPrecondition
  Message: Software update stream not open
```


### grpcurl requests  working
```bash
rc@gnolmir:~$ grpcurl -plaintext -d '{"reboot":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
{
  "apiVersion": "8",
  "reboot": {
    
  }
}
```
```bash
rc@gnolmir:~$ grpcurl -plaintext -d '{"get_status":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
{
  "apiVersion": "8",
  "dishGetStatus": {
    "deviceInfo": {
      "id": "ut01000000-00000000-00270e41",
      "hardwareVersion": "rev3_proto2",
      "softwareVersion": "2ce8c16a-67b6-4bbd-a135-a00662a60151.uterm.release",
      "countryCode": "DE",
      "utcOffsetS": 1,
      "bootcount": 69,
      "generationNumber": "1684883829"
    },
    "deviceState": {
      "uptimeS": "628401"
    },
    "obstructionStats": {
      "validS": 628111,
      "avgProlongedObstructionIntervalS": "NaN",
      "timeObstructed": 6.3682954e-08,
      "patchesValid": 4097
    },
    "alerts": {
      
    },
    "downlinkThroughputBps": 20560.479,
    "uplinkThroughputBps": 9042.919,
    "popPingLatencyMs": 34.52381,
    "boresightAzimuthDeg": 1.6949656,
    "boresightElevationDeg": 63.424454,
    "gpsStats": {
      "gpsValid": true,
      "gpsSats": 10
    },
    "ethSpeedMbps": 1000,
    "mobilityClass": "MOBILE",
    "isSnrAboveNoiseFloor": true,
    "readyStates": {
      "cady": true,
      "scp": true,
      "l1l2": true,
      "xphy": true,
      "aap": true,
      "rf": true
    },
    "softwareUpdateState": "IDLE",
    "disablementCode": "OKAY",
    "softwareUpdateStats": {
      "softwareUpdateState": "IDLE",
      "softwareUpdateProgress": 1
    },
    "alignmentStats": {
      "tiltAngleDeg": 26.285408,
      "boresightAzimuthDeg": 1.6949656,
      "boresightElevationDeg": 63.424454,
      "attitudeEstimationState": "FILTER_CONVERGED",
      "attitudeUncertaintyDeg": 0.53231573
    },
    "initializationDurationSeconds": {
      "attitudeInitialization": 112,
      "burstDetected": 36,
      "ekfConverged": 155,
      "firstCplane": 63,
      "firstPopPing": 72,
      "gpsValid": 28,
      "initialNetworkEntry": 36,
      "networkSchedule": 68,
      "rfReady": 34,
      "stableConnection": 113
    },
    "config": {
      "powerSaveDurationMinutes": 1,
      "applySnowMeltMode": true,
      "applyLocationRequestMode": true,
      "applyLevelDishMode": true,
      "applyPowerSaveStartMinutes": true,
      "applyPowerSaveDurationMinutes": true,
      "applyPowerSaveMode": true
    }
  }
}
```

```bash
rc@gnolmir:~$ grpcurl -plaintext -d '{"start_dish_self_test":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
{
  "apiVersion": "8",
  "startDishSelfTest": {
    
  }
}
```
```bash
rc@gnolmir:~$ grpcurl -plaintext -d '{"get_history":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
{
  "apiVersion": "8",
  "dishGetHistory": {
    "current": "626676",
    "popPingDropRate": [0,0,...,0,0],
    "popPingLatencyMs": [48.333332,47.8,...,46.666668,47.47619],
    "downlinkThroughputBps": [14705.2295,24805.113,...,6928.99,9714.008],
    "uplinkThroughputBps": [17733.518,11911.823,...,9042.919,34309.406],
    "outages": [
      {
        "cause": "NO_DOWNLINK",
        "startTimestampNs": "1371246075160167224",
        "durationNs": "400011278",
        "didSwitch": true
      },
      {
        "cause": "NO_PINGS",
        "startTimestampNs": "1371283269140157964",
        "durationNs": "999988759",
        "didSwitch": true
      }
    ....
    ]
  }
}
```
```bash
rc@gnolmir:~$ grpcurl -plaintext -d '{"get_device_info":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
{
  "apiVersion": "8",
  "getDeviceInfo": {
    "deviceInfo": {
      "id": "ut01000000-00000000-00270e41",
      "hardwareVersion": "rev3_proto2",
      "softwareVersion": "2ce8c16a-67b6-4bbd-a135-a00662a60151.uterm.release",
      "countryCode": "DE",
      "utcOffsetS": 1,
      "bootcount": 69,
      "generationNumber": "1684883829"
    }
  }
}
```

```bash
rc@gnolmir:~$ grpcurl -plaintext  -d '{"dish_power_save":{"power_save_duration_minutes":1}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
{
  "status": {
    
  },
  "apiVersion": "8"
}
```
```bash
rc@gnolmir:~$ grpcurl -plaintext -d '{"dish_get_config":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
{
  "apiVersion": "8",
  "dishGetConfig": {
    "dishConfig": {
      "powerSaveDurationMinutes": 1,
      "applySnowMeltMode": true,
      "applyLocationRequestMode": true,
      "applyLevelDishMode": true,
      "applyPowerSaveStartMinutes": true,
      "applyPowerSaveDurationMinutes": true,
      "applyPowerSaveMode": true
    }
  }
}
```
```bash
rc@gnolmir:~$ grpcurl -plaintext -d '{"dish_get_obstruction_map":{}}' 192.168.100.1:9200 SpaceX.API.Device.Device/Handle
(output omitted)
```
