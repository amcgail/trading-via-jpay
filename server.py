from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    from python import trade
    from cStringIO import StringIO

    return trade.printer.summaryCSV()

app.run( host='0.0.0.0', port=45373 )
