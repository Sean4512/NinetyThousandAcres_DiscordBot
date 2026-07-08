# -*- coding: utf-8 -*-
"""
@File    : player_register_cog.py
@Time    : 2026/6/16 下午 04:34
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

from __future__ import annotations

import discord
from discord import app_commands

from config.settings import get_discord_bot_settings
from config.questionnaire_settings import get_player_register_questionnaire

from bot.core import BaseCog, BaseView
from bot.commands.admin_test import admin_required

from services.guild_service import GuildService
from services.player_profiles_service import PlayerProfilesService

from utils.exceptions.discord_exceptions import GuildNotInitializedError, InternalError, GuildOnlyError, PlayerNoRegisteredError


from .player_register_flow import PlayerRegisterFlow


class PlayerRegisterCog(BaseCog):

    async def cog_load(self) -> None:

        self.bot.add_view(
            PlayerRegisterEntryView(
                cog=self,
            )
        )

    async def start_player_register(
            self,
            interaction: discord.Interaction,
            discord_id: str = ""
    ) -> None:
        guild = interaction.guild
        if guild is None:
            raise GuildOnlyError()

        user = interaction.user

        guild_id = str(guild.id)
        discord_id = discord_id if discord_id else str(user.id)

        guild_config = GuildService.get_guild_config_by_guild_id(guild_id)
        if guild_config is None:
            raise GuildNotInitializedError()

        player_profile = PlayerProfilesService.get_player_profiles_by_id(
            guild_id,
            discord_id,
        )
        is_update = False
        if player_profile is not None:
            is_update = True

        try:
            discord_bot_settings = get_discord_bot_settings()

            questionnaire = get_player_register_questionnaire()
            initial_answers = None

            if is_update:
                initial_answers = (
                    PlayerProfilesService.get_player_profile_answers(
                        guild_id=guild_id,
                        discord_id=discord_id,
                    )
                )

            flow = PlayerRegisterFlow(
                user=user,
                guild_id=guild_id,
                discord_id=discord_id,
                questionnaire=questionnaire,
                timeout_seconds=(
                    discord_bot_settings.PLAYER_REGISTER_TIMEOUT
                ),
                is_update=is_update,
                initial_answers=initial_answers,
            )

            await flow.start(interaction=interaction)

        except discord.Forbidden:
            raise

        except discord.HTTPException as e:
            raise InternalError("註冊表單私訊傳送失敗。") from e

        if questionnaire.delivery.is_direct_message:
            await self.send_interaction_message(
                interaction=interaction,
                message="✅ 註冊表單已透過私訊傳送給你，請前往私訊查看。"
            )
        else:
            await self.send_interaction_message(
                interaction=interaction,
                message="✅ 註冊表單已傳送給你。"
            )

    @app_commands.command(
        name="player_register",
        description="玩家註冊或更新資料",
    )
    @app_commands.guild_only()
    async def player_register(
            self,
            interaction: discord.Interaction
    ) -> None:
        await self.start_player_register(interaction)

    @app_commands.command(
        name="admin_player_register",
        description="管理員協助玩家註冊或更新資料",
    )
    @app_commands.guild_only()
    @admin_required()
    async def admin_player_register(
            self,
            interaction: discord.Interaction,
            user: discord.User
    ) -> None:
        await self.start_player_register(interaction, str(user.id))


    @app_commands.command(
        name="del_player_data",
        description="刪除玩家資料",
    )
    @app_commands.guild_only()
    @admin_required()
    async def del_player_data(
            self,
            interaction: discord.Interaction,
            user: discord.User
    ) -> None:
        guild = interaction.guild
        if guild is None:
            raise GuildOnlyError()

        guild_id = str(guild.id)
        discord_id = str(user.id)

        guild_config = GuildService.get_guild_config_by_guild_id(guild_id)
        if guild_config is None:
            raise GuildNotInitializedError()

        player_profile = PlayerProfilesService.get_player_profiles_by_id(
            guild_id,
            discord_id,
        )
        if player_profile is None:
            raise PlayerNoRegisteredError()

        PlayerProfilesService.delete_by_id(guild_id=guild_id, discord_id=discord_id)

        await self.send_interaction_message(
            interaction=interaction,
            message=f"✅ {user.global_name} 玩家資料已刪除。"
        )

    @app_commands.command(
        name="player_register_panel",
        description="發布玩家註冊按鈕",
    )
    @app_commands.guild_only()
    @admin_required()
    async def player_register_panel(
            self,
            interaction: discord.Interaction,
    ) -> None:
        embed = discord.Embed(
            title="九萬畝玩家註冊",
            description=(
                "點擊下方按鈕即可開始註冊或更新玩家資料。\n\n"
                "註冊流程開始後，請依照畫面提示完成問卷。"
            ),
            color=discord.Color.green(),
        )

        view = PlayerRegisterEntryView(
            cog=self,
        )


        await interaction.response.defer(ephemeral=True)
        await interaction.channel.send(
            embed=embed,
            view=view,
        )
        await interaction.followup.send(
            "✅ 玩家註冊按鈕已發布。",
            ephemeral=True,
        )




class PlayerRegisterEntryView(BaseView):
    """
    玩家註冊公開入口。

    timeout=None：
        建立 Persistent View，按鈕不會因 View timeout 失效。

    custom_id：
        Persistent View 必須使用固定且唯一的 custom_id。
    """

    def __init__(
        self,
        *,
        cog: PlayerRegisterCog,
    ) -> None:
        super().__init__(
            timeout=None,
            allowed_user_id=None,
        )

        self.cog = cog

    @discord.ui.button(
        label="玩家註冊／更新資料",
        style=discord.ButtonStyle.success,
        emoji="📝",
        custom_id="ninety_thousand_acres:player_register_panel",
    )
    async def player_register_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ) -> None:
        await self.cog.start_player_register(
            interaction=interaction,
            discord_id=str(interaction.user.id)
        )


