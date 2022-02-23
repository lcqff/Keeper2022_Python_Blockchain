import socket
import struct
import traceback
import threading

class BTPeerConnection:
    def __init__( self, peerid, host, port, sock=None, debug=False ):
        self.id = peerid
        self.debug = debug

        if not sock:
            self.s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            self.s.connect( ( host, int(port) ) ) #peer1에 연결한다?
        else:
            self.s = sock

        self.sd = self.s.makefile( 'rw', 0 )


    def __makemsg( self, msgtype, msgdata ):
        msglen = len(msgdata)
        msg = struct.pack( "!4sL%ds" % msglen, msgtype, msglen, msgdata )
        return msg

    def btdebug(msg):
        print ("[%s] %s" % (str(threading.currentThread().getName()), msg))
        """ Prints a messsage to the screen with the name of the current thread """

    def __debug( self, msg ):
        if self.debug: self.btdebug( msg )



    """
    senddata( message type, message data ) -> boolean status
    Send a message through a peer connection. Returns True on success
    or False if there was an error.
    """
    def senddata( self, msgtype, msgdata ):

        try:
            msg = self.__makemsg( msgtype, msgdata )
            self.sd.write( msg )
            self.sd.flush()
        except KeyboardInterrupt:
            raise
        except:
            if self.debug:
                traceback.print_exc()
            return False
        return True


    """
    recvdata() -> (msgtype, msgdata)
    Receive a message from a peer connection. Returns (None, None)
    if there was any error.
    """
    def recvdata( self ):
        try:
            msgtype = self.sd.read( 4 )
            if not msgtype: return (None, None)
            lenstr = self.sd.read( 4 )
            msglen = int(struct.unpack( "!L", lenstr )[0])
            msg = ""

            while len(msg) != msglen:
                data = self.sd.read( min(2048, msglen - len(msg)) )
                if not len(data):
                    break
                msg += data

                if len(msg) != msglen:
                    return (None, None)

        except KeyboardInterrupt:
            raise
        except:
            if self.debug:
                traceback.print_exc()
            return (None, None)

        return ( msgtype, msg )

    # end recvdata method

    """
    close()
    Close the peer connection. The send and recv methods will not work
    after this call.
    """
    def close( self ):
        self.s.close()
        self.s = None
        self.sd = None


    def __str__( self ):
        return "|%s|" % self.peerid