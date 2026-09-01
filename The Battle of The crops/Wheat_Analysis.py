import pandas as pd
import matplotlib.pyplot as plt
AnalyzeW= pd.read_csv("Wheat.csv")
Wheatdup= AnalyzeW.drop_duplicates()
WheatIn= Wheatdup.isnull()
MaizeLow = Wheatdup[Wheatdup["Soil_Moisture"] <= 5]
WheatRainFall = Wheatdup[Wheatdup["Rainfall"] >= 55]      
WheatGood= Wheatdup[Wheatdup["Crop_Health_Label"]==1]    
WheatBad= Wheatdup[Wheatdup["Crop_Health_Label"]==0]    
DrainGood=Wheatdup[Wheatdup["Drainage_Features"]==1]
DrainBad= Wheatdup[Wheatdup["Drainage_Features"]==0]   
print(len(WheatIn))         
print(Wheatdup["Bounding_Boxes"].min())
print(Wheatdup["Wind_Speed"].max())
print(Wheatdup.dtypes)
MaizeCount = Wheatdup["Crop_Health_Label"].value_counts()
MaizeCount.plot(kind="bar", color="skyblue")
plt.title("Wheat Crop Health Label Counts")
plt.ylabel("Count")
plt.tight_layout() 
plt.show()          
MaizeDrain = Wheatdup["Drainage_Features"].value_counts()
MaizeDrain.plot(kind="bar", color="salmon")
plt.title("Wheat Drainage Features Counts")
plt.ylabel("Count")
plt.tight_layout()
plt.show()   
Wheatdup.boxplot(column="Pest_Damage")
plt.title("Pest Distribution")
plt.ylabel("Pest")
plt.show()      
Wheatdup.boxplot(column="Soil_Moisture")
plt.title("Soil Distribution")
plt.ylabel("Soil")
plt.show()      
Wheatdup.boxplot(column="Rainfall")
plt.title("RainFall Distribution")
plt.ylabel("Rail")
plt.show() 

print("Healthy Wheat rainfall:", WheatGood["Rainfall"].mean())
print("Unhealthy Wheat rainfall:", WheatBad["Rainfall"].mean())
print("Healthy Wheat soil moisture:", WheatGood["Soil_Moisture"].mean())
print("Unhealthy Wheat soil moisture:", WheatBad["Soil_Moisture"].mean())
print("Healthy Wheat pest damage:", WheatGood["Pest_Damage"].mean())
print("Unhealthy Wheat pest damage:", WheatBad["Pest_Damage"].mean())