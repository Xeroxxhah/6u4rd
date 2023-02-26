from core.mail import EmailSender
from pyngrok import ngrok 
from core.portal import App
from time import sleep




app = App()

def send_ngrok_link(ngrok_link):    
    ngrok_tunnel_url = f"ngrok url: {ngrok_link}"
    mailer = EmailSender()
    mailer.send_email('ngrok url 6u4rd', ngrok_tunnel_url)

def main():
    while True:
        if len(ngrok.get_tunnels()) == 0:
            ngrok.connect(app.port)
            send_ngrok_link(ngrok.get_tunnels()[0])
            sleep(3600)
            ngrok.kill()


if __name__ == '__main__':
    sleep(60)
    main()
    