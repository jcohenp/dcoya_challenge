import ssl
import socket
import datetime
import certifi

def check_ssl_certificate(hostname, port):
    try:
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        conn = ssl_context.wrap_socket(socket.create_connection((hostname, port)), server_hostname=hostname)
        conn.settimeout(5.0)
        conn.do_handshake()

        ssl_info = conn.getpeercert()
        expiry_date_str = ssl_info.get('notAfter') or ssl_info.get('not_after') or ssl_info.get('expiry_date')
        if expiry_date_str:
            expiry_date = datetime.datetime.strptime(expiry_date_str, '%b %d %H:%M:%S %Y %Z')
        else:
            expiry_date = None

        current_date = datetime.datetime.now()
        days_until_expiry = (expiry_date - current_date).days if expiry_date else None

        return {
            'expiry_date': expiry_date,
            'current_date': current_date,
            'days_until_expiry': days_until_expiry,
            'ssl_info': ssl_info
        }

    except Exception as e:
        return {'error': f'SSL connection failed: {e}'}

# Test Example
hostname = 'dcoya'  # Replace with your hostname
port = 30000  # Replace with your port

ssl_details = check_ssl_certificate(hostname, port)
print("SSL Information:", ssl_details)

