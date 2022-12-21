from flask_line import app, db


def prologue():
    from models import StockInfo
    StockInfo.upgrade()


if __name__ == "__main__":
    db.create_all()
    prologue()
    app.run(host='0.0.0.0', port=5000)
