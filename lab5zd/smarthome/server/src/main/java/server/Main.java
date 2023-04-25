package server;

import io.grpc.Server;
import io.grpc.ServerBuilder;

import java.io.IOException;

public class Main {
    private static int server1Port = 50051;
    private static int server2Port = 50052;

    public static void main(String[] args) {
        TempSensorService tempSensorService = new TempSensorService();
        LightSwitchService lightSwitchService = new LightSwitchService();
        FurnaceService furnaceService = new FurnaceService();

        Server server1 = ServerBuilder
                .forPort(server1Port)
                .addService(tempSensorService)
                .addService(lightSwitchService)
                .addService(furnaceService)
                .build();

        Server server2 = ServerBuilder
                .forPort(server2Port)
                .addService(tempSensorService)
                .addService(lightSwitchService)
                .addService(furnaceService)
                .build();

        System.out.println("Server 1 is listening on port " + server1Port);
        System.out.println("Server 2 is listening on port " + server2Port);

        try {
            server1.start();
            server2.start();

            server1.awaitTermination();
            server2.awaitTermination();
        } catch (IOException | InterruptedException e) {
            throw new RuntimeException(e);
        }
    }
}