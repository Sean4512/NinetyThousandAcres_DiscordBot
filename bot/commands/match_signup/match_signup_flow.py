# -*- coding: utf-8 -*-
"""
@File    : match_signup_flow.py
@Time    : 2026/6/16 下午 10:31
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

from __future__ import annotations

from typing import Optional

import discord

from config.settings import get_discord_bot_settings
from config.questionnaire_settings import get_match_signup_questionnaire

from bot.core import BaseView
from bot.commands.questionnaire import QuestionnaireFlow
from bot.commands.admin_test import admin_required, ensure_admin_interaction

from services import GuildService, PlayerProfilesService, MatchSignupService

from utils.Types.questionnaire import (
    Questionnaire,
    QuestionnaireResult,
)

from utils.exceptions.discord_exceptions import (
    DebugError, InvalidInteractionContextError,
    GuildNotInitializedError, InternalError, GuildOnlyError, PlayerNoRegisteredError, ParameterError
)


def format_table(
    headers: list[str],
    rows: list[list[str]],
) -> str:
    if not headers:
        return ""

    all_rows = [headers, *rows]

    col_widths = [
        max(len(str(row[col])) for row in all_rows)
        for col in range(len(headers))
    ]

    def format_row(row: list[str]) -> str:
        return "  ".join(
            str(value).ljust(col_widths[index])
            for index, value in enumerate(row)
        )

    lines = [
        format_row(headers),
        format_row(["-" * width for width in col_widths]),
        *[format_row(row) for row in rows],
    ]

    return "```text\n" + "\n".join(lines) + "\n```"

async def get_member_by_discord_id(
    guild: discord.Guild,
    discord_id: str,
) -> discord.Member | None:
    user_id = int(discord_id)

    member = guild.get_member(user_id)
    if member is not None:
        return member

    try:
        return await guild.fetch_member(user_id)
    except discord.NotFound:
        return None
    except discord.Forbidden:
        return None
    except discord.HTTPException:
        return None





class PlayerMatchSignupFlow(QuestionnaireFlow):
    def __init__(
        self,
        *,
        user: discord.User | discord.Member,
        guild_id: str,
        thread_id: str,
        discord_id: str,
        questionnaire: Questionnaire,
        timeout_seconds: int,
        is_update: bool = False,
        initial_answers: dict | None = None,
    ) -> None:
        self.guild_id = guild_id
        self.thread_id = thread_id
        self.discord_id = discord_id
        self.is_update = is_update

        super().__init__(
            user=user,
            questionnaire=questionnaire,
            timeout_seconds=timeout_seconds,
            initial_answers=initial_answers,
            start_button_label=(
                "開始更新資料"
                if is_update
                else "開始報名"
            ),
            completed_message=(
                "🎉 玩家報名資料更新。"
                if is_update
                else "🎉 玩家報名完成。"
            ),
        )

    async def on_completed(
        self,
        *,
        interaction: discord.Interaction,
        result: QuestionnaireResult,
    ) -> None:
        success, message = MatchSignupService.signup_player(
            guild_id=self.guild_id,
            thread_id=self.thread_id,
            discord_id=self.discord_id,
            answers=result.answers,
            is_update=self.is_update
        )

        if not success:
            raise InternalError(message)

        self.logger.info(
            "MatchSignup: Player questionnaire completed. "
            f"operator_id={interaction.user.id}, player_id={self.discord_id}"
            f"guild_id={self.guild_id}, thread_id={self.thread_id}, is_update={self.is_update}"
        )


class PlayerMatchSignupView(BaseView):

    def __init__(
        self
    ) -> None:
        super().__init__(
            timeout=None,
            allowed_user_id=None,
        )

    @discord.ui.button(
        label="★報名☆",
        style=discord.ButtonStyle.success,
        emoji="📝",
        custom_id="ninety_thousand_acres:player_match_signup_panel",
    )
    async def player_match_signup_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        guild = interaction.guild
        channel = interaction.channel
        message = interaction.message
        user = interaction.user

        if guild is None:
            raise GuildOnlyError()

        if not isinstance(channel, discord.Thread) or message is None:
            raise InvalidInteractionContextError()

        guild_id = str(guild.id)
        thread_id = str(channel.id)
        discord_id = str(user.id)

        guild_config = GuildService.get_guild_config_by_guild_id(guild_id)
        if guild_config is None:
            raise GuildNotInitializedError()

        player_profiles = PlayerProfilesService.get_player_profiles_by_id(guild_id, discord_id)
        if player_profiles is None:
            raise PlayerNoRegisteredError()

        is_update = MatchSignupService.is_exists_match_signup_for_participants(
            guild_id=guild_id,
            thread_id=thread_id,
            discord_id=discord_id,
        )

        try:
            discord_bot_settings = get_discord_bot_settings()

            questionnaire = get_match_signup_questionnaire()
            initial_answers = None

            if is_update:
                initial_answers = (
                    MatchSignupService.get_participants_answers_by_id(
                        guild_id=guild_id,
                        thread_id=thread_id,
                        discord_id=discord_id
                    )
                )

            flow = PlayerMatchSignupFlow(
                user=user,
                guild_id=guild_id,
                thread_id=thread_id,
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

    @discord.ui.button(
        label="取消報名",
        style=discord.ButtonStyle.red,
        emoji="📝",
        custom_id="ninety_thousand_acres:cancel_player_match_signup_panel",
    )
    async def cancel_player_match_signup_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):

        guild = interaction.guild
        channel = interaction.channel
        message = interaction.message
        user = interaction.user

        if guild is None:
            raise GuildOnlyError()

        if not isinstance(channel, discord.Thread) or message is None:
            raise InvalidInteractionContextError()

        guild_id = str(guild.id)
        thread_id = str(channel.id)
        discord_id = str(user.id)

        guild_config = GuildService.get_guild_config_by_guild_id(guild_id)
        if guild_config is None:
            raise GuildNotInitializedError()

        player_profiles = PlayerProfilesService.get_player_profiles_by_id(guild_id, discord_id)
        if player_profiles is None:
            raise PlayerNoRegisteredError()

        is_exists = MatchSignupService.is_exists_match_signup_for_participants(
            guild_id=guild_id,
            thread_id=thread_id,
            discord_id=discord_id,
        )
        if is_exists:
            MatchSignupService.delete_participants_by_id(
                guild_id=guild_id,
                thread_id=thread_id,
                discord_id=discord_id,
            )
            await self.send_interaction_message(
                interaction=interaction,
                message="✅ 已取消報名。"
            )
        else:
            await self.send_interaction_message(
                interaction=interaction,
                message="尚未報名。"
            )


    @discord.ui.button(
        label="刪除報名表",
        style=discord.ButtonStyle.red,
        emoji="📝",
        custom_id="ninety_thousand_acres:delete_match_signup_panel",
    )
    async def delete_match_signup_button(
            self,
            interaction: discord.Interaction,
            button: discord.ui.Button,
    ):
        await ensure_admin_interaction(interaction)

        guild = interaction.guild
        channel = interaction.channel
        message = interaction.message
        user = interaction.user

        if guild is None:
            raise GuildOnlyError()

        if not isinstance(channel, discord.Thread) or message is None:
            raise InvalidInteractionContextError()

        guild_id = str(guild.id)
        thread_id = str(channel.id)

        guild_config = GuildService.get_guild_config_by_guild_id(guild_id)
        if guild_config is None:
            raise GuildNotInitializedError()

        MatchSignupService.insert_match_signup_forms(
            guild_id=guild_id,
            forum_id=guild_config.registration_forum_id,
            thread_id=thread_id,
            message_id=thread_id,
            status="close",
            title=None,
            content=None,
            log="",
        )

        await channel.delete(reason=f"Delete signup thread: {thread_id}"
                                    f", operator_id={user.id}"
                                    f", name={user.name}, guild_name={user.global_name}"
                             )

    @discord.ui.button(
        label="顯示名單",
        style=discord.ButtonStyle.secondary,
        emoji="📝",
        custom_id="ninety_thousand_acres:show_match_signup_player_list",
    )
    async def show_match_signup_player_list_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        await ensure_admin_interaction(interaction)
        guild = interaction.guild
        channel = interaction.channel
        message = interaction.message
        user = interaction.user

        if guild is None:
            raise GuildOnlyError()

        if not isinstance(channel, discord.Thread) or message is None:
            raise InvalidInteractionContextError()

        guild_id = str(guild.id)
        thread_id = str(channel.id)

        guild_config = GuildService.get_guild_config_by_guild_id(guild_id)
        if guild_config is None:
            raise GuildNotInitializedError()

        player_id_list = MatchSignupService.get_participants_by_id(
            guild_id=guild_id,
            thread_id=thread_id,
        )


        show_headers: list[str] = []
        show_rows_source: list[dict[str, str]] = []

        for player_dc_id in player_id_list:
            player_info = PlayerProfilesService.get_player_profile_answers(
                guild_id=guild_id,
                discord_id=player_dc_id,
            )

            player_match_signup_info = MatchSignupService.get_participants_answers_by_id(
                guild_id=guild_id,
                thread_id=thread_id,
                discord_id=player_dc_id,
            )

            player_info_keep_keys = ["game_uid", "game_name"]
            player_info = {
                key: value
                for key, value in player_info.items()
                if key in player_info_keep_keys
            }

            member = await get_member_by_discord_id(guild, player_dc_id)
            # discord_name = member.display_name if member is not None else "XXX"
            discord_name = str(member.display_name) if member is not None else "XXX"

            row_source: dict[str, str] = {
                "discord_id": discord_name,
                **player_info,
                **player_match_signup_info,
            }

            show_rows_source.append(row_source)

            for key in row_source.keys():
                if key not in show_headers:
                    show_headers.append(key)

        show_rows: list[list[str]] = [
            [
                str(row_source.get(header, ""))
                for header in show_headers
            ]
            for row_source in show_rows_source
        ]

        content = format_table(
            headers=show_headers,
            rows=show_rows,
        )
        if content == "":
            await self.send_interaction_message(interaction=interaction, message="目前無人報名")
        else:
            await self.send_interaction_message(interaction=interaction, message=content)









class CreateMatchSignupFlow(QuestionnaireFlow):
    def __init__(
        self,
        *,
        user: discord.User | discord.Member,
        guild: discord.Guild,
        discord_id: str,
        questionnaire: Questionnaire,
        timeout_seconds: int,
        is_update: bool = False,
        initial_answers: dict | None = None,
    ) -> None:
        self.guild = guild
        # self.guild_id = guild_id
        self.discord_id = discord_id
        self.is_update = is_update

        super().__init__(
            user=user,
            questionnaire=questionnaire,
            timeout_seconds=timeout_seconds,
            initial_answers=initial_answers,
            start_button_label=(
                "更新 報名表"
                if is_update
                else "建立 報名表"
            ),
            completed_message=(
                "🎉 報名表 已更新。"
                if is_update
                else "🎉 報名表 完成。"
            ),
        )

    async def on_completed(
        self,
        *,
        interaction: discord.Interaction,
        result: QuestionnaireResult,
    ) -> None:
        await self.create_match_signup(
            interaction=interaction,
            result=result,
            guild=self.guild
        )

    # @staticmethod
    async def create_match_signup(
            self,
            interaction: discord.Interaction,
            result: QuestionnaireResult,
            guild: discord.Guild,
    ):
        # guild = interaction.guild
        if guild is None:
            raise GuildOnlyError()

        guild_id = str(guild.id)

        guild_config = GuildService.get_config_by_id(guild_id=guild_id)
        if guild_config is None:
            raise GuildNotInitializedError()

        registration_forum_id = guild_config.get("registration_forum_id", None)
        if registration_forum_id is None:
            raise GuildNotInitializedError()

        forum = await MatchSignupService.get_registration_forum(
            guild,
            registration_forum_id,
        )

        if forum is None:
            raise GuildNotInitializedError()

        match_signup_title = result.answers.get("match_signup_title", "")
        if match_signup_title == "":
            raise ParameterError()

        match_signup_content = result.answers.get("match_signup_content", "")

        try:
            view = PlayerMatchSignupView()
            created_thread = await forum.create_thread(
                name=match_signup_title,
                content=(
                    f"{match_signup_content}\n\n"
                    "請點擊下方按鈕完成報名。"
                ),
                view=view,
                reason="Create match signup forum thread",
            )
        except Exception:
            raise

        thread: discord.Thread = created_thread.thread
        message: discord.Message = created_thread.message
        try:
            success, message = MatchSignupService.insert_match_signup_forms(
                guild_id=guild_id,
                forum_id=str(forum.id),
                thread_id=str(thread.id),
                message_id=str(message.id),
                status="open",
                title=match_signup_title,
                content=match_signup_content,
                log="",
            )
            if not success:
                raise InternalError(str(message))
        except Exception:
            try:
                await thread.delete(
                    reason="Rollback match signup thread because database insert failed"
                )
            except Exception:
                self.logger.exception("Failed to rollback match signup thread")
            # self.logger.exception(
            #     f"Database insert failed."
            #     f"guild_id={guild_id}, forum_id={str(forum.id)}, "
            #     f"thread_id={str(thread.id)}, message_id={str(message.id)}, "
            #     f"title=\"{match_signup_title}\", content=\"{match_signup_content}\"")
            raise

        return created_thread












