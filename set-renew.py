#!/usr/bin/python3

import json
import time
import ovh
import os
import dotenv
from datetime import datetime, timedelta, timezone

denv = dotenv.load_dotenv("./.env")

def update_renewal(client, id, renew_mode, renew_period):
    renew={}
    renew["mode"]=renew_mode
    renew["period"]=renew_period
    try:
        result = client.put(f"/services/{id}",
            renew = renew, # Renew information (type: services.update.Service.Renew, nullable)
        )
        return True
    except Exception as ex:
        print(ex)
        return False



client = ovh.Client()

print("""Welcome in OVH renew fix script!
      This script helps you to modify OVH-managed service(s) renewal settings.
      For more info, see the project README.
      You can always press CTRL+c to exit.
      """)

servers={}
service_ids=[]

product_ids = client.get("/services")
if len(product_ids) < 1:
    exit

for item in product_ids:
    product = client.get(f"/services/{item}")
    if product["route"] and product["billing"]["lifecycle"]["current"]["state"] == "active":
        serviceId = product["serviceId"]
        if serviceId not in servers:
            servers[serviceId]={}
        service=servers[serviceId]
        service["invoice"]=product["billing"]["plan"]["invoiceName"]
        service["planCode"]=product["billing"]["plan"]["code"]
        service["monthlyPrice"]=product["billing"]["pricing"]["price"]["text"]
        service["renewMode"]=product["billing"]["renew"]["current"]["mode"]
        service["displayName"]=product["resource"]["displayName"]
        service_ids.append(serviceId)
    elif product["route"] == None and "renew" in product["billing"] and product["billing"]["renew"] != None:
        if product["parentServiceId"] not in servers:
            servers[product["parentServiceId"]]={}
        if "addon_ids" not in servers[product["parentServiceId"]]:
            servers[product["parentServiceId"]]["addon_ids"]=[]
        addon={}
        addon["id"]=product["serviceId"]
        addon["invoice"]=product["billing"]["plan"]["invoiceName"]
        addon["renew_mode"]=product["billing"]["renew"]["current"]["mode"]
        servers[product["parentServiceId"]]["addon_ids"].append(addon)

print("#\tService\tInvoice\tPlanCode\tRenew mode\tRenew price")
for index,item in enumerate(servers):
    server=servers[item]
    print(f"{index}\t{server['displayName']}\t{server['invoice']}\t{server['planCode']}\t{server['renewMode']}\t{server['monthlyPrice']}")

print("Select a server by typing it's id and enter. Or select all by simply press enter.")
server_id = input()

try:
    server_id = int(server_id)
    if not service_ids[server_id]:
        server_id="all"
    else:
        service_api_id=service_ids[server_id]
except Exception as ex:
    server_id="all"

if server_id == "all":
    print("All servers selected.")
else:
    print(f"Selected: {servers[service_ids[server_id]]['displayName']}")
    print("Addons:")
    for i in servers[service_ids[server_id]]["addon_ids"]:
        print(f"{i['invoice']}: {i['renew_mode']}")

renew_mode = (input('Set renew mode. Possible values: manual, automatic (default is automatic): ') or "automatic")
renew_period = "P1M"
if renew_mode == "automatic":
    renew_period = (input('Set renew period. Default is P1M: ') or "P1M")
if renew_mode not in ["manual", "automatic"]:
    renew_mode = "automatic"
print("Setting up. If you will see the prompt changes saved.")
print("After this run, rerun the script to see the changes. Press CTRL+c in the summary table if you do not want to do more modifications.")

if server_id != "all":
    update_renewal(client, service_api_id, renew_mode, renew_period)
    for i in servers[service_api_id]["addon_ids"]:
        update_renewal(client, i["id"], renew_mode, renew_period)


if server_id == "all":
    for i in servers:
        server=servers[i]
        update_renewal(client, i, renew_mode, renew_period)
        for j in server["addon_ids"]:
            update_renewal(client, j["id"], renew_mode, renew_period)

print("Thanks for using my script. :)")
