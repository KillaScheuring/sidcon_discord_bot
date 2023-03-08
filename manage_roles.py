from assign_players import find_faction


def emoji_to_exclusion(emojis):
    """

    :param emojis:
    :return:
    """
    return [find_faction(emoji).get("exclusion") for emoji in emojis]


def find_role(ctx, role_name):
    """

    :param ctx:
    :param role_name:
    :return:
    """
    for role in ctx.guild.roles:
        if role.name == role_name:
            return role
