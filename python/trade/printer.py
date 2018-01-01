from python.trade import trader


class Indenter:
    def __init__(self, preIndentChar=".", postIndentChar=""):
        self.preIndentChar = preIndentChar
        self.postIndentChar = postIndentChar
        self.indentLevel = 0

    def __call__(self, string):
        lines = string.split("\n")
        indentedLines = [
            self.preIndentChar * self.indentLevel + " "
            + line
            + " " + self.postIndentChar * self.indentLevel
            for line in lines
            ]
        return "\n".join(indentedLines)

    def indent(self, s):
        self.indentLevel += 1

    def unindent(self, s):
        self.indentLevel -= 1


class DivIndenter(Indenter):
    def __init__(self, divClassName="indent"):
        Indenter.__init__(
            self,
            preIndentChar="<div class='%s'>" % divClassName,
            postIndentChar="</div>"
        )


def summary():
    import asciitable
    import os, json
    for fund in os.listdir("funds"):
        print "-%s" % fund
        stuff = json.loads(open("funds/%s" % fund).read())

        def getPrice(ticker):
            if ticker == '__CASH__':
                return 1

            data = trader.getDaysData(ticker)
            return float(data[-1].split(",")[2])

        def getVal(ticker, amt):
            try:
                price = getPrice(ticker)
                value = round(amt * price, 2)
                return value
            except:
                return 0

        def formatDollars(x):
            if x <= 0:
                return "--"

            intPart = str(int(x))
            intPart = [ intPart[max(0,i-3):i] for i in range(len(intPart), 0, -3)]
            intPart = ",".join( reversed(intPart) )
            centsPart = str( int( round( 100*(x - int(x)) ) ) )
            return "$%s.%s" % (intPart, centsPart)

        tickers = stuff.keys()
        # filter those which we don't own any of
        tickers = [x for x in tickers if stuff[x] != 0]
        # sort them
        tickers = sorted(tickers)

        myAmt = [stuff[t] for t in tickers]
        currentValue = [ getVal(t, stuff[t]) for t in tickers ]
        formattedCurrentValue = map(formatDollars, currentValue)
        prices = map(getPrice, tickers)

        asciitable.write({"OF": tickers, "I OWN": myAmt, "PRICE":prices, "VALUE":formattedCurrentValue}, Writer=asciitable.FixedWidth)
        print "TOTAL EQUITY: %s" % formatDollars(sum(currentValue))

def summaryCSV():
    csv = u""

    csv += "OF,OWN,PRICE,VALUE\n"

    import os, json
    for fund in os.listdir("funds"):
        print "-%s" % fund
        stuff = json.loads(open("funds/%s" % fund).read())

        def getPrice(ticker):
            if ticker == '__CASH__':
                return 1

            data = trader.getDaysData(ticker)
            return float(data[-1].split(",")[2])

        def getVal(ticker, amt):
            try:
                price = getPrice(ticker)
                value = round(amt * price, 2)
                return value
            except:
                return 0

        def formatDollars(x):
            if x <= 0:
                return "--"

            intPart = str(int(x))
            intPart = [ intPart[max(0,i-3):i] for i in range(len(intPart), 0, -3)]
            intPart = ",".join( reversed(intPart) )
            centsPart = str( int( round( 100*(x - int(x)) ) ) )
            return "$%s.%s" % (intPart, centsPart)

        tickers = stuff.keys()
        # filter those which we don't own any of
        tickers = [x for x in tickers if stuff[x] != 0]
        # sort them
        tickers = sorted(tickers)

        myAmt = [stuff[t] for t in tickers]
        currentValue = [ getVal(t, stuff[t]) for t in tickers ]
        formattedCurrentValue = map(formatDollars, currentValue)
        prices = map(getPrice, tickers)

        for i, x in enumerate(tickers):
            csv += "%s,%s,%s,%s\n" % (tickers[i], myAmt[i], prices[i], currentValue[i])

        print "TOTAL EQUITY: %s" % formatDollars(sum(currentValue))

    return csv
