import aiohttp
import nonebot.plugin
import nonebot
from nonebot.adapters.onebot.v11 import Bot,Message,MessageSegment,PrivateMessageEvent,GroupMessageEvent,GROUP_ADMIN,GROUP_OWNER,Event
from nonebot.plugin import on_regex
from nonebot.plugin import on_keyword
from lxml import etree

deck=on_keyword(['/deck'])
@deck.handle()
async def deckMethod(bot: Bot,event: Event):
    print("decktest")
    # key =str(event.message).strip()[3:].strip()
    imgs=(await main())
    msg=None
    print(imgs)
    for data in imgs:
        msg+=MessageSegment.image(data)
    if isinstance(event,GroupMessageEvent):
        await send_forward_msg_group(bot,event,"阴影",msg if msg else ["空"])
    elif isinstance(event,PrivateMessageEvent):
        await bot.send(event=event,message =msg if msg else "空")

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    async with aiohttp.ClientSession() as session:
        html = await fetch(session,'https://www.masterduelmeta.com/top-decks/diamond-i/april-2023/tearlaments/brock/LsYbU')
        demo = etree.HTML(html)
        imgs = demo.xpath('//img[@class="card-img full-width svelte-1xqpccf"]/@alt')
        img_url = []
        for img in imgs:
            img_url.append("https://s3.duellinksmeta.com/cards/" + img + "_w200.webp")
        return img_url


# 合并消息
async def send_forward_msg_group(
        bot: Bot,
        event: GroupMessageEvent,
        name: str,
        msgs: [],
):
    def to_json(msg):
        return {"type": "node", "data": {"name": name, "uin": bot.self_id, "content": msg}}
    messages = [to_json(msg) for msg in msgs]
    await bot.call_api(
        "send_group_forward_msg", group_id=event.group_id, messages=messages
    )

# 合并单独消息
async def send_forward_msg_person(
        bot: Bot,
        event: PrivateMessageEvent,
        name: str,
        msgs: [],
):
    def to_json(msg):
        return {"type": "node", "data": {"name": name, "uin": bot.self_id, "content": msg}}
    messages = [to_json(msg) for msg in msgs]
    await bot.call_api(
        "send_private_forward_msg", user_id=event.user_id, messages=messages
    )