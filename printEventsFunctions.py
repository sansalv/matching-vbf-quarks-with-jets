import ROOT

def bJet_VBFC_match_VBFCList(event):

    j0 = bJet_coordinate[event][0]
    j1 = bJet_coordinate[event][1]
    
    v0 = VBFCandidates_coordinate[event][0]
    v1 = VBFCandidates_coordinate[event][1]
    
    if j0 == v1 or j1 == v0:
        vx = v1
        v1 = v0
        v0 = vx
        
    if v0 == j0 and v1 == j1:
        bJet_VBFC_match = [True, True]
    elif v0 == j0 and v1 != j1:
        bJet_VBFC_match = [True, False]
    elif v0 != j0 and v1 == j1:
        bJet_VBFC_match = [False, True]
    else:
        bJet_VBFC_match = [False, False]
        
    return bJet_VBFC_match, [v0, v1]

ROOT.gInterpreter.Declare("""

using namespace ROOT::VecOps;

const ROOT::RVec<RVec<std::size_t>> intRVec_to_intRVecRVec(const ROOT::RVec<std::size_t>& rvec){

    std::size_t N = rvec.size();
    RVec<RVec<std::size_t>> L(N);
    
    for(std::size_t i = 0; i < N; i++) {
    
        std::size_t n = rvec[i];
        
        std::size_t m = n;
        std::size_t s = 0;
        while (m > 0) {
            if(m%2 == 1){
                s++;
            }
            m = m/2;
        }
        
        RVec<std::size_t> l(s);
        std::size_t j = 0;
        std::size_t k = 0;
        m = n;
        while (m > 0) {
            if(m%2 == 1){
                l[k]=j;
                k++;
            }   
            m = m/2;
            j++;
        }

        L[i] = l;
    }

    return L;
};
""")
#******************************************************************************************************
def getPdgId(i):
    string = ''
    if (i in pdgIdDir) or (-i in pdgIdDir):
        if i < 0:
            string = string + 'anti_'
            i = - i
        string = string + pdgIdDir[i]
    else:
        string = str(i)
    return string
#******************************************************************************************************
def printIdxStuff(event, motherPathsQ, printIdxStatus, printCoordinateAndPt):
    print('-------------------------------------------')
    print('-------------------------------------------')
    print('Index paths:')
    for i in range(len(motherPathsQ[0])):
        print(motherPathsQ[0][i])
    for i in range(len(motherPathsQ[1])):
        print(motherPathsQ[1][i])
    print('-------------------------------------------')
    
    for q in motherPathsQ:
        for mp in q:
            lastIndex = mp[-1]
            print('-------------------------------------------')
            print(str(mp) + ':')
            print('Last index (' + str(lastIndex)+') stats:')
            print('pdgId:       ' + getPdgId(pdgList[event][lastIndex]))
            if printIdxStatus:
                print('status:      ' +  str(status[event][lastIndex]) + '\n' +
                      'statusFlags: ', end='')
                statusFlags_readable = [statusFlagsDir[flag] for flag in statusFlags[event][lastIndex]]
                print(statusFlags_readable)
            if printCoordinateAndPt:
                lastIdxCoordinates = coordinate[event][lastIndex]
                lastIdxCoordinates_round = (round(lastIdxCoordinates[0],2), round(lastIdxCoordinates[1],2),
                                            int(round(lastIdxCoordinates[2])))
                print('coordinates: ' + str(lastIdxCoordinates_round))
        print('-------------------------------------------')

        
