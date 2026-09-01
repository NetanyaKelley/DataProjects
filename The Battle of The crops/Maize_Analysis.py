import pandas as pd
import matplotlib.pyplot as plt
AnalyzeM= pd.read_csv("Maize.csv")
Maizedup= AnalyzeM.drop_duplicates()
MaizeIn= Maizedup.isnull()
MaizeLow = MaizeIn[Maizedup["Soil_Moisture"] <= 5]
MaizeRainFall = MaizeIn[Maizedup["Rainfall"] >= 55]      
MaizeGood= Maizedup[Maizedup["Crop_Health_Label"]==1]    
MaizeBad= Maizedup[Maizedup["Crop_Health_Label"]==0]    
DrainGood=Maizedup[Maizedup["Drainage_Features"]==1]
DrainBad= Maizedup[Maizedup["Drainage_Features"]==0]   
print(len(MaizeIn))         
print(Maizedup["Bounding_Boxes"].min())
print(Maizedup["Wind_Speed"].max())
print(Maizedup.dtypes)
MaizeCount = Maizedup["Crop_Health_Label"].value_counts()
MaizeCount.plot(kind="bar", color="skyblue")
plt.title("Maize Crop Health Label Counts")
plt.ylabel("Count")
plt.tight_layout() 
plt.show()          
MaizeDrain = Maizedup["Drainage_Features"].value_counts()
MaizeDrain.plot(kind="bar", color="salmon")
plt.title("Maize Drainage Features Counts")
plt.ylabel("Count")
plt.tight_layout()
plt.show()   
Maizedup.boxplot(column="Pest_Damage")
plt.title("Pest Distribution")
plt.ylabel("Pest")
plt.show()      
Maizedup.boxplot(column="Soil_Moisture")
plt.title("Soil Distribution")
plt.ylabel("Soil")
plt.show()      
Maizedup.boxplot(column="Rainfall")
plt.title("RainFall Distribution")
plt.ylabel("Rail")
plt.show() 

print("Healthy maize rainfall:", MaizeGood["Rainfall"].mean())
print("Unhealthy maize rainfall:", MaizeBad["Rainfall"].mean())
print("Healthy maize soil moisture:", MaizeGood["Soil_Moisture"].mean())
print("Unhealthy maize soil moisture:", MaizeBad["Soil_Moisture"].mean())
print("Healthy maize pest damage:", MaizeGood["Pest_Damage"].mean())
print("Unhealthy maize pest damage:", MaizeBad["Pest_Damage"].mean())