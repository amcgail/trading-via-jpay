import python.trade.printer
import trade

if __name__ == '__main__':

    mark_for_deletion = []

    import sys

    file_to_process = sys.argv[1]

    import json
    trades = json.loads( open( file_to_process ).read() )

    doit = False
    if doit:
        for s in trades:
            s = "\n".join( s )
            ind = trade.printer.Indenter()
            print ind("Executing '''%s'''" % s.replace("\n","~"))
            trade.parse.executeCommand(s, 0, s)

    print "SUMMARY OF PORTFOLIOS"
    python.trade.printer.summary()

    '''
    for s in mark_for_deletion:
        del standing_trades[s]

    open( "standing_trades.json",'wb' ).write( json.dumps( standing_trades ) )
    '''