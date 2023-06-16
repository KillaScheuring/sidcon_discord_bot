import math
from discord import ui, Interaction, ButtonStyle, Member
import discord.errors
from discord.ui.button import Button
from sidcon_classes import SpeciesList


def determine_button_values(faction, faction_excluded):
    """
    returns the appropriate label and style for the button
    :param str faction: The faction for the button
    :param bool faction_excluded: Whether the factions is excluded
    :return: str, ButtonStyle
    """
    exclusion_text = "excluded" if faction_excluded else "included"

    return f"{faction} is {exclusion_text}", ButtonStyle.red if faction_excluded else ButtonStyle.green


class ExclusionSettings(ui.View):
    def __init__(self, member):
        """
        :param Member member:
        """
        super().__init__()
        self.species_list = SpeciesList()
        self.factions_excluded = {}
        self.member = member

        member_roles = [role.name for role in member.roles if "no-" in role.name]
        for index, faction in enumerate(self.species_list.factions()):
            self.factions_excluded[faction.name] = faction.exclusion_role in member_roles
            self.add_item(FactionButton(self, faction, math.floor(index / 4)))

    async def update_role(self, faction):
        try:
            role = [role for role in self.member.guild.roles if role.name == faction.exclusion_role][0]
        except IndexError:
            role = None

        if not role:
            return False

        if self.factions_excluded[faction.name]:
            await self.member.remove_roles(role, reason="Bot Requested")
        else:
            await self.member.add_roles(role, reason="Bot Requested")
        # Flip the value of the button
        self.factions_excluded[faction.name] = not self.factions_excluded[faction.name]
        return True


class FactionButton(Button):
    def __init__(self, parent, faction, row):
        self.parent = parent
        self.faction = faction
        label, style = determine_button_values(faction.name, self.check_role())
        super().__init__(label=label, style=style, emoji=faction.emoji, row=row)

    def check_role(self):
        return self.parent.factions_excluded[self.faction.name]

    async def callback(self, interaction: Interaction):
        try:
            await self.parent.update_role(self.faction)
            # Update the style to match the value
            label, style = determine_button_values(self.faction.name, self.check_role())
            self.style = style
            self.label = label
        except discord.errors.Forbidden as e:
            await interaction.response.edit_message(content=f'Error updating {self.faction.name}: {e.text}', view=self.parent)
            print(e)
        except discord.errors.InteractionResponded as e:
            pass
        else:
            await interaction.response.edit_message(content=f'{self.faction.name} updated!', view=self.parent)