def VBFC_match_print(Q, event, bJet_VBFC_match, VBFCandidates_coordinate_fixed, VBFCandidates_coordinate_round):
    
    if bJet_VBFC_match[Q]:
        print('| ===> RIGHT VBFC:   ' + str(VBFCandidates_coordinate_round[Q]))
        return [0]*10
    else:
        print('|')
        print('| ===> WRONG VBFC:   ' + str(VBFCandidates_coordinate_round[Q]))
        print('|')
        print('| The cause(s) of wrong VBFC (notice that one is already enough for incorrect match):')
        i = 1
        
        smallerPt, smallMjj, smallEta, bigEta, smallDeltaEta, jetIdWrong, puIdWrong, tooCloseHiggs, tooCloseMuon, tooCloseElectron = (0,)*10
        
        if bJet_pt[event][Q] < VBFCandidates_coordinate_fixed[Q][2]:
            smallerPt = 1
            print('|')
            print('| #' + str(i) + ': ', end='')
            print('bJet pT < VBFC pT:')
            i += 1
            print('|     ' + str(round(bJet_pt[event][Q], 1)) + ' < ' + str(round(VBFCandidates_coordinate_fixed[Q][2], 1)))
        #if bJet_pt[event][Q] <= 25:
        #    print('|')
        #    print('| #' + str(i) + ': ', end='')
        #    print('bJet pT <= 25:')
        #    i += 1
        #    print('|     ' + str(round(bJet_pt[event][Q])) + ' < 25')
        if bJet_mjj[event] <= 500:
            smallMjj = 1
            print('|')
            print('| #' + str(i) + ': ', end='')
            print('bJet mjj <= 500:')
            i += 1
            print('| bJet mjj:      ' + str(round(bJet_mjj[event])))
        if abs(bJet_eta[event][Q]) <= 1.5:
            smallEta = 1
            print('|')
            print('| #' + str(i) + ': ', end='')
            print('bJet |eta| <= 1.5:')
            i += 1
            print('|     bJet |eta|  = ' + str(round(abs(bJet_eta[event][Q]), 1)))
            print('|     VBFC |eta|  = ' + str(round(abs(VBFCandidates_coordinate_fixed[Q][0]), 1)))
        if abs(bJet_eta[event][Q]) >= 4.7:
            bigEta = 1
            print('|')
            print('| #' + str(i) + ': ', end='')
            print('bJet |eta| >= 4.7:')
            i += 1
            print('|     bJet |eta|  = ' + str(round(abs(bJet_eta[event][Q]), 1)))
            print('|     VBFC |eta|  = ' + str(round(abs(VBFCandidates_coordinate_fixed[Q][0]), 1)))
        if bJet_deltaEta[event] <= 4:
            smallDeltaEta = 1
            print('|')
            print('| #' + str(i) + ': ', end='')
            print('bJet |deltaEta| <= 4.0:')
            i += 1
            print('|     bJet |deltaEta|  = ' + str(round(bJet_deltaEta[event], 1)))
            print('|     VBFC |deltaEta|  = ' + str(round(abs(VBFCandidates_coordinate_fixed[0][0]-VBFCandidates_coordinate_fixed[1][0]), 1)))
        if not bJet_jetId[event][Q] & 2:
            jetIdWrong = 1
            print('|')
            print('| #' + str(i) + ': ', end='')
            print('bJet jetId != x1x:')
            i += 1
            jetId = "{0:b}".format(bJet_jetId[event][Q])
            jetId = '0'*(3-len(jetId)) + jetId
            print('|     bJet jetId  = ' + jetId)
        if (not bJet_puId[event][Q] & 2) and (bJet_pt[event][Q] <= 50):
            puIdWrong = 1
            print('|')
            print('| #' + str(i) + ': ', end='')
            print('(bJet puId != x1x) AND (bJet pT <= 50.0):')
            i += 1
            puId = "{0:b}".format(bJet_puId[event][Q])
            puId = '0'*(3-len(puId)) + puId
            print('|     (bJet puId  = ' + puId + ') AND (bJet pT  = ' + str(round(bJet_pt[event][Q], 1)) + ')')
        if bJet_closestHiggsCandidateDeltaR[event][Q] <= 1.2:
            tooCloseHiggs = 1
            print('|')
            print('| #' + str(i) + ': ', end='')
            print('bJet closestHiggsCandidateDeltaR <= 1.2:')
            i += 1
            print('|     bJet closestHiggsCandidateDeltaR  = '  + str(round(bJet_closestHiggsCandidateDeltaR[event][Q],1)))
        if bJet_closestMuonDeltaR[event][Q] <= 0.4:
            tooCloseMuon = 1
            print('|')
            print('| #' + str(i) + ': ', end='')
            print('bJet closestMuonDeltaR <= 0.4:')
            i += 1
            print('|     bJet closestMuonDeltaR  = '  + str(round(bJet_closestMuonDeltaR[event][Q],1)))
        if bJet_closestElectronDeltaR[event][Q] <= 0.4:
            tooCloseElectron = 1
            print('|')
            print('| #' + str(i) + ': ', end='')
            print('bJet closestElectronDeltaR <= 0.4:')
            i += 1
            print('|     bJet closestElectronDeltaR  = '  + str(round(bJet_closestElectronDeltaR[event][Q],1)))
        if i == 1:
            print('| ************ERROR:************')
            print('| ******************************')
            print('| The cause was not found... :-(')
            print('| ******************************')
            
        checkList = [smallerPt, smallMjj, smallEta, bigEta, smallDeltaEta, jetIdWrong, puIdWrong, tooCloseHiggs, tooCloseMuon, tooCloseElectron]
        
        return checkList
    
