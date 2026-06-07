# src/ai/model.py
import os
import pickle
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import accuracy_score, log_loss
import xgboost as xgb


class FootballPredictor:
    def __init__(self, model_path=None):
        if model_path is None:
            # По подразбиране моделът се записва в tools/ папката
            base_dir = os.path.dirname(os.path.abspath(__file__))
            model_path = os.path.join(base_dir, 'tools', 'xgboost_model.pkl')
        self.model_path = model_path
        self.model = None
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)


    def train(self, X, y, params=None):
        """
        X: list of feature lists or numpy array
        y: list of labels (0,1,2)
        """
        if params is None:
            params = {
                'n_estimators': 30,
                'max_depth': 3,
                'learning_rate': 0.2,
                'objective': 'multi:softprob',
                'num_class': 3,
                'eval_metric': 'mlogloss',
                'random_state': 42
            }
        X = np.array(X)
        y = np.array(y)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
        self.model = xgb.XGBClassifier(**params)
        self.model.fit(X_train, y_train)
        # Оценка
        y_pred = self.model.predict(X_test)
        y_proba = self.model.predict_proba(X_test)
        acc = accuracy_score(y_test, y_pred)
        loss = log_loss(y_test, y_proba)
        print(f"✅ Моделът е обучен. Тестова точност: {acc:.3f}, Log Loss: {loss:.3f}")
        # Кръстосана проверка
        cv_scores = cross_val_score(self.model, X, y, cv=StratifiedKFold(5, shuffle=True, random_state=42), scoring='accuracy')
        print(f"📊 Cross-validation accuracy: mean={cv_scores.mean():.3f} (+/- {cv_scores.std():.3f})")
        self.save()
        return acc, loss, cv_scores


    def predict_proba(self, features):
        """Връща вероятности [home, draw, away]"""
        if self.model is None:
            self.load()
        proba = self.model.predict_proba(np.array([features]))[0]
        return proba.tolist()


    def save(self):
        with open(self.model_path, 'wb') as f:
            pickle.dump(self.model, f)
        print(f"💾 Моделът е записан в {self.model_path}")


    def load(self):
        if os.path.exists(self.model_path):
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)
            print(f"📂 Моделът е зареден от {self.model_path}")
        else:
            raise FileNotFoundError(f"Моделът не съществува: {self.model_path}")


    def feature_importance(self, feature_names):
        if self.model is None:
            self.load()
        importance = self.model.feature_importances_
        return dict(zip(feature_names, importance))