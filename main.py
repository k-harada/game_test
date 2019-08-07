from flask import Flask, render_template, request
import othello
import os

app = Flask(__name__)


# init
@app.route('/')
def main():

    board = othello.create_init()

    return render_template('main.html', board=board, state=othello.judge(board))


@app.route('/change', methods=['POST'])
def change():

    hand = othello.tile_from_pic(request.form['hand'])  # hand

    board = [othello.tile_from_pic(pic) for pic in request.form.getlist('board')]

    new_board = othello.create_new_board(board, hand)

    return render_template('main.html', board=new_board, hand=hand, state=othello.judge(board))


local_test = False

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    if not local_test:
        app.run(host='0.0.0.0', port=port)
    else:
        app.run(host='127.0.0.1', port=port)
