import asyncio
import datetime
from aiogram import types
from loader import dp
from telethon.sync import TelegramClient
from telethon import functions, types as telethon_types
from loader import db

# Telethon API credentials
api_id = 24247088
api_hash = "b333a8fc15fd30ebdfa70c153731cf8f"

# Delay between messages (in seconds)
MESSAGE_TIMEOUT = 5

async def send_random_messages():
    print("Starting scheduled task to send random messages.")

    if db.pool is None:
        await db.create()
    commands = await db.get_select_commands()
    async with TelegramClient("session_name", api_id, api_hash) as client:
        try:
            for command in commands:
                commander = await db.get_staff(int(command["command_staff_id"]))
                staff = await db.get_staff(int(command["staff_id"]))

                if not staff:
                    print(f"Staff with id {command['staff_id']} not found.")
                    continue  # Skip if no staff found
                try:
                    result = await client(functions.contacts.ImportContactsRequest(
                        contacts=[telethon_types.InputPhoneContact(
                            client_id=0,
                            phone=staff["telegram_id"],
                            first_name=staff["name"],
                            last_name=""
                        )]
                    ))

                    if result and result.users:
                        user_entity = result.users[0]
                    else:
                        raise ValueError(f"Could not find a Telegram user for {staff['name']}.")

                    # Format the `time_limit` field
                    time_limit = command.get("time_limit", None)
                    if isinstance(time_limit, datetime.datetime):
                        formatted_time_limit = time_limit.strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        formatted_time_limit = "N/A"

                    # Construct the message
                    message_text = (
                        f"<b>📲Ynagi topshiriq</b>\n"
                        f"<b>🧑‍💼Topshiriq yuboruvchi: </b>{commander['name']}\n"
                        f"<b>⌚️Topshiriq bajarish muddati: </b>{formatted_time_limit}\n"
                        f"<b>🔉Topshiriq mazmuni: </b>{command['text']} \n"                        
                        f"Topshiriq haqida batafsil ma'lumot olish va bajarish uchun, Iltimos mobil ilovaga kiring."
                    )

                    # Send the message
                    await client.send_message(user_entity, message_text, parse_mode="html")
                    print(f"Message sent to {staff['telegram_id']}")
                    await db.set_command_status(int(command["id"]))
                    # Add delay between messages
                    await asyncio.sleep(MESSAGE_TIMEOUT)

                except Exception as e:
                    print(f"Error sending message to {staff['telegram_id']}: {e}")

        except Exception as e:
            print(f"Error during message sending: {e}")


# Scheduler function


