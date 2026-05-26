def grab_banner(socket_obj):

    try:
        banner = socket_obj.recv(
            1024
        ).decode().strip()

        if banner:
            return banner

        return "No Banner Available"

    except:
        return "No Banner Available"