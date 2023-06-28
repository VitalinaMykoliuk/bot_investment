import asyncio
from data.loader import *
from heandlers import *
from services.api_sqlite import *
from data.confige import *


users = Users()
config = Config()


async def add_money():
    while True:
        percent = config.get_percent()
        for user in users:
            to_plus = user['investments']
            users.change_investments(user['chat_id'], to_plus + to_plus*(percent/100))
            if user['is_ref']:
                ref_user = users.get_user(user['is_ref'])
                to_plus = ref_user['balance']
                users.change_balance(ref_user['chat_id'], to_plus + user['investments'] * (investmen / 100))
        await asyncio.sleep(86400)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(dp.start_polling())
    loop.run_forever()