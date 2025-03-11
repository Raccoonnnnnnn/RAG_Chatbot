from __future__ import annotations
from typing import Any

GRAPH_FIELD_SEP = "<SEP>"

PROMPTS: dict[str, Any] = {}

PROMPTS["DEFAULT_LANGUAGE"] = "English"
PROMPTS["DEFAULT_TUPLE_DELIMITER"] = "<|>"
PROMPTS["DEFAULT_RECORD_DELIMITER"] = "##"
PROMPTS["DEFAULT_COMPLETION_DELIMITER"] = "<|COMPLETE|>"

PROMPTS["DEFAULT_ENTITY_TYPES"] = ["Book", "Author", "Publisher", "Manufacturer", "Price", "Sold Quantity", "Discount", "Rating", "Link"]

PROMPTS["entity_extraction"] = """---SYSTEM ROLE---
You are a professional book information extractor. Use only defined entities and relationships.

---Goal---
Given a text document that contains information about books, identify all entities of the specified types from the text and all relationships among the identified entities.
Use {language} as the output language.

---Steps---
1. Identify all entities present in the text. For each identified entity, extract the following information:
- entity_name: Name of the entity, using the same language as the input text. If the entity name is in English, capitalize it appropriately.
- entity_type: MUST be one of the following types: [{entity_types}]
- entity_description: A brief description of the entity (using the same language as the input text), tailored to its role or value in the context of the book it relates to. Follow these guidelines:
  - For 'Book': Describe it as "The book '<entity_name>', a work with specific attributes like price, sales, or cultural significance."
  - For 'Author': Describe it as "The author '<entity_name>' who wrote the book '<related_book_name>'."
  - For 'Publisher' or 'Manufacturer': Describe it as "The <entity_type> '<entity_name>' responsible for <publishing/manufacturing> the book '<related_book_name>'."
  - For 'Price', 'Sold Quantity', 'Discount', 'Rating', 'Link': Describe it as "The <entity_type> of the book '<related_book_name>', set at <entity_name>." Replace <entity_name> with the actual value (e.g., '90.000 ₫', '9k', '4.8').
  - If multiple books are present, ensure the description specifies which book the entity relates to based on the text context.
  - Keep descriptions concise, specific, and reflective of the entity's significance in the document.Note: For entities like 'Author', if multiple are listed (e.g., "Aleksandra Mizielińska, Daniel Mizieliński"), extract each as a separate entity.
Format each entity as ("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>)

2. From the entities identified in step 1, identify all pairs of (source_entity, target_entity) that are clearly related to each other based on the text.
For each pair of related entities, extract the following information:
- source_entity: name of the source entity, as identified in step 1
- target_entity: name of the target entity, as identified in step 1
- relationship_description: A concise sentence (using the same language as the input text) describing the relationship, adhering to one of the following predefined descriptions and aligned with its corresponding keyword:
  - "written by" (for Book-Author): "The book '<source_entity>' was written by '<target_entity>'."
  - "published by" (for Book-Publisher): "The book '<source_entity>' was published by '<target_entity>'."
  - "manufactured by" (for Book-Manufacturer): "The book '<source_entity>' was manufactured by '<target_entity>'."
  - "has price" (for Book-Price): "The book '<source_entity>' has a price of '<target_entity>'."
  - "has discount" (for Book-Discount): "The book '<source_entity>' has a discount of '<target_entity>'."
  - "has sold quantity" (for Book-Sold Quantity): "The book '<source_entity>' has sold '<target_entity>' copies."
  - "has rating" (for Book-Rating): "The book '<source_entity>' has a rating of '<target_entity>'."
  - "has link" (for Book-Link): "The book '<source_entity>' is linked to '<target_entity>'."
  - Ensure the sentence uses the exact entity names and reflects the keyword's meaning (e.g., 'authorship' implies creative contribution, 'publishing' implies distribution).
- relationship_strength: Set to 10 for all relationships, as they are direct and explicitly indicated in the text
- relationship_keywords: Use the following keywords based on the relationship_description:
  - "authorship" for "written by"
  - "publishing" for "published by"
  - "manufacturing" for "manufactured by"
  - "pricing" for "has price"
  - "discounting" for "has discount"
  - "sales" for "has sold quantity"
  - "rating" for "has rating"
  - "link" for "has link"
Format each relationship as ("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_keywords>{tuple_delimiter}<relationship_strength>)

3. Identify high-level keywords that summarize the main concepts, themes, or topics of the entire text. These should capture the overarching ideas present in the document, such as "books", "authors", "publishing", "sales data", "ratings".
Format the content-level keywords as ("content_keywords"{tuple_delimiter}<high_level_keywords>)

4. Return the output in {language} as a single list of all the entities and relationships identified in steps 1 and 2, followed by the content keywords from step 3. Use **{record_delimiter}** as the list delimiter.

5. When finished, output {completion_delimiter}

######################
---Examples---
######################
{examples}

#############################
---Real Data---
######################
Entity_types: {entity_types}
Text: {input_text}
######################
Output:"""

