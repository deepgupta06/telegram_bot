#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import datetime
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import os
import glob
from setting import _TOKEN, _PROFILE_ROOT_DIR
import shutil

def config_log(filename):
    logging.basicConfig(
        filename=f"../local/log/{filename}.log",
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )
    # set higher logging level for httpx to avoid all GET and POST requests being logged
    logging.getLogger("httpx").setLevel(logging.WARNING)

    logger = logging.getLogger(__name__)
    return logger

class InstaProfile:
    def __init__(self, profile_name):
        self.profile = profile_name
        self.profile_dir = _PROFILE_ROOT_DIR
        self.content_dir = os.path.join(self.profile_dir, self.profile, "content")
        self.posts_dir = os.path.join(self.profile_dir, self.profile, "content", "posts")
        self.reels_dir = os.path.join(self.profile_dir, self.profile, "content", "reels")
        self.captions_dir = os.path.join(self.profile_dir, self.profile, "content", "captions")
        self.archive_dir = os.path.join(self.profile_dir, self.profile, "content", "archive")
    
    def get_catagory(self, conten_type:str):
        content_path = os.path.join(self.content_dir, conten_type)
        all_content_type = [x.split(".")[0].split()[0] for x in os.listdir(content_path)]
        all_content_type = list(set(all_content_type))
        return all_content_type
        
    
    def get_post_path(self, name='common', number_of_post = 4):
        print(os.path.join(self.posts_dir,f'{name}*.png'))
        posts_path = glob.glob(os.path.join(self.posts_dir,f'{name}*.png'))
        print(posts_path)
        return posts_path[:number_of_post]
    
    def get_reel_path(self, name='common', number_of_reels = 4):
        print(os.path.join(self.reels_dir,f'{name}*.mp4'))
        reel_path = glob.glob(os.path.join(self.reels_dir,f'{name}*.mp4'))
        print(reel_path)
        return reel_path[:number_of_reels]
    
    def get_caption_path(self, name='common', number_of_caption = 4):
        print(os.path.join(self.captions_dir,f'{name}*.mp4'))
        reel_path = glob.glob(os.path.join(self.captions_dir,f'{name}*.mp4'))
        print(reel_path)
        return reel_path[:number_of_caption]
    
    def move_content_to_archive(self, content_path):
        filename = os.path.basename(content_path)
        dst_filepath = os.path.join(self.archive_dir, filename)
        shutil.move(src=content_path, dst=dst_filepath)
    




profilename = None
instaprofile = None


async def getinfo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global profilename
    global instaprofile
    command = update.message.text
    
    if ("profile" in command):
        
        profilename = command.split()[1]
        instaprofile = InstaProfile(profilename)
        await update.message.reply_text(f"{profilename}")
    
    if "gettype" in command:
        if not profilename:
            await update.message.reply_text(f"Please provide a profilename first")
        else:
            if "reel" in command:
                content_types = instaprofile.get_catagory("reels")
                
            elif "post" in command:
                content_types = instaprofile.get_catagory("posts")
            elif "caption" in command:
                content_types = instaprofile.get_catagory("captions")
            type_string = "\n".join(content_types)
            await update.message.reply_text(type_string)
    
    if "getpost" in command:
        if not profilename:
            await update.message.reply_text(f"Please provide a profilename first")
        else:
            command_info = command.split()
            if len(command_info) == 3:
                command = command_info[0]
                content_name = command_info[1]
                content_count = command_info[2]
            else:
                content_name = "common"
                content_count = 1
                
            post_paths = instaprofile.get_post_path(name=content_name, number_of_post=int(content_count))
            await update.message.reply_text(f"Postname:{content_name}, Post count:{content_count}")
            for post_path in post_paths:
                if os.path.exists(post_path):
                    with open(post_path, 'rb') as photo_file:
                        await update.message.reply_photo(photo=photo_file)                        
                else:
                    update.message.reply_text(f"{post_path}---- Not Available")
            #
            for content_path in post_paths:
                instaprofile.move_content_to_archive(content_path)
    if "getreel" in command:
        if not profilename:
            await update.message.reply_text(f"Please provide a profilename first")
        else:
            command_info = command.split()
            if len(command_info) == 3:
                command = command_info[0]
                content_name = command_info[1]
                content_count = command_info[2]
            else:
                content_name = "common"
                content_count = 1
                
            reels_paths = instaprofile.get_reel_path(name=content_name, number_of_reels=int(content_count))
            await update.message.reply_text(f"Reel name:{content_name}, Reels count:{content_count}")
            for reel_path in reels_paths:
                if os.path.exists(reel_path):
                    with open(reel_path, 'rb') as reel_file:
                        await update.message.reply_video(video=reel_file)                        
                else:
                    update.message.reply_text(f"{reel_path}---- Not Available")
            #
            for content_path in reels_paths:
                instaprofile.move_content_to_archive(content_path)
        


            
            
"""    user = update.effective_user
    logger.info(f"{user}:{update.message.text}")
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )"""
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Echo the user message."""
        await update.message.reply_text(update.message.text)
async def send_local_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a local photo when the /localphoto command is issued."""
    # Replace 'path_to_your_photo.jpg' with the path to your local photo file
    photo_path = r'C:\Users\deepg\Downloads\austin-wilcox-z_U6bPp_Rjg-unsplash.jpg'
    with open(photo_path, 'rb') as photo_file:
        await update.message.reply_photo(photo=photo_file)

async def send_local_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a local photo when the /localphoto command is issued."""
    # Replace 'path_to_your_photo.jpg' with the path to your local photo file
    video_path = r'C:\Users\deepg\Downloads\pexels-anna-nekrashevich-7550763 (Original).mp4'
    with open(video_path, 'rb') as video_file:
        await update.message.reply_video(video=video_file)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


def main() -> None:
    present_time = datetime.datetime.now()
    logfilename = present_time.strftime("BOT_%Y%m%d")
    logger = config_log(logfilename)
    application = Application.builder().token(_TOKEN).build()
    #application.add_handler(CommandHandler("getinfo", getinfo))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("photo", send_local_photo))
    application.add_handler(CommandHandler("video", send_local_video))
    #application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, getinfo))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()