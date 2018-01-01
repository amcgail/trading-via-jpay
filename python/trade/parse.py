import os

def unindent(s):
    ss = s.split("\n")
    ss = [x[1:] for x in ss]
    ss = "\n".join(ss)
    return ss

import trader

def executeCommand(x, t, s=-1):
    global mark_for_deletion
    global fund_I_last_used
    global ind
    ind.indent()

    x1 = x.split("\n")[0].strip()

    if x1 == "":
        print ind("(empty command). doing nothing")
        ind.unindent()
        return

    cmds = x1.split(" ")
    cmds = filter(lambda z: z != "", cmds)

    if x1[:7] == "ACTION ":
        fundname = x1[7:]
        print "Switching to fund %s" % fundname
        fund_I_last_used = fundname
    if x1[:8] == "ACTIONS ":
        fundname = x1[8:]
        print "Switching to fund %s" % fundname
        fund_I_last_used = fundname

    if x1[:10] == "CREATEFUND":
        newfund_name = x1[11:]
        fund_fn = "funds/%s" % newfund_name
        if os.path.exists(fund_fn):
            print ind("Fund %s already exists." % newfund_name)
        else:
            print ind("Fund %s doesn't exist. Creating." % newfund_name)
            open(fund_fn, 'wb').write("{}")

        fund_I_last_used = newfund_name

    if x1[:6] == "ATOPEN" or x1[:7] == "AT OPEN":
        print ind("Executing following commands at open")
        for nextcommand in x.split("\n")[1:]:
            executeCommand(unindent(nextcommand), 0)

    if x1[:7] == "ADDCASH":
        args = x1.split(" ")
        args = filter(lambda z: z != "", args)
        if len(args) == 2:
            try:
                amt = int(args[1])
            except:
                raise Exception("ADDCASH argument must be an integer")
        else:
            raise Exception("not 2 arguments on ADDCASH?")

        if fund_I_last_used is None:
            raise Exception("ADDCASH knows not what fund to use!")

        print ind("Trying to add %d CASH to %s" % (amt, fund_I_last_used))
        trader.addCash(fund_I_last_used, amt)

    if cmds[0] == "AT" or cmds[0] == "IF":
        # print ".. IF/AT statement detected"

        x1_blah = x1[2:]
        tickr = ""
        while len(x1_blah) > 0 and x1_blah[0] not in [">", "<"]:
            tickr += x1_blah[0]
            x1_blah = x1_blah[1:]

        op = x1_blah[0]
        num = x1_blah[1:]

        tickr = tickr.strip()
        op = op.strip()
        num = num.strip()

        # print ".. IF/AT statement interpretation: buy %s when %s than %s" %(tickr, op, num)

        data = trader.getDaysData(tickr)

        for row in data:
            cols = row.split(",")
            price = float(cols[1])

            if op == ">" and price > float(num):
                print ind("Executed@%s:" % price)
                executeCommand(unindent("\n".join(x.split("\n")[1:])), int(cols[0]))
                if s >= 0:
                    mark_for_deletion.append(s)
                ind = ind[1:]
                return

            if op == "<" and price < float(num):
                print ind("Executed@%s:" % price)
                executeCommand(unindent("\n".join(x.split("\n")[1:])), int(cols[0]))
                if s >= 0:
                    mark_for_deletion.append(s)
                ind = ind[1:]
                return

        print "... Not executed"

    elif cmds[0] == "BUY":
        tickr = cmds[1]
        amt = int(cmds[2])

        print ind("Buying %s of %s" % (amt, tickr))
        trader.buyAtTime(tickr, amt, t)
        pass

    elif cmds[0] == "SELL":
        if len(cmds) == 2:
            tickr = cmds[1]
            print ind("Selling ALL of %s" % (tickr))
            trader.sellAtTime(tickr, None, t)
        elif len(cmds) == 3:

            if cmds[1] == 'ALL':
                tickr = cmds[2]
                print ind("Selling ALL of %s" % (tickr))
                trader.sellAtTime(tickr, None, t)
            else:
                try:
                    amt = int(cmds[1])
                    tickr = cmds[2]
                except:
                    amt = int(cmds[2])
                    tickr = cmds[1]

                print ind("Selling %s of %s" % (amt, tickr))
                trader.sellAtTime(tickr, amt, t)
        pass

    elif cmds[0] == "RETRACT":
        pass

    ind = ind[1:]