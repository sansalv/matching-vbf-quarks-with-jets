import ROOT
from ROOT import TLine

#******************************************************************************************************
# Returns histogram from dataset and previous variable list index (i) variable
# Uses global variables columnList and nameList

def histo0(df, i, names, cols):
    #--------------------------------------------------------------------
    minim = min(0, df.Min(names[i]).GetValue())
    for k in [0, -3, 4, -10, -30, -150, -150, -600, -5000, -3000, -30000, -40000]:
        if k <= minim:
            minim = k
            break
    maxim = round(df.Max(names[i]).GetValue()+1, 1)
    for m in [3, 4, 10, 30, 100, 150, 600, 3000, 5000, 30000, 40000]:
        if maxim <= m:
            maxim = m
            break
    if 'pdgId' in names[i]:
        minim = -40
        maxim = 40
    #--------------------------------------------------------------------    
    bins=60
    # Discrete cases:
    if (('nGen' in names[i]) or ('nJet' in names[i]) or ('pdgId' in names[i])):
        bins=int(maxim - minim)
    if 'eta' in names[i]:
        bins=2*bins
    #--------------------------------------------------------------------
    h_i = df.Histo1D(('h'+str(i),names[i] +';'+names[i]+';Simulated events', bins, minim, maxim), cols[i])
    h_i.SetFillColor(30)
    #h_i = df.Histo1D(("h"+str(i),names0[i]+";"+ x +";Simulated events", bins, minim, maxim), columns0[i])
    #h_i = df.Histo1D(("h"+str(i),names0[i]+";"+ x +";Simulated events", bins, minim, maxim), columns0[i])
    #--------------------------------------------------------------------
    return h_i
#******************************************************************************************************
# Returns canvas from a histogram (index to name the canvas)

def canvas0(h, i, param):
    #--------------------------------------------------------------------
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetTextFont(42)
    c = ROOT.TCanvas("c"+str(i), "", 400, 300)
    if 'log' in param:
        c.SetLogy()
    #--------------------------------------------------------------------
    h.SetTitle("")
    h.GetXaxis().SetTitleSize(0.04)
    h.GetYaxis().SetTitleSize(0.04)
    h.SetLineWidth(2)
    h.Draw()
    #--------------------------------------------------------------------
    label = ROOT.TLatex(); label.SetNDC(True)
    label.SetTextSize(0.040); label.DrawLatex(0.100, 0.920, "#bf{CMS} #it{Simulation}")
    label.SetTextSize(0.030); label.DrawLatex(0.829, 0.920, "13 TeV")
    #--------------------------------------------------------------------
    return c
#******************************************************************************************************
# Prints a pdf file from the variable list histograms (using histo0 and canvas0 methods)

def printPdf(df, filename, names, cols, param):
    n = len(cols)
    print(n)
    filename = filename + '_' + param + '.pdf'
    for i in range(n):
        print(i)
        h = histo0(df, i, names, cols)
        c = canvas0(h, i, param)
        if i == 0 and n != 1:
            c.Print(filename+"(","pdf")
        elif i != n-1:
            c.Print(filename,"pdf")
        else:
            c.Print(filename+")","pdf")
#******************************************************************************************************          
# Returns a histogram with filtered status and PdgId numbers
# Parameter s filters to initial (s='I') and final states (s='F'). s=0 if no status-filtering
# Parameter l is a list of PdgId numbers

# columns0 = LHEcols

def histoAdd(df, i, s, l, names, columns):
    #--------------------------------------------------------------------
    df_i = df.Define(names[i], columns[i])
    #--------------------------------------------------------------------
    minim = min(0,df_i.Min(names[i]).GetValue())
    if minim < 0:
        minim = round(minim-2,1)
    maxim = df_i.Max(names[i]).GetValue()
    for m in [2, 10, 30, 600, 3000]:
        if maxim <= m:
            maxim = m
            break
    #------------------------------------------- Special case (outliers): 
    if 'mass' in names[i]:
        minim = 0
        maxim = 0.02
    #--------------------------------------------------------------------
    bins = 60
    # Discrete cases:
    discretes = ['status', 'pdgId', 'nGenJet', 'nJet']
    if any(elem in names[i] for elem in discretes):
        if 'status' in names[i]:
            minim=-maxim
        bins = int(maxim-minim)
    #--------------------------------------------------------------------
    h_i = df_i.Histo1D(("h" + str(i), "h" + str(i) + ";" + names[i] + ";Simulated events", bins, minim, maxim), names[i])
    #--------------------------------------------------------------------
    return h_i
