package py4j.examples;

import py4j.GatewayServer;


public class NexusEntryPoint {

	public NexusEntryPoint() {
	}

	public String test() {
		return "Still good";
	}

	public static void main(String[] args) {
		GatewayServer gatewayServer = new GatewayServer(new NexusEntryPoint());
		gatewayServer.start();
		System.out.println("Gateway Server Started");
	}
}
