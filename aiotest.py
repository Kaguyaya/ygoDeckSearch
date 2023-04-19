import aiohttp
import asyncio
import os
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
        # html = await fetch(session, 'https://www.masterduelmeta.com/top-decks/diamond-i/april-2023/tearlaments/brock/LsYbU')
        # demo=etree.HTML(html)
        # imgs=demo.xpath('//img[@class="card-img full-width svelte-1xqpccf"]/@alt')
        # img_url=[]
        # for img in imgs:
        #     img_url.append("https://s3.duellinksmeta.com/cards/"+img+"_w200.webp")
        # for imgurl in img_url:
        #     print(await down_img(session, imgurl))
        await webp_to_jpg()
        # for i in img_url:
            # print(i)
        # img_url=https://s3.duellinksmeta.com/cards/"name"_w100.webp
        # for n in name:
        #     print()
        # t=etree.tostring(demo,encoding="utf-8",pretty_print=True)
        # print(html)
async def down_img(session,url):
    name=url.split('/')[-1]
    img=await session.get(url)
    content =await img.read()
    with open('./picture/'+str(name),'wb')as f:
        # 写入至文件
        f.write(content)
        print(f'{name} 下载完成！')
        return str(url)
async def webp_to_jpg():
    file="./picture"
    picture=[]
    for root,dirs,files in os.walk(file):
        for file in files:
            path=os.path.join(root,file)
            img=Image.open(path)
            image=img.convert('RGB')
            image.save("./picture/"+file.split(".")[0]+".jpg")

asyncio.run(main())
