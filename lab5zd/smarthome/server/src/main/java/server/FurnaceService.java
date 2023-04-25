package server;

import io.grpc.stub.StreamObserver;
import stubs.Common;
import stubs.FurnaceOuterClass;
import stubs.FurnaceServiceGrpc;

public class FurnaceService extends FurnaceServiceGrpc.FurnaceServiceImplBase {
    private FurnaceOuterClass.Furnace furnace;

    public FurnaceService() {
        furnace = FurnaceOuterClass.Furnace.newBuilder()
                .setCurrentTemp(20)
                .setIsWorking(false)
                .build();
    }

    @Override
    public void get(Common.Empty request, StreamObserver<FurnaceOuterClass.Furnace> responseObserver) {
        responseObserver.onNext(furnace);
        responseObserver.onCompleted();
    }

    @Override
    public void set(FurnaceOuterClass.Furnace request, StreamObserver<Common.Empty> responseObserver) {
        this.furnace = request;
        responseObserver.onNext(Common.Empty.newBuilder().build());
        responseObserver.onCompleted();
    }
}