def printDecayConclusion(event, showVBFCandidates, initialQuarks, initialCoordinates_round, finalStuff, finalCoordinates_round,
                         printCoordinateAndPt):
    print('-------------------------------------------')
    print('Decay conclusion:\n')
    print(initialQuarks[0] + ' ---> ' + str(finalStuff[0]) + ' ---> ' + str(getPdgId(bGenPart_pdgId[event][0])))
    print(initialQuarks[1] + ' ---> ' + str(finalStuff[1]) + ' ---> ' + str(getPdgId(bGenPart_pdgId[event][1])))
    print('\nStatus info (quark[0], quark[1]):')
    print('Weak match:   ', end='')
    print(weakStatus[event])
    print('Strong match: ', end='')
    print(strongStatus[event])
    #******************************************************************************************************************************
    #---------------------------------------------------------------
    if showVBFCandidates:
        bJet_VBFC_match, VBFCandidates_coordinate_fixed = bJet_VBFC_match_VBFCList(event)
        bJet_VBFC_match_int = [int(b) for b in bJet_VBFC_match]
        print('VBFCandidate: ' + str(bJet_VBFC_match_int))
    #---------------------------------------------------------------
    #******************************************************************************************************************************
    if printCoordinateAndPt:
        print('-  -  -  -  -  -  -  -  -  -  -  -  -  -  -')
        
        bGenPart_coordinate_round = [(round(c[0],2), round(c[1],2), int(round(c[2]))) for c in bGenPart_coordinate[event]]
        bGenJet_coordinate_round = [(round(c[0],2), round(c[1],2), int(round(c[2]))) for c in bGenJet_coordinate[event]]
        bJet_coordinate_round = [(round(c[0],2), round(c[1],2), int(round(c[2]))) for c in bJet_coordinate[event]]
        
        #******************************************************************************************************************************
        #---------------------------------------------------------------
        if showVBFCandidates:
            VBFCandidates_coordinate_round = [(round(c[0],2), round(c[1],2), int(round(c[2]))) for c in VBFCandidates_coordinate_fixed]
            if VBFCandidates_coordinate_fixed[0] == VBFCandidates_coordinate[event][1]:
                VBFCandidates_mjjx = VBFCandidates_mjj[0]
                VBFCandidates_mjj[0] = VBFCandidates_mjj[1]
                VBFCandidates_mjj[1] = VBFCandidates_mjjx
        #---------------------------------------------------------------
        #******************************************************************************************************************************
        print('with coordinates:')
        print('')
        
        for Q in range(2):
            
            print('Quark[' + str(Q) + '] coordinates (eta, phi, pT):')
            print('| Final state quark: ' + str(initialCoordinates_round[Q])  + ', {pdgId: ' + initialQuarks[Q] + '}')
            if len(finalCoordinates_round[Q]) != 1:
                print('| Final GenParts:   ', end='')
                print(finalCoordinates_round[Q])
                #print(', {pdgId: ' + str(finalStuff[Q]) + '}')
            print('| ---> bGenPart:     ' + str(bGenPart_coordinate_round[Q]) + ', {pdgId: ' + str(getPdgId(bGenPart_pdgId[event][Q])) + '}')
            print('| ===> bGenJet:      ' + str(bGenJet_coordinate_round[Q]))
            print('| ===> bJet:         ' + str(bJet_coordinate_round[Q]))
            #******************************************************************************************************************************
            #---------------------------------------------------------------
            if showVBFCandidates:
                checkList = VBFC_match_print(Q, event, bJet_VBFC_match, VBFCandidates_coordinate_fixed, VBFCandidates_coordinate_round)
                print('')
            #---------------------------------------------------------------
            #******************************************************************************************************************************

        print('-  -  -  -  -  -  -  -  -  -  -  -  -  -  -')
        print('All GenJet coordinates:')
        GenJet_coordinate[event].sort(key = lambda a: a[2], reverse = True)
        GenJet_coordinates = GenJet_coordinate[event]
        GenJet_coordinates_round = [(round(c[0],2), round(c[1],2), int(round(c[2]))) for c in GenJet_coordinates]
        print(GenJet_coordinates_round)
            
        print('All Jet coordinates:')
        Jet_coordinate[event].sort(key = lambda a: a[2], reverse = True)
        Jet_coordinates = Jet_coordinate[event]
        Jet_coordinates_round = [(round(c[0],2), round(c[1],2), int(round(c[2]))) for c in Jet_coordinates]
        print(Jet_coordinates_round)
            
    print('-------------------------------------------')
    print('**************************************************************************************')
    return checkList

