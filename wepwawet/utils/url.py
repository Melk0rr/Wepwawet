import ssl
import socket

class URL:

    def __init__(self,url="",port=666):
        self.l_URL = url
        self.l_Domain = self.Extract_Domain() or url
        self.l_Port = port or 666 
        self.l_Socket = -1
        self.l_SSLcontext = -1
        self.l_WrappedSocket = -1
        self.B_SOCKET_WRAPPED = False
        self.B_SOCKET_OPENED = False


    def Set_URL(self,v_URL):
        self.l_URL = v_URL
        self.l_Domain = self.Extract_Domain()

    def Get_URL(self):
        return self.l_URL

    def Set_Port(self,v_Port):
        self.l_Port = v_Port

    def Get_Port(self):
        return self.l_Port

    def Get_Domain(self):
        return  self.l_Domain

    def Extract_Domain(self):
        return self.l_URL.split("//")[-1].split("/")[0]

    def Create_Socket(self):
        try:
            self.l_Socket = socket.create_connection((self.Get_Domain(), self.Get_Port()))
            self.B_SOCKET_OPENED = True
            return self.l_Socket
        except:
            raise Exception("Error while creating socket")

    def Close_Socket(self):
        if self.B_SOCKET_OPENED:
            self.l_Socket.close();
        self.B_SOCKET_OPENED = False


    def Get_Socket(self):
        if(self.l_Socket!=-1):
            return self.l_Socket

    def Wrap_Socket(self):
        try:
            self.l_SSLcontext = ssl.create_default_context()
            self.l_WrappedSocket = self.l_SSLcontext.wrap_socket(self.Get_Socket(), server_hostname=self.Get_Domain())
            self.B_SOCKET_WRAPPED = True
            return True
        except:    
            print("cannot wrap socket with default context")
            return False

            
    def Wrap_Socket_With(self,TLS_version):
        try:
            self.l_SSLcontext = ssl.SSLContext(TLS_version)
            self.l_WrappedSocket = self.l_SSLcontext.wrap_socket(self.Get_Socket(), server_hostname=self.Get_Domain())
            self.B_SOCKET_WRAPPED = True
            return True
        except:    
            print("cannot wrap socket with",TLS_version)
            return False
            
    def Get_SSLVersion(self):
        if self.B_SOCKET_WRAPPED:
            return self.l_WrappedSocket.version()
        else:
            return "Socket was not Wrapped"

    def Get_SSLCyherUsed(self):
        if self.B_SOCKET_WRAPPED:
            return self.l_WrappedSocket.getpeercert()
        else:
            return "Socket is Not Wrapped: No cypher can be used"


    def Get_Certificate(self):
        if self.B_SOCKET_WRAPPED:
            return self.l_WrappedSocket.cipher()
        else:
            return "Socket is Not Wrapped: No certificate can be retrieved"

    def Get_Header(self):
        if self.B_SOCKET_WRAPPED:
            str_Data = f"HEAD / HTTP/1.0\r\nHost: {self.Get_Domain()}\r\n\r\n"
            str_Encoded = str.encode(str_Data)
            self.l_WrappedSocket.sendall(str_Encoded)
            return self.l_WrappedSocket.recv(1024).split(b"\r\n")
        else:
            return "Socket is Not Wrapped: No certificate can be retrieved"







