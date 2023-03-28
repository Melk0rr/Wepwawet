from wepwawet.utils.url import C_SSLSocket


def check_TLS(self, target):
    """ Main TLS function : Check TLS """
    print(f"Cheking TLS for {target['host']}")
    MyURL = C_SSLSocket(url=target['host'],port=443)
    
    TLS_response = {}
    error_message = ""

    try:

        TLS_response = MyURL.Get_TLS_State()
        print(TLS_response)
    except Exception as e:
        error_message = e
        self.handle_exception(e, f"Error while checking TLS informations for {target['host']}")

    return TLS_response