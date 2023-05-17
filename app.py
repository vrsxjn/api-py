from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

TOKENS_FILE = "tokens.txt"

def check_token(token):
    with open(TOKENS_FILE, "r") as f:
        lines = f.readlines()
        for line in lines:
            token_armazenado, expiration_date_str = line.strip().split(",")
            expiration_date = datetime.strptime(expiration_date_str, "%Y-%m-%d %H:%M:%S.%f")
            if token == token_armazenado:
                if datetime.now() <= expiration_date:
                    return True
                else:
                    lines.remove(line)
                    with open(TOKENS_FILE, "w") as f:
                        f.write("".join(lines))
                    return False
        return False

@app.route('/consultar', methods=['GET'])
def get_pessoa():
    token = request.args.get('token')
    id = request.args.get('id')

    if not check_token(token):
        return jsonify({'mensagem': 'Token inválido ou expirado'})

    conn = sqlite3.connect('./teste.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM DADOS WHERE ID = ?", (id,))
    pessoa = cursor.fetchone()

    if pessoa:
        result = {
          'data': {
            'informacao' : {
                'info': pessoa[0]
              }
            }
            }
        return jsonify(result)
    else:
        return jsonify({'mensagem': 'ID Inválido'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)