import asyncio
from pprint import pprint

import genshin


def print_history(history: list[genshin.models.Wish]):
    sorted_list = sorted([wish for wish in history], key=lambda x: x.time, reverse=True)
    for wish in sorted_list:
        print(f"{wish.time} - {wish.name} ({wish.rarity}* {wish.type}) {wish.id}")


async def main():
    # client = genshin.Client(
    #     {
    #         'ltoken': 'wK7nikcpE5hdtXIfiZQ8aNt9zb88TyuqLbPoO7Oz',
    #         'ltuid': 48912504,
    #     },
    #     game=genshin.Game.GENSHIN
    # )
    #
    # try:
    #     reward = await client.claim_daily_reward()
    # except genshin.AlreadyClaimed:
    #     print("Daily reward already claimed")
    # else:
    #     print(f"Claimed {reward.amount}x {reward.name}")

    print(genshin.utility.get_authkey())

    # client.authkey = genshin.utility.extract_authkey(
    #     'https://webstatic-sea.hoyoverse.com/genshin/event/e20190909gacha-v2/index.html?win_mode=fullscreen'
    #     '&authkey_ver=1&sign_type=2&auth_appid=webview_gacha&init_type=301&gacha_id'
    #     '=a489e839c5180f4c241cd9df7f8b88a689ddce6d&timestamp=1667348059&lang=ru&device_type=pc&game_version=OSRELWin3'
    #     '.2.0_R11468593_S11212885_D11498071&plat_type=pc&region=os_euro&authkey=04Ppi3lcrLCYSFLi1wuqLfP7PmhHeVy'
    #     '%2fuQMTMEcW7wM0LQkzHZ7EO5atKJUVUOJ%2b00bicf72cbT04%2fovwKe9%2fPDR8vits9auibnHDJXajtm3qG1o5YyjXuN0fzdXap'
    #     '%2fqgQLhltarCbyl54pyb8MHeO%2bMrucRGOm6938fmDc3gtSzHsN1l66IBYoVMutdwdk49phWk2jx8BhCllIDBJm'
    #     '%2fjIT9oxhmJ34OaTTuJk%2fRXZVSFOQrxQHohbWaItikRx%2bwM9LhbrPc0lYZZByyf7x5BktOeQcvpw1lQYtBud2KiBFXLM7sa0dgD3No'
    #     '%2bk6JB%2fYfSGfSEKjD541Gj0Nh1ZI3Ed%2fhYdZit%2bJU212z4FqMhdhivH47FMcQ9pi894pidlvRKhgbOdB'
    #     '%2fZLIW5onw08eRXdBoic1lhz438D3TNpZnNA56ljnQQ2kRvUr'
    #     '%2fXR0BstlX8iDUYISRjg0wNxALZqlfc5LXDIDhuArbwBqaOjZ6KPGEx856SXfCqFugienFEko%2bgnu2I7M9Aj2HYoYSKwF5%2bV'
    #     '%2b81j7fuTMPipVguCuruh2rLJ2ce042Y%2fQ3Ls65SWmUeiLirvBtIEyKRwouCBBxw9CniKegWASd6S0q'
    #     '%2bzzNISlilvqAsnrvkiFc3koSerCj6Shygk5kaxMvUTDph2fXWghRcFRHZKBMQCGRQ14M%2fMIO8x7j%2bIKGJfYyzi8UuOv'
    #     '%2blZCIhCUr6kasKlBuTmxEu6qAlctp6j82bz%2flLDIkGwppeB2pbXHJNsBeBzmeYUXUfw8TIp3Nir6FPwOjPDCc7axGbByS3P'
    #     '%2bhk8tR0t0fKzZpjRrxoG76NcF%2ffNZl%2fJRgwsLTkQTprsGabJceq%2f2xFx7tTO3kw%2fuXdTzFj'
    #     '%2fet031Cq61l9C00b7mJZ17skYJc%2bBHg6FBwmZnxv%2bncR0NS3FtHyCJD2WXwmVBZO5L'
    #     '%2fO0XiJsWo5zjY35aAV8RzLaFgH9nA6QNLgzUC4tc0qHjQ1Wr4aKBy7Z5lh8vM5bg9L%2b9gjGon2qBs%2fqFdRCP1Hg8Ms5Wt%2f'
    #     '%2bQsQiB8DpenoPJsrxfH7yksDIvNS1Vj8rhIvC924xIYtkpPP%2b9Gn%2f57KABSmWn10ivpdaegALpuzUqrE%2faF0kbOMGe'
    #     '%2fohjqK5xU07RPX%2b'
    #     '%2f6HlOjI1eGWScta5utbwJCQhVvPFy0jjiAn1upuqmCYB2YQt411mwE0zFzfqYyk2CQFyTtW3Jmslw9w24KPy9tHggp2OE4Aljznu7wYO3x7r'
    #     'VvMfj%2fITQPIo3mqXh0pTM%2bXmEgq0SUxHRMqnKX%2b%2f5CepZUdeqRn7ISoh4EKYDxmlGEnZD2mx%2bYXPeWKutGDWUmhi9HPQa0Vw47VN'
    #     'AeffZRVZMTmdz81Jj1tjGm5g%3d%3d&game_biz='
    # )
    #
    # history = await client.wish_history(limit=200, end_id=1665828360000574913).flatten()
    # print_history(history)
    #
    # print('-------------------------------------------------------------')
    #
    # full_history = await client.wish_history(limit=200).flatten()
    # print_history(full_history)
    # print(len(full_history))


if __name__ == '__main__':
    asyncio.run(main())
