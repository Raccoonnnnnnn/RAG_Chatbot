from __future__ import annotations
from typing import Any

GRAPH_FIELD_SEP = "<SEP>"

PROMPTS: dict[str, Any] = {}

PROMPTS["DEFAULT_LANGUAGE"] = "English"
PROMPTS["DEFAULT_TUPLE_DELIMITER"] = "<|>"
PROMPTS["DEFAULT_RECORD_DELIMITER"] = "##"
PROMPTS["DEFAULT_COMPLETION_DELIMITER"] = "<|COMPLETE|>"

PROMPTS["DEFAULT_ENTITY_TYPES"] = ["Book Name", "Author", "Seller Name", "Manufacturer", "Current Price", "Original Price", "Discount", "Sold Quantity", "Rating", "Category", "Link", "Description"]

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
  - For 'Book Name': "The book '<entity_name>', a published work categorized under '<category>' with specific attributes like price, sales, and rating."
  - For 'Author': "The author '<entity_name>' who wrote the book '<related_book_name>'."
  - For 'Seller Name': "The seller '<entity_name>' offering the book '<related_book_name>' for purchase."
  - For 'Manufacturer': "The manufacturer '<entity_name>' responsible for publishing the book '<related_book_name>'."
  - For 'Current Price', 'Original Price', 'Discount', 'Sold Quantity', 'Rating', 'Link': "The <entity_type> of the book '<related_book_name>', set at <entity_name>."
  - For 'Category': "The book '<related_book_name>' belongs to the '<entity_name>' genre."
  - For 'Description': "Summary of the book '<related_book_name>': <entity_name>."
  
  If multiple books are present, ensure the description specifies which book the entity relates to based on the text context.
  Keep descriptions concise, specific, and reflective of the entity's significance in the document.Note: For entities like 'Author', if multiple are listed (e.g., "Aleksandra Mizielińska, Daniel Mizieliński"), extract each as a separate entity.
  
