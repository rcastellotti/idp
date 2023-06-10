from itertools import chain
import math
import statistics
from typing import Dict, Iterable, List, Optional, Sequence, Tuple, get_type_hints
from typing_extensions import TypedDict, get_args

import grpc

try:
    from yagrc import importer

    importer.add_lazy_packages(["spacex.api.device"])
    imports_pending = True
except (ImportError, AttributeError):
    imports_pending = False

from spacex.api.device import device_pb2
from spacex.api.device import device_pb2_grpc
from spacex.api.device import dish_pb2

# Max wait time for gRPC request completion, in seconds. This is just to
# prevent hang if the connection goes dead without closing.
REQUEST_TIMEOUT = 10


def resolve_imports(channel: grpc.Channel):
    importer.resolve_lazy_imports(channel)
    global imports_pending
    imports_pending = False


class GrpcError(Exception):
    """Provides error info when something went wrong with a gRPC call."""

    def __init__(self, e, *args, **kwargs):
        # grpc.RpcError is too verbose to print in whole, but it may also be
        # a Call object, and that class has some minimally useful info.
        if isinstance(e, grpc.Call):
            msg = e.details()
        elif isinstance(e, grpc.RpcError):
            msg = "Unknown communication or service error"
        elif isinstance(e, (AttributeError, IndexError, TypeError, ValueError)):
            msg = "Protocol error"
        else:
            msg = str(e)
        super().__init__(msg, *args, **kwargs)


class ChannelContext:
    """A wrapper for reusing an open grpc Channel across calls.

    `close()` should be called on the object when it is no longer
    in use.
    """

    def __init__(self, target: Optional[str] = None) -> None:
        self.channel = None
        self.target = "192.168.100.1:9200" if target is None else target

    def get_channel(self) -> Tuple[grpc.Channel, bool]:
        reused = True
        if self.channel is None:
            self.channel = grpc.insecure_channel(self.target)
            reused = False
        return self.channel, reused

    def close(self) -> None:
        if self.channel is not None:
            self.channel.close()
        self.channel = None


def call_with_channel(
    function, *args, context: Optional[ChannelContext] = None, **kwargs
):
    """Call a function with a channel object.

    Args:
        function: Function to call with channel as first arg.
        args: Additional args to pass to function
        context (ChannelContext): Optionally provide a channel for (re)use.
            If not set, a new default channel will be used and then closed.
        kwargs: Additional keyword args to pass to function.
    """
    if context is None:
        with grpc.insecure_channel("192.168.100.1:9200") as channel:
            return function(channel, *args, **kwargs)

    while True:
        channel, reused = context.get_channel()
        try:
            return function(channel, *args, **kwargs)
        except grpc.RpcError:
            context.close()
            if not reused:
                raise


def get_status(context: Optional[ChannelContext] = None):
    """Fetch status data and return it in grpc structure format.

    Args:
        context (ChannelContext): Optionally provide a channel for reuse
            across repeated calls. If an existing channel is reused, the RPC
            call will be retried at most once, since connectivity may have
            been lost and restored in the time since it was last used.

    Raises:
        grpc.RpcError: Communication or service error.
        AttributeError, ValueError: Protocol error. Either the target is not a
            Starlink user terminal or the grpc protocol has changed in a way
            this module cannot handle.
    """

    def grpc_call(channel):
        if imports_pending:
            resolve_imports(channel)
        stub = device_pb2_grpc.DeviceStub(channel)
        response = stub.Handle(
            device_pb2.Request(get_status={}), timeout=REQUEST_TIMEOUT
        )
        return response.dish_get_status

    return call_with_channel(grpc_call, context=context)


def status_data(
    context: Optional[ChannelContext] = None,
):
    """Fetch current status data.

    Args:
        context (ChannelContext): Optionally provide a channel for reuse
            across repeated calls.

    Returns:
        A tuple with 3 dicts, mapping status data field names, obstruction
        detail field names, and alert detail field names to their respective
        values, in that order.

    Raises:
        GrpcError: Failed getting status info from the Starlink user terminal.
    """
    try:
        status = get_status(context)
    except (AttributeError, ValueError, grpc.RpcError) as e:
        raise GrpcError(e) from e

    try:
        if status.HasField("outage"):
            if status.outage.cause == dish_pb2.DishOutage.Cause.NO_SCHEDULE:
                # Special case translate this to equivalent old name
                state = "SEARCHING"
            else:
                try:
                    state = dish_pb2.DishOutage.Cause.Name(status.outage.cause)
                except ValueError:
                    # Unlikely, but possible if dish is running newer firmware
                    # than protocol data pulled via reflection
                    state = str(status.outage.cause)
        else:
            state = "CONNECTED"
    except (AttributeError, ValueError):
        state = "UNKNOWN"

    # More alerts may be added in future, so in addition to listing them
    # individually, provide a bit field based on field numbers of the
    # DishAlerts message.
    alerts = {}
    alert_bits = 0
    try:
        for field in status.alerts.DESCRIPTOR.fields:
            value = getattr(status.alerts, field.name, False)
            alerts["alert_" + field.name] = value
            if field.number < 65:
                alert_bits |= (1 if value else 0) << (field.number - 1)
    except AttributeError:
        pass

    obstruction_duration = None
    obstruction_interval = None
    obstruction_stats = getattr(status, "obstruction_stats", None)
    if obstruction_stats is not None:
        try:
            if (
                obstruction_stats.avg_prolonged_obstruction_duration_s > 0.0
                and not math.isnan(
                    obstruction_stats.avg_prolonged_obstruction_interval_s
                )
            ):
                obstruction_duration = (
                    obstruction_stats.avg_prolonged_obstruction_duration_s
                )
                obstruction_interval = (
                    obstruction_stats.avg_prolonged_obstruction_interval_s
                )
        except AttributeError:
            pass

    device_info = getattr(status, "device_info", None)
    return (
        {
            "id": getattr(device_info, "id", None),
            "hardware_version": getattr(device_info, "hardware_version", None),
            "software_version": getattr(device_info, "software_version", None),
            "state": state,
            "uptime": getattr(getattr(status, "device_state", None), "uptime_s", None),
            "snr": None,  # obsoleted in grpc service
            "seconds_to_first_nonempty_slot": getattr(
                status, "seconds_to_first_nonempty_slot", None
            ),
            "pop_ping_drop_rate": getattr(status, "pop_ping_drop_rate", None),
            "downlink_throughput_bps": getattr(status, "downlink_throughput_bps", None),
            "uplink_throughput_bps": getattr(status, "uplink_throughput_bps", None),
            "pop_ping_latency_ms": getattr(status, "pop_ping_latency_ms", None),
            "alerts": alert_bits,
            "fraction_obstructed": getattr(
                obstruction_stats, "fraction_obstructed", None
            ),
            "currently_obstructed": getattr(
                obstruction_stats, "currently_obstructed", None
            ),
            "seconds_obstructed": None,  # obsoleted in grpc service
            "obstruction_duration": obstruction_duration,
            "obstruction_interval": obstruction_interval,
            "direction_azimuth": getattr(status, "boresight_azimuth_deg", None),
            "direction_elevation": getattr(status, "boresight_elevation_deg", None),
            "is_snr_above_noise_floor": getattr(
                status, "is_snr_above_noise_floor", None
            ),
        },
        {
            "wedges_fraction_obstructed[]": [None] * 12,  # obsoleted in grpc service
            "raw_wedges_fraction_obstructed[]": [None]
            * 12,  # obsoleted in grpc service
            "valid_s": getattr(obstruction_stats, "valid_s", None),
        },
        alerts,
    )
