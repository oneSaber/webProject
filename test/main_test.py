import requests
from faker import Faker
import json
# test register
class Register:

    faker = Faker()

    def create_account(self,role):
        account = self.faker.word() + str(self.faker.random_number(5))
        password = str(self.faker.random_number(10))
        name = self.faker.name()
        email = self.faker.free_email()
        if role == "Student":
            address = self.faker.address()
            school = self.faker.word()+"school"
            return dict(role="student",account=account, password=password, name=name,email=email, address=address, school=school)
        if role == "Teacher":
            address = self.faker.address()
            return dict(role="teacher",account=account, password=password, name=name, email=email, address=address)
        if role == "Admin":
            return dict(account=account,password=password,name=name,email=email,role="admin")

    def register_Test(self):
        roles = ["Teacher","Student","Admin"]
        successful_count = 0
        failure_count = 0
        users = []
        import random
        for _ in range(10):
            role = random.choice(roles)
            user_info = self.create_account(role)
            users.append(user_info)
            se = requests.Session()
            re = se.post("http://39.105.64.7:5000/main/register",json=json.dumps(user_info))
            if re.status_code == 200:
                successful_count += 1
            else:
                failure_count += 1
        print("successful:", successful_count)
        print("failure:", failure_count)
        return users

# test login
class Login:
    def __init__(self,users):
        self.user_info = [{"role":user['role'], 'account':user['account'], "password":user['password']} for user in users]
        self.links = []
    def login_test(self):
        successful_count = 0
        failure_count = 0
        for user in self.user_info:
            se = requests.Session()
            re = se.post("http://39.105.64.7:5000/main/login",json=json.dumps(user))
            if re.status_code == 200:
                successful_count += 1
                self.links.append(se)
            else:
                failure_count += 1
        print("successful:", successful_count)
        print("failure:", failure_count)
        return self.links

if __name__ == "__main__":
    register = Register()
    users = register.register_Test()
    login = Login(users)
    links = login.login_test()