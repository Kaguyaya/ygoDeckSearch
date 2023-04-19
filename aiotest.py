import aiohttp
import asyncio
import os
from urllib.parse import unquote
from lxml import etree
from PIL import Image
from pathlib import Path
import requests
import re
import os
async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, 'https://www.masterduelmeta.com/top-decks/diamond-i/april-2023/tearlaments/brock/LsYbU')
        demo=etree.HTML(html)
        div=demo.xpath('//div[@class="svelte-16h7w79"]')
        for i in div:
            amounts=i.xpath('./div/img/@alt')
            amounts=("".join(amounts)).split(' copies')[0]
            href=i.xpath('./a/@href')
            href="".join(href)
            url_encode=unquote(href,'utf-8')
            url_spi=url_encode.split('/',2)[2]
            await (en_to_cn(url_spi))
            if(amounts==""):
                print(url_spi+" ×1")
            else:
                print(url_spi+" ×"+amounts)
        # href=demo.xpath('//a[@class="image-wrapper svelte-1xqpccf"]/@href')
        # names=[]
        # for i in href:
        #     url_encode=unquote(i,'utf-8')
        #     url_spi=url_encode.split('/',2)[2]
        #     names.append(url_spi)
        #     # print(url_spi)
        # print(names)

        # amouts=demo.xpath('//img[@class="card-amount svelte-1xqpccf"]/@alt')
        # print(amouts)

        # imgs=demo.xpath('//img[@class="card-img full-width svelte-1xqpccf"]/@alt')
        # img_url=[]
        # for img in imgs:
        #     img_url.append("https://s3.duellinksmeta.com/cards/"+img+"_w200.webp")
        # for imgurl in img_url:
        #     print(await down_img(session, imgurl))
        # await webp_to_jpg()
        # for i in img_url:
            # print(i)
        # img_url=https://s3.duellinksmeta.com/cards/"name"_w100.webp
        # for n in name:
        #     print()
        # t=etree.tostring(demo,encoding="utf-8",pretty_print=True)
        # print(html)
# async def down_img(session,url):
#     name=url.split('/')[-1]
#     img=await session.get(url)
#     content =await img.read()
#     with open('./picture/'+str(name),'wb')as f:
#         # 写入至文件
#         f.write(content)
#         print(f'{name} 下载完成！')
#         return str(url)
# async def webp_to_jpg():
#     file="./picture"
#     picture=[]
#     for root,dirs,files in os.walk(file):
#         for file in files:
#             path=os.path.join(root,file)
#             img=Image.open(path)
#             image=img.convert('RGB')
#             image.save("./picture/"+file.split(".")[0]+".jpg")

async def en_to_cn(key:str):
    url=f"https://ygocdb.com/?search={key}"
    print(key)
    async with aiohttp.ClientSession()as session:
        c= await fetch(session, url)
        demo=etree.HTML(c)
        # print(demo)
        cnName=demo.xpath("/html/body/main/div/div[2]/div[2]/h2/span/text()")
        print(cnName)
        # return cnName
asyncio.run(main())
