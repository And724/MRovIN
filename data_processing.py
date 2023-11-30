
def receive_send_data(data):
    data_extraction(data)
    return data

def data_extraction(data):
    data_dict = {}
    if data["photos"] != []:
        data_dict["sol"] = data["photos"][0]["sol"]
        data_dict["earth_date"] = data["photos"][0]["earth_date"]
        data_dict["rover"] = data["photos"][0]["rover"]["name"]
        data_dict["camera"] = data["photos"][0]["camera"]["full_name"]
        data_dict["img_link"] = data["photos"][0]["img_src"]
        print(data_dict)
        return data_dict


    
