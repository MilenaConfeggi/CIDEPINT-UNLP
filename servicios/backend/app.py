from administracion.src.web import create_app
import os
app = create_app()

if __name__ == "__main__":
    #app.run(ssl_context=("/etc/letsencrypt/live/api.servicios.cidepint.com/fullchain.pem",
    #                     "/etc/letsencrypt/live/api.servicios.cidepint.com/privkey.pem"), port=8000)
    os.chdir('/home/cidepint/CIDEPINT-UNLP')
    app.run()
