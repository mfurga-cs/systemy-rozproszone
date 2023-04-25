package sr;

import Demo.OpRequest;
import Demo.OpResponse;
import com.zeroc.Ice.Communicator;
import com.zeroc.Ice.InputStream;
import com.zeroc.Ice.OperationNotExistException;
import com.zeroc.Ice.OutputStream;


public class InvokeI implements com.zeroc.Ice.Blobject {
    @Override
    public Ice_invokeResult ice_invoke(byte[] inParams, com.zeroc.Ice.Current current) {
        System.out.println(inParams);

        Communicator communicator = current.adapter.getCommunicator();
        InputStream in = new InputStream(communicator, inParams);
        OutputStream out = new OutputStream(communicator);

        in.startEncapsulation();

        Ice_invokeResult r = new Ice_invokeResult();
        r.returnValue = true;

        System.out.println("OPERATION (" + current.operation + "):");

        if (current.operation.equals("reverseString"))
        {
            String message = in.readString();
            System.out.println(message);

            out.startEncapsulation();
            out.writeString(new StringBuilder(message).reverse().toString());
            out.endEncapsulation();
        }

        else if (current.operation.equals("reverseStringArray"))
        {
            String[] seq = in.readStringSeq();
            String[] res = new String[seq.length];

            for (int i = 0; i < seq.length; ++i)
            {
                if(i > 0)
                    System.out.print(", ");
                System.out.print(seq[i]);
                res[seq.length - i - 1] = seq[i];
            }

            out.startEncapsulation();
            out.writeStringSeq(res);
            out.endEncapsulation();
        }
        else if (current.operation.equals("doMath")) {
            OpRequest opRequest = OpRequest.ice_read(in);
            OpResponse opResponse = new OpResponse();

            switch (opRequest.operation) {
                case MAX -> opResponse.r = Math.max(opRequest.a, opRequest.b);
                case MIN -> opResponse.r = Math.min(opRequest.a, opRequest.b);
                case SUM -> opResponse.r = opRequest.a + opRequest.b;
                case SUB -> opResponse.r = opRequest.a - opRequest.b;
            }

            out.startEncapsulation();
            OpResponse.ice_write(out, opResponse);
            out.endEncapsulation();
        } else {
            OperationNotExistException ex = new OperationNotExistException();
            ex.id = current.id;
            ex.facet = current.facet;
            ex.operation = current.operation;
            throw ex;
        }
        System.out.println();

        r.outParams = out.finished();
        in.endEncapsulation();
        return r;
    }
}