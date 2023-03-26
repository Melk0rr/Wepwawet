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
            if self.B_SOCKET_OPENED:
                print (__class__.__name__ + ": Socket already opened")
                return -1
            else:
                self.l_Socket = socket.create_connection((self.Get_Domain(), self.Get_Port()))
                self.B_SOCKET_OPENED = True
                return self.l_Socket
        except:
            self.B_SOCKET_OPENED = False
            print (__class__.__name__ + ": Error while creating socket")
            return -1

    def Close_Socket(self):
        if self.B_SOCKET_OPENED:
            self.l_Socket.close();
            self.B_SOCKET_OPENED = False
            self.B_SOCKET_WRAPPED = False
        else:
            print(f"In {__class__.__name__} : Trying to close an unexisting socket")
        

    def Get_Socket(self):
        if(self.l_Socket!=-1):
            return self.l_Socket

    def Wrap_Socket(self,TLS_version=None):
        try:
            if self.B_SOCKET_WRAPPED:
                print(f"In {__class__.__name__} : Warning trying to wrap a socket already Wrapped")
                return False
            else:
                if TLS_version != None:
                    self.l_SSLcontext = ssl.SSLContext(TLS_version or ssl.PROTOCOL_SSLv23)
                else:
                    self.l_SSLcontext = ssl.create_default_context()
                    
                self.l_WrappedSocket = self.l_SSLcontext.wrap_socket(self.Get_Socket(), server_hostname=self.Get_Domain())
                self.B_SOCKET_WRAPPED = True
                return True
        except Exception as err:
            print(f"In {__class__.__name__} : {type(err).__name__} cannot wrap socket with default {TLS_version}: {err}")        
            self.B_SOCKET_WRAPPED = False
            return False

    def Get_SSLVersion(self):
        if self.B_SOCKET_WRAPPED:
            return self.l_WrappedSocket.version()
        else:
            print(f"In {__class__.__name__} : Socket was not Wrapped")

    def Get_SSLCyherUsed(self):
        if self.B_SOCKET_WRAPPED:
            return self.l_WrappedSocket.cipher()
        else:
            print(f"In {__class__.__name__} : Socket is Not Wrapped: No cypher can be used")

    def Get_Certificate(self):
        if self.B_SOCKET_WRAPPED:
            return self.l_WrappedSocket.getpeercert()
        else:
            print(f"In {__class__.__name__} : Socket is Not Wrapped: No certificate can be retrieved")

    def Get_Header(self):
        if self.B_SOCKET_WRAPPED:
            str_Data = f"HEAD / HTTP/1.0\r\nHost: {self.Get_Domain()}\r\n\r\n"
            str_Encoded = str.encode(str_Data)
            self.l_WrappedSocket.sendall(str_Encoded)
            return self.l_WrappedSocket.recv(1024).split(b"\r\n")
        else:
            print(f"In {__class__.__name__} : ERROR Socket is Not Wrapped: No certificate can be retrieved")

    def Get_SSLContext(self):
        if(self.l_SSLcontext!=-1):
            return self.l_SSLcontext

    def IsTLSEnabled(self,TLS_version):
        try:
            self.Create_Socket()
            value = self.Wrap_Socket(TLS_version)
            self.Close_Socket()
            return value
        except:
            return False


