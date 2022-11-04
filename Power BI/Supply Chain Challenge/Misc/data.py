import numpy as np
import pandas as pd


data = pd.read_csv("fact_order_lines.csv")
df = data.drop(columns=["order_id","product_id","order_qty","agreed_delivery_date","actual_delivery_date","delivery_qty"], axis=1)
df['order_placement_date'] = pd.to_datetime(df['order_placement_date'])

a = list(df["customer_id"].unique())
results = pd.DataFrame({
        'customer_id':[],
        "order_placement_date":[],
        "In Full":[],
        "On Time":[],
        "On Time In Full":[]
        })

def transformData(df, a, results):
    for i in a:
        output = pd.DataFrame({
        'customer_id':[],
        "order_placement_date":[],
        "In Full":[],
        "On Time":[],
        "On Time In Full":[]
        })
        x = df[df["customer_id"]==i]
        y = x.groupby("order_placement_date")[["In Full","On Time","On Time In Full"]].aggregate(np.average)
        output["order_placement_date"] = pd.Series(y.index)
        output['In Full'] = pd.Series(y['In Full'].values)
        output['On Time'] = pd.Series(y['On Time'].values)
        output['On Time In Full'] = pd.Series(y['On Time In Full'].values)
        output["customer_id"] = i
        print(output.shape)
        print(results.shape)
        results = pd.concat([results,output])
    results.sort_values(["customer_id","order_placement_date"],axis=1,inplace=True,ignore_index=True)
    return results


transformData(df=df,a=a,results=results)