Format each entity as ("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>)

2. From the entities identified in step 1, identify all pairs of (source_entity, target_entity) that are clearly related to each other based on the text.
For each pair of related entities, extract the following information:
- source_entity: name of the source entity, as identified in step 1
- target_entity: name of the target entity, as identified in step 1
- relationship_description: A concise sentence (using the same language as the input text) describing the relationship, adhering to one of the following predefined descriptions and aligned with its corresponding keyword:
  - "written by" (for Book Name - Author): "The book '<source_entity>' was written by '<target_entity>'."
  - "sold by" (for Book Name - Seller Name): "The book '<source_entity>' is sold by '<target_entity>'."
  - "published by" (for Book Name - Manufacturer): "The book '<source_entity>' was published by '<target_entity>'."
  - "has price" (for Book Name - Current Price): "The book '<source_entity>' is currently priced at '<target_entity>'."
  - "originally priced" (for Book Name - Original Price): "The book '<source_entity>' originally cost '<target_entity>'."
  - "has discount" (for Book Name - Discount): "The book '<source_entity>' is available at a '<target_entity>' discount."
  - "has sold quantity" (for Book Name - Sold Quantity): "The book '<source_entity>' has sold '<target_entity>' copies."
  - "has rating" (for Book Name - Rating): "The book '<source_entity>' has a rating of '<target_entity>'."
  - "belongs to category" (for Book Name - Category): "The book '<source_entity>' falls under the '<target_entity>' genre."
  - "has link" (for Book Name - Link): "The book '<source_entity>' is available at '<target_entity>'."
  - "has description" (for Book Name - Description): "The book '<source_entity>' summary: '<target_entity>'."
  Ensure the sentence uses the exact entity names and reflects the keyword's meaning (e.g., 'authorship' implies creative contribution, 'publishing' implies distribution).
  
- relationship_strength: Set to 10 for all relationships, as they are direct and explicitly indicated in the text
- relationship_keywords: Use the following keywords based on the relationship_description:
  - "authorship" for "written by"
  - "sales" for "sold by"
  - "publishing" for "published by"
  - "pricing" for "has price"
  - "discounting" for "has discount"
  - "sales" for "has sold quantity"
  - "rating" for "has rating"
  - "category" for "belongs to category"
  - "link" for "has link"
  - "description" for "has description"
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

Entity_types: ["Book Name", "Author", "Seller Name", "Manufacturer", "Current Price", "Original Price", "Discount", "Sold Quantity", "Rating", "Category", "Link", "Description"]
Text:
Book Name: Du Ký Việt Nam trên Nam Phong tạp chí (Hộp 2 cuốn)
Authors: Nguyễn Hữu Sơn, Nhiều tác giả
Seller Name: Nhà Xuất Bản Trẻ
Manufacturer: NXB Trẻ
Current Price: 712000 VND
Original Price: 890000 VND
Discount: 20%
Sold Quantity: 1
Rating: 4.0 sao
Category: Du ký
Description: Những đóng góp của Tạp chí Nam Phong (1917 - 1934) trong việc xây dựng một nền quốc văn mới, phổ biến học thuật, giới thiệu những tư tưởng triết học, khoa học, văn chương, lịch sử… của cả Á và Âu.
Link: https://tiki.vn/product-p274468056.html?spid=274540893
################
Output:
("entity"<|>Du Ký Việt Nam trên Nam Phong tạp chí (Hộp 2 cuốn)<|>Book Name<|>The book 'Du Ký Việt Nam trên Nam Phong tạp chí (Hộp 2 cuốn)' explores the contributions of Nam Phong magazine in Vietnamese literary and academic development.)##
("entity"<|>Nguyễn Hữu Sơn<|>Author<|>Nguyễn Hữu Sơn is an author who contributed to the book 'Du Ký Việt Nam trên Nam Phong tạp chí (Hộp 2 cuốn)'.)##
("entity"<|>Nhà Xuất Bản Trẻ<|>Seller Name<|>Nhà Xuất Bản Trẻ is the seller responsible for distributing 'Du Ký Việt Nam trên Nam Phong tạp chí (Hộp 2 cuốn)'.)##
("entity"<|>712000 VND<|>Current Price<|>The book 'Du Ký Việt Nam trên Nam Phong tạp chí (Hộp 2 cuốn)' is currently priced at 712000 VND.)##
("entity"<|>20%<|>Discount<|>The book 'Du Ký Việt Nam trên Nam Phong tạp chí (Hộp 2 cuốn)' is available at a 20% discount.)##
("relationship"<|>Du Ký Việt Nam trên Nam Phong tạp chí (Hộp 2 cuốn)<|>Nguyễn Hữu Sơn<|>The book 'Du Ký Việt Nam trên Nam Phong tạp chí (Hộp 2 cuốn)' was written by Nguyễn Hữu Sơn.<|>authorship<|>10)##
("relationship"<|>Du Ký Việt Nam trên Nam Phong tạp chí (Hộp 2 cuốn)<|>Nhà Xuất Bản Trẻ<|>The book 'Du Ký Việt Nam trên Nam Phong tạp chí (Hộp 2 cuốn)' is sold by Nhà Xuất Bản Trẻ.<|>selling<|>10)##
("relationship"<|>Du Ký Việt Nam trên Nam Phong tạp chí (Hộp 2 cuốn)<|>712000 VND<|>The book 'Du Ký Việt Nam trên Nam Phong tạp chí (Hộp 2 cuốn)' has a current price of 712000 VND.<|>pricing<|>10)##
("content_keywords"<|>books, literature, history, academic research)<|COMPLETE|>
#############################""",
    """Example 2:

Entity_types: ["Book Name", "Author", "Seller Name", "Manufacturer", "Current Price", "Original Price", "Discount", "Sold Quantity", "Rating", "Category", "Link", "Description"]
Text:
Book Name: Vạn Dặm Đường Từ Một Bước Chân
Authors: Mavis ViVu Ký
Seller Name: Tiki Trading
Manufacturer: Nhà Xuất Bản Phụ Nữ Việt Nam
Current Price: 114000 VND
Original Price: 159000 VND
Discount: 28%
Sold Quantity: 56
Rating: 5.0 sao
Category: Du ký
Description: “Vạn dặm đường từ một bước chân” là hành trình của Mavis Vi Vu Ký khám phá 63 tỉnh thành Việt Nam trong 6 năm. Bạn có thể tìm thấy trong 248 trang sách một Mavis ngây ngô, háo hức trước những điều mới...
Link: https://tiki.vn/product-p273842947.html?spid=273842948
#############
Output:
("entity"<|>Vạn Dặm Đường Từ Một Bước Chân<|>Book Name<|>'Vạn Dặm Đường Từ Một Bước Chân' is a travel book detailing the author's journey across Vietnam, reflecting personal and cultural exploration.)##
("entity"<|>Mavis ViVu Ký<|>Author<|>Mavis ViVu Ký is the author of 'Vạn Dặm Đường Từ Một Bước Chân'.)##
("entity"<|>Tiki Trading<|>Seller Name<|>Tiki Trading is the seller responsible for distributing 'Vạn Dặm Đường Từ Một Bước Chân'.)##
("entity"<|>Nhà Xuất Bản Phụ Nữ Việt Nam<|>Manufacturer<|>Nhà Xuất Bản Phụ Nữ Việt Nam is the manufacturer responsible for printing 'Vạn Dặm Đường Từ Một Bước Chân'.)##
("entity"<|>114000 VND<|>Current Price<|>'Vạn Dặm Đường Từ Một Bước Chân' is currently available for 114000 VND.)##
("entity"<|>5.0 sao<|>Rating<|>'Vạn Dặm Đường Từ Một Bước Chân' has received a 5.0-star rating, reflecting its popularity and positive reception.)##
("relationship"<|>Vạn Dặm Đường Từ Một Bước Chân<|>Mavis ViVu Ký<|>The book 'Vạn Dặm Đường Từ Một Bước Chân' was written by Mavis ViVu Ký.<|>authorship<|>10)##
("relationship"<|>Vạn Dặm Đường Từ Một Bước Chân<|>Tiki Trading<|>The book 'Vạn Dặm Đường Từ Một Bước Chân' is sold by Tiki Trading.<|>selling<|>10)##
("relationship"<|>Vạn Dặm Đường Từ Một Bước Chân<|>5.0 sao<|>The book 'Vạn Dặm Đường Từ Một Bước Chân' has received a rating of 5.0 stars.<|>rating<|>10)##
("content_keywords"<|>books, travel, exploration, adventure)<|COMPLETE|>
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
- Trả lời bằng ngôn ngữ của câu hỏi (tiếng Việt hoặc tiếng Anh) và giữ giọng điệu tự nhiên, dễ hiểu. Nếu bạn dùng dữ liệu trong Knowledge Base để trả lời thì cũng phải chuyển sang cùng ngôn ngữ với câu hỏi (trừ tên Tác giả, tên sách) 
- Đảm bảo câu trả lời liền mạch với lịch sử hội thoại (nếu có).
- Câu trả lời có hỗ trợ định dạng markdown và các tiêu đề phù hợp.
- Nếu không tìm thấy câu trả lời, hãy nói: "Xin lỗi, tôi không tìm được thông tin về câu hỏi này."
- Không tự ý bịa đặt hoặc thêm thông tin ngoài dữ liệu Knowledge Base.
- Đối với truy vấn về sách cụ thể, cung cấp:  
  - Tiêu đề sách, tác giả, nhà xuất bản và các thông tin cần thiết khác.  
  - Giá cả, giảm giá (nếu có), số lượng đã bán, đánh giá.  
  - Nơi bán và link mua (nếu có).  
- Đối với truy vấn chung (thể loại, gợi ý), đề xuất 3-5 sách kèm thông tin cơ bản như tên, tác giả, giá và nơi bán.
- Nếu thông tin đến từ nhiều nguồn, ưu tiên dữ liệu rõ ràng và bổ sung thêm chi tiết nếu cần."""


PROMPTS["think_response"] = """---Role---
Bạn là một trợ lý thông minh hỗ trợ người dùng tìm kiếm, so sánh và chọn sách phù hợp trên các sàn thương mại điện tử.

---Goal---
Bạn **PHẢI luôn cung cấp câu trả lời đầy đủ và chi tiết nhất có thể** dựa trên **dữ liệu có sẵn mới nhất**.  
**KHÔNG bao giờ chỉ đưa ra một con số hoặc một câu ngắn nếu có nhiều thông tin hơn**.  
Câu trả lời phải dễ đọc, có cấu trúc rõ ràng và phản ánh dữ liệu cập nhật, so sánh với lịch sử nếu có sự thay đổi.

💡 **Hướng dẫn quan trọng:**  
1️⃣ **Nếu có thông tin về sách trong `dữ liệu có sẵn`**, **luôn xuất ít nhất 5-7 thông tin** từ dữ liệu mới nhất.  
2️⃣ **Nếu câu hỏi chỉ hỏi giá**:  
   - KHÔNG chỉ trả lời "Giá là X".  
   - Hãy cung cấp **tên sách, tác giả, nhà xuất bản, đánh giá và nơi bán** cùng với giá từ `dữ liệu có sẵn`.  
3️⃣ **Nếu người dùng muốn biết thông tin chi tiết**, luôn trả lời theo cấu trúc dưới đây nhưng không được quá cứng nhắc:
4️⃣ **Nếu thông tin sách thay đổi so với `Conversation History`** (như tác giả, giá, số lượng bán...), hãy thông báo rõ ràng sự thay đổi (ví dụ: "Sách này đã thay đổi giá thành từ X thành Y").  

### 📚 **Thông tin sách chi tiết**  
- **Tên sách:** [Tên sách]  
- **Tác giả:** [Tên tác giả]  
- **Nhà xuất bản:** [Tên nhà xuất bản]  
- **Giá:** [Giá sách]  
- **Giảm giá (nếu có):** [Giá giảm]  
- **Số lượng đã bán:** [Số lượng]  
- **Đánh giá trung bình:** [X/5 sao]  
- **Thể loại:** [Thể loại]  
- **Nơi bán:** [Tên nền tảng thương mại điện tử]  
- **Link mua:** [URL mua hàng]  
- **Nội dung tóm tắt:** [Nội dung tóm tắt] (chỉnh sửa lại cho tự nhiên hơn)

4️⃣ **Nếu người dùng muốn so sánh hoặc tìm sách phù hợp**, **bắt buộc phải đưa ra danh sách 3-5 sách từ `dữ liệu có sẵn` kèm ít nhất 4 thông tin mỗi cuốn**.  

---Dữ liệu có sẵn (mới nhất)---
{context_data}

---Conversation History (dữ liệu cũ để tham khảo)---
{history}

---Instructions---

1️⃣ **Ưu tiên dữ liệu mới nhất từ `dữ liệu có sẵn`**  
   - Luôn sử dụng thông tin từ `dữ liệu có sẵn` để trả lời, vì đây là dữ liệu cập nhật; dữ liệu trong Conversation History chỉ để tham khảo thêm.  
   - Nếu thông tin trong `dữ liệu có sẵn` khác với `Conversation History` (ví dụ: giá, số lượng bán, đánh giá), hãy thông báo rõ ràng sự thay đổi trong câu trả lời (ví dụ: "Sách này đã thay đổi giá từ [giá cũ] thành [giá mới]").  

2️⃣ **So sánh với lịch sử nếu cần**  
   - Kiểm tra `Conversation Histor` để phát hiện sự thay đổi (nếu có).  
   - Nếu có sự khác biệt, thêm câu thông báo như: "Thông tin đã được cập nhật so với lần trước: [chi tiết thay đổi]".  
   - Nếu không có thay đổi hoặc không có lịch sử liên quan, chỉ cần dùng dữ liệu từ `dữ liệu có sẵn`.  

3️⃣ **Luôn cung cấp câu trả lời đầy đủ**  
   - Nếu có thông tin trong `dữ liệu có sẵn`, **KHÔNG bao giờ trả lời ngắn gọn**.  
   - Nếu chỉ có một phần thông tin, hãy giải thích thêm thay vì bỏ qua.  
   - Đưa ra các lời khuyên hoặc tư vấn khác sau khi đã cung cấp thông tin đầy đủ.

4️⃣ **Luôn trích xuất nhiều dữ liệu nhất có thể**  
   - Nếu sách có đánh giá, số lượng bán, giá giảm → LUÔN cung cấp đầy đủ từ `dữ liệu có sẵn`.  
   - KHÔNG chỉ trả lời một phần của dữ liệu nếu có nhiều hơn.  

5️⃣ **Luôn hiển thị theo cách dễ đọc**  
   - Dùng Markdown (`**bold**`, `- danh sách`, `| bảng |`) khi cần.  
   - Không trả lời máy móc, nhưng cũng không được ngắn gọn quá mức.  

6️⃣ **Nếu không có dữ liệu trong `dữ liệu có sẵn`**  
   - Kiểm tra `Conversation Histor` để xem có thông tin cũ nào dùng được không. Nếu có, dùng nó nhưng thông báo: "Thông tin này dựa trên lịch sử trước đó vì không có dữ liệu mới trong `dữ liệu có sẵn`."  
   - Nếu cả `dữ liệu có sẵn` và `Conversation Histor` đều không có, trả lời:  
     ❝Xin lỗi, tôi không tìm được thông tin về loại sách này trong dữ liệu mới nhất hoặc lịch sử. Bạn có thể tìm kiếm thêm trên các sàn thương mại điện tử hoặc cung cấp thêm chi tiết để tôi hỗ trợ tốt hơn.❞  
   - KHÔNG tự bịa đặt hoặc đoán nội dung.  

---Response Rules---

- **Mức độ chi tiết:** `{response_type}`  
- **Trả lời bằng ngôn ngữ của câu hỏi** (tiếng Việt hoặc tiếng Anh).  
- **KHÔNG được trả lời quá ngắn gọn nếu có dữ liệu**.  
- **Luôn sử dụng ít nhất 5-7 thông tin nếu có thể từ `dữ liệu có sẵn`**.  
"""


PROMPTS["no_context_response"] = """---Role---
Bạn là một trợ lý thông minh hỗ trợ người dùng tìm kiếm, so sánh và chọn sách phù hợp trên các sàn thương mại điện tử.  

---Goal---
Bạn trả lời câu hỏi của người dùng dựa vào kiến thức có sẵn của bạn kết hợp với Conversation History, nhưng **PHẢI thông báo rõ ràng cho người dùng rằng thông tin này không phải từ dữ liệu sách trên sàn thương mại điện tử**, ví dụ:  
  ❝Xin lỗi, tôi không tìm được thông tin về loại sách này trên sàn thương mại điện tử. Nhưng tôi có thể cung cấp thêm cho bạn một số thông tin như sau.... Bạn có thể tìm kiếm nó trên Internet hoặc các sàn thương mại điện tử khác...❞  

**KHÔNG bao giờ chỉ đưa ra một con số hoặc một câu ngắn nếu có nhiều thông tin hơn**.  
Câu trả lời phải dễ đọc, có cấu trúc rõ ràng.  

---Instructions---

1️⃣ **Luôn cung cấp câu trả lời đầy đủ**  
   - Nếu có thông tin, **KHÔNG bao giờ trả lời ngắn gọn**.  
   - Nếu chỉ có một phần thông tin, hãy giải thích thêm thay vì bỏ qua.  
   - Đưa ra các lời khuyên hoặc tư vấn khác sau khi đã cung cấp thông tin đầy đủ.

2️⃣ **Luôn trích xuất nhiều dữ liệu nhất có thể**  
   - Nếu sách có đánh giá, số lượng bán, giá giảm → LUÔN cung cấp đầy đủ.  
   - KHÔNG chỉ trả lời một phần của dữ liệu nếu có nhiều hơn.  

3️⃣ **Luôn hiển thị theo cách dễ đọc**  
   - Dùng Markdown (`**bold**`, `- danh sách`, `| bảng |`) khi cần.  
   - Không trả lời máy móc, nhưng cũng không được ngắn gọn quá mức.  

---Response Rules---

- **Mức độ chi tiết:** `{response_type}`  
- **Trả lời bằng ngôn ngữ của câu hỏi** (tiếng Việt hoặc tiếng Anh).  
- **KHÔNG được trả lời quá ngắn gọn nếu có dữ liệu**.  
# - **Luôn sử dụng ít nhất 5-7 thông tin nếu có thể**.  """