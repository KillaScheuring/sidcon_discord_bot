from discord import ui, Interaction, ButtonStyle, Member
from discord.ui.button import Button
from sidcon_classes import Faction, resource_emoji_dict
from pprint import pprint
from assign_players import structure_assignments, random_assignment


class AssignmentInteraction(ui.View):
    def __init__(self, factions, random_assignment_params):
        super().__init__()
        self.random_assignment_params = random_assignment_params
        self.update_factions(factions)
        self.impact = 0
        self.consumption = {
            "green": 0,
            "brown": 0,
            "white": 0,
            "black": 0,
            "blue": 0,
            "yellow": 0,
            "ultratech": 0
        }
        self.production = {
            "green": 0,
            "brown": 0,
            "white": 0,
            "black": 0,
            "blue": 0,
            "yellow": 0,
            "ultratech": 0
        }
        self.factions = factions

    def update_factions(self, factions):
        self.impact = 0
        self.consumption = {
            "green": 0,
            "brown": 0,
            "white": 0,
            "black": 0,
            "blue": 0,
            "yellow": 0,
            "ultratech": 0
        }
        self.production = {
            "green": 0,
            "brown": 0,
            "white": 0,
            "black": 0,
            "blue": 0,
            "yellow": 0,
            "ultratech": 0
        }
        self.factions = factions
        for faction in factions:
            self.impact += faction.impact
            for resource in self.consumption:
                self.consumption[resource] += (1 if faction.consumes[resource] > 0 else 0)
                self.production[resource] += (1 if faction.produces[resource] > 0 else 0)

    @ui.button(label="Impact")
    async def impact_callback(self, interaction: Interaction, button):
        """
        Returns the impact of the assignment in an ephemeral message
        :param interaction:
        :param button:
        :return:
        """
        await interaction.response.send_message(content=f"Impact is {self.impact}", ephemeral=True)

    @ui.button(label="Resources")
    async def resource_callback(self, interaction: Interaction, button):
        """
        Returns the number of factions that consume and produce each resource in an ephemeral message
        :param interaction:
        :param button:
        :return:
        """
        consumer_message = []
        producer_message = []
        for resource in resource_emoji_dict:
            consumer_message.append(f"{self.consumption[resource]} {resource_emoji_dict[resource]}")
            producer_message.append(f"{self.production[resource]} {resource_emoji_dict[resource]}")
        consumer_message = "; ".join(consumer_message)
        producer_message = "; ".join(producer_message)
        await interaction.response.send_message(content=f"Consumes: {consumer_message}\nProduces: {producer_message}",
                                                ephemeral=True)

    @ui.button(label="Score")
    async def score_callback(self, interaction: Interaction, button):
        """
        Returns an ephemeral message with a template for final score recording
        :param interaction:
        :param button:
        :return:
        """
        scoring_template = []
        for faction in self.factions:
            scoring_template.append(f"{faction.emoji} - ")
        await interaction.response.send_message(content="\n".join(scoring_template), ephemeral=True)

    @ui.button(label="Reroll", row=2)
    async def reroll_callback(self, interaction: Interaction, button):
        """
        Returns a new assignment message
        :param interaction:
        :param button:
        :return:
        """
        new_assignments = random_assignment(**self.random_assignment_params)
        self.update_factions(list(new_assignments.values()))
        await interaction.response.edit_message(content=structure_assignments(new_assignments), view=self)
