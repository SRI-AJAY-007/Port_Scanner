import socket
import time
from concurrent.futures import ThreadPoolExecutor

from services import services
from risk import get_risk
from banner import grab_banner
from report import save_results


print("""
=========================================
        SentinelScan v1.0
   Intelligent Network Recon Tool
=========================================
""")


open_ports = []
active_hosts = []


# ------------------------------------
# Host Discovery
# ------------------------------------

def discover_host(ip):

    common_ports = [80, 443, 22, 445, 3389]

    for port in common_ports:

        try:

            s = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )

            s.settimeout(0.3)

            result = s.connect_ex(
                (ip, port)
            )

            s.close()

            if result == 0:

                return ip

        except:
            pass

    return None


def scan_network(base_ip):

    print("\nSearching for active hosts...\n")

    ip_range = [
        f"{base_ip}.{i}"
        for i in range(1,255)
    ]

    discovered = []

    with ThreadPoolExecutor(max_workers=100) as executor:

        results = executor.map(
            discover_host,
            ip_range
        )

    for host in results:

        if host and host not in discovered:

            discovered.append(host)

            print(
                f"[+] Active Host: {host}"
            )

    return discovered


# ------------------------------------
# Target Selection
# ------------------------------------

choice = input(
    "Scan network first? (y/n): "
)

if choice.lower() == "y":

    base_ip = input(
        "Enter base network (Example: 192.168.1): "
    )

    hosts = scan_network(base_ip)

    if not hosts:

        print(
            "\nNo active hosts found."
        )

        exit()

    print(
        "\nDetected Hosts:\n"
    )

    for host in hosts:
        print(host)

    target = input(
        "\nChoose target IP: "
    )

else:

    target = input(
        "Enter target IP: "
    )


start_port = int(
    input("Start Port: ")
)

end_port = int(
    input("End Port: ")
)


print(
    f"\nScanning {target}...\n"
)

start_time = time.time()


# ------------------------------------
# Port Scanner
# ------------------------------------

def scan_port(port):

    try:

        s = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        s.settimeout(0.5)

        result = s.connect_ex(
            (target, port)
        )

        if result == 0:

            service_name = services.get(
                port,
                "Unknown Service"
            )

            banner = grab_banner(
                s
            )

            risk = get_risk(
                port
            )

            data = {

                "port": port,
                "service": service_name,
                "banner": banner,
                "risk": risk
            }

            open_ports.append(
                data
            )

        s.close()

    except:
        pass


with ThreadPoolExecutor(
    max_workers=100
) as executor:

    executor.map(
        scan_port,
        range(
            start_port,
            end_port + 1
        )
    )


# ------------------------------------
# Results Processing
# ------------------------------------

open_ports = sorted(
    open_ports,
    key=lambda x: x["port"]
)


for result in open_ports:

    print(
        f'{result["port"]} → '
        f'{result["service"]} → '
        f'{result["banner"]} → '
        f'{result["risk"]}'
    )


save_results(
    target,
    open_ports
)


high_count = sum(
    1 for p in open_ports
    if "HIGH" in p["risk"]
)

medium_count = sum(
    1 for p in open_ports
    if "MEDIUM" in p["risk"]
)

low_count = sum(
    1 for p in open_ports
    if p["risk"] == "LOW"
)


end_time = time.time()


print("\n========== Scan Summary ==========")

print(
    f"Open Ports Found: {len(open_ports)}"
)

print(
    f"High Risk: {high_count}"
)

print(
    f"Medium Risk: {medium_count}"
)

print(
    f"Low Risk: {low_count}"
)

print(
    f"Scan Time: "
    f"{round(end_time-start_time,2)} seconds"
)

print("\nScan Completed")