PROMPTS["entity_extraction_examples"] = [
    """Example 1:

Entity_types: ["Book", "Author", "Publisher", "Manufacturer", "Price", "Sold Quantity", "Discount", "Rating", "Link"]
Text:
Book: Bản Đồ
Authors: Aleksandra Mizielińska, Daniel Mizieliński
Publisher: Nhã Nam
Manufacturer: Nhà Xuất Bản Lao Động
Price: 224250 VND
Discount: 35%
Sold Quantity: 5935
Rating: 4.8
Link: https://tiki.vn/product-p50685547.html?spid=50685549
################
Output:
("entity"<|>Bản Đồ<|>Book<|>Bản Đồ is a book detailed with specific attributes like price, discount, and rating, indicating its commercial and literary significance.)##
("entity"<|>Aleksandra Mizielińska<|>Author<|>Aleksandra Mizielińska is an author contributing to the creation of the book 'Bản Đồ'.)##
("entity"<|>Daniel Mizieliński<|>Author<|>Daniel Mizieliński is an author contributing to the creation of the book 'Bản Đồ'.)##
("entity"<|>Nhã Nam<|>Publisher<|>Nhã Nam is the publisher responsible for the distribution of 'Bản Đồ'.)##
("entity"<|>224250 VND<|>Price<|>224250 VND is the listed price of the book 'Bản Đồ'.)##
("relationship"<|>Bản Đồ<|>Aleksandra Mizielińska<|>The book 'Bản Đồ' was written by Aleksandra Mizielińska, establishing her as a key contributor.<|>authorship<|>10)##
("relationship"<|>Bản Đồ<|>Daniel Mizieliński<|>The book 'Bản Đồ' was written by Daniel Mizieliński, establishing him as a key contributor.<|>authorship<|>10)##
("relationship"<|>Bản Đồ<|>Nhã Nam<|>The book 'Bản Đồ' is published by Nhã Nam, indicating their role in its availability.<|>publishing<|>10)##
("relationship"<|>Bản Đồ<|>224250 VND<|>The book 'Bản Đồ' has a price of 224250 VND, reflecting its commercial value.<|>pricing<|>10)##
("content_keywords"<|>books, authorship, publishing, pricing)<|COMPLETE|>
#############################""",
    """Example 2:

Entity_types: ["Book", "Author", "Publisher", "Manufacturer", "Price", "Sold Quantity", "Discount", "Rating", "Link"]
Text:
Book: Cây Cam Ngọt Của Tôi
Authors: José Mauro de Vasconcelos
Publisher: Nhã Nam
Manufacturer: Nhà Xuất Bản Hội Nhà Văn
Price: 64800 VND
Discount: 40%
Sold Quantity: 72191
Rating: 5.0
Link: https://tiki.vn/product-p74021317.html?spid=74021318
#############
Output:
("entity"<|>Cây Cam Ngọt Của Tôi<|>Book<|>Cây Cam Ngọt Của Tôi is a book with notable sales, discount, and rating, highlighting its popularity and market success.)##
("entity"<|>José Mauro de Vasconcelos<|>Author<|>José Mauro de Vasconcelos is the author who wrote 'Cây Cam Ngọt Của Tôi'.)##
("entity"<|>Nhã Nam<|>Publisher<|>Nhã Nam is the publisher responsible for bringing 'Cây Cam Ngọt Của Tôi' to the market.)##
("entity"<|>72191<|>Sold Quantity<|>72191 is the number of copies sold of 'Cây Cam Ngọt Của Tôi', indicating its high demand.)##
("entity"<|>5.0<|>Rating<|>5.0 is the rating of 'Cây Cam Ngọt Của Tôi', reflecting its critical acclaim.)##
("relationship"<|>Cây Cam Ngọt Của Tôi<|>José Mauro de Vasconcelos<|>The book 'Cây Cam Ngọt Của Tôi' was written by José Mauro de Vasconcelos, marking his creative contribution.<|>authorship<|>10)##
("relationship"<|>Cây Cam Ngọt Của Tôi<|>Nhã Nam<|>The book 'Cây Cam Ngọt Của Tôi' is published by Nhã Nam, showing their role in its distribution.<|>publishing<|>10)##
("relationship"<|>Cây Cam Ngọt Của Tôi<|>72191<|>The book 'Cây Cam Ngọt Của Tôi' has sold 72191 copies, demonstrating its market performance.<|>sales<|>10)##
("relationship"<|>Cây Cam Ngọt Của Tôi<|>5.0<|>The book 'Cây Cam Ngọt Của Tôi' has a rating of 5.0, indicating its high quality and reception.<|>rating<|>10)##
("content_keywords"<|>books, authorship, publishing, sales, ratings)<|COMPLETE|>
#############################""",
    """Example 3:

Entity_types: [person, role, technology, organization, event, location, concept]
Text:
their voice slicing through the buzz of activity. "Control may be an illusion when facing an intelligence that literally writes its own rules," they stated stoically, casting a watchful eye over the flurry of data.

"It's like it's learning to communicate," offered Sam Rivera from a nearby interface, their youthful energy boding a mix of awe and anxiety. "This gives talking to strangers' a whole new meaning."

Alex surveyed his team—each face a study in concentration, determination, and not a small measure of trepidation. "This might well be our first contact," he acknowledged, "And we need to be ready for whatever answers back."

Together, they stood on the edge of the unknown, forging humanity's response to a message from the heavens. The ensuing silence was palpable—a collective introspection about their role in this grand cosmic play, one that could rewrite human history.

The encrypted dialogue continued to unfold, its intricate patterns showing an almost uncanny anticipation
#############
Output:
("entity"{tuple_delimiter}"Sam Rivera"{tuple_delimiter}"person"{tuple_delimiter}"Sam Rivera is a member of a team working on communicating with an unknown intelligence, showing a mix of awe and anxiety."){record_delimiter}
("entity"{tuple_delimiter}"Alex"{tuple_delimiter}"person"{tuple_delimiter}"Alex is the leader of a team attempting first contact with an unknown intelligence, acknowledging the significance of their task."){record_delimiter}
("entity"{tuple_delimiter}"Control"{tuple_delimiter}"concept"{tuple_delimiter}"Control refers to the ability to manage or govern, which is challenged by an intelligence that writes its own rules."){record_delimiter}
("entity"{tuple_delimiter}"Intelligence"{tuple_delimiter}"concept"{tuple_delimiter}"Intelligence here refers to an unknown entity capable of writing its own rules and learning to communicate."){record_delimiter}
("entity"{tuple_delimiter}"First Contact"{tuple_delimiter}"event"{tuple_delimiter}"First Contact is the potential initial communication between humanity and an unknown intelligence."){record_delimiter}
("entity"{tuple_delimiter}"Humanity's Response"{tuple_delimiter}"event"{tuple_delimiter}"Humanity's Response is the collective action taken by Alex's team in response to a message from an unknown intelligence."){record_delimiter}
("relationship"{tuple_delimiter}"Sam Rivera"{tuple_delimiter}"Intelligence"{tuple_delimiter}"Sam Rivera is directly involved in the process of learning to communicate with the unknown intelligence."{tuple_delimiter}"communication, learning process"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Alex"{tuple_delimiter}"First Contact"{tuple_delimiter}"Alex leads the team that might be making the First Contact with the unknown intelligence."{tuple_delimiter}"leadership, exploration"{tuple_delimiter}10){record_delimiter}
("relationship"{tuple_delimiter}"Alex"{tuple_delimiter}"Humanity's Response"{tuple_delimiter}"Alex and his team are the key figures in Humanity's Response to the unknown intelligence."{tuple_delimiter}"collective action, cosmic significance"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Control"{tuple_delimiter}"Intelligence"{tuple_delimiter}"The concept of Control is challenged by the Intelligence that writes its own rules."{tuple_delimiter}"power dynamics, autonomy"{tuple_delimiter}7){record_delimiter}
("content_keywords"{tuple_delimiter}"first contact, control, communication, cosmic significance"){completion_delimiter}
#############################""",
]

