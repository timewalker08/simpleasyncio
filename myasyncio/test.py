
from event import Eventloop


async def main():
    loop = Eventloop.get_current_loop()
    print(await loop.listen_io(1))
    print(await loop.listen_io(2))
    print(await loop.listen_io(3))

if __name__ == "__main__":
    loop = Eventloop.get_current_loop()
    loop.run_until_complete(main())
