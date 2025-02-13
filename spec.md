<!-- spec.md -->
# JSON-PC Specification

## Overview

JSON-PC (JSON Page Content) is a standard for representing webpage content in JSON format. It organizes content into sections, text blocks, lists, images, videos, FAQs, and hyperlinks for clear and manageable representation. JSON-PC also supports microdata attributes to enhance semantic information and enable structured data compliance with schema.org.

## Data Structure

### Page Object
The root JSON object contains:
- **url**: The URL of the page.
- **slug**: A URL-friendly identifier for the page (e.g., `"example-page"`).
- **title**: The title of the page.
- **metaDescription**: A short description for SEO purposes.
- **content**: An array of section objects, lists, images, videos, FAQs, and hyperlinks.

### Section Object
Each section represents a portion of the webpage and includes:
- **type**: Must be `"section"`.
- **header**: The header text (typically derived from an `<h2>` element).
- **elements**: An array of content elements (e.g., text blocks, lists, images, videos, FAQs, links).
- **microdata** (optional): An object containing microdata attributes (`itemscope`, `itemtype`, `itemprop`).

### Text Block Object
Represents a block of text, potentially combining multiple paragraphs.
- **type**: Must be `"textBlock"`.
- **content**: A string containing the text.
- **microdata** (optional): An object with microdata attributes.

### List Object
Represents a list of items.
- **type**: Must be `"list"`.
- **title** (optional): A title for the list, often taken from a preceding `<h3>` element.
- **items**: An array of strings representing list items.
- **microdata** (optional): An object with microdata attributes.

### Image Object
Represents an image element.
- **type**: Must be `"image"`.
- **src**: The URL of the image.
- **alt** (optional): Alternative text describing the image.
- **caption** (optional): A caption for the image.
- **microdata** (optional): An object with microdata attributes.

### Video Object
Represents a video element.
- **type**: Must be `"video"`.
- **src**: The URL of the video.
- **poster** (optional): A URL to a poster image for the video.
- **caption** (optional): A caption for the video.
- **microdata** (optional): An object with microdata attributes.

### Hyperlink Object
Represents a hyperlink.
- **type**: Must be `"link"`.
- **text**: The visible text of the link.
- **url**: The destination URL.
- **target** (optional): `"self"` for same-window navigation or `"blank"` for a new tab.
- **microdata** (optional): An object with microdata attributes.

### FAQ Object
Represents a Frequently Asked Questions (FAQ) section.
- **type**: Must be `"faq"`.
- **microdata** (optional): Must include `itemscope: true` and `itemtype: "https://schema.org/FAQPage"`.
- **questions**: An array of question-answer pairs.

### Question Object
Each FAQ question and answer is structured as:
- **question**: The question text.
- **answer**: The answer text.
- **microdata** (optional): Must include:
  - **itemscope: true**
  - **itemtype: "https://schema.org/Question"**
  - **itemprop: "mainEntity"**

## Example Structure

Below is an example of a JSON-PC document enriched with microdata, including images, videos, hyperlinks, and an FAQ section:

```json
{
  "url": "https://example.com/page",
  "slug": "example-page",
  "title": "Example Page with FAQ",
  "metaDescription": "This is an example page demonstrating JSON-PC format.",
  "content": [
    {
      "type": "section",
      "header": "Introduction",
      "elements": [
        {
          "type": "textBlock",
          "content": "This is the introduction text.",
          "microdata": {
            "itemscope": true,
            "itemtype": "https://schema.org/Article"
          }
        },
        {
          "type": "image",
          "src": "https://example.com/images/intro.jpg",
          "alt": "Introduction Image",
          "caption": "An image representing the introduction.",
          "microdata": {
            "itemscope": true,
            "itemtype": "https://schema.org/ImageObject"
          }
        },
        {
          "type": "link",
          "text": "Read more about JSON-PC",
          "url": "https://example.com/json-pc",
          "target": "blank",
          "microdata": {
            "itemprop": "relatedLink"
          }
        }
      ],
      "microdata": {
        "itemscope": true,
        "itemtype": "https://schema.org/WebPage"
      }
    },
    {
      "type": "section",
      "header": "Details",
      "elements": [
        {
          "type": "textBlock",
          "content": "Detailed explanation."
        },
        {
          "type": "list",
          "title": "Key Points",
          "items": [
            "Point A",
            "Point B"
          ],
          "microdata": {
            "itemscope": true,
            "itemtype": "https://schema.org/ItemList"
          }
        },
        {
          "type": "video",
          "src": "https://example.com/videos/detail.mp4",
          "poster": "https://example.com/images/detail-poster.jpg",
          "caption": "A video explaining key details.",
          "microdata": {
            "itemscope": true,
            "itemtype": "https://schema.org/VideoObject"
          }
        }
      ]
    },
    {
      "type": "faq",
      "microdata": {
        "itemscope": true,
        "itemtype": "https://schema.org/FAQPage"
      },
      "questions": [
        {
          "question": "What is JSON-PC?",
          "answer": "JSON-PC is a custom JSON format for structuring webpage content.",
          "microdata": {
            "itemscope": true,
            "itemtype": "https://schema.org/Question",
            "itemprop": "mainEntity"
          }
        },
        {
          "question": "How does JSON-PC handle FAQs?",
          "answer": "It integrates microdata and follows the FAQPage schema for SEO.",
          "microdata": {
            "itemscope": true,
            "itemtype": "https://schema.org/Question",
            "itemprop": "mainEntity"
          }
        }
      ]
    }
  ]
}