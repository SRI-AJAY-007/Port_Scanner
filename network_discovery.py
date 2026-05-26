import socket
from concurrent.futures import ThreadPoolExecutor


active_hosts = []


def discover_host(ip):

    try:
        socket.setdefaulttimeout(0.5)

        s = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        result = s.connect_ex(
            (ip, 80)
        )

        if result == 0:

            print(
                f"[+] Active Host: {ip}"
            )

            active_hosts.append(
                ip
            )

        s.close()

    except:
        pass


def scan_network(base_ip):

    print(
        "\nSearching for active hosts...\n"
    )

    ip_range = [
        f"{base_ip}.{i}"
        for i in range(1,255)
    ]

    with ThreadPoolExecutor(
        max_workers=100
    ) as executor:

        executor.map(
            discover_host,
            ip_range
        )

    return active_hosts