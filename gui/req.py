import random
import string
import aiohttp
import asyncio

class Tester:
    def __init__(self):
        self.session = aiohttp.ClientSession()
        self.url = "http://127.0.0.1:8000/users/sing_up"
        self.first_names = ["Аня", "Борис", "Света", "Геннадий", "Лена"]
        self.last_names = ["Петров", "Иванов", "Сидорова", "Кузнецов", "Смирнова"]
        self.domains = ["example.com", "gmail.com", "yahoo.com", "hotmail.com"]
        self.headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        }

    def generate_random_email(self, length=10):
        username = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))
        return f"{username}@{random.choice(self.domains)}"

    def generate_random_password(self, length=12):
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for _ in range(length))

    def generate_random_phone_number(self):
        area_code = random.randint(900, 999)
        first_part = random.randint(100, 999)
        second_part = random.randint(10, 99)
        third_part = random.randint(10, 99)
        return f"+7 ({area_code}) {first_part}-{second_part}-{third_part}"

    def generate_json(self):
        return {
            "first_name": random.choice(self.first_names),
            "last_name": random.choice(self.last_names),
            "password": self.generate_random_password(),
            "phone": self.generate_random_phone_number(),
            "email": self.generate_random_email(),
        }

    async def send_request(self):
        while True:
            try:
                async with self.session.post(url=self.url, json=self.generate_json(), headers=self.headers) as resp:
                    # print(await resp.text()) 
                    print(resp.headers)
            except Exception as e:
                print(f"Ошибка при отправке запроса: {e}")


    async def close(self):
        await self.session.close() 

async def main():
    tester = Tester()
    try:
        await tester.send_request()
    except KeyboardInterrupt:
        print("Завершение программы.")
    finally:
        await tester.close()

if __name__ == "__main__":
    asyncio.run(main()) 