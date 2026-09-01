import pandas as pd
import matplotlib.pyplot as plt
AnalyzeR= pd.read_csv("Rice.csv")
Ricedup= AnalyzeR.drop_duplicates()
RiceIn= Ricedup.isnull()
Riceow = Ricedup[Ricedup["Soil_Moisture"] <= 5]
RiceRainFall = Ricedup[Ricedup["Rainfall"] >= 55]      
RiceGood= Ricedup[Ricedup["Crop_Health_Label"]==1]    
RiceBad= Ricedup[Ricedup["Crop_Health_Label"]==0]    
DrainGood=Ricedup[Ricedup["Drainage_Features"]==1]
DrainBad= Ricedup[Ricedup["Drainage_Features"]==0]   
print(len(RiceIn))         
print(Ricedup["Bounding_Boxes"].min())
print(Ricedup["Wind_Speed"].max())
print(Ricedup.dtypes)
RiceCount = Ricedup["Crop_Health_Label"].value_counts()
RiceCount.plot(kind="bar", color="skyblue")
plt.title("Rice Crop Health Label Counts")
plt.ylabel("Count")
plt.tight_layout() 
plt.show()          
MaizeDrain = Ricedup["Drainage_Features"].value_counts()
MaizeDrain.plot(kind="bar", color="salmon")
plt.title("Rice Drainage Features Counts")
plt.ylabel("Count")
plt.tight_layout()
plt.show()   
Ricedup.boxplot(column="Pest_Damage")
plt.title("Pest Distribution")
plt.ylabel("Pest")
plt.show()      
Ricedup.boxplot(column="Soil_Moisture")
plt.title("Soil Distribution")
plt.ylabel("Soil")
plt.show()      
Ricedup.boxplot(column="Rainfall")
plt.title("RainFall Distribution")
plt.ylabel("Rail")
plt.show() 

print("Healthy Rice rainfall:", RiceGood["Rainfall"].mean())
print("Unhealthy Rice rainfall:", RiceBad["Rainfall"].mean())
print("Healthy Rice soil moisture:", RiceGood["Soil_Moisture"].mean())
print("Unhealthy Rice soil moisture:",RiceBad["Soil_Moisture"].mean())
print("Healthy Rice pest damage:", RiceGood["Pest_Damage"].mean())
print("Unhealthy Rice pest damage:", RiceBad["Pest_Damage"].mean())