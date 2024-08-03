# Jogo da cobrinha

Este projeto é sobre uma variação do jogo da cobrinha, com adição de perda de pontos e necessidade de executar contas matemáticas rapidamente.

## Instalação
Após clonar o repositório na sua máquina será necessário executar comandos no terminal, começe criando um ambiente virtual usando:
```bash
python -m venv venv
```
Se a política de ativação do ambiente virtual estiver bloquada use:
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Após isso, ative o ambiente virtual.

```bash
venv/Scripts/activate
```
Com o ambiente virtual ativo, baixe as dependências com:
```bash
pip install -r requirements.txt
```

Com isso, o projeto pode ser executado, caso tenha algum problema nos passos acima, leia: [Creation of virtual environments](https://docs.python.org/pt-br/3/library/venv.html)
## Uso

```bash
python main.py
```