#******************************************************************************************************
# Prints a pdf file from the variable list 2 histograms (using histoAdd and canvas0 methods)

def printPdfAdd(df, filename, s, l, columns0, param):
    n = len(columns0)
    names, columns = makeLists(s, l, columns0)
    print(names)
    filename = filename + str(s) + str(len(l)) + '_' + param + '.pdf'
    for i in range(n):
        h = histoAdd(df, i, s, l, names, columns)
        c = canvas0(h, i, param)
        if i == 0:
            c.Print(filename+"(","pdf")
        elif 0 < i < n-1:
            c.Print(filename,"pdf")
        elif i == n-1:
            c.Print(filename+")","pdf")        
#******************************************************************************************************
def returnMinMaxBins(x, param):
    if 'test' not in param:
        minim = 0
        maxim = 8
        bins = 50

        #--------------------------------------------------------------------
        # Variable recognition:

        eta = '\eta' in x
        phi = '\phi' in x
        pt = 'p_{T' in x
        pdgId = 'pdgId' in x
        deltaR = '\Delta R' in x
        count = any(elem in x for elem in ['/event', 'pdgId'])

        division = '/' in x
        delta = '\Delta' in x
        abs1 = '|' in x
        abs2 = '||' in x
        q1 = 'Q1' in x

        # Parameter recognition:
        log = 'log' in param
        zoom = 'zoom' in param
        big = 'big' in param
        viljaFiltered = 'vilja' in param
        #--------------------------------------------------------------------
        # Individual quark case:
        if not q1:
            bins = 50
            if eta:
                if (not abs1):
                    minim = -maxim
                    bins = bins*2
                if abs1 and delta:
                    if zoom:
                        maxim = 0.5
                    elif log:
                        bins = 80
            elif phi:
                maxim = 4
                if (not abs1):
                    minim = -maxim
                if abs1 and delta:
                    if zoom:
                        bins = 50
                        maxim = 0.5
            elif pt:
                bins = 80
                maxim = 2400
                if zoom:
                    bins = 80
                    maxim = 400
                    if delta:
                        bins = 75
                        minim = -50
                        maxim = 100
                    if division:
                        bins = 75
                        minim = -1
                        maxim = 2
                elif delta:
                    bins = 70
                    minim = -400
                    maxim = 2400
                    if division:
                        bins = 80
                        minim = -2
                        maxim = 14
            elif pdgId:
                if zoom:
                    minim = -15
                    maxim = 25
                    bins = 40
            elif deltaR:
                bins = 40
                if zoom:
                    bins = 50
                    maxim = 0.5
            elif count:
                maxim = 220
                
        #--------------------------------------------------------------------
        # Q1 vs. Q2 case:
        else:
            if eta:
                bins = 40
                if delta:
                    bins = 24
                    maxim = 12
                    if abs2:
                        maxim = int(maxim/2)
            elif phi:
                bins = 48
                maxim = 4
                if (not abs1):
                    minim = -maxim
            elif pt:
                bins = 50
                maxim = 500
                if division:
                    maxim = 5
                    if 'rel' in x:
                        bins = 20
                        maxim = 1
                elif delta and abs1:
                    maxim = 250
        #--------------------------------------------------------------------
        # Special cases:
        if big:
            bins = bins*4
        if param.isdigit():
            if param != '0':
                maxim = int(param)
        if 'rough' in param:
            bins = int(bins/2)
        #--------------------------------------------------------------------
        # Discrete cases:
        if count:
            bins = int(maxim-minim)
        #--------------------------------------------------------------------
    else:
        minim=4
        maxim=5.1
        bins=30
    #--------------------------------------------------------------------
    return minim, maxim, bins
