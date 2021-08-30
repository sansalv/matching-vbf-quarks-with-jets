# Investigation of three machine learning methods
# Print prediction results and ROC curve for each
# *****************************************
classifiers = [KNeighborsClassifier(n_neighbors=7),
               LogisticRegression(random_state=0, solver='lbfgs', multi_class='ovr'),
               MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)]

names = ['KNN(n=7)','LogisticRegression','MLPClassifier']

j = 0
for classifier in classifiers:
    
    print('Classifier: ' + str(names[j]) + ':\n')
    
    
    y_proba = classifier.fit(X_train, y_train).predict_proba(X_test)
    y_pred = classifier.fit(X_train, y_train).predict(X_test)
    print(classification_report(y_test, y_pred))
    print('Total accuracy: ' + str(round(accuracy_score(y_test, y_pred), 4)))
    print('ROC score:      ' + str(round(roc_auc_score(y_test, y_proba[:, 1]), 4)))
    print('Confusion matrix:')
    print(confusion_matrix(y_test, y_pred))
    

    fpr, tpr, _ = roc_curve(y_test, y_proba[:,1])
    roc_auc = auc(fpr, tpr)

    plt.figure()
    plt.plot(fpr, tpr, color='darkorange', label='ROC curve (area = %0.4f)' %roc_auc)
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.0])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC curve for ' + names[j] + ':')
    plt.legend(loc="lower right")
    plt.show()
    j += 1
    
    print('*************************************************')