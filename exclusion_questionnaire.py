import math
from discord import ui, Interaction, ButtonStyle
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


class ExclusionQuestionnaire(ui.View):
    def __init__(self):
        super().__init__()
        self.species_list = SpeciesList()
        self.factions_excluded = {}
        for index, faction in enumerate(self.species_list.factions()):
            self.factions_excluded[faction.name] = False
            self.add_item(FactionButton(self, faction.name, faction.emoji, math.floor(index / 4)))


class FactionButton(Button):
    def __init__(self, parent, faction, emoji, row):
        self.parent = parent
        self.faction = faction
        label, style = determine_button_values(faction, self.faction_excluded())
        super().__init__(label=label, style=style, emoji=emoji, row=row)
        print(faction, row)

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
