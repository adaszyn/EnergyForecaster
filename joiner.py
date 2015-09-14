def join_hourly_values(consumptions, temperatures):
	consumptions_dict = {(idx + 1) %24: float(consumption) for idx, consumption in enumerate(consumptions[0][3:])}
	temperatures_dict = {temperature[2].hour: float(temperature[3]) for temperature in temperatures}
	result = {key: (consumptions_dict[key],temperatures_dict[key]) for key in consumptions_dict.keys()}
	return result