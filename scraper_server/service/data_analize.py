from database_manager import get_offers_from_database, get_avg_price_per_meter_offers_with_address


def most_popular_districts():
    offers = get_offers_from_database()
    addresses = []

    for offer in offers:
        addresses.append(offer[2])

    my_dict = {i: addresses.count(i) for i in addresses}
    sorted_dict = {k: my_dict[k] for k in sorted(my_dict, key=my_dict.get, reverse=True)}

    result = []

    for x in list(sorted_dict.items())[:7]:
        json_address = {
            "text": x[0],
            "value": x[1]
        }
        result.append(json_address)

    return result


def district_per_price():
    districts = most_popular_districts()

    for district in districts:
        avg_price = get_avg_price_per_meter_offers_with_address(district["text"])
        district["value"] = avg_price[0][0]

    return districts

