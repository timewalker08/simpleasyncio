
from event import Eventloop

def later_call():
    print(99999)

async def main():
    loop = Eventloop.get_current_loop()
    loop.call_later(3, later_call)
    print(await loop.listen_io(1))
    print(await loop.listen_io(2))
    print(await loop.listen_io(3))

if __name__ == "__main__":
    loop = Eventloop.get_current_loop()
    loop.run_until_complete(main())
