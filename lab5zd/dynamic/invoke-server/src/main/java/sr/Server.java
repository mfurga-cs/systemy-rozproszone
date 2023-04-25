package sr;

import com.zeroc.Ice.Communicator;
import com.zeroc.Ice.Identity;
import com.zeroc.Ice.ObjectAdapter;
import com.zeroc.Ice.Util;

public class Server
{
	public static void main(String[] args)
	{
		Communicator communicator = Util.initialize(args);

		// 2. Konfiguracja adaptera
		// METODA 1 (polecana produkcyjnie): Konfiguracja adaptera Adapter1 jest w pliku konfiguracyjnym podanym jako parametr uruchomienia serwera
		//ObjectAdapter adapter = communicator.createObjectAdapter("Adapter1");

		// METODA 2 (niepolecana, dopuszczalna testowo): Konfiguracja adaptera Adapter1 jest w kodzie źródłowym
		//ObjectAdapter adapter = communicator.createObjectAdapterWithEndpoints("Adapter1", "tcp -h 127.0.0.2 -p 10000");
		//ObjectAdapter adapter = communicator.createObjectAdapterWithEndpoints("Adapter1", "tcp -h 127.0.0.2 -p 10000 : udp -h 127.0.0.2 -p 10000");
		ObjectAdapter adapter = communicator.createObjectAdapterWithEndpoints(
				"Adapter", "tcp -h 127.0.0.2 -p 10000 -z : udp -h 127.0.0.2 -p 10000 -z");

		// 3. Utworzenie serwanta/serwantów

		// 4. Dodanie wpisów do tablicy ASM, skojarzenie nazwy obiektu (Identity) z serwantem
		adapter.add(new InvokeI(), new Identity("invoke", "invoke"));

		// 5. Aktywacja adaptera i wejście w pętlę przetwarzania żądań
		adapter.activate();

		System.out.println("Entering event processing loop...");
		communicator.waitForShutdown();
	}
}
