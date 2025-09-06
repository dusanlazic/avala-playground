from avala import Avala

avl = Avala(
    host="localhost",
    port=2024,
    name="s4ndu",
    password="avalarocks",
    protocol="http",
    redis_url="redis://localhost:6379/0",
)

avl.register_directory("sploits")

if __name__ == "__main__":
    avl.run()
