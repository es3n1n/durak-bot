# Durak Bot

*Durak is a shedding-type card game that is popular in post-Soviet states. The objective of the game is to get rid of all one's cards. At the end of the game, the last player with cards in their hand is the durak ("fool"). For more detailed information, visit the [Wikipedia page on Durak](https://en.wikipedia.org/wiki/Durak).*

There are many online resources where you can play this card game; however, the most popular one is Durak Online, available for [Android](https://play.google.com/store/apps/details?id=com.rstgames.durak&hl=en_US) and [iOS](https://apps.apple.com/us/app/durak-online-card-game/id891825663). This bot is an automated script that plays in lobbies in this version of the game.

## What's Supported

Pretty much everything, which includes:
* Short games
* Fast games
* All sizes of decks
* All sizes of lobbies
* Games with and without tricks
* Games with and without passing enabled

## Other Functionality

* Automatic lobby joining once invited
* Automatic friend requests acceptance
* Storing all the players seen in a SQLite database
* Storing all played games in a database with stats aggregation

## The Algorithm

Overall, this algorithm is fairly straightforward and obvious. Here's how it works:

*(non-latex description below)*

$$
\text{Let } H = \{c_1, c_2, ..., c_n\} \text{ be the hand, where } c_i < c_{i+1}
$$

$$
\text{Let } K_p = \{\text{cards player } p \text{ took when they couldn't defend}\}
$$

$$
\text{Let } D = \{\text{cards not yet seen in the game}\}
$$

$$
\text{Let } S = \{\text{cards seen in attacks, defenses, or passes}\}
$$

$$
D = \text{All cards} \setminus (H \cup S \cup \bigcup_{p} K_p)
$$

$$
\text{Defense strategy:} \quad D(a) = \min_{c \in H} \{c : c > a\}
$$

$$
\text{Attack strategy:} \quad A = \min_{c \in H} \{c\}
$$

$$
\text{Pass strategy:} \quad P(c, p) = \begin{cases} 
      \text{Pass} & \text{if } p \text{ and } (\exists c' \in H : \text{value}(c') = \text{value}(c)) \\
      \text{Attack} & \text{otherwise}
   \end{cases}
$$

Where:
- $c$ is the card on the table
- $p$ is a boolean indicating if passing is enabled
- $\text{value}(c)$ returns the numerical value of the card

Our hand is sorted by the card values from lower to higher (trumps are always higher in rank than any other card).

For each player's turn, we calculate the cards we've seen, the cards we know each player took when they couldn't defend, and all related information. We keep track of the cards left in the deck by subtracting all the cards we've seen in play, the cards in our hand, and the cards known to be taken by players from the full set of cards in the game.

Essentially, this bot knows everything it can about the game state. But despite having a lot of information about the game, the bot doesn't really do anything complex with it. Instead, here's what it does:

For defense, it will try to beat all cards using anything possible (of course, it will try to use cheap cards first). This is represented by the function $D(a)$, which selects the minimum card in the hand that can beat the attacking card $a$.

For attacking, it will always attack with cheap cards, keeping the higher cards for the endgame. This is represented by the function $A$, which selects the minimum card in the hand.

If the bot can pass a card (assuming passing is enabled and it has a card of the same value), it will always do so. This is represented by the function $P(c, p)$, which decides to pass if passing is enabled and the bot has a card of the same value as the card on the table. Otherwise, it will attack.

## Durakonline Library

This bot utilizes an open-source [implementation](https://github.com/Zakovskiy/durakonline.py) of Durakonline's network protocol.

While this library is able to interact with the game, it has some limitations and areas for improvement. I've added a few methods and features to enhance its functionality, but there's still significant room for optimization.

Due to the library's unconventional implementation, there are a few dirty workarounds in place, particularly regarding non-blocking responses within handlers.

For those interested in further developing this project, consider reviewing the existing codebase of this library and potentially refactoring or rewriting parts of it to better suit your needs. This could lead to a more robust and efficient implementation.

## Development

### Running

1. Install poetry 
    ```commandline
    python3 -m pip install poetry
    ```

2. Install project
    ```commandline
    poetry install
    ```

3. Activate shell
    ```commandline
    poetry shell
    ```

4. Fill .env
    ```commandline
    cp .env.example .env
    vim .env
    ```

5. Start the bot
    ```commandline
    python3 -m durak_bot
    ```

### Linting

1. Ruff
    ```commandline
    ruff format
    ruff check --fix
    ```

2. mypy
    ```commandline
    mypy .
    ```

### Testing

1. pytest
    ```commandline
    pytest .
    ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
