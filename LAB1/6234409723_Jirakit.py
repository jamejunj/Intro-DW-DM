import pandas as pd

# Import Excel desired sheet from pandas
productSrc1 = pd.read_excel('ETLDataSource1.xlsx', sheet_name='productSource1')
orderSrc1 = pd.read_excel('ETLDataSource1.xlsx', sheet_name='orderSource1')
stateAbbriv = pd.read_excel('ETLDataSource1.xlsx', sheet_name='StateLookup')

productSrc2 = pd.read_excel('ETLDataSource2.xlsx', sheet_name='productSource2')
orderSrc2 = pd.read_excel('ETLDataSource2.xlsx', sheet_name='orderSource2')

# Join productSrc1 and productSrc2 on OrderID
joinedSrc1 = pd.merge(productSrc1, orderSrc1, on='OrderID', how='inner')

# map CustomerState abbriv to their full name
joinedSrc1['CustomerState'] = joinedSrc1['CustomerState'].map(stateAbbriv.set_index('Abbreviation')['State'].to_dict())

# reindex by columns alphabetically
joinedSrc1.reindex(sorted(joinedSrc1.columns), axis=1)

# Join productSrc2 and orderSrc2 on OrderID
joinedSrc2 = pd.merge(productSrc2, orderSrc2, on='OrderID', how='inner')

# replace A in OrderID with empty string
joinedSrc2['OrderID'] = joinedSrc2['OrderID'].replace('A', '', regex=True)

# tranform OrderID to int
joinedSrc2['OrderID'] = joinedSrc2['OrderID'].astype(int)

# recalculate TotalDiscount 
joinedSrc2['TotalDiscount'] = joinedSrc2['FullPrice'].astype(float) - joinedSrc2['ExtendedPrice'].astype(float)

# join customer firstname and lastname as CustomerName
joinedSrc2['CustomerName'] = joinedSrc2['CustomerFirstName'].astype(str) + ' ' + joinedSrc2['CustomerLastName'].astype(str)

# drop entity CustomerFirstName and CustomerLastName
joinedSrc2 = joinedSrc2.drop(['CustomerFirstName','CustomerLastName'], axis=1)

# reindex by columns alphabetically
joinedSrc2.reindex(sorted(joinedSrc2.columns), axis=1)

# concat 2 tables togethers
new = pd.concat([joinedSrc1, joinedSrc2])

desired_index = ['OrderID', 'OrderDate', 'CustomerName', 'CustomerCity', 'CustomerState', 'CustomerStatus', 'ProductID', 'Product', 'UnitPrice', 'Quantity', 'FullPrice', 'ExtendedPrice', 'Discount', 'TotalDiscount']

# reindex as desired
new = new.reindex(desired_index, axis=1)

# export to excel
new.to_excel('PDOutput.xlsx', index=False)