#******************************************************************************************************
def histoEx(df, i, columns0, names0, x, param):
    #--------------------------------------------------------------------
    minim, maxim, bins = returnMinMaxBins(x, param)
    col = columns0[i]
    
    #gen = 'gen' in param
    #jet = 'jet' in param
    #if gen:
    #    col = columns0[i] + '_genDet'
    #elif jet:
    #    col = columns0[i] + '_jetDet'
    #else:
    #    col = columns0[i]
    
    #--------------------------------------------------------------------
    h_i = df.Histo1D(('h'+str(i),names0[i]+';'+ x +';Simulated events', bins, minim, maxim), col)
    print(h_i.Integral())
    #--------------------------------------------------------------------
    return h_i
#******************************************************************************************************
#Prints pdf to file with multiple histograms (columns0)

def PrintPdfMultiple(df, filename, columns0, names0, x, j, colors, ymax0, param):
    #------------------------------------------------------------------------------------------------------
    n=len(columns0)
    filename += '.pdf'
    #------------------------------------------------------------------------------------------------------
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetTextFont(42)
    ROOT.gStyle.SetOptTitle(0)
    c = ROOT.TCanvas("c", "", 400, 300)
    if 'log' in param:
        c.SetLogy()
    #------------------------------------------------------------------------------------------------------
    if colors == 'blue':
        colors=[4]
    elif colors == 'green':
        colors = [ROOT.kGreen+1]
    elif colors == 'pink':
        colors = [6]
    #------------------------------------------------------------------------------------------------------
    hs=[]
    if 'rough' in param:
        ymax0 = ymax0*2
    for i in range(n):
        hs.append(histoEx(df, i, columns0, names0, x, param))
        hs[i].GetXaxis().SetTitleSize(0.04)
        hs[i].GetYaxis().SetTitleSize(0.04)
        if ymax0 != 0:
            if allData or bigData:
                ymax = ymax0*4
                if 'pdgId' in x:
                    ymax = ymax0*8
            else:
                ymax = ymax0
            hs[i].GetYaxis().SetRangeUser(0.5,ymax)
        hs[i].SetLineWidth(2)
        hs[i].SetLineColor(colors[i])
        if i == 0:
            hs[i].Draw()
        else:
            hs[i].Draw('same')
    #------------------------------------------------------------------------------------------------------
    # OLD LEGENDS:
    if n == 1:
        ROOT.gPad.BuildLegend(0.55,0.85,0.9,0.9)
    elif n == 2:
        ROOT.gPad.BuildLegend(0.55,0.82,0.9,0.9)     
    elif n==3:
        ROOT.gPad.BuildLegend(0.59,0.78,0.9,0.9)
    else:
        if 'middle' in param:
            ROOT.gPad.BuildLegend(0.35,0.1,0.65,0.26)
            #myline = TLine(0,100,0,ymax)
            #myline.Draw("same")
        else:
            ROOT.gPad.BuildLegend(0.59,0.68,0.9,0.9)
        
    if ('|' not in x) and ('middle' not in param):
        myline = TLine(0,0,0,ymax0)
        myline.Draw('same')
    #------------------------------------------------------------------------------------------------------
    label = ROOT.TLatex(); label.SetNDC(True)
    label.SetTextSize(0.040); label.DrawLatex(0.100, 0.920, '#bf{CMS} #it{Simulation}')
    label.SetTextSize(0.030); label.DrawLatex(0.829, 0.920, '13 TeV')
    #------------------------------------------------------------------------------------------------------
    if j == 0:
        c.Print(filename+'(','pdf')
    elif j == 1:
        c.Print(filename,'pdf')
    elif j == 2:
        c.Print(filename+')','pdf')
        
# Example of use:
# 'deltaR_b'
#-------------------------------------------------
#df = df0
#p = 'b'
#if WW:
#    if WW_ll:
#        p += '_WWll'
#    elif WW_tt:
#        p += '_WWtt'
#if allData or bigData:
#    p += '_big'
#name = 'deltaR_'+p
#print(name)
#-------------------------------------------------
#PrintPdfMultiple(df, name, ['bGenJet_deltaR', 'bJet_deltaR'],
#                 ['Weak match', 'Strong match'], '\Delta R', 0, [2,ROOT.kGreen+2], 4000, 'lin_zoom'+p)
#
#PrintPdfMultiple(df, name, ['bGenJet_deltaR','bJet_deltaR'],
#                 ['Weak match', 'Strong match'], '\Delta R', 2, [2,ROOT.kGreen+2], 25000, 'log'+p)