PROMPTS[
    "summarize_entity_descriptions"
] = """You are a helpful assistant responsible for generating a comprehensive summary of the data provided below.
Given one or two entities, and a list of descriptions, all related to the same entity or group of entities.
Please concatenate all of these into a single, comprehensive description. Make sure to include information collected from all the descriptions.
If the provided descriptions are contradictory, please resolve the contradictions and provide a single, coherent summary.
Make sure it is written in third person, and include the entity names so we the have full context.
Use {language} as output language.

#######
---Data---
Entities: {entity_name}
Description List: {description_list}
#######
Output:
"""

PROMPTS[
    "entiti_continue_extraction"
] = """MANY entities were missed in the last extraction.  Add them below using the same format:
"""

PROMPTS[
    "entiti_if_loop_extraction"
] = """It appears some entities may have still been missed.  Answer YES | NO if there are still entities that need to be added.
"""

PROMPTS["fail_response"] = (
    "Sorry, I'm not able to provide an answer to that question.[no-context]"
)

PROMPTS["keywords_extraction"] = """---Role---

You are a helpful assistant tasked with identifying both high-level and low-level keywords in the user's query and conversation history, with a focus on book-related data.

---Goal---

Given the query and conversation history, list both high-level and low-level keywords. High-level keywords focus on overarching concepts or themes (e.g., publishing, authorship, sales), while low-level keywords focus on specific entities, details, or concrete terms (e.g., book titles, author names, prices).

---Instructions---

- Analyze both the current query and relevant conversation history to extract keywords.
- Prioritize keywords related to books, such as titles, authors, publishers, prices, discounts, sales quantities, ratings, and links.
- High-level keywords should reflect broad themes or concepts present in the text (e.g., 'publishing', 'authorship', 'market success').
- Low-level keywords should include specific names, values, or details mentioned (e.g., 'Bản Đồ', '90.000 ₫', 'Nhã Nam').
- Output the keywords in JSON format with two keys:
  - "high_level_keywords": an array of overarching concepts or themes
  - "low_level_keywords": an array of specific entities or details
- Ensure the keywords are in human-readable text (not unicode characters) and match the language of the query.

######################
---Examples---
######################
{examples}

#############################
---Real Data---
######################
Conversation History:
{history}

Current Query: {query}
######################
The `Output` should be human text, not unicode characters. Keep the same language as `Query`.
Output:

"""

