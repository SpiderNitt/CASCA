package udp_sample.simulations;

@license(LGPL);

import inet.networklayer.configurator.ipv4.Ipv4NetworkConfigurator;
import inet.node.inet.StandardHost;
import ned.DatarateChannel;

network UdpAppExample
{
    types:
        channel C extends DatarateChannel
        {
            datarate = 1Mbps;
            delay = 0.1us;
        }
    submodules:
        configurator: Ipv4NetworkConfigurator {
            parameters:
                @display("p=100,100;is=s");
        }
        client: StandardHost {
            parameters:
                @display("p=250,100;i=device/pc3");
        }
        server: StandardHost {
            parameters:
                @display("p=400,100;i=device/pc2");
        }
    connections allowunconnected:
        client.pppg++ <--> C <--> server.pppg++;
}