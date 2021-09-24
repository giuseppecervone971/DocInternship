import subprocess


def main():

        subprocess.run(["zabbix_sender", "-z", "192.168.1.157", "-i", "data.txt", "-T"])



if __name__ == '__main__':
    main()
