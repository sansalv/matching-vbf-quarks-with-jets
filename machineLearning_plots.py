# Scatter plots for different variables
# *****************************************
# (DeltaEta, mjj)

X = pddf_s.iloc[:,1:7]
y = pddf_s.iloc[:,7]
y2 = pddf_s.iloc[:,8]

plt.figure(figsize = (6,6))
plt.scatter(X['DeltaEta'], X['Mjj'], s=10, c='gray', alpha=0.05, label='JetPair')
plt.scatter(X['DeltaEta'][y == 1], X['Mjj'][y == 1], s=10, c='blue', alpha=0.7, label='Strong JetPair')
if viljaFiltered:
    plt.title('Strong JetPairs vs. VBFC JetPairs', fontsize=16)
    plt.scatter(X['DeltaEta'][y2 == 1][y == 1], X['Mjj'][y2 == 1][y == 1], s=10, c='green', alpha=0.7, label='Right VBFC JetPair')
    plt.scatter(X['DeltaEta'][y2 == 1][y == 0], X['Mjj'][y2 == 1][y == 0], s=10, c='red', alpha=0.7, label='Wrong VBFC JetPair')
else:
    plt.title('Strong JetPairs vs. all JetPairs', fontsize=16)
plt.xlabel('DeltaEta', fontsize=14)
plt.ylabel('Mjj', fontsize=14)
plt.xlim(0)
plt.ylim(0)
plt.grid(alpha=0.5)
plt.axvline(x=4, ymin=0, ymax=6000, c='black')
plt.axhline(y=500, xmin=0, xmax=12, c='black')

leg = plt.legend()
for lh in leg.legendHandles: 
    lh.set_alpha(1)

plt.show()
# *****************************************
# (pT[0], pT[1])

X = pddf_s.iloc[:,1:7]
y = pddf_s.iloc[:,7]
y2 = pddf_s.iloc[:,8]

plt.figure(figsize = (6,6))
plt.scatter(X['Pt0'], X['Pt1'], s=5, c='gray', alpha=0.1, label='JetPair')
plt.scatter(X['Pt0'][y == 1], X['Pt1'][y == 1], s=5, c='blue', alpha=0.5, label='Strong JetPair')
if viljaFiltered:
    plt.title('Strong vs. VBFC JetPair pTs', fontsize=16)
    plt.scatter(X['Pt0'][y2 == 1][y == 1], X['Pt1'][y2 == 1][y == 1], s=5, c='green', label='Right VBFC JetPair')
    plt.scatter(X['Pt0'][y2 == 1][y == 0], X['Pt1'][y2 == 1][y == 0], s=5, c='red', label='Wrong VBFC JetPair')
plt.title('Strong vs. all JetPair pTs', fontsize=16)
plt.ylim(0)
plt.xlim(0)
plt.xlabel('Pt0', fontsize=14)
plt.ylabel('Pt1', fontsize=14)
plt.grid(alpha=0.5)

leg = plt.legend()
for lh in leg.legendHandles: 
    lh.set_alpha(1)

plt.show()
# *****************************************
# (eta[0], eta[1])

X = pddf_s.iloc[:,1:7]
y = pddf_s.iloc[:,7]

plt.figure(figsize = (6,6))
plt.scatter(X['Eta0'], X['Eta1'], s=10, c='gray', alpha=0.05, label='JetPair')
plt.scatter(X['Eta0'][y == 1], X['Eta1'][y == 1], s=10, c='blue', alpha=0.3, label='Strong JetPair')
if viljaFiltered:
    plt.title('Strong vs. VBFC JetPair etas', fontsize=16)
    plt.scatter(X['Eta0'][y2 == 1][y == 1], X['Eta1'][y2 == 1][y == 1], s=10, c='green', alpha=0.5, label='Right VBFC JetPair')
    plt.scatter(X['Eta0'][y2 == 1][y == 0], X['Eta1'][y2 == 1][y == 0], s=10, c='red', alpha=0.5, label='Wrong VBFC JetPair')
else:
    plt.title('Strong vs. all JetPair etas', fontsize=16)

plt.xlabel('Eta0', fontsize=14)
plt.ylabel('Eta1', fontsize=14)

plt.vlines(x=-4.7, ymin=1.2, ymax=4.7, color='black')
plt.vlines(x=-1.2, ymin=1.2, ymax=4.7, color='black')
plt.vlines(x=1.2, ymin=-4.7, ymax=-1.2, color='black')
plt.vlines(x=4.7, ymin=-4.7, ymax=-1.2, color='black')

plt.hlines(y=-4.7, xmin=1.2, xmax=4.7, color='black')
plt.hlines(y=-1.2, xmin=1.2, xmax=4.7, color='black')
plt.hlines(y=1.2, xmin=-4.7, xmax=-1.2, color='black')
plt.hlines(y=4.7, xmin=-4.7, xmax=-1.2, color='black')

plt.grid(alpha=0.5)

leg = plt.legend()
for lh in leg.legendHandles: 
    lh.set_alpha(1)

plt.show()
# *****************************************
# principal components for "optimal" 2D projection visualization

pca = PCA(n_components=2)
principalComponents = pca.fit_transform(X)
principalX = pd.DataFrame(data = principalComponents, columns = ['principal component 1', 'principal component 2'])

plt.figure(figsize = (6,6))
plt.scatter(principalX.iloc[:,0], principalX.iloc[:,1], s=10, c='gray', alpha=0.05, label='JetPair')
plt.scatter(principalX.iloc[:,0][y == 1], principalX.iloc[:,1][y == 1], s=10, c='blue', alpha=0.4, label='Strong JetPair')
plt.title('Two-dimensional feature data after PCA', fontsize=16)
if viljaFiltered:
    plt.scatter(principalX.iloc[:,0][y2 == 1][y == 1], principalX.iloc[:,1][y2 == 1][y == 1], s=10, c='green', alpha=0.6, label='Right VBFC JetPair')
    plt.scatter(principalX.iloc[:,0][y2 == 1][y == 0], principalX.iloc[:,1][y2 == 1][y == 0], s=10, c='red', alpha=0.6, label='Wrong VBFC JetPair')
plt.xlabel('principal component 1', fontsize=14)
plt.ylabel('principal component 2', fontsize=14)
plt.grid(alpha=0.5)

leg = plt.legend()
for lh in leg.legendHandles: 
    lh.set_alpha(1)

plt.show()