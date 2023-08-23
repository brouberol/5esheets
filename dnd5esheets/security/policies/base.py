from dnd5esheets.exceptions import Forbidden
from dnd5esheets.models import Party, Player, Role


def _in_same_party(current_player: Player, players_in_party: list[Player]):
    if current_player not in players_in_party:
        raise Forbidden(
            detail="Only a member of the same party can access this resource"
        )


def _is_party_gm(players: list[Player], party: Party):
    for player in players:
        for player_role in player.player_roles:
            if player_role.party_id == party.id and player_role.role == Role.gm:
                return
    raise Forbidden(
        detail="Only the resource owner or the party GM can access this resource"
    )
