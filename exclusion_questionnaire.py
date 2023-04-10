from discord import ui, Interaction, ButtonStyle
from discord.ui.button import Button
from sidcon_classes import species_list


def determine_button_values(faction, faction_excluded):
    """
    returns the appropriate label and style for the button
    :param str faction: The faction for the button
    :param bool faction_excluded: Whether the factions is excluded
    :return: str, ButtonStyle
    """
    exclusion_text = "excluded" if faction_excluded else "included"

    return f"{faction} is {exclusion_text}", ButtonStyle.red if faction_excluded else ButtonStyle.green


class ExclusionQuestionnaire(ui.View):
    def __init__(self):
        super().__init__()
        self.factions_excluded = {}
        for faction in list_factions():
            name = faction.get("short", [None])[0]
            self.factions_excluded[name] = False
            self.add_item(FactionButton(self, name, faction.get("emoji", "")))

    # @ui.button(label="click me!", emoji="<:kit:973968075655356476>", style=ButtonStyle.green)
    # async def button_callback(self, interaction: Interaction, button: Button):
    #     # Flip the value of the button
    #     self.no_kit = not self.no_kit
    #     # Update the style to match the value
    #     button.style = ButtonStyle.red if self.no_kit else ButtonStyle.green
    #
    #     await interaction.response.edit_message(content=f'Information updated!', view=self)

    # async def on_submit(self, interaction: Interaction):
    #     await interaction.response.send_message(f'Thanks for your response!', ephemeral=True)


class FactionButton(Button):
    def __init__(self, parent, faction, emoji):
        self.parent = parent
        self.faction = faction
        label, style = determine_button_values(faction, self.faction_excluded())
        super().__init__(label=label, style=style, emoji=emoji)

    def faction_excluded(self):
        return self.parent.factions_excluded[self.faction]

    async def callback(self, interaction: Interaction):
        # Flip the value of the button
        self.parent.factions_excluded[self.faction] = not self.parent.factions_excluded[self.faction]
        # Update the style to match the value
        label, style = determine_button_values(self.faction, self.faction_excluded())
        self.style = style
        self.label = label

        await interaction.response.edit_message(content=f'{self.faction} updated!', view=self.parent)
