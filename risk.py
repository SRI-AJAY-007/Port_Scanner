risk_levels = {
    21: "MEDIUM - FTP exposed",
    23: "HIGH - Telnet exposed",
    445: "MEDIUM - SMB exposed",
    3306: "HIGH - MySQL exposed",
    3389: "MEDIUM - RDP exposed"
}

def get_risk(port):
    return risk_levels.get(port, "LOW")