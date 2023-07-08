import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# charger les données
df = pd.read_csv('your_file.csv')

# assurer que les données sont numériques
df['pas de vis'] = pd.to_numeric(df['pas de vis'], errors='coerce')
df['Longueur d\'onde'] = pd.to_numeric(df['Longueur d\'onde'], errors='coerce')

# supprimer les valeurs nulles s'il y en a
df = df.dropna()

x = df['pas de vis'].values.reshape(-1,1)
y = df['Longueur d\'onde'].values


# définir le nombre maximum de degrés
max_degree = 10

# initialiser le score R² et le degré optimal
best_score = 0
best_degree = 0

for degree in range(1, max_degree + 1):
    # transformer les données
    poly = PolynomialFeatures(degree)
    x_poly = poly.fit_transform(x)

    # ajuster le modèle
    model = LinearRegression()
    model.fit(x_poly, y)

    # faire une prédiction
    y_pred = model.predict(x_poly)

    # calculer le score R²
    score = r2_score(y, y_pred)

    # vérifier si le score est meilleur
    if score > best_score:
        best_score = score
        best_degree = degree

print('Le degré optimal est:', best_degree)

# une fois que vous avez le degré optimal, vous pouvez ajuster et afficher le modèle
poly = PolynomialFeatures(best_degree)
x_poly = poly.fit_transform(x)

model = LinearRegression()
model.fit(x_poly, y)

plt.scatter(x, y, color = 'blue')
plt.plot(x, model.predict(poly.fit_transform(x)), color = 'red')
plt.title('Régression polynomiale')
plt.xlabel('pas de vis')
plt.ylabel('Longueur d\'onde')
plt.show()

# imprimer les coefficients
print('Coefficients du polynôme:', model.coef_)

