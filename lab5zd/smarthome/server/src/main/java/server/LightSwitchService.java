package server;

import io.grpc.Status;
import io.grpc.stub.StreamObserver;
import stubs.Common;
import stubs.LightSwitchServiceGrpc;
import stubs.Lightswitch;

import java.util.ArrayList;
import java.util.Optional;

public class LightSwitchService extends LightSwitchServiceGrpc.LightSwitchServiceImplBase {
    private ArrayList<Lightswitch.LightSwitch> lightSwitches = new ArrayList<>();

    public LightSwitchService() {
        Lightswitch.LightSwitch.Builder builder = Lightswitch.LightSwitch.newBuilder();
        lightSwitches.add(builder.setId(1).setLocationValue(Common.Location.BATHROOM_VALUE).setState(true).build());
        lightSwitches.add(builder.setId(2).setLocationValue(Common.Location.GARAGE_VALUE).setState(true).build());
        lightSwitches.add(builder.setId(3).setLocationValue(Common.Location.KITCHEN_VALUE).setState(false).build());
    }

    @Override
    public void list(Common.Empty request, StreamObserver<Lightswitch.ListResponse> responseObserver) {
        Lightswitch.ListResponse response = Lightswitch.ListResponse.newBuilder()
                .addAllLightSwitches(this.lightSwitches)
                .build();
        responseObserver.onNext(response);
        responseObserver.onCompleted();
    }

    @Override
    public void get(Lightswitch.Request request, StreamObserver<Lightswitch.LightSwitch> responseObserver) {
        Optional<Lightswitch.LightSwitch> lightSwitch = lightSwitches.stream()
                .filter(s -> s.getId() == request.getId())
                .findFirst();
        if (lightSwitch.isPresent()) {
            responseObserver.onNext(lightSwitch.get());
        } else {
            responseObserver.onError(Status.NOT_FOUND.asRuntimeException());
        }
        responseObserver.onCompleted();
    }

    @Override
    public void toggle(Lightswitch.Request request, StreamObserver<Common.Empty> responseObserver) {
        Optional<Lightswitch.LightSwitch> lightSwitch = lightSwitches.stream()
                .filter(s -> s.getId() == request.getId())
                .findFirst();
        if (lightSwitch.isPresent()) {
            Lightswitch.LightSwitch ls = lightSwitch.get();
            lightSwitches.add(
                Lightswitch.LightSwitch.newBuilder()
                        .setId(ls.getId())
                        .setLocation(ls.getLocation())
                        .setState(!ls.getState())
                        .build());
            lightSwitches.remove(ls);
            responseObserver.onNext(Common.Empty.newBuilder().build());
        } else {
            responseObserver.onError(Status.NOT_FOUND.asRuntimeException());
        }
        responseObserver.onCompleted();
    }
}
