# API RESTful com Python e Flask
_Publicando modelos de classificação de textos através de uma API_

## Instruções do Projeto

1. Clone o repositório e navegue até o diretório criado.

	```	
		git clone https://github.com/kennedysousa/flaskapi.git
		cd flaskapi
	```

2. Baixe e instale o [Anaconda](https://www.anaconda.com/download/)

3. Crie o ambiente virtual a instale os pacotes necessários.

    Com __conda__:
	```
		conda env create -f environment.yml
		source activate flaskapi
	```
    
    ou

    Com __pip__:
	```
		conda env create flaskapi
		source activate flaskapi
        pip install -r requirements.txt
	```

4. Se preferir, gere os certificados auto-assinados.

    Para __Linux__:
    ```
        openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
    ```

5. Inicie o servidor.

    Para __Linux__:
    ```
        gunicorn --certfile cert.pem --keyfile key.pem -b localhost:8080 server:app
    ```
    
    Para __Windows__:
    ```
        waitress-serve --listen=localhost:8080 server:app
    ```
