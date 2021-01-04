# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 19:06:23 2019

@author: Jorge
"""
# Modelo básico del Problema del Granjero del libro de John R. Birge and Francois Louveaux.

from gurobipy import *
from random   import *
import numpy as np

CROPS = ["trigo", "maiz", "remolacha"]

TotalArea = 500
               # acre
Yield = {
"trigo": 2.5,
"maiz" : 3.0,
"remolacha": 20.0,
}        # T/acre
        
PlantingCost = {
"trigo": 150,
"maiz" : 230,
"remolacha": 260,
}      # $/acre
        
SellingPrice = {
"trigo": 170,
"maiz" : 150,
"remolacha": 36,
}      # $/T
        
ExcessSellingPrice = 10      # $/T

PurchasePrice = {
"trigo": 238,
"maiz" : 210,
"remolacha": 100,
}      # $/T
        
MinRequirement = {
"trigo": 200,
"maiz" : 240,
"remolacha": 0,
}      # $/T

promedio = {
"trigo": 2000,
"maiz" : 2400,
"remolacha": 2700,
}      # $/T

sigma = {
"trigo": 200,
"maiz" : 500,
"remolacha": 350,
}      # $/T

Requerimiento = 1000000
        
BeetsQuota = 6000         # T

farmer = Model("Birge and Louveaux Farmer's Model")
#farmer.Params.NonConvex = 2
#farmer.Params.Method = 1
# variables
area = farmer.addVars(CROPS,lb=0,ub=GRB.INFINITY,name="Area_for_crop")
sell = farmer.addVars(CROPS,lb=0,ub=GRB.INFINITY,name="Crops_sold")
buy = farmer.addVars(CROPS,lb=0,ub=GRB.INFINITY,name="Crops_bought")
slack = farmer.addVar(name = 'holgura')
sellExcess = farmer.addVar(lb=0,ub=GRB.INFINITY,name="Sugar_beets_excess") 
 
farmer.setObjective(ExcessSellingPrice*sellExcess + quicksum((SellingPrice[c]*sell[c]-PurchasePrice[c]*buy[c]-PlantingCost[c]*area[c]) for c in CROPS),GRB.MAXIMIZE)

areaconstr = farmer.addConstr(quicksum(area[c] for c in CROPS) <= TotalArea, name = "Available_area")
reqconstr = farmer.addConstrs(((Yield[c]*area[c]-sell[c]+buy[c] >= MinRequirement[c]) for c in CROPS), name = "Crops_requirements")  
quotaconstr = farmer.addConstr(sell["remolacha"] <= BeetsQuota, name = "Beets_quota")
sellconstr = farmer.addConstr(sell["remolacha"] + sellExcess <= Yield["remolacha"]*area["remolacha"], name = "Beets_sell")

#Restricción agua
farmer.addConstr(slack == (sum(promedio[c]*area[c] for c in CROPS)-Requerimiento)/1.65) 
guaconstr = farmer.addConstr( sum(((sigma[c])*(sigma[c]))*((area[c])*area[c]) for c in CROPS) <= slack * slack , name = "agua")

farmer.optimize() 

print('\n ***** Problema del Granjero resuelto**** \n\n')
print('\n Valor óptimo: %8.4f \n\n' % farmer.objval)

print('Superficies a sembrar: ')
for c in CROPS:
    print(c,area[c].X)
    
print('\nCultivos a vender: ')
for c in CROPS:
    print(c,sell[c].X)

print('\nCultivos a comprar: ')
for c in CROPS:
    print(c,buy[c].X)
    
print('\nExceso de remolacha: %8.4f ' % sellExcess.X)

print('\nPrecio sombra restricción de área: %8.4f ' % areaconstr.Pi)

print('\nSensibilidad al precio de venta de los cultivos: ')
for c in CROPS:
    print(c,sell[c].SAObjUp,sell[c].SAObjLow)

