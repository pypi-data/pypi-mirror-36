# Worin

Worin(월인, 月印) is a Korean POS Tagger using artificial neural networks.
The name 'worin' comes from "월인천강지곡" written by King Sejong.
This project is still on pre-alpha stage.

## Installation

1. install `tensorflow` or other `keras` backends
2. install `worin`

```sh
pip install worin
```

## Usage

```python
from worin.tag import FeedForward

tagger = FeedForward()
tagger.nouns('')
```
