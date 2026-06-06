import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,f1_score,confusion_matrix
df = pd.read_csv("ipl2024 Matches.csv")
features=["team1","team2","toss_winner","decision"]
target="winner"
df=df[features+[target]]
df.dropna(inplace=True)
encoders={}
for col in features:
    le=LabelEncoder()
    df[col]=le.fit_transform(df[col])
    encoders[col]=le
le_target=LabelEncoder()

X=df[features]
y=le_target.fit_transform(df[target])

X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)

model = RandomForestClassifier(n_estimators=200,random_state=42)
model.fit(X_train,y_train)
y_pred=model.predict(X_test)
accuracy_score(y_test, y_pred)
f1_score(y_test,y_pred,average="weighted")
confusion_matrix(y_test,y_pred)
print("accuracy:",accuracy_score(y_test,y_pred))
print("f1 score:",f1_score(y_test,y_pred,average="weighted"))
print("confusion matrix:\n",confusion_matrix(y_test,y_pred))