import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score,f1_score,confusion_matrix
df = pd.read_csv("match_data.csv")
df.dropna(inplace=True)
le = LabelEncoder()
df["team1_enc"]=le.fit_transform(df["team1"])
df["team2_enc"]=le.fit_transform(df["team2"])
df["venue_enc"]=le.fit_transform(df["venue"])
df["result_enc"]=le.fit_transform(df["result"])
X=df[["team1_enc","team2_enc","venue_enc"]]
y=df["result_enc"]



X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.3,random_state=42)
model = LogisticRegression(max_iter=1000)
model.fit(X_train,y_train)
y_pred=model.predict(X_test)
accuracy_score(y_test, y_pred)
f1_score(y_test,y_pred,average="weighted")
confusion_matrix(y_test,y_pred)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("F1 Score:", f1_score(y_test, y_pred, average="weighted"))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))