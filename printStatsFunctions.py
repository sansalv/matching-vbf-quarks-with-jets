def printRatios(npdf, col):
    #------------------------------------------------------------
    if 'Gen' in col:
        gen = True
    else:
        gen = False
        
    if 'eta' in col:
        eta = True
    else:
        eta = False
        
    if 'table' in col:
        det = True
    else:
        det = False
    #------------------------------------------------------------
    m = len(npdf[col])

    sum2 = 0
    sum1 = 0
    sum0 = 0

    for i in range(m):
        if npdf[col][i] == 2:
            sum2 += 1
        elif npdf[col][i] == 1:
            sum1 += 1
        elif npdf[col][i] == 0:
            sum0 += 1

    r2 = round(sum2/m, 3)
    r1 = round(sum1/m, 3)
    r0 = round(sum0/m, 3)
    
    if 'weak' in col:
        string = 'in weak match'
    elif 'strong' in col:
        string = 'and strong match'
    else:
        string = '# particles/event:\n\n'
        if det:
            if eta:
                string1 = '# particles/event with filter: detectable eta'
                string2 = '\n(|bGenPart_eta| < 5.1 && |bGenJet_eta| < 5.1)\n'
            elif gen:
                string1 = '# particles/event with filter: detectable GenJets'
                string2 = '\n(bGenPart_pT > 10)\n'
            else:
                string1 = '# particles/event with filter: detectable GenJets and Jets'
                string2 = '\n(|bGenPart_eta| < 5.1 && |bGenJet_eta| < 5.1 \n&& bGenPart_pT > 10 && bGenJet_pT > 15)'
            string = string1 + string2  
    print(string)
    print('= 2:  ' + str(r2))
    print('  1:  ' + str(r1))
    print('  0:  ' + str(r0))
#******************************************************************************************************
def printOverall(npdf, col, m_quarks, m_events, param):
    first = ('weak' not in col) and ('strong' not in col)
    #------------------------------------------------------------
    if 'weak' in col:
        string = 'in weak match'
    elif 'strong' in col:
        string = 'and strong match'
    #------------------------------------------------------------
    if 'table' in col:
        det = True
    else:
        det = False
    #------------------------------
    if 'eta' in col:
        eta = True
    else:
        eta = False
    #------------------------------
    if 'Gen' in col:
        gen = True
    else:
        gen = False
    #------------------------------------------------------------

    m = len(npdf[col])
    s = 0

    for i in range(m):
        if npdf[col][i] == 2:
            s += 2
        elif npdf[col][i] == 1:
            s += 1
    r=str(s)+'/'+str(m_quarks)
    if first:
        if det:
            print('\n# all filtered particles / # all particles\n= ' +str(s)+'/'+str(2*m_events)+ ' = ' +str(round(m_quarks/(2*m_events), 3)))
        else:
            print('\n# all particles\n= ' +str(m_quarks))
    else:
        print('')
        
        if det:
            filtered = ' (filtered)'
        else:
            filtered = ''
            
        if param != 0:
            print('# strong matched particles / # weak matched particles\n= ' + str(s)+'/'+str(param) + ' = ' +str(round(s/param, 3)))
            
        if 'weak' in col:
            print('# weak matched particles / # all' + filtered + ' particles\n= ' +r+ ' = ' +str(round(s/m_quarks, 3)))
        elif 'strong' in col:
            print('# strong matched particles / # all' + filtered + ' particles\n= ' +r+ ' = ' +str(round(s/m_quarks, 3)))
    
    return s
#******************************************************************************************************
def printStats(df, l):
    npdf = df.AsNumpy(l)
    first_col = npdf[l[0]]
    m_events = len(first_col)
    m_quarks = int(np.sum(first_col))
    print('-----------------------------------------------------------')
    print('Statistics of ' + str(m_events) + ' events with deltaRmax = '+str(deltaRmax)+':')
    print('-----------------------------------------------------------')
    for c in l:
        printRatios(npdf, c)
        if 'strong' not in c:
            s = printOverall(npdf, c, m_quarks, m_events, 0)
        else:
            s = printOverall(npdf, c, m_quarks, m_events, s)
        print('-----------------------------------------------------------')