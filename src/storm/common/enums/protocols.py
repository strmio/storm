from enum import Enum

class Protocol(Enum):
    HTTP = "http"
    HTTPS = "https"
    FTP = "ftp"
    SFTP = "sftp"
    SMTP = "smtp"
    POP3 = "pop3"
    IMAP = "imap"
    WS = "ws"  # WebSocket
    WSS = "wss"  # Secure WebSocket
    GRPC = "grpc"  # gRPC
    MQTT = "mqtt"  # Message Queuing Telemetry Transport
    AMQP = "amqp"  # Advanced Message Queuing Protocol
    COAP = "coap"  # Constrained Application Protocol
    RTSP = "rtsp"  # Real-Time Streaming Protocol
    SSH = "ssh"  # Secure Shell
    TELNET = "telnet"
    SNMP = "snmp"  # Simple Network Management Protocol
    LDAP = "ldap"  # Lightweight Directory Access Protocol
    SMB = "smb"  # Server Message Block
    NFS = "nfs"  # Network File System
    RDP = "rdp"  # Remote Desktop Protocol
    SOAP = "soap"  # Simple Object Access Protocol
    XML_RPC = "xml-rpc"  # XML-RPC Protocol
    TOR = "tor"  # The Onion Router Protocol
