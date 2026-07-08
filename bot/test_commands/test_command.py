# -*- coding: utf-8 -*-
"""
@File    : test_command.py
@Time    : 2026/4/13 下午 06:03
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    :
"""


import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional # 引入 Optional 以提供更精確的型別提示

from bot.core import BaseCog

# --- 表單 Modal ---

class RegisterModalPage1(discord.ui.Modal, title="報名表單 - 第 1 頁"):
    """第一頁的表單 Modal。送出後會嘗試透過私訊傳送下一步。"""
    name = discord.ui.TextInput(
        label="姓名",
        placeholder="請輸入姓名",
        max_length=50,
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        page1_data: dict[str, str | int] = {
            "user_id": interaction.user.id,
            "user_name": str(interaction.user),
            "name": self.name.value,
        }

        # 【關鍵點 1】嘗試透過私訊 (DM) 傳送「下一步」按鈕給使用者
        try:
            await interaction.user.send(
                content="第一頁已完成，請點擊下方「下一步」繼續填寫第二頁。",
                view=RegisterNextStepView(page1_data=page1_data)
            )
            # 如果私訊成功，在原頻道用 ephemeral 訊息提醒使用者去收信
            await interaction.response.send_message(
                content="✅ 已將第二頁的報名連結傳送至您的「私訊」，請前往查看！",
                ephemeral=True
            )
        except discord.Forbidden:
            # 【錯誤處理】如果使用者關閉了陌生私訊功能，則無法發送
            await interaction.response.send_message(
                content="❌ 無法傳送私訊給您！請至「使用者設定 ➔ 隱私與安全」中，開啟「允許伺服器成員傳送私人訊息」後再試一次。",
                ephemeral=True
            )


class RegisterModalPage2(discord.ui.Modal, title="報名表單 - 第 2 頁"):
    """第二頁的表單 Modal。送出後會移除私訊中的按鈕。"""
    def __init__(
        self,
        page1_data: dict,
        next_step_message: discord.Message,
    ) -> None:
        super().__init__()
        self.page1_data: dict = page1_data
        self.next_step_message: discord.Message = next_step_message

    food = discord.ui.TextInput(
        label="是否用餐",
        placeholder="例如：是 / 否",
        max_length=10,
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        final_data: dict = {
            **self.page1_data,
            "food": self.food.value,
        }

        # TODO: 之後可以改成寫入 SQLite / Google Sheet
        print("收到報名資料：")
        print(final_data)

        # 1. 先回覆第二頁 Modal 的送出結果
        await interaction.response.send_message(
            content=(
                "🎉 報名完成，資料已成功送出！\n\n"
                f"姓名：{final_data.get('name', '未填寫')}\n"
                f"是否用餐：{final_data.get('food', '未填寫')}"
            ),
            ephemeral=True, # 這裡用 ephemeral 是因為只是個短暫的成功提示
        )

        # 2. 【關鍵點 2】編輯私訊中帶有按鈕的那則訊息，將 view 設為 None 來徹底移除按鈕
        #    因為 next_step_message 是個實體訊息，所以可以隨時編輯。
        if self.next_step_message is not None:
            try:
                await self.next_step_message.edit(
                    content="✅ 已完成第二步，報名流程已結束。",
                    view=None,  # 這行是讓按鈕從私訊中消失的關鍵
                )
            except discord.HTTPException as e:
                print(f"編輯私訊中的按鈕訊息失敗: {e}")


# --- 按鈕 View ---

class RegisterNextStepView(discord.ui.View):
    """在私訊中顯示的「下一步」按鈕。"""
    def __init__(self, page1_data: dict) -> None:
        # timeout=None 讓按鈕永不逾時，使用者可以隨時回來填寫
        super().__init__(timeout=None)
        self.page1_data: dict = page1_data

    @discord.ui.button(
        label="下一步",
        style=discord.ButtonStyle.primary,
        custom_id="register_next_step_button",
    )
    async def next_step(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ) -> None:
        # 【關鍵點 3】因為這是在私訊中，interaction.message 絕對會是那則包含按鈕的「實體訊息」
        # 我們可以把它傳給下一頁的 Modal，以便之後進行編輯。
        next_step_message: discord.Message = interaction.message

        await interaction.response.send_modal(
            RegisterModalPage2(
                page1_data=self.page1_data,
                next_step_message=next_step_message,
            )
        )


class RegisterStartView(discord.ui.View):
    """在伺服器頻道中顯示的初始「我要報名」按鈕。"""
    def __init__(self) -> None:
        # timeout=None 讓這個面板永久存在於頻道上
        super().__init__(timeout=None)

    @discord.ui.button(
        label="我要報名",
        style=discord.ButtonStyle.success,
        custom_id="register_start_button",
    )
    async def register_start(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ) -> None:
        # 按下按鈕後，彈出第一頁的 Modal
        await interaction.response.send_modal(RegisterModalPage1())


# --- Cog ---

class RegisterCog(commands.Cog):
    """管理報名相關指令的 Cog。"""
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        # 為了讓 Bot 重新啟動後，之前發出的 RegisterStartView 按鈕還能繼續作用
        # 我們需要在 Bot 啟動時就把它註冊進去
        self.bot.add_view(RegisterStartView())

    @app_commands.command(
        name="register_panel",
        description="在當前頻道建立一個永久的報名面板",
    )
    @app_commands.default_permissions(administrator=True)
    async def register_panel(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(
            title="活動報名",
            description="請點擊下方「我要報名」按鈕開始填寫報名表單。",
            color=discord.Color.green(),
        )
        embed.add_field(
            name="填寫方式",
            value="表單將會透過「私訊」傳送給您，請注意查收。",
            inline=False,
        )
        embed.set_footer(text="這是一個永久有效的報名面板")

        await interaction.response.send_message(
            embed=embed,
            view=RegisterStartView(),
        )




class TestCommand(BaseCog):

    @app_commands.command(
        name="test_command",
        description="test_com",
    )
    @app_commands.guild_only()
    async def test_command(
        self,
        interaction: discord.Interaction,
        admin_role: discord.Role,
        category: discord.CategoryChannel,
        a: discord.ForumChannel | None = None,
    ) -> None:

        await self.send_interaction_message(interaction=interaction, message="無任何作用")

async def setup(bot: commands.Bot) -> None:
    """將 Cog 載入 Bot 中。"""
    # await bot.add_cog(RegisterCog(bot))
    await bot.add_cog(TestCommand(bot))
