package server;

import com.google.rpc.StatusProto;
import io.grpc.Status;
import io.grpc.stub.StreamObserver;
import stubs.Common;
import stubs.Common.Location;
import stubs.TempSensorServiceGrpc;
import stubs.Tempsensor;

import java.util.Arrays;
import java.util.List;
import java.util.Optional;

public class TempSensorService extends TempSensorServiceGrpc.TempSensorServiceImplBase {
    private List<Tempsensor.TempSensor> tempSensors;

    public TempSensorService() {
        Tempsensor.TempSensor.Builder builder = Tempsensor.TempSensor.newBuilder();
        this.tempSensors = Arrays.asList(
                builder.setId(1).setLocationValue(Location.BATHROOM_VALUE).setTemperature(20).build(),
                builder.setId(2).setLocationValue(Location.GARAGE_VALUE).setTemperature(5).build(),
                builder.setId(3).setLocationValue(Location.KITCHEN_VALUE).setTemperature(22).build()
        );
    }

    @Override
    public void get(Tempsensor.GetRequest request, StreamObserver<Tempsensor.TempSensor> responseObserver) {
        Optional<Tempsensor.TempSensor> tempSensor = tempSensors.stream()
                .filter(s -> s.getId() == request.getId())
                .findFirst();
        if (tempSensor.isPresent()) {
            responseObserver.onNext(tempSensor.get());
        } else {
            responseObserver.onError(Status.NOT_FOUND.asRuntimeException());
        }
        responseObserver.onCompleted();
    }

    @Override
    public void list(Common.Empty request, StreamObserver<Tempsensor.ListResponse> responseObserver) {
        Tempsensor.ListResponse response = Tempsensor.ListResponse.newBuilder()
                .addAllSensors(this.tempSensors)
                .build();
        responseObserver.onNext(response);
        responseObserver.onCompleted();
    }
}