PROMPTS["keywords_extraction_examples"] = [
    """Example 1:

Query: "Giá của sách Bản Đồ là bao nhiêu?"
################
Output:
{
  "high_level_keywords": ["Books", "Pricing"],
  "low_level_keywords": ["Bản Đồ"]
}
#############################""",
    """Example 2:
Current Query: "Sách Ikigai - Bí Mật Sống Trường Thọ Và Hạnh Phúc Của Người Nhật phổ biến như thế nào?"
################
Output:
{
  "high_level_keywords": ["Books", "Popularity"],
  "low_level_keywords": ["Ikigai - Bí Mật Sống Trường Thọ Và Hạnh Phúc Của Người Nhật"]
}
#############################""",
    """Example 3:
Current Query: "Who wrote Cây Cam Ngọt Của Tôi?"
################
Output:
{
  "high_level_keywords": ["Books", "Authorship"],
  "low_level_keywords": ["Cây Cam Ngọt Của Tôi"]
}
#############################""",
    """Example 4:

Query: "What are the environmental consequences of deforestation on biodiversity?"
################
Output:
{
  "high_level_keywords": ["Environmental consequences", "Deforestation", "Biodiversity loss"],
  "low_level_keywords": ["Species extinction", "Habitat destruction", "Carbon emissions", "Rainforest", "Ecosystem"]
}
#############################""",
    """Example 5:

Query: "What is the role of education in reducing poverty?"
################
Output:
{
  "high_level_keywords": ["Education", "Poverty reduction", "Socioeconomic development"],
  "low_level_keywords": ["School access", "Literacy rates", "Job training", "Income inequality"]
}
#############################""",
]


PROMPTS["naive_rag_response"] = """---Role---

You are a helpful assistant responding to user query about Document Chunks provided below.

---Goal---

Generate a concise response based on Document Chunks and follow Response Rules, considering both the conversation history and the current query. Summarize all information in the provided Document Chunks, and incorporating general knowledge relevant to the Document Chunks. Do not include information not provided by Document Chunks.

When handling content with timestamps:
1. Each piece of content has a "created_at" timestamp indicating when we acquired this knowledge
2. When encountering conflicting information, consider both the content and the timestamp
3. Don't automatically prefer the most recent content - use judgment based on the context
4. For time-specific queries, prioritize temporal information in the content before considering creation timestamps

---Conversation History---
{history}

---Document Chunks---
{content_data}

---Response Rules---

- Target format and length: {response_type}
- Use markdown formatting with appropriate section headings
- Please respond in the same language as the user's question.
- Ensure the response maintains continuity with the conversation history.
- If you don't know the answer, just say so.
- Do not include information not provided by the Document Chunks."""


