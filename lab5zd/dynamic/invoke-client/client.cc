#include <Ice/Ice.h>

#include <memory>

#include <Invoke.h>

using namespace std;
using namespace Demo;

int run(const shared_ptr < Ice::Communicator > & );

int
main(int argc, char * argv[]) {
  #ifdef ICE_STATIC_LIBS
  Ice::registerIceSSL();
  #endif

  int status = 0;

  try {
    //
    // CommunicatorHolder's ctor initializes an Ice communicator,
    // and its dtor destroys this communicator.
    //
    const Ice::CommunicatorHolder ich(argc, argv);

    // The communicator initialization removes all Ice-related arguments from argc/argv
    if (argc > 1) {
      cerr << argv[0] << ": too many arguments" << endl;
      status = 1;
    } else {
      status = run(ich.communicator());
    }
  } catch (const std::exception & ex) {
    cerr << argv[0] << ": " << ex.what() << endl;
    status = 1;
  }

  return status;
}

void menu();

int
run(const shared_ptr < Ice::Communicator > & communicator) {
  //auto obj = communicator->propertyToProxy("Printer.Proxy");
  auto obj = communicator -> stringToProxy(
    "invoke/invoke:tcp -h 127.0.0.2 -p 10000 -z : udp -h 127.0.0.2 -p 10000 -z");

  menu();

  char ch = 'x';
  do {
    try {
      cout << "==> ";
      cin >> ch;
      if (ch == '1') {
        // Marshal the in parameter.
        Ice::ByteSeq inParams, outParams;
        Ice::OutputStream out(communicator);
        out.startEncapsulation();
        out.write("ala ma kota");
        out.endEncapsulation();
        out.finished(inParams);

        // Invoke operation.
        if (!obj -> ice_invoke("reverseString", Ice::OperationMode::Normal, inParams, outParams)) {
          cout << "Error" << endl;
        }

        // Read result
        std::string res;
        Ice::InputStream in (communicator, outParams);
        in.startEncapsulation();
        in.read(res);
        in.endEncapsulation();
        cout << res << endl;
      } else if (ch == '2') {
        // Marshal the in parameter.
        Ice::ByteSeq inParams, outParams;
        Ice::OutputStream out(communicator);
        out.startEncapsulation();
        //const Demo::StringSeq arr({"The", "streaming", "API", "works!"});
        std::vector<std::string> arr = { "ala", "ma", "kota" };
        out.write(arr);
        out.endEncapsulation();
        out.finished(inParams);

        // Invoke operation.
        if(!obj->ice_invoke("reverseStringArray", Ice::OperationMode::Normal, inParams, outParams)) {
            cout << "Unknown user exception" << endl;
        }

        std::vector<std::string> res;
        Ice::InputStream in (communicator, outParams);
        in.startEncapsulation();
        in.read(res);
        in.endEncapsulation();

        for (int i = 0; i < res.size(); i++) {
          if (i > 0) {
            cout << ", ";
          }
          cout << res[i];
        }
        cout << endl;
      } else if (ch == '3') {
        // Marshal the in parameter.
        Ice::ByteSeq inParams, outParams;
        Ice::OutputStream out(communicator);
        out.startEncapsulation();

        Demo::OpRequest r;
        r.operation = Operation::SUM;
        r.a = 10;
        r.b = 20;

        out.write(r);
        out.endEncapsulation();
        out.finished(inParams);

        // Invoke operation.
        if(!obj->ice_invoke("doMath", Ice::OperationMode::Normal, inParams, outParams)) {
          cout << "Error" << endl;
        }

        Demo::OpResponse res;
        Ice::InputStream in(communicator, outParams);
        in.startEncapsulation();
        in.read(res);
        in.endEncapsulation();

        cout << res.r << endl;
      } else if (ch == 'x') {
        // Nothing to do.
      } else if (ch == '?') {
        menu();
      } else {
        cout << "unknown command `" << ch << "'" << endl;
        menu();
      }
    } catch (const Ice::Exception & ex) {
      cerr << ex << endl;
    }
  }
  while (cin.good() && ch != 'x');

  return 0;
}

void
menu() {
  cout <<
    "1) reverse string\n"
  "2) reverse string array\n"
  "3) do math (add)\n" << endl;
}
