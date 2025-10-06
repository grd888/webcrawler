from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import asyncio
import aiohttp


class AsyncCrawler:
    def __init__(self, base_url, max_concurrent = 3, max_pages = 10):
        self.base_url = base_url
        self.base_domain = urlparse(base_url).netloc
        self.page_data = {}
        self.lock = asyncio.Lock()
        self.max_concurrency = max_concurrent
        self.max_pages = max_pages
        self.should_stop = False
        # initialize all_tasks with an empty set
        self.all_tasks = set()
        self.semaphore = asyncio.Semaphore(self.max_concurrency)
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def add_page_visit(self, normalized_url):
        async with self.lock:
            if normalized_url in self.page_data:
                return False
            else:
                return True

    async def get_html(self, url):
        if self.should_stop:
            return False
        if len(self.page_data) >= self.max_pages:
            self.should_stop = True
            print("Reached maximum number of pages to crawl.")
            for task in self.all_tasks:
                task.cancel()
            return False
        
        try:
            async with self.session.get(
                url, headers={"User-Agent": "BootCrawler/1.0"}
            ) as r:
                if r.status >= 400:
                    raise Exception(f"Failed to fetch {url}")
                if not r.headers.get("Content-Type", "").startswith("text/html"):
                    raise Exception(f"Content-Type is not text/html: {url}")
                return await r.text()
        except Exception as e:
            print(f"Failed to crawl {url}: {str(e)}")
            return None

    async def crawl(self):
        """Start crawling from base_url and return the page_data dictionary."""
        await self.crawl_page(self.base_url)
        return self.page_data

    async def crawl_page(self, current_url):
        if self.should_stop:
            return
        # Check if URL is in same domain
        current_domain = urlparse(current_url).netloc
        if self.base_domain != current_domain:
            return

        # Normalize and check if already visited
        normalized_url = normalize_url(current_url)
        is_new = await self.add_page_visit(normalized_url)
        if not is_new:
            return

        try:
            print(f"Crawling {current_url}")

            # Limit concurrent requests with semaphore
            async with self.semaphore:
                # Fetch HTML
                html = await self.get_html(current_url)
                if html is None:
                    return

                # Extract page data
                page_info = extract_page_data(html, current_url)

                # Add page data to dictionary using lock
                async with self.lock:
                    self.page_data[normalized_url] = page_info

                # Extract new URLs
                urls = get_urls_from_html(html, self.base_url)

            # Create tasks for each URL (outside semaphore to avoid deadlock)
            tasks = []
            for url in urls:
                task = asyncio.create_task(self.crawl_page(url))
                tasks.append(task)

            # Wait for all tasks
            if tasks:
              await asyncio.gather(*tasks)

        except Exception as e:
            print(f"Failed to crawl {current_url}: {str(e)}")


async def crawl_site_async(base_url, max_concurrent, max_pages):
    async with AsyncCrawler(base_url, max_concurrent, max_pages) as crawler:
        return await crawler.crawl()


def normalize_url(url):
    parsed_url = urlparse(url)
    netloc = parsed_url.netloc
    path = parsed_url.path
    full_path = netloc + path
    full_path = full_path.rstrip("/")
    return full_path


def get_h1_from_html(html):
    soup = BeautifulSoup(html, "html.parser")
    h1 = soup.find("h1")
    return h1.get_text(strip=True) if h1 else ""


def get_first_paragraph_from_html(html):
    soup = BeautifulSoup(html, "html.parser")
    main = soup.find("main")
    if main:
        p = main.find("p")
    else:
        p = soup.find("p")

    return p.get_text(strip=True) if p else ""


def get_urls_from_html(html, base_url):
    urls = []
    soup = BeautifulSoup(html, "html.parser")
    anchors = soup.find_all("a")

    for anchor in anchors:
        if href := anchor.get("href"):
            try:
                absolute_url = urljoin(base_url, href)
                urls.append(absolute_url)
            except Exception as e:
                print(f"{str(e)}: {href}")

    return urls


def get_images_from_html(html, base_url):
    image_urls = []
    soup = BeautifulSoup(html, "html.parser")
    images = soup.find_all("img")

    for img in images:
        if src := img.get("src"):
            try:
                absolute_url = urljoin(base_url, src)
                image_urls.append(absolute_url)
            except Exception as e:
                print(f"{str(e)}: {src}")

    return image_urls


def extract_page_data(html, page_url):
    return {
        "url": page_url,
        "h1": get_h1_from_html(html),
        "first_paragraph": get_first_paragraph_from_html(html),
        "outgoing_links": get_urls_from_html(html, page_url),
        "image_urls": get_images_from_html(html, page_url),
    }
