import pandas as pd
import Maize_Analysis as maize
import Wheat_Analysis as wheat
import RIce_Analysis as rice
from scipy.stats import ttest_ind
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import numpy as np

Crops = pd.read_csv("CropDataSet.csv")
def get_crop_data(df, crop_name):
    crop = df[df["Crop_Type"] == crop_name]

    healthy = crop[crop["Crop_Health_Label"] == 1]
    unhealthy = crop[crop["Crop_Health_Label"] == 0]

    return crop, healthy, unhealthy
Maize, MaizeGood, MaizeBad = get_crop_data(Crops, "Maize")
Wheat, WheatGood, WheatBad = get_crop_data(Crops, "Wheat")
Rice, RiceGood, RiceBad = get_crop_data(Crops, "Rice")
print(len(Maize) + len(Wheat) + len(Rice))

def Health_percentage(health_group, crop):

    CropP = (len(health_group) / len(crop)) * 100

    return round(CropP,2)
def health_test(healthy, unhealthy, variable):

    t_stat, p_value = ttest_ind(
        healthy[variable],
        unhealthy[variable],
        equal_var=False
    )

    print(variable)
    print("T-statistic:", t_stat)
    print("P-value:", p_value)

    return t_stat, p_value
def crop_regression(crop, crop_name):

    X = crop[["Rainfall", "Soil_Moisture", "Pest_Damage"]]
    y = crop["Crop_Health_Label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.30,
        random_state=42,
        stratify=y
    )

    model = LogisticRegression()

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    print(crop_name)
    
    print("Accuracy:", accuracy)
    print("Coefficients:", model.coef_)
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, predictions))
    print()

crop_regression(Maize, "Maize")
crop_regression(Wheat, "Wheat")
crop_regression(Rice, "Rice")

health_test(MaizeGood, MaizeBad, "Rainfall")
health_test(WheatGood, WheatBad, "Rainfall")
health_test(RiceGood, RiceBad, "Rainfall")
health_test(MaizeGood, MaizeBad, "Soil_Moisture")
health_test(WheatGood, WheatBad, "Soil_Moisture")
health_test(RiceGood, RiceBad, "Soil_Moisture")
health_test(MaizeGood, MaizeBad, "Pest_Damage")
health_test(WheatGood, WheatBad, "Pest_Damage")
health_test(RiceGood, RiceBad, "Pest_Damage")
print(f"{Health_percentage(MaizeGood, Maize):.2f}%")
print(f"{Health_percentage(MaizeBad, Maize):.2f}%")

print(f"{Health_percentage(WheatGood, Wheat):.2f}%")
print(f"{Health_percentage(WheatBad, Wheat):.2f}%")

print(f"{Health_percentage(RiceGood, Rice):.2f}%")
print(f"{Health_percentage(RiceBad, Rice):.2f}%")

crops = ["Maize", "Wheat", "Rice"]

healthy_percentages = [
    Health_percentage(MaizeGood, Maize),
    Health_percentage(WheatGood, Wheat),
    Health_percentage(RiceGood, Rice)
]

unhealthy_percentages = [
    Health_percentage(MaizeBad, Maize),
    Health_percentage(WheatBad, Wheat),
    Health_percentage(RiceBad, Rice)
]

x = np.arange(len(crops))
width = 0.35

plt.bar(x - width/2, healthy_percentages, width, label="Healthy")
plt.bar(x + width/2, unhealthy_percentages, width, label="Unhealthy")

plt.xticks(x, crops)
plt.ylabel("Percentage (%)")
plt.xlabel("Crop Type")
plt.title("Crop Health Percentage by Crop Type")
plt.legend()

plt.show()


