import socket
import ssl

# Exemple Usage

# MyURL = C_SSLSocket(url="https://www.ramsaysante.fr",port=443)
# print(MyURL.Get_Domain())
# print("TLS 1.0 = ",MyURL.IsTLSEnabled(ssl.PROTOCOL_TLSv1))
# print("TLS 1.1 = ",MyURL.IsTLSEnabled(ssl.PROTOCOL_TLSv1_1))
# print("TLS 1.2 = ",MyURL.IsTLSEnabled(ssl.PROTOCOL_TLSv1_2))

# MyURL.Open_Socket()
# MyURL.Wrap_Socket()
# print(MyURL.Get_SSLVersion())
# MyURL.Close_Socket()

# Exemple Usage 2
# MyURL = C_SSLSocket(url="https://www.ramsaysante.fr",port=443)
# print(MyURL.Get_TLS_State())
# --> {'result_list': 'False, False, true, true'}

SSLEquiv = ( 
        ("TLS1.0",ssl.PROTOCOL_TLSv1),
        ("TLS1.1",ssl.PROTOCOL_TLSv1_1),
        ("TLS1.2",ssl.PROTOCOL_TLSv1_2),
        ("TLS1.3",None)) 

class C_Socket:
    
    def __init__(self,url,port=666):
        self.l_URL = url
        self.l_Domain = self.Extract_Domain() or url
        self.l_Port = port or 666
        self.l_Socket = -1
        self.B_SOCKET_OPENED = False

    def Set_Socket(self,v_URL):
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

    def Open_Socket(self):
        if 443 in self.l_URL.open_ports:
            try:
                if self.B_SOCKET_OPENED:
                    print (__class__.__name__ + ": Socket already opened")
                    return -1
                else:
                    self.l_Socket = socket.create_connection((self.Get_Domain(), 443))
                    self.B_SOCKET_OPENED = True
                    return self.l_Socket
            except:
                self.B_SOCKET_OPENED = False
                print (__class__.__name__ + ": Error while creating socket")
                return -1
        else:
            

    def Close_Socket(self):
        if self.B_SOCKET_OPENED:
            self.l_Socket.close();
        else:
            print(f"In {__class__.__name__} : Trying to close an unexisting socket")
        self.B_SOCKET_OPENED = False
        self.B_SOCKET_WRAPPED = False

    def Get_Socket(self):
        if(self.l_Socket!=-1):
            return self.l_Socket

class C_SSLSocket(C_Socket):

    def __init__(self,url="",port=666):
        super().__init__(url=url,port=port)
        self.l_SSLcontext = -1
        self.l_WrappedSocket = -1
        self.B_SOCKET_WRAPPED = False

    def Get_SSLContext(self):
        if(self.l_SSLcontext!=-1):
            return self.l_SSLcontext

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
                self.l_WrappedSocket = self.l_SSLcontext.wrap_socket(super().Get_Socket(), server_hostname=super().Get_Domain())
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



    #*******************************************************
    #def IsTLSEnabled(self,TLS_version)
    #   where TLS_version can be: 
    #       ssl.PROTOCOL_TLSv1
    #       ssl.PROTOCOL_TLSv1_1
    #       ssl.PROTOCOL_TLSv1_2 
    #*******************************************************
    def IsTLSEnabled(self,TLS_version):
        value =""
        super().Open_Socket()
        if self.Wrap_Socket(TLS_version):
            value = self.Get_SSLVersion()
        super().Close_Socket()
        return value

    def Get_TLS_State(self):
        result_list = dict()
        for i in range(0,4):
            response = self.IsTLSEnabled(SSLEquiv[i][1])
            if response:
                if (SSLEquiv[i][0]=="TLSv1.3" and response != "TLSv1.3"):
                    value = False
                else:
                    value = True
            else:
                value = False
            result_list[SSLEquiv[i][0]] = value
        return result_list
