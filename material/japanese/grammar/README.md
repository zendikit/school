# Japanese Grammar

## Materials

This directory contains the following materials:

**grammar.json:**

This is the collection of Zendikit Japanese grammar points formatted as JSON.

**to_csv.py:**

This script converts the Zendikit Japanese grammar JSON file to CSV. You can use
this script to convert the JSON file into something Anki can import.

To see full usage: `python3 to_csv.py -h`.

The row schema is as follows, where each point is a field in a row:

1. Sort: (str) you can order by this in Anki; n5 material comes first, then n4,
   etc.
1. Level: (str) the approximate JLPT level corresponding to the grammar point
1. Name: (str) the Japanese grammar point itself (ex: くらい)
1. Meaning: (str) the English meaning of the grammar point
1. Example Sentences: (str) a collection of pairs of Japanese and English
   context sentences. Each sentence is encapsulated in an HTML div. Japanese
   sentences have class `jp` and English ones `en`.

You can create a note type based on the fields above to use in Anki.

## Example Anki Note Styling

**Front:**

```html
<div id="example-sentences-front">{{Example Sentences}}</div>
```

**Back:**

```html
<div id="example-sentences-back">{{Example Sentences}}</div>

<hr id=answer>

<table>
  <tbody>
    <tr>
      <td class="label">Name</td>
      <td>{{Name}}</td>
    </tr>
    <tr>
      <td class="label">Meaning</td>
      <td>{{Meaning}}</td>
    </tr>
    <tr>
      <td class="label">Level</td>
      <td>{{Level}}</td>
    </tr>
  </tbody>
</table>
```

**Styling:**

```css
.card {
 font-family: arial;
 font-size: 20px;
 color: black;
 background-color: white;
}

em {
  font-style: bold;
}

#example-sentences-front {
  text-align: center;
}

#example-sentences-back {
  text-align: center;
}

#example-sentences-front .en {
  color: transparent;
  text-shadow: #a0a0a0 1px 0 10px;
}

.jp {
  margin-bottom: 10px;
}

table {
  min-width: 100%;
  margin-top: 1em;
}

td {
  padding: 0.25em;
}

td[class^="label"] {
  text-align: right;
  vertical-align: top;
  color: #bfbfbf;
  width: 25%;
}
```

## Known Issues

If you change the order of elements in the JSON `points` array, `to_csv.py`
will assign different `Sort` IDs to points, and if you import these as-is into
Anki, you will overwrite one grammar point's card with content from another.
