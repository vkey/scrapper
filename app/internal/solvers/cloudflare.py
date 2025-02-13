from playwright._impl._page import Page
import logging


class CloudflareSolver:
    ACCESS_DENIED_TITLES = [
        # Cloudflare
        'Access denied',
        # Cloudflare http://bitturk.net/ Firefox
        'Attention Required! | Cloudflare'
    ]
    ACCESS_DENIED_SELECTORS = [
        # Cloudflare
        'div.cf-error-title span.cf-code-label span',
        # Cloudflare http://bitturk.net/ Firefox
        '#cf-error-details div.cf-error-overview h1'
    ]
    CHALLENGE_TITLES = [
        # Cloudflare
        'Just a moment...',
        # DDoS-GUARD
        'DDoS-Guard'
    ]
    CHALLENGE_SELECTORS = [
        # Cloudflare
        '#cf-challenge-running', '.ray_id', '.attack-box', '#cf-please-wait', '#challenge-spinner', '#trk_jschal_js',
        '#turnstile-wrapper', '.lds-ring',
        # Custom CloudFlare for EbookParadijs, Film-Paleis, MuziekFabriek and Puur-Hollands
        'td.info #js_info',
        # Fairlane / pararius.com
        'div.vc div.text-box h2'
    ]
    @staticmethod
    async def is_blocked(page: Page) -> bool:
        page_title = await page.title()
        # find access denied titles
        for title in CloudflareSolver.ACCESS_DENIED_TITLES:
            if title == page_title:
                return True
        # find access denied selectors
        for selector in CloudflareSolver.ACCESS_DENIED_SELECTORS:
            found_elements = await page.query_selector_all(selector)
            if len(found_elements) > 0:
                return True
        return False

    @staticmethod
    async def is_challenge(page: Page) -> bool:
        page_title = await page.title()
        challenge_found = False
        for title in CloudflareSolver.CHALLENGE_TITLES:
            if title.lower() == page_title.lower():
                challenge_found = True
                logging.info("Challenge detected. Title found: " + page_title)
                break
        if not challenge_found:
            # find challenge by selectors
            for selector in CloudflareSolver.CHALLENGE_SELECTORS:
                found_elements = await page.query_selector_all(selector)
                if len(found_elements) > 0:
                    challenge_found = True
                    logging.info("Challenge detected. Selector found: " + selector)
                    break
        return challenge_found

    @staticmethod
    async def solve_challenge(page: Page):
        try:
            element = await page.query_selector("//h1[./img]/following-sibling::div[.//input]")
            if element is None:
                raise Exception("Елемент не знайдено")
            bounding_box = await element.bounding_box()
            if bounding_box is None:
                raise Exception("Не вдалося отримати bounding box елемента")
            x = bounding_box["x"]
            y = bounding_box["y"]
            for offset in range(0, 101, 10):
                current_y = y + offset
                await page.mouse.click(x, current_y)
        except Exception as e:
            logging.error(f"Failed to click on the challenge widget input: {e}")
