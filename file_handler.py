import os
import io
import math
from discord import Message
import discord
import cipher

chunk_size = 25559 * 1024

async def upload_chunks(file, file_name, file_size, channel) -> None:
    message_ids = []
    num_chunks = math.ceil(file_size/chunk_size)
        
    # Upload chunks
    for i in range(0, num_chunks):
        chunk = cipher.encrypt(file.read(chunk_size))
        file.seek(chunk_size*(i+1))
        chunk_file = io.BytesIO(chunk)
        chunk_file.name = f"{file_name}_chunk{i}.bin"
        
        msg = await channel.send(file=discord.File(chunk_file))
        message_ids.append(msg.id)

    # Produce metadata
    # Metadata notes
    """
        Line 1: original file name
        Line 2: file extension
        Line 3 and onwards: message ids
    """
    metadata_content = f"{file_name.split(".")[0]}\n{file_name.split(".")[1]}\n" + "\n".join(map(str, message_ids))
    metadata_file = io.BytesIO(cipher.encrypt(metadata_content.encode()))
    metadata_file.name = f"{file_name}_metadata.bin"

    msg = await channel.send(file=discord.File(metadata_file))
    return msg.id

"""
async def upload_chunks(file, channel) -> None:
    raw_data = bytes()
    message_ids = []
    num_chunks = math.ceil(os.path.getsize(file)/chunk_size)
    
    async def sendFile(file_name: str):
        msg = await channel.send(file=discord.File(file_name))
        message_ids.append(msg.id)
        os.remove(file_name)

    # Read raw data of file
    with open(file, "rb") as f:
        raw_data = f.read()

    # Produce chunks
    for i in range(0, num_chunks):
        chunk = cipher.encrypt(raw_data[i * chunk_size: (i + 1) * chunk_size])

        with open(f"{file}_chunk{i}.bin", "wb") as f:
            f.write(chunk)

        await sendFile(f"{file}_chunk{i}.bin")
        print(f"Uploaded {round(float(((i+1)/num_chunks)*100), 1)}%...")

    # Produce metadata
    # Metadata notes
    
        Line 1: original file name
        Line 2: file extension
        Line 3 and onwards: message ids
    
    with open(f"{file}_metadata.txt", "w") as f:
        print("Uploading metadata...")
        f.writelines([f"{os.path.splitext(file)[0]}\n", f"{os.path.splitext(file)[1]}\n"])
        for i in message_ids:
            f.write(f"{i}\n")

    await sendFile(f"{file}_metadata.txt")
"""



"""
async def download_file(mtd_msg, channel) -> None:
    raw_data = bytes()
    to_read = []
    mtd_filename = None
    og_filename, og_ext = "", ""

    for a in mtd_msg.attachments:
        await a.save(a.filename)
        mtd_filename = a.filename

    with open(mtd_filename, "r") as f:
        for i in f.readlines():
            to_read.append(i[:-1])
        og_filename, og_ext = to_read.pop(0), to_read.pop(0)
    os.remove(mtd_filename)
    
    count = 1
    for i in to_read:
        chunk_msg = await channel.fetch_message(i)
        for a in chunk_msg.attachments:
            await a.save(a.filename)
            with open(a.filename, "rb") as f:
                raw_data += cipher.decrypt(f)
            os.remove(a.filename)
        print(f"Retrieved {round(float((count/len(to_read))*100), 1)}%...")
        count += 1

    with open(f"{og_filename}_download{og_ext}", "wb") as f:
        print("Downloading to system...")
        f.write(raw_data)
"""