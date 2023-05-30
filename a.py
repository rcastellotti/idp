from starlink_grpc import status_data
pop_ping_latency_ms=status_data()[0]["pop_ping_latency_ms"]
print(pop_ping_latency_ms)