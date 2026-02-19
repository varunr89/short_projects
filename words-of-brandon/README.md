# Words of Brandon Archive

Complete archive of **16,282 Q&A entries** from [Arcanum](https://wob.coppermind.net/) — the official Brandon Sanderson fan archive of interviews, signings, and Q&As.

## Files

- `wob_entries.json` — All entries (17 MB)
- `download_wob.py` — Script used to fetch the data

## Data Structure

Each entry contains:
```json
{
  "id": 1356,
  "event": 108,
  "event_name": "Idaho Falls signing 2014",
  "event_date": "2014-11-29",
  "paraphrased": false,
  "tags": ["worldhopping", "perpendicularities"],
  "lines": [
    {"speaker": "Questioner", "text": "<p>Can non-Invested people worldhop?</p>"},
    {"speaker": "Brandon Sanderson", "text": "<p>I'm gonna go ahead and RAFO that.</p>"}
  ],
  "note": ""
}
```

## Source

Data fetched from the [Arcanum API](https://wob.coppermind.net/api/) on February 19, 2026.

## Usage

```python
import json

with open('wob_entries.json') as f:
    entries = json.load(f)

# Search for entries about Hoid
hoid_entries = [e for e in entries if any('hoid' in line['text'].lower() for line in e['lines'])]
print(f"Found {len(hoid_entries)} entries mentioning Hoid")
```

## License

This data is compiled from publicly available fan transcriptions. All content belongs to Brandon Sanderson and the Coppermind/17th Shard community.