def printIfWanted(showVBFCandidates, onlyNotWeaks, onlyNotWeaks_and_bigPt, printShort, printIdx, printIdxStatus, printCoordinateAndPt,
                  event, motherPathsQ, initialQuarks, finalStuff, finalCoordinates_round):
    
    weakEvent = (nB_weak[event] == 2)
    if onlyNotWeaks:
        if weakEvent:
            return [0]*10
        elif onlyNotWeaks_and_bigPt:
            for q in range(2):
                if weakStatus[event][q] == 0 and bGenPart_coordinate[event][q][2] > 12:
                    break
                if q == 0:
                    continue
                else:
                    return [0]*10
    if printShort:
        print('Event ' + str(event) + ':')
    #-------------------------------------------------------------------------
    if printIdx or printCoordinateAndPt:
        print('-------------------------------------------')
        print('Final state quarks: ')
        print(initialQuarks)
    initialCoordinates = coordinate[event][4:6]
    initialCoordinates_round = [(round(c[0], 2), round(c[1], 2), int(round(c[2]))) for c in initialCoordinates]
    if printCoordinateAndPt and printIdx:
        print('-  -  -  -  -  -  -  -  -  -  -  -  -  -  -')
        print('with GenPart coordinates (eta, phi, pT):')
        print(initialCoordinates_round)
        
    #-------------------------------------------------------------------------
    if printIdx:
        printIdxStuff(event, motherPathsQ, printIdxStatus, printCoordinateAndPt)
    #-------------------------------------------------------------------------
    if printShort or printCoordinateAndPt or printIdx:
        checkList = printDecayConclusion(event, showVBFCandidates, initialQuarks, initialCoordinates_round, finalStuff, finalCoordinates_round,
                                           printCoordinateAndPt)
    return checkList