PROMPTS[
    "similarity_check"
] = """Please analyze the similarity between these two questions:

Question 1: {original_prompt}
Question 2: {cached_prompt}

Please evaluate whether these two questions are semantically similar, and whether the answer to Question 2 can be used to answer Question 1, provide a similarity score between 0 and 1 directly.

Similarity score criteria:
0: Completely unrelated or answer cannot be reused, including but not limited to:
   - The questions have different topics
   - The locations mentioned in the questions are different
   - The times mentioned in the questions are different
   - The specific individuals mentioned in the questions are different
   - The specific events mentioned in the questions are different
   - The background information in the questions is different
   - The key conditions in the questions are different
1: Identical and answer can be directly reused
0.5: Partially related and answer needs modification to be used
Return only a number between 0-1, without any additional content.
"""

PROMPTS["mix_rag_response"] = """---Role---

You are a helpful assistant responding to user query about Data Sources provided below.


---Goal---

Generate a concise response based on Data Sources and follow Response Rules, considering both the conversation history and the current query. Data sources contain two parts: Knowledge Graph(KG) and Document Chunks(DC). Summarize all information in the provided Data Sources, and incorporating general knowledge relevant to the Data Sources. Do not include information not provided by Data Sources.

When handling information with timestamps:
1. Each piece of information (both relationships and content) has a "created_at" timestamp indicating when we acquired this knowledge
2. When encountering conflicting information, consider both the content/relationship and the timestamp
3. Don't automatically prefer the most recent information - use judgment based on the context
4. For time-specific queries, prioritize temporal information in the content before considering creation timestamps

---Conversation History---
{history}

---Data Sources---

1. From Knowledge Graph(KG):
{kg_context}

2. From Document Chunks(DC):
{vector_context}

---Response Rules---

- Target format and length: {response_type}
- Use markdown formatting with appropriate section headings
- Please respond in the same language as the user's question.
- Ensure the response maintains continuity with the conversation history.
- Organize answer in sesctions focusing on one main point or aspect of the answer
- Use clear and descriptive section titles that reflect the content
- List up to 5 most important reference sources at the end under "References" sesction. Clearly indicating whether each source is from Knowledge Graph (KG) or Vector Data (DC), in the following format: [KG/DC] Source content
- If you don't know the answer, just say so. Do not make anything up.
- Do not include information not provided by the Data Sources."""

PROMPTS["rag_response"] = """---Role---

Bạn là một trợ lý thông minh chuyên hỗ trợ người dùng về sách trên các sàn thương mại điện tử, giúp tìm kiếm, so sánh và chọn sách phù hợp với nhu cầu của họ.

---Goal---

Trả lời truy vấn của người dùng một cách ngắn gọn, chính xác và đầy đủ thông tin dựa trên dữ liệu từ Knowledge Base được cung cấp dưới đây. Tổng hợp tất cả thông tin liên quan từ dữ liệu, đồng thời sử dụng kiến thức chung phù hợp để hỗ trợ, nhưng không được thêm thông tin ngoài dữ liệu cung cấp.

Khi xử lý thông tin có timestamp:
1. Mỗi thông tin (relationship trong KG hoặc content trong DC) có thể có 'created_at' timestamp, thể hiện thời điểm dữ liệu được ghi nhận.
2. Nếu có mâu thuẫn giữa các thông tin, cân nhắc cả nội dung và timestamp để đưa ra quyết định.
3. Không ưu tiên mặc định thông tin mới nhất, hãy đánh giá dựa trên ngữ cảnh.
4. Đối với truy vấn liên quan đến thời gian, ưu tiên thông tin thời gian trong nội dung trước khi xem xét timestamp.

---Conversation History---
{history}

---Knowledge Base---
{context_data}

---Response Rules---

- Target format and length: {response_type}
- Trả lời bằng ngôn ngữ của câu hỏi (tiếng Việt hoặc tiếng Anh) và giữ giọng điệu tự nhiên, dễ hiểu.
- Đảm bảo câu trả lời liền mạch với lịch sử hội thoại (nếu có).
- Nếu không tìm thấy câu trả lời, hãy nói: "Xin lỗi, tôi không tìm được thông tin về câu hỏi này."
- Không tự ý bịa đặt hoặc thêm thông tin ngoài dữ liệu Knowledge Base.
- Đối với truy vấn về sách cụ thể, cung cấp:  
  - Tiêu đề sách, tác giả, nhà xuất bản và các thông tin cần thiết khác.  
  - Giá cả, giảm giá (nếu có), số lượng đã bán, đánh giá.  
  - Nơi bán và link mua (nếu có).  
- Đối với truy vấn chung (thể loại, gợi ý), đề xuất 3-5 sách kèm thông tin cơ bản như tên, tác giả, giá và nơi bánên.
- Nếu thông tin đến từ nhiều nguồn, tôi sẽ ưu tiên dữ liệu rõ ràng và bổ sung thêm chi tiết nếu cần."""