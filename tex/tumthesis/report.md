# Visualizing satellite handovers 

The Starlink gRPC api exposes a `dish_get_obstruction_map` method, following the approach described in CITE_LEO_PAPER we can use the information we gather from polling this method each second to extract the current obstruction map and visualize satellite handovers. The reason this works is the dish is adding a dot (setting a value to 1) in a 123*123 matrix whenever it sees a satellite in that position, whenever the dish is rebooted (using i.e `nine981.reboot`) the matrix is cleared by setting every entry to -1, whenever a satellite is detected entry is set. If we poll the endpoint frequently enough we can observe satellites traces.



First of all we need to write a script to extract obstruction maps from the dish, to achieve this goal we can use the `nine981.get_obstruction_map` function, this returns a    



## convert a single 