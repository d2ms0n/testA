from models import User

def id_to_name(data):
	cars = []
	car_dict={}
	managers_dict = {
		user.id: user.name 
		for user in User.query.all()
	}

	for car in data:
		
		manager_name = managers_dict.get(car.manager_id)

		#print(f"manager{manager_name}")
		
		car_dict = car.__dict__
		#print(f"**{car_dict}***\n")

		# Проверяем, что имя найдено
		if manager_name:
			car_dict["name"] = manager_name
			print(f"-managerOK-{car_dict["name"]}----/n")
		else:
			car_dict["name"] = ""

		print(f"**{car_dict}****\n")
		cars.append(car_dict)
		print(f"-cars-{cars}----")
	return cars