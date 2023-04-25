package sr;

import Demo.OpRequest;
import Demo.OpResponse;
import Demo.Operation;
import com.zeroc.Ice.*;
import com.zeroc.Ice.Object;

import java.util.Arrays;

public class Client
{
	public static void main(String[] args) {
		Communicator communicator = Util.initialize(args);
		run(communicator);
	}

	private static int run(com.zeroc.Ice.Communicator communicator)
	{
		com.zeroc.Ice.ObjectPrx obj = communicator.stringToProxy(
				"invoke/invoke:tcp -h 127.0.0.2 -p 10000 -z : udp -h 127.0.0.2 -p 10000 -z");

		menu();

		java.io.BufferedReader reader = new java.io.BufferedReader(new java.io.InputStreamReader(System.in));
		String line = null;

		do  {
			try {
				System.out.print("==> ");
				System.out.flush();
				line = reader.readLine();

				if (line == null) {
					break;
				}

				if (line.equals("1")) {
					// Marshal the in parameter
					OutputStream out = new OutputStream(communicator);
					out.startEncapsulation();
					out.writeString("ala ma kota");
					out.endEncapsulation();

					byte[] res = out.finished();
					for (int i = 0; i < res.length; i++) {
						System.out.printf("\\x%02x", res[i]);
					}
					System.out.println();

					// Invoke operation
					Object.Ice_invokeResult r = obj.ice_invoke("reverseString",
							OperationMode.Normal, out.finished());

					if (!r.returnValue) {
						System.out.println("Error");
					}

					InputStream in = new InputStream(communicator, r.outParams);
					in.startEncapsulation();
					System.out.println(in.readString());
					in.endEncapsulation();

				} else if (line.equals("2")) {
					// Marshal the in parameter.
					OutputStream out = new OutputStream(communicator);
					out.startEncapsulation();
					final String[] arr = {"ala", "ma", "kota"};
					out.writeStringSeq(arr);
					out.endEncapsulation();

					// Invoke operation.
					Object.Ice_invokeResult r = obj.ice_invoke("reverseStringArray",
							OperationMode.Normal, out.finished());

					if (!r.returnValue) {
						System.out.println("Error");
					}

					// Marshal the out parameter.
					InputStream in = new InputStream(communicator, r.outParams);
					in.startEncapsulation();
					String[] seq = in.readStringSeq();
					in.endEncapsulation();

					for (int i = 0; i < seq.length; ++i)
					{
						if(i > 0)
							System.out.print(", ");
						System.out.print(seq[i]);
					}
					System.out.println();
				} else if (line.equals("3")) {
					// Marshal the in parameter.
					OutputStream out = new OutputStream(communicator);
					out.startEncapsulation();
					OpRequest opRequest = new OpRequest();
					opRequest.operation = Operation.SUM;
					opRequest.a = 10;
					opRequest.b = 5;
					OpRequest.ice_write(out, opRequest);
					out.endEncapsulation();

					// Invoke operation.
					Object.Ice_invokeResult r = obj.ice_invoke("doMath",
							OperationMode.Normal, out.finished());

					if (!r.returnValue) {
						System.out.println("Error");
					}

					// Marshal the out parameter.
					InputStream in = new InputStream(communicator, r.outParams);
					in.startEncapsulation();
					OpResponse opResponse = OpResponse.ice_read(in);
					in.endEncapsulation();
					System.out.println(opResponse.r);
				}
				else
				{
					System.out.println("unknown command " + line);
					menu();
				}
			}
			catch(java.io.IOException | com.zeroc.Ice.LocalException ex)
			{
				ex.printStackTrace();
			}
		} while(!line.equals("x"));

		return 0;
	}

	private static void menu()
	{
		System.out.println(
			"1) reverse string\n" +
			"2) reverse string array\n" +
			"3) do math (add)\n"
		);
	}

}