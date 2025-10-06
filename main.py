import sys
import asyncio
from crawl import crawl_site_async

async def main():
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    elif len(sys.argv) > 4:
        print("too many arguments provided")
        sys.exit(1)
    else:
        BASE_URL = sys.argv[1]
        MAX_CONCURRENT = int(sys.argv[2])
        MAX_PAGES = int(sys.argv[3])
        print(f"starting crawl of: {BASE_URL}")
        page_data = await crawl_site_async(BASE_URL, MAX_CONCURRENT, MAX_PAGES)

        print(f"Found {len(page_data)} pages:")
        for page in page_data.values():
            print(f"- {page['url']}: {len(page['outgoing_links'])} outgoing links")


if __name__ == "__main__":
    asyncio.run(main())
