from sklearn import metrics
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import Perceptron
from sklearn.svm import SVC
import sys
import graderUtil

#######################################################################
# Do not make any change in this block
# a dict stores the final result
task_result = {
    "y_pred": []
} 

# read task file content
training_filename = sys.argv[1]
testing_filename = sys.argv[2]
answer_filename = sys.argv[3]

df = graderUtil.load_file(training_filename)
X_test = graderUtil.load_testing_file(testing_filename)
y_test = graderUtil.load_answer_file(answer_filename)

#print(df.sample(5))
#print(X_test.sample(5))
#print(y_test)

##########################################################
# BEGIN_YOUR_CODE

## Training ##
# data spliting
X = df.iloc[:,[2,3]] 
y = df.iloc[:,-1]
# z-score normalization
scaler = StandardScaler().fit(X) 
X_scaled = scaler.transform(X)
X_test_scaled = scaler.transform(X_test.iloc[:,[2,3]])
X_train, X_validation, y_train, y_validation = train_test_split(X_scaled,y, test_size=0.2, random_state=10)

## Learning ##
# initialization
Per_clf = Perceptron()
LogReg_clf = LogisticRegression()
DTree_clf = DecisionTreeClassifier()
SVC_clf = SVC()
voting_clf = VotingClassifier(estimators=[('Per', Per_clf), ('SVC', SVC_clf), ('DTree', DTree_clf), ('LogReg', LogReg_clf)], voting='hard')
# optimization
voting_clf.fit(X_train, y_train)
# prediction
y_pred_test = voting_clf.predict(X_test_scaled)
print(metrics.accuracy_score(y_pred_test, y_test))
task_result["y_pred"] = y_pred_test;

# END_YOUR_CODE
# Do Not Make Any Change BELOW
#######################################################################

# output your final result
print("Prediction:")
print(task_result["y_pred"])
print("Score(100%): " + str(graderUtil.accuracy_score(task_result['y_pred'],y_test['target'])))