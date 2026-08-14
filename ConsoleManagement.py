from tcp import *
from http import *
from networking import *
from time import *

choice = 6
tcp_state = -1
http_state = -1

def line():
    print("----------------------------------------")

def tcp_done(s):
    global tcp_state
    tcp_state = s

def http_done(s, d):
    global http_state
    if s == 200:
        http_state = 0
    else:
        http_state = 4

def tcp_test(ip, port):
    global tcp_state
    tcp_state = -1

    try:
        c = TCPClient()
        c.onConnectionChange(tcp_done)
        c.connect(ip, port)

        n = 0
        while tcp_state == -1 and n < 50:
            delay(100)
            n += 1

        c.close()
        return tcp_state == 0
    except:
        return False

def http_test(url):
    global http_state
    http_state = -1

    try:
        h = HTTPClient()
        h.onDone(http_done)
        h.open(url)

        n = 0
        while http_state == -1 and n < 50:
            delay(100)
            n += 1

        h.stop()
        return http_state == 0
    except:
        return False

def show(name, ok):
    if ok:
        print(name + ": Online - Success")
    else:
        print(name + ": Offline - Failed")

def check_dns():
    ok = http_test("http://www.university.local")
    show("DNS", ok)
    return ok

def check_web():
    ok = http_test("http://192.168.40.12")
    show("Web Server", ok)
    return ok

def check_mail():
    ok = tcp_test("192.168.40.13", 25)
    show("Mail Server", ok)
    return ok

def check_file():
    ok = tcp_test("192.168.40.14", 21)
    show("File Server", ok)
    return ok

def check_dhcp():
    try:
        ip = localIP()
        p = ip.split(".")
        ok = False

        if len(p) == 4:
            if p[0] == "192" and p[1] == "168" and p[2] == "10":
                n = int(p[3])
                if n >= 100 and n <= 199:
                    ok = True

        if ok:
            print("DHCP: Online - Success")
            print("Local IP: " + ip)
        else:
            print("DHCP: Offline - Failed")

        return ok
    except:
        print("DHCP: Offline - Failed")
        return False

def report():
    good = 0

    line()
    print("University Network Service Report")
    line()

    if check_dns():
        good += 1
    if check_web():
        good += 1
    if check_mail():
        good += 1
    if check_file():
        good += 1
    if check_dhcp():
        good += 1

    line()
    print("Online Services: " + str(good) + "/5")

    if good == 5:
        print("Overall: SUCCESS - All services online")
    elif good == 0:
        print("Overall: FAILED - All services offline")
    else:
        print("Overall: WARNING - Some services offline")

    line()

def menu():
    line()
    print("University Network Management Console")
    line()
    print("1. Check DNS")
    print("2. Check Web Server")
    print("3. Check Mail Server")
    print("4. Check File Server")
    print("5. Check DHCP")
    print("6. Overall Service Report")
    print("7. Exit")
    line()
    print("Selected option: " + str(choice))
    print("")

    if choice == 1:
        check_dns()
    elif choice == 2:
        check_web()
    elif choice == 3:
        check_mail()
    elif choice == 4:
        check_file()
    elif choice == 5:
        check_dhcp()
    elif choice == 6:
        report()
    elif choice == 7:
        print("Console closed")
    else:
        print("Invalid option")

menu()