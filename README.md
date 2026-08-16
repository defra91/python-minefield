# Python Minefield

This project helped me to face the boring days in the summer, while the temperature outside was really too hot to do anything else. 

I wanted to learn Python from scratch, so I decided to create a simple game, which is a clone of the classic Minesweeper.

This project is intentionally an amateur one, and I don't want to make it too complex. The main goal is to learn Python and have fun while doing it.

Please feel free to contribute or fork this project, and if you have any suggestions or improvements, I would be happy to hear them.

One last thing: forgive me for the lack of documentation or best practices. I am doing my best, but remember that I am on holidays and I am looking for fun and enjoyment. We will reach for perfection the next time, I promise.

## Get Started

### Why `uv`?

This project is built using `uv`, a modern tool that allows to run Python code in a fast and efficient way. This tools is used as our primary Python package and project manager. I have decided to use uv because:

- It's written in Rust, therefore guarantees high performances.
- It simplifies dependency management for Python projects.
- It collects multiple tools in a single one, which makes it easier to use and learn.
- Ensures reproducible installations across different environments
- Downloads and manages different Python versions, which is useful for testing and compatibility.


```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Get Started

### Install dependencies

```bash
uv sync
```

### Run the Game

```bash
uv run python-minefield
```