from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

def run_ftp_server():
    # Setting up user authentication
    authorizer = DummyAuthorizer()
    authorizer.add_user("user", "12345", ".", perm="elradfmw")  # Username, Password, Root Directory, Permissions
    authorizer.add_anonymous(".", perm="elr")  # Optional: Anonymous access

    # Configuring the FTP handler
    handler = FTPHandler
    handler.authorizer = authorizer

    # Running the server on localhost:2121
    server = FTPServer(("0.0.0.0", 2121), handler)
    print("FTP server running on port 2121...")
    
    # Start the server
    server.serve_forever()

if __name__ == "__main__":
    run_ftp_server()
