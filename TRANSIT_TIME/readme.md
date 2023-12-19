Transit time = transmission time + processing time + routing delay + propogation time

Processing time and propogation time is independent of packet length. Since in the equation it woudld cancel each other out.

Transmission time is packetlength / bandwidth
routing delay is discardedpackets / (inputrate + outputrate)

to run : 
python . community hostid filesize

for files lesser than 1gb, transmission time and routing delay is negligible and can be ignored, for faster processing. Just take rtt/2
