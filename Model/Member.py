from Database.Database import Database


class Member:
	def __init__(self, name: str):
		self.__id = None
		self.__name = name
	
	def save(self):
		db = Database()
		if self.__id is None:
			values = {"name": self.__name}
			self.__id = db.insert("members", values)
		return self
	
	@staticmethod
	def show(member_id: int) -> 'Member':
		db = Database()
		result = db.select_by_id("members", member_id)
		if result is None:
			return None

		member = Member(result[1])
		member.__id = result[0]
		return member
	
	def update(self, **kwargs) -> None:
		db = Database()
		values = {"name": kwargs['name']}
		db.update("members", self.__id, values)
	
	def delete(self) -> None:
		self.delete_traveller_member()
		db = Database()
		db.delete("members", self.__id)
		
	@staticmethod
	def list_by_traveller(traveller_id):
		db = Database()
		results = db.select(f"SELECT members.* FROM traveller_members JOIN members ON traveller_members.member_id = members.id WHERE traveller_members.traveller_id={traveller_id}")
		members = []
		for result in results:
			member = Member(result[1])
			member.__id = result[0]
			members.append(member)
	
		return members
	
	@property
	def name(self) -> str:
		return self.__name
	
	@name.setter
	def name(self, name: str) -> None:
		self.__name = name
	
	@property
	def id(self):
		return self.__id

	# Relacionamento Member e Traveller
	def save_traveller_member(self, traveller_id):
		db = Database()
		values = {
			'member_id': self.__id,
			'traveller_id': traveller_id
		}
		db.insert('traveller_members', values)
		
	def get_traveller_id_for_member(self):
		db = Database()
		member_id = self.__id
		query = f"SELECT traveller_id FROM traveller_members WHERE member_id={member_id}"
		result = db.select(query)
		if result:
			return result[0][0]
		return None

	def delete_traveller_member(self):
		db = Database()
		member_id = self.__id
		traveller_id = self.get_traveller_id_for_member()
		query = f"DELETE FROM traveller_members WHERE member_id={member_id} AND traveller_id={traveller_id}"
		db.raw_sql(query)

	# Relacionamento Member e Spot
	def save_spot_member(self, spot_id):
		db = Database()
		values = {
			'member_id': self.__id,
			'spot_id': spot_id
		}
		db.insert('spot_members', values)

	def get_spot_id_for_member(self):
		db = Database()
		member_id = self.__id
		query = f"SELECT spot_id FROM spot_members WHERE member_id={member_id}"
		result = db.select(query)
		if result:
			return result[0][0]
		return None

	def delete_spot_member(self, spot_id):
		db = Database()
		member_id = self.__id
		query = f"DELETE FROM spot_members WHERE member_id={member_id} AND spot_id={spot_id}"
		db.raw_sql(query)

	@staticmethod
	def validate_member_name_by_traveller(name: str, traveller_id: int, member_id = None) -> bool:
		db = Database()
		query = f"SELECT * FROM members JOIN traveller_members ON members.id = traveller_members.member_id WHERE members.name = '{name}' AND traveller_members.traveller_id = {traveller_id} "
		if member_id is not None:
			query += f"AND members.id <> {member_id}"
		result = db.select(query)
		return len(result) == 0
