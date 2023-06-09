import aiohttp
import nonebot.plugin
import nonebot
from urllib.parse import unquote
from nonebot.adapters.onebot.v11 import Bot,Message,MessageSegment,PrivateMessageEvent,GroupMessageEvent,GROUP_ADMIN,GROUP_OWNER,Event
from nonebot.plugin import on_regex
from nonebot.plugin import on_keyword
from lxml import etree

deck=on_keyword(['/deck','卡组'])
@deck.handle()
async def deckMethod(bot: Bot,event: Event):
    ####img#####
    # key =str(event.message).strip()[3:].strip()
    # imgs=(await main())
    # msg=None
    # print(imgs)
    # for data in imgs:
    #     msg+=MessageSegment.image(data)
    # if isinstance(event,GroupMessageEvent):
    #     await send_forward_msg_group(bot,event,"阴影",msg if msg else ["空"])
    # elif isinstance(event,PrivateMessageEvent):
    #     await bot.send(event=event,message =msg if msg else "空")

####msg####
    msg=(await main())
    # print(msg)
    if isinstance(event,GroupMessageEvent):
        await bot.send(event=event, message=msg if msg else "空")
        # await send_forward_msg_group(bot,event,"阴影",msg if msg else ["空"])
    elif isinstance(event,PrivateMessageEvent):
        await bot.send(event=event,message =msg if msg else "空")
async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    ##图片版##
    # async with aiohttp.ClientSession() as session:
    #     html = await fetch(session,'https://www.masterduelmeta.com/top-decks/diamond-i/april-2023/tearlaments/brock/LsYbU')
    #     demo = etree.HTML(html)
    #     imgs = demo.xpath('//img[@class="card-img full-width svelte-1xqpccf"]/@alt')
    #     img_url = []
    #     for img in imgs:
    #         img_url.append("https://s3.duellinksmeta.com/cards/" + img + "_w100.webp")
    #     return img_url

    ##文字版##
    async with aiohttp.ClientSession() as session:
        html = await fetch(session,'https://www.masterduelmeta.com/top-decks/diamond-i/april-2023/tearlaments/brock/LsYbU')
        demo = etree.HTML(html)
        div = demo.xpath('//div[@class="svelte-16h7w79"]')
        msg = ""
        for i in div:
            amounts = i.xpath('./div/img/@alt')
            amounts = ("".join(amounts)).split(' copies')[0]
            href = i.xpath('./a/@href')
            href = "".join(href)
            url_encode = unquote(href, 'utf-8')
            url_spi = url_encode.split('/', 2)[2]
            name=await (en_to_cn(url_spi))
            if (amounts == ""):
                msg = msg + name + " ×1\n"
            else:
                msg = msg + name + " ×" + amounts + "\n"
        # print(msg)
        return msg


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
async def en_to_cn(key:str):
    url=f"https://ygocdb.com/?search={key}"
    async with aiohttp.ClientSession()as session:
        c=await fetch(session, url)
        demo=etree.HTML(c)
        cnName=demo.xpath("/html/body/main/div/div[2]/div[2]/h2/span/text()")
        return "".join(cnName)