#******************************************************************************************************
def eventLoop(r, showVBFCandidates, onlyNotWeaks, onlyNotWeaks_and_bigPt, printShort, printIdx, printIdxStatus, printCoordinateAndPt):
    
    allFinalStuff = []
    allFinalStuff_anti = []
    
    overallList = [0]*10
    
    for event in r:
        #-------------------------------------------------------------------------
        initialQuarks = [getPdgId(pdgList[event][4]), getPdgId(pdgList[event][5])]
        finalStuff = [[], []]
        #-------------------------------------------------------------------------
        allMothers = []
        allF8MotherPaths = []
        motherPathsQ = [[], []]
        #-------------------------------------------------------------------------
        for i in range(nGenPart[event]-1, -1, -1):
            mother = idxMother[event][i]
            iMothers = []
            if i not in allMothers:
                while mother not in [0, -1]:
                    iMothers.append(mother)
                    allMothers.append(mother)
                    mother = idxMother[event][mother]

                l=([i]+iMothers)[::-1]
                if (len(iMothers) != 0) and (l[0] in [4, 5]):
                    allF8MotherPaths.append(l)
        #-------------------------------------------------------------------------
        allF8MotherPaths = sorted(allF8MotherPaths)
        finalCoordinates = [[], []]
        finalCoordinates_round = [[], []]
        #-------------------------------------------------------------------------
        for path in allF8MotherPaths:
            if path[0] == 4:
                idx = 0
            else:
                idx = 1
            
            motherPathsQ[idx].append(path)
            lastIndex = path[-1]
            
            pdgid = getPdgId(pdgList[event][lastIndex])
            finalStuff[idx].append(pdgid)
            
            coordinate0 = coordinate[event][lastIndex]
            coordinate0_round = (round(coordinate0[0],2), round(coordinate0[1],2), int(round(coordinate0[2])))
            finalCoordinates[idx].append(coordinate0)
            finalCoordinates_round[idx].append(coordinate0_round)
            #-------------------------------------------------------------------------
            # sort by pT
            sortedZip = sorted(zip(finalCoordinates[idx], finalStuff[idx]), key=lambda coord: coord[0][2], reverse = True)
            finalStuff[idx] = [x for _,x in sortedZip]

            finalCoordinates[idx].sort(key = lambda coord: coord[2], reverse = True)
            finalCoordinates_round[idx].sort(key = lambda coord: coord[2], reverse = True)
            #-------------------------------------------------------------------------
            if pdgid not in (allFinalStuff+allFinalStuff_anti):
                if 'anti' in pdgid:
                    allFinalStuff_anti.append(pdgid)
                else:
                    allFinalStuff.append(pdgid)
                    
        motherPathsQ[0].sort(key=len)
        motherPathsQ[1].sort(key=len)
        
        # PRINT STUFF
        checkList = printIfWanted(showVBFCandidates, onlyNotWeaks, onlyNotWeaks_and_bigPt, printShort, printIdx, printIdxStatus, printCoordinateAndPt,
                      event, motherPathsQ, initialQuarks, finalStuff, finalCoordinates_round)
        #print(str(type(checkList)))
        overallList = [x + y for x, y in zip(checkList, overallList)]
        # PRINT STUFF
        
    return allFinalStuff, allFinalStuff_anti, overallList
#******************************************************************************************************
def printEvents(r, showVBFCandidates, onlyNotWeaks, onlyNotWeaks_and_bigPt, printShort, printIdx, printIdxStatus, printCoordinateAndPt):
    print('**************************************************************************************')
    if showVBFCandidates:
        print('Filters:')
        print('mjj > 500 GeV                                                    || sum of both Jets invariant masses > 500 GeV')
        print('1.5 < |eta| < 4.7')
        print('|deltaEta| > 4.0')
        print('jetId == x1x                                                     || bit2 is tight')
        print('(puId == x1x) OR (pT > 50.0 GeV)                                 || puId = Pilup ID flags with 80X (2016) training')
        print('no electrons, muons or Higgs jets nearby (deltaR > 0.4)')
        print('---> choose two biggest Jets')
        print('**************************************************************************************')
    if type(r) == tuple:
        r = range(r[0], r[1])
    elif type(r) == list:
        r = r
    else:
        r = range(r) 
        
    # Event loop starts-------------------------------------------------------------------------
    allFinalStuff, allFinalStuff_anti, overallList = eventLoop(r, showVBFCandidates, onlyNotWeaks, onlyNotWeaks_and_bigPt, printShort, printIdx,
                                                               printIdxStatus, printCoordinateAndPt)
    # Event loop ends -------------------------------------------------------------------------
    print('overallList = [smallerPt, smallMjj, smallEta, bigEta, smallDeltaEta, jetIdWrong, puIdWrong, tooCloseHiggs, tooCloseMuon, tooCloseElectron]:')
    print('overallList = ' + str(overallList))
    print('-------------------------------------------')
    print('All ' + str(len(allFinalStuff)) + ' final particles:')
    print(sorted(allFinalStuff, key=len))
    print('-------------------------------------------')
    print('All ' + str(len(allFinalStuff_anti)) + ' final anti-particles:')
    print(sorted(allFinalStuff_anti, key=len))
    print('-------------------------------------------')
    
    print('**************************************************************************************')