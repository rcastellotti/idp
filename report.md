# Visualizing satellite handovers 

The Starlink gRPC api exposes a `dish_get_obstruction_map` method, following the approach described in CITE_LEO_PAPER we can use the information we gather from polling this method each second to detect and visualize satellite handovers. In the following paragraphs we describe 