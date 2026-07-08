# -*- coding: utf-8 -*-
"""
@File    : ShowComponentObject.py
@Time    : 2026/5/5 下午 11:59
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""
# bot/commands/show_component_object.py

from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands


# =========================
# Modal: TEXT / PARAGRAPH
# =========================

class TextExampleModal(discord.ui.Modal, title="TEXT / PARAGRAPH 範例"):
    text = discord.ui.TextInput(
        label="TEXT：短文字",
        placeholder="例如：Sean",
        style=discord.TextStyle.short,
        required=True,
        max_length=100,
    )

    paragraph = discord.ui.TextInput(
        label="PARAGRAPH：多行文字",
        placeholder="例如：請輸入一段自我介紹",
        style=discord.TextStyle.paragraph,
        required=False,
        max_length=1000,
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(
            content=(
                "✅ 你提交了 Modal：\n"
                f"TEXT：`{self.text.value}`\n"
                f"PARAGRAPH：\n```text\n{self.paragraph.value}\n```"
            ),
            ephemeral=True,
        )


# =========================
# View Select: STRING_SELECT
# =========================

class ExampleStringSelect(discord.ui.Select):
    def __init__(self) -> None:
        options = [
            discord.SelectOption(
                label="戰士",
                value="warrior",
                description="近戰角色",
                emoji="⚔️",
            ),
            discord.SelectOption(
                label="法師",
                value="mage",
                description="魔法角色",
                emoji="🪄",
            ),
            discord.SelectOption(
                label="弓箭手",
                value="archer",
                description="遠程角色",
                emoji="🏹",
            ),
        ]

        super().__init__(
            placeholder="STRING_SELECT：請選擇職業",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(
            f"你選擇的 STRING_SELECT value 是：`{self.values[0]}`",
            ephemeral=True,
        )


# =========================
# View Select: BOOLEAN_SELECT
# =========================

class BooleanSelect(discord.ui.Select):
    def __init__(self) -> None:
        options = [
            discord.SelectOption(
                label="是",
                value="true",
                description="代表 True",
                emoji="✅",
            ),
            discord.SelectOption(
                label="否",
                value="false",
                description="代表 False",
                emoji="❌",
            ),
        ]

        super().__init__(
            placeholder="BOOLEAN_SELECT：請選擇是或否",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        result = self.values[0] == "true"

        await interaction.response.send_message(
            f"你選擇的 BOOLEAN_SELECT 結果是：`{result}`",
            ephemeral=True,
        )


# =========================
# View Select: USER_SELECT
# =========================

class ExampleUserSelect(discord.ui.UserSelect):
    def __init__(self) -> None:
        super().__init__(
            placeholder="USER_SELECT：請選擇一位使用者",
            min_values=1,
            max_values=1,
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        user = self.values[0]

        await interaction.response.send_message(
            f"你選擇的使用者是：{user.mention}",
            ephemeral=True,
        )


# =========================
# View Select: ROLE_SELECT
# =========================

class ExampleRoleSelect(discord.ui.RoleSelect):
    def __init__(self) -> None:
        super().__init__(
            placeholder="ROLE_SELECT：請選擇一個身分組",
            min_values=1,
            max_values=1,
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        role = self.values[0]

        await interaction.response.send_message(
            f"你選擇的身分組是：{role.mention}",
            ephemeral=True,
        )


# =========================
# View Select: CHANNEL_SELECT
# =========================

class ExampleChannelSelect(discord.ui.ChannelSelect):
    def __init__(self) -> None:
        super().__init__(
            placeholder="CHANNEL_SELECT：請選擇一個頻道",
            min_values=1,
            max_values=1,
            channel_types=[
                discord.ChannelType.text,
                discord.ChannelType.voice,
                discord.ChannelType.category,
            ],
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        channel = self.values[0]

        await interaction.response.send_message(
            f"你選擇的頻道是：{channel.mention}",
            ephemeral=True,
        )


def get_checkbox_value(checkbox: object) -> bool:
    """
    不同 discord.py / fork 版本可能使用不同屬性名稱。
    優先讀 checked，其次讀 value。
    """

    if hasattr(checkbox, "checked"):
        return bool(getattr(checkbox, "checked"))

    if hasattr(checkbox, "value"):
        return bool(getattr(checkbox, "value"))

    return False


# =========================
# Modal: CHECKBOX
# =========================

class CheckboxExampleModal(discord.ui.Modal, title="CHECKBOX 範例"):
    def __init__(self) -> None:
        super().__init__()

        Checkbox = getattr(discord.ui, "Checkbox", None)

        if Checkbox is None:
            raise RuntimeError(
                "目前的 discord.py 版本不支援 discord.ui.Checkbox"
            )

        self.agree_rules = Checkbox(
            label="CHECKBOX：我同意伺服器規則",
            required=True,
            default=False,
        )

        self.receive_notice = Checkbox(
            label="CHECKBOX：我願意接收活動通知",
            required=False,
            default=False,
        )

        self.add_item(self.agree_rules)
        self.add_item(self.receive_notice)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        agree_rules = get_checkbox_value(self.agree_rules)
        receive_notice = get_checkbox_value(self.receive_notice)

        await interaction.response.send_message(
            content=(
                "✅ 你提交了 CHECKBOX Modal：\n"
                f"是否同意規則：`{agree_rules}`\n"
                f"是否接收活動通知：`{receive_notice}`"
            ),
            ephemeral=True,
        )


# =========================
# Main View
# =========================

class ComponentExampleView(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=300)

        self.add_item(ExampleStringSelect())
        self.add_item(BooleanSelect())
        self.add_item(ExampleUserSelect())
        self.add_item(ExampleRoleSelect())
        self.add_item(ExampleChannelSelect())

    async def on_timeout(self) -> None:
        for item in self.children:
            item.disabled = True


# =========================
# Button View: 開啟 Modal
# =========================

class ModalOpenView(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=300)

    @discord.ui.button(
        label="開啟 TEXT / PARAGRAPH Modal",
        style=discord.ButtonStyle.primary,
    )
    async def open_text_modal(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ) -> None:
        await interaction.response.send_modal(TextExampleModal())

    @discord.ui.button(
        label="開啟 CHECKBOX Modal",
        style=discord.ButtonStyle.secondary,
    )
    async def open_checkbox_modal(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ) -> None:
        if not hasattr(discord.ui, "Checkbox"):
            await interaction.response.send_message(
                content=(
                    "❌ 你目前的 discord.py 版本不支援 `discord.ui.Checkbox`。\n"
                    "你可以先用 `BOOLEAN_SELECT` 代替 CHECKBOX。"
                ),
                ephemeral=True,
            )
            return

        try:
            await interaction.response.send_modal(CheckboxExampleModal())

        except RuntimeError as exc:
            await interaction.response.send_message(
                content=f"❌ {exc}",
                ephemeral=True,
            )


# =========================
# Cog
# =========================

class ShowComponentObject(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="show_component_object",
        description="顯示 Discord UI Object 範例",
    )
    async def show_component_object(
        self,
        interaction: discord.Interaction,
    ) -> None:
        await interaction.response.send_message(
            content=(
                "下面是常用 Discord UI Object 範例。\n\n"
                "這一組是訊息上的 Select 類型：\n"
                "- STRING_SELECT\n"
                "- USER_SELECT\n"
                "- ROLE_SELECT\n"
                "- CHANNEL_SELECT\n"
                "- BOOLEAN_SELECT\n\n"
                "按鈕可以開啟 Modal，Modal 裡面示範：\n"
                "- TEXT\n"
                "- PARAGRAPH"
            ),
            view=ComponentExampleView(),
            ephemeral=True,
        )

        await interaction.followup.send(
            content="這個按鈕會開啟 TEXT / PARAGRAPH Modal。",
            view=ModalOpenView(),
            ephemeral=True,
        )

    @app_commands.command(
        name="show_component_object_dm",
        description="私訊顯示 Discord UI Object 範例",
    )
    @app_commands.guild_only()
    async def show_component_object_dm(
        self,
        interaction: discord.Interaction,
    ) -> None:
        """
        這個指令在伺服器輸入，
        但 UI Object 範例會由機器人私訊給使用者。
        """

        if interaction.guild is None:
            await interaction.response.send_message(
                "❌ 這個指令只能在伺服器中使用。",
                ephemeral=True,
            )
            return

        try:
            await interaction.user.send(
                content=(
                    "這是由伺服器指令觸發的私訊 UI Object 範例。\n\n"
                    "這一組是訊息上的 Select 類型：\n"
                    "- STRING_SELECT\n"
                    "- USER_SELECT\n"
                    "- ROLE_SELECT\n"
                    "- CHANNEL_SELECT\n"
                    "- BOOLEAN_SELECT\n\n"
                    "你也可以透過另一則私訊中的按鈕開啟 Modal，Modal 會示範：\n"
                    "- TEXT\n"
                    "- PARAGRAPH"
                ),
                view=ComponentExampleView(),
            )

            await interaction.user.send(
                content="這個按鈕會開啟 TEXT / PARAGRAPH Modal。",
                view=ModalOpenView(),
            )

            await interaction.response.send_message(
                "✅ 已經將 UI Object 範例私訊給你。",
                ephemeral=True,
            )

        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ 我無法私訊你。請確認你有開啟「允許伺服器成員傳送私人訊息」。",
                ephemeral=True,
            )

        except discord.HTTPException as exc:
            await interaction.response.send_message(
                f"❌ 私訊發送失敗：`{exc}`",
                ephemeral=True,
            )


# ==========================================
# 5. Setup 函式
# ==========================================
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ShowComponentObject(bot))


