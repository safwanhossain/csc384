import java.net.*;
import java.io.*;
import java.util.Scanner;

public class GoBackNClientPart2 {

	public static void main(String[] args) throws UnknownHostException, IOException {
		// TODO Auto-generated method stub
		try{
		    Socket socket = new Socket("localhost", 9876 );
            
            // Reading whats on server
            BufferedReader reader=new BufferedReader(new InputStreamReader(socket.getInputStream()));
            DataOutputStream writer = new DataOutputStream(socket.getOutputStream());

            Scanner scr = new Scanner( System.in );
            System.out.println("Number of packets? ");
            int numPackets = scr.nextInt();
            System.out.println("Error Probability? ");
            int errorProb = scr.nextInt();

            String CRLF = "\r\n";
            writer.write( numPackets );
            writer.write( errorProb );
            
            //Sent can be thought of as the sequence number (ish). Both sender and reciver
            //must match the sent numbers in order to progress. Hence we aim to keep consistancy
            int sent = 1;
            while( sent <= numPackets ) {
                System.out.println( String.format("Sending: %d", sent ) );
                writer.write( sent );
                sent++;
            }
            while( (int)reader.read() != numPackets );
            socket.close(); 
        }
        catch( Exception e ) {
            e.getStackTrace();
        }
	}
}



