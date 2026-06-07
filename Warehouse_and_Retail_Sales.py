# %% [markdown]
# IMPORTING DATA
# %%
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
# %%
warehouse = pd.read_csv('H:/الكورس/projects/Warehouse and Retail Sales/archive (1)/Warehouse_and_Retail_Sales.csv')
# %% [markdown]
#  PREPROCEESING DATA
# %%
warehouse.info()
# %%
warehouse.columns
# %%
warehouse.describe()
# %%
warehouse.isna().sum()
# %%
warehouse['RETAIL SALES']=warehouse['RETAIL SALES'].interpolate(method='linear')
# %%
warehouse["SUPPLIER"]=warehouse["SUPPLIER"].fillna(warehouse["ITEM DESCRIPTION"])
# %%
warehouse.duplicated()
# %%
warehouse.to_csv('H:/الكورس/projects/Warehouse and Retail Sales/archive (1)/Warehouse_and_Retail_Sales_cleaned.csv',index=False)

# %% [markdown]
# #  **Dashboard 1 — Executive Overview**
# 
# %% [markdown]
# ## **KPIs**
# %% [markdown]
# ### **TotalRetailSales**
# %%
TotalRetailSales=warehouse['RETAIL SALES'].sum()
print(TotalRetailSales)
# %% [markdown]
# ### **Total Warehouse Sales**
# %%
TotalWarehouseSales=warehouse['WAREHOUSE SALES'].sum()
print(TotalWarehouseSales)
# %% [markdown]
# ### **Total Transfers**
# %%
TotalTransfers=warehouse['RETAIL TRANSFERS'].sum()
print(TotalTransfers)
# %% [markdown]
# ### **Number of Products**
# %%
NumberofProducts=warehouse['ITEM CODE'].count()
print(NumberofProducts)
# %% [markdown]
# ### **Number of Suppliers**
# %%
NumberofSuppliers=warehouse['SUPPLIER'].nunique()
print(NumberofSuppliers)
# %% [markdown]
# ### **Avg Monthly Sales**
# %%
AvgMonthlySales=warehouse['MONTH'].mean()
print(AvgMonthlySales)
# %% [markdown]
# # **Charts**
# %% [markdown]
# ## **Monthly Sales Trend**
# %%
MonthlySales=(warehouse.groupby(['YEAR','MONTH'])['RETAIL SALES'].sum().reset_index())
MonthlySales['date']=pd.to_datetime(MonthlySales['YEAR'].astype(str)+'-'+MonthlySales['MONTH'].astype(str))
plt.plot(MonthlySales['date'],MonthlySales['RETAIL SALES'],c='r')
plt.title('Monthly Sales Trend')
plt.grid(False)
plt.show()

# %% [markdown]
# ## **Sales by Item Type**
# %%
SalesByItem=warehouse.groupby('ITEM TYPE')['WAREHOUSE SALES'].sum()
plt.barh(SalesByItem.index,SalesByItem.values,color='gold')
plt.title(' Sales by Item Type')
plt.grid(False)
plt.show()



# %% [markdown]
# ## **Top 10 Products**
# %%
Top10Products=(warehouse.groupby('ITEM CODE')['RETAIL SALES'].sum().sort_values(ascending=False).head(10))
plt.bar(Top10Products.index.astype(str),Top10Products.values,color='lightgreen')
plt.title('Top 10 Products')
plt.grid(False)
plt.show()
# %% [markdown]
# ## **Warehouse vs Retail**
# %%
WarehousevsRetail=warehouse.groupby('MONTH')[['RETAIL SALES','WAREHOUSE SALES']].sum()
x = np.arange(len(WarehousevsRetail.index))
width = 0.35
plt.bar( x - width/2,WarehousevsRetail['RETAIL SALES'], width=width,color='pink')
plt.bar( x + width/2,WarehousevsRetail['WAREHOUSE SALES'], width=width,color='purple')
plt.xticks(x, WarehousevsRetail.index)
plt.title('Warehouse vs Retail')
plt.grid(False)
plt.show()
# %% [markdown]
# # **Dashboard 2 — Product Performance**
# %% [markdown]
# ## **KPIs**
# %% [markdown]
# ## **Best Selling ITEM TYPE **
# %%
BestSellingitemtype=(warehouse.groupby('ITEM TYPE')['RETAIL SALES'].sum().idxmax())
print(BestSellingitemtype)
# %% [markdown]
# ## **Worst Selling ITEM TYPE**
# %%
WorstSellingitemtype = (warehouse.groupby('ITEM TYPE')['RETAIL SALES'].sum().idxmin())
print(WorstSellingitemtype)
# %% [markdown]
# ## **Avg Product Sales**
# %%
AvgProductSales=warehouse.groupby('ITEM TYPE')['RETAIL SALES'].mean().sort_values(ascending=False)
display(AvgProductSales)
# %% [markdown]
# # **Charts**
# %% [markdown]
# ## **Top Products**
# %%
TopProducts=warehouse.groupby('ITEM TYPE')['RETAIL SALES'].sum().sort_values(ascending=False).head(5)
plt.bar(TopProducts.index.astype(str),TopProducts.values,color='navy')
plt.title('Top Products')
plt.grid(False)
plt.show()

# %% [markdown]
# ## **Bottom Products**
# %%
BottomProducts=warehouse.groupby('ITEM TYPE')['RETAIL SALES'].sum().sort_values(ascending=True).tail(5)
plt.barh(BottomProducts.index.astype(str),BottomProducts.values,color='silver')
plt.title('Bottom Products')
plt.grid(False)
plt.show()
# %% [markdown]
# ## **Product Sales Distribution**
# %%
ProductsalesDistribution=(warehouse.groupby('ITEM CODE')['WAREHOUSE SALES'].sum())
plt.boxplot(ProductsalesDistribution)
plt.title('Product Sales Distribution')
plt.grid(False)
plt.show()
# %% [markdown]
# ## **Correlation Analysis**
# %%
corr = warehouse[["RETAIL SALES", "WAREHOUSE SALES", "RETAIL TRANSFERS"]].corr()
sns.heatmap(corr, annot=True,cmap="coolwarm")
plt.title('Correlation Matrix')
plt.show()

# %% [markdown]
# ## **Product Contribution %**
# %%
ProductSales = (warehouse.groupby('ITEM CODE')['RETAIL SALES'].sum().sort_values(ascending=False).head(20))
Pareto = ProductSales.reset_index()
Pareto.columns = ['ITEM CODE', 'SALES']
Pareto['Cumulative Sales'] = Pareto['SALES'].cumsum()
Pareto['Cumulative Percentage'] = (Pareto['Cumulative Sales']/ Pareto['SALES'].sum()) * 100
fig, ax1 = plt.subplots(figsize=(12,6))
ax1.bar(Pareto['ITEM CODE'].astype(str),Pareto['SALES'],color='steelblue')
ax2 = ax1.twinx()
ax2.plot(Pareto['ITEM CODE'].astype(str),Pareto['Cumulative Percentage'],color='red', marker='o')
ax2.set_ylim(0, 110)
plt.title('Pareto Analysis of Product Sales')
plt.grid(False)
plt.xticks([])
plt.show()