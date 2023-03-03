//package org.example;

import java.awt.*;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.nio.ByteBuffer;
import java.util.Arrays;

public class JavaUdpServer {

    public static void main(String args[])
    {
        System.out.println("JAVA UDP SERVER");
        DatagramSocket socket = null;
        int portNumber = 9009;

        try{
            socket = new DatagramSocket(portNumber);
            byte[] receiveBuffer = new byte[1024];

            while(true) {
                Arrays.fill(receiveBuffer, (byte)0);
                DatagramPacket receivePacket = new DatagramPacket(receiveBuffer, receiveBuffer.length);
                socket.receive(receivePacket);
                byte[] res = receivePacket.getData();

//                Integer num = res[1] << 8 | res[0];
                Integer num = java.nio.ByteBuffer.wrap(res).order(java.nio.ByteOrder.LITTLE_ENDIAN).getInt();

                System.out.println(num);
                InetAddress address = receivePacket.getAddress();

                num += 1;

                byte[] sendBuffer = ByteBuffer.allocate(4).putInt(num).array();
                DatagramPacket sendPacket = new DatagramPacket(sendBuffer, sendBuffer.length, address, portNumber + 1);
                socket.send(sendPacket);
                System.out.println();
            }
        }
        catch(Exception e){
            e.printStackTrace();
        }
        finally {
            if (socket != null) {
                socket.close();
            }
        }
    }
}

