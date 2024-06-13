import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from colorama import init, Fore, Style

# 初始化 colorama
init(autoreset=True)

def print_banner():
    banner = f"""
{Fore.RED}{Style.NORMAL}
██████╗ ██╗  ██╗██████╗      ██████ ██████╗   ██╗
██╔══██╗██║  ██║██╔══██╗    ██╔═══  ██╔════╝  ██║
██████╔╝███████║██████╔╝    ██║     ██║  ███╗ ██║
██╔═══╝ ██╔══██║██╔═══╝     ██║     ██║   ██║ ██║
██║     ██║  ██║██║         ╚██████ ██████╔╝  ██║
╚═╝     ╚═╝  ╚═╝╚═╝          ╚═════ ╚═════╝   ╚═╝

{Fore.GREEN}{Style.NORMAL}          --Made By Hobin
{Fore.GREEN}{Style.NORMAL}Useage: 【*】http://www.example.com --scan
{Fore.GREEN}{Style.NORMAL}        【*】targets=urls.txt --scan  
{Fore.RESET}{Style.RESET_ALL}
"""
    print(banner)

def get_image_url(website_url):
    try:
        favicon_url = urljoin(website_url, '/favicon.ico')
        favicon_response = requests.get(favicon_url)
        if favicon_response.status_code == 200:
            return favicon_url
        
        response = requests.get(website_url)
        response.raise_for_status()  # 检查请求是否成功
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 尝试查找<link rel='icon'>或<link rel='shortcut icon'>
        icon_link = soup.find('link', rel='icon')
        if not icon_link:
            icon_link = soup.find('link', rel='shortcut icon')
        if icon_link and icon_link.get('href'):
            icon_url = urljoin(website_url, icon_link['href'])
            return icon_url
        
        img_tag = soup.find('img')
        if img_tag and img_tag.get('src'):
            img_url = urljoin(website_url, img_tag['src'])
            return img_url
    
        css_tag = soup.find('link', rel='stylesheet', href=True)
        if css_tag and css_tag.get('href'):
            css_url = urljoin(website_url, css_tag['href'])
            return css_url
            
        js_tag = soup.find('script', src=True)
        if js_tag and js_tag.get('src'):
            js_url = urljoin(website_url, js_tag['src'])
            return js_url

        return "网站中未找到可测试的图片资源！"

    except requests.RequestException as e:
        return f"An error occurred: {e}"

def scan_url(website_url):
    image_url = get_image_url(website_url)
    payload = image_url + "/xxxx.php"
    try:
        if requests.get(payload).status_code != 200:
            print(website_url + "\t\t\t\t【未发现漏洞】")
        else:
            print(Fore.RED + Style.BRIGHT + website_url + "\t\t【存在漏洞】")

    except requests.RequestException as e:
        print(Fore.RED + f"请求过程中出现错误：{e}" + Style.RESET_ALL)

def main():
    print_banner()
    inputer = input("Input > ")
    args = inputer.split(" ")

    if len(args) >= 2 and args[1].lower() == "--scan":
        if args[0].startswith("targets="):
            file_name = args[0].split("=")[1]
            try:
                with open(file_name, 'r') as file:
                    urls = file.readlines()
                    for url in urls:
                        scan_url(url.strip())
            except FileNotFoundError:
                print(Fore.RED + f"文件 {file_name} 未找到！" + Style.RESET_ALL)
        else:
            website_url = args[0]
            scan_url(website_url)
    else:
        print(Fore.RED + "命令错误，请重新输入！" + Style.RESET_ALL)

if __name__ == "__main__":
    main()
