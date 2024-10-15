from collections import defaultdict
from dataclasses import dataclass, field

from durak_bot.const.decks import CARDS_FOR_DECK
from durak_bot.ctx.types.base import BaseState
from durak_bot.types.card import Card
from durak_bot.ctx.types.lobby_state import _lobby_state


@dataclass
class CardsState(BaseState):
    # Deck stats
    deck_left: int = 0
    discarded_count: int = 0

    # Cards in our hand
    our_hand: list[Card] = field(default_factory=list)

    # Might be either in deck, or in someone's hands, includes the trump card
    unseen_cards: list[Card] = field(default_factory=list)

    # When someone takes the cards, they are saved here.
    # Key is player id, ours aren't tracked.
    # If a card is known and contains in this dict,
    #   it still presents in `unseen_cards`
    known_cards: dict[int, list[Card]] = field(default_factory=lambda: defaultdict(list))

    # Number of cards player have, key is player id
    number_of_cards: dict[int, int] = field(default_factory=lambda: defaultdict(int))

    # Game
    beaten_cards_on_table: list[Card] = field(default_factory=list)
    unbeaten_cards_on_table: list[Card] = field(default_factory=list)

    # Beaten cards + unbeaten cards + cards used to beat
    cards_on_table: list[Card] = field(default_factory=list)

    # Trump card, when deck is empty only type is set, value would be an empty str
    trump_card: Card = field(default=Card(type='', value=''))

    # Internal state
    got_tricked: bool = False
    forwarding: bool = False

    @property
    def trump_card_type(self) -> str:
        return self.trump_card.type

    @property
    def table_values(self) -> set[str]:
        return {x.value for x in self.cards_on_table}

    @property
    def should_ignore_trumps(self) -> bool:
        # If we are almost out of cards, we dont really care about trumps
        return len(self.our_hand) > 1

    def mark_card_as_seen(self, card: Card) -> None:
        if card in self.unseen_cards:
            self.unseen_cards.remove(card)

    def remove_known_card(self, card: Card, player_index: int | None) -> None:
        if player_index is None:
            return
        if card in self.known_cards[player_index]:
            self.known_cards[player_index].remove(card)

    def push_known_card(self, card: Card, player_index: int) -> None:
        self.known_cards[player_index].append(card)

    def push_card_on_table(self, card: Card) -> None:
        self.mark_card_as_seen(card)
        self.cards_on_table.append(card)

    def push_unbeaten_card_on_table(self, card: Card, player_index: int | None = None) -> None:
        assert card not in self.unbeaten_cards_on_table
        self.push_card_on_table(card)
        self.unbeaten_cards_on_table.append(card)
        self.remove_known_card(card, player_index)

    def card_beaten(self, card: Card, beaten_by: Card | None = None, player_index: int | None = None) -> None:
        self.unbeaten_cards_on_table.remove(card)
        self.beaten_cards_on_table.append(card)

        if beaten_by:
            self.push_card_on_table(beaten_by)
            self.remove_known_card(beaten_by, player_index)

    def inc_cards_count(self, player_index: int) -> None:
        self.number_of_cards[player_index] += 1

    def dec_cards_count(self, player_index: int) -> None:
        self.number_of_cards[player_index] -= 1

    def remove_from_our_hand(self, card: Card) -> None:
        self.dec_cards_count(_lobby_state.position)
        self.our_hand.remove(card)

    def add_to_our_hand(self, card: Card) -> None:
        self.inc_cards_count(_lobby_state.position)
        self.our_hand.append(card)

    def mark_card_as_unseen(self, card: Card) -> None:
        assert card not in self.unseen_cards
        self.unseen_cards.append(card)

    def remove_card_from_table(self, card: Card) -> None:
        self.mark_card_as_unseen(card)
        self.cards_on_table.remove(card)

        if card in self.unbeaten_cards_on_table:
            self.card_beaten(card)

    def clear_table(self) -> None:
        self.unbeaten_cards_on_table.clear()
        self.beaten_cards_on_table.clear()
        self.cards_on_table.clear()

    def reload_cards(self) -> None:
        self.unseen_cards = list(CARDS_FOR_DECK[_lobby_state.deck_size])
        self.deck_left = _lobby_state.deck_size
        self.our_hand.clear()
        self.known_cards.clear()
        self.number_of_cards.clear()
        self.clear_table()

    def ensure_hand_cards_are_seen(self) -> None:
        for card in self.our_hand:
            if card in self.unseen_cards:
                self.unseen_cards.remove(card)


_cards_state = CardsState()
