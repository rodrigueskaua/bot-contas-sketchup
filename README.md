# Bot de Criação de Contas SketchUp (Trimble)

Projeto Python parar automatizar a criação de contas no site da Trimble, permitindo utilizar o período gratuito de 7 dias do SketchUp. Utiliza e-mails temporários e navegação automatizada com Playwright.

## Requisitos

- Python 3.11
- pip
- Bibliotecas do projeto

## Instalação

Clone o repositório:

```bash
git clone https://github.com/rodrigueskaua/bot-contas-sketchup.git
cd bot-contas-sketchup
```

Crie um ambiente virtual (opcional):

```bash
python -m venv venv
venv\Scripts\activate     # Windows
# ou
source venv/bin/activate  # macOS/Linux
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Instale o navegador do Playwright:

```bash
python -m playwright install
```

## Execução

Para executar o bot, use:

```bash
python main.py
```