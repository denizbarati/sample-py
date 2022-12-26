import asyncio
from bscscan import BscScan
from tech_test.core.config import settings

async def get_balance(address):
  async with BscScan(settings.bsc_api_key) as bsc:
      result = await bsc.get_bnb_balance(address=address)
      return {"result:":result}

if __name__ == "__main__":
  asyncio.run(main())